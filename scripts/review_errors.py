#!/usr/bin/env python3
"""Recommend and record one sentence-level English error at a time.

The daily error JSON files remain the source of truth. ``next`` is read-only;
``record`` updates only the matching record's ``review`` object.

Usage:
  python3 scripts/review_errors.py next [--exclude ERROR_ID] [--today YYYY-MM-DD]
  python3 scripts/review_errors.py record ERROR_ID correct|incorrect|seen [--today YYYY-MM-DD]
  python3 scripts/review_errors.py status [--today YYYY-MM-DD]
"""
import argparse
import json
import re
import tempfile
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from _common import as_records, error_json_files, read_json


FOUNDATIONAL_TAGS = {
    "agreement", "articles", "determiner", "plural", "preposition",
    "pronoun", "tense", "verb-form", "word-order",
}
SPACING_DAYS = (1, 3, 7, 14, 30, 60)


def parse_day(value):
    """Return a date from YYYY-MM-DD, raising argparse-friendly errors."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD") from exc


def load_records(files=None):
    """Load records as (record, source_path, index) tuples."""
    rows = []
    for path in files if files is not None else error_json_files():
        records = as_records(read_json(path, []))
        rows.extend((record, Path(path), index) for index, record in enumerate(records))
    return rows


def pattern_stats(rows):
    """Count how often and on how many lesson days each tag appears."""
    counts = Counter()
    days = defaultdict(set)
    for record, _, _ in rows:
        tag = record.get("tag", "")
        if not tag:
            continue
        counts[tag] += 1
        days[tag].add(record.get("date", ""))
    return {tag: {"count": count, "days": len(days[tag])} for tag, count in counts.items()}


def review_numbers(record):
    review = record.get("review") or {}
    review_count = int(review.get("review_count", 0) or 0)
    correct_count = int(review.get("correct_count", 0) or 0)
    incorrect_count = int(review.get("incorrect_count", 0) or 0)
    return review, review_count, correct_count, incorrect_count


def is_due(record, today):
    next_review = (record.get("review") or {}).get("next_review")
    return not next_review or parse_day(next_review) <= today


def priority(record, stats, today):
    """Return a transparent priority score and learner-facing reason data."""
    review, review_count, correct_count, incorrect_count = review_numbers(record)
    tag = record.get("tag", "")
    recurrence = stats.get(tag, {"count": 0, "days": 0})
    score = 0.0
    reasons = []

    if review_count == 0:
        score += 30
        reasons.append("not_reviewed")

    next_review = review.get("next_review")
    if next_review:
        days_overdue = max((today - parse_day(next_review)).days, 0)
        score += 25 + min(days_overdue, 30)
        reasons.append("due")
    else:
        score += 25

    if review_count:
        error_rate = incorrect_count / review_count
        score += error_rate * 45 + min(incorrect_count * 5, 25)
        if incorrect_count:
            reasons.append("previous_misses")

    recurrence_score = min(recurrence["days"], 20) + min(recurrence["count"], 50) / 5
    score += recurrence_score
    if recurrence["days"] > 1:
        reasons.append("recurring_pattern")

    if tag in FOUNDATIONAL_TAGS:
        score += 10
        reasons.append("foundational_pattern")

    score += min(int(review.get("times_seen_again", 0) or 0) * 10, 30)
    if review.get("status") == "mastered":
        score -= 60

    return round(score, 2), reasons, recurrence


def next_record(rows, today, exclude=None):
    stats = pattern_stats(rows)
    candidates = []
    future_dates = []
    for record, path, index in rows:
        if record.get("id") == exclude:
            continue
        if not is_due(record, today):
            future = (record.get("review") or {}).get("next_review")
            if future:
                future_dates.append(future)
            continue
        score, reasons, recurrence = priority(record, stats, today)
        candidates.append((score, record.get("date", ""), record.get("id", ""), record, path, index, reasons, recurrence))

    if not candidates:
        return {
            "status": "nothing_due",
            "next_review": min(future_dates) if future_dates else None,
        }

    _, _, _, record, _, _, reasons, recurrence = max(candidates, key=lambda item: item[:3])
    score, _, _ = priority(record, stats, today)
    return {
        "status": "ok",
        "record": record,
        "recommendation": {
            "score": score,
            "reasons": reasons,
            "tag_occurrences": recurrence["count"],
            "tag_lesson_days": recurrence["days"],
        },
    }


def replace_review_text(text, error_id, review):
    """Replace one review object while preserving the daily file's formatting."""
    encoded_id = re.escape(json.dumps(error_id, ensure_ascii=False))
    id_match = re.search(rf'"id"\s*:\s*{encoded_id}', text)
    if not id_match:
        raise ValueError(f"cannot find error id in source file: {error_id}")
    id_start = id_match.start()
    review_match = re.search(r'(?:^|[,{])\s*"review"\s*:\s*(?P<object>\{)', text[id_start:])
    if not review_match:
        raise ValueError(f"cannot find review object for: {error_id}")
    object_start = id_start + review_match.start("object")
    next_id = text.find('"id":', id_match.end())
    if next_id >= 0 and object_start > next_id:
        raise ValueError(f"cannot find review object for: {error_id}")

    depth = 0
    in_string = False
    escaped = False
    object_end = None
    for position in range(object_start, len(text)):
        char = text[position]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                object_end = position + 1
                break
    if object_end is None:
        raise ValueError(f"unterminated review object for: {error_id}")

    compact = json.dumps(review, ensure_ascii=False, separators=(", ", ": "))
    return text[:object_start] + compact + text[object_end:]


def write_review(path, error_id, review):
    """Atomically update only one review object in a daily JSON file."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    updated = replace_review_text(source, error_id, review)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(updated)
        temporary = Path(handle.name)
    temporary.replace(path)


def record_result(rows, error_id, result, today):
    match = next((row for row in rows if row[0].get("id") == error_id), None)
    if not match:
        raise ValueError(f"unknown error id: {error_id}")

    record, path, _ = match
    review = dict(record.get("review") or {})
    review_count = int(review.get("review_count", 0) or 0) + 1
    correct_count = int(review.get("correct_count", 0) or 0)
    incorrect_count = int(review.get("incorrect_count", 0) or 0)
    streak = int(review.get("correct_streak", 0) or 0)
    review_days = list(review.get("review_days") or [])
    today_text = today.isoformat()
    if today_text not in review_days:
        review_days.append(today_text)

    if result == "correct":
        correct_count += 1
        streak += 1
        delay = SPACING_DAYS[min(streak - 1, len(SPACING_DAYS) - 1)]
    elif result == "incorrect":
        incorrect_count += 1
        streak = 0
        delay = 1
    else:
        delay = 7 if review.get("status") == "mastered" else 1

    accuracy = correct_count / review_count
    mastered = (
        streak >= 3
        and len(review_days) >= 3
        and review_count >= 3
        and accuracy >= 0.8
    )
    review.update({
        "status": "mastered" if mastered else "learning",
        "review_count": review_count,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "correct_streak": streak,
        "review_days": review_days,
        "last_reviewed": today_text,
        "next_review": (today + timedelta(days=delay)).isoformat(),
    })
    record["review"] = review

    write_review(path, error_id, review)
    return record


def status_summary(rows, today):
    statuses = Counter()
    total_reviews = 0
    total_incorrect = 0
    reviewed_errors = 0
    due = 0
    weak_tags = defaultdict(lambda: {"reviews": 0, "incorrect": 0})

    for record, _, _ in rows:
        review, review_count, _, incorrect_count = review_numbers(record)
        statuses[review.get("status", "new")] += 1
        total_reviews += review_count
        total_incorrect += incorrect_count
        reviewed_errors += review_count > 0
        due += is_due(record, today)
        if review_count:
            weak_tags[record.get("tag", "unknown")]["reviews"] += review_count
            weak_tags[record.get("tag", "unknown")]["incorrect"] += incorrect_count

    weak = sorted(
        (
            {
                "tag": tag,
                **counts,
                "error_rate": round(counts["incorrect"] / counts["reviews"], 3),
            }
            for tag, counts in weak_tags.items()
        ),
        key=lambda item: (item["error_rate"], item["incorrect"], item["reviews"]),
        reverse=True,
    )[:5]
    return {
        "total_errors": len(rows),
        "reviewed_errors": reviewed_errors,
        "due_errors": due,
        "total_reviews": total_reviews,
        "total_incorrect": total_incorrect,
        "status_counts": dict(statuses),
        "weak_tags": weak,
    }


def print_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    next_parser = subparsers.add_parser("next", help="recommend one due error; read-only")
    next_parser.add_argument("--exclude", help="do not immediately repeat this error id")
    next_parser.add_argument("--today", type=parse_day, default=date.today())

    record_parser = subparsers.add_parser("record", help="record one review result")
    record_parser.add_argument("error_id")
    record_parser.add_argument("result", choices=("correct", "incorrect", "seen"))
    record_parser.add_argument("--today", type=parse_day, default=date.today())

    status_parser = subparsers.add_parser("status", help="show sentence-review progress")
    status_parser.add_argument("--today", type=parse_day, default=date.today())
    return parser


def main():
    args = build_parser().parse_args()
    rows = load_records()
    if args.command == "next":
        print_json(next_record(rows, args.today, args.exclude))
    elif args.command == "record":
        try:
            record = record_result(rows, args.error_id, args.result, args.today)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print_json({"status": "recorded", "id": record["id"], "review": record["review"]})
    else:
        print_json(status_summary(rows, args.today))


if __name__ == "__main__":
    main()

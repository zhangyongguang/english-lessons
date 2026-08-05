#!/usr/bin/env python3
"""Validate the error log and vocabulary store against their schemas (read-only).

Checks the controlled vocabulary, required fields, id/word uniqueness, and date
format. Exits 0 if everything is valid (warnings allowed), 1 if there are errors.
Never writes any file — safe to run in CI.

Usage:  python scripts/validate.py
"""
import re
import sys
from _common import ROOT, as_records, error_json_files, read_json

VOCAB = ROOT / "data" / "vocab" / "vocab.json"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Controlled vocabularies (mirror templates/*.md). Categories and pos are fixed;
# tags and topics are extendable, so unknown ones only warn.
CATEGORIES = {"grammar", "vocabulary", "collocation", "naturalness", "pronunciation", "discourse"}
POS = {"noun", "verb", "adjective", "adverb", "phrase", "idiom", "preposition", "conjunction", "other"}

ERROR_REQUIRED = ["id", "date", "category", "tag", "my_sentence", "correction", "explanation", "correct_examples", "review"]
VOCAB_REQUIRED = ["word", "pos", "definition", "example", "first_seen", "review"]

errors = []    # hard failures -> exit 1
warnings = []  # soft notes -> still exit 0


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_review(obj, where):
    review = obj.get("review")
    if not isinstance(review, dict):
        err(f"{where}: 'review' must be an object")
        return
    if "status" in review and review["status"] not in {"new", "learning", "mastered"}:
        warn(f"{where}: unusual review.status '{review['status']}'")
    for field in ("times_seen_again", "review_count", "correct_count", "incorrect_count", "correct_streak"):
        if field in review and (
            not isinstance(review[field], int)
            or isinstance(review[field], bool)
            or review[field] < 0
        ):
            err(f"{where}: review.{field} must be a non-negative integer")
    for field in ("last_reviewed", "next_review"):
        value = review.get(field)
        if value is not None and (not isinstance(value, str) or not DATE_RE.match(value)):
            err(f"{where}: review.{field} must be null or YYYY-MM-DD")
    if "review_days" in review:
        days = review["review_days"]
        if not isinstance(days, list) or any(
            not isinstance(day, str) or not DATE_RE.match(day) for day in days
        ):
            err(f"{where}: review.review_days must be a list of YYYY-MM-DD dates")
        elif len(days) != len(set(days)):
            err(f"{where}: review.review_days must not contain duplicate dates")
    review_count = review.get("review_count", 0)
    correct_count = review.get("correct_count", 0)
    incorrect_count = review.get("incorrect_count", 0)
    if all(isinstance(value, int) and not isinstance(value, bool) for value in (
        review_count, correct_count, incorrect_count
    )) and correct_count + incorrect_count > review_count:
        err(f"{where}: correct_count + incorrect_count cannot exceed review_count")


def validate_errors():
    seen_ids = {}
    files = error_json_files()
    total = 0
    for f in files:
        try:
            records = as_records(read_json(f, []))
        except ValueError as e:  # JSONDecodeError is a subclass of ValueError
            err(f"{f.name}: invalid JSON ({e})")
            continue
        for i, rec in enumerate(records):
            total += 1
            where = f"{f.name}[{rec.get('id', i)}]"
            for field in ERROR_REQUIRED:
                if not rec.get(field) and rec.get(field) != 0:
                    err(f"{where}: missing required field '{field}'")
            cat = rec.get("category")
            if cat and cat not in CATEGORIES:
                err(f"{where}: category '{cat}' not in controlled vocabulary")
            if not rec.get("tag"):
                err(f"{where}: empty tag")
            d = rec.get("date", "")
            if d and not DATE_RE.match(d):
                err(f"{where}: bad date format '{d}' (want YYYY-MM-DD)")
            ex = rec.get("correct_examples")
            if ex is not None and not isinstance(ex, list):
                err(f"{where}: correct_examples must be a list")
            rid = rec.get("id")
            if rid:
                if rid in seen_ids:
                    err(f"{where}: duplicate id (also in {seen_ids[rid]})")
                else:
                    seen_ids[rid] = f.name
            check_review(rec, where)
    return total


def validate_vocab():
    if not VOCAB.exists():
        return 0
    try:
        records = as_records(read_json(VOCAB, []))
    except ValueError as e:
        err(f"vocab.json: invalid JSON ({e})")
        return 0
    seen_words = {}
    for i, rec in enumerate(records):
        word = rec.get("word", "")
        where = f"vocab.json[{word or i}]"
        for field in VOCAB_REQUIRED:
            if not rec.get(field) and rec.get(field) != 0:
                err(f"{where}: missing required field '{field}'")
        pos = rec.get("pos")
        if pos and pos not in POS:
            err(f"{where}: pos '{pos}' not in controlled vocabulary")
        ex = rec.get("example")
        if ex is not None and not isinstance(ex, list):
            err(f"{where}: example must be a list")
        d = rec.get("first_seen", "")
        if d and not DATE_RE.match(d):
            err(f"{where}: bad first_seen format '{d}' (want YYYY-MM-DD)")
        key = word.strip().lower()
        if key:
            if key in seen_words:
                err(f"{where}: duplicate word (case-insensitive)")
            else:
                seen_words[key] = True
        check_review(rec, where)
    return len(records)


def main():
    n_err = validate_errors()
    n_vocab = validate_vocab()

    for w in warnings:
        print(f"⚠️  {w}")
    for e in errors:
        print(f"❌ {e}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s). "
              f"Checked {n_err} error records, {n_vocab} vocab words.")
        sys.exit(1)
    print(f"✅ Valid: {n_err} error records, {n_vocab} vocab words, {len(warnings)} warning(s).")


if __name__ == "__main__":
    main()

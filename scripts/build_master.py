#!/usr/bin/env python3
"""Merge data/errors/json/**/*.json into database/errors_master.csv.

Usage:  python scripts/build_master.py
Standard library only, no network or dependencies needed.
"""
import csv
import json

from _common import ROOT, as_records, error_json_files, read_json

OUT = ROOT / "database" / "errors_master.csv"

COLUMNS = [
    "id", "date", "category", "tag", "my_sentence", "correction",
    "explanation", "correct_examples", "context",
    "status", "times_seen_again", "last_reviewed", "source_ref",
]


def flatten(rec):
    review = rec.get("review") or {}
    examples = rec.get("correct_examples") or []
    if isinstance(examples, list):
        examples = " | ".join(examples)
    return {
        "id": rec.get("id", ""),
        "date": rec.get("date", ""),
        "category": rec.get("category", ""),
        "tag": rec.get("tag", ""),
        "my_sentence": rec.get("my_sentence", ""),
        "correction": rec.get("correction", ""),
        "explanation": rec.get("explanation", ""),
        "correct_examples": examples,
        "context": rec.get("context", ""),
        "status": review.get("status", ""),
        "times_seen_again": review.get("times_seen_again", 0),
        "last_reviewed": review.get("last_reviewed") or "",
        "source_ref": rec.get("source_ref", ""),
    }


def main():
    rows = []
    files = error_json_files()
    if not files:
        print("No real data files found (*.example.json is skipped).")
        print("Save each day's extracted JSON to data/errors/json/YYYY-MM/YYYY-MM-DD.json first.")
        return
    for f in files:
        try:
            data = read_json(f, [])
        except json.JSONDecodeError as e:
            print(f"⚠️  Skipping {f.name}: JSON parse failed ({e})")
            continue
        for rec in as_records(data):
            rows.append(flatten(rec))

    rows.sort(key=lambda r: (r["date"], r["id"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"✅ Wrote {len(rows)} errors → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

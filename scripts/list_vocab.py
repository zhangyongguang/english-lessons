#!/usr/bin/env python3
"""Quick status of the vocabulary store.

Usage:  python scripts/list_vocab.py
Shows total words, status breakdown, how many added this ISO week,
and the most-looked-up (stubborn) words.
"""
from collections import Counter
from datetime import date
from _common import ROOT, as_records, read_json

SRC = ROOT / "data" / "vocab" / "vocab.json"


def iso_week(d: str) -> str:
    y, w, _ = date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def main():
    if not SRC.exists():
        print(f"Not found: {SRC.relative_to(ROOT)}. Use /word to add some words first.")
        return
    data = as_records(read_json(SRC, []))
    if not data:
        print("No words yet. Use /word <word…> to add some.")
        return

    status = Counter((e.get("review") or {}).get("status", "new") for e in data)
    this_week = iso_week(date.today().isoformat())
    added_this_week = sum(
        1 for e in data
        if e.get("first_seen") and iso_week(e["first_seen"]) == this_week
    )
    stubborn = sorted(
        data,
        key=lambda e: (e.get("review") or {}).get("times_looked_up", 1),
        reverse=True,
    )

    print(f"Total words: {len(data)}")
    print("By status: " + ", ".join(f"{k} {v}" for k, v in status.most_common()))
    print(f"Added this week ({this_week}): {added_this_week}")

    repeated = [e for e in stubborn if (e.get("review") or {}).get("times_looked_up", 1) > 1]
    if repeated:
        print("\nLooked up more than once (worth a closer review):")
        for e in repeated[:5]:
            n = (e.get("review") or {}).get("times_looked_up", 1)
            print(f"  {e.get('word', '')}  ×{n}")


if __name__ == "__main__":
    main()

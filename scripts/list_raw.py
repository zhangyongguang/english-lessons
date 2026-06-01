#!/usr/bin/env python3
"""List transcripts in data/raw/, grouped by date, marking which days are not yet extracted.

Usage:  python scripts/list_raw.py
Used by the /extract workflow to decide which day to process.
"""
from collections import defaultdict
from _common import ROOT, error_json_path, parse_date

RAW = ROOT / "data" / "raw"


def main():
    groups = defaultdict(list)
    for f in sorted(RAW.glob("*.txt")):
        d = parse_date(f.name) or "unknown-date"
        groups[d].append(f.name)

    if not groups:
        print("No transcripts in data/raw/. Drop the .txt files downloaded from Tencent Meeting here.")
        return

    pending = []
    for d in sorted(groups):
        done = error_json_path(d).exists()
        mark = "✅ extracted" if done else "⬜ pending"
        if not done:
            pending.append(d)
        print(f"{d}  {mark}  ({len(groups[d])} transcript(s))")
        for n in groups[d]:
            print(f"      - {n}")

    print()
    if pending:
        print(f"Pending dates: {', '.join(pending)}")
        print(f"Most recent pending: {pending[-1]}")
    else:
        print("All extracted 🎉")


if __name__ == "__main__":
    main()

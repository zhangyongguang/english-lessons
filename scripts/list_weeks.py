#!/usr/bin/env python3
"""List extracted errors by ISO week, marking which weeks have no weekly report yet.

Usage:  python scripts/list_weeks.py
Used by /weekly to decide which week to summarize (same logic as list_raw.py:
has data but analysis/weekly/<week>.md does not exist = pending).
"""
import csv
from collections import defaultdict
from datetime import date
from _common import ROOT

MASTER = ROOT / "database" / "errors_master.csv"
WEEKLY = ROOT / "analysis" / "weekly"


def iso_week(d: str) -> str:
    y, w, _ = date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def main():
    if not MASTER.exists():
        print("No master table yet. Run first: python scripts/build_master.py")
        return

    weeks = defaultdict(lambda: {"count": 0, "dates": set()})
    with MASTER.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            d = (row.get("date") or "").strip()
            if not d:
                continue
            try:
                wk = iso_week(d)
            except ValueError:
                continue
            weeks[wk]["count"] += 1
            weeks[wk]["dates"].add(d)

    if not weeks:
        print("No error data in the master table yet. Extract a few days with /extract first.")
        return

    pending = []
    for wk in sorted(weeks):
        done = (WEEKLY / f"{wk}.md").exists()
        mark = "✅ summarized" if done else "⬜ pending"
        if not done:
            pending.append(wk)
        info = weeks[wk]
        span = f"{min(info['dates'])} ~ {max(info['dates'])}"
        print(f"{wk}  {mark}  ({info['count']} errors, {len(info['dates'])} day(s): {span})")

    print()
    if pending:
        print(f"Pending weeks: {', '.join(pending)}")
        print(f"Most recent pending: {pending[-1]}")
    else:
        print("All summarized 🎉")


if __name__ == "__main__":
    main()

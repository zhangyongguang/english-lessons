#!/usr/bin/env python3
"""Render a day's errors JSON into a compact two-column Markdown table.

Reads  data/errors/json/YYYY-MM/DATE.json
Writes data/errors/md/YYYY-MM/DATE.md
Only the "Mistake" and "Correct" columns are shown; other fields
(explanation, examples, context, etc.) are omitted.
Usage:  python scripts/render_md.py 2026-05-28
"""
import sys
from _common import ROOT, as_records, error_json_path, error_md_path, md_cell, read_json


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/render_md.py YYYY-MM-DD")
        return
    date = sys.argv[1]
    src = error_json_path(date)
    if not src.exists():
        print(f"Not found: {src.relative_to(ROOT)}")
        return

    data = as_records(read_json(src, []))

    lines = [
        f"# Mistakes · {date}",
        "",
        "| Mistake | Correct |",
        "|---|---|",
    ]
    for e in data:
        lines.append(f"| {md_cell(e.get('my_sentence', ''))} | {md_cell(e.get('correction', ''))} |")
    lines.append("")

    out = error_md_path(date)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Generated report → {out.relative_to(ROOT)} ({len(data)} rows)")


if __name__ == "__main__":
    main()

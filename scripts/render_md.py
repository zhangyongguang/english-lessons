#!/usr/bin/env python3
"""Render a day's data/errors/DATE.json into a compact two-column Markdown table.

Only the "Mistake" and "Correct" columns are shown; other fields
(explanation, examples, context, etc.) are omitted.
Usage:  python scripts/render_md.py 2026-05-28
Output: data/errors/2026-05-28.md
"""
import json
import sys
from _common import ROOT


def cell(text):
    """Make text safe inside a Markdown table cell: escape pipes, flatten newlines."""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/render_md.py YYYY-MM-DD")
        return
    date = sys.argv[1]
    src = ROOT / "data" / "errors" / f"{date}.json"
    if not src.exists():
        print(f"Not found: {src.relative_to(ROOT)}")
        return

    data = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = [data]

    lines = [
        f"# Mistakes · {date}",
        "",
        "| Mistake | Correct |",
        "|---|---|",
    ]
    for e in data:
        lines.append(f"| {cell(e.get('my_sentence', ''))} | {cell(e.get('correction', ''))} |")
    lines.append("")

    out = ROOT / "data" / "errors" / f"{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Generated report → {out.relative_to(ROOT)} ({len(data)} rows)")


if __name__ == "__main__":
    main()

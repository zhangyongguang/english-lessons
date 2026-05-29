#!/usr/bin/env python3
"""Render data/vocab/vocab.json into a readable Markdown table (newest lookups first).

Columns: Word | Meaning | Example | Date. Date (first_seen) is last since it's
secondary; words still cluster by day for review. The first example sentence is
shown so you can grasp the usage at a glance.
Usage:  python scripts/render_vocab_md.py
Output: data/vocab/vocab.md
"""
import json
from _common import ROOT

SRC = ROOT / "data" / "vocab" / "vocab.json"
OUT = ROOT / "data" / "vocab" / "vocab.md"


def cell(text):
    """Make text safe inside a Markdown table cell: escape pipes, flatten newlines."""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def first_example(entry):
    ex = entry.get("example") or []
    if isinstance(ex, str):
        return ex
    return ex[0] if ex else ""


def sort_key(item):
    # Newest first: by last_seen date, then by insertion order in the file.
    # New entries are appended, so a higher index = added more recently. This
    # breaks same-day ties so the most recently added word is always on top.
    idx, entry = item
    review = entry.get("review") or {}
    last = review.get("last_seen") or entry.get("first_seen") or ""
    return (last, idx)


def main():
    if not SRC.exists():
        print(f"Not found: {SRC.relative_to(ROOT)}")
        return
    data = json.loads(SRC.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = [data]

    ordered = sorted(enumerate(data), key=sort_key, reverse=True)
    data = [entry for _, entry in ordered]

    lines = [
        "# Vocabulary  (latest first)",
        "",
        f"{len(data)} word(s).",
        "",
        "| Word | Meaning | Example | Date |",
        "|---|---|---|---|",
    ]
    for e in data:
        word = e.get("word", "")
        pos = e.get("pos", "")
        head = f"{word} _({pos})_" if pos else word
        date = e.get("first_seen", "")
        lines.append(f"| {cell(head)} | {cell(e.get('definition', ''))} | {cell(first_example(e))} | {cell(date)} |")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Generated vocab list → {OUT.relative_to(ROOT)} ({len(data)} words)")


if __name__ == "__main__":
    main()

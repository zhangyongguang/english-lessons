#!/usr/bin/env python3
"""Convert database/errors_master.csv into an Anki-importable TSV.

Usage:  python scripts/make_anki.py
Output: exercises/anki/anki_import.tsv
Import: Anki -> File -> Import, separator = Tab, map fields to Front/Back/Tags.
Standard library only.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "database" / "errors_master.csv"
OUT = ROOT / "exercises" / "anki" / "anki_import.tsv"


def build_card(row):
    # Front: ask yourself to fix the sentence (use your own wrong sentence as the prompt)
    front = f"Fix this sentence:<br>{row['my_sentence']}"
    # Back: correct version + explanation + examples
    examples = row["correct_examples"].replace(" | ", "<br>• ")
    back_parts = [f"✅ {row['correction']}"]
    if row["explanation"]:
        back_parts.append(f"<br><br>📖 {row['explanation']}")
    if examples:
        back_parts.append(f"<br><br>e.g.<br>• {examples}")
    back = "".join(back_parts)
    tags = f"{row['category']} {row['tag']}".strip()
    return front, back, tags


def clean(s):
    # Newlines/tabs would break the TSV layout
    return s.replace("\t", " ").replace("\n", "<br>")


def main():
    if not SRC.exists():
        print("Master table not found. Run first: python scripts/build_master.py")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with SRC.open(encoding="utf-8-sig", newline="") as fh, \
         OUT.open("w", encoding="utf-8", newline="") as out:
        reader = csv.DictReader(fh)
        for row in reader:
            front, back, tags = build_card(row)
            out.write(f"{clean(front)}\t{clean(back)}\t{clean(tags)}\n")
            n += 1
    print(f"✅ Generated {n} cards → {OUT.relative_to(ROOT)}")
    print("   In Anki: separator = Tab, map the 3 columns to Front / Back / Tags.")


if __name__ == "__main__":
    main()

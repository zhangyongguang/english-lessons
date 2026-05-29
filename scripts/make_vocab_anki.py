#!/usr/bin/env python3
"""Convert data/vocab/vocab.json into an Anki-importable TSV.

Usage:  python scripts/make_vocab_anki.py
Output: exercises/anki/vocab_anki.tsv
Import: Anki -> File -> Import, separator = Tab, map fields to Front/Back/Tags.
Standard library only.
"""
from _common import ROOT, as_records, read_json, tsv_clean

SRC = ROOT / "data" / "vocab" / "vocab.json"
OUT = ROOT / "exercises" / "anki" / "vocab_anki.tsv"


def build_card(entry):
    word = entry.get("word", "")
    pos = entry.get("pos", "")
    front = f"{word} <i>({pos})</i>" if pos else word

    back_parts = [entry.get("definition", "")]
    examples = entry.get("example") or []
    if isinstance(examples, str):
        examples = [examples]
    if examples:
        back_parts.append("<br><br>e.g.<br>• " + "<br>• ".join(examples))
    synonyms = entry.get("synonyms") or []
    if synonyms:
        back_parts.append("<br><br>syn: " + ", ".join(synonyms))
    back = "".join(back_parts)

    tags = " ".join(t for t in [pos, entry.get("topic", "")] if t).strip()
    return front, back, tags


def main():
    if not SRC.exists():
        print(f"Not found: {SRC.relative_to(ROOT)}")
        return
    data = as_records(read_json(SRC, []))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with OUT.open("w", encoding="utf-8", newline="") as out:
        for entry in data:
            front, back, tags = build_card(entry)
            out.write(f"{tsv_clean(front)}\t{tsv_clean(back)}\t{tsv_clean(tags)}\n")
            n += 1
    print(f"✅ Generated {n} vocab cards → {OUT.relative_to(ROOT)}")
    print("   In Anki: separator = Tab, map the 3 columns to Front / Back / Tags.")


if __name__ == "__main__":
    main()

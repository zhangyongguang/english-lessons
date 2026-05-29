#!/usr/bin/env python3
"""Create placeholder files for a new day.

Usage:
    python scripts/new_day.py            # use today's date
    python scripts/new_day.py 2026-05-30 # a specific date
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    raw = ROOT / "data" / "raw" / f"{d}.txt"
    errors = ROOT / "data" / "errors" / f"{d}.json"

    if not raw.exists():
        raw.write_text("", encoding="utf-8")
        print(f"📄 Created empty {raw.relative_to(ROOT)} — paste the Tencent Meeting transcript here")
    if not errors.exists():
        errors.write_text("[]\n", encoding="utf-8")
        print(f"📄 Created empty {errors.relative_to(ROOT)} — store the extraction here")

    print("\nNext steps:")
    print(f"  1. Save the transcript to data/raw/{d}.txt")
    print("  2. Send it + prompts/extract_errors.md to Claude")
    print(f"  3. Save the resulting JSON to data/errors/{d}.json")
    print("  4. Run python scripts/build_master.py to update the master table")


if __name__ == "__main__":
    main()

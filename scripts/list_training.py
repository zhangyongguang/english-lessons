#!/usr/bin/env python3
"""Show the active Chat Live prompt and current target mastery.

Usage: python3 scripts/list_training.py
This script is read-only; /extract or the training-loop skill creates prompts.
"""
import json

from _common import ROOT, read_json

CURRENT = ROOT / "training" / "live" / "current.md"
MASTERY = ROOT / "data" / "training" / "mastery.json"


def percent(correct, total):
    if not total:
        return "—"
    return f"{correct / total:.0%}"


def main():
    if CURRENT.exists():
        print(f"Chat Live file: {CURRENT.relative_to(ROOT)}")
    else:
        print("No current Chat Live file. Run /extract or use the training-loop skill to plan a week.")

    try:
        mastery = read_json(MASTERY, {}) or {}
    except json.JSONDecodeError as exc:
        print(f"Invalid mastery data: {exc}")
        return

    if not mastery:
        return

    print("\nCurrent targets:")
    for target_id, item in mastery.items():
        accuracy = percent(
            item.get("correct_first_attempt", 0),
            item.get("total_opportunities", 0),
        )
        print(
            f"  {target_id}: {item.get('status', 'new')}, "
            f"first-attempt {accuracy}, next review {item.get('next_review') or 'unscheduled'}"
        )


if __name__ == "__main__":
    main()

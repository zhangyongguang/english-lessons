---
name: training-loop
description: Turn extracted English errors and Chat Live reports into a closed weekly speaking-training loop. Use when selecting exactly three weekly targets, showing or refreshing training/live/current.md, processing a Training report, scheduling delayed retrieval, or updating mastery.
---

# Training Loop

Train from Jack's real errors while exposing only three high-value targets per week.

## Plan or refresh a week

1. Read `CLAUDE.md`, `templates/training_plan_schema.md`, and `references/target-selection.md`.
2. Run `python3 scripts/build_master.py`; analyze the requested ISO week plus two preceding weeks.
3. Read `data/training/mastery.json` when present.
4. If no plan exists, select exactly three targets and write `training/plans/WEEK.md`.
5. Keep target IDs stable through the week. New extractions update evidence, contexts, and difficulty—not target identity.
6. Generate `training/live/WEEK-session-NN.md` from `templates/live_session_template.md` and copy the complete active prompt to `training/live/current.md`.

Do not replace `current.md` when refreshing an older historical week.

## Process a Training report

1. Preserve raw Markdown under `training/results/WEEK/`.
2. Normalize metrics under `data/training/results/json/WEEK/` using `templates/training_result_schema.md`.
3. Verify metric consistency.
4. Update `data/training/mastery.json` using `templates/mastery_schema.md` and `references/mastery-rules.md`.
5. Generate the next versioned session and replace `training/live/current.md`.

Immediate prompted repetition never counts as mastery. Base decisions on first attempts, delayed retrieval, and transfer.

## Show status

Run `python3 scripts/list_training.py` and tell the user to give `training/live/current.md` to Chat Live.

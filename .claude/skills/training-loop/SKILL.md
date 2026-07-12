---
name: training-loop
description: Turn this project's extracted English errors into a closed weekly speaking-training loop. Use when selecting exactly three weekly targets, generating a Markdown prompt for Chat Live, processing a live-session report, scheduling delayed retrieval, or deciding whether a target should continue, enter review, or be marked mastered.
---

# Training Loop

Build training from the learner's real errors instead of generic lesson material. Keep the error database complete, but expose only three high-value targets in any training week.

## Plan a week

1. Read `CLAUDE.md`, `templates/error_schema.md`, and `templates/training_plan_schema.md`.
2. Refresh `database/errors_master.csv` with `python3 scripts/build_master.py`.
3. Analyze the requested ISO week and the preceding two weeks. Count both occurrences and distinct lesson days.
4. Read `data/training/mastery.json` when it exists. Do not select a mastered target unless recent errors show relapse.
5. Select exactly three narrow, observable targets. Apply `references/target-selection.md`.
6. Write the structured plan to `data/training/plans/json/WEEK.json` when that data directory exists in the current implementation.
7. Render or write the learner-facing plan to `training/plans/WEEK.md`, following `templates/training_plan_schema.md`.
8. Generate `training/live/WEEK.md` from `templates/live_session_template.md`.

Once a week's plan exists, keep its three target IDs stable through that week. New extractions may update evidence, examples, prompt contexts, and difficulty, but must not silently replace a target. Change a target only during the weekly review or when the user explicitly requests it.

Never select goals such as “improve grammar” or “speak naturally.” Define a trigger, examples from the error log, and a measurable first-attempt success criterion.

## Generate a live session

Read the weekly plan and `templates/live_session_template.md`. Make Chat Live:

- track only the three weekly targets;
- let the learner finish before correction;
- ask for self-correction before supplying an answer;
- require the complete answer again after correction;
- retest later without announcing the target;
- transfer the same form to a different situation;
- ignore unrelated minor errors unless meaning breaks down;
- finish with the exact report contract in `templates/training_result_schema.md`.

Use a progression across sessions: establish forms, retrieve without prompts, transfer contexts, mix under time pressure, then assess without coaching.

Write each prompt to `training/live/WEEK-session-NN.md`. Also write the active prompt as a complete standalone copy at `training/live/current.md`. Never make `current.md` a link-only pointer because the user may paste or upload that file without repository context. Do not replace `current.md` while refreshing a historical week newer than the active plan.

## Process results

1. Preserve the raw Chat Live report.
2. Normalize it according to `templates/training_result_schema.md`.
3. Count first attempts separately from prompted corrections.
4. Update mastery according to `templates/mastery_schema.md` and `references/mastery-rules.md`.
5. Schedule the next retrieval. Immediate repetition alone never proves mastery.

## Review a week

Report each target as `continue`, `review`, `mastered`, or `relapsed`. Base the decision on first-attempt accuracy, delayed retrieval, and transfer—not lesson attendance or the number of collected errors. Carry no more than two failed targets forward so that the next week can still introduce one new priority.

Do not modify transcripts. Treat JSON as source data and Markdown as a generated, readable artifact.

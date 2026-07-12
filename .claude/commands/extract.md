---
description: Extract errors from transcripts and refresh the current weekly speaking training
argument-hint: "[date, optional, e.g. 2026-05-28]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write, Glob
---

## Pending transcripts
!`python3 scripts/list_raw.py`

## Task
You are my spoken-English teaching assistant. Using the list above:

1. **Decide which date(s) to process**:
   - If `$ARGUMENTS` is a date (e.g. `2026-05-28`), process that day.
   - If `$ARGUMENTS` is `all`, process **every** "pending" date above, from earliest to latest (use this when several days have piled up).
   - If `$ARGUMENTS` is empty, process the "most recent pending" day.
   - If there are no pending dates, tell me and stop.
   Do steps 2–6 once for each date DATE you process.
2. **Read the transcripts**: use Glob/Read to read every `.txt` in `data/raw/` whose filename contains DATE's digits (e.g. `20260528`). A day may have several recordings — read and merge them all.
3. **Extract errors**: following the requirements and field spec below, extract "the mistakes `Jack` (the student = me) made + `ZIVA_Teacher` (the teacher)'s corrections" and write them to `data/errors/json/YYYY-MM/DATE.json` (sharded by year-month, e.g. `data/errors/json/2026-05/2026-05-28.json`; a JSON array; merge multiple recordings; sequential ids `DATE-001`, `DATE-002`, …). Create the `YYYY-MM` folder if it doesn't exist.

Extraction requirements:

@prompts/extract_errors.md

Field definitions and controlled tag vocabulary:

@templates/error_schema.md

4. **Self-review pass (required)**: after writing the JSON, re-read the full transcript(s) once more and check the result against it. Verify both:
   - **Omissions**: scan every `Jack` line again — did you miss any real sentence-level error the teacher corrected (or any clearly wrong structure)? Add the missing ones.
   - **Correctness**: for each entry, is `my_sentence` a faithful restoration of what I meant, and is `correction` actually correct, natural English that matches the teacher's intent? Fix anything wrong, garbled, or fabricated; drop entries that aren't real errors.
   If you change anything, rewrite the same `data/errors/json/YYYY-MM/DATE.json` (keep ids sequential) before moving on. Briefly note in your final report what the review changed (e.g. "added 1, fixed 2"), or "no changes" if clean.
5. **Render the report**: run `python3 scripts/render_md.py DATE` (writes `data/errors/md/YYYY-MM/DATE.md`, a two-column "Mistake / Correct" table; the script creates the folder).
6. **Update the master table**: run `python3 scripts/build_master.py`.
7. **Refresh this week's training (required)**:
   - Determine DATE's ISO week WEEK.
   - Follow `@.claude/skills/training-loop/SKILL.md` and refresh that week's training from the newly updated master table.
   - If `training/plans/WEEK.md` does not exist, select exactly three targets and create the plan.
   - If the plan already exists, **keep its three target IDs stable for the rest of the week**. Update their evidence with the new errors; don't replace targets midweek merely because counts changed.
   - Read `data/training/mastery.json` and the latest report under `training/results/WEEK/` when present. Generate or update the next needed session prompt without overwriting completed session reports.
   - Write the versioned prompt to `training/live/WEEK-session-NN.md` and write the same standalone prompt to `training/live/current.md`. `current.md` is the stable file the user gives to Chat Live.
   - If WEEK is historical and a newer active training week already exists, refresh the historical plan but do not replace `training/live/current.md`.
8. **Report back**: tell me how many errors were extracted (and what the self-review changed), give the error report path, and give the current Chat Live file path `training/live/current.md`. Don't restate errors one by one.

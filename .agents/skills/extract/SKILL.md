---
name: extract
description: Extract Jack's English errors from pending Tencent Meeting transcripts, self-review them, rebuild generated error outputs, and refresh the relevant weekly Chat Live training. Use when the user asks to extract/process the latest transcript, a specific lesson date, or all pending lesson dates.
---

# Extract English Errors

Process one or more lesson dates without modifying raw transcripts.

## Select dates

1. Run `python3 scripts/list_raw.py`.
2. Process a specified `YYYY-MM-DD`, every pending date for `all`, or the most recent pending date by default.
3. Stop cleanly when nothing is pending.

## Extract a date

1. Read `CLAUDE.md`, `prompts/extract_errors.md`, and `templates/error_schema.md` completely.
2. Find every `.txt` under `data/raw/` whose filename contains the date without hyphens. Ignore `._*`. Merge multiple recordings for one date.
3. Extract only Jack's real sentence-level errors and teacher-supported corrections. `Jack` is the student; `ZIVA_Teacher` is the teacher. Treat transcription noise cautiously.
4. Write a JSON array to `data/errors/json/YYYY-MM/DATE.json` with sequential IDs and controlled schema values.
5. Re-read every transcript. Add omissions, fix inaccurate restorations/corrections, remove fabricated entries, and resequence IDs.
6. Run `python3 scripts/render_md.py DATE`.

Never rename, edit, or delete files under `data/raw/`.

## Rebuild and verify

1. Run `python3 scripts/build_master.py` after all selected dates.
2. Run `python3 scripts/validate.py`.
3. Follow `$training-loop` for each applicable week: create three targets if absent, keep existing target IDs stable within the week, update evidence, and refresh `training/live/current.md` only for the active/latest week.

## Report

Report each date's error count, self-review changes, error Markdown path, and `training/live/current.md`. Do not restate every error.

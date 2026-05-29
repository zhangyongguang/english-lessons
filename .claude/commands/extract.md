---
description: Extract my (Jack's) English errors from the latest Tencent Meeting transcript into a readable Markdown report
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
3. **Extract errors**: following the requirements and field spec below, extract "the mistakes `Jack` (the student = me) made + `ZIVA_Teacher` (the teacher)'s corrections" and write them to `data/errors/DATE.json` (a JSON array; merge multiple recordings; sequential ids `DATE-001`, `DATE-002`, …).

Extraction requirements:

@prompts/extract_errors.md

Field definitions and controlled tag vocabulary:

@templates/error_schema.md

4. **Self-review pass (required)**: after writing the JSON, re-read the full transcript(s) once more and check the result against it. Verify both:
   - **Omissions**: scan every `Jack` line again — did you miss any real sentence-level error the teacher corrected (or any clearly wrong structure)? Add the missing ones.
   - **Correctness**: for each entry, is `my_sentence` a faithful restoration of what I meant, and is `correction` actually correct, natural English that matches the teacher's intent? Fix anything wrong, garbled, or fabricated; drop entries that aren't real errors.
   If you change anything, rewrite `data/errors/DATE.json` (keep ids sequential) before moving on. Briefly note in your final report what the review changed (e.g. "added 1, fixed 2"), or "no changes" if clean.
5. **Render the report**: run `python3 scripts/render_md.py DATE` (produces a two-column "Mistake / Correct" table).
6. **Update the master table**: run `python3 scripts/build_master.py`.
7. **Report back**: tell me in one sentence how many errors were extracted (and what the self-review changed) and that the report is at `data/errors/DATE.md`. Don't restate them one by one and don't add extra explanation (I'll look it up myself).

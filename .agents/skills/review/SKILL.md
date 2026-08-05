---
name: review
description: Review Jack's real sentence-level English mistakes one at a time using English only, automatically record review and error counts, schedule spaced repetition, and recommend the highest-priority error. Use when the user invokes $review, asks to review mistakes or see the next or recommended error, requests review progress, or responds to an active review card with y, n, s, or a corrected sentence.
---

# Review English Errors

Use the structured error JSON behind `data/errors/md/YYYY-MM/DATE.md`; never
parse the generated Markdown when the matching JSON is available.

## Start or continue

1. Read `CLAUDE.md` and `templates/error_schema.md` completely.
2. Run `date +%F` and use that exact date for every command in this turn.
3. If the user is responding to the last displayed card, assess and record it first:
   - `correct`: the user replies `y`, or writes a grammatically correct sentence with the same intended meaning;
   - `incorrect`: the user replies `n`, or their attempted correction still contains the target error;
   - `seen`: the user replies `s` without claiming knowledge or attempting a correction.
4. Record with `python3 scripts/review_errors.py record ERROR_ID RESULT --today DATE`.
5. Fetch one new card with `python3 scripts/review_errors.py next --today DATE --exclude ERROR_ID`. Omit `--exclude` when starting without an active card.

Do not record anything when the user merely starts `$review`, stops, or asks for
status. Never hand-edit review counters; use the script so scheduling and mastery
rules remain consistent.

## Show one card

Use English only for every review card, explanation, instruction, progress summary,
and response, even when the user invokes the skill in another language. Present
exactly one error using this shape:

```text
...
...
...
```

Do not display the `Mistake:`, `Problem:`, or `Correction:` labels; show the
three corresponding content lines in the same order. Do not display a reply
prompt; the accepted responses remain `y`, `n`, `s`, or the user's correction.

Compress the stored English `explanation` into one plain English sentence. Do not
show the error ID, score, tag counts, examples, or a second card
unless the user asks. If the script returns `nothing_due`, say when the next review
is due instead of bypassing the schedule.

## Show progress

For `$review status`, run:

```bash
python3 scripts/review_errors.py status --today DATE
```

Summarize total unique errors reviewed, total reviews, total incorrect reviews,
due errors, mastered errors, and the weakest reviewed tags. Keep this status view
separate from weekly target mastery in `data/training/mastery.json`.

## Boundaries

- Keep `data/raw/` and generated `data/errors/md/` files unchanged.
- Preserve `times_seen_again`; it describes recurrence in lessons, not review misses.
- Treat `y` as the user's self-rating. For a written correction, assess grammar
  and intended meaning; accept natural alternatives, not only exact string matches.
- The script requires correct reviews on three distinct days and at least 80%
  overall accuracy before marking one sentence `mastered`.

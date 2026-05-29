---
description: Summarize a week's English errors, analyze high-frequency weak spots, output a weekly report
argument-hint: "[ISO week, optional, e.g. 2026-W22]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## Refresh the master table
!`python3 scripts/build_master.py`

## Week status (pending / summarized)
!`python3 scripts/list_weeks.py`

## Task
1. **Decide which week WEEK to summarize**: if `$ARGUMENTS` gives an ISO week (e.g. `2026-W22`), use it; otherwise take the "most recent pending" week above. If there are no pending weeks, tell me and stop.
2. Read `database/errors_master.csv` and **filter only the errors belonging to WEEK** (judge each row by whether its `date`'s ISO week equals WEEK).
3. Do the pattern analysis below and write it to `analysis/weekly/WEEK.md` (e.g. `analysis/weekly/2026-W22.md`), in English, conclusions first then data, concise:

@prompts/analyze_patterns.md

4. Tell me in one sentence the single thing I should fix this week.

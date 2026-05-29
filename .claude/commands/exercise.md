---
description: Generate targeted practice from recent errors (correction / fill-in / translation / multiple choice)
argument-hint: "[tag, optional, e.g. articles]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## Refresh the master table
!`python3 scripts/build_master.py`

## Task
Read `database/errors_master.csv`. If `$ARGUMENTS` specifies a tag (e.g. `articles`), build questions around that tag only; otherwise cover my 3 most frequent weak spots.

Following the requirements below, write 10 questions (use brand-new sentences, don't copy my originals; keep questions and answers separate) to `exercises/generated/<date>-<topic>.md`, and tell me the file path:

@prompts/generate_exercises.md

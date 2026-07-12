---
description: Show or refresh the current Chat Live speaking session
argument-hint: "[refresh, optional]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write, Glob
---

## Current training status
!`python3 scripts/list_training.py`

## Task

- With no arguments, report the active targets and tell the user to give `training/live/current.md` to Chat Live. Do not regenerate anything.
- If `$ARGUMENTS` is `refresh`, follow `@.claude/skills/training-loop/SKILL.md`, read the current plan, mastery data, and latest result, then regenerate the next appropriate versioned session and the identical standalone `training/live/current.md`.
- Never replace the week's three target IDs during a refresh.

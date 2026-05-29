---
description: Export the error log into an Anki-importable card file
allowed-tools: Bash(python3:*), Bash(python:*)
---

## Generate cards
!`python3 scripts/build_master.py`
!`python3 scripts/make_anki.py`

## Task
Based on the output above, tell me: how many cards were generated, that the file is at `exercises/anki/anki_import.tsv`, and how to import it — Anki ▸ File ▸ Import, separator = **Tab**, map the three columns to Front / Back / Tags.

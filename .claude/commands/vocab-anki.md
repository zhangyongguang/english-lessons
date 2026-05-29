---
description: Export the vocabulary store into an Anki-importable card file
allowed-tools: Bash(python3:*), Bash(python:*)
---

## Generate cards
!`python3 scripts/make_vocab_anki.py`

## Task
Based on the output above, tell me: how many vocab cards were generated, that the file is at `exercises/anki/vocab_anki.tsv`, and how to import it — Anki ▸ File ▸ Import, separator = **Tab**, map the three columns to Front / Back / Tags.

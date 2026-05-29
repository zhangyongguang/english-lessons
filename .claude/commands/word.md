---
description: Save unfamiliar words to the vocabulary store (from arguments, or harvested from this session), with a self-review pass
argument-hint: "[word(s), optional; empty = harvest from this chat session]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## Current vocabulary
!`python3 scripts/list_vocab.py`

## Task
You are my English vocabulary assistant. Decide which words to capture:

- **If `$ARGUMENTS` is non-empty**: those are the word(s) to save (may be several, and may include the sentence/context where I met them).
- **If `$ARGUMENTS` is empty**: harvest from **this chat session's conversation** — scan our earlier messages for English words I asked the meaning of, or that you defined/explained for me, and capture those. Use the surrounding conversation as each word's context/sense. If you find none, tell me there were no looked-up words in this session and stop (don't invent any).

Capture them into `data/vocab/vocab.json` following the spec below — including the
**required self-review pass**:

@prompts/lookup_word.md

Field definitions and controlled vocabulary:

@templates/vocab_schema.md

Then:
1. **Render the list**: run `python3 scripts/render_vocab_md.py` (newest first, at `data/vocab/vocab.md`).
2. **Report back** in one or two lines: how many words were added, how many were repeat lookups (count bumped), what the self-review changed (or "no changes"), and that the list is at `data/vocab/vocab.md`. Don't restate every definition.

---
description: Save unfamiliar words to the vocabulary store (from arguments, or harvested from this session), with a self-review pass
argument-hint: "[word(s), optional; empty = harvest from this chat session]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## Today's date
!`date +%F`

> Use **exactly** this date for every `first_seen` / `review.last_seen` you write or bump. Do **not** infer "today" from memory, the conversation, or any system message — only the value printed above is authoritative.

## Current vocabulary
!`python3 scripts/list_vocab.py`

## Task
You are my English vocabulary assistant. Decide which words to capture:

- **If `$ARGUMENTS` is non-empty**: those are the word(s) to save (may be several, and may include the sentence/context where I met them).
- **If `$ARGUMENTS` is empty**: harvest from **this chat session's conversation** — scan our earlier messages for English words I asked the meaning of, or that you defined/explained for me, and capture those. Use the surrounding conversation as each word's context/sense. If you find none, tell me there were no looked-up words in this session and stop (don't invent any).

**Filter before capturing** — only keep words/phrases that are worth studying, i.e. common and useful enough that I'm likely to meet or reuse them. **Skip and don't save**:
- Words too rare/obscure/archaic, or hyper-specialized jargon I'm unlikely to encounter again.
- Words so basic I obviously already know them.
- Proper nouns (names of people, places, brands) and one-off transcription noise.
When I pass words explicitly as arguments, still apply this filter but be lenient — if I asked for it, lean towards keeping it. Tell me which ones you skipped and why (briefly).

Capture the remaining words into `data/vocab/vocab.json` following the spec below — including the
**required self-review pass**:

@prompts/lookup_word.md

Field definitions and controlled vocabulary:

@templates/vocab_schema.md

Then:
1. **Render the list**: run `python3 scripts/render_vocab_md.py` (newest first, at `data/vocab/vocab.md`).
2. **Report back** in one or two lines: how many words were added, how many were repeat lookups (count bumped), how many were skipped by the filter (and why, briefly), what the self-review changed (or "no changes"), and that the list is at `data/vocab/vocab.md`. Don't restate every definition.

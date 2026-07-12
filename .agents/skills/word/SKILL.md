---
name: word
description: Record useful English words or phrases that Jack looked up in the current conversation into the repository vocabulary store, deduplicating entries and refreshing vocab.md. Use when the user invokes $word, asks to save or record vocabulary, supplies words to add, or asks to harvest unfamiliar words from the current chat.
---

# Record Vocabulary

Update the existing vocabulary list without modifying lesson transcripts.

## Select words

1. Read `CLAUDE.md`, `prompts/lookup_word.md`, and `templates/vocab_schema.md` completely.
2. With arguments, process the supplied words or phrases. Without arguments, collect the English words or phrases Jack asked to have explained in the current conversation.
3. Skip obvious noise, proper nouns, highly obscure terms, and words that are not useful for study; be lenient with explicitly supplied items.
4. Preserve the sense from Jack's context. If the intended sense is genuinely ambiguous, ask one concise question before writing.

## Update the store

1. Run `date +%F` and use its output for lookup dates.
2. Treat `data/vocab/vocab.json` as the source of truth and deduplicate by lowercase lemma.
3. For a new item, append one schema-valid entry with a concise English definition and a short, natural first example.
4. For an existing item, keep `first_seen`, increment `review.times_looked_up`, and set `review.last_seen` to today's date. Update the definition or examples only when needed for correctness or the encountered sense.
5. Preserve unrelated entries and existing review status. Never edit `data/raw/`.

## Review and verify

1. Recheck each changed entry for meaning, part of speech, natural examples, contextual sense, controlled tags, deduplication, and lookup counts; fix any problem found.
2. Run `python3 scripts/render_vocab_md.py` to rebuild `vocab.md`.
3. Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests`.

## Report

Report the words added, repeated words updated, self-review changes (or `no changes`), and the `vocab.md` path. Do not print the whole vocabulary table.

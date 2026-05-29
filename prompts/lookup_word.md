# Prompt: capture a looked-up word

Use this when I look up unfamiliar word(s). The single source of truth is
`data/vocab/vocab.json` (one growing JSON array). Field definitions and the
controlled vocabulary are in `templates/vocab_schema.md`.

---

First, **filter out words not worth studying**: skip ones too rare/obscure/archaic or hyper-specialized to reuse, ones so basic I clearly already know, and proper nouns or transcription noise. Keep only common, useful words. (For words I passed explicitly, be lenient.)

For each remaining word to capture (passed as arguments, or harvested from this session):

1. **Deduplicate first**: search `data/vocab/vocab.json` for the same lowercase `word`.
   - **Not there** → append a new entry with `first_seen` = today and `review.times_looked_up` = 1.
   - **Already there** → do NOT add a duplicate. Bump `review.times_looked_up` by 1 and set `review.last_seen` to today (keep the original `first_seen`).
2. **Fill the fields** (see `templates/vocab_schema.md`):
   - `definition`: concise English.
   - `example`: the **first** sentence must be short, everyday, and make the usage instantly obvious; an optional 2nd can be more advanced.
   - `pos`, and where useful `synonyms`, `topic`, `note`.
   - If I gave context (the sentence/scene where I met the word), record the **sense that matches that context** — a word can have several meanings; pick the right one.

Requirements:
- Definitions and examples are in **English**.
- Use the controlled `pos` / `topic` vocabulary; don't invent synonyms for tags.
- Keep `vocab.json` a valid JSON array.

## Self-review pass (required)
After writing, re-check every entry you just added or updated:
- **Definition accurate** and `pos` correct.
- **Example correct**: natural, grammatical, and it actually uses *this* word in *this* sense (not a different meaning).
- **Sense matches context**: if I gave a source sentence, the recorded meaning is the one I actually encountered.
- **Dedup is right**: no duplicate entries; `times_looked_up` / `last_seen` updated correctly.

Fix anything wrong in `vocab.json` before rendering. In your final report, note what the review changed (e.g. "fixed 1 sense") or "no changes".

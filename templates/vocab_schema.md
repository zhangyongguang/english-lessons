# Vocabulary record schema

All looked-up words live in a single growing file: `data/vocab/vocab.json`.
It is a **JSON array**; each element is one word with these fields:

| Field | Description | Required |
|---|---|---|
| `word` | The headword, lowercase lemma (e.g. `eloquent`, `take after`) | ✅ |
| `pos` | Part of speech (controlled, see below) | ✅ |
| `definition` | Concise English definition | ✅ |
| `example` | Array; the **first** is one short, everyday sentence that makes the usage instantly clear; an optional 2nd can be more advanced | ✅ |
| `synonyms` | Array of close synonyms (optional) | ⬜ |
| `topic` | Topic tag for grouping/quizzes (controlled, see below) | ⬜ |
| `note` | Where you saw it / nuance / why you looked it up (optional) | ⬜ |
| `first_seen` | Date you first looked it up, `YYYY-MM-DD` | ✅ |
| `review` | Review-status object, see below | ✅ |
| `source_ref` | Where you encountered it (optional) | ⬜ |

`review` object:
```json
{ "status": "new", "times_looked_up": 1, "last_seen": "2026-05-29" }
```
- `status`: `new` / `learning` / `mastered`
- `times_looked_up`: how many times you've looked it up (≥1; bumped on re-lookup — a stubborn-word signal)
- `last_seen`: date of the most recent lookup (the `vocab.md` table is sorted by this, newest first)

## Deduplication
One word = one entry, keyed by the lowercase `word`. On a repeat lookup, **don't add a new entry**: bump `times_looked_up` by 1 and set `last_seen` to today (keep the original `first_seen`).

## Controlled vocabulary (keep it consistent)

`pos`:
- `noun`, `verb`, `adjective`, `adverb`, `phrase`, `idiom`, `preposition`, `conjunction`, `other`

`topic` (extendable, but reuse existing ones):
daily, business, academic, technology, emotion, communication, health, travel, food, nature, …

> When adding a new topic, record it here. Don't create synonyms.

## Example entry
```json
{
  "word": "eloquent",
  "pos": "adjective",
  "definition": "fluent and persuasive in speaking or writing",
  "example": ["She gave an eloquent speech.", "He's an eloquent writer."],
  "synonyms": ["articulate", "fluent"],
  "topic": "communication",
  "note": "saw it when the teacher defined 'public speaker'",
  "first_seen": "2026-05-29",
  "review": { "status": "new", "times_looked_up": 1, "last_seen": "2026-05-29" }
}
```

# Error record schema

Each day's errors are stored as a **JSON array**, file
`data/errors/json/YYYY-MM/YYYY-MM-DD.json` (sharded by year-month). The readable
report is generated alongside at `data/errors/md/YYYY-MM/YYYY-MM-DD.md`.
Every element is one error with these fields:

| Field | Description | Required |
|---|---|---|
| `id` | Unique id, suggested `date-index`, e.g. `2026-05-29-001` | ✅ |
| `date` | Class date `YYYY-MM-DD` | ✅ |
| `category` | Top-level category (see controlled vocabulary below) | ✅ |
| `tag` | Fine-grained tag (see below), for pattern stats | ✅ |
| `my_sentence` | What you said (may be garbled by speech-to-text; restore your intended meaning) | ✅ |
| `correction` | The teacher's correct version; multiple separated by ` / ` | ✅ |
| `explanation` | Why it's wrong and what the rule is (in English) | ✅ |
| `correct_examples` | 1–2 correct example sentences, an array | ✅ |
| `context` | What you were talking about (optional) | ⬜ |
| `review` | Review-status object, see below | ✅ |
| `source_ref` | Location in the transcript, e.g. `line 412` (optional) | ⬜ |

`review` object:
```json
{ "status": "new", "times_seen_again": 0, "last_reviewed": null }
```
- `status`: `new` / `learning` / `mastered`
- `times_seen_again`: how many times you made it again afterwards (tracks stubborn errors)
- `last_reviewed`: last review date, or null

## Controlled vocabulary (keep it consistent so stats stay accurate)

`category` (top level, fixed to these 6):
- `grammar`
- `vocabulary` (word choice)
- `collocation`
- `naturalness` (un-idiomatic / L1-influenced phrasing)
- `pronunciation`
- `discourse` (cohesion / fluency)

`tag` (fine-grained, extendable, but reuse existing ones where possible):
articles, tense, aspect, preposition,
plural, agreement, word-order,
adverb, conditional, modal,
phrasal-verb, false-friend, register,
filler, linking, stress,
comparative, relative-clause, word-choice,
pronoun (missing / wrong personal or possessive pronouns, inconsistent subject),
possessive (missing noun possessive 's, e.g. "the school reputation" → "the school's reputation"),
conciseness (tighten / combine clauses, avoid comma splices), word-boundary (compound-word boundaries / blending into one word),
minimal-pair (confusable consonant/vowel sounds, e.g. sales/share, shown/sure),
verb-form (errors in forming the verb group: omitted/extra auxiliary, missing 'be' in the passive, wrong gerund/infinitive complement after a verb), …

> When adding a new tag, record it here. Don't create synonyms (e.g. don't keep both `prep` and `preposition`).

# Training mastery schema

Long-term target state lives in `data/training/mastery.json`, keyed by stable target ID.

```json
{
  "past-tense-narrative": {
    "status": "learning",
    "introduced_week": "2026-W28",
    "last_practiced": "2026-07-12",
    "next_review": "2026-07-13",
    "sessions": 1,
    "total_opportunities": 12,
    "correct_first_attempt": 7,
    "successful_self_corrections": 3,
    "delayed_correct": 1,
    "delayed_total": 2,
    "transfer_contexts": ["daily-life", "work"],
    "consecutive_unprompted_passes": 0
  }
}
```

Allowed states: `new`, `learning`, `reviewing`, `mastered`, `relapsed`.

Do not mark a target mastered from immediate repetition. Require at least two unprompted passes on different days, at least 80% first-attempt accuracy, a delayed retest, and successful use in two contexts.

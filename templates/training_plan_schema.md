# Weekly training plan schema

One plan covers one ISO week and contains exactly three observable speaking targets.

The structured source is `data/training/plans/json/WEEK.json`; the readable plan is `training/plans/WEEK.md`.

## Required plan fields

| Field | Description |
|---|---|
| `week` | ISO week, for example `2026-W28` |
| `source_window` | First and last ISO weeks analyzed |
| `targets` | Array containing exactly three targets |

## Required target fields

| Field | Description |
|---|---|
| `id` | Stable lowercase hyphenated identifier |
| `name` | Narrow learner-facing goal |
| `reason` | Why it was selected now |
| `source_tags` | Relevant error-log tags |
| `recent_errors` | Count in the requested week |
| `recent_days` | Distinct lesson days in the requested week |
| `window_errors` | Count in the complete analysis window |
| `trigger` | Situation in which the form should be used |
| `error_examples` | Two or three real mistake/correction pairs |
| `success_criteria` | Numeric assessment requirements |

Minimum success criteria are 10 opportunities, 80% first-attempt accuracy, one delayed retest, and two transfer contexts. Keep prompted correction and first-attempt performance separate.

The Markdown rendering must contain: three targets, evidence, target forms, success criteria, a five-session schedule, and instructions for Chat Live.

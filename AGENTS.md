# Codex project guidance

Read `CLAUDE.md` for the complete project conventions, data layout, speaker identities, controlled vocabularies, and generated-file rules. Those rules apply to Codex too.

Repository Skills:

- `$extract` — process transcripts, rebuild error outputs, and refresh weekly training.
- `$training-loop` — show or refresh `training/live/current.md`, process Chat Live reports, and update mastery.
- `$sync` — explicitly commit and push intentional changes with an English message.

Run `python3 -m unittest discover -s tests` and `python3 scripts/validate.py` after relevant changes. Never modify `data/raw/`.

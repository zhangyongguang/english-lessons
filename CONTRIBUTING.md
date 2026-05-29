# Contributing

Thanks for your interest! This is a small, dependency-free toolkit that turns
English-class transcripts into a structured error log and vocabulary store, used
with Claude Code slash commands.

## Principles (please keep these)

- **Pure standard library.** Scripts must run on Python 3 with no `pip install`.
  Tests use the stdlib `unittest`. Don't add runtime dependencies.
- **Raw data is never modified.** Files under `data/raw/` are the source of truth
  and must not be renamed or edited. All processing produces new files.
- **Generated files are generated, not hand-edited.** `*.md` reports,
  `database/errors_master.csv`, and `exercises/anki/*.tsv` are produced by scripts.
  Change the script, then regenerate.
- **Controlled vocabulary.** Categories/tags/pos/topics live in `templates/*.md`.
  Reuse existing values; record any new tag/topic there instead of inventing
  synonyms.
- **Two subsystems, shared helpers.** The errors and vocab pipelines share
  `scripts/_common.py`. Put common logic there rather than duplicating it.

## Project layout

See the directory map in [README.md](README.md). In short: `.claude/commands/`
holds the slash commands, `prompts/` the prompt sources they reference,
`scripts/` the deterministic Python tools, `templates/` the schemas.

## Before you open a PR

Run the checks locally (both must pass; CI runs the same):

```bash
python3 -m unittest discover -s tests   # unit tests
python3 scripts/validate.py             # data/schema validation
```

If you changed a script that produces output, regenerate and confirm the data
files are untouched:

```bash
python3 scripts/build_master.py
python3 scripts/make_anki.py
python3 scripts/render_vocab_md.py
python3 scripts/make_vocab_anki.py
git status --short data/   # should show no changes to data/raw or *.json sources
```

## Privacy note

Real transcripts under `data/raw/` may contain personal classroom conversation.
If you fork this for your own use and host it publicly, consider uncommenting
`data/raw/` in `.gitignore` to keep transcripts local.

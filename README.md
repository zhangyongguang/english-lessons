# english-lessons — my English error log

Turn the Tencent Meeting transcripts of my daily 3-hour 1-on-1 class into a structured error log,
using **Claude Code** slash commands to extract errors, find patterns, generate practice, and export to Anki — all in one step.

## The commands (type `/` in Claude Code)

| Command | What it does | Output |
|---|---|---|
| `/extract [date\|all]` | Extract my errors from pending transcripts | `data/errors/DATE.md` (readable) + `.json` |
| `/weekly [week]` | Summarize a week, analyze high-frequency weak spots | `analysis/weekly/YEAR-Wnn.md` |
| `/exercise [tag]` | Generate targeted practice by weak spot | `exercises/generated/...md` |
| `/anki` | Export error Anki cards | `exercises/anki/anki_import.tsv` |
| `/word [word(s)]` | Save looked-up words (or harvest them from this chat) | `data/vocab/vocab.md` + `vocab.json` |
| `/vocab-quiz [topic]` | Quiz from recent/unmastered words | `exercises/generated/...md` |
| `/vocab-anki` | Export vocab Anki cards | `exercises/anki/vocab_anki.tsv` |
| `/sync [message]` | Commit and push changes to GitHub | — |

All arguments are optional:
- `/extract` defaults to the "most recent pending" date; `/extract 2026-05-28` targets one day; `/extract all` clears everything that piled up.
- `/weekly` defaults to the "most recent pending" week; `/weekly 2026-W22` targets one week.
- `/exercise articles` drills a single tag.
- `/word eloquent junkyard` saves those words; bare `/word` harvests the words you asked about in the current session.

## How "new today/this week" is determined

Not based on the system clock or download time, but on **whether it's been processed** (idempotent):
- **Day**: a transcript for some date exists in `data/raw/` but `data/errors/DATE.json` does not → that day is "pending". The date is parsed from the Tencent filename (`_20260528...` → 2026-05-28).
- **Week**: an ISO week has errors but `analysis/weekly/YEAR-Wnn.md` does not exist → that week is "pending".

So which day you backfilled, several recordings per day, or backfilling missed days later — none of it matters, and re-running won't reprocess.
Check status anytime: `python3 scripts/list_raw.py` (by day), `python3 scripts/list_weeks.py` (by week).

## Directory layout

```
english-lessons/
├── CLAUDE.md               # project notes, auto-loaded by Claude Code (the "rules")
├── .claude/commands/       # ★ the slash commands
│   ├── extract.md  weekly.md  exercise.md  anki.md  sync.md
│   └── word.md  vocab-quiz.md  vocab-anki.md
├── data/
│   ├── raw/                # raw transcripts, original Tencent filename (date inside), never modified
│   ├── processed/          # cleaned versions (optional)
│   ├── errors/             # DATE.json (structured) + DATE.md (readable)
│   └── vocab/              # vocab.json (single growing store) + vocab.md (readable, newest first)
├── database/errors_master.csv    # master table of all errors (script-generated)
├── exercises/{generated,anki}/   # practice + Anki files (anki_import.tsv = errors, vocab_anki.tsv = words)
├── analysis/weekly/        # weekly pattern reports
├── prompts/                # the prompts; commands reference them via @ as the single source of truth
├── scripts/                # small tools (pure standard library, no network or install)
│   ├── list_raw.py  list_weeks.py  render_md.py  build_master.py  make_anki.py  new_day.py
│   └── render_vocab_md.py  make_vocab_anki.py  list_vocab.py
├── templates/error_schema.md     # field definitions + tag vocabulary for each error
└── templates/vocab_schema.md     # field definitions + tag vocabulary for each word
```

## Setup

1. Open this folder in Claude Code — `.claude/commands/` is auto-detected, so typing `/` shows `extract`, `weekly`, etc.; `CLAUDE.md` is auto-loaded as project context.
2. You need Python 3 installed (scripts run with `python3`; on Windows use `python`).

> Note: newer Claude Code merges slash commands into Skills (`.claude/skills/`), but `.claude/commands/` still works fully. For these manually-invoked commands, `commands` is simpler.

## Design ideas

1. **raw is never changed**: the raw transcript is the source; all processing produces new files for traceability.
2. **Structured + readable, two tracks**: `/extract` first has Claude extract errors into structured JSON (unified fields/tags, see `templates/error_schema.md`), then a script renders a quick-browse Markdown table. JSON feeds stats and Anki; the Markdown is for you.
3. **Claude thinks, scripts do the legwork**: extraction/analysis/exercises rely on Claude + prompts; listing, rendering, merging, exporting rely on scripts — deterministic and token-cheap.
4. **"Processed or not" determines what's new**: see the section above — idempotent, clock-independent.

## A few notes

- **Transcripts have errors** (especially accented English). The commands tell Claude to restore intended meaning from context and trust the teacher's corrections first. Your transcripts have clear speaker labels (`Jack` = you, `ZIVA_Teacher` = the teacher), so accuracy is decent.
- **Privacy**: transcripts contain class conversation. If hosting on a public Git repo, consider uncommenting `data/raw/` in `.gitignore`.

---
Works without Claude Code too (manual verification):
```bash
python3 scripts/list_raw.py            # which days are pending
python3 scripts/render_md.py 2026-05-28
python3 scripts/build_master.py
python3 scripts/list_weeks.py          # which weeks are pending
python3 scripts/make_anki.py
```

---
name: save-note
description: Normalize pasted Markdown about English grammar, words, phrases, or questions and save it as a dated study note in this repository. Use when the user invokes $save-note, pastes English-learning notes to archive, or asks to save a ChatGPT English discussion as Markdown.
---

# Save an English Study Note

Save user-provided learning notes without modifying transcripts, error records, or vocabulary data.

## Prepare the note

1. Read `CLAUDE.md` and `templates/study_note_template.md` completely.
2. Require actual note content. If `$save-note` is invoked without pasted content in the current conversation, ask the user to paste it.
3. Preserve the user's meaning, useful detail, and English examples. Correct only clear Markdown, spelling, or factual errors; do not silently invent learning conclusions.
4. Normalize the content to the template while omitting sections that have no useful content. Keep Chinese explanations when supplied and keep English examples in English.
5. Use a concise descriptive title and add the date returned by `date +%F`.

## Choose the path

1. Save notes under `notes/questions/YYYY-MM/` using the current date from `date +%F`.
2. Name the file `YYYY-MM-DD-topic.md`, with a short lowercase ASCII kebab-case topic inferred from the content.
3. Never overwrite an unrelated existing note. If the path exists, merge only when it clearly covers the same conversation; otherwise add a short distinguishing topic or numeric suffix.

## Review and report

1. Re-read the saved file and check that headings are consistent, code uses backticks or fenced blocks, tables render correctly, and no supplied question or conclusion was lost.
2. Run `python3 scripts/validate.py`, `python3 -m unittest discover -s tests`, and `git diff --check`.
3. Report the saved note path and any substantive correction made. Do not repeat the whole note.

Never modify files under `data/raw/`.

# Prompt: extract errors from a transcript (daily use)

Send this prompt + that day's `data/raw/YYYY-MM-DD.txt` to Claude.

---

You are my spoken-English teaching assistant. Below is the Tencent Meeting speech transcript of a 1-on-1 English class (mixed Chinese/English, and **the transcript itself may have recognition errors**, especially for the English I speak).

Speaker labels: `Jack` is the student (me), `ZIVA_Teacher` is the teacher. A day may have several recording sessions — process them together. In the filename, the digits in `_20260528210658-` are YYYYMMDDhhmmss; the first 8 are the class date.

Extract "the mistakes I (Jack) made + the teacher's (ZIVA_Teacher) corrections" and output a **JSON array**, each item strictly matching this structure:

```json
{
  "id": "date-3digit-index, e.g. 2026-05-29-001",
  "date": "YYYY-MM-DD",
  "category": "one of: grammar | vocabulary | collocation | naturalness | pronunciation | discourse",
  "tag": "fine-grained tag, e.g. articles / tense / preposition / adverb",
  "my_sentence": "what I said (if the transcript is clearly wrong, restore what I meant)",
  "correction": "the teacher's correct version; separate multiple with ' / '",
  "explanation": "explain in English why it's wrong and what the rule is",
  "correct_examples": ["correct example 1", "correct example 2"],
  "context": "what we were talking about (brief)",
  "review": { "status": "new", "times_seen_again": 0, "last_reviewed": null },
  "source_ref": "rough location in the transcript, e.g. 'line 88'; empty string if none"
}
```

Requirements:
1. Only extract **real language errors** and clear corrections; don't treat normal conversation as errors.
2. **Focus on sentence-level expression** (structure, collocation, word order, tense/agreement, natural phrasing). Don't create entries for single vocabulary words; I'll look isolated word choices up myself.
3. Some of `Jack`'s lines are slips or transcription errors, others are real language errors; use whether the teacher corrected it to judge.
4. If the teacher didn't say it explicitly but you're sure of a more natural version, you may add it, but mark "(assistant note)" in `explanation`.
5. Use the controlled vocabulary for category and tag (see templates/error_schema.md); don't invent synonym tags.
6. Output the JSON array directly — **no** surrounding text, no Markdown code fences.

> Write `explanation` and `correct_examples` in **English**. Keep `my_sentence` / `correction` as the original English.
> The rendered `DATE.md` shows only the "Mistake / Correct" two columns (handled by the script), so fill in all other JSON fields as usual — they feed the stats and Anki.

# Prompt: generate a vocabulary quiz

Send this + the words to test (the whole `data/vocab/vocab.json`, a topic, or the
most recent / not-yet-mastered words) to Claude.

---

Based on my vocabulary list below, build a quiz to check I really know these words. Requirements:

- Test in **new sentences/contexts**, never reuse the example sentences stored with the word (otherwise I'm just recalling them).
- Mix question types:
  1. **Meaning**: give the word, I pick/recall the definition.
  2. **Fill in the blank**: a sentence with the word blanked out; I supply it from context.
  3. **Usage choice**: pick the sentence that uses the word correctly among 2–3 options.
  4. **Production**: write my own sentence using the word correctly.
- 10 questions, gradually harder.
- Keep **questions and answers separate**: all questions first, then a combined "answers + one-line note" section, so I can self-test first.

If I specify a topic or a set of words, quiz only those; otherwise prioritize words that are `new`/`learning` or were looked up more than once.

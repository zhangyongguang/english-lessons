---
name: explain-word
description: Explain an unfamiliar English word or phrase to Jack in exactly one short sentence using simple English. Use when the user invokes $explain-word, provides a word or phrase for its meaning, asks what an English expression means, or requests a simple English definition without asking to save it.
---

# Explain a Word or Phrase

1. Identify the meaning that matches any context the user provides; otherwise use the most common everyday meaning.
2. Reply in English with exactly one short sentence.
3. Use simpler, more common words than the item being explained.
4. Include the word or phrase and its meaning in the sentence, normally as: `“X” means ... .`
5. Prefer a plain definition; add a tiny clarifying example within the same sentence only when the definition alone may be unclear.
6. Do not use Chinese, multiple senses, pronunciation, etymology, formatting, or extra commentary unless the user explicitly requests it.
7. Do not update vocabulary files; use `$word` separately when the user asks to record the item.

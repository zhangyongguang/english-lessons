# Prompt: analyze error patterns (weekly / monthly)

Send this + `database/errors_master.csv` (or the last few days' errors JSON) to Claude.

---

This is my recent English error log. Help me analyze the patterns. The goal is to find a **few high-frequency weak spots** so I can focus my effort instead of spreading it evenly.

Give me:
1. **Error distribution**: counts and percentages by category and tag, sorted high to low.
2. **Stubborn errors**: errors with a high `times_seen_again`, or the same kind recurring — call them out separately.
3. **3 priorities for the week**: based on the data, the 3 things I should fix first; for each give a one-line diagnosis and one minimal practice suggestion.
4. **Progress signals**: compared with earlier data, which tags are decreasing (if there's enough data).

Write in English, be concise, conclusions first then data. Don't pile on jargon.

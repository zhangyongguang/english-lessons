# Live training result schema

Chat Live must end every session with this Markdown block so the result can later be normalized into JSON.

```markdown
## Training report

Date: YYYY-MM-DD
Week: YYYY-Wnn
Session: 1–5

| Target ID | Opportunities | Correct first attempt | Self-corrected | Still wrong after help | Delayed correct / total | Transfer contexts |
|---|---:|---:|---:|---:|---:|---|
| target-id | 0 | 0 | 0 | 0 | 0 / 0 | context-1, context-2 |

Errors to revisit:
- Said: ...
  Correct: ...

Retrieve next time:
- ...

Recommended next action: repeat / advance / assess
```

Rules:

- Count an opportunity whenever the prompt naturally requires the target form.
- `Correct first attempt` excludes prompted repairs and repetitions.
- `Self-corrected` means Jack repaired the form before being given the answer.
- Record at most five representative errors, not the entire conversation.

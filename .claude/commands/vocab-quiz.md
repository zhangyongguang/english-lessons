---
description: Generate a quiz from recent / not-yet-mastered vocabulary
argument-hint: "[topic or word(s), optional]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## Vocabulary status
!`python3 scripts/list_vocab.py`

## Task
Read `data/vocab/vocab.json`. If `$ARGUMENTS` specifies a topic or specific words,
quiz only those; otherwise prioritize words that are `new`/`learning` or were looked
up more than once.

Following the requirements below, write a 10-question quiz (new contexts, questions
and answers kept separate) to `exercises/generated/<date>-vocab-quiz.md`, and tell me
the file path:

@prompts/vocab_quiz.md

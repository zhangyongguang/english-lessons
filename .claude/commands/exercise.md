---
description: 根据最近的错误生成针对性练习（改错/填空/翻译/选择）
argument-hint: "[标签，可选，如 articles]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## 刷新总表
!`python3 scripts/build_master.py`

## 任务
读取 `database/errors_master.csv`。如果 `$ARGUMENTS` 指定了标签（如 `articles`），只围绕那个标签出题；否则覆盖我最高频的 3 个弱点。

按下面的要求出 10 题（用全新句子，不要照搬我的原句；题目与答案分开），写入 `exercises/generated/<日期>-<主题>.md`，并告诉我文件路径：

@prompts/generate_exercises.md

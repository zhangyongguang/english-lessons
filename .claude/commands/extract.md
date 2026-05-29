---
description: 从最新的腾讯会议转写提取我(Jack)的英语错误，生成易读的 Markdown 报告
argument-hint: "[日期，可选，如 2026-05-28]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write, Glob
---

## 待处理的转写
!`python3 scripts/list_raw.py`

## 任务
你是我的英语口语老师助理。结合上面的列表：

1. **确定要处理的日期**：
   - 若 `$ARGUMENTS` 是某个日期（如 `2026-05-28`），处理那一天。
   - 若 `$ARGUMENTS` 是 `all`，把上面**所有**「待提取」的日期从早到晚依次全部处理（攒了好几天没整时用这个）。
   - 若 `$ARGUMENTS` 为空，处理「最近一个待提取」的那一天。
   - 若没有任何待提取日期，告诉我并停止。
   下面第 2–5 步对每个要处理的日期 DATE 各做一遍。
2. **读取转写**：用 Glob/Read 读取 `data/raw/` 下文件名包含 DATE 那串数字（如 `20260528`）的所有 `.txt`。一天可能有多段录音，全部读取、合并处理。
3. **提取错误**：按下面的要求和字段规范，提取「`Jack`（学生＝我）犯的错 + `ZIVA_Teacher`（老师）的纠正」，写入 `data/errors/DATE.json`（JSON 数组，多段录音合并，id 连续编号 `DATE-001`、`DATE-002`…）。

提取要求：

@prompts/extract_errors.md

字段定义与受控标签词表：

@templates/error_schema.md

4. **渲染报告**：运行 `python3 scripts/render_md.py DATE`（生成「错误 / 正确」两列表格）。
5. **更新总表**：运行 `python3 scripts/build_master.py`。
6. **汇报**：用一句话告诉我提取了几条、报告在 `data/errors/DATE.md`。不要逐条复述、不要额外解释（解释我会自己查）。

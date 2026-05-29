---
description: 汇总某一周的英语错误，分析高频弱点，输出每周报告
argument-hint: "[ISO 周，可选，如 2026-W22]"
allowed-tools: Bash(python3:*), Bash(python:*), Read, Write
---

## 刷新总表
!`python3 scripts/build_master.py`

## 各周状态（待汇总 / 已汇总）
!`python3 scripts/list_weeks.py`

## 任务
1. **确定要汇总的周 WEEK**：若 `$ARGUMENTS` 给了 ISO 周（如 `2026-W22`）就用它；否则取上面「最近一个待汇总」的周。若没有待汇总的周，告诉我并停止。
2. 读取 `database/errors_master.csv`，**只筛选属于 WEEK 这一周**的错误（按每行的 `date` 判断其 ISO 周是否等于 WEEK）。
3. 按下面的要求做规律分析，写入 `analysis/weekly/WEEK.md`（如 `analysis/weekly/2026-W22.md`），中文，先结论后数据，简洁：

@prompts/analyze_patterns.md

4. 用一句话告诉我这一周最该攻克的那个点。

---
description: 把错误库导出成 Anki 可导入的卡片文件
allowed-tools: Bash(python3:*), Bash(python:*)
---

## 生成卡片
!`python3 scripts/build_master.py`
!`python3 scripts/make_anki.py`

## 任务
根据上面的输出，告诉我：生成了多少张卡片、文件在 `exercises/anki/anki_import.tsv`，以及导入方法 —— Anki ▸ File ▸ Import，分隔符选 **Tab**，三列分别映射到 正面 / 背面 / 标签。

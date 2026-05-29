# 项目：英语错题库（english-lessons）

把每天 1v1 英语课的腾讯会议转写，沉淀成结构化错题库，用来复习、找规律、出练习、导 Anki。

## 关键约定
- **原始转写**放 `data/raw/`，保留腾讯下载的原文件名；**日期藏在文件名里**：`..._20260528210658-...` 前 8 位即上课日期（2026-05-28）。不要重命名。
- **说话人**：`Jack` = 我（学生），`ZIVA_Teacher` = 老师。只提取 Jack 的错误 + 老师的纠正。
- **一天可能多段录音**，按天合并成一份错题。
- **每条错误的字段和受控标签词表**见 `templates/error_schema.md`，务必遵守，不要自造同义标签。
- **错误存两份**：`data/errors/日期.json`（结构化，喂统计和 Anki）+ `日期.md`（易读，由脚本生成）。
- **raw 永不修改**，所有加工都生成新文件。
- 转写有语音识别噪声、中英混杂；按上下文还原我的本意，**老师的纠正更可靠，优先采信**。

## 命令（输入 `/` 调用）
- `/extract [日期|all]` — 提取错误 → `data/errors/日期.md` + `.json`
- `/weekly [周]` — 周规律汇总 → `analysis/weekly/`
- `/exercise [标签]` — 生成针对性练习 → `exercises/generated/`
- `/anki` — 导出 Anki 卡片 → `exercises/anki/anki_import.tsv`

## "新增"是怎么判断的（重要）
不依赖系统时钟或文件下载时间，而是看**有没有被处理过**：
- **天**：`data/raw/` 里某日期的转写存在，但 `data/errors/日期.json` 不存在 → 该日「待提取」。`/extract` 默认处理「最近一个待提取」；`/extract all` 把所有待提取日补齐。
- **周**：某 ISO 周有错误数据，但 `analysis/weekly/年-周.md` 不存在 → 该周「待汇总」。`/weekly` 默认处理「最近一个待汇总」。
- 好处：哪天补的、一天几段录音、漏了几天再补，都不影响；重复运行不会重复处理（幂等）。
- 看状态：`python3 scripts/list_raw.py`（按天）、`python3 scripts/list_weeks.py`（按周）。

## 脚本（纯标准库，无需联网或装依赖）
- `scripts/list_raw.py` — 列出转写、标出哪天待提取
- `scripts/list_weeks.py` — 按 ISO 周列出错误、标出哪周待汇总
- `scripts/render_md.py 日期` — 日期.json → 易读的 日期.md
- `scripts/build_master.py` — 合并每天 JSON → 总表 CSV
- `scripts/make_anki.py` — 总表 → Anki 导入文件
- 运行用 `python3`（Windows 用 `python`）。

# english-lessons —— 我的英语错题库

把每天 3 小时 1v1 课的腾讯会议转写，沉淀成结构化错题库，
用 **Claude Code** 斜杠命令一键提取错误、找规律、出练习、导 Anki。

## 四个命令（在 Claude Code 里输入 `/`）

| 命令 | 作用 | 产出 |
|---|---|---|
| `/extract [日期\|all]` | 从待提取的转写里提取我的错误 | `data/errors/日期.md`（易读）+ `.json` |
| `/weekly [周]`  | 汇总某一周、分析高频弱点 | `analysis/weekly/年-周.md` |
| `/exercise [标签]` | 按弱点生成针对性练习 | `exercises/generated/...md` |
| `/anki` | 导出 Anki 卡片 | `exercises/anki/anki_import.tsv` |

参数都可省：
- `/extract` 默认处理「最近一个待提取」的日期；`/extract 2026-05-28` 指定某天；`/extract all` 把攒下的几天一次补齐。
- `/weekly` 默认汇总「最近一个待汇总」的周；`/weekly 2026-W22` 指定某周。
- `/exercise articles` 只练某个标签。

## "今天/本周新增的"是怎么判断的

不靠系统时钟或文件下载时间，而是看**处理过没有**（幂等）：
- **天**：`data/raw/` 里有某天的转写、但 `data/errors/日期.json` 还不存在 → 该天「待提取」。日期是从腾讯文件名里解析的（`_20260528...` → 2026-05-28）。
- **周**：某 ISO 周有错误、但 `analysis/weekly/年-周.md` 还不存在 → 该周「待汇总」。

所以哪天补的、一天几段录音、漏几天再补都不影响，重复运行也不会重复处理。
随时看状态：`python3 scripts/list_raw.py`（按天）、`python3 scripts/list_weeks.py`（按周）。

## 目录结构

```
english-lessons/
├── CLAUDE.md               # 项目说明，Claude Code 每次自动加载（相当于"规则"）
├── .claude/commands/       # ★ 四个斜杠命令
│   ├── extract.md  weekly.md  exercise.md  anki.md
├── data/
│   ├── raw/                # 原始转写，保留腾讯原文件名（日期在文件名里），永不修改
│   ├── processed/          # 清洗版本（可选）
│   └── errors/             # 日期.json（结构化）+ 日期.md（易读）
├── database/errors_master.csv    # 所有错误汇总总表（脚本生成）
├── exercises/{generated,anki}/   # 练习 + Anki 文件
├── analysis/weekly/        # 每周规律报告
├── prompts/                # 三个提示词，命令用 @ 引用它们做单一事实源
├── scripts/                # 小工具（纯标准库，无需联网或装依赖）
│   ├── list_raw.py  list_weeks.py  render_md.py  build_master.py  make_anki.py  new_day.py
└── templates/error_schema.md     # 每条错误的字段定义 + 标签词表
```

## 安装

1. 用 Claude Code 打开本文件夹即可——`.claude/commands/` 会被自动识别，输入 `/` 就能看到 `extract`、`weekly` 等命令；`CLAUDE.md` 会自动作为项目上下文加载。
2. 需要本机装好 Python 3（命令里跑脚本用 `python3`；Windows 改成 `python`）。

> 说明：Claude Code 较新版本已把斜杠命令并入 Skills（`.claude/skills/`），但 `.claude/commands/` 仍然完全可用。这种自己手动调用的命令用 commands 更简单。

## 设计思路

1. **raw 永远不改**：原始转写是底稿，所有加工都生成新文件，方便回溯。
2. **结构化 + 易读双轨**：`/extract` 先让 Claude 把错误抽成结构化 JSON（统一字段/标签，见 `templates/error_schema.md`），再由脚本渲染成你快速浏览的 Markdown。JSON 喂统计和 Anki，Markdown 给你看。
3. **Claude 动脑、脚本动手**：提取/分析/出题靠 Claude + prompts；列清单、渲染、合并、导出靠脚本，确定且省 token。
4. **靠"处理过没有"判断新增**：见上一节，幂等、不依赖时钟。

## 几个注意点

- **转写会出错**（尤其口音英文）。命令已让 Claude 按上下文还原本意、优先采信老师的纠正。你的转写有清晰说话人标注（`Jack` = 你，`ZIVA_Teacher` = 老师），准确率较高。
- **隐私**：转写含课堂对话。若托管到公开 Git 仓库，建议在 `.gitignore` 取消注释 `data/raw/`。

---
不装 Claude Code 也能跑（手动验证）：
```bash
python3 scripts/list_raw.py            # 哪天待提取
python3 scripts/render_md.py 2026-05-28
python3 scripts/build_master.py
python3 scripts/list_weeks.py          # 哪周待汇总
python3 scripts/make_anki.py
```

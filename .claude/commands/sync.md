---
description: 自动把改动提交并推送到 GitHub（add + commit + push）
argument-hint: "[提交说明，可选；不填则自动生成]"
allowed-tools: Bash(git:*)
---

## 当前改动
!`git status --short`

## 任务
把工作区改动同步到 GitHub。按顺序执行：

1. **若没有任何改动**（上面为空且本地没领先远程）：告诉我「没有要同步的改动」，停止。
2. **暂存全部**：`git add -A`
3. **提交**：
   - 若 `$ARGUMENTS` 非空，用它作为提交说明。
   - 否则自动生成一句中文说明，概括本次改动（如「更新 2026-05-28 错题」「新增 sync 命令」）。
   - 提交信息末尾加一行：`Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
4. **推送**：`git push`（首次或没有上游时用 `git push -u origin main`）。
5. **汇报**：一句话说明提交了什么、推到了哪个分支。失败就把 git 报错原样贴给我。

> 不交互、不反问，直接跑完。

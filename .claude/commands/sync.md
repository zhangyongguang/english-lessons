---
description: Automatically commit and push changes to GitHub (add + commit + push)
argument-hint: "[commit message, optional; auto-generated if omitted]"
allowed-tools: Bash(git:*)
---

## Current changes
!`git status --short`

## Task
Sync working-tree changes to GitHub. Do these in order:

1. **If there are no changes** (the list above is empty and the local branch is not ahead of remote): tell me "nothing to sync" and stop.
2. **Stage everything**: `git add -A`
3. **Commit**:
   - If `$ARGUMENTS` is non-empty, use it as the commit message.
   - Otherwise auto-generate a short message summarizing the change (e.g. "Update 2026-05-28 errors", "Add sync command").
   - Append a final line to the message: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
4. **Push**: `git push` (use `git push -u origin main` on the first push or when there's no upstream).
5. **Report back**: one sentence on what was committed and which branch it went to. On failure, paste the raw git error.

> No interaction, no questions — just run it through.

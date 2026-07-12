---
name: sync
description: Intentionally publish this repository's local changes by reviewing scope, validating relevant work, committing with an English message, and pushing the current branch. Use only when the user explicitly invokes $sync or clearly asks to commit and push/sync changes to Git.
---

# Sync Repository Changes

1. Run `git status --short`, inspect relevant diffs, and check the current branch and upstream.
2. If there are no changes and the branch is not ahead, report `nothing to sync` and stop.
3. Preserve unrelated user changes. Stage only the requested scope unless the user explicitly requests all changes.
4. Run `python3 -m unittest discover -s tests`, `python3 scripts/validate.py`, and `git diff --check` when relevant.
5. Use a provided commit message or generate a concise English imperative subject.
6. Commit non-interactively. Do not amend unless explicitly requested.
7. Push to the configured upstream, or use `git push -u origin <current-branch>` when none exists.
8. Report commit hash, subject, branch, and push result. Preserve the working tree and show raw errors on failure.

Never use destructive Git commands or force-push without exact explicit authorization.

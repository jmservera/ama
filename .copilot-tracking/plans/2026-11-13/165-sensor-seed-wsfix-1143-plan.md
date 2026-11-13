---
title: Issue 165 whitespace fix plan
ms.date: 2026-11-13
---

## Plan

* Phase 1: remove the trailing space at the end of line 6 of the parent critique file; no other change.
* Phase 2: before commit inspect `git diff` (only one 1-char removal on line 6) and run `git diff --check` on the worktree; independent review; commit with `Refs #165`; after commit verify `git diff --check 3b05143179..HEAD` exits 0 and `git diff 3b05143179..HEAD --stat -- src docs` is empty.

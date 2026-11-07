---
title: Issue 149 parent preparation for child 229, phase details
ms.date: 2026-11-07
---

## Phase details

* Phase 1 and 2: `git merge --no-edit origin/test/ux-evidence-149`, then `git merge origin/main -m "chore: adopt main f0afa8d7 into the 149 parent topic"` with the trailer and repository-local privacy email.
* Phase 3: `git diff --stat origin/main...HEAD`, `git diff origin/main...HEAD -- src/core` and blob compare of `role-screens.js` against main.
* Phase 4: from this worktree, install editable `src/core`, `src/agents` and `src/api` into a venv outside the repository if packages are missing (pip), then run the four unittest modules, ruff and mypy per the workflows, with caches under /tmp.

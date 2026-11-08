---
title: Issue 79 details, r21 merge of main a1d26534
ms.date: 2026-11-07
---

## Phase 1: records

* Commit research, plan and details before any merge. Success: planning commit exists; ref `preserve/issue-79-r21-planning` at it.

## Phase 2: merge

* `git fetch origin main`; require `a1d265340` or a score-only descendant. `git merge --no-ff -m "chore: merge main a1d265340 into ranking publication topic (Refs #79)" <main>`. Stop on conflict.

## Phase 3: proof and checks

* `git ls-tree` comparison for every path in `git diff --raw 395060275 a1d265340` and for every path changed by topic versus the pre-merge head.
* Run the commands in the plan with scratch logs `<name>.out`, `<name>.err`, `<name>.exit`.
* Write Changes, one author Review, state JSON and a log entry; commit and freeze.

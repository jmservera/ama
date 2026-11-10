---
title: Issue 111 parent adoption plan critique
ms.date: 2026-11-10
task_id: 111-parent-adoption-1855
---

One pass, by the planning agent (no new agents permitted); verdict compatible with changes. Not independent.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | The commit-complete witness needs a commit whose source matches the reviewed source; a staged-but-uncommitted merge makes the implement-done and review-done checks run on a dirty tree. | Applied: do `git merge --no-ff --no-commit`, validate, then commit. If the witness refuses a dirty tree at implement-done, stop and report rather than heal. |
| 2 | The 22 MSSQL cases may be skipped by the local selector if env gates are missing; skip is not pass. | Applied: pass criterion requires 0 skips and all cases run. |
| 3 | The parent may move between planning and merge. | Applied: recheck the parent and main identities immediately before the merge. |
| 4 | Forced `ConflictError` and `CommittedReloadError` branches stay unproven. | Accepted as reviewed nonblocking gaps; no new tests (no second correction). |
| 5 | Merge may bring changes that fail ruff or mypy outside the sensor files. | Applied: report as parent-owned adverse results; no repair. |

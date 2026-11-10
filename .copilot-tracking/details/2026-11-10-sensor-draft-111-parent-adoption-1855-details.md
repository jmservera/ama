---
title: Issue 111 parent adoption details
ms.date: 2026-11-10
task_id: 111-parent-adoption-1855
---

## Merge procedure

* Preconditions: child clean at `325cb5c0c`; parent still `06374dfca` and ancestor of `origin/main`; recheck with `git fetch` and `git rev-parse` immediately before the merge. If the parent moved, inspect and report instead of assuming.
* Command: `git merge --no-ff --no-commit feat/demo-sensor-review-109-1110`, inspect status, then commit with a conventional merge message, repo-local privacy-safe identity and the Copilot trailer. The merge commit is made after the review and the commit witness in the final phase, so it is staged but uncommitted during validation.
* Conflicts: mechanical append, import or config overlap only; keep both intents; no rebase, reset, amend, force, source transplant or new policy exemption.

## Checks

As listed in the plan. Raw commands, exits, skips and outputs go to `ROOT/checks-111-parent-adoption-1855/`.

## MSSQL script

Reuse the established task-owned pattern of `checks-111-current-mssql-1400/run.sh` as a new script under the new checks directory; random synthetic password never logged; container removed by the script.

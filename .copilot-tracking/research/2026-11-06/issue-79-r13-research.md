---
title: Issue 79 research, continuation r13 (ancestor-preserving alignment with current main)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

This research, plan and details are committed before the merge. No r4 to r12 record, source, test, log or receipt is edited. The r12 state was committed before its separate Review, so its null review pointer is historical chronology; the r12 Review is author-only and its Ruff 0.17.3 and mypy 2.4.1 checks were noncanonical (pins differ). Neither is upgraded here.

## Intake (read before this record)

* Branch `feat/ranking-publication-runner-79`, head `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5`, tree `e806cf3486ec00921ea090fa23ee1e33351f8606`, ignored-inclusive status empty. No remote branch for this branch exists.
* Freshly fetched `origin/main` is `56eec736906774ef56d8c9a66ed7f3f9c1e520c6` (#1236, coordinator agent change); merge base with the branch is `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Parent `origin/feat/case-workbench-integration-73` equals the same `56eec736`, so it is an empty ancestor of main; it is not moved.
* Main added 226 files (agent and tracking material). The branch changed 51 files since `bb3a3b03`. The intersection of the two path sets is empty, and `git merge-tree --write-tree` predicts a clean merge (tree `68884137247e627d70df38e3151a0754e7c21f9f`).
* Package manifest `src/core/pyproject.toml` pins `ruff==0.17.1` and `mypy==2.4.0`.

## Options

* Plain `--no-ff` merge of main: preserves all commits and corrected source, matches r6. Selected.
* Rebase: rewrites history and invalidates evidence. Rejected.
* Retarget or merge into parent73: forbidden.

## Limits

* Light checks only: blob proof, merge provenance, focused tests, pinned Ruff and mypy from an isolated external environment, JSON and link checks. No heavy gate, SQL, browser, build, push or PR. Nothing here is a receipt, independent assessment or acceptance; policy signoff, Legal retention and scheduling remain unproven. The helper race and #1231 corrections stay in the child lane. Planning Readiness: Ready.

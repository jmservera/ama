---
title: Issue 1231 r10 changes (normal local merge of the named parent)
ms.date: 2026-11-06
---

## Execution

Written 2026-11-06 after the actual merge and checks. Prospective commit `629cf02b4` (research, plan, details, critique, state) preceded the merge.

## Changes

* Preserved prealignment ref `backup/issue-1231-29d1669-pre-r10-align` at `29d1669e6ddf09a8566861228c6584d30fba8b51`.
* Normal `git merge --no-ff` of the SHA `d654634fcbe5c82a362e9a3d948d09d0c2993d6d` (parent `feat/ranking-publication-runner-79`, parent not moved). The staged tree matched the recomputed expected tree `1626e65ae99ad9432e201fb24796de3799fc4749`; no conflicts.
* Merge commit `a4d01c1033ca4b67add3e79d0847924130109145`, tree `1626e65ae99ad9432e201fb24796de3799fc4749`, parents `629cf02b45338f796a996f518f5f06af121b1fc8` and `d654634fcbe5c82a362e9a3d948d09d0c2993d6d`.
* No source, test, policy or infrastructure edit and no history rewrite.

## Proofs

* Ancestors of the merge: `43080ab42`, `d654634fc`, `56eec7369`, `29d1669e6`, `629cf02b4`.
* `src`, `infra`, `tools` and `.github/workflows` trees are identical to `29d1669e6`. Outside `.copilot-tracking` only `.github/agents/ama-backlog-delivery-coordinator.agent.md` changed (from main #1236).
* The eight child-corrected source, test and README blobs are identical to `29d1669e6`.
* Main `origin/main` is `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`; local `feat/case-workbench-integration-73` is the same.

## Checks (lightweight, source-bound, outputs under `/mnt/ama-gates/restart-1106-1231-align/`)

| Check | Result |
| --- | --- |
| Import origin | `ranking_publication.py` and `server.py` imported from this worktree (`origins.txt`) |
| Core `test_ranking_publication` and `test_ranking_publication_runner` | 59 tests OK, 0 skipped |
| API `test_ranking_publication_wiring` | 14 tests OK, 0 skipped |
| Ruff check, shared `/tmp/zf79venv` 0.17.3 and pinned 0.17.1 from the r7 api venv, no cache | pass on `src/api` and five core ranking files |
| Ruff format --check, pinned 0.17.1 | `src/api` 115 files formatted; 1 file unformatted: `src/core/src/zava_forward/core/store.py` |
| mypy from `src/core` (268 files) | Success, no issues |
| Ignored-inclusive status after checks | empty |

The `store.py` format finding is pre-existing: the unformatted hunk is an older line (blame `cf9459dc9`), the file is unchanged since `2c4f7c3d8` and identical to the head that passed r9 FULL, whose project groups do not format-check core. It is reported, not edited.

## Limits

Source-bound tests in a shared read-only venv, not an installed-distribution proof. No SQL, browser, image, API-suite or FULL run. The r9 receipt does not verify this head. A fresh FULL, independent exact-head assessment and human approvals are still required.

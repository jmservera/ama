# Issue 1231 r29 final root d99e6901 / main f0afa8d7 reconciliation: changes

Plan: .copilot-tracking/plans/2026-11-07/issue-1231-r29-final-mainf0af-reconciliation-plan.md
Details: .copilot-tracking/details/2026-11-07/issue-1231-r29-final-mainf0af-reconciliation-details.md

## Changes

* Backup ref `backup/issue-1231-5630f-pre-r29-merge` created at 5630fb25.
* Prospective research/plan/details/critique committed first as 9cca0f9c.
* Normal merge (no rebase) of root d99e6901 (contains main f0afa8d7) into the child: merge commit 679e69af, tree 9c6a553f0af2eeb9e010f1d7ad7568d76e900cd3, parents 9cca0f9c and d99e6901.
* Conflicts: 7 paths (ranking README, helper, runner add/add, Store, both core tests, API wiring test). All resolved by taking the child blob; root blobs for these equal bb7e044c, already merged in r28. No hand-merged source.
* Adopted from root unchanged: role-screens.js, test_data_operator_screen.py, test_exception_register_screen.py, score JSON, log.md append, root r27 RPI files, cutover-evidence-pack.md.

## Preservation proof

* src diff vs 5630fb25 contains only the 3 UI files; no ranking production or test blob changed.
* No existing .copilot-tracking path modified (additions only). log.md: 0 deletions against 5630fb25 and f0afa8d7.
* f0afa8d7, d99e6901, 5630fb25 are all ancestors of HEAD. Root worktree untouched.

## Light evidence (own venv, imports resolved to this worktree, PYTHONDONTWRITEBYTECODE=1)

* Core ranking helper+runner: 73 tests OK (exit 0).
* API wiring + exception register + register screen + data operator screen: 65 tests OK (exit 0).
* `tests.test_exception_register.Config`: 2 tests OK. This separately corrects root R26's note that the Config unit is absent; the root note is preserved unedited.
* Ruff check clean, format 332 files already formatted, mypy 128 files clean.
* Ignored-inclusive status empty. Logs under /mnt/ama-gates/g1231-r29-prep-mainf0af-1107/logs.

## Limits

* Light/author evidence only; not FULL, independent, hosted or human approval. Score-only root adoption claims no new runtime checks.

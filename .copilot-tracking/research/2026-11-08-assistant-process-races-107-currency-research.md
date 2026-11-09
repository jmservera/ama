---
title: Currency research and plan for the OS-process race tests against current main (#107, C10)
description: Lineage versus PR 1216, drift of main f548b65 against the local branch, and the single normal merge plan
ms.date: 2026-11-08
---

Task `assistant-process-races-107-currency`, a continuation of `assistant-process-races-107` ([original research](2026-11-07-assistant-process-races-107-research.md), [original plan](../plans/2026-11-07-assistant-process-races-107-plan.md), [critique](../plans/2026-11-07-assistant-process-races-107-critique.md)); all of those and the earlier changes and Review are preserved unchanged. LIGHT preparation only. Not MSSQL, FULL, acceptance or publication.

## Start state (verified)

Worktree `/home/azureuser/source/ama-wt/issue-107-process-races`, branch `test/assistant-process-races-107`, HEAD `ede8bd7011bb352716d8d9d6ba1671b31668da98`, tree `62a49c9464a05ddb088ffa66f1a5af8cfca4e52e`, ignored-inclusive clean. Fetched `origin/main` is `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (tree `32ecad35029eb102f435c7802a29edd148de5642`); merge base is `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`; left-right count is 3 local and 5 on main.

## PR 1216 lineage

The coordinator snapshot (data only) and a read-only `gh pr view 1216` agree: PR 1216 is OPEN, head `docs/paper-scientific-reconciliation` at `50f776c3490458f5456ee9d934a0272aa70e2fd5`, base main, titled "Reconcile the paper with the current five-arm study source".

* Git proof: that commit exists locally, is an ancestor of neither this HEAD nor `origin/main`, and its merge base with this branch is `c6d5a8f3c`. Its diff (17 files, paper and capstone material) touches neither `test_assistant_release.py` nor `assistant_process_worker.py`.
* Conclusion: PR 1216 is an unrelated paper workstream. It is not this candidate, not a parent, child or stack of it, and must not be retargeted, updated, closed or reopened for it. The safe relationship is independent: a future publication is a NEW pull request from `test/assistant-process-races-107` targeting main, with `Refs #107` and `Refs #104` only. Nothing was changed on PR 1216.

## Drift of main against the coupled contracts

* Between the base and `origin/main`, no change touches `assistants.py`, `assistant_release.py`, `release_support.py`, `test_assistants.py`, `test_continuity.py`, the SQL stores, `ai_consumption` or `tools/rpi-checks.py`; a source diff outside tests has zero lines mentioning `assistant_release`, `assistant_allowance`, `used_calls` or `release_context`.
* The `store.py` hunks (lines 1 to 6, 241 to 269 and later) are the ranking publication work (1239/1231), not the release functions. Other main changes are ranking publication, workbench checks, the rubric score JSON and tracking records.
* Main touches neither of my two test files. `git merge-tree` of HEAD and `origin/main` reports no conflict.
* `SQL_SELECTORS` on main still contains `test_assistant_release.MssqlUnleasedRevocation` (line 47), so the new methods remain selected with no `--extra-test` need. `src/README.md` states `--extra-test` is for issue-specific extra selectors and is argv-based; receipts are inert.

Planning Readiness: Ready. No test or fixture reconciliation is expected. A confirmed production defect would be reported as a scoped finding with an owner and not fixed here.

## Plan

* [ ] Commit this prospective record, then make ONE normal merge of the pinned `origin/main` `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (`git merge --no-ff`; no rebase, amend, reset, force or branch move). Stop if main has moved or the merge conflicts.
* [ ] Verify two parents, that the two test files keep their pre-merge blobs, that main's `.github/rubric/scores/latest.json` and canonical records keep main's blobs, and `git diff --check`.
* [ ] LIGHT checks only (SQLite proxy, ruff, mypy, the three-module suite) from a fresh external venv with synthetic data; no MSSQL, Docker, browser or scanner.
* [ ] Author changes, one author Review, state; commit and freeze clean.

## Future gates (not run now)

Held by the coordinator's single admitted selected-tier gate (P123 may move main). Later, after one nonqueued admission and a normal merge of then-current main, the then-current own-tree runner is read and run as `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir> --jobs 2 --lock-timeout 0 < /dev/null`. No `--extra-test` is used or needed: `SQL_SELECTORS` already selects `test_assistant_release.MssqlUnleasedRevocation`, and the critique found that an `--extra-test` selector runs without `ZF_TEST_MSSQL=1`, so the new methods would skip and the runner rejects integration skips. The two reviewed method names to look for in the SQL log, derived from this source and not from any receipt, are `MssqlUnleasedRevocation.test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance` and `MssqlUnleasedRevocation.test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment`. The verbose SQL log must show both `ok`, not skipped. Independent exact-head review, hosted checks and the human, attestation and live gates remain required.

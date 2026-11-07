---
title: Research for OS-process race and restart coverage of assistant release and allowance (#107, C10)
description: Source-path independence from the active ranking candidate, existing contracts, and the smallest missing process-level regression increment
ms.date: 2026-11-07
---

Task `assistant-process-races-107`. Worktree `/home/azureuser/source/ama-wt/issue-107-process-races`, branch `test/assistant-process-races-107`, target main, base `f0afa8d76d7be13ec4278321e09e16e23eaeb37c` (equals origin/main when fetched, tree `d9414abc0a8c696c7f0069e30a827b2dad92b1c2`). Research disposition: executed. Earlier #107 records, original and adverse, are unchanged. Issue 107 is open; parent 104 stays open. Comment 6709144116 was read as data: PR 1255 merged, the sequential separate-connection revocation case ran unskipped on local disposable SQL, hosted SQL does not select it, and it is not process restart, race, real model or approval evidence.

## Source-path independence from the active gate

The heavy lock holder is PID 700151 running in `issue-1231-ranking-archive` with `--stack d99e6901... --stack 61f3ebe1...` against base f0afa8d76. I diffed base to `61f3ebe1a` for `src/`, `tools/` and `.github/`: nine files only, namely `api/.../server.py`, `api/tests/test_ranking_publication_wiring.py`, `core/README.md`, `core/pyproject.toml`, `core/.../ranking_publication.py`, `core/.../ranking_publication_runner.py`, `core/.../store.py`, and two ranking test files.

* No line of that source diff mentions `assistant_release`, `assistant_allowance`, `assistants.py`, `release_block`, `release_context` or `used_calls`.
* `store.py` hunks start at line 243 and end near 300 (publish_ranking_snapshot); the release functions `release_block`, `release_context` and `release_current` are at lines 76 to 97 and are not in any hunk.
* `server.py` hunks are the ranking publication endpoint and verify handler; the assistants routes (about lines 157 and 524 to 540) are untouched.
* `core/pyproject.toml` only adds the ranking runner module names to a coverage list.

Conclusion: the shared Store and API file names overlap, but the release, allowance and claim paths do not. The candidate is independent for this test-only slice. No assistants production file is edited here, so the future gate base reconciliation is a normal merge question only.

## Existing contracts used (read, not changed)

* `Assistants.claim` (`assistants.py` about 878): inside one `BEGIN IMMEDIATE` (SERIALIZABLE on SQL Server) transaction it rejects a leased task with an unexpired lease, evaluates `disabled()` (release denial), epoch, release reference and source signature, throttles on active calls, then applies the shared allowance: `calls`, `tokens` and `expires` are clamped to the minimum of stored and configured values ("same authority cannot extend expiry or increase allowance by restarting/config changes"), exhaustion disables the task, and a successful claim increments `used_calls` in the same transaction.
* `Assistants.execute` calls claim, then re-checks admission, epoch and release immediately before dispatch.
* Existing coverage: `Release.test_racing_workers_and_restart_after_revocation_keep_allowance_and_make_no_call` uses threads in one process; PR 1255 `UnleasedRevocation` uses sequential separate connections in one process. Neither uses OS processes, and neither exercises a finite allowance being contended and then restarted.
* Fixtures: `Base` (SQLite file store, constructed data), `MssqlFixture` (local-only disposable SQL, database `zf_test_assistants`), `release_support.install` (inserts only `fx-` release rows).

## Gap

No test proves, with independent OS processes and reopened source-current stores, that (a) a finite shared call allowance is never exceeded when several processes race the same proposals, nor replenished by a restart with a larger configuration, and (b) a revocation made before processes proceed is honoured by every racing and restarted process with no provider call and a durable release-specific denial.

## Runner selection

`tools/rpi-checks.py` `SQL_SELECTORS` already contains `test_assistant_release.MssqlUnleasedRevocation` (PR 1255). A new mixin added to the bases of that existing class and its SQLite twin is selected by the runner with no tool change. Hosted `src-ci.yml` does not select it; that is a disclosed gap and out of scope.

## Feasibility

A process test needs a small worker script that opens a source-current store and service from the same installed packages, with a counting fake provider writing append-only lines to a file in the test's own temporary directory. No production abstraction is needed: the worker uses `SqlStore` or `MssqlStore` and `Assistants` with the public constructors, and the three-line provider wiring that `release_support.install` performs (without reinstalling release rows, which would reset revocation). Barriers use marker files with a hard deadline. Policy is not invented: the expected outcomes are the claim linearization above (exactly allowance-many calls when tasks exceed allowance; none after revocation).

Planning Readiness: Ready. Residual risk: SQLite cross-process locking or SQL Server serialization errors under the race may surface as exceptions; if so they are recorded, and a confirmed production defect would stop implementation and be routed separately.

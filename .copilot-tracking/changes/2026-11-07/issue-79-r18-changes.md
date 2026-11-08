---
title: Issue 79 changes, correction cycle 1 for the 357e842d assessment
ms.date: 2026-11-07
---

Task `issue-79-r18-357-assessment-corrections`. Planning commit `3e9983a69` (research, plan with critique, details) preceded every test and source edit; preserve ref `preserve/issue-79-r18-planning`.

## Chronology

* Planning committed, then runner import path confirmed to be this worktree (`/home/azureuser/source/ama-wt/issue-79-publisher/src/core/src/zava_forward/core/ranking_publication_runner.py`, pre-edit SHA-256 `70803c8bc460c8bdf5ed911792d0906fb7d828a9454a4e9e43c854a99e48f362`).
* RED: new `AssessmentCycle1Tests` against the unchanged runner: 33 tests, 4 failures (`/tmp/79-r18-1107/red.log`). Reasons: blocked schedule exited 0, future date reported `ok`/overdue false, stale-hash policy and mismatched key accepted.
* GREEN attempt 1: one existing test (`test_archived_latest_without_a_next_day_is_a_problem_not_a_crash`) failed because I had introduced a new refusal code `archive_date_future`, and Ruff E501 and mypy `arg-type` findings appeared. Kept in `/tmp/79-r18-1107/green-core.log`, `ruff.log`, `mypy.log`. Decision: reuse the existing `archive_unverified` code with the specific message, leaving the existing test unchanged; a one-line `sed` replaced the code name in my new test (deviation: the edit tool was preferred).
* GREEN: `green-core3.log` 53 tests OK, `green-api3.log` 15 API wiring tests OK, Ruff check clean, mypy clean (268 files, pinned `ruff==0.17.1`, `mypy==2.4.0`, caches were generated in-tree by the tools).

## Changes

* `src/core/src/zava_forward/core/ranking_publication_runner.py`: `_policy_problem` (registry key equals version, `ranking.policy_hash` equals `content_hash`), refusal `policy_invalid` before sign-off; `_future` problem for a latest archived date after the run day in verify and schedule (window state null) and a publish refusal; `main` returns 2 for `blocked`. Post-edit SHA-256 `5987f45dadedbbe2bb075517cb04930b2901af0a17461865f39e18fadc878a08`.
* `src/core/tests/test_ranking_publication_runner.py`: `AssessmentCycle1Tests` (4 tests).
* `src/core/README.md`: one paragraph on the three behaviors.
* `docs/reference/log.md`: one appended entry.

## Cleanup

* Ruff and mypy created ignored caches in the worktree (`.ruff_cache`, `src/{agents,api,core,importer,orchestrator}/.ruff_cache`, `src/core/.mypy_cache`). Each was verified as a directory, not a symlink, with zero tracked files and a creation time within this run on a worktree that was ignored-clean at start; each was removed individually with `rm -r` on its exact path. No other path was deleted. Final `git status --short --ignored` showed only the three intended modifications.

## Limits

* `ruff format --check src` also reports pre-existing `src/check-container.py` as unformatted; it is unrelated, untouched and not part of this task.
* No FULL, browser, SQL, image or push. The #1231 child was not touched. The earlier FULL receipts do not cover this head.

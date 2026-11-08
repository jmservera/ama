---
title: Issue 79 details, correction cycle 1
ms.date: 2026-11-07
---

## Phase 2: regressions (RED first)

* In `test_ranking_publication_runner.py` add one class `AssessmentCycle1Tests(RunnerBase)`:
  * stale-hash registry: deep copy of `signed_registry()`, change a non-rule field such as `effective_date` without recomputing `content_hash`; assert `policy_invalid` for schedule, publish and exercise, and no archive directory.
  * registry key not equal to the policy version refuses the same way.
  * future date: publish on 2026-11-05, then publish a second snapshot dated 2026-11-04 as the legitimate older record, rewrite the first record's `published_on` to 2026-11-09 only in a copy of the archive; assert verify and schedule `problem`, publish refusal `archive_date_future`, exercise no-write.
  * CLI schedule exit 2 for unsigned shipped policy and for `--policy 9.9`; CLI schedule current exits 0.
* Run with `/tmp/zf79venv/bin/python` from `src/core/tests`, `PYTHONDONTWRITEBYTECODE=1`, logs in `/tmp/79-r18-1107/`.

## Phase 3: implementation

* Add `_policy_problem(key, policy)` using `ranking.policy_hash`; call after policy selection in `run`.
* Compute `future = latest is not None and latest > today` from the verify result in verify and schedule paths; append one problem, null `overdue`/`due`/`next_window_start`.
* Publish: `archive_date_future` refusal after the existing unreadable/unverified refusals when not exercise.
* `main`: `EXIT_REFUSED` when status is `refused` or `blocked`.
* README: one sentence for `policy_invalid`, future date and blocked exit 2.

## Phase 4: checks and records

* Pinned tools in `/tmp/79-align-r13-1106/venv` for Ruff check, format and mypy; tests with `/tmp/zf79venv`. Confirm the runner import path points at this worktree and record the source SHA-256.
* Changes, state and author Review under `.copilot-tracking/*/2026-11-07/issue-79-r18-*`; one log.md entry; commit with repository-local noreply identity and the Copilot trailer.

---
title: Changes for OS-process race and restart tests (#107, C10)
description: Test-only delta, actual local results, skips and the unverified actual-SQL disposition
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-process-races-107-plan.md). Critique: [critique](../plans/2026-11-07-assistant-process-races-107-critique.md). Base `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`.

## Delta (test-only)

* `src/api/tests/assistant_process_worker.py` (new, not discovered as a test): a worker that opens a source-current `SqlStore` or `MssqlStore` and `Assistants`, uses a counting fake provider that appends to an owned call log, gates its first claim behind file markers with a hard deadline, runs `execute` actions and prints one JSON line.
* `src/api/tests/test_assistant_release.py`: new mixin `ProcessRaces(UnleasedRevocation)` with two methods; the existing `SqliteUnleasedRevocation` and `MssqlUnleasedRevocation` now use it as base, so the runner's existing `SQL_SELECTORS` entry `test_assistant_release.MssqlUnleasedRevocation` selects them with no tool change. Imports `subprocess`, `sys` and `Path` added.
* No production, tool, workflow, dependency, README, schema, approval or attestation change.

## Methods

* `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance`: four OS processes (distinct PIDs, none the test's) all stop at the claim barrier (the parent proves four claim markers before release), then race three pending proposals under a stored allowance of two calls. Result: exactly two provider calls, two `ready` and one `disabled`, allowance row calls 2, tokens 2000000, used_calls 2, two attempt rows, a fourth proposal still `pending` with zero attempts. Two restarted processes with a call allowance of 1000, larger tokens and later expiry then execute the pending proposal: both false, no further call, the task disabled with the allowance-exhausted reason and one event, and the allowance row and attempts unchanged (the stored limits were not raised).
* `test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment`: a separate process executes an unaffected control (positive control: true, one call logged). The pending unleased proposal is then held by three processes at the claim barrier, the parent revokes its release through a separate service with an approver, and the processes proceed. Result: all false, still one call, the task `disabled` with attempts 0 and no owner, reason beginning "Release admission denied", one matching disabled event, release `revoked`, allowance unchanged. Two restarted processes with a larger configuration: false, no call, same state and one event, allowance unchanged.

Outcomes follow the existing claim linearization and allowance clamp; no policy was invented. Both cases use constructed data, a local fake provider and a simulated approver; no real model, cost or domain action.

## Findings during implementation

* The first run returned false for every worker because the worker's fake provider lacked the `model_version`, `model_version_strong` and `release` attributes that `release_support.install` sets on the parent provider; release admission correctly denied "no approved release matches (model_version)". The worker now sets them to the fixture's model name. This was a test-wiring error, not a production defect.
* Lint and strict mypy initially failed on the new helper (annotations, import order); fixed in the helper. The configured mypy overrides for older test modules were not changed.

## Local results (no services; own venv `/mnt/ama-gates/g107-process-races-preparation-1107/venv`; external caches; PYTHONDONTWRITEBYTECODE=1; unmasked exits)

* Install: `pip install -e src/core -e src/agents -e "src/api[dev]"` exit 0. Three generated ignored egg-info folders were moved by explicit path to `.../relocated-egg-info/`; import origins verified under this worktree.
* `python -m unittest test_assistant_release.SqliteUnleasedRevocation` (from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`): three consecutive runs and one post-relocation run, each 3 tests OK, exit 0.
* `python -m unittest -v test_assistant_release test_assistants test_continuity`: 194 tests, OK, skipped 61 (MSSQL opt-in classes including `MssqlUnleasedRevocation` with all three methods).
* `ruff check .` exit 0; `mypy` exit 0 (190 files); `ruff format --check tests/assistant_process_worker.py` exit 0. `test_assistant_release.py` is excluded from the formatter; the added block was checked against `ruff format` output with no differences in it (pre-existing baseline differences elsewhere in the file are unchanged).
* `git diff --check` exit 0. No orphan worker processes remained.

## Disposition

Tests prepared locally; SQLite proxy passes; actual disposable SQL for the two new methods is UNVERIFIED (skipped here, correctly, without `ZF_TEST_MSSQL=1`). FULL PUBLICATION NOT READY. Hosted `src-ci.yml` MSSQL does not select the class. Nothing here is attestation, approval, real-model or cost evidence, and no whole-issue criterion is claimed.

## Remaining gate

After coordinator admission to one nonqueued shared-lock slot: merge the then-current origin/main normally if it moved, then run the then-current runner `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir> --jobs 2 < /dev/null`. Its SQL group must show `MssqlUnleasedRevocation.test_racing_processes_...` and `test_processes_after_revocation_...` as `ok`, not skipped, against the runner-owned loopback SQL container (database `zf_test_assistants` created by the fixture), with fresh images and all groups. Then independent exact-head review and hosted gates. Expected resources as for earlier FULL runs: one SQL container, fresh images and Chromium, tens of GB of external output.

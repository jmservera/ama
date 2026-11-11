---
title: Issue 1360 extension 2 CI regression changes
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

Base: `29d94d10` merged with main `6f5e5007a` (ordinary merge `a7fcbb1aa`, no conflict, no rebase). E2 of the Nov 10 five additional corrections; E1 spent; no reset.

## Source

* `src/core/src/zava_forward/core/sqlstore.py`: the shared `save` post-commit handler again catches only `RuntimeError` (the pre-E1 contract) through `_committed_sync_errors()`. `_persist_import_refusals` alone sets a thread-local marker (restored in `finally`) that widens the tuple to `OSError` and `ValueError`, so the Importer transfer still reports a committed outcome.

## Tests

* `src/core/tests/test_priority_order.py`: the E1 direct-`save` test now runs through `_persist_import_refusals` (committed, one row, idempotent retry) and asserts a plain `save()` on the same store keeps the original `OSError`/`ValueError`; a new test proves the marker is cleared after a pre-commit failure. No assertion was weakened; the four hosted failing selectors are unchanged.

## Evidence (`phase1360-extension2-ci-evidence-1110/`)

* Red before fix: `logs/red-before-fix-core-selectors.log` (6 failures, 2 errors, matching hosted).
* Green after fix: selectors, Importer 82, API `test_case_journey`, ruff, mypy core and importer, complete Core unit run `core-full-rerun.log` (3057 tests, OK, 384 skipped).
* Preserved first runs: `changed-ruff-check-E501-first-run.log` (E501 in my new comment, fixed) and `core-full-first-run-azure-iot-hub-missing.log` (50 errors from the missing declared dev pin `azure-iot-hub==2.7.0` in my own venv, installed there only and rerun).

## Limits

MSSQL selectors blocked: no owned local SQL Server fixture exists (no container, no `ZF_TEST_MSSQL`); no cloud, pull or new fixture. Core `ruff format --check sqlstore.py` still fails as at base (not touched). Hosted CI, API hosted run and independent review unobserved.

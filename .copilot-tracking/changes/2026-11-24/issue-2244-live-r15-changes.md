---
title: Issue 2244 live r15 changes
ms.date: 2026-11-24
---

Tier: FULL (src change); the complete gate is the coordinator's step, `rpi-checks.py --all` was not run.

## Files

* `src/core/src/zava_forward/core/continuity.py`: read-only `gate_in_sync`.
* `src/core/src/zava_forward/core/sqlstore.py`: `_identity_drift` extracted from `_repair_identity_columns` (behaviour unchanged).
* `src/core/src/zava_forward/core/mssqlstore.py`: `_migrate_current`, `_migrate` override (skips the write lock when current).
* `src/core/tests/test_mssql_startup_lock.py`: `MigrateFastPathTests` (4 tests).
* `docs/reference/research/issue-2244-live-r15-2026-11-24.md`, `issue-2244-live-r15-assets/` (proof script, logs), index and log entries.

## Amendments and divergences

* A first run of the full core suite exposed a regression (SqlStore-backed MssqlStore tests passed `mssql=True` to a SQLite database); fixed by using `hasattr(self, "_env")` as `_migrate` did. Re-run of related suites passes.
* Live overlay used `mssql=True`, which is equivalent on the real store.

## Validation

* `test_mssql_startup_lock`: 25 tests OK. All core test modules mentioning SqlStore, MssqlStore or continuity: OK, except pre-existing failures also present on the unmodified tree (`test_discovery_assistant_demo`, `test_device_registry_azure`, `test_telemetry`: missing packages or environment).
* `mypy`: 3 errors, identical to the unmodified tree (opentelemetry stubs, unused ignore). `ruff check`: clean.
* Live on a throwaway database copy: see the research note. Throwaway jobs and the database were deleted; live API untouched (revision 0000068 Healthy, `/healthz` 200).

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff | Proven (live logs, unit tests) | research r15 |
| C2 skip lock when schema current | Proven for the full start-up path with this change on a throwaway copy (1.7 s to 1.8 s under a held lock); prior code incomplete (`_migrate`) | research r15 |
| C3 live API starts without crash-loop | Proven for deployed 0000068; the fix is not deployed (no production change authorised) | research r15 |
| C4 long writer cannot take the demo down | Proven on a throwaway copy (old code failed at 211.2 s under a 300 s writer, new code opened in 1.7 s); unproven on the deployed app until a release and redeploy | research r15 |
| C5 holder of the 2026-11-22 incident identified | Unproven: no data, incident past | none |

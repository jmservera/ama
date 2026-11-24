---
title: Issue 2244 live r15 phase details
ms.date: 2026-11-24
---

* Phase 2: `continuity.gate_in_sync(db, mssql)` read-only; `SqlStore._identity_drift()` extracted from `_repair_identity_columns`; `MssqlStore._migrate_current()` and `_migrate` override; tests in `src/core/tests/test_mssql_startup_lock.py`; tighten the populated count test is not possible on SQLite, so add fake-db tests.
* Phase 3: from `src/core`, `python3 -m unittest test_mssql_startup_lock`, wider core tests sequentially, bare `python3 -m mypy`, `python3 -m ruff check`.
* Phase 4: the deployed image cannot be changed without a deployment (not authorised for this goal: no production changes), so live proof of the new code is by a throwaway job that overlays the changed files onto the image path via the proof script, run against the throwaway database only.

---
title: Issue 1401 numeric concern order cycle 1 details
ms.date: 2026-11-11
task_id: 1401-numeric-order-1111
---

## Phase 2 tests

* `src/core/tests/test_aftercare.py` `SnapshotTests`: `test_restore_is_numeric_whatever_the_json_key_order` (999, 1000, 1001; text-sorted and reversed insertion) and `test_restore_still_refuses_gaps_and_non_canonical_identifiers_past_999` (gap, unpadded `AC-0501`, foreign key, id/key mismatch).
* `src/core/tests/test_aftercare_store.py` `Contract` (runs on JSON Store, SQLite and, when admitted, SQL Server): `seed` clones the first recorded concern, receipt and request to N valid entries; `test_register_at_1000_reads_after_restart`; `test_writes_across_999_1000_1001_survive_restart_and_replay` (write, reopen store, check numeric restore order, replay the same request id).

## Phase 3 change

`src/core/src/zava_forward/core/aftercare.py`: add `_concern_number` and sort the restored concerns by it before the unchanged positional validation loop.

## Phase 4 commands

Core: `cd src/core && PYTHONPATH=tests:src:../agents/src:../api/src python3 -m unittest tests.test_aftercare tests.test_aftercare_intake tests.test_aftercare_store`. SQL Server: `/tmp/run_mssql_1401.sh` under `flock -n /tmp/ama-rpi-heavy.lock` (owned labelled loopback container, removed on exit). API: `cd src/api && PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_aftercare_served tests.test_aftercare_screen`. Lint: `ruff check`, `ruff format --check`, `mypy`.

---
title: Issue 1401 numeric concern order cycle 1 changes
ms.date: 2026-11-11
task_id: 1401-numeric-order-1111
---

## Files

* `src/core/src/zava_forward/core/aftercare.py`: `_concern_number` and numeric-sorted restore in `AftercareRegister.from_state` (11 added lines, `import re`). Validation unchanged.
* `src/core/tests/test_aftercare.py`: two register restore tests (999/1000/1001 any key order; gap, unpadded, foreign key, id mismatch still refused).
* `src/core/tests/test_aftercare_store.py`: `seed`, `assert_listed` and two `Contract` tests run on every adapter.

## Evidence (raw outputs retained in the handoff)

* Original failure, unmodified code: JSON Store, 1001 sequential `record_concern` calls; call 1001 raised `StateInvalid` after 105 s.
* RED (fix stashed, 9 selected new tests, JSON Store and SQLite): `FAILED (errors=7)`, 4 `StateInvalid` plus 3 reversed-order unit errors, exit 1.
* GREEN same 9 tests: `OK`, exit 0.
* Final focused core run `tests.test_aftercare tests.test_aftercare_intake tests.test_aftercare_store`: `Ran 104 tests, OK (skipped=15)`, exit 0; the 15 skips are the SQL Server variants.
* Owned disposable SQL Server 2022 (label `zf.task`, loopback, manifest, non-queued heavy lock, container removed): `tests.test_aftercare_store.MssqlAdapter` `Ran 15 tests, OK`, including both new tests, exit 0. RED was not run on SQL Server; the failure is adapter-independent in `from_state` and was shown on JSON Store and SQLite.
* API `tests.test_aftercare_served tests.test_aftercare_screen`: 21 tests OK. `ruff check`, `ruff format --check` and `mypy` clean for the touched files.

## Limits

Synthetic tests only; no approval of high-volume or long-lived production use. Per-operation validation and listing remain O(n) to O(n^2) at 1000 concerns (105 s for 1001 writes), a performance observation left unchanged. #1402, other aftercare bugs and whole #133/#89 acceptance are untouched. Development note: the source edit was made before RED capture; RED was then taken by stashing the source file.

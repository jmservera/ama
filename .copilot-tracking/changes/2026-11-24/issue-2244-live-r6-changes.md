---
title: Issue 2244 live run 6 changes
ms.date: 2026-11-24
---

Status: complete. Tier FULL (src change); the coordinator runs the gate, `rpi-checks.py --all` was not run.

## Changes

* `src/core/src/zava_forward/core/sqlstore.py`: read-only fast paths in `_seed`, `_ensure_queue_membership`, `_migrate_recommendations` (`_recommendations_current`, `_rec_order_indexes_present`).
* `src/core/src/zava_forward/core/mssqlstore.py`: `_rec_order_indexes_present` for SQL Server.
* `src/core/tests/test_mssql_startup_lock.py`: `PopulatedStartupLockCountTests`; `src/core/tests/test_sqlstore.py`: stub binding.
* Research note `docs/reference/research/issue-2244-live-r6-2026-11-24.md`, index and log entries.

## Validation

42 tests OK (`test_mssql_startup_lock`, `test_sqlstore`); ruff clean; mypy 3 pre-existing errors identical to base. No Azure change; no drill; no secret read.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| C1 retry with backoff | Proven (unit tests; live lines in run 5) | tests |
| C2 skip lock when schema current | Proven by tests; live only for earlier steps | tests, hash match |
| C3 live start without crash-loop | Proven for 0000059 at reading time; new paths not deployed | live reads |
| C4 long writer cannot take demo down | Unproven: requires a lock drill, excluded by the owner | n/a |
| C5 lock holder identified | Unproven: no log names it | n/a |
| Live carries these fixes | Unproven: owner deploys | hashes |

Issue 2244 stays open.

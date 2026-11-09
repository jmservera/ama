---
title: Issue 1292 C1 changes
description: Source and test changes correcting the independent review findings, with commands, exits, hashes and pending gates
ms.date: 2026-11-08
---

C1 starts from head `641c11ffd26d03549e1e174179efc8b01b8e3544`, tree `7faf00ae6d96f548b8cda1802fd5b2b3decbafb6`, research and plan commit `dedd67277`. Earlier records, SQL logs and the earlier SQL red/green results are unchanged and historical: they describe the pre-correction source and do not validate C1.

## Changes

* `sqlstore.py`: new `_repair_zero_ordinals`, `_audit_creation_order`, `_backfill_zero_ordinals`; `_migrate_recommendations` now calls the same fenced path. `_sync` repairs zero ordinals under the write lock before any load (fail closed: errors propagate). `save` repairs before allocating the first new ordinal. `_queue_candidates` marks its own write transaction so `_sync` does not nest a second one. Counter and `executemany` replace the quadratic loop and per-row updates. Every batch appends to `meta.rec_order_backfills`; `rec_order_legacy` is written only for a first-ever migration with no existing record and is never replaced. Refinement of the C1 details: `rec_order_legacy` is written only when no positive ordinal existed (as before), not for rollback batches.
* `tests/sqlguard.py` (new) and calls in `MssqlPriorityOrder.setUp` and `MssqlResidentControls.setUp`: refuse any `ZF_SQL_SERVER` that is not localhost or a loopback IP literal and any `ZF_SQL_AUTH` other than `password`, before the mssqlstore import, connection or DDL.
* `tests/test_priority_order.py`: fixture classes split so SQLite-only cases do not run twice; new tests per the plan. `src/core/README.md` section updated. `mssqlstore.py` and `store.py` unchanged.

## Source hashes (sha256)

* `sqlstore.py`: previous `d38b07f6fa7ad68e98667908194174c025700c074d9eeb992fc6fbe77e2835aa`, now `36d524f97e45e06eb8354c647b8f8bee827e003cd83a569291c13a43b6d0b5fd`.
* `mssqlstore.py`: `0e618ac5f05fe02e3e08ab8c5eb30d3989817995e56077a2c5a035c02c6e16d1` (unchanged).
* `test_priority_order.py`: `cbeb46f76c4d884a531e8c54e0ee19be7647b99804bc0e39049ee4f6b16a93ec`; `sqlguard.py`: `84b357632207c171b2fb12a179788681432873c30e65f38dde6b1b8389cae3eb`.

## Observed results (light, no SQL Server; logs in `changes/logs/1292-2026-11-08-c1/`)

Environment: `HOME` and `ZF_DATA` under `/tmp/ama-1292-scratch` (no data file, synthetic fixtures only), `PYTHONPATH=src:tests` from `src/core`, no package installs.

* Red 1 (`red-1.*`): new tests against the unchanged source before the test guards were applied: exit 1, 40 run, 6 failures, 3 errors, 16 skipped. Covers F1 (two failures), F2 audit order, F3, F4 (`database is locked` for concurrent openers on a 30,000 row backfill), F5 guard, fail-closed (missing method), ambiguity record and broken chain.
* Red 2 (`red-2.*`): same tests against `git archive` of the previous source (hash above), with the guards already in the tests: exit 1, 40 run, 5 failures, 3 errors (the F5 guard test passes because the guard is in the shared tests directory, not the source).
* Green final (`green-3.*`): `python3 -m unittest test_priority_order` exit 0, 40 run, OK, 16 skipped; the 16 are the `MssqlPriorityOrder` class, PENDING native SQL Server. `green-1` and `green-2` are earlier passes of the same tests before test reformatting.
* Original selectors on SQLite (`test_resident_decisions.SqlResidentDecisions...`): both exit 0. The two SQL Server selectors were not run.
* Related suites (`related-2.*`): `test_resident_decisions test_sqlstore test_sqlreads test_sqlqueues test_seed_merge test_taskqueues test_recovery` exit 0, 360 run, 93 skipped. API `test_mssqlstore` discover form (`api-mssql.*`): exit 0, 226 run, 217 skipped.
* `ruff check src tests` and `ruff format --check` on the new and changed test files: exit 0 (`ruff-3.txt`; `lint-2.txt` is an earlier run that listed line-length findings fixed afterwards). mypy 2.4.0 from the scratch venv over `src` and `tests`: exit 0, 271 files (`mypy-3.txt`). `git diff --check` clean.
* `sqlstore.py` is not `ruff format` clean at the base either; it was not reformatted.

## Pending and unproven

* Native SQL Server red/green (new class, both original selectors, audit recovery, backfill batch records and fence) is PENDING separate coordinator admission. The new SQL (`executemany`, audit chain read, `COUNT`) is read against the adapter, not run.
* 30,000 row timing and concurrency are measured only on SQLite. SQL Server scale and the ledger-enabled migration are UNPROVEN.
* FULL local gate with external receipt, independent exact-head review, hosted CI: PENDING.
* The guard covers the two fixtures named in the finding. Other test modules that read `ZF_SQL_SERVER` are unchanged and out of scope here (residual).

## Human decisions still required

* How the named data owner resolves recorded ambiguous groups in any live database, and the release boundary for draining older writers; no approval is claimed and no historical data was altered.

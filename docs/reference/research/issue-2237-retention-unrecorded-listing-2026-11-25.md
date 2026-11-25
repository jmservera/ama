---
title: Issue 2237 retention listing tolerates a busy write lock (2026-11-25)
description: Why GET /api/retention still answered 503 under SQL write-lock contention, the failing-first test and fix that make the listing answer 200 unrecorded, and a per-criterion table
ms.date: 2026-11-25
---

Synthetic demo, desktop only. Refs #2237. Source and test change on a local branch; not deployed, so no new live proof was possible. No Azure change; no throwaway resource; no credentials used.

## Finding

The [2026-11-25 re-proof](./issue-2237-live-reproof-2026-11-25.md) logged 39 `/api/retention` 503s in 48 h. The cause is in code: `Store.retention_due` is a read-only listing, but it queued the `retention_job_listed` audit entry inside its lock block, and `SqlStore._finish` takes the global `sp_getapplock` write lock (15 s) when that block exits. Any long writer therefore turned the listing into an error. `Store.briefing` already avoids this (issue #2320).

## Fix

`retention_due` now builds the list first, then records the audit under `write_wait(2000)`. If the lock is busy it returns the list with `recorded: false` and a plain-language note; any other error still propagates. The next request records the entry.

## Evidence

* Failing-first: `test_retention_listing_survives_a_busy_write_lock_unrecorded` in `src/api/tests/test_document_controls.py` raised the driver lock error before the change (2 errors, Store and SqlStore variants) and passes after.
* `src/api/tests/test_error_logging.py`: the 503 mapping test now simulates a busy lock by failing `retention_due` itself; the recovery test now expects 200 unrecorded, then 200 recorded.
* Local runs: test_document_controls and test_error_logging pass; core `test_resident_decisions` passes (458 run, 162 skipped); `mypy` clean in `src/api`; `ruff` clean on changed files. `src/core` mypy reports 3 errors in `telemetry.py` and `device_provision.py`, files not touched here.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history; not on demand | 11 logged 500s on 2026-11-21 to 22; contention now 503; drills excluded |
| Find the cause in the demo container logs | Proven | [2026-11-23 note](./issue-2237-live-cause-and-fix-2026-11-23.md); lock holder still unidentified |
| Fix with a regression test | Proven | 503 mapping (merged) plus this unrecorded-200 change with a failing-first test |
| Re-prove 200 live | Proven on 0000068; unproven for this change | The new code is undeployed; deployment is outside this task |

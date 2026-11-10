---
title: Quality sensor demo 1288 C6 changes
ms.date: 2026-11-08
---

Recorded 2026-11-08T22:49Z after implementation over base `5f89248b` (plan commits `3706fcdc8`, `9a7cff5fc`). Light SQLite and static evidence only; no heavy process was started.

## Dispositions

* C6-1 dispatch/withdrawal ordering: new `assistant_dispatch_hold` (home, task, fence, `expires_at` on the database clock). `call()` commits the final consent check and the hold in one transaction before the provider and releases it in `finally`; `SensorConsumer.configure` waits (50 ms poll, 45 s ceiling) for a live hold outside its write transaction, then raises `SENSOR_DISPATCH_IN_FLIGHT`. A hold that cannot be written sends nothing. A withdrawal is delayed at most one provider timeout plus 5 s per home call; no global lock. Direct SQL that bypasses `configure` is outside the guarantee (documented). SQL Server DDL and `DATEDIFF_BIG` check are written, unexecuted.
* C6-2 identity: refresh-in-place removed. A changed capture on an unrequested proactive task in the same schedule marks it stale and enqueues the current capture as its own task (max 3 replacements without a dispatch, reset on a proactive dispatch); a request during the lease reuses the current task and keeps provenance.
* C6-3 migration: lazy per-case `_adopt` from the newest dispatched non-requested task of the same release and epoch (index `ix_assistant_case`); an empty unscoped slot otherwise; no fleet scan; nothing unrecorded is treated as approved.
* C6-4 UI: a stale `review-suggested` flag stays in the main case panel and counts as waiting (`assistants.js:195,235`, `case-workspace.js:19`); Accept and verify stay disabled because `ready` requires a non-stale proposal.
* C6-5 manual slot: a manual task services a non-sensor schedule but not the autonomous Quality flag (`_due`); manual work is never relabelled proactive.
* C6-6 backend variants: tests use `JSON_MODIFY`, `sys.triggers` and a backend-neutral statement recorder when the service is SQL Server. SQL Server tests remain skipped (92 skips in `test_quality_sensors`); no SQL pass is claimed.
* C6-7 request as-of: the flag block shows captured as-of, freshness and age, or "unknown: do not treat as live" (`assistants.js:20`).
* C6-8 panel wording: the sensor panel is the "current authorised capture"; `review_flag` adds `changed_since_capture` and `newer_reading_count` (`ops.js:46,55`).

## Files and hashes (sha256 prefix)

* `src/core/src/zava_forward/core/assistants.py` ea7688d25597fac5
* `src/core/src/zava_forward/core/sensor_consumer.py` 3647d4b133246dc5
* `src/api/src/zava_forward/api/web/assistants.js` 3a0767cd8fa235a3
* `src/api/src/zava_forward/api/web/case-workspace.js` 1eb1a13328016
* `src/api/src/zava_forward/api/web/ops.js` 91662fd18be17cae
* `src/api/tests/test_quality_sensors.py` ed4e50908a1a345e
* `src/api/tests/test_assistants.py` 1ca4f004daa62fad (DDL count 7; budget sentinel changed to 9183461 because `93417` collided with a hex digest)
* `src/core/README.md` (C6 paragraph)

## Evidence

* Red: `/tmp/c6-red-1.txt` exit 1 (9 failures, 4 errors).
* Green: `/tmp/c6-final-test_quality_sensors.txt` exit 0 (187 run, 92 skipped); `test_assistants` exit 0 (58 skipped); `test_assistant_release`, `test_sensor_consumer`, `test_sensor_ingestion`, `test_iot_stream`, `test_regulatory_chat_api` exit 0 (`/tmp/c6-final-*.txt`).
* Ruff `--select F,E9` on `assistants.py` and `test_assistants.py` exit 0 (`/tmp/c6-ruff-2.txt`); `sensor_consumer.py` clean; `test_quality_sensors.py` still has long-line E501 findings in test text (baseline had 10; `/tmp/c6-ruff-3.txt`). `node --check` on the three JS files exit 0.
* Web guidelines source fetched before edits and again before review; text-only changes, no new interaction, no `file:line` violations found. Not a browser, axe or assistive-technology result.

## Plan amendments

* The weakly discriminating assessment-change test remains as written; it passes trivially.
* Manual occupancy of the slot was restored for non-Quality capabilities after `test_scan_valid_cases_does_not_enqueue_and_changes_enqueue_material_versions` failed without it.
* The C5 churn test was rewritten for the replacement chain (one dispatch).

## Pending gates

Actual SQL Server (hold, schedule and index DDL, MSSQL variants, query plans), browser, axe, keyboard and reflow, #184 and #1292 integration, FULL receipt, release and attestation, live walkthrough.

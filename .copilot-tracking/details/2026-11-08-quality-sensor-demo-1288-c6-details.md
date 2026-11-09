---
title: Quality sensor demo 1288 C6 details
ms.date: 2026-11-08
---

Written 2026-11-08T22:26Z (corrected from a later stated minute) with the C6 plan, before any product or test edit.

## Files

* `src/core/src/zava_forward/core/assistants.py`: `assistant_dispatch_hold` in both DDL tuples and `ix_assistant_case` in `migrate`; `call()` writes consent check plus hold in one transaction and releases in `finally`; claim supersedes and enqueues instead of refreshing; `_enqueue` occupies the slot only for `proactive`; `_due` with lazy backfill and exact-row suppression; `review_flag` adds `changed_since_capture`, `newer_reading_count`.
* `src/core/src/zava_forward/core/sensor_consumer.py`: `configure` waits (bounded, database clock) for a live hold and fails with `SENSOR_DISPATCH_IN_FLIGHT`.
* `src/api/src/zava_forward/api/web/assistants.js`, `case-workspace.js`, `ops.js`: flag block, waiting count, panel wording (after guideline refresh).
* `src/api/tests/test_quality_sensors.py`, `test_assistants.py`: new tests, backend-specific helpers, DDL count.
* `src/core/README.md`: C6 paragraph.

## Constants

* Hold `until` = database now + provider timeout + 5 s; `configure` polls every 0.05 s up to timeout + 5 s then raises.
* Replacement bound: 3 per coarse signature without dispatch.

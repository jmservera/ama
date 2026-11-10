---
title: Quality sensor demo 1288 C5 details
ms.date: 2026-11-08
---

Written 2026-11-08T21:59Z with the C5 plan, before any product or test edit.

## Files

* `src/core/src/zava_forward/core/sensor_consumer.py`: guard triggers, v2 marker, `ensure_control_home` and `_schema` hooks.
* `src/core/src/zava_forward/core/sensor_view.py`: marker version and trigger check in `_controls`; `freshness()`; unbounded future probe.
* `src/core/src/zava_forward/core/assistants.py`: `assistant_schedule` DDL (both lists), `_schedule`/`_due`/`_enqueue`, claim refresh and `dispatch.as_of`, stale requeue, consent hold at pre-dispatch and in the dispatch thread, `build_request` freshness, `review_flag` newer-readings and freshness.
* `src/api/tests/test_quality_sensors.py`: R1 to R8 (mock provider; labelled mock).
* `src/core/README.md`: short C5 paragraph.

## Schedule row

* `assistant_schedule(capability, case_id, scope, signature, task_id, at)` primary key (capability, case_id). Scope is a digest of the release reference and continuity epoch. Written by `_enqueue` on a new or requeued task.
* `_due`: not eligible means false. A row in the current scope with the same coarse signature occupies the slot unless its task is a never-dispatched stale task; occupied means no new work. An exact task that is stale and below the attempt limit is requeued by `_enqueue`.

## Validation

Light only: the six C4 suites plus `test_iot_stream` and `test_regulatory_chat_api`, ruff (line length 100; `assistants.py` F,E9). Raw exits in unique `/tmp/c5-*.txt`.

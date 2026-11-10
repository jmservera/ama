---
title: Quality sensor demo 1288 C7 details
ms.date: 2026-11-08
---

Written 2026-11-08T23:00Z with the C7 plan, before any product or test edit.

## Files

* `src/core/src/zava_forward/core/ai_consumption.py`: `DISPATCH_GATE` context variable, `dispatch_gate()` context manager, `DispatchWithdrawn`.
* `src/core/src/zava_forward/core/ai.py`: `honours_dispatch_gate`; gated connection and opener used only when a gate is set (existing `urlopen` path unchanged otherwise); `evidence()` maps `DispatchWithdrawn` to `suspended-before-dispatch`.
* `src/core/src/zava_forward/core/assistants.py`: `assistant_dispatch_gate` DDL (both backends); `assistant_tasks.dispatched`, `ix_assistant_dispatched`; idempotent `migrate` of `replaced` and `dispatched`, fail closed to `schema-unavailable`; per-attempt gate in `call()`; `claim` stamps `dispatched`, exhaustion reason; `_adopt` bounded and own-signature; `_due` frozen-dispatch serviced status and exhausted-slot quiet interval; `review_flag` content comparison.
* `src/core/src/zava_forward/core/sensor_consumer.py`: per-home `_dispatch_in_flight`, changed-home derivation in `configure`.
* `src/api/src/zava_forward/api/web/assistants.js`: distinguish changed cited readings from additional readings (text only).
* `src/api/tests/test_quality_sensors.py`, `src/api/tests/test_assistants.py` (DDL count): tests and Ruff cleanup.
* `src/core/README.md`: C7 paragraph, residual limit.

## Order

Red tests first and retained, then source, then green and lint.

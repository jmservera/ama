---
title: Issue 2202 live details b, 2026-11-24
ms.date: 2026-11-24
---

## Phase 2 details

* File `src/api/src/zava_forward/api/iot_stream.py`, callback `on_event`: check `stop` first (RUN_STOPPED unchanged); if the monotonic clock is at or past the deadline and `bounded_window`, call `finished.set()` and return; otherwise keep RUN_STOPPED.
* Test: fake `time` module in iot_stream with a clock jumping past the deadline before the callback; expect `run(..., bounded_window=True)` returns `()` without raising. Verified to fail without the change.
* Success: all `tests.test_iot_stream` tests pass; mypy and ruff clean.

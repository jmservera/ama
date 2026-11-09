---
title: Details for #188 slice 1
ms.date: 2026-11-05
---

* Phase 1: `src/core/src/zava_forward/core/sensor_consumer.py` gains `LIVE_FIELDS`, `_live_shape` (closed shape, slot-aligned time, `reading_id` equals `LIVE-<sensor>-<slot>`, lowercase scenario, `injected_fault=none`, sunlight number), quality checks (sunlight unit `W/m2`, range 0..1400, calibration from the confirmed control), `observed_series` branch, and a `schema_version` width for SQL Server.
* Phase 2: tests in `src/core/tests/test_sensor_consumer_live.py` and `LiveSimulatorRowTests` in `src/api/tests/test_iot_stream.py`.
* Phase 3: `src/api/README.md` paragraph on the message schema.

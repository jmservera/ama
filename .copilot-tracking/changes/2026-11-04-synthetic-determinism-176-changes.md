---
title: Changes for #176 slice 1
ms.date: 2026-11-04
---

* `sensor_stream.descriptor` now records `generator_revision`.
* Audit gains `sensor-stream` replay (wire frames plus descriptor, byte compared).
* Tests added or extended; README section and log entry added.
* Validation run: ruff check and format check, mypy (cache /tmp/mypy-176) on two modules, unittest for test_determinism_audit, test_sensor_stream, test_sensor_handover, test_stock_register (39 tests, OK).
* Not run: gate, benchmarks, full suites, Azure.

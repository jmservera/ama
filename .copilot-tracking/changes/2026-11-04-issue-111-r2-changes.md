---
title: Issue 111 round 2 changes
ms.date: 2026-11-04
---

* Added `src/core/src/zava_forward/core/sensor_analysis_store.py`.
* Added `SensorConsumer.home_consent` in `sensor_consumer.py`.
* Added `src/core/tests/test_sensor_analysis_store.py` (7 tests).
* Updated `src/core/README.md` and `docs/reference/log.md`.

Validation run: `test_sensor_analysis*.py` (18 tests, one fix of my own test expectation), `test_sensor_consumer.py` (37) on SQLite; ruff check and format; mypy with `--cache-dir=/tmp/mypy-530` on the two source files. Not run: SQL Server variant, gate, benchmarks, full suites, mypy on tests, browser.

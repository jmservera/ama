---
title: IoT threshold advisory changes
ms.date: 2026-11-14
---

* `src/core/src/zava_forward/core/sensor_view.py`: constants, `advisory()`, and `advisory` field in `view()`.
* `src/api/tests/test_iot_threshold_advisory.py`: new focused tests.

Validation: new tests 7 OK; `test_accessibility_baseline.py` 13 OK; `test_quality_sensors*.py` 448 OK (179 skipped); changed files pass ruff check and format; mypy reports only two pre-existing unused-ignore errors in `tests/test_ai_consumption_api.py`; repo-wide ruff reports pre-existing findings outside this change. No UI change, so no browser check. Not pushed.

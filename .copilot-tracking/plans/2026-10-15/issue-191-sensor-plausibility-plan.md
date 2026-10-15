---
title: Issue 191 sensor plausibility plan
ms.date: 2026-10-15
---

* Add `mvp/tests/test_sensor_plausibility.py` with checker helpers (bounds, flat-line), outdoor and indoor bounds, seasonal and diurnal structure, age and dwelling humidity ordering, profile mix, and missing and fault rates vs injection.
* Use 150 homes, 730 days, 360 minute cadence to keep runtime under a second.
* Label expected ranges as exercise values; no generator change.
* Note the test in `mvp/README.md`. No knowledge-base file changes.

Critique (single pass): checkers must have negative self-tests so they demonstrably fail on bad series; applied directly.

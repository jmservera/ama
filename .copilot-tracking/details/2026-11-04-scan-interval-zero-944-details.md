---
title: Details for #944
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/assistants.py`: guard in `forecast` after the SQL check.
* `src/api/tests/test_assistants.py`: `test_forecast_refuses_a_zero_or_negative_scan_interval` builds services with `scan_interval` 0 and -5 and expects `ValueError` containing "greater than zero".

---
title: Details, issue 133 sensor context
ms.date: 2026-11-04
---
* `src/core/src/zava_forward/core/aftercare.py`: `_context` validates string pairs and applies `neutral_text`; `add_sensor_context` merges context and appends a history event only.
* `src/core/tests/test_aftercare.py`: later normal signal leaves investigation, outcome, remedy and unresolved list unchanged; guard, typing, empty and unknown id refused.

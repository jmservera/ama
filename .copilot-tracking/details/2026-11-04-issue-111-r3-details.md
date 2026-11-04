---
title: Issue 111 round 3 details
ms.date: 2026-11-04
---

* `status_text(signal)`: states review, normal, declined, stale, insufficient. Unknown or non-sufficient data never reads as normal.
* `map_and_list(signals)`: same sorted entries for map and list, so the text is identical.
* Every text says the status does not change repairs or queue place, and names the manual route.
* Files: `src/core/src/zava_forward/core/sensor_status_text.py`, `src/core/tests/test_sensor_status_text.py`.

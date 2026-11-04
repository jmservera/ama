---
title: Details for #462 resident demo journey slice
ms.date: 2026-11-04
---

* New status text: "No reading recorded"; "Not shown: this reading looked wrong"; "Not shown: the sensor seemed stuck"; "Not shown: outside the expected range".
* Files: `src/core/src/zava_forward/core/resident_showcase.py`, `src/api/src/zava_forward/api/resident_demo/web/demo.js`, `src/core/tests/test_resident_sensors.py`, `src/api/tests/test_resident_demo_api.py`, `src/api/checks/resident_sensors_browser_check.py`.
* Slow-start: `setTimeout` 4000 ms in `start()`; only replaces the exact "Loading..." status, only while the transition id is unchanged; cleared in both then and catch paths.

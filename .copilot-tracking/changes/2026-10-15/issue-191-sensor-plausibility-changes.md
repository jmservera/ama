---
title: Issue 191 sensor plausibility changes
ms.date: 2026-10-15
---

* Added `mvp/tests/test_sensor_plausibility.py` (8 tests).
* Added a README bullet in `mvp/README.md`.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` passes.
* Divergence: cadence 360 minutes for speed, so diurnal checks use hours 6, 12, 18 and 0.

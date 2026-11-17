---
title: Issue 1818 c1 details
---

Phase 1: key rename in sensor_map.py (field `provenance=PROVENANCE` becomes `source=PROVENANCE`), app.js line 2565 reads `point.sensor?.source`, test line 31 reads `s["source"]`.
Phase 2: demo.js line 303 class `sensor-source`.

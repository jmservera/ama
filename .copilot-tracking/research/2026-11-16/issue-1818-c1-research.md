---
title: Issue 1818 c1 research
---

Research disposition: executed. Planning Readiness: Ready.

CI failures on PR 1826 (`src-api`):

* `test_content_standard`: `app.js:2565` reads `point.sensor?.provenance`; the word is an internal term in web copy and is not in the ALLOWED list.
* `test_epic149_child_ux_contracts`: `resident_demo/demo.js:303` uses the CSS class `sensor-provenance`, matched by the resident copy scan.

Cause: the map sensor payload key `provenance` (`core/sensor_map.py:86`) and a demo class name. Only `test_map_sensors.py:31` consumes the key. Fix: rename the payload key to `source` and the class to `sensor-source`; no CSS rule uses the old class.

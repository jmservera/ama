---
title: Issue 1818 c1 changes
---

* `core/sensor_map.py`: map sensor payload key `provenance` renamed to `source`.
* `api/web/app.js:2565`: reads `point.sensor?.source`.
* `api/tests/test_map_sensors.py:31`: asserts `s["source"]`.
* `api/resident_demo/web/demo.js:303`: class `sensor-provenance` renamed to `sensor-source`.

Validation (PYTHONPATH pointing at the worktree sources): test_content_standard 29 OK, test_epic149_child_ux_contracts 14 OK, test_map_sensors 13 OK, test_map_fullscreen 8 OK, core test_resident_showcase 42 OK; `node --check` on app.js and demo.js OK; `ruff check` on touched Python OK.

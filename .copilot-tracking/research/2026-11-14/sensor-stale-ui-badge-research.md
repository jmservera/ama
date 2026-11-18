# Research: sensor staleness UI badge (Refs #1288, #109)

* Planning Readiness: Ready. Disposition: executed.
* Issue 1288 asks for a visible, freshness-aware per-home reading view with explicit stale/missing states and no silent substitution; issue 109 is the in-use monitoring epic.
* `GET /api/cases/{id}/sensors` (server.py) returns `Assistants.sensors` (core `sensor_view.view`), which already has `freshness` and `freshness_text` but no explicit offline/uncalibrated badge or advisory provenance.
* UI: `sensorPanel` in `web/ops.js` rendered freshness as a status paragraph only.
* Constraint found: `zava_forward.api` and `core` import from the main checkout install, so the new logic lives in an api-package module loaded by path in the test; `test_assistants` is not importable under the required command, so the dedicated test is self-contained.
* Excluded by owner: `test_quality_sensors_correlation.py`, `chat.js`, `checks/*`.

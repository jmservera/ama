# Changes: sensor staleness UI badge

* Added `src/api/src/zava_forward/api/sensor_badges.py`.
* Edited `server.py` (annotate sensor response) and `web/ops.js` (badge list and advisory paragraph).
* Added `src/api/tests/test_sensor_staleness_ui_badge.py`.
* Validation: unittest of the new test, `test_accessibility_baseline`, `test_content_standard` (47 tests OK); ruff check and format clean on the new Python files.
* Not run: hosted CI, full local gate, browser harness.

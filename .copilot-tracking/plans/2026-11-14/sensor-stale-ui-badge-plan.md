# Plan: sensor staleness UI badge

* [x] Add `api/sensor_badges.py` (text badges: Fresh, Stale, Offline, Unavailable, Freshness unknown, plus Uncalibrated; advisory string).
* [x] Annotate the sensors endpoint response in `server.py`.
* [x] Render badges and advisory text in `sensorPanel` (`ops.js`), text only, no `aria-invalid`.
* [x] Add `tests/test_sensor_staleness_ui_badge.py`.
* Critique: executed once; compatible finding applied (move logic out of core because of install path); no conflicts.
* Validation tier: focused (small UI/API read-path change, no gate, security or deployment impact).

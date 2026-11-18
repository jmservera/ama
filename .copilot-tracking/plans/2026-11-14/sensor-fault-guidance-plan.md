# Plan: sensor fault guidance (Refs #111)

* [x] Core: `sensor_view.reading_health` (ok, fault, out_of_range, none), emitted as `health` by `view()`; capture identity unchanged.
* [x] API: `sensor_badges` adds Withheld and health badges plus one plain-language `next_action` (withheld, offline, fault/out_of_range, stale).
* [x] UI: `ops.js` renders `Next action:` text; no colour-only cues, no aria-invalid.
* [x] Tests: `core/tests/test_sensor_view_health.py`, extended `api/tests/test_sensor_staleness_ui_badge.py`.
* Critique: executed once (self); no conflicting advice. Validation tier: focused (read-only display, no gate/security/deploy impact).

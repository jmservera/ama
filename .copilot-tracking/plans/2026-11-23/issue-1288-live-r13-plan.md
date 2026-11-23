# Issue 1288 r13 plan

* [x] Phase 1: add `_log_unavailable(path, exc)` in server.py and call it from the sensors and sensor-drafts catch-all handlers.
* [x] Phase 2: regression test in test_quality_sensor_grounding.py (503 body unchanged, log has class and site, no message text).
* [x] Phase 3: run focused tests, mypy, ruff; write changes record with per-criterion table; review once; commit.

Details: .copilot-tracking/details/2026-11-23/issue-1288-live-r13-details.md

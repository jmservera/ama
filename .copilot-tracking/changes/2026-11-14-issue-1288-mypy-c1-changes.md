# Issue 1288 mypy correction, Cycle 1: changes

Branch feat/demo-1288-sensor-stale-ui-0952 (PR 1650, Refs 1288, 111). Original artifacts preserved.

* `src/api/src/zava_forward/api/sensor_badges.py`: `freshness_state` returns `str(freshness)` for fresh/stale, fixing the return-value error.
* `src/api/tests/test_sensor_staleness_ui_badge.py`: imports `zava_forward.api.sensor_badges` directly (no `spec_from_file_location`); fixtures typed `dict[str, Any]`, fixing union-attr and `**` mapping errors.

Validation (from src/api): targeted unittest 5 OK; ruff check, ruff format --check, and mypy on both files all clean. Not pushed.

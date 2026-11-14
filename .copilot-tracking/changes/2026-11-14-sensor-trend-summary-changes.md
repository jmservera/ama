# Changes: 7-day sensor trend summary (Refs #1288, Refs #111)

Date: 2026-11-14. Plan: [plan](../plans/2026-11-14-sensor-trend-summary-plan.md).

* `src/core/src/zava_forward/core/sensor_view.py`: added `trend_summary` and a `trend` key on `view` (the `AssistantService.sensors` payload). `_select` gained an optional `sensor_id` filter. `capture_source`, the snapshot digest, `signature` and the model request are unchanged.
* `src/api/tests/test_sensor_trend_summary.py`: 10 unit tests (rising, falling, steady, bounded dense history, insufficient by count and span, unusable values, 7-day window, advisory provenance, consent withheld, trend outside capture and gates).
* Divergence from plan: none. Thresholds: 0.5 degC, 2 %RH; at least 6 readings and 24 hours of span.
* Local pre-commit validation: `unittest tests.test_sensor_trend_summary -v` 10 OK; `ruff check`, `ruff format --check`, `mypy` clean in `src/core` and `src/api`; sensor Quality tests in `src/api` (380 run, 140 skipped for missing SQL Server) OK. Imports resolved through `PYTHONPATH` to this worktree because the editable installs point at another checkout.
* Not done: no UI rendering of the trend, no live or model-consumption evidence, no hosted CI.

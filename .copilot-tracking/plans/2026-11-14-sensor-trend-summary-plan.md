# Plan: 7-day sensor trend summary (Refs #1288, Refs #111)

Date: 2026-11-14. Research: [research](../research/2026-11-14-sensor-trend-summary-research.md).

## Phases

* [ ] P1 `sensor_view.trend_summary(db, home_id, sensor_id, now, mssql)`: bounded read of the oldest 12 and newest 12 synthetic readings of the latest reading's sensor in the 7 days to `now`; compare mean of the earlier half with the later half per variable.
  * Per variable `direction`: `rising`, `steady`, `falling` or `insufficient`; thresholds 0.5 degC and 2 %RH.
  * `insufficient` when fewer than 6 usable readings or less than 24 hours between first and last.
  * Plain-language `text` per variable and overall `summary`.
  * `provenance`: `advisory_only` true, `affects_stage_gates` false, uncalibrated synthetic, deterministic basis.
* [ ] P2 `view` adds `trend` only when state is `ok`; otherwise an `insufficient` trend with the reason. `capture_source`, snapshot, digest and signature stay unchanged.
* [ ] P3 Tests in `src/api/tests/test_sensor_trend_summary.py`: rising, steady, falling, insufficient (count, span, no readings), consent withheld, advisory provenance, bounded query, snapshot digest unchanged, no stage-gate mutation.
* [ ] P4 Validate (unittest, ruff check, ruff format --check, mypy in `src/core` and `src/api`), commit, no push.

## Critique (single pass)

Direction from endpoint-half means is simple and robust to bounded reads; restricting to one sensor avoids mixing sensor offsets. Applied directly: skip non-numeric values, keep the trend out of the capture. No conflicts with confirmed decisions.

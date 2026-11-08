# Details: #1288 C3

Written 2026-11-08T20:54Z before product or test edits. Refs #1288.

## Files

* `src/core/src/zava_forward/core/sensor_view.py`: `capture_source` state, `_controls` count guard.
* `src/core/src/zava_forward/core/assistants.py`: `_withhold_sensors`, `_scrub_events`, `review`, `_enqueue`, `claim`, `scan`, `forecast`, `migrate`.
* `src/core/src/zava_forward/core/sensor_consumer.py`: `reconcile_control_home` and a `migrate_control_index` method; `_schema` calls it in place of the empty-only backfill.
* `src/api/tests/test_quality_sensors.py`, `src/core/tests/test_sensor_consumer.py`: regressions.
* `src/core/README.md`: short update.

## Interfaces frozen

* Task body gains `manual_requested: bool`; `dispatch.trigger` is `requested` unless the field is explicitly false at claim.
* Index reconcile derives only `sensor_consumer_control_home` from `sensor_consumer_control`; it writes no policy, control or consent row.
* Stored task and event bodies are never rewritten with projected values.

## Commands (light, SQLite, task-owned venv `/tmp/ama-1288-venv`)

From `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests /tmp/ama-1288-venv/bin/python -m unittest <module> -q > /tmp/c3-<name>.txt 2>&1; echo EXIT $?`. Ruff `--line-length 100` on changed new code. Not run: Mssql variants, FULL, browser.

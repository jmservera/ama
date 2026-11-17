# Issue 188 research: ingestion and backfill consistency

Base: origin/main eb51af5c9. Tier FOCUSED. Disposition: executed (opening record; findings appended below).

## Scope
Assess FR-050 / AC-066 criteria against merged main: queryable together per home, no handover discontinuity, idempotent window re-run. Issue comments state all three are live-Azure criteria, unticked.

## Measurements (2026-11-17, worktree src/core via PYTHONPATH, SQLite-backed fixtures, no SQL Server)
Command (from src/core): `PYTHONPATH=$PWD/src:$PWD/tests python3 -m unittest tests.test_sensor_handover tests.test_sensor_backfill tests.test_sensor_consumer tests.test_sensor_stream tests.test_sensor_consumer_live`
Result: 77 tests, OK, no skips in handover/live modules (an extra module name I guessed, `test_sensor_consistency`, does not exist; that ImportError is my selector mistake, not a product failure). Installed `zava_forward.core` points at the main checkout, hence the PYTHONPATH override.

## Criteria mapping on main
* Queryable together per home: `test_sensor_consumer_live.test_sunlight_retained_and_joins_backfill_series`, `test_sensor_backfill.test_load_reuses_validation_and_is_idempotent`.
* No handover discontinuity beyond tolerance: `test_sensor_handover` (zero and non-zero inclusive tolerances, step and stddev boundaries, weather reference, invalid tolerance refusal). `sensor_consistency.py` states the weather tolerance is not an approved operational tolerance.
* Idempotent window re-run: `test_sensor_consumer_live.test_accepts_and_replays_without_duplicate`, `test_envelope_round_trip_is_lossless_and_replays`, `test_sensor_consumer.test_append_replay_conflict_reopen_no_other_mutation`.

## Finding
No reproducible defect or coverage gap in source. The three criteria are live Hub-to-Azure SQL criteria per the 2026-11-11 and 2026-11-16 issue comments; local synthetic tests do not prove them. Not run: owned SQL Server suites (heavy-resource lock held by a full gate; SQL is FULL-tier scope).

Planning Readiness: Ready (evidence-only outcome).

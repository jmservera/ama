# Plan: issue 183 sensor backfill generator

* [x] Add `mvp/zavaforward_mvp/sensor_backfill.py`: seeded per-home series, faults, estimate, sharded CSV, manifest, validation, idempotent load, Azure SQL DDL.
* [x] Add `mvp/tests/test_sensor_backfill.py`.
* [x] Update `mvp/README.md` and `docs/reference/log.md`.
* [x] Run the mvp unit suite.
* Critique (single pass): keep one sensor per home and hourly cadence; do not import #110 code; record open items instead of inventing climate data. Applied directly.

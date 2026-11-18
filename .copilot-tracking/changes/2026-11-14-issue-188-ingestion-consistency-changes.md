# Issue #188 changes

* Added `src/core/src/zava_forward/core/sensor_ingest.py`.
* Added `src/core/tests/test_sensor_ingest.py` (6 tests).
* Divergence: first draft compared floats; a failing inclusive-tolerance test led to exact Decimal comparison.
* Validation: 63 sensor consumer, live, handover and ingest tests OK; ruff check and format check pass for `src/core`. Hosted CI not run (no push).

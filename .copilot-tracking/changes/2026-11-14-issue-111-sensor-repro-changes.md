# Issue #111 criterion 6 changes (2026-11-14)

* `src/core/src/zava_forward/core/sensor_analysis.py`: tuple-based `input_digest`, `reading_tuples`, `reproduce_sensor_analysis`.
* `src/api/tests/test_sensor_analysis_reproducibility.py`: version, order independence, drift, threshold and mixed-home tests.
* Validation: fast formula (63 tests, ruff, mypy) passed; core `test_sensor_analysis_reproducibility` and `test_sensor_analysis_store` (15 tests) passed. Full gate not run (focused tier).

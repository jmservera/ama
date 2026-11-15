# Changes

* src/api/src/zava_forward/api/live_simulator.py: dry run no longer prints raw readings.
* infra/tests/test_diagnostic_log_privacy.py (new, 7 tests).
* src/api/tests/test_diagnostic_log_privacy.py (new, 5 tests).
Validation (focused tier): ruff check and format pass; mypy 0 errors in 245 files; both unittest suites and tests.test_live_simulator pass. Hosted CI and full gate not run.

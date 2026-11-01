# Changes: gate browser evidence matcher (2026-11-01)

* `tools/rpi-checks.py`: new `_single_test_passed`; `check_skips` uses it for exact-test evidence.
* `tools/test_rpi_checks.py`: new test for interleaved pass accepted; FAIL, ERROR, no result, true skip, duplicate name, wrong name and missing test rejected.
* Validation: `python3 -m unittest tools.test_rpi_checks` 56 tests OK; ruff adds no new findings (pre-existing findings remain with the repo-less config).

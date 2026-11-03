# Issue 185 changes, round 2 (2026-11-03)

* Added `rotate()` to `src/core/src/zava_forward/core/synthetic/device_identity.py`.
* Added `RotationTests` (6 tests) to `src/core/tests/test_device_identity.py`.

Validation run (src/core): `PYTHONPATH=src python3 -m unittest tests.test_device_identity` (37 tests OK), ruff check, ruff format --check, mypy (module and test file, cache /tmp/mypy-185).
Not run: local RPI gate, full suites, benchmarks, live Azure.

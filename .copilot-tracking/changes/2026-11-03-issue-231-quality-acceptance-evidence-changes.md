# Changes: issue #231 slice 5

* `src/api/src/zava_forward/api/web/role-screens.js`: quality queue blocks handover text for accepted records without a named or independent accepter and for open defects without a named owner.
* `src/api/tests/test_technical_quality_screens.py`: new test with five subcases.

Validation run (PYTHONDONTWRITEBYTECODE=1): `unittest` for test_technical_quality_screens, test_role_screens_conformance, test_role_screens (29 tests OK, with PYTHONPATH including src paths); ruff check and format; mypy --cache-dir=/tmp/mypy-231 on the test file.
Not run: browser stories, full suites, gate, benchmarks. No security, infrastructure, SQL or deployment change, so no gate is claimed.

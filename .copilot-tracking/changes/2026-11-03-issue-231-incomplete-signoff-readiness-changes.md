# Changes: issue #231 slice 4

* `src/api/src/zava_forward/api/web/role-screens.js`: incomplete sign-off records are not valid and block readiness text.
* `src/api/tests/test_technical_quality_screens.py`: new blocking test (three broken shapes).

Validation run: `unittest` for test_technical_quality_screens, test_role_screens_conformance, test_role_screens (28 OK, with PYTHONPATH from the component guide); ruff check and format; mypy --cache-dir=/tmp/mypy-231 on the test file.
Not run: browser stories 231 and 231q, full suites, gate, benchmarks.

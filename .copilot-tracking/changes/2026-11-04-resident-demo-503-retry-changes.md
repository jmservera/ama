# Changes: resident demo 503 retry (#1054, slice 2)

* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: one automatic retry on view 503.
* `src/api/tests/test_resident_demo_script.py`: `busy` scenario and test.
* Validation run: test_resident_demo_script and test_resident_demo_api (49 OK), ruff check and format, mypy (tests included, `--cache-dir=/tmp/mypy-1054`, 175 files). Not run: gate, benchmarks, full suites, browser or live burst.

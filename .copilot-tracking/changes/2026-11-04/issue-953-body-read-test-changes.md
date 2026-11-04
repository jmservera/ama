# Changes: issue 953 slice 2

* Modified `src/api/tests/test_error_logging.py`: POST body-read reset regression test.
* Modified `docs/reference/log.md`: appended entry.

## Validation (focused tier)

* Run from `src/api`: `test_error_logging` (8 OK) with PYTHONPATH to src and tests dirs; `ruff check src tests`; `ruff format --check` on the test file; `mypy --cache-dir=/tmp/mypy-530 src` (clean).
* Not run: full suites, gate, benchmarks (no security, infrastructure, SQL or deployment change).

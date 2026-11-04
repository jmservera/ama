# Changes: issue 953

* Modified `src/api/src/zava_forward/api/server.py`: request-read disconnects log WARNING (phase=request-read); backend ConnectionError unchanged (500 and ERROR).
* Modified `src/api/tests/test_error_logging.py`: new regression test.
* Modified `docs/reference/log.md`: appended entry.

## Validation (focused tier)

* Run: `tests.test_error_logging` and `tests.test_bulk_edit_api` (13 tests OK); `ruff check src tests`; `mypy --cache-dir=/tmp/mypy-952 src` in `src/api` (clean).
* `ruff format --check` reports `server.py` as needing reformat; this is pre-existing on origin/main (verified by stashing) and was not changed.
* `mypy` on the test file reports unused `type: ignore` only because local PYTHONPATH/MYPYPATH replaces the installed stubs; not a repository change.
* Not run: full suites, gate, benchmarks (not required: no security, infrastructure, SQL or deployment change). No pyproject.toml edited.

## Divergences

None. The body-read branch (`_body_read_failed`) has no dedicated test; only the request-line and header read phase is tested.

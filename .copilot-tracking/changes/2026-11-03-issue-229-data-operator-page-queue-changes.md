# Changes: issue #229 slice 4

* `src/api/src/zava_forward/api/web/role-screens.js`: page-level conflict and return queue.
* `src/api/tests/test_data_operator_screen.py`: new unit test.
* `src/api/README.md`: note on the page-level view and its coverage limit.

## Validation run

* `python3 -m unittest tests.test_data_operator_screen` (api): 6 tests OK.
* `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-229` on the test file: clean.
* `data_operator_browser_check` with pinned axe 4.10.3: RESULT PASS (per-home view; it does not visit the page-level view).

## Not run

Gate, full suites, benchmarks, other browser checks. No assistive-technology or human review. No knowledge-base files changed, so no log.md entry.

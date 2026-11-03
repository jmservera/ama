# Changes: issue #229 slice 5

* `src/api/checks/data_operator_browser_check.py`: page-level queue assertions, Tab reach, reflow and axe.
* `src/api/README.md`: describes the new coverage.

## Validation run

* Browser check with pinned axe 4.10.3 and ZF_AXE_REQUIRED=1: RESULT PASS (both views).
* `tests/test_data_operator_screen.py`: 6 tests OK. ruff check and mypy (cache /tmp/mypy-229): clean.

## Not run

Gate, full suites, benchmarks, other browser checks. No assistive-technology or human review. No knowledge-base files changed, so no log.md entry.

<!-- markdownlint-disable-file -->
# Changes: issue-98-r1-manifest-freshness

## Added

* src/core/src/zava_forward/core/form_review.py: `_freshness` and `diagnostic_freshness` in `view`.
* src/core/tests/test_form_review.py: two freshness tests.

## Modified

* src/core/README.md: documents `diagnostic_freshness` and the remaining boundary.
* docs/reference/log.md: appended entry.

## Validation record

* Run: `PYTHONPATH=tests:src:../agents/src python3 -m unittest test_form_review test_form_staging -q` from src/core: 40 tests OK.
* Run: ruff check and format check on both Python files: passed. mypy `--cache-dir=/tmp/mypy-98` on both files: no issues.
* Not run: complete gate, full suites, API suite, benchmarks, SQL Server, browser, hosted CI.
* Note: the pre-installed zava-forward packages point at another worktree, so PYTHONPATH was used for this checkout.

## Divergences

None. No plan amendments.

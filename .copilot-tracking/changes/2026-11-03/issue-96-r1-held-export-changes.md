<!-- markdownlint-disable-file -->
# Changes: issue-96-r1-held-export

* Added `src/core/src/zava_forward/core/form_export.py`.
* Added `src/core/tests/test_form_export.py` (3 tests, run against JSON and SQL stores).
* Updated `src/core/README.md` and `docs/reference/log.md`.
* No divergence from plan. Validation (focused): ruff check and format, mypy `--cache-dir=/tmp/mypy-96`, `unittest test_form_export test_form_review test_form_staging` 41 OK.
* Not run: complete gate, API or full suites, benchmarks, SQL Server, browser, hosted CI.

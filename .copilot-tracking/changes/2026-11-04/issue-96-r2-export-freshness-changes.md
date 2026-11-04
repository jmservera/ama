<!-- markdownlint-disable-file -->
# Changes: issue-96-r2-export-freshness

* Added `BODY_KEYS` and `export_freshness` in `src/core/src/zava_forward/core/form_export.py`.
* Added three behavioural tests in `src/core/tests/test_form_export.py`.
* Documented in `src/core/README.md`; log entry in `docs/reference/log.md`.

Validation run: unittest test_form_export test_form_review test_form_staging (46 OK, JSON and SQL stores, PYTHONPATH set to this worktree's core src and tests because the installed core points at another worktree); ruff check and format; mypy --cache-dir=/tmp/mypy-96.
Not run: complete gate, API and full suites, benchmarks, SQL Server, browser, hosted CI.
Divergence: none.

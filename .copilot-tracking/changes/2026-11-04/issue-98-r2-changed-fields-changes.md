<!-- markdownlint-disable-file -->
# Changes: issue-98-r2-changed-fields

* src/core/src/zava_forward/core/form_review.py: `changed_fields` in `diagnostic_freshness`.
* src/core/tests/test_form_review.py: assertions for `changed_fields` (area changed; source-only change gives none).
* src/core/README.md, docs/reference/log.md: documented.

## Validation

* Run from src/core: `unittest test_form_review test_form_staging` 40 OK (JSON and SQL stores); ruff check/format; mypy `--cache-dir=/tmp/mypy-98` on form_review.py.
* Not run: complete gate, full/API suites, benchmarks, SQL Server, browser, hosted CI.

## Divergences

None.

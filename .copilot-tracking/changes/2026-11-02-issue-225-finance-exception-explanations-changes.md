# Changes: issue 225 finance exception explanations (2026-11-02)

* `role-screens.js`: `financeExplain`, `financeExplainRows`, `financeExceptionPanel`; each invoice block now ends with a grouped exception explanation table (exception, where, meaning, what a person still checks, who decides). Unchecked invoices and unknown codes show Unknown. Read-only, no controls, no server change.
* `test_finance_grants_screens.py`: explanation, clean-match and keyboard/semantics structural tests; fixture exceptions now carry codes.
* `atlas-screen-trace.md` and `docs/reference/log.md`: updated.
* Validation run locally 2026-11-02 (self-review only): `python3 -m unittest tests.test_finance_grants_screens tests.test_content_standard` from `src/api` (25 tests, OK, node harness); ruff check, ruff format --check and mypy on the test file clean. Full `src/api` discovery was run: 1629 tests, 11 errors, 323 skipped, not triaged and not attributed to this change. Focused gate result: see PR description. No browser, axe or assistive-technology run.

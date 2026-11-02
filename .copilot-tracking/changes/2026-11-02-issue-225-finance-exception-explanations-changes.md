# Changes: issue 225 finance exception explanations (2026-11-02)

* `role-screens.js`: `financeExplain`, `financeExplainRows`, `financeExceptionPanel`; each invoice block now ends with a grouped exception explanation table (exception, where, meaning, what a person still checks, who decides). Unchecked invoices and unknown codes show Unknown. Read-only, no controls, no server change.
* `test_finance_grants_screens.py`: explanation, clean-match and keyboard/semantics structural tests; fixture exceptions now carry codes.
* `atlas-screen-trace.md` and `docs/reference/log.md`: updated.
* Validation: see the PR description (focused gate `--changed`, never `--all`).

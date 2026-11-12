<!-- markdownlint-disable-file -->
# Changes: issue-98-denial-interface-1112

Base `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`; branch `research/funding-denial-interface-98-1112`; `Refs #98` only (criteria 2 and 3 stay unproven; no closure, tick or approval).

## Source

* `src/core/src/zava_forward/core/form_export.py`: `_issues_by_field` validates and groups `open_issues`; `export_freshness` names fields whose open-issue group differs between the saved and current export (only fields in the saved form; new-schema-field issues keep their schema-level reason) and gives the reason "An open validation issue changed." when only issues differ. A digest-valid copy with malformed issues is `Invalid`.
* `src/core/tests/test_form_export.py`: new `test_changed_open_issue_stales_only_its_field` (failing first on both stores) and `test_removed_open_issue_stales_and_malformed_issues_are_invalid`; `test_saved_export_goes_stale_only_for_dependent_fields` deliberately updated: a stale `epc` makes the conditional issue on dependent `area` change, so `area` is now named (FR-043 dependent propagation, per critique).
* `src/core/README.md`: one sentence on open validation issues.

## Divergences and amendments

* Critique (one, independent, `needs change`, compatible): applied direct validation of issue shape, accurate reason text, tests for removal, malformed and the conditional dependent. No conflict with a confirmed decision.
* First run after the fix had one regression, `test_new_schema_field_needs_review_even_when_no_field_is_stale` (issue for a field not in the saved form); fixed by restricting the comparison to saved fields. Original output kept as `after-form-tests-first-run-1-failure.out`.
* The source edit to `form_export.py` was first applied with a short Python replace script rather than the edit tool; the result is the committed diff.

## Validation (focused tier)

* Core `test_form_*.py`: 69 tests OK; API `test_finance_grants_screens.py`: 20 OK; ruff check clean; ruff format applied to the two touched files; mypy on `form_export.py` clean. Editable installs confirmed to import this worktree. Evidence in `.copilot-tracking/evidence/2026-11-12/issue-98-denial-interface-1112/`. Not run: complete local gate, SQL Server, browser, hosted CI.

## Follow-ups

1. Approved rules/template (FD-01 to FD-14): human Finance decision.
2. Case-scoped hold lineage (`draft_id=None`) is never evaluated per draft: needs a decision.

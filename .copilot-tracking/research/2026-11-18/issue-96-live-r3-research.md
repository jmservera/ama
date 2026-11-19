# Issue 96 live research, run 3 (opened 2026-11-18)

Refs #96. Demo, desktop only. Only unticked criterion: "Each assisted form has an approved versioned schema". Earlier runs (issue-96-live, issue-96-live-r2) found `{"schemas": []}` live and no code path setting `Approved`. This run re-verifies both against current main and the live demo and looks for any approval route (API, CLI, seed, importer) not yet considered.
Disposition: executed. Planning Readiness: pending findings.

## Findings

* Live (Entra employee, role Retrofit Programme Manager, desktop 1366x900, Playwright): `GET /api/form-schemas` returns 200 `{"schemas": []}` and `/api/form-schemas.csv` returns 200 with an empty body. Output: `.copilot-tracking/evidence/2026-11-18/issue-96-live-r3/probe.json` (credentials asserted absent) and `form-schemas-response.png` (a JSON body only, no account data).
* Repository at `eba446c9e`: `grep` for `approval.*Approved` over `src/*/src` finds only three read-side checks in `form_validation.py` (lines 170, 218, 232), retained in `approval-search.txt`. The only write route is `POST /api/form-schemas` (`server.py:1781`), which calls `forms.register_schema`, and that stores every version as `Unapproved`.
* 79 focused core tests pass (`test_form_staging`, `test_form_dependencies`, `test_form_export`, `test_form_review`, `test_form_criteria_5_6`, `test_issue_98_field_validation`); raw output `core-tests.txt`.
* Registering a throwaway schema live was considered and rejected: no delete route exists, so it could not be removed, and the result would be `Unapproved` regardless.
* Conclusion: criterion 1 cannot be proven for the demo. Approval is a named human act with recorded evidence; no shipped path records one.

Planning Readiness: Ready. Disposition: executed.

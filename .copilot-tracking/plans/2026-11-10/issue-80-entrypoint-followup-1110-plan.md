# Plan: issue 80 entrypoint follow-up (proposal only)

* Date: 2026-11-10
* Task: `issue-80-entrypoint-followup-1110`
* Research: `.copilot-tracking/research/2026-11-10/issue-80-entrypoint-followup-1110-research.md`; details and critique alongside (`details/`, `plans/...-critique.md`).
* Status: plan only. Implement and Review not run. No source, test, config or workflow change is authorised; no source allowance. Every-list criterion UNPROVEN; criterion 2, criterion 4 and #73 open.

## Evidence position

For role pam on the synthetic populated fixture at pin `583d4fbd`: no `packages.csv` or `workorders.csv` control was located on `#/capacity` or the Package queue `ZF-1` screen; no rendered control produced `cases.csv?report=progress` on My cases, All cases, the progress dashboard or the overview. The server routes `packages.csv` and `workorders.csv` exist and respond 200 to the same role. Three driver stages remain unobserved.

## Options for Root (not decided here)

1. Accept the observation as scenario-qualified: the two CSV routes exist without a reachable staff-page control for the manager role in this fixture; treat as a gap against "Every list offers an Excel or CSV export" if Root reads the criterion that way. Whether a list screen must carry its own control is a requirement reading Root owns.
2. If Root authorises implementation, the smallest proposal uses existing contracts: add one `Download for Excel` anchor (`href="/api/packages.csv"`, `download="packages.csv"`) beside the Packages heading and one (`/api/workorders.csv`, `workorders.csv`) beside the Work orders heading in `capacityView` (`web/ops.js`), copying the existing pattern at `web/ops.js:246` including the one-way read-only sentence. Roles unchanged (manager-only screen, same as the JSON reads); routes, `LIST_EXPORTS`, projections and retention unchanged. Regression selectors: `a[download='packages.csv'][href='/api/packages.csv']` and `a[download='workorders.csv'][href='/api/workorders.csv']` on `#/capacity` (populated fixture), plus the existing `api/tests/test_list_export_api.py` role checks. Web edits first need the web-design-guidelines fetch and Fluent 2, WCAG and plain-language precedence read, not done. Nothing is implemented.
3. Progress variant: no change proposed. The bare route needs `as_of` and the progress dashboard is a separate register; adding a control is a requirement decision. The two URL probes can be observed in a separately authorised run if Root wants them.

## Decisions Root owns

* Reading of the criterion for per-screen controls, and whether the progress variant needs one.
* Whether to authorise the option 2 change and its validation.
* Whether to authorise another observation of the three unobserved stages.

Out of scope: other roles and registers, owner thresholds, Excel writeback, acceptance or AT approval, push, PR or GitHub change.

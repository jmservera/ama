# Issue 96 live research (opened 2026-11-18)

Task: issue-96-live. Refs #96. Demo, desktop only, docs/evidence only.
Unticked criterion: "Each assisted form has an approved versioned schema".
Research disposition: executed. Planning Readiness: pending findings below.

## Findings
* `forms.register_schema` (src/core forms.py:355-386) always stores `approval="Unapproved"`, `approval_evidence=None`, `source_policy_status="Unapproved"`. No shipped code path sets "Approved"; only a read-side gate (`form_validation._approval_gaps`) checks it.
* Live demo `GET /api/form-schemas` (Entra employee, 200) returns `{"schemas": []}`; the CSV export is empty. No assisted form schema is registered on the demo.
* 67 focused core form tests pass (staging, dependencies, export, review, criteria 5/6).
* Approval is a named human (Finance/Legal/programme owner) act; production-only, deferred to #1905-#1908.
Planning Readiness: Ready. Disposition: executed. Evidence: `.copilot-tracking/evidence/2026-11-18/issue-96-live/run1.json`.

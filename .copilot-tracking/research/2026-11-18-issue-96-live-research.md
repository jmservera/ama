---
title: Issue 96 live demo research
ms.date: 2026-11-18
---

## Disposition

Research disposition: executed (opening record; findings added below as they land).

## Task

Issue #96. One unticked criterion: each assisted form has an approved versioned schema. Prove it on the deployed synthetic demo or state why not. Docs and evidence only.

## Findings

* Only criterion 1 is unticked: "Each assisted form has an approved versioned schema". The other five are ticked and were not re-opened beyond the offline tests below.
* Code: `forms.register_schema` always records `approval="Unapproved"`, `approval_evidence=None`, `source_policy_status="Unapproved"`; versions are immutable (next version only). No source path sets `Approved` (`form_schemas` is written only at `forms.py:380`). `form_validation._approval_gaps` treats a missing approval as a gap and reports Not evaluated.
* Live (staff sign-in, Retrofit Programme Manager, 16 demo cases): `/api/form-schemas` 200 with `{"schemas": []}`; the CSV is empty; one case's `form-candidates` has no batches and `form-review` has no drafts or holds, with the Unapproved notice. So the deployed demo holds no registered schema, approved or not.
* Registering a throwaway schema would add an immutable record with no delete route, so it was not done. It could only show `Unapproved`, which does not prove the criterion.
* Offline: `test_form_staging`, `test_form_review`, `test_form_dependencies` (core) 67 tests OK.
* Criterion 1 cannot be proven for the demo: approval is a named human template and source-policy approval, not an engineering result.

## Evidence

`.copilot-tracking/evidence/2026-11-18/issue-96-live/` (`probe.py`, `probe1.json`, `form-schemas-response.png`, `offline-core-tests.txt`). Record: `docs/reference/research/issue-96-live-demo-evidence-2026-11-18.md`.

## Planning Readiness

Ready: no further investigation required.

# Research: issue 231 technical queue and quality screens (2026-11-01)

Task: issue-231-retrofit-technical-quality-screens. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` (merged for #226) provides `registerRoleScreen({id,title,roles,load,render})`, helpers `screenPanel`, `screenFields`, `screenTable`, `screenUnknown`, `assetAgeDays`, and the explicit-home, read-only, no-write boundary. The loader needs no change.
* Technical data: `core/signoffs.py` defines four separate sign-offs (assessment: Quality Inspector; design: Retrofit Coordinator; building: Building Safety Liaison; coordination: managers), `technical.design_version`, per-sign-off `status` (Signed off, Returned, Needs reassessment, Not given) with `version`, `by`, `reason`, `history`. Case detail exposes `technical`, `technical_missing` (item plus `assigned_to`) and `checklist` (evidence kind, present).
* Source facts: `stock_reconciliation` and events (same as #226).
* Quality data: `core/quality.py` records per measure with `state` (Submitted, Accepted, Returned, Fixed awaiting reinspection, Handed over, Superseded), `items` (label, evidence), `defect` (owner, description, raised_by, fixed_by, remediation_evidence), `evidence_version`, `checklist_version`. Case `measures` is a list or comma string.
* Roles: no assessor or designer role exists; competent roles are the sign-off roles above. No role simulator needed.
* Journey sources are desk hypotheses, not observed behaviour; validation sits in #155.

## Decisions

* Register two read-only screens: "Technical queue" (Retrofit Coordinator, Quality Inspector, Building Safety Liaison, managers) and "Quality queue" (Quality Inspector, managers).
* Readiness is derived only from recorded evidence: design exists, every sign-off Signed off on the current design version, no missing items. Anything else shows a blocked panel with owner and next action.
* Returns show the competent role for that sign-off, never a generic approval.
* Quality handover shows blocked unless every case measure has an Accepted or Handed over record with no open defect.

## Not in scope

Server changes, write actions, observed validation (#155), browser/axe run (CI).

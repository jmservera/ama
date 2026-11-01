# Research: issue 232 housing officer and resident engagement screens (2026-11-01)

Task: issue-232-housing-officer-screens. Disposition: executed (focused, reuse of #226 pattern). Planning Readiness: Ready.

## Evidence

* `src/api/src/zava_forward/api/web/role-screens.js` hosts `#/screens` with `registerRoleScreen({id,title,roles,load,render})`, bounded queue, explicit home selection, read-only (merged for #226). `app.js` lazy-loads it, so no loader change.
* Case view (`GET /api/cases/{id}`) already exposes `measure_decisions` (list: measure, status, readiness, context scope/revision/design_version, versions with status, answered_by, note, recorded_by, next_update), `resident_update` (purpose, owner_identity, due_at, basis, safe_contact_ref, status, version) and `service_requests` (route, status, accessibility, next_update). Resident-view roles are `RESIDENT_VIEW_ROLES` in `core/controls.py` (Resident Liaison Officer, Retrofit Coordinator, plus the two managers). Other roles have these fields stripped by `projection.py`.
* Decision statuses are Waiting, Accepted, Declined, Paused, Withdrawn; Paused or Withdrawn is a resident decision recorded in their words and is separate from contact history and access needs (`ACCESS_CODES`). Contact or access is never treated as a yes (existing panel copy).
* Existing `panels.js` resident panel is a case-workspace write form; this slice is a distinct read-only queue screen.
* Journey sources (frontline.md, residents.md, atlas O01-O05, O13, O15) are desk hypotheses, not observed behaviour; validation sits in #155.

## Decisions

* Register one screen, "Resident choice and update queue", for `RESIDENT_VIEW_ROLES`.
* Per selected home: measure table (version-specific choice, scope revision and design version, linked answer note), pause or withdrawal as its own labelled panel, update commitment (purpose, owner, due, safe route reference, version), access needs and service requests shown separately from decision state.
* No contact is made, no form or button; links to case workspace for recording and #154 for resident-facing designs.

## Not in scope

Server changes, resident-facing screens (#154), observed validation (#155), new roles.

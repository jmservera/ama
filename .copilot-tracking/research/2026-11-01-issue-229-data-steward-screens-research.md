# Research: issue 229 data steward and digital operator screens (2026-11-01)

Task: issue-229-data-steward-screens. Disposition: executed (focused, reuses issue 226 research). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` provides `registerRoleScreen({id,title,roles,load,render})`, a bounded permitted-case queue, explicit home selection, abort handling and no writes. The issue 226 screen `asset-board` is the pattern; helpers `screenPanel`, `screenTable`, `screenFields`, `screenUnknown`, `screenPerson`, `screenStamp` are reusable.
* Conflict data: `core/stock.py` and `core/store.py stock_query_event` give `stock_reconciliation` (left/right assertion with value, source_id, date, version, validation_state; query_owner; authority/resolution/eligibility "Unknown") and `stock_reconciliation_events` (id, query_id, status Withdrawn/Reconciled, reason, evidence, `at`, `recorded_by`). Events are narrative dispositions, not an audit trail; the audit log is separate.
* Returned and exception work: `case.work` (owner, reason, next_action, source, evidence, version, recorded_at, as_of, handoff with destination/proposed/confirmed receiver/chase owner, `blockers[]` with step/reason/owner/next_action/source/version). Missing values stay Unknown.
* Roles: no data steward, analyst or digital operator role exists; `MANAGER_ROLES` is the nearest authority (same as issue 226). No role simulator is added.
* PRD "Profile Journey Contract": Digital operator and auditor, conflict/return queue -> both source values/provenance (646), illustrative event metadata and recovery context (863); preserve unresolved eligibility and original source; no replay, silent correction or audit-trail claim. Journeys in `customer-journeys/data.md` are desk hypotheses.

## Decisions

* Register one screen `data-operator`, "Data steward and operator view", for MANAGER roles, read-only, no new endpoints.
* Panels: evidence boundary; conflict and return queue (both values, source id, version, date, validation state, owner, status); eligibility Unknown and original source preserved; exception queue from work blockers and handoff with owner and next action; event metadata and recovery context with an explicit not-an-audit-trail note.
* No replay, correct, resolve or retry controls.

## Not in scope

Server changes, observed validation (#155), real integration monitoring (no source exists; shown as Unknown with owner).

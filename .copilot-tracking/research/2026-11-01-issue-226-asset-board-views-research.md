# Research: issue 226 asset executive and board views (2026-11-01)

Task: issue-226-asset-board-views. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` renders `#/screens` with a bounded permitted-case queue, explicit home selection, no writes, and `registerRoleScreen({id,title,roles,load,render})`. No screen is registered yet, so the slice adds the first.
* Stock comparisons: `core/stock.py` and `panels.js stockPanel` expose `stock_reconciliation` (field, left/right assertion with value, source_id, date, version, validation_state, query_owner, authority/resolution/eligibility all "Unknown") and `stock_reconciliation_events` (terminal Withdrawn or Reconciled). Source age is derivable from assertion `date`.
* Roles: no asset, executive or board role exists in fixtures; `STAFF_ROLES` and `MANAGER_ROLES` are the nearest. `/api/ai/report` is manager-only and returns `consumption` with `cost_per_accepted_proposal`, `token_cost`, `quality_status`, `evidence_label`, `cash_value` (Unknown by default; no price source, BRD OD-51).
* Journey sources (asset.md, reviewer.md) are desk hypotheses; budgets, priorities, forecasts, eligibility and board data are unknown company details.
* Loader: `app.js` lazy-loads `/role-screens.js` for `#/screens`, so a screen added to that file needs no loader change.

## Decisions

* Register one screen, "Asset and board view", for MANAGER roles (no role simulator, no new server authority, read-only).
* Per selected home: stock conflict comparison with source age, missing investment inputs (all Unknown, named owner or "Unassigned" action), eligibility Unknown with owner, benefits and phase gate Unknown, evidence boundary, no approval control.
* Separate portfolio scope panel: permitted-case count labelled as role scope, not stock total.
* Board panel: AI cost per accepted outcome beside quality floor and value status with evidence class; never a token-only figure.

## Not in scope

Server changes, observed validation (#155), investment approval, real budgets.

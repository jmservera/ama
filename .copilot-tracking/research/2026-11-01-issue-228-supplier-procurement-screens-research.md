# Research: issue 228 supplier, contractor and procurement screens (2026-11-01)

Task: issue-228-supplier-procurement-screens. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` renders `#/screens`: bounded permitted-case queue, explicit home selection, no writes, `registerRoleScreen({id,title,roles,load,render})`. `app.js` already routes contractors to `#/screens` and lazy-loads the file. The merged #226 screen (`asset-board`) is the pattern: `screenPanel`, `screenFields`, `screenTable`, `screenUnknown`, node-vm tests in `src/api/tests/test_asset_board_screen.py`.
* Server data already exists. `GET /api/packages` (managers): name, period_from/to, contract_ref, contract_version, scope, scope_version, per-contractor capacity (offered, committed, in_use, headroom, evidence, evidence_status, version). `GET /api/workorders?case=` returns work orders; contractors see only their own, with `needs_notice` and a named contact, never the vulnerability reason (`core/procurement.py _wo_view`, `projection.py`).
* No server endpoint exists for contractor job pack submission, acknowledgement, correction or reviewer acceptance. PRD line 828 marks the contractor job pack "Deferred; separate decision", needing supplier-scoped access design and BRD OD-47. `/api/checklists` is staff-only (contractor GET allow-list: me, cases, case, workorders).
* Journey sources (`suppliers.md`, atlas O08 and O11) are desk hypotheses: committed versus offered capacity, versioned scope, human dispatch and QA acceptance, worker confirms and QA accepts.

## Decisions

* Two read-only screens in `role-screens.js`, no server change, no new role, no write control:
  * `procurement-packages` "Package queue" for managers: per package period, scope and scope version, contract or call-off reference and version, offered versus committed capacity, work-order references for the selected home. Draft readiness only, with unmet prerequisites and the next reviewer named or Unassigned.
  * `contractor-job-pack` "Job pack and evidence checklist" for `Contractor`: own work-order reference, version, scope, notice flag and named contact; evidence checklist items all "Not supplied"; submission and acknowledgement recorded separately from independent review and acceptance; no reason for notice.
* The submit and correct actions are not built (no authority or endpoint). The screen says how to submit (named contact) and that nothing is sent from the screen.

## Not in scope

Server changes, provider portal, identity claims, booking, self-approval, observed validation (#155), browser and axe run (no playwright locally).

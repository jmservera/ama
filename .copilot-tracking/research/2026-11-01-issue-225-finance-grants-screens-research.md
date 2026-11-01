# Research: issue 225 finance and grants screens (2026-11-01)

Task: issue-225-finance-grants-screens. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* Host `src/api/src/zava_forward/api/web/role-screens.js` (pattern merged for #226): `#/screens`, bounded permitted-case queue, explicit home selection, read-only, `registerRoleScreen({id,title,roles,load,render})`; helpers `screenPanel`, `screenTable`, `screenFields`, `screenUnknown`, `assetCost`. `app.js` lazy-loads this file, so no loader change.
* Case record (`GET /api/cases/{id}`) carries `finance` (budget, commitments with measure/quantity/amount/work_order, invoices with lines measure/quantity/amount/milestone_ref, exceptions per line, hold, disposition, payment_status), `grants` (state, pending, history with source/approver) and `funding` (route, status, reference).
* `core/finance.py match_invoice` already compares quantity, scope, budget, over-commitment, duplicate and accepted milestone evidence per line; `FINANCE_ROLES` = Grants and Evidence Officer plus the two manager roles; `FINANCE_APPROVERS` = managers. Payment is record-only (`PAYMENT_NOTE`).
* `GET /api/cases/{id}/form-review` (`form_review.view`) returns constructed field drafts: template, rule_refs, funding, per-field state/value/evidence, issues (Conflict for unreviewed source alternatives, Unknown for stale or missing), `reviewed_ready=false`, `status=Held`, notice that no eligibility, submission, award or payment is established.
* `GET /api/ai/report` is manager-only; `consumption` gives quality floor, evidence label and cash value (Unknown by default, BRD OD-51 open). Non-managers get 403, so cost stays Unknown.
* Journey sources (finance.md, atlas O16/O17) are desk hypotheses, not observed behaviour; validation is #155.

## Decisions

* Two read-only screens for FINANCE_ROLES (no role simulator): "Invoice queue" (approver and payment officer view) and "Funding route and claim pack" (grant preparer view).
* Invoice screen: queue of invoices across cases from `/api/finance` plus, for the selected home, line-level comparison against commitment (measure, quantity), version (invoice record id and commitment), budget and milestone evidence; exceptions by line; unknown where absent; payment status shown as a record only; AI economics section (token component only with a passed quality floor, otherwise Unknown).
* Funding screen: route and template, grant stages with evidence, constructed field draft with conflict and stale states, readiness export view that is always "Held" unless backend says otherwise; no submission, award or payment inferred.
* No server change; no controls on either screen.

## Not in scope

Observed validation (#155), approval actions, real prices or budgets, Playwright scenario (SCENARIOS registry empty on main).

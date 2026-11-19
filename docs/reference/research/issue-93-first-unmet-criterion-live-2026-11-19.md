---
title: Epic 93 first unmet demo criterion, stabilization re-check (2026-11-19)
description: Per-criterion proven and unproven table for epic 93, fresh offline and live evidence, a BRD identifier mismatch in the issue body, and why the first unmet criterion needs no code
ms.date: 2026-11-19
ms.topic: reference
---

Refs #93. Scope is the synthetic demo, desktop only, on branch base `b9e3f98d4` (origin/main had advanced to `e5a9a59d9`). Owner decisions of 2026-11-18 apply: live Azure authorised in resource group `ama`, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive technology testing are not needed. No source file changed, no Azure resource was created (nothing to delete), no demo record was written and nothing is ticked in any issue.

## First unmet criterion

Issue #93 has three criteria. C1 (stabilization checkpoint #440) is the first unticked one. C1 asks for BRD/PRD and ADR reconciliation, local regression checks, bug disposition and a recorded owner decision on residuals. That is evidence and governance work. No finding in this task or in the [2026-11-18 audit](./issue-93-epic-audit-live-2026-11-18.md) is a confirmed defect on the finance surface, so there is nothing a test-backed code change could fix. The task therefore adds evidence only.

## Fresh evidence (2026-11-19)

* Offline, from `src/core`: `PYTHONPATH=src:tests:../agents/src:../agents/tests python3 -m unittest -v` over `test_finance_no_automated_path_93`, `test_finance_match_controls`, `test_finance_signoffs`, `test_grant_lifecycle_controls`, `test_exposure_limits`, `test_funding_automation_boundary`, `test_form_staging`, `test_form_review`, `test_form_review_pack`, `test_form_dependencies`, `test_form_export`, `test_form_criteria_5_6`: 269 tests in 379.6 s, OK, 45 skipped (opt-in local SQL Server; not claimed as passed). Log: `.copilot-tracking/evidence/2026-11-19/issue-93-live/offline-core-tests.txt`.
* Azure, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` returned revision `ca-cutover-test-demo-api--0000033` (0000031 on 2026-11-18) with image digest `sha256:5368f4e4...`, the same digest as the earlier notes.
* Live, Playwright Chromium 1366 by 900, employee demo account signed in through Entra, credentials read at run time and never printed or saved, e-mail and GUID scrubbed (scan of the saved JSON found no `@`). Five GET calls, all HTTP 200, no write, no screenshot (it could show the account name): `/api/me`, `/api/finance`, `/api/finance/exposure`, `/api/funding`, `/api/form-schemas`. Files: `live_probe.py`, `live_probe.json`, `live_probe_summary.txt`, `az_revision.json`.
  * Finance: 13 invoice rows, 7 `Received` and 6 `Exceptions` with 6 on hold; none paid, approved or cleared.
  * Exposure: status `Held`, signal "Pause for human decision", `automatic_cut` false, `decision_owner` null, notice that it does not approve, resume or accelerate delivery.
  * Funding: 167 cases (1 `Draft ready`, 25 `To prepare`, 141 `Not started`); grants column "No grant record" for 163 and "Not recorded" for 4; no award, claim or cash.
  * Form schemas: `{"schemas": []}`.
* GitHub, read on 2026-11-19: #93, #96 and #440 OPEN; #94, #95 and #99 CLOSED. #96 holds one unticked criterion and its latest comment (2026-11-18) says it needs a named human approval of a schema. No owner deferral of #96 and no recorded owner pivot for #93 exists.

## Reconciliation finding: issue body cites the wrong BRD identifiers

The #93 body lists "BRD: BG-007, BG-008, FR-018, FR-019, RULE-009 to RULE-012, CON-005, CON-006". In `docs/brds/agentic-retrofit-programme-brd.md` (last changed in `0ae7583fc`), FR-018 is the human handoff rule and FR-019 is capacity evidence. The finance rows are FR-023 (four mutually exclusive grant states), FR-024 (grant transition evidence), RULE-009, RULE-010 (no automated bid, match approval, claim certification or cash), RULE-012 (downside tolerance pause), CON-005 and CON-006. The PRD FR-018 and FR-019 are the finance requirements the body means. The collision is already known (see the [440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md)); correcting the issue body is an owner action and was not done here.

Traceability by acceptance criterion: AC-035 (RULE-010) is exercised in `test_finance_no_automated_path_93`, `test_funding_automation_boundary` and `test_journey_acceptance`; AC-038 (RULE-012) is implemented in `journey_acceptance.py` and shown live by the Held exposure signal; AC-032 and AC-033 (FR-023, RULE-009) are satisfied by the live funding view showing no secured amount and by the grants column, but have no test named by those identifiers (not a defect, a traceability gap).

## Per-criterion table

| Issue | Criterion | Result | Evidence | Why |
| --- | --- | --- | --- | --- |
| #93 C1 | Stabilization checkpoint #440 | Unproven | Sub-points below | #440 is OPEN with two unticked criteria; the criterion says merged children alone do not satisfy it; no owner pivot or deferral decision is recorded |
| #93 C1a | BRD/PRD and ADR reconciliation | Proven for finance rows | Identifier finding above; ADR-0001/0002 (Azure SQL) unchanged | Issue-body ID mismatch needs owner edit |
| #93 C1b | Local-first regression checks | Proven | 269 tests OK, 45 skipped | SQL Server variants skipped, not claimed |
| #93 C1c | Bugs dispositioned | Proven | No finance defect confirmed; the open drafts D1 to D4 in the 440 triage gate other epics, not #93 | Unchanged since 2026-11-18 |
| #93 C1d | Azure-only residuals and owner pivot or defer decision | Unproven | Live read-only probe | The owner decision is a human act; the residual is #96 schema approval |
| #93 C2 | All child features closed or deferred | Unproven | #96 OPEN | Needs #96 closed or an owner deferral |
| #93 C3 | No automated bid, match approval, claim certification or cash | Proven again | Offline tests plus live views with no paid, awarded or cash state | Already ticked; no contradiction |
| #96 C1 | Approved versioned schema | Unproven | `/api/form-schemas` empty; registry append-only with no delete route | Needs a named approver; a throwaway schema cannot be cleaned up |

## Unmet criteria

#93 C1 and C2 and #96 C1. Owner actions that would clear them: record a continue verdict and the #96 deferral or schema approval, and correct the BRD identifiers in the #93 body.

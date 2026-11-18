---
title: Epic 93 finance, grants and form-assisted funding audit with live demo read (Refs #93)
description: Per-criterion evidence table for epic 93, the remaining demo gaps for child 96, production-only items, and a fresh read-only live probe of the synthetic demo on 2026-11-18
ms.date: 2026-11-18
---

Refs #93. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive Azure billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. This note ticks nothing in any issue. No source code changed, no Azure resource was created (nothing to delete) and no demo record was written.

## Method and retained evidence

* Issue state read with `gh issue view` on 2026-11-18 for #93, #94, #95, #96, #99 and #440.
* Azure CLI, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` returned revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4...c17e5fb` (unchanged from the other 2026-11-18 notes), `ZF_STORE` `mssql`, `ZF_DEPLOYMENT_PROFILE` `demo`.
* Playwright Chromium, 1366 by 900, Entra sign-in as the employee demo account (role Retrofit Programme Manager). The driver read credentials at run time, never printed or saved them and scrubbed e-mail addresses and GUIDs; a scan of the saved JSON found no `@`. Five GET calls only (`/api/me`, `/api/finance`, `/api/finance/exposure`, `/api/funding`, `/api/form-schemas`), all HTTP 200, no write. The landing screenshot was deleted because it could show the account name; the proof is the JSON.
* Offline: from `src/core`, `PYTHONPATH=src:tests:../agents/src:../agents/tests python3 -m unittest -v` over `test_finance_no_automated_path_93`, `test_finance_match_controls`, `test_finance_signoffs`, `test_grant_lifecycle_controls`, `test_exposure_limits`, `test_funding_automation_boundary`, `test_form_staging`, `test_form_review`, `test_form_review_pack`, `test_form_dependencies`, `test_form_export` and `test_form_criteria_5_6`: 269 tests, OK, 45 skipped (19 "opt-in isolated local SQL Server", 26 "opt-in local SQL Server"). The skipped tests are not claimed as passed.
* Files are in `.copilot-tracking/evidence/2026-11-18/issue-93-live/`: `live_probe.py`, `live_probe.json` (trimmed), `live_probe_summary.json`, `offline-core-tests.txt`.
* Reused, not repeated: the [#96 live demo evidence](./issue-96-live-demo-evidence-2026-11-18.md), the [#96 schema approval check](./issue-96-live-form-schema-approval-evidence-2026-11-18.md) and the [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md).

## Fresh live observations (2026-11-18)

* `/api/finance`: 13 invoice rows; 7 `Received`, 6 `Exceptions` with 6 `on_hold` true. Row fields are address, case, invoice, supplier, reference, status, exceptions, hold and total. No row status is paid, approved or cleared, which fits record-only.
* `/api/finance/exposure`: status `Held`, signal "Pause for human decision", reason "No person-approved envelope or tolerances are recorded.", `automatic_cut` false, `decision_owner` null, notice "does not approve, resume or accelerate delivery".
* `/api/funding`: 167 cases; statuses 1 `Draft ready`, 25 `To prepare`, 141 `Not started`; grant column is `No grant record` for 163 and `Not recorded` for 4. No case shows an award, claim or cash.
* `/api/form-schemas`: `{"schemas": []}`. The demo holds no registered form schema.

## Epic 93 acceptance criteria

| # | Criterion (state on the issue) | Demo result | Evidence | Tickable now |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Not met | #440 is OPEN with two unticked criteria (triage into independent RPI issues with owner approval for pivots and deferrals, and the PR research, plan, changes and review artifacts for the coordinator change). The [triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) gives #93 the verdict "Continue", names #96 as its only open child and records no blocking finding for #93. The criterion states that merged children alone do not satisfy it. | No. Needs #440 closed and the owner's recorded pivot or deferral decision for #96. |
| 2 | All child features closed or deferred (unticked) | Not met | #94, #95 and #99 CLOSED. #96 OPEN with one unticked criterion. No owner deferral of #96 is recorded. | No. Needs #96 closed or an explicit owner deferral. |
| 3 | No automated path submits a bid, approves match funding, certifies a claim or records cash (ticked) | Consistent, fresh | Offline: `test_finance_no_automated_path_93` (guard `verify_no_automated_finance_authority`, all four operations refuse automated actors with zero mutation, AI proposals never apply, agents and orchestrator expose no such path) and `test_funding_automation_boundary` passed in the 269-test run. Live: finance and funding views carry no paid, awarded, certified or cash state; the exposure signal states it cannot approve, resume or accelerate. | Already ticked; no contradiction found. |

## Remaining gap for child 96

| Criterion | Exact remaining gap for the demo | Class |
| --- | --- | --- |
| Each assisted form has an approved versioned schema (unticked) | The demo has zero schemas. Code registers schemas only as `Unapproved` and no source path writes `Approved`; downstream validation reports Not evaluated without a human-recorded approval bound to the schema digest. Approving a template is a named human decision (Finance or template authority), outside engineering. | Owner decision: appoint a demo template approver, register one synthetic schema and record the approval. Registry is append-only with no delete route, so a throwaway schema cannot be cleaned and was not created. Approval of a real funder template is production-only. |
| Five ticked criteria (lineage, per-field review, validation, export, dependent staleness) | Not re-proven on the deployed demo because no schema exists; offline tests above pass (included in the 269). | Dependent on the schema decision above. |

## Production-only items (not demo gaps)

* Board-approved envelope and tolerances (OD-12, OD-15) for #99 and actual funder form templates and rules for #96: real company and funder inputs, deferred to the production follow-ups #1905 to #1908.
* Form-specific MSSQL results beyond the demo store, the 45 skipped SQL-Server tests and real submission, payment or award workflows: excluded by the no-drills and no-production decisions.
* DPO and Legal approval, billing reconciliation and assistive technology testing: waived for the demo by the owner decision.

## Unmet criteria

C1 and C2 on #93, and C1 on #96. Nothing in this note changes any issue.

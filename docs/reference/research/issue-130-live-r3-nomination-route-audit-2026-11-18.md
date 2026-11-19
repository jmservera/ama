---
title: Third live audit of the nomination, self-referral, acknowledgement and challenge route (issue 130)
description: Third 2026-11-18 audit with raw output retained, a per-criterion proven or unproven table, and production-only items separated
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - live demo
estimated_reading_time: 4
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18: live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This run repeats the [first](./issue-130-live-nomination-route-evidence-2026-11-18.md) and [second](./issue-130-live-r2-nomination-route-evidence-2026-11-18.md) runs. No source file changed, no Azure resource was created or changed, nothing needs deleting, and no issue box is ticked.

## Method

* Issue read with `gh issue view 130`: one unticked criterion (representative participation and comprehension need authorized human evidence); all other boxes are ticked on the issue.
* Azure CLI, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api`. Revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`. Both are identical to the second run, so no fix has been deployed. `ca-resident-demo` was not exercised.
* Playwright Chromium at 1366 by 900, signed in as the employee demo account. Credentials were read at run time and never printed; a literal scan of the evidence directory for each credential value found no match, and e-mail addresses are scrubbed.
* Case: synthetic `ZF-2025-0331`. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-130-live-r3/`: `probe1.py`, `common.py`, raw `probe1.out.txt`, `image-digest.txt`, `offline-core-tests.txt`, `offline-api-tests.txt`, plus a read-only listing probe (`live_nomination_probe.py` and `.json`) and `nomination-routes-1366.png`.
* Writes attempted are the same five as run 2 against one case; none succeeded, so 0 nomination records existed before and after and stage and days in stage were unchanged. Nothing to clean up.

## Live results

| Probe | Result |
| --- | --- |
| `GET /api/cases/ZF-2025-0331` permissions | 200; `can_view`, `can_write`, `can_submit_digital`, `can_submit_staff_recorded_non_digital` true; 1 staff owner; `representative_authorities` empty; 7 channels, 5 assisted, 6 challenge |
| Valid staff-recorded phone referral, owner not staff, role name as owner, `hazard_concern` null | All 403 "Reload your current staff identity before recording this step." |
| Referral with `representative_ref` and `raised_by` | 400 "Supply only permitted route fields", naming both fields |
| `?view=nomination-routes-html` | 200; text "Urgent hazards use the hazard reporting route immediately and are never queued here. A named person owns every review and response."; "No referrals recorded." and "No challenges recorded." |
| `GET /api/cases` | 200, 16 cases; the same route view renders for the first listed case |

## Offline results

* `src/core`: `test_nomination_route`, `test_challenges`, `test_nomination_bootstrap`, `test_challenge_no_retaliation_220`, `test_hazard_referral`, `test_issue_220_challenge_route`: 91 tests, OK, 1 skipped.
* `src/api`: `test_nomination_api_routes`, `test_nomination_screen`: 14 tests, OK.
* Covered by name in the files read: competing evidence retained for resident and representative challenges (`test_ac2_resident_and_representative_challenge_retain_competing_evidence`), unknown identity, support needs and risk flags kept `Unknown`, and the staffed non-digital route with named owner and staff-recorded acknowledgement.

## Cause of the write refusal

Unchanged from run 2: `resident_decisions._operation` refuses a write when the resolved actor differs from the roster person for the signed-in e-mail. Changing it alters a security identity control in `src/core` and needs a redeploy and the FULL tier, so this docs-only audit does not touch it.

## Per-criterion result

| Criterion in #130 | Issue state | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| Representative participation and comprehension need authorized human evidence | Unticked | Unproven; cannot be proven for the demo | Needs real representatives and residents. The demo has no confirmed representative authority (empty `representative_authorities`) and the owner excluded person-run testing. Constructed checks cannot pass this gate by the issue's own wording. |
| Nomination and self-referral keep original account, source and channel | Ticked | Offline proven; live write unproven | 91 and 14 offline tests pass; live write 403 |
| Acknowledged route and named owner before review | Ticked | Offline proven; live read of owner list only | One staff owner listed; no record created |
| Challenge or correction with competing evidence, reviewer and outcome | Ticked | Offline proven; live write unproven | Route view 200 with no records |
| Correction re-reviews dependents without auto-acceptance | Ticked | Offline proven; live unproven | Needs a live write |
| Hazard concerns go to #85, not this queue | Ticked | Stated route text read live; hazard referral not exercised live | Offline `test_hazard_referral` passes |
| Non-response and support needs never lower priority; unknown never none | Ticked | Offline proven; partly read live | Null `hazard_concern` refused, not defaulted; ranking effect not exercised live |
| Tests cover wrong identity, limited authority, manual route | Ticked | Proven offline | Test files above |
| Nothing sent, booked or approved automatically | Ticked | Observed live | No write succeeded; no outbound action |

## Production-only or out of demo scope

* Real representative authority (OD-41, OD-42) and actual representative comprehension evidence: need authorized people and an owner decision.
* Whether a staffed acknowledgement was actually delivered: needs live operational records, not constructed ones.
* Appointed policy owner for identity and eligibility review (`resident_decisions.py` names it "not yet appointed").
* Azure SQL coverage for nomination-specific challenge and explanation and whole-graph dependent-decision acceptance: engineering gaps named on the issue, outside this evidence-only task.

## Evidence limits

* The 2026-11-17 reports of HTTP 400 "Could not read that." on form-encoded browser submissions were not retested.
* Independent exact-head review and hosted CI remain outstanding.

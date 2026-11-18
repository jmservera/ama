---
title: Fourth live audit of the nomination, self-referral, acknowledgement and challenge route (issue 130)
description: Recorded 2026-11-18 run against the synthetic demo that re-checks the deployed image, the live write refusal and the form-encoded 400, with a per-criterion proven or unproven table and production-only items separated
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - representative authority
  - live demo
estimated_reading_time: 5
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18: live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This run repeats the [first](./issue-130-live-nomination-route-evidence-2026-11-18.md), [second](./issue-130-live-r2-nomination-route-evidence-2026-11-18.md) and [third](./issue-130-live-r3-nomination-route-audit-2026-11-18.md) runs. No source file changed, no Azure resource was created or changed, nothing needs deleting and no issue box is ticked.

## Method

* The issue has one unticked criterion: representative participation and comprehension need authorized human evidence. Every other box is ticked.
* Azure CLI, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api`. The latest revision is now `ca-cutover-test-demo-api--0000032` (run 3 saw `--0000031`); the image digest is the same `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`, so no code fix was deployed. Origin main has no new change to the nomination or identity code since run 3 (the recent commits are documentation).
* Playwright Chromium at 1366 by 900, signed in as the employee demo account. Credentials were read at run time and never printed; a literal scan of the evidence directory for each value in the three credential files found no match (observed; raw output not retained), and e-mail addresses are scrubbed.
* Case: synthetic `ZF-2025-0331`. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-130-live-r4/`: `common.py`, `probe1.py` with `probe1.json` and `probe1.out.txt`, `probe2.py` with `probe2.json` and `probe2.out.txt`, `image-digest.txt`, `offline-tests.txt` and `route-view.png`. The Resident tab screenshot was deleted because it showed resident and staff names.
* Writes attempted: the five from run 3 plus one form-encoded POST. None succeeded; 0 nomination records existed before and after and stage and days in stage were unchanged.

## Live results

| Probe | Result |
| --- | --- |
| `GET /api/cases/ZF-2025-0331` permissions | 200; view, write, digital and staff-recorded non-digital submission true; 1 staff owner; `representative_authorities` empty; 7 channels, 5 assisted, 6 challenge |
| Valid staff-recorded phone referral, owner not staff, role name as owner, `hazard_concern` null | All 403 "Reload your current staff identity before recording this step." |
| Referral with `representative_ref` and `raised_by` | 400 "Supply only permitted route fields", naming both fields |
| Same referral sent form-encoded | 400 "Could not read that." |
| `?view=nomination-routes-html` | 200; urgent hazards use the hazard route and are never queued here; a named person owns every review and response; no referrals and no challenges recorded |
| Workbench Resident tab at 1366 wide | The three panels (Representative authority, Nominations and self-referrals, Challenge a suggestion or ask for a correction) each render once; the representative selector has 0 options because no authority is confirmed |

## Form-encoded 400 explained

The 2026-11-17 reports of "Could not read that." on form submissions are reproduced for a raw form-encoded POST. `do_POST` in `src/api/src/zava_forward/api/server.py` accepts a JSON object body only, and the workbench scripts (`app.js`, `nomination-routes.js`, `role-screens.js`) send `Content-Type: application/json`. The 400 therefore comes from the content type of the probe, not from the screen. This closes that evidence limit from run 3 for the browser UI path as far as source reading goes; no UI-driven live write was possible because of the 403.

## Offline results

* `src/core`: `test_nomination_route`, `test_nomination_bootstrap`, `test_hazard_referral`: 66 tests, OK, 1 skipped.
* `src/api`: `test_nomination_api_routes`, `test_representative_expiry_api`: 9 tests, OK; `test_nomination_screen`: 8 tests, OK.

## Cause of the write refusal

Unchanged: `resident_decisions._operation` refuses a write when the resolved actor differs from the roster person for the signed-in e-mail. Changing it alters a security identity control in `src/core`, needs a redeploy and the FULL tier, and is outside this evidence-only task.

## Per-criterion result

| Criterion in #130 | Issue state | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| Representative participation and comprehension need authorized human evidence | Unticked | Unproven; cannot be proven for the demo | Needs real representatives and residents. The demo has no confirmed representative authority (empty list) and the owner excluded person-run testing. The issue says constructed UI checks alone cannot pass this gate. |
| Nomination and self-referral keep original account, source and channel | Ticked | Offline proven; live write unproven | 66 core tests pass; live write 403 |
| Acknowledged route and named owner before review | Ticked | Offline proven; live read of owner list only | One staff owner listed; no record created |
| Challenge or correction with competing evidence, reviewer and outcome | Ticked | Offline proven; live write unproven | Route view 200 with no records |
| Correction re-reviews only dependents without auto-acceptance | Ticked | Offline proven; live unproven | Needs a live write |
| Hazard concerns go to #85, not this queue | Ticked | Route text read live; hazard referral not exercised | `test_hazard_referral` passes offline |
| Non-response and support needs never lower priority; unknown never none | Ticked | Offline proven; partly read live | Null `hazard_concern` refused, not defaulted; ranking effect not exercised live |
| Tests cover wrong identity, limited authority and manual route | Ticked | Proven offline | `test_nomination_api_routes`, `test_representative_expiry_api` |
| Nothing is sent, booked or approved automatically | Ticked | Observed live | No write succeeded; no outbound action |
| Challenge and correction criteria on constructed UI checks (RAI list) | Ticked | Read live only | Panels render with the no-sanction and no-consent wording |

## Production-only or out of demo scope

* Real representative authority (OD-41, OD-42) and representative comprehension evidence: need authorized people and an owner decision.
* Whether a staffed acknowledgement was delivered: needs live operational records, not constructed ones.
* An appointed policy owner for identity and eligibility review.
* Azure SQL coverage for nomination-specific challenge and explanation and whole-graph dependent-decision acceptance: engineering gaps named on the issue, outside this task.

## Evidence limits

* The empty-selector result is a locator count and would also hold if the selector were absent.
* The resident app `ca-resident-demo` was not probed; earlier notes found no challenge route there.
* Independent exact-head review and hosted CI remain outstanding.

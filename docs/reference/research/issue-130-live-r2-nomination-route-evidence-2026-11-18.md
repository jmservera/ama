---
title: Live demo recheck of the nomination, self-referral, acknowledgement and challenge route (issue 130, run 2)
description: Second 2026-11-18 run against the synthetic demo with raw output retained, showing the live write defect persists, and a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - live demo
estimated_reading_time: 4
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed). This run repeats and extends the [first run](./issue-130-live-nomination-route-evidence-2026-11-18.md).

## Method

* Target `ca-cutover-test-demo-api`, revision `0000031`, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb` (read with Azure CLI; retained in `image-digest.txt`). Identical to the first run, so no fix has been deployed.
* Playwright Chromium at 1366 by 900 with the employee demo sign-in. Credentials were read at run time, never printed; a literal scan of the evidence directory for each credential value found no match. Email addresses are scrubbed.
* Case: synthetic `ZF-2025-0331`. Evidence under `.copilot-tracking/evidence/2026-11-18/issue-130-live-r2/`: `probe1.py`, raw `probe1.out.txt`, `probe1.json`, `route-view.png`, `image-digest.txt`, `offline-core-tests.txt`, `offline-api-tests.txt`.
* Cleanup: 0 nomination records before and after, stage and days in stage unchanged, no Azure resource created or changed, nothing to delete. No source changed.

## Results

| Probe | Result (retained raw output) |
| --- | --- |
| Case read with permissions | 200; `can_view`, `can_write`, digital and staff-recorded non-digital all true; 1 staff owner; `representative_authorities` empty; 7 channels, 5 assisted channels, 6 challenge channels |
| Valid staff-recorded phone referral; owner not staff; role name as owner; `hazard_concern` null | All 403 "Reload your current staff identity before recording this step." |
| Referral carrying `representative_ref` and `raised_by` | 400 "Supply only permitted route fields", naming both fields |
| Route view HTML | 200; text "Urgent hazards use the hazard reporting route immediately and are never queued here. A named person owns every review and response."; no referrals and no challenges recorded |
| Offline tests | 19 core (`test_nomination_route`, `test_nomination_bootstrap`) and 9 api (`test_nomination_api_routes`, `test_representative_expiry_api`) OK; summary lines retained, full per-test output not retained |

## Cause and why it is not fixed here

The 403 comes from `resident_decisions._operation` (`src/core/src/zava_forward/core/resident_decisions.py`, line 1112), which refuses a write when the resolved actor differs from the roster person for the signed-in email. Changing it alters a security identity control in `src/core`, needs a redeploy and the FULL validation tier, so this evidence-only task stops and reports it.

## Per-criterion result

| Criterion in #130 | Demo result | Evidence and limit |
| --- | --- | --- |
| Representative participation and comprehension need authorized human evidence (UNTICKED) | Unproven; cannot be proven for the demo | Needs real representatives and residents; the demo has no confirmed representative authority and the owner excluded person-run testing. Do not tick. |
| Original account, source and channel kept | Unproven live; offline tests pass | Live write 403 |
| Acknowledged route and named owner before review | Read live; write unproven | One staff owner listed; no record created |
| Challenge or correction with evidence, reviewer, outcome | Read live; write unproven | Route view 200; write blocked |
| Correction re-reviews dependents only | Unproven live; offline tests pass | Needs a write |
| Hazard concerns go to #85, not this queue | Read live (stated route text) | No live hazard referral exercised |
| Non-response and support needs never lower priority; unknown never none | Partly read live | Null `hazard_concern` is refused, not defaulted; ranking effect not exercised |
| Tests cover wrong identity, limited authority, manual route | Offline pass | 9 api tests |
| Nothing sent, booked or approved automatically | Observed live | No write succeeded; panel text |

## Evidence limits

* All live results are from this run's retained `probe1.out.txt`; the first run's screenshots of the Resident tab panels are not repeated here.
* 2026-11-17 reports of HTTP 400 "Could not read that." on form-encoded browser submissions are not retested.
* The resident app `ca-resident-demo` was not exercised.
* Independent exact-head review and hosted CI remain outstanding; no criterion is ticked.

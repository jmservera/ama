---
title: Fifth live audit of the nomination, self-referral, acknowledgement and challenge route (issue 130)
description: Recorded 2026-11-18 re-check of the synthetic demo showing the same image, the same live write refusal and the same form-encoded 400, with a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - representative authority
  - live demo
estimated_reading_time: 4
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18: live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This run repeats the [fourth audit](./issue-130-live-r4-nomination-route-audit-2026-11-18.md) and adds a check of the resident app. Nothing was deployed or changed.

## Method

* The issue has one unticked criterion: representative participation and comprehension need authorized human evidence.
* Azure CLI, read-only. `ca-cutover-test-demo-api` is still on revision `--0000032` (Healthy, created 2026-11-18T16:20:23Z) with the same image digest `sha256:5368f4e4...e5fb` as runs 3 and 4. `ca-resident-demo` is on `--0000013`. Origin main moved only by documentation commits (one new commit, a #146 evidence note); no `src/` file differs from this branch.
* Playwright Chromium at 1366 by 900 signed in as the employee demo account. Credentials were read at run time and never printed; e-mail addresses are scrubbed from the retained output.
* Case: synthetic `ZF-2025-0331`. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-130-live-r5/`: `common.py`, `probe1.py` with `probe1.json` and `probe1.out.txt`, `probe2.py` with `probe2.json` and `probe2.out.txt`, `image-digest.txt`, `resident-routes.txt`, `offline-tests.txt` and `route-view.png` (the route view, with no names). The Resident tab screenshot was deleted because it shows resident and staff names.
* Writes attempted: the five from run 4 plus one form-encoded POST. None succeeded; 0 nomination records existed before and after, and stage and days in stage were unchanged.

## Live results

| Probe | Result |
| --- | --- |
| `GET /api/cases/ZF-2025-0331` permissions | 200; view, write, digital and staff-recorded non-digital submission true; 1 staff owner; `representative_authorities` empty; 7 channels, 5 assisted, 6 challenge |
| Valid staff-recorded phone referral, owner not staff, role name as owner, `hazard_concern` null | All 403 "Reload your current staff identity before recording this step." |
| Referral with `representative_ref` and `raised_by` | 400 naming both fields as not accepted |
| Same referral form-encoded | 400 "Could not read that." (the API accepts JSON bodies only; the workbench sends JSON) |
| `?view=nomination-routes-html` | 200; hazards use the hazard route and are never queued here; a named person owns every review; no referrals or challenges recorded |
| Workbench Resident tab | Representative authority, Nominations and self-referrals, and Challenge panels each render once; the representative selector has 0 options |
| Resident app `ca-resident-demo` | `/` 200; `/api/me`, `/challenge`, `/api/challenge`, `/nomination` all 404, so no nomination or challenge route is discoverable there |

## Offline results

* `src/core`: `test_nomination_route`, `test_nomination_bootstrap`, `test_hazard_referral`: 66 tests, OK, 1 skipped.
* `src/api`: `test_nomination_api_routes`, `test_representative_expiry_api`, `test_nomination_screen`: 17 tests, OK.

## Cause of the write refusal

Unchanged from run 4: `resident_decisions._operation` refuses a write when the resolved actor differs from the roster person for the signed-in e-mail. Changing it alters a security identity control in `src/core`, needs a redeploy and the FULL tier, and is outside this evidence-only task.

## Per-criterion result

| Criterion in #130 | Issue state | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| Representative participation and comprehension need authorized human evidence | Unticked | Unproven; cannot be proven for the demo | Needs real representatives and residents. The demo has no confirmed representative authority and the owner excluded person-run testing. The issue states that constructed UI checks alone cannot pass this gate. |
| Nomination and self-referral keep original account, source and channel | Ticked | Offline proven; live write unproven | 66 core tests; live write 403 |
| Acknowledged route and named owner before review | Ticked | Offline proven; live owner list read only | One staff owner listed; no record created |
| Challenge or correction with competing evidence, reviewer and outcome | Ticked | Offline proven; live write unproven | Route view 200 with no records |
| Correction re-reviews only dependents, no auto-acceptance | Ticked | Offline proven; live unproven | Needs a live write |
| Hazard concerns go to #85, not this queue | Ticked | Route text read live; hazard referral not exercised live | `test_hazard_referral` passes offline |
| Non-response and support needs never lower priority; unknown never none | Ticked | Offline proven; null `hazard_concern` refused live, not defaulted | Ranking effect not exercised live |
| Tests cover wrong identity, limited authority, manual route | Ticked | Proven offline | `test_nomination_api_routes`, `test_representative_expiry_api` |
| Nothing is sent, booked or approved automatically | Ticked | Observed live | No write succeeded; no outbound action |
| Challenge, explanation and non-digital route criteria (RAI list) | Ticked | Read live only | Panels render with the no-sanction and no-consent wording |

## Production-only or out of demo scope

* Real representative authority (OD-41, OD-42) and representative comprehension evidence need authorized people and an owner decision.
* Whether a staffed acknowledgement was delivered needs live operational records, not constructed ones.
* Azure SQL coverage for nomination-specific challenge and explanation, and whole-graph dependent-decision acceptance, are engineering gaps named on the issue.

## Evidence limits

* The empty-selector result is a locator count and would also hold if the selector were absent.
* The resident app was checked by status code of five paths only, not signed in.
* Independent exact-head review and hosted CI remain outstanding.

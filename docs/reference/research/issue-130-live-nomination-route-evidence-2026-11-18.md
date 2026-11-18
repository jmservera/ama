---
title: Live demo evidence for the nomination, self-referral, acknowledgement and challenge route (issue 130)
description: Recorded 2026-11-18 run against the synthetic demo showing what the nomination route shows and enforces live, why the representative-participation criterion cannot be proven for the demo, and a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - representative authority
  - live demo
estimated_reading_time: 6
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Production-only criteria stay deferred (#1905-#1908). Nothing here is resident, production or legal evidence.

Issue #130 has one unticked criterion: "Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate." Every other criterion is already ticked. This note answers the unticked one and records what the live demo shows for the ticked ones.

## Method

* Target: `ca-cutover-test-demo-api` (image digest `sha256:5368f4e4...e17e5fb`, unchanged), Entra sign-in with the employee demo account, Playwright Chromium at 1366 by 900. Credentials were read at run time and never printed; a literal scan of every evidence file for each credential value found no match.
* Case: synthetic `ZF-2025-0331`. Scripts, JSON outputs and screenshots are under `.copilot-tracking/evidence/2026-11-18/issue-130-live/` (`probe1.py`, `probe1.json`, `ui1.py`, `ui1.json`, `ui2.py`, `ui2.json`, `route-view.png`, `resident-tab.png`, `nomination-panel.png`, `representative-panel.png`, `challenge-panel.png`).
* Offline: `src/core/tests` `test_nomination_route` and `test_nomination_bootstrap` (19 tests) and `src/api/tests` `test_nomination_api_routes` and `test_representative_expiry_api` (9 tests), all OK.
* No Azure resource was created or changed, so there is nothing to delete. No source changed.

## Observations

| Observation | Result |
| --- | --- |
| `GET /api/cases/ZF-2025-0331` permissions for the Programme Manager demo account | `can_view`, `can_write`, digital and staff-recorded non-digital submission all true; 7 intake channels, 5 assisted media, 1 selectable staff owner; `representative_authorities` is an empty list; 0 nomination records |
| Route view `?view=nomination-routes-html` | 200, accessible-structure fragment: "Urgent hazards use the hazard reporting route immediately and are never queued here. A named person owns every review and response." Both sections report nothing recorded. |
| Workbench Resident tab (`/app#/case/ZF-2025-0331`) | Panels "Representative authority", "Nominations and self-referrals" and "Challenge a suggestion or ask for a correction" render. Text: "Nothing is sent here", "A person confirms authority with the resident. Scheduling or interpreting is not authority for works consent", "A challenge never means consent, refusal or a sanction." |
| Representative selector | No confirmed-representative option exists (`select[name=representative_ref]` has no options) because the case holds no confirmed representative authority. The UI offers a representative only when authority is already confirmed. |
| Write with `representative_ref` or `raised_by` on a new referral | 400 "Supply only permitted route fields", so a representative cannot be asserted on a new referral |
| Valid staff-recorded phone referral, wrong owner identity, role name as owner, `hazard_concern` null | 403 "Reload your current staff identity before recording this step." for every variant |
| Case stage and days in stage after the refused writes | Unchanged; 0 nomination records |

## Blocking defect for live writes

All writes were refused with the same 403, including those that should have returned a specific validation message, so the live demo cannot distinguish wrong identity, limited authority or valid input by response text. This is the Entra principal versus roster comparison in `resident_decisions._operation` already reported with an offline reproduction in `issue-220-live-challenge-route-evidence-2026-11-18.md`. Re-checking on 2026-11-18 shows the deployed image is unchanged and the defect persists on the nomination route. Fixing it changes `src/core`, needs the full validation tier and a redeploy, which is outside this evidence-only task.

## Per-criterion result

| Criterion in #130 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate (UNTICKED) | Cannot be proven for the demo, by design | The gate requires actual representatives and residents taking part and showing comprehension. The demo holds only synthetic data, no confirmed representative authority (empty list), and no person-run testing, which the owner has excluded. Constructed UI checks above show the gate is not bypassable by the screen: no representative option without confirmed authority, representative fields refused on new referrals. They do not pass it. Stays open; the human evidence is production and participation work (#1905-#1908 scope for sign-off). Do not tick. |
| Nomination and self-referral keep the original account, source and channel (ticked) | Offline only | 19 core tests pass. Live write refused by the identity defect. |
| Acknowledged route and named owner before review (ticked) | Read live, write offline | Live permissions list a named staff owner and the panel states a named person owns every response. No live record could be created. |
| Challenge or correction with competing evidence, reviewer and outcome (ticked) | Read live, write offline | Challenge panel renders with its explanation that a person owns the response and that a recorded correction stales only suggestions and reviews that used that version; write blocked live. |
| Correction re-reviews only dependent decisions (ticked) | Offline only | Needs a correction write; blocked live. |
| Emergency or hazard concerns route to hazard intake (#85) (ticked) | Read live | Route view and panel both state urgent hazards use the hazard route immediately. A live hazard referral could not be exercised. |
| Non-response and support needs never lower priority; unknown never none (ticked) | Read live, partly | Panel guarantees state no lowered priority and no inferred refusal; per-measure answers show "Not recorded", not "none". A `hazard_concern` of null stays unwritable (refused), not defaulted. |
| Tests cover wrong identity, limited authority and manual route (ticked) | Offline only | `test_nomination_api_routes` and `test_representative_expiry_api` pass. |
| Nothing is sent, booked or approved automatically (ticked) | Read live | Panels state "Nothing is sent here"; no write succeeded. |

## What this does not prove

* Any live write, because of the identity defect.
* Representative or resident comprehension, participation or authority for a real person.
* The resident app `ca-resident-demo` was not exercised; the #220 note found it offers no challenge route.

## Remaining work

* Obtain authorized representative and resident participation evidence before the unticked criterion can be ticked.
* Fix the Entra identity comparison (full tier, owner-approved redeploy) and repeat `probe1.py` to prove live writes.

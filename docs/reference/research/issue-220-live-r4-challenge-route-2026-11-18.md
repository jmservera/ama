---
title: Live demo re-verification of the challenge and correction route, fourth run (issue 220)
description: Repeat of the 2026-11-18 live probe on revision 0000032 with a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
---

Refs #220. Scope: synthetic desktop demo under the owner decisions of 2026-11-18. Builds on the [earlier note](./issue-220-live-challenge-route-evidence-2026-11-18.md). Nothing here is resident, production or legal evidence.

## Method and results

* Target `ca-cutover-test-demo-api`, revision `--0000032` (created 2026-11-18T16:20Z), image digest `sha256:5368f4e4...e17e5fb`, unchanged from the earlier runs. Raw files are under `.copilot-tracking/evidence/2026-11-18/issue-220-live-r4/`: `run1.py`, `common.py`, `run1.out.txt`, `live-revision.txt`.
* Playwright sign-in as the employee demo account; credentials read at run time and never printed. A literal scan of the evidence folder for each credential value found no match.
* Staff-recorded phone route write on `ZF-2025-0331`: 403 "Reload your current staff identity before recording this step." Same with `hazard_concern` true. No nomination record was created.
* Forbidden fields `retaliation_flag`, `refusal`, `hazard_pause`, `priority_penalty`: 400 each, "Supply only permitted route fields", before any write. Missing `hazard_concern`: 400.
* Protected state (stage, days in stage, closed, resident, hazards, measure decisions) hashed before and after: identical. The hazard stays "Repair evidenced, hold active".
* Offline: 11 core tests (`test_no_retaliation_guard_220`, `test_challenge_no_retaliation_220`, `test_issue_220_challenge_route`) and 10 api tests (`test_challenge_non_retaliation_hazard_guard`, `test_challenge_no_retaliation_api_220`) pass. Outputs: `offline-core-tests.txt`, `offline-api-tests.txt`.
* Source line `resident_decisions.py:1112` still compares the whole principal with the roster row; origin/main holds no fix. No Azure resource was created, so nothing needed deleting.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work (ticked) | Offline only | Live write refused by the 403 |
| Explanations, owner, next update, resolution visible (ticked) | Offline only | No live challenge exists to display |
| Only dependent proposals and reviews stale (ticked) | Offline only | Needs a live correction write |
| No inferred consent, refusal, sanction, closure or hazard-clock change (ticked) | Partly live | Forbidden fields refused, state unchanged; positive write blocked |
| No retaliation, inferred refusal or delayed hazard response (unticked) | Unproven live; proven offline | The server check on a successful write was not observed live |

## Why the open criterion cannot be proven for the demo

A successful live write needs a fix to the identity comparison in `src/core`. That is a source change needing the FULL validation tier and a demo image redeploy; neither is authorised, so none was attempted. A real resident's experience of retaliation over time is a production matter and outside the demo.

## Evidence limits

* Output files were not edited. The probe repeats the earlier `run1.py` unchanged.
* The criterion stays unticked.

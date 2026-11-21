---
title: Issue 220 eighth live run, oid-less roster row refusal (2026-11-21)
description: Live probe of the challenge route on revision 0000040, the root cause of the persisting 403 and the local fix
author: AMA RPI agent
ms.date: 2026-11-21
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Method and results

* Target `ca-cutover-test-demo-api`, revision `--0000040` (created 2026-11-21T12:51Z), image digest `sha256:2efbf683...ecea4b4` (main 78ecac16af). Raw files are in `.copilot-tracking/evidence/2026-11-21/issue-220-live-r8/`: `run1.py`, `run1.out.txt`, `diag.py`, `live-revision.txt`. Playwright sign-in; credentials read at run time and never printed.
* The staff-recorded `nomination_record` write is still refused 403 "Reload your current staff identity before recording this step.", with `hazard_concern` true or false. No record was created. The earlier fix for the whole-principal comparison is in this image, so it was not the full cause.
* Forbidden fields `retaliation_flag`, `refusal`, `hazard_pause`, `priority_penalty` give 400 before any write; a missing `hazard_concern` gives 400. Hashes of stage, days in stage, closed, resident, hazards and measure decisions are identical before and after; the hazard hold stays active.
* Diagnosis: the signed-in principal carries code, email, oid and tid; the demo roster rows carry the derived code and email and expose no oid. With no oid on the row, `identity.matches` finds no bound row, and `_same_signed_in_person` then compares the actor oid with an empty roster oid and refuses. Reproduced offline on the JSON store.
* Fix (local commit, not deployed): code and email must match; oid must match only when the roster row records one (`resident_decisions._same_signed_in_person`, also used by `_owner_rights`). New test `test_roster_row_without_oid_still_admits_the_matching_principal` fails before and passes after. 491 core tests in the related modules pass (162 skipped for missing SQL/browser prerequisites). `mypy` reports 3 errors in `telemetry.py` and `device_provision.py`, unchanged by this work.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work (ticked) | Offline proven; live blocked by the 403 until the fix is deployed | Test above; live probe |
| Explanations, owner, next update, resolution visible (ticked) | Offline proven; no live challenge exists to display | Core tests |
| Only dependent proposals and reviews stale (ticked) | Offline proven | Core tests |
| No inferred consent, refusal, sanction, closure or hazard-clock change (ticked) | Offline proven; live partly: forbidden fields refused and state unchanged | Probe hashes |
| No retaliation, inferred refusal or delayed hazard response (unticked) | Offline proven (guard tests and new regression). Live success path unproven: needs a rebuild and redeploy, not authorised. Retaliation over time and real hazard-response delay are production-only. Stays unticked | Tests; revision check |

No Azure change was made and no resource was created.

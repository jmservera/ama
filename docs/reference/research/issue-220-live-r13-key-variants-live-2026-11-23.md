---
title: Issue 220 thirteenth run, live check of adverse-key variants on revision 0000058 (2026-11-23)
description: Live probe showing the demo API rejects case, spacing and hyphen variants of forbidden challenge fields, with a per-criterion proven and unproven table
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Method and results

* Live state on 2026-11-23: `ca-cutover-test-demo-api` active revision `--0000058` (created 2026-11-23T19:20Z, 100% traffic). The [twelfth-run](./issue-220-live-r12-key-normalisation-2026-11-23.md) guard change was committed after that revision was built, so 0000058 does not contain it. Raw files: `.copilot-tracking/evidence/2026-11-23/issue-220-live-r13/` (`run1.py`, `run1.json`, `run1.out.txt`, `live-revision.txt`). Playwright sign-in; credentials read at run time and never printed; output has 0 `@` characters.
* Case `ZF-2025-0331` (synthetic), action `nomination_record`, staff-recorded route. Each of `Retaliation_Flag`, ` refusal`, `hazard-pause`, `HAZARD_PAUSE` and `priority penalty` set to true returns HTTP 400 "Supply only permitted route fields". Nomination records stay at 11 and the protected hashes (stage, days in stage, closed, resident, hazards, measure decisions, resident reviews and scopes) are equal before and after.
* Reading: the live route already rejects every variant through its permitted-field list, so the r12 key-matching weakness in `challenges.py` was a second-line (defence in depth) gap and was not reachable through this route on 0000058. Deploying the r12 guard is therefore not required to close the live criterion; it remains an owner-gated image roll.
* No source change was needed this run, so the tier is focused (no `src` edit). No Azure resource was created or changed; no constructed record was added.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven live (earlier [r11](./issue-220-live-r11-revision-0054-2026-11-23.md)); not re-run on 0000058 | Earlier probe |
| Explanations, owner, next update, resolution visible | Proven live for owner, next update, route; resolution by offline tests | r11; tests |
| Only dependent proposals and reviews stale | Proven offline | Tests |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live on 0000054; on 0000058 adverse inputs leave protected hashes unchanged | r11; this run |
| No retaliation, inferred refusal or delayed hazard response | Proven for the constructed case and for key variants on 0000058. Retaliation over time and real hazard-response timing need production history and cannot be shown in the synthetic demo, so the checkbox stays unticked | This run; r11; tests |

Owner-gated: ticking the final issue checkbox and deploying the r12 guard image. Not needed for the demo: billing, DPO or Legal approval, person-run assistive-technology testing.

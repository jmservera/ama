---
title: Epic 81 audit round 3, child features all closed or deferred (Refs #81)
description: Per-criterion proven/unproven table for epic 81 on 2026-11-20; criterion 2 is now proven for the demo, criterion 1 stays unproven
ms.date: 2026-11-20
---

Refs #81. Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, no production change). No Azure resource was created, so nothing needed deleting. No source changed, FOCUSED tier. This note ticks nothing; the owner ticks the epic.

## What changed since round 2

The [round 2 audit](./issue-81-epic-audit-live-r2-2026-11-19.md) found #130 OPEN with no recorded deferral. #130 was closed on 2026-11-19T14:17Z (COMPLETED) with the comment "Closed: criteria moved to #2117". Issue #2117 is OPEN with label `delivery:deferred` and holds the one production-only criterion (authorised real representative participation and comprehension evidence).

## Evidence

Read with `gh` on 2026-11-20:

| Child | State | Disposition |
| --- | --- | --- |
| #82 | CLOSED | Delivered |
| #83 | CLOSED | Delivered |
| #84 | CLOSED | Delivered |
| #85 | CLOSED | Delivered |
| #86 | CLOSED | Delivered |
| #87 | CLOSED | Delivered |
| #88 | CLOSED | Delivered |
| #130 | CLOSED | Seven code criteria ticked; the remaining production-only criterion deferred to #2117 |
| #131 | CLOSED | Delivered |

Also read: #440 OPEN with two unticked criteria (owner-approved triage into issues; PR artifacts); #1837 OPEN. Revision `0000033` of `ca-cutover-test-demo-api` is unchanged since round 2, so the deployed image still predates the form fix; no redeploy was attempted.

## Epic 81 acceptance criteria

| # | Criterion | Proven for the demo? | Evidence and reason |
| --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Unproven | #440 is OPEN with two unticked criteria and the criterion says merged children alone do not satisfy it. The deployed image predates the #1837 fix and a redeploy is a production change the owner excluded |
| 2 | All child features closed or deferred (unticked) | Proven | Every child in the table above is CLOSED and the only residual criterion has a recorded deferral to #2117 under the owner rule of 2026-11-19. Checked by `python3 tools/test_epic_81_child_disposition.py` |
| 3 | No controlled progression with unresolved safety evidence (ticked) | Not re-examined | No contradiction found |
| 4 | No work started without valid resident agreement or authorised exception (ticked) | Not re-examined | No contradiction found |

## Result

Criterion 2 is proven for the demo and can be ticked by the owner. Criterion 1 still needs #440 to complete its triage and PR artifacts, which needs the owner.

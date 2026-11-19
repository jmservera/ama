---
title: Resident and Representative UX on the Live Demo, Round 5 (Issue 154)
description: Re-audit of the unticked #154 criterion against the owner demo scope of 2026-11-18, with the live app configuration check
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope and authority

Synthetic demo, desktop only, owner decisions of 2026-11-18. One read-only Azure CLI query (`az containerapp show`, resource group `ama`, app `ca-resident-demo`) listed environment variable names and the image digest. No resource was created or changed, so nothing needed deleting. No sign-in value was read or printed.

## Finding

The only unticked criterion in the issue is the fifth: "No live resident contact; designs are validated through the usability programme before any use". It has two parts.

* No live resident contact: proven for the demo in round 3 ([note](./issue-154-live-resident-ux-r3-2026-11-18.md)). Nothing in this round changes that.
* Validation through the usability programme: the programme ([plan](./ux/usability-test-programme-plan.md)) needs moderated sessions with residents, and the owner has decided person-run testing is not needed for the demo. The clause gates "any use" with real residents, which the demo does not have. No code can satisfy it.

The ticked third criterion (representative views task-limited and expiring) is proven over local HTTP in round 4 ([note](./issue-154-live-resident-ux-r4-2026-11-18.md)). The live app (revision `ca-resident-demo--0000014`, image digest `sha256:65481780...bbd19`) has no `ZF_DEMO_REP_GRANTS_PATH` variable, so the round 4 loader is not configured live. Showing it live needs an image rebuild, a mounted grants file and a revision change. That is a deployment action for the coordinator, not a code gap; the loader is already on main (`src/api/src/zava_forward/api/resident_demo/rep_grants.py`).

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| 1 Journeys cover choice, pause or withdrawal, appointments, commitments, handover, complaint | Proven earlier | Round 2 live captures; not re-run |
| 2 Non-digital alternative, language, literacy, adjustments | Proven earlier | Round 2; not re-run |
| 3 Representative view task-limited and expiring | Proven locally, not live | Round 4 HTTP test; live app lacks the grants variable, so live proof waits on a coordinator deploy |
| 4 Offers distinct from confirmed commitments | Proven earlier | Round 2; not re-run |
| 5a No live resident contact | Proven for the demo | Round 3 |
| 5b Validated through the usability programme | Unproven; out of demo scope | Needs moderated resident sessions the owner excluded |

## Outcome

No demo-scope criterion is unmet by a code gap. No source change was made, so the validation tier is FOCUSED (documentation only).

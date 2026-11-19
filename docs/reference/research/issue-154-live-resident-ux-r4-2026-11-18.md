---
title: Resident and Representative UX on the Live Demo, Round 4 (Issue 154)
description: Code gap that blocked a representative view on the deployed demo, the fix and the per-criterion status of #154
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Synthetic demo, desktop only, owner decisions of 2026-11-18. No Azure resource was created or changed in this round, so nothing needed deleting, and no sign-in value was read. Round 3 ([note](./issue-154-live-resident-ux-r3-2026-11-18.md)) proved criterion 5a and left criterion 3 unproven live.

## Finding

The deployable entrypoint `resident_demo/__main__.py` never passed representative grants to `ResidentDemo`, and the SQL reader has no grant loader. The representative view was reachable only from unit tests, so no deployed demo could show it. Fix: an optional `ZF_DEMO_REP_GRANTS_PATH` file of synthetic task-limited grants, loaded fail-closed by `resident_demo/rep_grants.py` (expiry mandatory and capped at the authority end, unknown fields rejected, no secret held). Evidence: [rep-grants-tests-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r4/rep-grants-tests-raw.txt); 57 tests across `test_rep_grants`, `test_representative_expiry_api` and `test_resident_demo_api` pass, mypy and ruff are clean.

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| 1 Journeys cover choice, pause or withdrawal, appointments, commitments, handover, complaint | Proven earlier | Round 2 live captures; not re-run |
| 2 Non-digital alternative, language, literacy, adjustments | Proven earlier | Round 2; not re-run |
| 3 Representative view task-limited and expiring | Proven locally over HTTP, unproven live | The new HTTP test loads a grants file, signs in as the representative, sees only the granted measure and, after the clock passes expiry, no active view. Live proof needs the coordinator to deploy the image and supply a grants file with a case in the allowlist view |
| 4 Offers distinct from confirmed commitments | Proven earlier | Round 2; not re-run |
| 5a No live resident contact | Proven for the demo | Round 3 network trace and Azure check; the new file loader adds no outbound path |
| 5b Validated through the usability programme | Unproven; not demo scope | Needs moderated sessions the owner has not requested |

## Limits

Local loopback tests, one date. The deployed image is unchanged until the coordinator publishes and redeploys.

---
title: Entra roles and field-level visibility, demo evidence round 4 (#116)
description: Demo confirmation of the vulnerability-reason role set, a fail-closed fix and a per-criterion proven or unproven table
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only. Retrieval and test date 2026-11-19. Owner decision of 2026-11-18: DPO and Legal approval is not needed for the demo, and live Azure use is authorised within resource group `ama`.

## What changed

The round-3 note left criterion 1 unproven because it read "confirmed" as a named DPO or Legal approval. For the demo the owner's direction (2026-10-08, recorded in [gap-analysis-next-build.md](./gap-analysis-next-build.md)) and the 2026-11-18 decision confirm the set: Resident Liaison Officer, Building Safety Liaison and Retrofit Programme Manager see the reason; every other staff role sees a held marker; the contractor never sees it.

A probe found a defect against that confirmation. A `ZF_REASON_ROLES` override naming `Contractor` made `can_see_reason` true for the contractor. `projection.reason_roles()` now drops `Contractor` from any override. The new test `test_reason_role_override_never_grants_the_contractor` in `src/api/tests/test_role_matrix.py` pins the three confirmed roles, the override behaviour and the empty value.

## Evidence

| Check | Result |
| --- | --- |
| Probe before the fix (`reason_roles()` with `Contractor` set) | `('Contractor',)`, `can_see_reason` True |
| `python3 -m unittest test_role_matrix test_role_endpoint_inventory -q` from `src/api` (41 tests, includes every role against every endpoint) | OK |
| `python3 -m mypy` in `src/core` | 22 errors, the same count as the unmodified tree (missing `opentelemetry` stubs); none in `projection.py` |
| `ruff format --isolated --line-length 100 --check projection.py` | Reports reformatting needed on the unmodified file too; not caused by this change |

No live Azure call was made this round. Live evidence for the reason role is in [round 3](./issue-116-live-r3-evidence-2026-11-18.md).

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Proven for the demo | Owner decision 2026-11-18 confirms the set; role matrix tests (41 OK) and the new override test enforce it. Production still needs DPO, Legal and control-owner approval |
| 2 | Allowlists and size limits at every provider boundary | Unproven | Offline provider-spy evidence exists (round 3); live payloads are not exposed; no new work this round |
| 3 | Permissions rechecked on outputs, citations, explanations, errors, review records and exports | Unproven | Partial live evidence for one role only (round 3); other roles are not signed in live |
| 4 | Document AI requires derivative or scoped necessity exception | Unproven live | Uploading changes demo state; offline document controls pass in round 3 |

No acceptance box is ticked. The source change is in `src/core`, so the FULL validation tier applies; the complete gate was not run (heavy lock held, owner instruction). Independent review and hosted CI remain outstanding.

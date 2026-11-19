---
title: Issue 116 live round 4 research
ms.date: 2026-11-19
---

## Scope

Issue #116, demo only, desktop, synthetic data. Fourth round. First unmet criterion: "Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19)".

## Opening findings

* Rounds 1 to 3 left the box unproven because "confirmed" was read as a named DPO/Legal approval. The owner decision of 2026-11-18 removes that approval for the demo.
* Default reason roles: Resident Liaison Officer, Building Safety Liaison, Retrofit Programme Manager (`projection.DEFAULT_REASON_ROLES`).
* Planning Readiness: Ready. Research disposition: executed.

## Probe result (offline, `/tmp/probe116.py`)

| `ZF_REASON_ROLES` | `reason_roles()` | `can_see_reason(Contractor)` |
| --- | --- | --- |
| unset | the three default roles | False |
| `Contractor` | `('Contractor',)` | True |
| `Contractor,Retrofit Programme Manager` | both | True |
| empty | none | False |

Gap: a configuration value can give the contractor the vulnerability reason, which contradicts PR-002 and OD-14 ("never the reason"). Existing test `test_reason_roles_can_be_configured` only checks a staff role. The code path is `projection.reason_roles()` in `src/core/src/zava_forward/core/projection.py`.

## Other criteria

Criteria 2 to 4 are production-boundary or live-only items; earlier rounds recorded their offline and live evidence (`docs/reference/research/issue-116-live-r3-evidence-2026-11-18.md`). They are not re-run live in this round.

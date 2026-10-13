---
title: Zava Azure Reset and Live Acceptance Plan
description: Owner-authorised disposable ama reset, renamed redeployment and final review
ms.date: 2026-10-12
---

## Approved scope and decisions

The owner explicitly requested deletion of everything inside resource group
`ama` except necessary user-assigned identities, followed by redeployment,
issue fixes and a final names/references review. Downtime and synthetic-data
recreation are authorised. Keep the resource group, operator system identity,
tenant registrations and Microsoft 365 resources outside this destructive scope.
Continue PR #65 and the original 980-case/443-open-case fixture.

Reuse the established Bicep, provisioning scripts and migration guide.
Do not disable authentication or replace live acceptance with localhost checks.
Current Graph application-management denial remains a known dependency, not a
reason to silently claim Entra login works. Source/runtime issues discovered
during redeployment are within the requested fixes.

## Implementation

<!-- rpi:phase id=P01 -->
### P01: Reset and redeploy

* [x] P01-T01: Capture resource inventory, external auth and SQL identity mappings;
  classify identities and securely retain the existing auth secret for transfer.
* [x] P01-T02: Delete only inventoried resources inside ama in dependency order;
  verify no unapproved or required identity was removed.
* [x] P01-T03: Deploy renamed Bicep, build application image, restore SQL users/data,
  wire model access and protect the API with Entra.

<!-- rpi:phase id=P02 -->
### P02: Acceptance and review

* [x] P02-T01: Fix discovered deployment/runtime failures; verify health, real SQL
  write/read/restart, actual AI, lists, map and authentication where authorised.
* [x] P02-T02: Run one final names/reference review, record unresolved gates,
  update rebuild documentation and publish fixes/evidence through #65.

### Remaining acceptance gate

P02-T01's authorised operator/workload checks passed. Interactive Entra login,
signed-in lists and map remain blocked on the tenant owner adding the new
callback and completing registration/role naming. This is partial acceptance,
not permission to bypass authentication or a conformant migration claim.

## Dependencies and evidence

Details: [zava-azure-reset-phase-details.md](../../details/2026-10-12/zava-azure-reset-phase-details.md).
Changes: [zava-azure-reset-changes.md](../../changes/2026-10-12/zava-azure-reset-changes.md).
The owner-selected reset and existing tested deployment contract are the plan
basis. No repeated branding critique or infrastructure redesign is authorised.

---
title: Zava Azure Reset Phase Details
description: Execution boundaries and live validation evidence required
ms.date: 2026-10-12
---

## P01

Subscription: `e51ebc89-79d0-4a52-a82b-01a292eefd5b`.
Resource group: `ama`; location: `uksouth`; workload: `forward`; environment:
`test`; disposable development profile. Retain current region, model SKUs and
capacity from the observed deployment rather than inventing replacements.

The operator is the system-assigned `ama-deployer-mi` principal outside this
resource inventory. The four old user-assigned identities serve only the
recreated workload; active evidence storage is Blob and SharePoint site is empty.
Do not preserve their old names merely for internal Azure grants that Bicep/SQL
provisioning recreates. Tenant applications and their existing assignments stay
outside scope. Retain the auth credential temporarily in a mode-0600 local file,
never in tracked files, reports or output; remove after transfer to the new vault.
Capture synthetic staff object-id mappings privately, without publishing them.

Delete apps/jobs and endpoints before environment/network; delete parent
resources rather than separately racing managed child/NIC deletions. Preserve
the group and its policy-exception tag. No force-push or main merge.

## P02

Verify the changed image/version, health and unauthenticated denial, SQL seed
counts and identity mappings, managed-identity access, actual inference, restart
durability, accessible map tiles/points, displayed brand and logo. A denied
registration update blocks interactive Entra callback acceptance; it does not
justify opening the API.

Final review covers active code/docs/contracts, Azure resource names and image
references, relative links and historical exceptions, presentation delivery
copies and source consistency. Record actual outcomes and unresolved boundaries.

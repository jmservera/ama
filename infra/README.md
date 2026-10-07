---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Proper Warm demonstrator Azure architecture
author: AMA programme
ms.date: 2026-10-08
ms.topic: how-to
---

Proposed, non-production infrastructure. The design and its rationale are in
[ADR 0001](../docs/adrs/0001-azure-architecture.md).

## Layout

* `main.bicep`: resource group scope entry point wiring all modules.
* `main.bicepparam`: dev parameters; replace the placeholder alert email and Entra group.
* `modules/`: identity, network (VNet, NSGs, private DNS), monitoring (Log Analytics, App Insights, AMPLS), Key Vault, storage, registry, SQL, Foundry, Container Apps and the generic private endpoint.
* `scripts/create-sql-users.sql`: contained SQL users for the managed identities.

## Deploy

```bash
az group create -n rg-proper-warm-dev -l swedencentral
az deployment group what-if -g rg-proper-warm-dev -f infra/main.bicep -p infra/main.bicepparam
az deployment group create -g rg-proper-warm-dev -f infra/main.bicep -p infra/main.bicepparam
```

Then run the SQL script from a host with private network access, push the
application images to the registry and update the image parameters.

## Validate locally

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

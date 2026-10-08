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
* `scripts/grant-sharepoint-access.sh`: optional Graph `Sites.Selected` grant for the SharePoint evidence store.

Optional parameters: `teamsWebhookUrl`, `evidenceStore`, `sharePointSiteId`, `monthlyBudget`. See the M365 section of the ADR.

## Deploy

```bash
az group create -n rg-proper-warm-dev -l swedencentral
az deployment group what-if -g rg-proper-warm-dev -f infra/main.bicep -p infra/main.bicepparam
az deployment group create -g rg-proper-warm-dev -f infra/main.bicep -p infra/main.bicepparam
```

Then run the SQL script from a host with private network access, push the
application images to the registry and update the image parameters.

## Development access from external networks

`allowPublicNetworkAccess` (default `false`) is a development switch. When `true`, the private endpoints stay in place but the following also accept external connections:

* Storage, Key Vault, Foundry, Container Registry, Log Analytics and Application Insights: public network access enabled (network ACL default action `Allow`).
* Azure SQL: public access enabled with a firewall rule `dev-external-access` covering all addresses. Entra-only authentication still applies. In the MCAPS subscription an external policy reverts SQL `publicNetworkAccess` to `Disabled` unless the resource group carries the tag `SecurityControl=Ignore` (observed 2026-10-08), so set that tag on the resource group first.
* Container Apps environment: external (not internal) with public access enabled, so the API gets a public FQDN. The private DNS zone for the environment is not created.

The Container Registry export policy is set to `enabled` in this mode because ACR requires it when public access is on. Identity and RBAC controls are unchanged (no keys, no SQL logins). Never set it to `true` outside a throwaway development stack, and do not use it as evidence for the private-network claims in ADR 0001.

## Disposable Key Vault for development

`keyVaultPurgeProtection` (default `true`) keeps 90 day soft delete with purge protection. Set it to `false` for a disposable environment: 7 day soft delete and no purge protection, so a deleted vault can be purged with `az keyvault purge`. Purge protection cannot be switched off on an existing vault, so choose before the first deploy. The vault name also hashes the location, which avoids collisions when a resource group is recreated.

## Tested deployment

Region notes for `northeurope` (observed 2026-10-08): Azure SQL was not accepting new servers, so set `sqlLocation` (for example `uksouth`; the private endpoint stays in the VNet region), and `gpt-4.1*` has no pay-as-you-go SKU, so override `modelDeployments` (for example `gpt-5.4-nano` and `gpt-5.4` with `DataZoneStandard`).

Deployed on 2026-10-08 to resource group `ama` with `location=uksouth environmentName=test`. `swedencentral` returned `AKSCapacityHeavyUsage` for the Container Apps environment, so keep `location` a parameter. The SQL admin can be a user, group or application (`sqlAdminPrincipalType`).

## Validate locally

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

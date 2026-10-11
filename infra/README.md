---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Zava Forward demonstrator Azure architecture
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
* `scripts/create-sql-users.sql`: contained SQL users for the managed identities. `scripts/create-sql-users.py` runs the same grants idempotently from the Azure CLI login.
* `scripts/create-api-app-registration.sh`: Entra app registration, app roles and secret (Key Vault) for API sign-in.
* `scripts/configure-m365-provisioner-app.sh`: delegated Graph permissions for the app the m365 CLI uses to set up SharePoint and Teams.
* `scripts/grant-sharepoint-access.sh`: optional Graph `Sites.Selected` grant for the SharePoint evidence store.

Optional parameters: `teamsWebhookUrl`, `evidenceStore`, `sharePointSiteId`, `monthlyBudget`. See the M365 section of the ADR.

## Deploy

```bash
az group create -n rg-zava-forward-dev -l swedencentral
az deployment group what-if -g rg-zava-forward-dev -f infra/main.bicep -p infra/main.bicepparam
az deployment group create -g rg-zava-forward-dev -f infra/main.bicep -p infra/main.bicepparam
```

Then run the SQL script from a host with private network access, push the
application images to the registry and update the image parameters.

## Deployment profile

`deploymentProfile` is the general switch. It defaults to `production`, so a plain deployment keeps every isolation control.

| Control | production (default) | development |
|---|---|---|
| Network access | Private endpoints only, internal Container Apps environment | Also accepts external networks and gives the API a public FQDN (as `allowPublicNetworkAccess=true`) |
| Registry quarantine | Enabled: pushed images wait for scan and release | Disabled: new images can be pulled at once |
| Key Vault | 90 day soft delete with purge protection | 7 day soft delete, no purge protection |

`allowPublicNetworkAccess` and `keyVaultPurgeProtection` still work on their own to relax a single control in a production profile. Do not use the development profile as evidence for the private-network claims in ADR 0001.

Example: `az deployment group create -g ama -f main.bicep -p main.bicepparam -p deploymentProfile=development`.

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

## Deploying the workbench image and sign-in

Observed 2026-10-11 in resource group `ama` (`uksouth`, `environmentName=test`, `deploymentProfile=development`):

```bash
az acr build -r <registry> -t zava-forward-mvp:<tag> mvp
az login --tenant <tenant> --allow-no-subscriptions          # as an Application or Global Administrator
infra/scripts/create-api-app-registration.sh -u https://<api-fqdn> -a <admin-upn>:ProgrammeManager -v <key-vault>
python3 infra/scripts/create-sql-users.py ama <sql-server> retrofit id-forward-test   # as the SQL Entra admin
az deployment group create ... -p entraClientId=<client id> apiImage=<registry>.azurecr.io/zava-forward-mvp:<tag>
```

Notes:

* The registry accepts `az acr build` when public access is on (development profile).
* The image carries no data. Seed the SQL database once from an operator machine (see `mvp/README.md`, Azure SQL store); set `oid` on a staff record to a signed-in user's object id so that user maps to a workbench role.
* With `entraClientId` set, built-in authentication redirects browsers to sign in and returns 401 to clients that do not look like browsers. Only users assigned an app role can sign in. `/healthz` is excluded. The client secret is a Key Vault secret named `entra-client-secret` read through the API identity.
* The API listens on 8088 and serves only `/healthz` for probes (there is no `/readyz`). The agents, orchestrator and import workloads still run the placeholder image because no code for them exists yet.
* `ZF_ENV=production` is set when authentication is on, so the map has no background until `tileUrl` is set (for a dev test: `tileUrl=https://tile.openstreetmap.org/{z}/{x}/{y}.png tileAttribution='&copy; OpenStreetMap contributors'`, within the OSM tile usage policy; choose a licensed provider before real use). The CSP follows the tile host.
* The previous `allowedPrincipals` restriction on the auth config was removed: it listed managed identity client ids where object ids are expected and would have blocked signed-in users. Access is limited by the app role requirement instead.

## Microsoft 365 permissions

The runtime identity needs only Microsoft Graph application permission `Sites.Selected` plus a per-site grant (`scripts/grant-sharepoint-access.sh`, role `write` for the evidence library). Teams alerts use a Workflows webhook, which needs no Graph permission and is created by hand in the channel.

Setting the site and channel up through the m365 CLI needs delegated Graph permissions on the app it signs in with, consented by an administrator: `Sites.FullControl.All`, `Team.Create`, `Channel.Create`, `AppRoleAssignment.ReadWrite.All` and `Application.Read.All`, plus the existing `AllSites.Read`. `scripts/configure-m365-provisioner-app.sh <app id> --consent` adds them. Remove `Sites.FullControl.All` and the consent once the grants are made.

## Validate locally

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

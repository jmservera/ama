---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Zava Forward demonstrator Azure architecture
author: AMA programme
ms.date: 2026-10-12
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
* `scripts/initialize-api-auth.py`: post-deployment callback synchronization for an existing API registration, without replacing roles, assignments or credentials.
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

For a from-empty rebuild, first set `deployApplications=false`. This creates
the dependencies without temporarily exposing an unauthenticated placeholder
workbench. Build the real image, provision the vault auth secret and seed SQL,
then deploy again with `deployApplications=true`, `entraClientId` and `apiImage`.
The flag does not delete existing apps in incremental deployment mode.

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
* With `entraClientId` set, `/` is a public branded welcome and `/sign-in`
  deliberately enters Microsoft sign-in. `/app` and every data API stay
  protected; anonymous APIs return 401. Only the welcome, its stylesheet/logo,
  sign-in route and probes are excluded. The client secret is a Key Vault
  secret named `entra-client-secret` read through the API identity.
* The API listens on 8088 and serves only `/healthz` for probes (there is no `/readyz`). The agents, orchestrator and import workloads still run the placeholder image because no code for them exists yet.
* `ZF_ENV=production` is set when authentication is on, so the map has no background until `tileUrl` is set (for a dev test: `tileUrl=https://tile.openstreetmap.org/{z}/{x}/{y}.png tileAttribution='&copy; OpenStreetMap contributors'`, within the OSM tile usage policy; choose a licensed provider before real use). The CSP follows the tile host.
* The previous `allowedPrincipals` restriction on the auth config was removed: it listed managed identity client ids where object ids are expected and would have blocked signed-in users. Access is limited by the app role requirement instead.
* For the existing MVP's direct, human-reviewed model drafts, explicitly set
  `enableApiAi=true`. This grants the API identity model invocation access and
  supplies `AI_ENDPOINT` and both deployment names. The default remains false
  for the separately proposed agent-runner topology. Placeholder worker images
  do not provide real AI to the workbench; verify a result with `source=ai`.
* `entraRoleMap` can explicitly map an existing registration's role values to
  workbench roles during a rename. It does not update tenant roles or callback
  URLs and is not proof of a completed identity rename. An authorised
  registration owner must update those separately; remove the transitional
  mapping when the new default `ZavaForward.*` values are issued.

## Post-deployment API authentication initialization

An environment rebuild changes the ingress FQDN even when the API registration
is retained. After the protected API has been deployed, initialize its callback:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --login
```

The deployment operator discovers the tenant, current FQDN and configured client
ID. Explicit `--login` starts tenant-scoped device-code authentication in a
separate private Azure CLI profile, by default
`$AZURE_CONFIG_DIR/zava-entra-init` (or `~/.azure/zava-entra-init` when unset).
Complete it as an authorised registration owner or administrator. This does
not overwrite the deployment identity or grant tenant permissions to it.
Keep the profile outside the repository: it contains authentication material.

Subsequent initialization runs omit `--login`. Use `--tenant-profile <directory>`
to select an existing Graph-authorised provisioning profile. Verify without
changing the registration:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --check
```

The command validates tenant/client identity and enabled ingress authentication,
then reads the existing registration by client ID. It adds the current callback
to `web.redirectUris` only if missing, preserves prior redirects, and verifies
the update. Reruns do not patch an already initialized registration. Missing
callbacks in check-only mode, permission denial and unverifiable updates exit
nonzero. The command does not change display names, roles, assignments or
secrets. The existing creation helper is for first-time registration and role
provisioning, not a callback-only repair.

### Tenant staff and application-role initialization

An enterprise-app role assignment alone is not enough. The workbench also
requires an internal staff record bound to the person's Entra object id. A
valid role with no matching staff `oid` produces `Account not authorised`;
email fallback remains disabled. SQL staff is cached at startup, so completing
the binding also requires reloading the API replicas.

Use `scripts/initialize-workbench-staff.py` after callback initialization and
SQL seeding. Its private JSON roster is an array of `code`/`userId` objects:
include every existing staff code, with a distinct enabled tenant member for
each. The current fixture needs ten internal positions; one additional
Contractor makes eleven people covering all eight role kinds. New Contractor
entries also require `"role": "Contractor"` and `"contractor"` naming an
existing case supplier. Room, desk and workspace accounts are rejected.

Keep the roster outside the repository with file mode 0600 and parent-directory
mode 0700, for example `~/.azure/zava-forward-staff/roster.json`. The initializer
resolves current names/UPNs from Graph; do not put directory names, UPNs or ids
in committed examples. Title/group-based allocation is illustrative exercise
coherence, not evidence of professional competence or delegated authority.

```bash
PYTHONPATH=mvp python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-forward-test-api \
  --roster "$HOME/.azure/zava-forward-staff/roster.json" --check
PYTHONPATH=mvp python3 infra/scripts/initialize-workbench-staff.py \
  --resource-group ama --container-app ca-forward-test-api \
  --roster "$HOME/.azure/zava-forward-staff/roster.json" --apply --restart
```

Use the existing MVP dependencies and an operator allowed through the SQL
firewall/private endpoint with SQL write authority. Graph management uses the
isolated `~/.azure/zava-entra-init` profile, or `--tenant-profile`. It needs
delegated `AppRoleAssignment.ReadWrite.All`, `Application.Read.All`, directory
user/group read access and an appropriate administrative role. No new grants
are consented automatically. See the official
[application-role assignment API](https://learn.microsoft.com/en-us/graph/api/serviceprincipal-post-approleassignedto?view=graph-rest-1.0).

Check mode is read-only: exit 0 means the directory/SQL configuration matches,
2 means reconciliation is required; it does not claim a user's browser sign-in.
Apply adds missing roles only for this application, preserves Default Access,
rejects conflicting effective roles (including direct group grants), and never changes
directory administrator roles or group membership. Existing bound identities
cannot be replaced. SQL staff/current owner labels are updated atomically,
preserving workload codes, cases, supplier scope, prior approvals,
recommendations and the existing audit prefix; one generic audit event records
the initialization. Historical generated actors remain historical.
Nested group assignments do not cascade to users, so only direct group
membership counts toward an effective role. See Microsoft's
[enterprise-app assignment guidance](https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal).

`--apply --restart` replaces replicas on every traffic-serving revision,
including after a no-op SQL retry. Apply without restart exits 3 to report
incomplete runtime convergence. If SQL commits but restart fails, retry the
same command: no duplicate role grant or audit event is created. Do not reseed
or weaken authentication to repair onboarding. New role assignments may
require the person to sign out and sign in again for fresh role claims.

### Public welcome and Microsoft account photos

The existing registration is retained. Add only delegated own-user Graph
`User.Read` with the same isolated provisioning profile:

```bash
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --account-photo
python3 infra/scripts/initialize-api-auth.py \
  -g ama -n ca-forward-test-api --account-photo --check
```

This opt-in flag merges `User.Read` into existing requested permissions,
preserving all previous permissions/redirects. It does not grant administrator
consent, change roles, rotate credentials or request app-only
`ProfilePhoto.Read.All`. Users complete normal Microsoft sign-in/MFA/consent;
an administrator handles consent if tenant policy requires it. Never share
passwords, device codes, access tokens or a CLI profile directory.

Photos use the supported Container Apps Blob token store and a server-only
Graph `/me/photo/$value` proxy, not browser `/.auth/me` token retrieval.
Deployment has two deliberate stages:

1. Keep all existing deployment parameters and the real image. Deploy with
   `enableEntraTokenStore=true entraTokenStoreReady=false`. This creates a
   dedicated token-only storage account, private `auth-tokens` container,
   private endpoint, scoped maintenance identity and daily renewal job.
   Shared account keys and public Blob access remain disabled.
2. Start the maintenance job and require execution status `Succeeded`:

   ```bash
   az containerapp job start -g ama -n job-forward-test-auth-renewal -o none
   az containerapp job execution list -g ama -n job-forward-test-auth-renewal \
     --query '[].{name:name,status:properties.status,start:properties.startTime}' -o table
   ```

3. Only after success, redeploy the same parameters with
   `enableEntraTokenStore=true entraTokenStoreReady=true`. The API references
   the existing `entra-token-store-sas` secret; Bicep never resets its value.
   Auth now requests `openid profile email`, own-user `User.Read` and
   `offline_access`, with the Microsoft account chooser on fresh login.
4. Sign out and sign in again to obtain the new delegated scope. Confirm the
   account name/photo and logout/switch with an actual authorised user.

The job uses `ManagedIdentityCredential` and a five-day, HTTPS-only,
read/write/delete user-delegation SAS, renewed daily at 03:00 UTC. Its identity
has Blob Delegator at account scope, Blob Contributor only on `auth-tokens`,
Secrets Officer only on `entra-token-store-sas`, and registry pull. Existing
evidence/import identities get no rights on the separate token account.
Authentication tokens are real secret/personal authentication data, not the
constructed fixture. No token values/photos enter Git, job output or evidence.

Monitor failed/missing renewal executions and act before the last successful
SAS expires; daily renewal leaves about four days of overlap. Job output
reports only status/expiry and fails nonzero without overwriting a secret on
delegation failure. Versionless Key Vault references retrieve updates within
30 minutes; the secret-ref environment setting triggers active revision
refresh. Do not expose its value. See Microsoft's
[Container Apps secret rotation guidance](https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets#reference-secret-from-key-vault)
and [token-store contract](https://learn.microsoft.com/en-us/azure/container-apps/token-store),
checked 2026-10-12.

The UI shows initials and an explicit status when no photo exists or token,
consent or upstream access fails. An expired photo token gets at most one
supported `/.auth/refresh` attempt. This does not weaken workbench/API
authentication or make a mocked photo a live acceptance result.

## Microsoft 365 permissions

The runtime identity needs only Microsoft Graph application permission `Sites.Selected` plus a per-site grant (`scripts/grant-sharepoint-access.sh`, role `write` for the evidence library). Teams alerts use a Workflows webhook, which needs no Graph permission and is created by hand in the channel.

Setting the site and channel up through the m365 CLI needs delegated Graph permissions on the app it signs in with, consented by an administrator: `Sites.FullControl.All`, `Team.Create`, `Channel.Create`, `AppRoleAssignment.ReadWrite.All` and `Application.Read.All`, plus the existing `AllSites.Read`. `scripts/configure-m365-provisioner-app.sh <app id> --consent` adds them. Remove `Sites.FullControl.All` and the consent once the grants are made.

### API registration management with the existing M365 session

The existing delegated M365 session was checked on 2026-10-12. Its consented
Graph scopes do not include application management. Being logged in does not
make `entra app` write operations authorised. Azure RG Owner and the signed-in
user's directory authority are also distinct from the CLI client's consented
Graph permissions.

For delegated Graph application updates, Microsoft's
[Update application permission table](https://learn.microsoft.com/en-us/graph/api/application-update?view=graph-rest-1.0)
requires `Application.ReadWrite.All`, plus appropriate ownership/directory
authority. `Application.Read.All` is not sufficient to change redirects, app
names or roles. Prefer an authorised owner making this one-off portal update.
If CLI management is needed, an authorised administrator must temporarily
consent the management permission for the provisioning client and obtain a
fresh authenticated session. Remove unnecessary provisioning grants afterwards;
do not add tenant-management permissions to runtime identities.

A separate, legitimate delegated API-token request through the current M365
client returned `AADSTS65001` (consent required). That client is not an
alternative authenticated acceptance path. Graph management consent and
workbench sign-in are separate concerns: updating the registration does not
automatically consent another client to call the API, and an API token cannot
be substituted with a Graph token or forged proxy claims.

## From-empty rebuild observed on 2026-10-12

The owner-authorised `ama` reset retained the group, its policy-exception tag,
external deployment identity and tenant/M365 resources. No workload identity
needed preservation: Blob was the active evidence store, and Bicep/SQL recreated
the four workload identities and their grants. Do not generalise that decision
to identities with external site grants or other shared consumers.

Deletion has service-specific dependencies. Remove apps/jobs and private
endpoints before their environment/network, the Foundry project before its
account, and the private-link scope before its linked App Insights component.
Wait for accepted deletions to finish. Enumerate and delete resource-group
budgets separately; `az resource list` does not list them. Verify both the
generic inventory and this budget list are empty before deploying:

```bash
az resource list -g ama --query '[].{name:name,type:type}' -o json
az rest --method get --url \
  "https://management.azure.com/subscriptions/<subscription>/resourceGroups/ama/providers/Microsoft.Consumption/budgets?api-version=2023-05-01" \
  --query 'value[].name' -o json
```

Rebuild sequence:

1. Prepare non-secret deployment parameters: `workload=forward`,
   `environmentName=test`, both locations `uksouth`, `deploymentProfile=development`,
   the actual SQL Entra administrator/principal type, `enableApiAi=true`, Entra
   client ID, and the selected tile URL/attribution. In this subscription the
   tested models were `standard` / `gpt-4.1-mini` and `capable` / `gpt-4.1`, both
   version `2025-04-14`, `skuName=GlobalStandard`, capacity 30. Availability and
   quota must be rechecked, not assumed for another subscription.
2. Deploy with `deployApplications=false`. Use deployment outputs to discover
   the registry, SQL server, model endpoint and vault; do not guess hashed names.
3. Build a versioned `zava-forward-mvp` image with `az acr build`. Provision
   `entra-client-secret` in the new vault through an authorised operator. RG
   Owner alone does not grant Key Vault data-plane access. Transfer a retained
   credential only through a private file or the provisioning script, not a
   command argument or tracked parameter file.
4. Run `create-sql-users.py` as the configured SQL Entra administrator. Seed
   through the [Azure SQL store instructions](../mvp/README.md#azure-sql-store)
   before exposing replicas. Retain the continuing synthetic stock/cases and
   privately restore any signed-in staff object-id mapping. The image contains
   no fixture; a new, empty SQL database is not equivalent to the previous MVP.
5. Deploy with `deployApplications=true` and the real `apiImage`, keeping the
   same non-secret parameters. An explicit transitional `entraRoleMap` can
   preserve existing tenant role values; it cannot update the registration.
6. Run [post-deployment authentication initialization](#post-deployment-api-authentication-initialization)
   against the retained registration, using an authorised isolated tenant
   profile. A new callback does not require a replacement client ID or secret.
7. Wait for rollout, then check public `/healthz`, API 401 without credentials
   and browser redirection. Check SQL reads/writes and both model deployments
   from the API's own identity. Restart the actual revision and verify the
   audit writes persist. A template fallback or operator-only SQL test is not
   evidence of workload model/SQL access.

Both group deployments succeeded. The restored database has 980 cases, 443
open; the API identity read and appended audit entries; both model deployments
returned `source=ai`. Audit entries survived an actual application revision
restart. The initial health 503 cleared after cold image/auth-sidecar rollout;
subsequent health returned 200, unauthenticated API 401 and browser 302.
Worker jobs/apps still use placeholders and Decision 1 scoring is not thereby
implemented.

The owner subsequently confirmed working workbench sign-in and completed the
isolated provisioning login on 2026-10-12. A real initializer `--check` then
verified the retained callback, and the opt-in `--account-photo` merge and
read-only check succeeded. This separate provisioning profile has authority
for that registration; the deployment identity's directory rights were not
broadened. Live user photo/consent, map acceptance and tenant naming/role
transition are distinct checks, not established by CLI authentication.

## Validate locally

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
```

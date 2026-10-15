---
title: Azure Infrastructure (Bicep)
description: Bicep deployment of the proposed Zava Forward demonstrator Azure architecture
author: AMA programme
ms.date: 2026-10-14
ms.topic: how-to
---

Proposed, non-production infrastructure. The design and its rationale are in
[ADR 0001](../docs/adrs/0001-azure-architecture.md).

The [executive and technical Excalidraw views](../docs/architecture/README.md)
map these sources and the current ADR 0002 exercise realization. They
distinguish working API assistants from placeholder workers, configured
dependencies from observed proof, and development access from the intended
private production profile. They do not authorize deployment.

## Layout

* `main.bicep`: resource group scope entry point wiring all modules.
* `main.bicepparam`: dev parameters; replace the placeholder alert email and Entra group.
* `modules/`: identity, network (VNet, NSGs, private DNS), monitoring (Log Analytics, App Insights, AMPLS), Key Vault, storage, registry, SQL, Foundry, IoT Hub, Container Apps and the generic private endpoint.
* `role-assignments.json`: role-assignment matrix; `entra/app-registration.json`: declarative Entra registration and owners. Both are checked by `tests/test_identity_rbac.py`.
* `scripts/create-sql-users.sql`: contained SQL users for the managed identities. `scripts/create-sql-users.py` runs the same grants idempotently from the Azure CLI login.
* `scripts/create-api-app-registration.sh`: Entra app registration, app roles and secret (Key Vault) for API sign-in.
* `scripts/initialize-api-auth.py`: post-deployment callback synchronization for an existing API registration, without replacing roles, assignments or credentials.
* `scripts/initialize-workbench-staff.py`: private tenant-member/app-role/SQL binding reconciliation, with idempotent checks and serving-replica restart.
* `scripts/configure-m365-provisioner-app.sh`: delegated Graph permissions for the app the m365 CLI uses to set up SharePoint and Teams.
* `scripts/grant-sharepoint-access.sh`: optional Graph `Sites.Selected` grant for the SharePoint evidence store.

Optional parameters: `teamsWebhookUrl`, `evidenceStore`, `sharePointSiteId`, `monthlyBudget`. See the M365 section of the ADR.

## Deploy

```bash
az group create -n rg-zava-forward-dev -l uksouth
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

`allowPublicNetworkAccess=true` and `keyVaultPurgeProtection=false` are rejected in the production profile (see Quality gates). Use `deploymentProfile=development` for a throwaway stack. Do not use the development profile as evidence for the private-network claims in ADR 0001.

Example from the repository root: `az deployment group create -g ama -f infra/main.bicep -p infra/main.bicepparam -p deploymentProfile=development`.

## Quality gates

Run before a pull request (CI runs the same in `.github/workflows/mvp-validation.yml`):

```bash
az bicep lint --file infra/main.bicep
python3 -m unittest discover -s infra/tests -v
```

* `bicepconfig.json` sets every enabled linter rule to `error`, so a warning that matters (unused parameters, secrets in parameters or outputs, hardcoded environment URLs or locations, unsafe resource identifiers) fails `az bicep lint` and the build.
* `tests/test_bicep_policy.py` compiles `main.bicep` and checks the claims in this README against the template: every public access setting follows the single computed switch, no storage or Application Insights/Foundry keys, no registry admin user, Entra-only SQL with no login or password, Key Vault purge protection and RBAC, immutability policies on the audit containers, and private endpoints for each data service. It evaluates the profile logic to show the default production profile cannot set public access.
* `modules/guard.bicep` rejects unsupported parameter combinations before resources change: every module and top-level resource in `main.bicep` declares `dependsOn: [guard]` (directly or through another module), and a test fails if one can deploy first. CI sets `REQUIRE_AZ_BICEP=1`, so the infra tests fail rather than skip when `az` is missing. The failing parameter name states the problem: production profile with `allowPublicNetworkAccess=true` or `keyVaultPurgeProtection=false`, `evidenceStore=sharepoint` without `sharePointSiteId`, `entraTokenStoreReady` without `enableEntraTokenStore`, and `entraRoleMap` without `entraClientId`.

Open items: confirm in a subscription that `az deployment group validate` (or `what-if`) reports the guard parameter name and description for an unsupported combination (not verified here, no Azure session); the tests check the compiled template, not the deployed resources, so live policy evidence (for example Azure Policy compliance) remains separate.

## Development access from external networks

`allowPublicNetworkAccess` (default `false`) is a development switch. When `true`, the private endpoints stay in place but the following also accept external connections:

* Storage, Key Vault, Foundry, Container Registry, Log Analytics and Application Insights: public network access enabled (network ACL default action `Allow`).
* Azure SQL: public access enabled with a firewall rule `dev-external-access` covering all addresses. Entra-only authentication still applies. In the MCAPS subscription an external policy reverts SQL `publicNetworkAccess` to `Disabled` unless the resource group carries the tag `SecurityControl=Ignore` (observed 2026-10-08), so set that tag on the resource group first.
* Container Apps environment: external (not internal) with public access enabled, so the API gets a public FQDN. The private DNS zone for the environment is not created.

The Container Registry export policy is set to `enabled` in this mode because ACR requires it when public access is on. Identity and RBAC controls are unchanged (no keys, no SQL logins). Never set it to `true` outside a throwaway development stack, and do not use it as evidence for the private-network claims in ADR 0001.

## Governance controls

Governance as code for issue #147 (ADR 0002 decision 6). Owner decisions (2026-10-15): region `uksouth`; subscription owner and Legal/Compliance/DPO owner Juan Manuel Servera.

| Control | Where | Decision | Owner | Cost |
| --- | --- | --- | --- | --- |
| Azure Policy assignments (SQL and storage public access, Key Vault deletion protection, required tags) | [`governance.bicep`](./governance.bicep), subscription scope, deployed separately by the subscription owner | Built-in definitions, audit only (`enforcementMode=DoNotEnforce`): policy reports non-compliance but blocks nothing; a Deny stance is an open owner decision | Juan Manuel Servera | No charge for Azure Policy |
| Defender for Cloud plans (Storage, SQL servers, Key Vaults, Containers) | [`governance.bicep`](./governance.bicep) | Decided; plans stay on Free (no protection added) until the owner accepts a cost and sets `enableDefenderPlans=true` | Juan Manuel Servera | Per-resource pricing, not yet estimated: open item, confirm in the Azure pricing calculator before enabling |
| Resource locks | `enableLocks` in `main.bicep` (Key Vault, SQL, storage) | [`main.pilot.example.bicepparam`](./main.pilot.example.bicepparam) (a non-deployable example with placeholders; copy it to a private file and fill every value) sets `true`; the development file keeps `false` so the stack can be reset | Juan Manuel Servera | None |
| Tagging standard | `allTags` in `main.bicep` | `workload`, `environment`, `dataClassification`, `purpose`, `owner` on every resource; the required-tag policy checks `workload`, `environment`, `dataClassification` and `owner` on resource groups | Juan Manuel Servera | None |
| Known exceptions | [`policy-exceptions.json`](./policy-exceptions.json) | EX-001: `SecurityControl=Ignore` on the development resource group (MCAPS SQL public-access policy); expires 2026-12-31 | Juan Manuel Servera | None |

```bash
az deployment sub what-if -l uksouth -f infra/governance.bicep
az deployment sub create -l uksouth -f infra/governance.bicep
```

Open items: Defender cost estimate and the decision to enable; renewal of EX-001 after 2026-12-31 (never on a pilot group); whether to switch any policy from audit to Deny; the group must carry the required tags before Deny is considered. The platform-wide MCAPS policy itself is managed outside this repository.

## Identity and role assignments (issue 141)

[role-assignments.json](role-assignments.json) lists every identity, scope, role and reason, plus SQL grants. `tests/test_identity_rbac.py` parses every Bicep role assignment (principal, role definition and scope, including the token-maintenance rows) and fails when the set of (identity, role, scope) tuples differs from the matrix, when Owner, Contributor, User Access Administrator or Reader appear, or when a shared key, SQL login or connection string is introduced. The only connection string is the Application Insights ingestion string (not a data credential); `entra-client-secret` and `entra-token-store-sas` are inventoried in [secret-inventory.json](secret-inventory.json).

| Identity | Scope and role | Reason |
| --- | --- | --- |
| api | Key Vault Secrets User; blob Data Contributor; queue Message Sender; AcrPull; OpenAI User and Azure AI User (only when `enableApiAi`); IoT Hub Event Hubs Data Receiver; SQL reader, writer, ddladmin | Serve the workbench, enqueue tasks, read telemetry |
| agents | queue Data Contributor; AcrPull; OpenAI User and Azure AI User; no SQL | Run agents, reach data only through the API |
| orchestrator | queue Message Sender; AcrPull; no SQL | Enqueue only |
| import | blob and queue Data Contributor; AcrPull; SQL reader and writer | Imports |
| token-maintenance | Blob Delegator (account); blob Data Contributor (container); Secrets Officer (one secret); AcrPull | Renew the short-lived SAS |

Chat and memory store (ADR 0004, accepted by the owner 2026-10-15): no Bicep resource exists yet. When added it gets one data-plane role for the api identity, local auth disabled, and a new matrix row.

Entra registration: [entra/app-registration.json](entra/app-registration.json) is the declarative record (audience, callback, eight app roles mapped to the MVP personas, assignment required). `create-api-app-registration.sh` applies the registration idempotently but does not read the manifest: a test only keeps manifest, script app roles and `DEFAULT_ROLE_MAP` identical, and callback hostnames are supplied with `-u` at run time. Reproducibility (criterion 4) is therefore met by explicit manual steps and a named owner, not declaratively. Existing sign-in, picture and user switching are unchanged. Owner of the manual steps: Juan Manuel Servera (subscription owner; tenant ownership unconfirmed).

Open items:

* Owner sign-off of the matrix review (reviewer line is pending).
* Contractor B2B guest model (ADR 0002, #116) is proposed, not confirmed; tenant guest and cross-tenant policy are manual tenant steps.
* Drop `db_ddladmin` from the api identity after schema migration moves out of app start.
* Live `az role assignment list` comparison against a deployed group was not run here.

## Key Vault secret lifecycle

Secrets are listed in [secret-inventory.json](secret-inventory.json) with an owner, rotation interval and expiry alert window. `infra/scripts/secret_lifecycle.py` checks vault metadata against it (never secret values), produces the access review record and prints the rotation steps. Run `python3 -m unittest discover -s infra/tests -q` for its tests.

| Secret | Rotation interval | Expiry alert | Owner |
| --- | --- | --- | --- |
| `entra-client-secret` | 180 days | 30 days | Platform operator, named person open |
| `entra-token-store-sas` | 1 day (renewal job) | 3 days | Platform operator, named person open |

Expiry alerting: the vault diagnostic setting sends all logs to Log Analytics, and `modules/keyvault.bicep` adds a scheduled query alert on `SecretNearExpiryEventGridNotification` and `SecretExpiredEventGridNotification` (logged whether or not an Event Grid subscription exists) routed to the operations action group. A second alert fires on repeated 401/403 data-plane results. Every secret must carry an `--expires` date or the alert cannot fire; `check` reports secrets with no expiry.

### Rotate the Entra client secret

Run `secret_lifecycle.py rotation-plan --vault <vault> --app-id <id>`. The order gives no downtime: append a new app credential (the old stays valid), write it as a new version of `entra-client-secret` with an expiry, let the versionless Container Apps reference refresh (up to 30 minutes) or restart the active revision, verify sign-in, then delete the old credential. Do not delete first. The repeatable scripted step is `create-api-app-registration.sh -v <vault>`; add an `--end-date` when setting the secret.

### Access review

Quarterly (`reviewIntervalDays` 90), export `az role assignment list --scope <vault id> --include-inherited -o json` and run `secret_lifecycle.py review --assignments roles.json --reviewer <name>`. A named human sets each pending decision to keep or remove and the signed record is kept with the operations evidence. Owner alone gives no data-plane access.

### Open items

* Named owners for each secret and for the review.
* A live no-downtime rotation exercise in the test environment; only the ordering and checks are tested offline.
* Confirmation after deployment that the alert rules evaluate in Azure Monitor (not verified here; the template builds with `az bicep build`).
* Scheduling the review and `check` runs (for example a calendar task or pipeline) is an owner choice.

## Disposable Key Vault for development

`keyVaultPurgeProtection` (default `true`) keeps 90 day soft delete with purge protection. Set it to `false` for a disposable environment: 7 day soft delete and no purge protection, so a deleted vault can be purged with `az keyvault purge`. Purge protection cannot be switched off on an existing vault, so choose before the first deploy. The vault name also hashes the location, which avoids collisions when a resource group is recreated.

## Tested deployment

Region notes for `northeurope` (observed 2026-10-08): Azure SQL was not accepting new servers, so set `sqlLocation` (for example `uksouth`; the private endpoint stays in the VNet region), and `gpt-4.1*` has no pay-as-you-go SKU, so override `modelDeployments` (for example `gpt-5.4-nano` and `gpt-5.4` with `DataZoneStandard`).

Deployed on 2026-10-08 to resource group `ama` with `location=uksouth environmentName=test`. `swedencentral` returned `AKSCapacityHeavyUsage` for the Container Apps environment, so keep `location` a parameter. The SQL admin can be a user, group or application (`sqlAdminPrincipalType`).

## Deploying the workbench image and sign-in

Observed 2026-10-11 in resource group `ama` (`uksouth`, `environmentName=test`, `deploymentProfile=development`):

```bash
az acr build -r <registry> -f src/api/Dockerfile -t zava-forward-mvp:<tag> src
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

### Current exercise handover (2026-10-13)

The dated deployment notes above are history. The newer five-assistant
handover below supersedes the account-switch serving revision.
At that account-switch handover, after the from-empty rebuild, callback initialization, public welcome/photo
setup and tenant staff reconciliation, the deployed API is
`ca-forward-test-api`, serving image
`crforwardtestrzsrg.azurecr.io/zava-forward-mvp:account-switch-20261013-01`
in ready revision `ca-forward-test-api--0000009`. The tested image digest is
`sha256:8cf327786ac2b891a586e78981b4abf0cc9c86313d721cef74ea7fcda80fa599`.
The account-switch rollout changed the image only; private comparisons
preserved app/auth settings, SQL/AI configuration and secret references.

The owner reports working administrator and Coordinator sign-in. Eleven
tenant members are privately provisioned for ten stable internal positions
plus a supplier-scoped Contractor; no roster is committed. This is not
acceptance of every role, guest onboarding or a changed authenticated session.
The existing registration and `ProperWarm.*` compatibility role map are
retained deliberately, not silently renamed. Next-run recovery starts with
the check modes below; do not replace the registration, reseed the workload
or grant runtime tenant-management rights to fix a sign-in failure.

For observed outcomes and pending product gates, see the
[dated addendum](../docs/case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213).
Actual account replacement and own-photo acceptance remain separate from
operator checks, unit tests and the source-head CI/rubric results on #65.

### Five-assistant version: current handover

Historical rollout: after explicit owner authorization, image `assistants-20261013-02`
was published and deployed to the existing API as revision `--0000010`, pinned
to ACR digest
`sha256:d3e652cec1bdef8846270a75c124d55743bdb757231ffaeae585cc423e6b8786`.
Private comparisons preserve SQL/AI/auth configuration, workload identity,
scale and the old controlled-domain fingerprints. No model call occurred.

Live Azure SQL exposed a ledger-only DDL incompatibility before assistance
could run. Source `99aeaac` fixes fresh append-only ledger events, preserves
initial generated procurement/as-of, and enriches the
[existing synthetic generator](../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13).
After preserving the concurrent intended-proposal identity fix, combined
backend source `ec7721b` passes all 73 local actual SQL tests. A later
populated-visits rendering correction yields latest source `cd14b3b` and local
image `assistants-20261013-05`, with 389-test discovery (316 passed, 73 conditional
skips), 21 browser regressions and 21 exact-image generated-data UI/API/local
restart checks. It was subsequently published and deployed on 2026-10-14
as described below. Full evidence is in
[ADR 0002](../docs/adrs/0002-pilot-readiness-architecture.md#fresh-ledger-and-synthetic-coverage-learning-2026-10-13).

The owner stopped migration and requested a synthetic database reset. QA
authority was removed; historical revision `--0000011` served image
`d3e652ce`, with proactive off and assistance disabled. Database deletion was
cancelled on 2026-10-13. The owner explicitly reauthorized deletion/recreation
and all offered remaining delivery on 2026-10-14; that cancellation no longer
blocks the exact authorized action.

Only `retrofit` was deleted/recreated, with ledger enabled, serverless Gen5
2 vCore/minimum 0.5, auto-pause 60 minutes, 32 GB, local backups, 14-day
retention/12-hour differential backups and restored diagnostics. Original
contained user SIDs/roles/grants and all 11 privately bound staff were restored
without tenant changes. The generated date/procurement baseline now contains
980 cases, 38 booked visits (11 in the week 2026-10-12 to 2026-10-18), 12
Finance/quality/grant/request records, one package/601 source orders and four
offered handoffs. Previous recommendations/audit were intentionally reset.

Current serving revision is `ca-forward-test-api--0000012`, image05/source
`cd14b3b379026a87ebfa3e9058ac10c0df7888eb`, pinned to ACR manifest
`sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
Existing identity, auth configuration and scale are preserved; an independent
auth-token rotation stamp was retained. Health and restarted replicas pass.
This is
explicit exercise reset authority, not a general reseed or evidence-deletion
permission. Preserve tenant registration/authentication; do not grant runtime
tenant-management permissions. Keep real QA within its effective expiry,
call/token allowance and scoped spend approval; never extend or replenish it
because a reset occurred. Token limits are not a currency guarantee.

Renewed bounded operator QA used the registered service inside this serving
workload, with process-local authority, 10-call/126000-token allowance and
one-hour expiry, proactive off. All five returned distinct citation-validated
`ready` proposals through Azure OpenAI deployment `standard`, model
`gpt-4.1-mini-2025-04-14`: five attempts, 6884 total tokens and 15 ledger events.
Independent SQL controlled-domain hashes stayed unchanged; full assistant
table content hashes, outputs and usage survived a real revision restart.
The normal serving app still has no assistant authority and proactive remains
off; no standing paid worker or fabricated human verification/acceptance.

AC-057 requires a registered assistant through the changed deployed API,
provider/model/usage/outcome and independent actual SQL task/event evidence
before/after an app restart, plus unchanged controlled state and failure/
manual handling. General SQL Server CI or an anonymous HTTP 200 cannot
replace that proof. The operator service/model/SQL/restart portion is now
observed, not blocked on reset authorization. A real staff-authenticated
browser/API acceptance session, semantic calibration, role/accessibility
acceptance and measured benefit remain separate and are not claimed by
operator execution or local Chromium fixtures.

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

The initializer imports `ledger` and `mssqlstore` from `zava_forward.core` (moved in M2 of #199), so run `pip install --no-deps -e src/core -e src/agents -e src/api` first (M4 of #199 moved `chat_privacy`, `chat_isolation`, `recovery` to `core` and `ai_eval` to `agents`; no infra script imports them); `zava_forward.api.auth` (moved in M5 of #199) supplies the role map.

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

#### Account selection and safe flow diagnostics

"Use another account" is not Sign out. It goes to the fixed
`/sign-in?switch=1` route, which requests Easy Auth login with
`prompt=select_account` and returns to `/app`. Microsoft presents remembered
accounts or a sign-in form when none are remembered; the user chooses the
account. No global Microsoft logout is requested. Cancelling or choosing the
same account does not guarantee a changed account or a signed-out session.
Normal Sign out still uses platform logout and returns to the public welcome.
See Microsoft's [account-selection parameter](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#request-an-authorization-code).

The API emits five fixed console markers: `sign-in-started`,
`account-picker-started`, `account-switch-requested`, `sign-out-requested` and
`workbench-entered`, prefixed `auth flow:`. The latter three require successful
app authorization; POST markers also require the existing CSRF header.
New markers contain no identity, URL/query, cookie, principal or token values.
This does not claim all pre-existing platform/denial logs are identity-free.
Generic HTTP access logging remains disabled.

The existing environment `allLogs` diagnostic setting already routes console
output to `log-forward-test`; no new logging resources or role grants are
needed. Live console access:

```bash
az containerapp logs show -g ama -n ca-forward-test-api \
  --type console --tail 50
```

Use the resource-specific `ContainerAppConsoleLogs` table, not the legacy
`ContainerAppConsoleLogs_CL`. Allow ingestion delay and query fixed events
instead of publishing raw platform logs:

```kusto
ContainerAppConsoleLogs
| where TimeGenerated > ago(1h)
| where ContainerAppName == "ca-forward-test-api"
| extend Event = extract(@"auth flow: (sign-in-started|account-picker-started|account-switch-requested|sign-out-requested|workbench-entered)", 1, Log)
| where isnotempty(Event)
| summarize Events=count(), Latest=max(TimeGenerated) by Event, RevisionName
```

These events show attempted routes, not which account was chosen. Actual
acceptance starts with an authenticated browser: open Use another account,
select another authorised account and verify its current-account view and
permitted work. A fresh anonymous browser or operator CLI cannot prove session
replacement. Do not share browser cookies, passwords or tokens.

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

For the optional SharePoint evidence store, the runtime identity needs
Microsoft Graph application permission `Sites.Selected` plus a per-site grant
(`scripts/grant-sharepoint-access.sh`, role `write` for the evidence library).
The rebuilt exercise uses Blob; SharePoint grants are not a prerequisite for
that deployment. Teams alerts use a Workflows webhook, which needs no Graph
permission and is created by hand in the channel. Neither an optional template
parameter nor a placeholder worker proves that integration has run.

Setting the optional site and channel up through the m365 CLI needs delegated
Graph permissions on its provisioning app, consented by an administrator:
`Sites.FullControl.All`, `Team.Create`, `Channel.Create`,
`AppRoleAssignment.ReadWrite.All` and `Application.Read.All`.
The existing SharePoint `AllSites.Read` permission is separate from these
Graph scopes and does not grant application-management authority.
`scripts/configure-m365-provisioner-app.sh <app id> --consent` requests and
optionally consents the Graph scopes; it is an operator step, not runtime
startup. Remove unnecessary provisioning consent afterwards, including
`Sites.FullControl.All` once the grants are made. Own-user photos separately
use delegated `User.Read`, not tenant-wide application photo permission.

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
3. Build a versioned `zava-forward-mvp` image with `az acr build` with the `src/` folder as build context (`-f src/api/Dockerfile src`). Provision
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
   If enabling own-user photos, complete the separate
   [staged token-store setup](#public-welcome-and-microsoft-account-photos).
   Reconcile the private roster with the
   [staff initializer](#tenant-staff-and-application-role-initialization)
   after seeding, including its serving-replica restart and read-only check.
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
broadened. Later tenant-staff reconciliation and owner-reported sign-in are
recorded in the current handover above. Live user photo/consent, changed-account
acceptance, map acceptance and tenant naming/role transition remain distinct
checks, not established by CLI authentication.

## Validate locally

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
az bicep build --file infra/governance.bicep --stdout > /dev/null
python3 -m unittest infra/tests/test_governance.py
```

## IoT Hub (issue 140, ADR 0003 decision 6)

`modules/iothub.bicep` provisions the device-to-cloud ingestion boundary for simulated in-use monitoring. Decisions recorded here are proposals pending owner approval of ADR 0003.

| Item | Decision |
| --- | --- |
| Region | uksouth (owner decision) |
| Tier and units | B1, 1 unit: device-to-cloud and message routing only, enough for the simulator. Move to S1 (parameter `iotHubSku`) only if twins, cloud-to-device or IoT Edge are needed |
| Cost | Estimate of 25 per month in the billing currency, set as a hub-scoped budget (`iotHubMonthlyCost`) with 80 percent actual and 100 percent forecast alerts. An estimate: confirm against the Azure pricing page before provisioning |
| Retention | Built-in endpoint keeps messages 1 day (`iotHubRetentionDays`, maximum 7). Azure SQL is the system of record |
| Consumer | Consumer group `api-consumer` on the built-in endpoint; the API managed identity has only Azure Event Hubs Data Receiver on the hub |
| Service credentials | `disableLocalAuth` is true: no shared access policy or connection string exists, so none can be stored in source or logs |
| Network | Production profile: public access disabled, private endpoint with `privatelink.azure-devices.net` and `privatelink.servicebus.windows.net`. Development profile: public access allowed for a throwaway stack |
| Diagnostics | Connections, DeviceIdentityOperations, Routes, Configurations and metrics to Log Analytics. DeviceTelemetry is not logged, keeping readings and device ids out of logs |
| Device identity | Individual device identities with per-device keys or X.509 certificates, issued by the simulator provisioning step (#185). Device Provisioning Service is deferred until real sensors are in scope |
| Credential owner | Juan Manuel Servera issues and rotates device credentials (owner decision); device keys are held in Key Vault, never in source |

Gates: `az bicep build` and `az bicep lint` run in `mvp-validation.yml`; `infra/tests/test_iothub_module.py` guards the module. Open: a live `az deployment group what-if` against the target resource group needs subscription access and has not been run; real pricing confirmation; B1 private endpoint behaviour verified in a deployment.

## Private networking and public edge (issue 143, ADR 0002 decision 6)

Private-endpoint and DNS coverage per service (checked by `infra/tests/test_edge_module.py`, which parses each module's private endpoint calls and resolves their DNS zones against the zone list in `network.bicep`; any module with a public-access switch must have a private endpoint):

| Service | Private endpoint group | Private DNS zone |
|---|---|---|
| Azure SQL | `sqlServer` | `privatelink.database.windows.net` |
| Storage | `blob`, `queue` | `privatelink.blob...`, `privatelink.queue...` |
| Token-only auth storage | `blob` | `privatelink.blob...` |
| Key Vault | `vault` | `privatelink.vaultcore.azure.net` |
| Container Registry | `registry` | `privatelink.azurecr.io` |
| Foundry (Azure OpenAI) | `account` | `cognitiveservices`, `openai`, `services.ai` zones |
| IoT Hub | `iotHub` | `privatelink.azure-devices.net`, `privatelink.servicebus.windows.net` |
| Monitor (AMPLS) | `azuremonitor` | `monitor`, `oms`, `ods`, `agentsvc`, `blob` zones |
| Container Apps environment | Internal environment in the delegated subnet (no endpoint) | Environment DNS zone (`envDns.bicep`) |

Any new store must add a `privateEndpoint.bicep` call, a zone in `network.bicep`, and an entry in the test's coverage map.

Public edge: `enablePublicEdge=true` deploys `modules/edge.bicep` (Front Door Premium, WAF policy with the default and bot rule sets, Private Link origin to the internal environment, diagnostics to Log Analytics). The guard rejects it in the development profile or with `allowPublicNetworkAccess=true`, so development public access cannot be enabled together with the edge or in the production profile. After deployment an owner must approve the pending private endpoint connection on the Container Apps environment (Networking, Private endpoint connections). `edgeCustomDomain` adds a managed-certificate custom domain; the domain is attached to the route in the same deployment, but the managed certificate stays Pending until the owner creates the DNS validation TXT and CNAME records, so the custom host does not serve traffic before that; deploy without a domain first if that matters.

Open items for the edge (no production-profile deployment evidence yet): Private Link to the `managedEnvironments` group of an internal, VNet-injected Container Apps environment is unverified for this configuration, so do not rely on `enablePublicEdge` until a deployment shows the pending connection and a healthy origin; a live `az deployment group what-if` has not been run. The `entraRedirectUri` output is the callback URL to register (`infra/scripts/create-api-app-registration.sh -u https://<edge host>`), and the API sets the forward-proxy convention so sign-in callbacks use the edge host.

Open items (not verified here):

* Evidence for private-network claims must come from a production-profile deployment (uksouth, Azure only). This change was validated by `az bicep build`, lint and static tests only; no deployment ran. Record the deployment evidence before any claim.
* Confirm Front Door Premium Private Link support for Container Apps environments in uksouth and its current pricing at deployment time.
* Custom domain name and DNS ownership, and the pilot edge go/no-go, are owner decisions (ADR 0002 open: pilot network design).

---
title: Environment Strategy, Region and Quota Parameterization, and Recorded Checks
description: Canonical specification of Zava Forward dev, test, and pilot Bicep parameter sets, bounded region and service quota parameters, mechanical fail-closed check-reference guards, and dated capability/quota evidence
author: GitHub Copilot
ms.date: 2026-11-15
ms.topic: reference
---

## Architectural Principle and Scope

Zava Forward treats Azure region selection and every service SKU, capacity, and budget choice as explicit, compile-time-bounded infrastructure parameters backed by dated, reviewed capability and quota checks, never as silent template assumptions.

* One canonical resource-group entry point (`infra/main.bicep`) promotes across `dev` (`infra/main.bicepparam`), `test` (`infra/main.test.bicepparam`), and `pilot` (`infra/main.pilot.example.bicepparam`) by changing only parameter files and immutable container image digests.
* All permitted demonstrator deployments stay inside the existing Azure resource group `ama` (`resourceGroupMustBeAma`). Environment names isolate resource prefixes (`forward-dev`, `forward-test`, `forward-pilot`) inside `ama`; separate operational subscriptions or resource groups remain an owner architecture decision recorded in [ADR 0002](../adrs/0002-pilot-readiness-architecture.md).
* Committed parameter files are deliberately non-deployable: `regionCheckReference` and `quotaCheckReference` remain empty `PLACEHOLDER` strings in Git, and `infra/main.pilot.example.bicepparam` additionally retains empty `location` and `sqlLocation` `PLACEHOLDER` strings until subscription binding, SQL region admission, sizing, and named human sign-off are recorded privately.
* Passing mechanical Bicep or CLI validation proves only parameter syntax, numeric/domain bounds, and non-placeholder check-reference formatting. It never substitutes for a fresh read-only capability/quota check on the target subscription or human deployment approval.

For operator deployment runbooks and the full historical query output, see [Infrastructure Runbook (`infra/README.md`)](../../infra/README.md#environments).

## Environment Parameter Matrix (`dev`, `test`, `pilot`)

All three committed `.bicepparam` sets declare region, security-profile, and service quota inputs explicitly rather than relying on uninspected defaults. `infra/main.bicepparam` and `infra/main.pilot.example.bicepparam` omit demo-chat overrides completely (enforced offline by `infra/tests/test_bicep_policy.py`), while `infra/main.pilot.example.bicepparam` omits serverless auto-pause inputs completely (enforced offline by `infra/tests/test_sql_tier.py`).

| Parameter or capability | `dev` (`infra/main.bicepparam`) | `test` (`infra/main.test.bicepparam`) | `pilot` (`infra/main.pilot.example.bicepparam`) |
| --- | --- | --- | --- |
| `environmentName` | `dev` | `test` | `pilot` |
| `deploymentProfile` | `development` | `production` | `production` |
| `location` | `uksouth` | `uksouth` | `''` (`PLACEHOLDER`; owner selected `uksouth` on 2026-10-15, committed example stays non-deployable) |
| `sqlLocation` | `uksouth` | `uksouth` | `''` (`PLACEHOLDER`; separate SQL region admission remains unselected) |
| `zoneRedundant` | `false` | `false` | `false` (`PLACEHOLDER` pending regional zone verification and owner decision) |
| `regionCheckReference` | `''` (`PLACEHOLDER`) | `''` (`PLACEHOLDER`) | `''` (`PLACEHOLDER`) |
| `quotaCheckReference` | `''` (`PLACEHOLDER`) | `''` (`PLACEHOLDER`) | `''` (`PLACEHOLDER`) |
| `sqlTier` and SQL SKU | `serverless` (`GP_S_Gen5`) | `serverless` (`GP_S_Gen5`) | `provisioned` (`GP_Gen5`, [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) decision 1) |
| `sqlVCores` | `2` | `2` | `2` (`PLACEHOLDER` pending pilot load sizing) |
| `sqlAutoPauseDelayMinutes` | `60` | `60` | Not declared (`provisioned` tier disables serverless auto-pause) |
| `sqlBackupRetentionDays` | `14` (template default) | `14` (template default) | `14` (`PLACEHOLDER`; PITR window only, legal retention is Issue `#121`) |
| `apiMinReplicas` | `0` (scale-to-zero demo default) | `0` | `0` (set `2` in private copy for always-on replicas after budget approval) |
| `modelDeployments` | `standard`: `gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1` | `standard`: `gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1` | `standard`: `gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1` |
| `iotHubSku` / `iotHubUnits` | `B1` / `1` | `B1` / `1` | `B1` / `1` |
| `iotHubRetentionDays` / `iotHubMonthlyCost` | `1` day / `60` | `1` day / `60` | `1` day / `60` (`PLACEHOLDER` within verified subscription budget) |
| `monthlyBudget` | `300` | `300` | `300` (`PLACEHOLDER` pending pilot billing confirmation) |
| `allowPublicNetworkAccess` | `false` | `false` | `false` |
| `keyVaultPurgeProtection` | `false` (7-day soft delete) | `true` (90-day soft delete + purge protection) | `true` (90-day soft delete + purge protection) |
| `registryQuarantineEnabled` | `false` (explicit dev opt-out) | `true` | `true` |
| `enableLocks` | `false` | `false` | `true` (`CanNotDelete` on stateful services) |
| Failing `parameter-guard` checks as committed | `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded` | `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded` | `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, `deploymentLocationsMustBeSelected`, `primaryLocationMustBeUKSouth` |

## Region Parameter Contract and Standalone Entry Points

Primary stack deployments separate the workload region from the Azure SQL logical server region so regional SQL server admission limits can be accommodated without moving the VNet or Private Link boundary:

* `location` (`infra/main.bicep`, default `resourceGroup().location`) sets the primary deployment region for VNet, Container Apps, Key Vault, Storage, Container Registry, Foundry, IoT Hub, and Private Endpoints. `primaryLocationMustBeUKSouth` requires `location == 'uksouth'`.
* `sqlLocation` (`infra/main.bicep`, default `location`) sets the Azure SQL logical server and database region (`infra/modules/sql.bicep` `location: sqlLocation`), while `endpointLocation: location` keeps the SQL Private Endpoint inside `vnet-{prefix}` (`pe` subnet) in the primary `uksouth` VNet.
* `zoneRedundant` (`bool = false`) propagates consistently to `modules/storage.bicep` (`Standard_ZRS` vs `Standard_LRS`), `modules/registry.bicep` (`ZoneRedundancy`), `modules/sql.bicep` (`zoneRedundant` and `Zone` vs `Local` backup storage redundancy when `sqlBackupStorageRedundancy` is empty), and `modules/containerapps.bicep` (`zoneRedundant`).

Standalone operational and prototype templates enforce explicit regional boundaries independent of `infra/main.bicep`:

| Template | Regional parameter and constraint | Scope guard and boundary |
| --- | --- | --- |
| `infra/iot-hub-live.bicep` (`infra/iot-hub-live.bicepparam`) | `param location string = 'uksouth'` | `iot-live-scope-guard` enforces `resourceGroup().name == 'ama'` and `location == 'uksouth' && hub.location == location`, binding read-only consumer-group and diagnostic attachment to `iot-cutover-test-rzsrg` (`B1`, `1` unit). |
| `infra/modules/iothub.bicep` | `param location string` | `iot-scope-guard` enforces `resourceGroup().name == 'ama'` and `location == 'uksouth'` before provisioning any IoT Hub or Event Hub resource. |
| `infra/resident-demo.bicep` | `param location string = resourceGroup().location` | `resident-demo-scope` enforces `resourceGroup().name == 'ama'`, `environmentName == 'cae-cutover-test-demo'`, immutable `@sha256:` image digest, and bounded `expiresAt` ceiling. |
| `infra/resident-assistant.bicep` | `@allowed(['swedencentral']) param location string = 'swedencentral'` | Opt-in voice/realtime prototype isolated to `swedencentral` (`gpt-realtime-1.5` preview regional availability, documented in [Resident Assistant Prototype](resident-assistant-prototype.md)); never changes primary Zava Forward data residency in `uksouth`. |

## Quota, SKU, and Capacity Parameter Catalog

Every adjustable capacity, SKU, and budget input in `infra/main.bicep` and its child modules carries compile-time bounds, while fixed service tiers that lack owner approval to vary remain locked in module definitions:

| Parameter | Defined in | Bounds and default | Downstream resource target |
| --- | --- | --- | --- |
| `sqlTier` | `main.bicep`, `modules/sql.bicep` | `@allowed(['serverless', 'provisioned'])`, default `'serverless'` | `Microsoft.Sql/servers/databases` SKU (`GP_S_Gen5` when `serverless`, `GP_Gen5` when `provisioned`) |
| `sqlVCores` (`maxVCores` in `modules/sql.bicep`) | `main.bicep`, `modules/sql.bicep` | `@minValue(1) @maxValue(80)`, default `2` | `Microsoft.Sql/servers/databases` `sku.capacity` (with `minCapacity: '0.5'` in `serverless` mode) |
| `sqlAutoPauseDelayMinutes` (`autoPauseDelayMinutes` in `modules/sql.bicep`) | `main.bicep`, `modules/sql.bicep` | `@minValue(-1)`, default `60`; `serverlessAutoPauseDelayMustBeSupported` enforces `-1` or `15..10080` when `sqlTier == 'serverless'` | `Microsoft.Sql/servers/databases` `autoPauseDelay` (omitted when `provisioned`) |
| `sqlBackupRetentionDays` | `main.bicep`, `modules/sql.bicep` | `@minValue(1) @maxValue(35)`, default `14` | `Microsoft.Sql/servers/databases/backupShortTermRetentionPolicies` `retentionDays` |
| `apiMinReplicas` | `main.bicep`, `modules/containerapps.bicep` | `@minValue(0) @maxValue(4)`, default `0`; `publicSimulationRequiresSingleReplica` requires `<= 1` when `enablePublicSimulationLane` is enabled | `ca-{applicationPrefix}-api` `scale.minReplicas` (paired with locked `maxReplicas: enablePublicSimulationLane ? 1 : 4`, `0.5` CPU, `1Gi` memory; agent apps lock `minReplicas: 0`, `maxReplicas: 5`, `0.25` CPU, `0.5Gi` memory) |
| `modelDeployments` | `main.bicep`, `modules/foundry.bicep` | `@minLength(1)`, default `[{ name: 'standard', model: chatModelName, version: chatModelVersion, skuName: chatModelSku, capacity: chatModelCapacity }]` | `Microsoft.CognitiveServices/accounts/deployments` (`AIServices` kind, `S0` SKU, serial `@batchSize(1)` deployment) |
| `chatModelName` / `chatModelVersion` / `chatModelSku` / `chatModelCapacity` | `main.bicep` | `'gpt-4.1-nano'`, `'2025-04-14'`, `@allowed(['GlobalStandard', 'Standard'])` `'GlobalStandard'`, `@minValue(1)` `1` | Populates the default `standard` entry of `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep` (separate from employee demo-chat runtime activation gated by `demoDirectIngress` and `chatDemoActivation == 'approved-2026-11-03'` in `modules/containerapps.bicep`) |
| `iotHubSku` / `iotHubUnits` | `main.bicep`, `modules/iothub.bicep` | `@allowed(['B1'])` `'B1'`, `@minValue(1) @maxValue(1)` `1` | `Microsoft.Devices/IotHubs` `sku.name` and `sku.capacity` (paired with `EventHub` `Standard` capacity `1` when provisioned) |
| `iotHubRetentionDays` / `iotHubMonthlyCost` | `main.bicep`, `modules/iothub.bicep` | `@minValue(1) @maxValue(7)` `1`, `@minValue(1) @maxValue(700)` `60` | IoT built-in and Event Hub message retention (`1..7` days) and IoT monthly cost budget (`monthlyCostEstimate` in `modules/iothub.bicep`) |
| `monthlyBudget` | `main.bicep`, `modules/operationalMonitoring.bicep` | `@minValue(1)`, default `300` | `budget-{prefix}` (`Microsoft.Consumption/budgets` in `main.bicep` and budget alert metadata in `modules/operationalMonitoring.bicep`, notifications at 80 percent actual and 100 percent forecast; advisory alert, not a hard billing cap) |

Fixed module SKUs that are intentionally not exposed as entry-point parameters include Log Analytics `PerGB2018` (`90`-day retention), Key Vault `standard`, Storage `StorageV2` (`Standard_LRS` or `Standard_ZRS`), Container Registry `Premium` (`30`-day retention), Foundry account `AIServices` `S0`, Container Apps `Consumption` workload profile, and optional Front Door `Premium_AzureFrontDoor` (`enablePublicEdge`).

## Mechanical Fail-Closed Guards (Bicep and Python CLI)

Both ARM template validation (`infra/modules/guard.bicep` wired as `parameter-guard` in `infra/main.bicep`, containing 29 `@minLength(1)` controls that every child module depends on) and the Python deployment wrappers (`infra/scripts/pipeline.py` and `infra/scripts/deploy.py`) enforce fail-closed validation before any Azure resource write:

* Recorded check guards (`regionCheckMustBeRecorded` and `quotaCheckMustBeRecorded` in `infra/main.bicep`):
  * Trim and lowercase `regionCheckReference` and `quotaCheckReference`.
  * Reject empty or whitespace-only values.
  * Reject substring markers `placeholder`, `example.invalid`, `n/a`, and the all-zero GUID `00000000-0000-0000-0000-000000000000`.
  * Tokenize punctuation delimiters (`-`, `_`, `/`, `#`, `.`, `:`, `,`, `;`, `(`, `)`) and reject whole-word assumption or skip tokens (`todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `na`, `skip`) without false positives on legitimate repository words or section anchors such as `spending` or `jtbd`.
  * Reject bare 36-character `8-4-4-4-12` hex UUIDs in Bicep so subscription, tenant, or object IDs cannot be pasted as check references.
* Location guards (`primaryLocationMustBeUKSouth` and `deploymentLocationsMustBeSelected` in `infra/main.bicep`):
  * Require `location == 'uksouth'` with no leading/trailing whitespace or uppercase characters.
  * Require `sqlLocation` to be at least 3 characters, start with a lowercase ASCII letter, contain only `[a-z0-9-]` with no empty hyphen segments (no leading, trailing, or double hyphens), and exclude bare UUIDs, `placeholder`, and the assumption/skip word set.
* CLI preflight guards (`infra/scripts/pipeline.py` and `infra/scripts/deploy.py`):
  * Apply the same case-insensitive ASCII non-alphanumeric-bounded (`(?<![a-z0-9])...(?![a-z0-9])`, treating `_` as a delimiter) assumption and placeholder rejection to `regionCheckReference` and `quotaCheckReference`, plus full regex rejection of both bare and prose- or underscore-embedded UUIDs (`(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])`).
  * Enforce `location == "uksouth"` and lowercase alphanumeric Azure region slugs (`^[a-z][a-z0-9]+$`) excluding placeholder/assumption words (`sqlLocation=placeholder`, `sqlLocation=assumed`, `sqlLocation=tbd`, etc.).
  * Inspect every `--parameter NAME=VALUE` flag passed to `deploy.py` in order without collapsing duplicate keys and never echo raw rejected parameter values in `PipelineError` or `DeploymentError` messages.

## Recorded Capability and Quota Check Ledger (`R1` through `R17`)

Read-only management-plane capability and quota queries `R1` through `R17` were executed on `2026-10-18` (and reproduced identically on `2026-10-19` at `06:43 UTC`) against historical commit `612cbed78a35a4ab426571aa7d2aeb0ae6d691dd` (`infra/main.bicep` SHA-256 `daea1e37adc95f704fba7673883e0b4b6c7b65ab00179b59d8473654ab71f42a`). Full command shapes and REST API versions are maintained in [`infra/README.md`](../../infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137).

| Check IDs | Service and `uksouth` scope | 2026-10-18 recorded status | Architectural boundary and remaining prerequisite |
| --- | --- | --- | --- |
| `R1`, `R12` | Container Apps `Microsoft.App` provider and Consumption profile | Observed (`Pass` catalog listing: `cores=4`, `memoryGiB=8`) | Profile shape only; does not establish spare regional Consumption-core quota. |
| `R1`, `R3` | Container Apps availability-zone mappings (`locations/uksouth`) | `Unknown` / `Blocked` (`AuthorizationFailed` on location GET) | `zoneRedundant` remains `false` (`PLACEHOLDER` in `pilot`) until zone support is verified. |
| `R2` | Container Apps regional usages (`ManagedEnvironmentCount` `2/50`) | `Unknown` Consumption-core quota | Environment count is not vCore headroom; re-check before scaling replicas. |
| `R4` | Azure SQL `uksouth` capabilities (`GP_S_Gen5_2` serverless) | Observed (`Pass` catalog listing for `GP_S_Gen5_2` on `2026-10-18`) | Historical `R4` queried serverless `GP_S_Gen5_2`; provisioned `GP_Gen5` in `main.pilot.example.bicepparam` and live server admission in `sqlLocation` remain `Unknown` until a fresh `R4` query runs on the target subscription. |
| `R5`, `R16` | Azure SQL regional usages (`2023-08-01`, `2021-11-01`) | `Unknown` (`value=[]` empty collections) | Empty usage list does not mean zero or unlimited vCore quota; verify vCore headroom on the bound pilot subscription. |
| `R6`, `R13` | IoT Hub `Microsoft.Devices` SKUs and provider regions | Observed regional listing; `Unknown` `B1`/unit/zone detail (`value=[]`) | Provider lists UK South; exact `B1` unit and zone availability require target-subscription confirmation. |
| `R7`, `R14` | IoT Hub regional usages (`2023-06-30`, `2021-07-02`) | `Blocked` (`Bad Gateway`, exit `1`) | No IoT quota usage/limit established by the `2026-10-18` snapshot. |
| `R8` | Cognitive Services / Foundry model catalog (`uksouth`) | Observed (`gpt-4.1-mini` and `gpt-4.1`, `2025-04-14`, `GlobalStandard` listed on `2026-10-18`) | Historical `R8` queried `gpt-4.1-mini` and `gpt-4.1` (`capacity = 30`); current template default `gpt-4.1-nano` (`2025-04-14`, `GlobalStandard`, `capacity = 1`) post-dates `612cbed7` and remains `Unknown` until a fresh `R8` catalog check runs on the target subscription. |
| `R9`, `R15` | Cognitive Services regional usages (`uksouth`) | `Unknown` (`[]` / `value=[]` for inference usage rows) | Current TPM/RPM usage and quota headroom for `gpt-4.1-nano` (and any secondary model) remain `Unknown` until verified on the bound subscription. |
| `R10` | Storage `StorageV2` (`Standard_LRS`, `Standard_ZRS`) | Observed (`Pass` regional SKU listing, `restrictions=[]`) | Catalog listing only; storage redundancy selection follows `zoneRedundant` decision. |
| `R11`, `R17` | Container Registry `Microsoft.ContainerRegistry` SKUs and provider | Observed regional listing; `Unknown` `Premium` SKU/zone/quota detail (`value=[]`) | Re-verify `Premium` registry quota and zone support when `zoneRedundant` is evaluated. |

Operational rules for `regionCheckReference` and `quotaCheckReference`:

* Record references as repository-relative document anchors or reviewed ticket/runbook identifiers (for example `infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137` only when deploying a configuration covered by that reviewed check, or the private dated check record created for a target subscription).
* Never place Azure subscription IDs, tenant IDs, Entra object IDs, resource IDs, or secrets inside `regionCheckReference` or `quotaCheckReference`.
* Re-run capability and quota checks whenever the target subscription, `location`, `sqlLocation`, `zoneRedundant`, `sqlTier`, `sqlVCores`, `modelDeployments`, `apiMinReplicas`, or IoT Hub SKU/unit parameters change.

## Deterministic Offline Verification

`infra/tests/test_environment_quota_parameters.py` provides offline, zero-credential verification of the parameter, guard, and documentation contract:

* Compiles `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`, standalone regional templates (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), and all three `.bicepparam` sets with `az bicep`, asserting exact `@allowed`, `@minValue`, `@maxValue`, and `@minLength` bounds, module forwarding, and committed fail-closed guard sets.
* Evaluates compiled `parameter-guard` ARM expressions against blank, whitespace, placeholder, assumption-word, bare UUID, and malformed-region inputs, plus positive repository anchors containing substrings such as `spending` and `jtbd`, and runs negative ARM template mutations to verify tamper detection.
* Exercises `infra/scripts/pipeline.py` and `infra/scripts/deploy.py` parameter validation against placeholder, assumption, bare/embedded UUID, duplicate `--parameter`, and invalid-region overrides while verifying that raw rejected values are never echoed in errors.
* Verifies parity across compiled Bicep defaults, this architecture document, `docs/architecture/README.md`, and `infra/README.md` (`## Environments` and `R1` through `R17`).

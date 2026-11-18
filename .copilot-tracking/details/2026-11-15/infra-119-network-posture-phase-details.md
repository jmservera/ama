<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #119 Network Posture, Private Endpoints and Secret Store

## Metadata

* Task ID: issue-119-network-posture-2026-11-15
* Task slug: infra-119-network-posture
* Related plan: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md, infra/main.bicep, infra/modules/network.bicep, infra/modules/privateEndpoint.bicep, infra/modules/envDns.bicep, infra/modules/containerapps.bicep, infra/scripts/bicep_inventory.py, infra/secret-inventory.json, docs/architecture/README.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Author deterministic network-posture and secret-binding inventory contract | ready | P01, P01-T01 |
| P02 | Synchronize architecture network-posture diagram and infrastructure docs | ready | P02, P02-T01, P02-T02 |
| P03 | Implement offline network-posture, secret-store, and diagram-parity test suite and validate | ready | P03, P03-T01, P03-T02 |

## Locked Test & Artifact Ownership Contract

* Applicable test ownership: `infra/tests/test_network_posture.py` (new single test module owning AC-01, AC-02, AC-03, and fail-closed mutation checks).
* Exact test removals: `none` (all existing `infra/tests/test_*.py` suites remain intact and passing).
* Maximum test additions: `1` new test file (`infra/tests/test_network_posture.py`) containing `<= 18` focused semantic and fail-closed mutation test methods.
* Canonical vs generated targets:
  * Canonical authored files: `infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`, `infra/tests/test_network_posture.py`.
  * Generated/untouched artifacts: `docs/architecture/zava-forward-executive-architecture.excalidraw` and `docs/architecture/zava-forward-technical-architecture.excalidraw` are NOT regenerated or modified (`docs/architecture/update-architecture.mjs --check` remains undisturbed).
* Semantic vs regression coverage:
  * Semantic contract checks verify compiled ARM output (`az bicep build --stdout` and `az bicep build-params --stdout`), AST-scanned Bicep resource declarations (`bicep_inventory.scan_bicep_tree`), `secret-inventory.json` alignment, `src/` `ManagedIdentityCredential` / `ZF_SQL_AUTH='msi'` enforcement, and parsed Mermaid nodes/edges + Markdown tables in `docs/architecture/network-posture.md`.
  * Negative mutation checks verify fail-closed rejection when an unmapped data store is injected, a private endpoint is deleted, an exercise exception omits `owner` or `rationale`, a literal secret `value` is added to Container Apps `secrets`/`env`/`appSettings` or `listKeys` appears in Bicep, or a subnet/DNS zone/VNet link/private endpoint is removed from the Mermaid diagram or tables in `docs/architecture/network-posture.md`.
* Validation evidence commands (Focused tier; `tools/rpi-checks.py` explicitly excluded):
  * `python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`
  * `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_network_posture.py`
  * `python3 -m ruff format --isolated --line-length 100 --check infra/tests`
  * `python3 -m mypy infra/tests/test_network_posture.py`

<!-- rpi:phase id=P01 -->
## P01: Author deterministic network-posture and secret-binding inventory contract

### Context

`infra/main.bicep`, `infra/modules/*.bicep`, and standalone `infra/*.bicep` define the Azure VNet, subnets, NSGs, private DNS zones, VNet links, 10 `Microsoft.Network/privateEndpoints` deployments, optional Front Door `sharedPrivateLinkResource`, bounded exercise exceptions, and Key Vault managed-identity secret references (`C1`–`C17`). Commit `252125ad2` (`#136`) placed general Bicep component discovery in `infra/scripts/bicep_inventory.py`, while `#142` placed secret rotation rules in `infra/secret-inventory.json`. A dedicated `infra/network-posture-inventory.json` bridges both contracts into one explicit network-posture and secret-binding manifest.

### Intent

Create `infra/network-posture-inventory.json` with deterministic schemas for VNet/subnets/NSGs, private DNS zones + VNet links, data-store private endpoints, exercise exceptions (with `owner` and `rationale`), and Container App Key Vault secret bindings.

### Boundaries

* Included: `infra/network-posture-inventory.json`.
* Excluded: Modifying Bicep infrastructure behavior (existing Bicep templates already enforce private endpoints, `guard.bicep` invariants, and Key Vault `keyVaultUrl` + `identity`).

### Likely Targets

* `infra/network-posture-inventory.json`: New canonical JSON contract.

### Dependencies

* None.

### Validation Expectations

* `python3 -m json.tool infra/network-posture-inventory.json > /dev/null` succeeds and `test_network_posture.py` validates every entry against compiled Bicep and `bicep_inventory.py`.

### Completion Evidence

* `infra/network-posture-inventory.json` exists on disk and encodes all subnets, NSGs, 14+1 DNS zones and VNet links, 10 private endpoints + optional Front Door shared private link, 7 owned exercise exceptions, and 4 Key Vault secret bindings (`2` on `ca-${prefix}-api`, `2` on `ca-resident-demo`).

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Create `infra/network-posture-inventory.json` covering all network primitives, data stores, exercise exceptions, and Key Vault secret bindings

#### Context

Grounded in `C4`–`C17`:
* VNet `vnet-${prefix}` (`10.40.0.0/16`) in `infra/modules/network.bicep` with subnets `snet-aca` (`10.40.0.0/23`, NSG `nsg-${prefix}-aca`, delegation `Microsoft.App/environments`), `snet-pe` (`10.40.4.0/24`, NSG `nsg-${prefix}-pe`, `privateEndpointNetworkPolicies: 'Enabled'`), and conditional `snet-aca-demo` (`10.40.6.0/23`, NSG `nsg-${prefix}-aca-demo`, delegation `Microsoft.App/environments`, condition `demoDirectIngress`), plus standalone temporary child subnet `issue360-publisher-20261019-subnet` (`10.40.8.0/28`) in `infra/private-proof-publisher.bicep`.
* 14 static private DNS zones + `link-${prefix}` VNet links (`registrationEnabled: false`) in `infra/modules/network.bicep` (`sql`, `blob`, `queue`, `vault`, `acr`, `cognitive`, `openai`, `aiServices`, `monitor`, `oms`, `ods`, `agentsvc`, `iotHub`, `iotHubEndpoint`) plus conditional 15th internal ACA `defaultDomain` private DNS zone + `link-${prefix}` VNet link in `infra/modules/envDns.bicep` (`!externalEnvironment`).
* 10 `privateEndpoint.bicep` module instances in `snet-pe` (using exact Bicep symbolic names and compiled ARM deployment names per `PC-003`):
  1. `sql` (`Microsoft.Sql/servers`, `infra/modules/sql.bicep`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-${name}'`, `groupId: 'sqlServer'`, `dnsZoneKeys: ['sql']`, `publicNetworkAccess: 'Disabled'` unconditional).
  2. `storage-blob` (`Microsoft.Storage/storageAccounts`, `infra/modules/storage.bicep`, `peSymbolicName: 'blobEndpoint'`, `peDeploymentName: 'pe-${name}-blob'`, `groupId: 'blob'`, `dnsZoneKeys: ['blob']`, `allowSharedKeyAccess: false`).
  3. `storage-queue` (`Microsoft.Storage/storageAccounts`, `infra/modules/storage.bicep`, `peSymbolicName: 'queueEndpoint'`, `peDeploymentName: 'pe-${name}-queue'`, `groupId: 'queue'`, `dnsZoneKeys: ['queue']`, `allowSharedKeyAccess: false`).
  4. `auth-token-store-blob` (`Microsoft.Storage/storageAccounts`, `infra/modules/authTokenStore.bicep`, conditional `enableEntraTokenStore`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-${name}-blob'`, `groupId: 'blob'`, `dnsZoneKeys: ['blob']`, `allowSharedKeyAccess: false`).
  5. `keyvault` (`Microsoft.KeyVault/vaults`, `infra/modules/keyvault.bicep`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-${name}'`, `groupId: 'vault'`, `dnsZoneKeys: ['vault']`, `enableRbacAuthorization: true`).
  6. `acr` (`Microsoft.ContainerRegistry/registries`, `infra/modules/registry.bicep`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-${name}'`, `groupId: 'registry'`, `dnsZoneKeys: ['acr']`, `adminUserEnabled: false`).
  7. `foundry` (`Microsoft.CognitiveServices/accounts`, `infra/modules/foundry.bicep`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-${name}'`, `groupId: 'account'`, `dnsZoneKeys: ['cognitive', 'openai', 'aiServices']`, `disableLocalAuth: true`).
  8. `iothub` (`Microsoft.Devices/IotHubs`, `infra/modules/iothub.bicep`, `peSymbolicName: 'hubEndpoint'`, `peDeploymentName: 'pe-${name}'`, `groupId: 'iotHub'`, `dnsZoneKeys: ['iotHub', 'iotHubEndpoint']`, `disableLocalAuth: true`).
  9. `telemetry-eventhub` (`Microsoft.EventHub/namespaces`, `infra/modules/iothub.bicep`, `peSymbolicName: 'telemetryEndpoint'`, `peDeploymentName: 'pe-eh-${name}'`, `groupId: 'namespace'`, `dnsZoneKeys: ['iotHubEndpoint']`, `publicNetworkAccess: 'Disabled'` unconditional, `trustedServiceAccessEnabled: true`, `disableLocalAuth: true`).
  10. `ampls` (`microsoft.insights/privateLinkScopes`, `infra/modules/monitoring.bicep`, `peSymbolicName: 'endpoint'`, `peDeploymentName: 'pe-ampls'`, `groupId: 'azuremonitor'`, `dnsZoneKeys: ['monitor', 'oms', 'ods', 'agentsvc', 'blob']`, covering `scopedResources` `Microsoft.OperationalInsights/workspaces` and `Microsoft.Insights/components` in `infra/modules/monitoring.bicep` with `PrivateOnly` ingestion/query per `PC-001`).
  * Plus optional edge private origin link (`Microsoft.Cdn/profiles/originGroups/origins` in `infra/modules/edge.bicep`, called conditionally from `infra/main.bicep` when `enablePublicEdge` and from standalone `infra/public-edge-existing.bicep`, `sharedPrivateLinkResource` `groupId: 'managedEnvironments'`).
* `existingStoreReferences` across the 30 `.bicep` files (`PC-001`): explicit mapping of every `existing` data-store declaration (`infra/modules/authTokenStore.bicep` `existing` Key Vault + ACR; `infra/staff-initializer-rbac.bicep` `existing` Storage Account; `infra/public-edge-existing.bicep` `existing` Log Analytics Workspace; `infra/iot-hub-live.bicep` `existing` IoT Hub + Log Analytics Workspace; `infra/resident-demo.bicep` `existing` Key Vault + ACR) to its private-endpoint-backed store or bounded exercise exception.
* Bounded exercise exceptions (each with `id`, `storeCategory`, `bicepPath`, `resourceType`, `owner: "Juan Manuel Servera (@jmservera)"`, `rationale`, `compensatingControls`):
  1. `NP-EX-001`: Development-profile `allowPublicNetworkAccess` opt-in (`infra/main.bicep`, aligned with `EX-001` in `infra/policy-exceptions.json`: defaults `false` in all 3 `infra/main*.bicepparam` files, forbidden in `production`/`pilot`/`demoDirectIngress` by `guard.bicep`, never applies to SQL or Event Hub).
  2. `NP-EX-002`: Standalone opt-in resident assistant OpenAI (`infra/resident-assistant.bicep`, `Microsoft.CognitiveServices/accounts`, `swedencentral`, `enabled = false` default, outside core UK/private boundary, `disableLocalAuth: true`, USD20 SQL budget cap).
  3. `NP-EX-003`: Standalone live IoT Hub consumer-group/diagnostics child reconciliation (`infra/iot-hub-live.bicep`, `Microsoft.Devices/IotHubs` `existing` + `Microsoft.OperationalInsights/workspaces` `existing`, attaches `api-consumer` + metrics-only diagnostics to existing private-endpoint-backed exercise hub `iot-cutover-test-rzsrg` without hub PUT).
  4. `NP-EX-004`: Standalone synthetic telemetry job certificate `AzureFile` share (`infra/live-simulator-job.bicep` and `infra/live-receiver-job.bicep`, existing ACA environment storage `certStorageName`, mounted read-only `ro` for synthetic device X.509 certs).
  5. `NP-EX-005`: Standalone resident showcase Container App external dependencies (`infra/resident-demo.bicep`, references pre-provisioned private ACA environment, existing Key Vault `keyVaultUrl` + user-assigned MI, existing private ACR, and showcase SQL FQDN with `ZF_SQL_AUTH: 'msi'`).
  6. `NP-EX-006`: Opt-in public simulation lane volatile scratch SQLite (`infra/modules/containerapps.bicep`, `enablePublicSimulationLane = false` default, replica-local `EmptyDir` `/state/public-simulation/store.sqlite`, non-durable synthetic exercise state).
  7. `NP-EX-007`: Unimplemented SharePoint evidence-store topology selector (`infra/main.bicep`, `evidenceStore == 'sharepoint'`, external Microsoft Graph `Sites.Selected` SaaS boundary when selected; default is private `blob`).
* Secret bindings (`keyVaultUrl` + user-assigned `identity`, recording both `containerSecretName` and `keyVaultSecretName` plus gating conditions per `PC-004`):
  * `ca-${prefix}-api` (`infra/modules/containerapps.bicep`): `containerSecretName` / `keyVaultSecretName` `entra-client-secret` (via `entraClientSecretName`, conditional on `requireEntraAuth && entraCredentialStore == 'keyVault'`, consumed by `clientSecretSettingName` in `authConfigs`) and `entra-token-store-sas` (conditional on `enableEntraTokenStore`, consumed by `secretRef` in `AUTH_TOKEN_STORE_ROTATION` + `sasUrlSettingName` in `authConfigs`), both using `identityIds.api`.
  * `ca-resident-demo` (`infra/resident-demo.bicep`): `containerSecretName: 'demo-password-verifier'` -> `keyVaultSecretName: 'resident-demo-password-verifier'` (`secretRef` in `ZF_DEMO_PASSWORD_VERIFIER`) and `containerSecretName: 'demo-session-key'` -> `keyVaultSecretName: 'resident-demo-session-key'` (`secretRef` in `ZF_DEMO_SESSION_KEY`), both using `identity.id` and matching `infra/secret-inventory.json`.

#### Intent

Write `infra/network-posture-inventory.json` with clean, self-documenting keys so both humans and `infra/tests/test_network_posture.py` can audit every resource and exception deterministically.

#### Boundaries

* Included: `infra/network-posture-inventory.json`.
* Excluded: Hardcoding any live secret value, tenant ID, or subscription ID.

#### Likely Targets

* `infra/network-posture-inventory.json`: Create file.

#### Dependencies

* None.

#### Validation Expectations

* Valid JSON with complete schema checked in `P03-T01`.

#### Completion Evidence

* `infra/network-posture-inventory.json` created and verified against Bicep.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Synchronize architecture network-posture diagram and infrastructure docs

### Context

`docs/architecture/README.md` currently collapses VNet networking into one summary node `network["VNet / NSGs / private endpoints / DNS / AMPLS"]` (`line 234`) and says `"two subnets"` (`line 277`) (`C18`). Following the established companion-doc pattern in `docs/architecture/environment-region-quota-strategy.md` (`#137`) and `docs/architecture/resident-assistant-prototype.md`, creating `docs/architecture/network-posture.md` and linking/reconciling `docs/architecture/README.md` + `infra/README.md` gives reviewers and `test_network_posture.py` an exact, readable, machine-checkable Mermaid network diagram and specification without touching immutable Excalidraw hashes (`docs/architecture/update-architecture.mjs`).

### Intent

Publish `docs/architecture/network-posture.md` and reconcile `docs/architecture/README.md` and `infra/README.md` so every subnet, NSG, VNet link, private DNS zone, private endpoint, Key Vault secret flow, and exercise exception matches `infra/modules/network.bicep` and `infra/main.bicep`.

### Boundaries

* Included: `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`.
* Excluded: `docs/architecture/*.excalidraw`, `docs/capstone/source/diagrams/architecture/*`.

### Likely Targets

* `docs/architecture/network-posture.md`: Create canonical network-posture diagram and reference tables.
* `docs/architecture/README.md`: Link `network-posture.md` and update the subnet count description (`two base subnets plus conditional snet-aca-demo`).
* `infra/README.md`: Cross-reference `infra/network-posture-inventory.json` and `infra/tests/test_network_posture.py`.

### Dependencies

* `P01-T01` (`infra/network-posture-inventory.json` identifiers and labels).

### Validation Expectations

* Markdown follows AMA style rules (YAML frontmatter without duplicate H1, `*` unordered lists, plain ASCII punctuation, no em dashes, no bolded-prefix list items), relative links resolve, `node docs/architecture/update-architecture.mjs --check` continues to pass if checked, and `test_network_posture.py` verifies every subnet, DNS zone, VNet link, and private endpoint in both the Mermaid block and Markdown tables.

### Completion Evidence

* `docs/architecture/network-posture.md` created; `docs/architecture/README.md` and `infra/README.md` updated cleanly.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create `docs/architecture/network-posture.md` with Mermaid topology diagram and canonical tables

#### Context

AC-03 requires that every subnet, VNet link, private DNS zone, and private endpoint in `infra/modules/network.bicep` and `infra/main.bicep` matches the documented diagram and is checked by `infra/tests/test_network_posture.py`.

#### Intent

Write `docs/architecture/network-posture.md` containing:
1. YAML frontmatter (`title`, `description`, `ms.date: 2026-11-15`) with no duplicate `#` H1 heading.
2. A Mermaid `flowchart TB` network posture diagram containing explicit nodes and edges for:
   * `vnet-${prefix}` (`10.40.0.0/16`)
   * Subnets & NSGs: `snet-aca` (`10.40.0.0/23`, `nsg-${prefix}-aca`), `snet-pe` (`10.40.4.0/24`, `nsg-${prefix}-pe`), conditional `snet-aca-demo` (`10.40.6.0/23`, `nsg-${prefix}-aca-demo`)
   * All 14 static private DNS zones (`privatelink.database.windows.net`, `privatelink.blob.core.windows.net`, `privatelink.queue.core.windows.net`, `privatelink.vaultcore.azure.net`, `privatelink.azurecr.io`, `privatelink.cognitiveservices.azure.com`, `privatelink.openai.azure.com`, `privatelink.services.ai.azure.com`, `privatelink.monitor.azure.com`, `privatelink.oms.opinsights.azure.com`, `privatelink.ods.opinsights.azure.com`, `privatelink.agentsvc.azure-automation.net`, `privatelink.azure-devices.net`, `privatelink.servicebus.windows.net`) plus conditional 15th ACA internal `defaultDomain` private DNS zone (`envDns.bicep`), each linked via `link-${prefix}` (`virtualNetworkLinks`, `registrationEnabled: false`)
   * All 10 `privateEndpoint.bicep` resources in `snet-pe` (`sqlServer`, `blob` primary, `queue` primary, conditional `blob` auth token store, `vault`, `registry`, `account` Foundry, `iotHub`, `namespace` telemetry Event Hub, `azuremonitor` AMPLS) plus optional Front Door Premium `sharedPrivateLinkResource` (`managedEnvironments`)
   * Separate dashed boundary for outside-core / standalone exercise exceptions (`NP-EX-001`..`NP-EX-007`) and Key Vault user-assigned managed identity secret pull (`keyVaultUrl` + `identity` -> `secretRef`).
3. Canonical Markdown tables for Subnets & NSGs, Private DNS Zones & VNet Links, Data Store Private Endpoints, Key Vault Managed-Identity Secret Bindings, and Exercise Exceptions.

#### Boundaries

* Included: `docs/architecture/network-posture.md`.
* Excluded: `.copilot-tracking/` citations (never place tracking paths in docs or code).

#### Likely Targets

* `docs/architecture/network-posture.md`: Create file.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* Parsed and verified against Bicep + `network-posture-inventory.json` by `test_network_posture.py`; conforms to AMA Markdown style rules.

#### Completion Evidence

* `docs/architecture/network-posture.md` exists and passes all parity assertions.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile `docs/architecture/README.md` and `infra/README.md` references

#### Context

`docs/architecture/README.md:277` currently states `"Bicep declares VNet integration, two subnets, NSGs, private endpoints and DNS."` and lists companion architecture specs (`environment-region-quota-strategy.md`, `resident-assistant-prototype.md`). `infra/README.md` documents `infra/` contracts and test suites.

#### Intent

Update `docs/architecture/README.md` to link `network-posture.md` and accurately describe the two base subnets (`snet-aca`, `snet-pe`) plus conditional `snet-aca-demo`, 14 core + 1 conditional private DNS zones/VNet links, and 10 private endpoints; update `infra/README.md` to reference `infra/network-posture-inventory.json` and `infra/tests/test_network_posture.py`.

#### Boundaries

* Included: Surgical edits to `docs/architecture/README.md` and `infra/README.md`.
* Excluded: Rewriting unrelated sections or breaking existing `test_bicep_architecture_inventory_136.py` or `test_environment_quota_parameters.py` assertions on `infra/README.md` and `docs/architecture/README.md`.

#### Likely Targets

* `docs/architecture/README.md`: Add link to `network-posture.md` and update line 277 subnet wording.
* `infra/README.md`: Add concise pointer to `network-posture-inventory.json` and `test_network_posture.py`.

#### Dependencies

* `P02-T01`.

#### Validation Expectations

* Existing `test_bicep_architecture_inventory_136.py` and `test_environment_quota_parameters.py` continue to pass alongside `test_network_posture.py`.

#### Completion Evidence

* Both README files updated and verified by unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Implement offline network-posture, secret-store, and diagram-parity test suite and validate

### Context

`infra/tests/` uses Python `unittest`, compiles Bicep via `az bicep build --file ... --stdout`, formats with `ruff format --isolated --line-length 100`, lints with `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, and type-checks cleanly with `mypy` (`C3`).

### Intent

Create `infra/tests/test_network_posture.py` proving AC-01, AC-02, and AC-03 with both positive verification and fail-closed mutation tests, and run the Focused validation suite.

### Boundaries

* Included: `infra/tests/test_network_posture.py` and running Focused validation commands.
* Excluded: Running `tools/rpi-checks.py` (prohibited by caller instructions).

### Likely Targets

* `infra/tests/test_network_posture.py`: Create test suite.

### Dependencies

* `P01-T01`, `P02-T01`, `P02-T02`.

### Validation Expectations

* All `infra/tests/test_*.py` unit tests, `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy` pass with exit code `0`.

### Completion Evidence

* Command outputs recorded in `.copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Implement `infra/tests/test_network_posture.py` with compiled-Bicep, runtime secret-store, diagram-parity, and mutation tests

#### Context

`infra/tests/test_network_posture.py` must deterministically prove all three acceptance criteria and reject synthetic regressions:
1. **AC-01 (Data stores -> private endpoint or recorded exercise exception)**:
   * Scan all 30 `.bicep` files under `infra/` (`10` top-level `infra/*.bicep` and `20` `infra/modules/*.bicep`) using both `az bicep build --stdout` compiled ARM resources and `infra/scripts/bicep_inventory.py` loaded via `importlib.util.spec_from_file_location` (`scan_bicep_tree` + `REQUIRED_ARCHITECTURE_COMPONENTS`).
   * Identify every `(bicepPath, resourceType, mode)` stateful data-store / private-link target declaration (`Microsoft.Sql/servers`, `Microsoft.Storage/storageAccounts`, `Microsoft.KeyVault/vaults`, `Microsoft.ContainerRegistry/registries`, `Microsoft.Devices/IotHubs`, `Microsoft.EventHub/namespaces`, `Microsoft.CognitiveServices/accounts`, `microsoft.insights/privateLinkScopes`, `Microsoft.OperationalInsights/workspaces`, `Microsoft.Insights/components`) across all 30 Bicep templates.
   * Assert every discovered `(bicepPath, resourceType, mode)` tuple maps fail-closed in `infra/network-posture-inventory.json` to: (a) a verified `Microsoft.Network/privateEndpoints` deployment (`peSymbolicName` in Bicep source + `peDeploymentName` in compiled ARM) targeting `snet-pe` with exact `groupId`, `privateDnsZoneGroups` zone references, and hardened auth/public-access posture (`sql` and `telemetryNamespace` unconditional `publicNetworkAccess: 'Disabled'`; `guard.bicep` blocking `allowPublicNetworkAccess` in `production`, `pilot`, and `demoDirectIngress`; all 3 `infra/main*.bicepparam` files setting `allowPublicNetworkAccess == false`); (b) an AMPLS `scopedResources` binding (`monitoring.bicep` `workspaces` and `components` with `PrivateOnly` ingestion/query); (c) an `existingStoreReferences` entry tied to its private-endpoint-backed store or exception; OR (d) an explicit `exerciseExceptions` entry with non-empty `id`, `owner`, `rationale`, `bicepPath`, and `compensatingControls`.
   * Negative mutation checks: fail if an unmapped data store (`provisioned` or `existing`) appears in Bicep, if a `privateEndpoints` resource or DNS zone group is removed, or if an exercise exception has empty/placeholder `owner` or `rationale`.
2. **AC-02 (Secrets read from Key Vault via managed identity; none in code or app settings)**:
   * Inspect compiled ARM templates for every `Microsoft.App/containerApps`, `Microsoft.App/jobs`, and Web/Function `appSettings` across all `infra/*.bicep` and `infra/modules/*.bicep`, unwrapping both static arrays and ARM `concat`/`if` expressions on `configuration.secrets` and `env`.
   * Assert every secret object in `configuration.secrets` uses `keyVaultUrl` + non-empty user-assigned `identity` (never literal `value`), cross-checking both `containerSecretName` and `keyVaultSecretName` against `infra/network-posture-inventory.json` and `infra/secret-inventory.json`.
   * Compile all 4 `infra/*.bicepparam` files (`main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam`, `iot-hub-live.bicepparam`) via `az bicep build-params --stdout` and assert zero secret parameters or literal credential values.
   * Assert every secret-consuming `env` item or `authConfigs` field uses `secretRef` / `clientSecretSettingName` / `sasUrlSettingName`, and no `env`/`appSettings` entry with secret-sensitive names sets a literal `value`.
   * Assert zero `FORBIDDEN_KEY_FUNCTIONS` (`listKeys`, `listAccountSas`, `listCredentials`, `listSecrets`, `administratorLoginPassword`) appear anywhere in `infra/**/*.bicep`, and `@secure()` parameters (`teamsWebhookUrl`) never flow into Container Apps/Jobs `env` or `secrets`.
   * Inspect `src/` production Python packages (`src/*/src/**/*.py`) to confirm Key Vault access (`token_store.py`) uses `ManagedIdentityCredential`, Azure SQL (`mssqlstore.py`) defaults to `msi` and blocks password auth outside loopback CI containers, and zero hardcoded Key Vault secrets, connection-string passwords, or SAS tokens exist in `src/*/src/`.
   * Negative mutation checks: fail if a Container App secret uses `value: 'literal'`, omits `identity` or `keyVaultUrl`, puts a literal secret in `env` or `.bicepparam`, or invokes `listKeys`.
3. **AC-03 (Network diagram matches Bicep modules)**:
   * Extract VNet default CIDR (`10.40.0.0/16`), all subnets (`snet-aca` `10.40.0.0/23`, `snet-pe` `10.40.4.0/24`, conditional `snet-aca-demo` `10.40.6.0/23`), NSGs (`nsg-${prefix}-aca`, `nsg-${prefix}-pe`, conditional `nsg-${prefix}-aca-demo`), all 14 private DNS zones + 14 `link-${prefix}` VNet links from `infra/modules/network.bicep`, the conditional 15th ACA `defaultDomain` private DNS zone + `link-${prefix}` VNet link from `infra/modules/envDns.bicep`, and all 10 `privateEndpoint.bicep` module deployments + optional Front Door `sharedPrivateLinkResource` across `infra/main.bicep` and child modules.
   * Parse both the `mermaid` fenced block and Markdown tables in `docs/architecture/network-posture.md` (plus verify `docs/architecture/README.md` links `network-posture.md` and accurately states two base subnets plus conditional `snet-aca-demo`).
   * Assert exact set equality across Bicep <-> `infra/network-posture-inventory.json` <-> `docs/architecture/network-posture.md` Mermaid diagram <-> `docs/architecture/network-posture.md` tables.
   * Negative mutation checks: fail if any subnet, CIDR, VNet link, private DNS zone, or private endpoint is removed or renamed in the Mermaid diagram or tables.

#### Intent

Deliver complete, fast, readable, strictly typed tests in `infra/tests/test_network_posture.py` compiling each Bicep template once in `setUpClass`.

#### Boundaries

* Included: `infra/tests/test_network_posture.py`.
* Excluded: Network/cloud calls, `.copilot-tracking/` references in code/comments/docstrings.

#### Likely Targets

* `infra/tests/test_network_posture.py`: Create file.

#### Dependencies

* `P01-T01`, `P02-T01`, `P02-T02`.

#### Validation Expectations

* Passes `unittest`, `ruff check`, `ruff format --check`, and `mypy`.

#### Completion Evidence

* Zero failures across all positive and negative mutation tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute Focused validation suite (`unittest`, `ruff check`, `ruff format --check`, `mypy`)

#### Context

Caller prompt mandates Focused validation (`python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`, `ruff check`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests`) and explicitly forbids running `tools/rpi-checks.py`.

#### Intent

Run all Focused checks (`unittest` across `infra/tests`, `ruff check` and `ruff format --check` on `infra/tests/test_network_posture.py` plus directory-wide baseline observation, `mypy`, `bicep_inventory.py --check`, and `git diff --check`) and confirm zero errors on all changed and added files while keeping pre-existing untouched `infra/tests/*.py` and `.excalidraw` files unmodified.

#### Boundaries

* Included: Local read-only test/lint/format/typecheck commands.
* Excluded: `tools/rpi-checks.py`.

#### Likely Targets

* `infra/tests/test_network_posture.py`, `infra/network-posture-inventory.json`, `docs/architecture/network-posture.md`, `docs/architecture/README.md`, `infra/README.md`.

#### Dependencies

* `P03-T01`.

#### Validation Expectations

* Exit code `0` on every validation command.

#### Completion Evidence

* Validation outputs recorded in `.copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md`.

#### Unresolved Items

* None.

<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #119 Network Posture, Private Endpoints and Secret Store

## Metadata

* Task ID: issue-119-network-posture-2026-11-15
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver a deterministic, offline-verifiable network-posture, secret-store, and diagram-parity contract on branch `feat/infra-119-network-posture` (targeting `feat/demo-164-chat-grounding-provenance-0900` / PR #1641) validated at the Focused tier (`infra/tests` unit tests, `ruff check`, `ruff format --isolated --line-length 100 --check`, without running `tools/rpi-checks.py`, pushing, or opening a PR) and attributed with `Refs #119, #143, #142` (never `Closes #119`).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md (`C1` through `C20`), .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md, .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md, `infra/main.bicep`, `infra/*.bicep` (10 top-level Bicep files), `infra/modules/*.bicep` (20 module Bicep files), `infra/*.bicepparam` (4 parameter files), `infra/scripts/bicep_inventory.py`, `infra/secret-inventory.json`, `infra/policy-exceptions.json`, `infra/tests/test_bicep_architecture_inventory_136.py`, `infra/tests/test_secret_lifecycle.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/orchestrator/src/zava_forward/orchestrator/token_store.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `.github/workflows/src-ci.yml`, `docs/architecture/README.md`, `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/update-architecture.mjs`, and `infra/README.md`.
* Decisions, dependencies, and acceptance criteria considered:
  * AC1 / AC-01: Every data store (`SQL`, `Storage`, `Key Vault`, `ACR`, `IoT Hub` / `Event Hub`, plus adjacent stateful/telemetry/AI resources) across `infra/main.bicep`, `infra/modules/*.bicep`, standalone `infra/*.bicep`, and `infra/scripts/bicep_inventory.py` (`#136`) has either a Bicep private endpoint resource or an explicit documented exercise exception with owner and rationale in `infra/network-posture-inventory.json`, verified by `infra/tests/test_network_posture.py`.
  * AC2 / AC-02: Secrets are read from Key Vault through user-assigned managed identity (`keyVaultUrl` + `identity` and `secretRef` / Easy Auth setting names) with zero literal secrets or ARM key-listing calls in Bicep `appSettings`/`env`, `.bicepparam`, or `src/` runtime code, verified by `infra/tests/test_network_posture.py`.
  * AC3 / AC-03: `docs/architecture/` network posture documentation (`docs/architecture/network-posture.md` and `docs/architecture/README.md`) matches every subnet, VNet link, private DNS zone, and private endpoint in `infra/modules/network.bicep`, `infra/modules/envDns.bicep`, and `infra/main.bicep`, verified by `infra/tests/test_network_posture.py` without mutating historical `.excalidraw` hashes.
* Assessment boundary: Evaluates offline Bicep, parameter, Python runtime, inventory, test, and documentation accuracy against repository ground truth. Live Azure network traversal, DNS resolution inside a deployed VNet, and Front Door Shared Private Link approval remain outside offline scope as already recorded in the plan.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| FR-01 / AC-01 (data-store PE or owned exception) | Partial | Core 10 `privateEndpoint.bicep` modules and 7 exercise exceptions are identified, but `P01-T01` and `P03-T01` omit AMPLS-scoped monitoring resource types, standalone/module `existing` store declarations across all 30 `.bicep` files (`PC-001`), and use non-existent `peModuleName` identifiers (`PC-003`). |
| FR-02 / AC-02 (Key Vault MI secrets; zero literal secrets) | Partial | Covers Container Apps, `FORBIDDEN_KEY_FUNCTIONS`, `token_store.py`, and `mssqlstore.py`, but applies `allowPublicNetworkAccess = false` across all `.bicepparam` files including `infra/iot-hub-live.bicepparam` which has no such parameter (`PC-002`), and conflates Container App `secretName` with Key Vault secret names in `infra/secret-inventory.json` (`PC-004`). |
| FR-03 / AC-03 (Mermaid + Markdown network diagram parity) | Covered | `P02-T01` and `P02-T02` establish `docs/architecture/network-posture.md` and update `docs/architecture/README.md` (`two subnets` -> `snet-aca`, `snet-pe`, conditional `snet-aca-demo`, 14+1 DNS zones/links, 10 PEs + optional Front Door link) while preserving untouched `.excalidraw` hashes verified by `docs/architecture/update-architecture.mjs --check`. |
| NFR-01 / NFR-02 / AC-04 (offline Focused validation & commit policy) | Covered | `P03-T02` aligns with `.github/workflows/src-ci.yml` (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy`), excludes `tools/rpi-checks.py`, push, and PR creation, and uses `Refs #119, #143, #142`. |
| Research `C1` through `C20` | Partial | `C4` through `C20` accurately capture core network, secret, and runtime facts, but downstream plan/detail translation missed the 4th `.bicepparam` file (`iot-hub-live.bicepparam`), exact Bicep module symbolic names (`endpoint`, `blobEndpoint`, `queueEndpoint`, `hubEndpoint`, `telemetryEndpoint`), and `existing` store references across the full 30-file Bicep tree (`PC-001` through `PC-004`). |
| P01 / P01-T01 (`infra/network-posture-inventory.json`) | Partial | Needs direct schema tightening for `(bicepPath, resourceType, mode)` store resolution (`PC-001`), exact `peModuleName` / compiled deployment names (`PC-003`), and distinct `containerSecretName` vs `keyVaultSecretName` + conditional secret flags (`PC-004`). |
| P02 / P02-T01 / P02-T02 (`docs/architecture/` & `infra/README.md`) | Covered | Companion specification pattern matches `docs/architecture/environment-region-quota-strategy.md` and preserves `#136` structured tables in `infra/README.md`. Should reflect the corrected PE module/deployment identifiers from `P01-T01`. |
| P03 / P03-T01 / P03-T02 (`infra/tests/test_network_posture.py` & validation) | Partial | Test contract needs tightened discovery rules for AMPLS-scoped and `existing` data-store resources (`PC-001`), split `.bicepparam` assertions (`PC-002`), verified PE module/deployment names (`PC-003`), and unwrapped conditional ARM secret expressions + `keyVaultSecretName` parity (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The architectural approach, three-phase structure, Mermaid companion-doc strategy, and Focused validation boundary are well-grounded, but four concrete discrepancies between the phase details and actual repository files (`PC-001` through `PC-004`) would either break `infra/tests/test_network_posture.py` immediately against current Bicep/parameter sources or force the implementer to weaken fail-closed assertions. All four findings are factual planner corrections resolvable directly without user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Fail-closed AC-01 Bicep store scan omits AMPLS-scoped monitoring resources and `existing` data-store declarations across the 30-file Bicep tree

* Related IDs: FR-01, AC-01, P01-T01, P03-T01, C1, C13, C15
* Evidence: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md (`P01-T01`, `P03-T01`); .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md (`Sources`); infra/modules/monitoring.bicep; infra/staff-initializer-rbac.bicep; infra/public-edge-existing.bicep; infra/iot-hub-live.bicep; infra/resident-demo.bicep; infra/modules/authTokenStore.bicep; infra/scripts/bicep_inventory.py
* Concern: `P03-T01` specifies scanning every `.bicep` file under `infra/` (30 files total: 10 top-level `infra/*.bicep` and 20 `infra/modules/*.bicep`, rather than the "21 Bicep files" stated in plan `Sources`) for 10 stateful resource types (`Microsoft.Sql/servers`, `Microsoft.Storage/storageAccounts`, `Microsoft.KeyVault/vaults`, `Microsoft.ContainerRegistry/registries`, `Microsoft.Devices/IotHubs`, `Microsoft.EventHub/namespaces`, `Microsoft.CognitiveServices/accounts`, `microsoft.insights/privateLinkScopes`, `Microsoft.OperationalInsights/workspaces`, `Microsoft.Insights/components`) and requiring 100% fail-closed mapping in `infra/network-posture-inventory.json`. Two unmapped categories exist in current Bicep files:
  1. `infra/modules/monitoring.bicep` provisions `Microsoft.OperationalInsights/workspaces` (line 15) and `Microsoft.Insights/components` (line 31) with `publicNetworkAccessForIngestion: 'Disabled'` and `publicNetworkAccessForQuery: 'Disabled'` and binds them via `microsoft.insights/privateLinkScopes/scopedResources` (lines 53-67) into `ampls` rather than deploying direct per-resource `privateEndpoints`. `P01-T01` item 10 records only `microsoft.insights/privateLinkScopes`, leaving both scanned monitoring types without an inventory mapping.
  2. `bicep_inventory.parse_bicep_file()` separates `provisioned_types` from `existing_types`, whereas AST/ARM scanning across all 30 `.bicep` files encounters `existing` store declarations not listed in `P01-T01`'s 10 PE records or `NP-EX-001`..`NP-EX-007`: `infra/staff-initializer-rbac.bicep` (`existing` `Microsoft.Storage/storageAccounts`), `infra/public-edge-existing.bicep` (`existing` `Microsoft.OperationalInsights/workspaces`, plus a second caller of `modules/edge.bicep` alongside `infra/main.bicep`), `infra/iot-hub-live.bicep` (`existing` `Microsoft.OperationalInsights/workspaces` in addition to `Microsoft.Devices/IotHubs`), `infra/resident-demo.bicep` (`existing` `Microsoft.ContainerRegistry/registries` in addition to `Microsoft.KeyVault/vaults`), and `infra/modules/authTokenStore.bicep` (`existing` `Microsoft.KeyVault/vaults` and `Microsoft.ContainerRegistry/registries`).
* Impact: A strict `(bicepPath, resourceType)` fail-closed test in `test_network_posture.py` will fail against valid committed Bicep templates, or the implementer will silently bypass `existing` resources and monitoring resource types, weakening AC-01 coverage across standalone `infra/*.bicep`.
* Smallest useful change: Update `P01-T01` and `P03-T01` (and correct the 30-file `.bicep` count in plan `Sources`) so `infra/network-posture-inventory.json` explicitly maps (a) `Microsoft.OperationalInsights/workspaces` and `Microsoft.Insights/components` in `infra/modules/monitoring.bicep` as `scopedResources` covered by the `ampls` private endpoint, and (b) every `existing` store reference across standalone `infra/*.bicep` and `infra/modules/*.bicep` (`existingStoreReferences` or explicit `existing` entries referencing their private-endpoint-backed store or bounded exercise exception, plus recording both `infra/main.bicep` and `infra/public-edge-existing.bicep` as callers of `infra/modules/edge.bicep`). Also note loading `infra/scripts/bicep_inventory.py` via `importlib.util.spec_from_file_location` (matching `infra/tests/test_bicep_architecture_inventory_136.py`) so standalone `mypy` succeeds cleanly.
* Action owner: Planning parent
* Exact resolving evidence: Revised `P01-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md` and `Sources` in `.copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md` accounting for 100% of `(bicepPath, resourceType, mode)` occurrences across all 30 `.bicep` files.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Blanket `.bicepparam` assertion on `allowPublicNetworkAccess = false` fails on `infra/iot-hub-live.bicepparam`

* Related IDs: FR-02, AC-01, AC-02, P01-T01, P03-T01, C6
* Evidence: .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md (`FR-02`, `P03-T01`); .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md (`P01-T01`, `P03-T01`); infra/iot-hub-live.bicepparam; infra/main.bicepparam; infra/main.test.bicepparam; infra/main.pilot.example.bicepparam
* Concern: `FR-02` and `P03-T01` require asserting that "all `.bicepparam` files contain zero secrets and set `allowPublicNetworkAccess = false`". The repository has four committed `.bicepparam` files: `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`, and `infra/iot-hub-live.bicepparam`. Because `infra/iot-hub-live.bicepparam` targets `./iot-hub-live.bicep` (child consumer-group and diagnostics reconciliation on an existing IoT Hub), it has no `allowPublicNetworkAccess` parameter. Conversely, restricting parameter compilation solely to `infra/main*.bicepparam` (as plan `P03-T01` Expected result states) would omit `infra/iot-hub-live.bicepparam` from AC-02's zero-secret scan.
* Impact: Either `test_network_posture.py` raises an assertion/key error on `infra/iot-hub-live.bicepparam` during AC-01 checks or leaves `infra/iot-hub-live.bicepparam` unchecked for hardcoded secrets under AC-02.
* Smallest useful change: Update `FR-02`, `P01-T01`, and `P03-T01` to compile all four `infra/*.bicepparam` files via `az bicep build-params --stdout` for AC-02 zero-secret verification, while scoping the `allowPublicNetworkAccess == false` assertion to parameter files targeting `main.bicep` (`infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`).
* Action owner: Planning parent
* Exact resolving evidence: Updated `FR-02` and `P03-T01` in `.copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md` and `P01-T01`/`P03-T01` in `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md` explicitly distinguishing all 4 `infra/*.bicepparam` files (secret scan) from the 3 `infra/main*.bicepparam` files (`allowPublicNetworkAccess = false`).
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P01-T01` specifies non-existent `peModuleName` values (`pe`, `blobPe`, `queuePe`, `telemetryPe`) that contradict Bicep module and ARM deployment names

* Related IDs: FR-01, AC-01, AC-03, P01-T01, P02-T01, P03-T01, C7, C8, C9, C10, C11, C12, C13
* Evidence: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md (`P01-T01` items 1-10); infra/modules/sql.bicep; infra/modules/storage.bicep; infra/modules/authTokenStore.bicep; infra/modules/keyvault.bicep; infra/modules/registry.bicep; infra/modules/foundry.bicep; infra/modules/iothub.bicep; infra/modules/monitoring.bicep
* Concern: `FR-01` and `P01-T01` define `peModuleName` in `infra/network-posture-inventory.json` using values `pe`, `blobPe`, `queuePe`, and `telemetryPe`. None of those identifiers exist in the Bicep modules:
  * `infra/modules/sql.bicep:143`: symbolic `endpoint`, deployment `name: 'pe-${name}'`
  * `infra/modules/storage.bicep:177,189`: symbolic `blobEndpoint` (`name: 'pe-${name}-blob'`) and `queueEndpoint` (`name: 'pe-${name}-queue'`)
  * `infra/modules/authTokenStore.bicep:105`: symbolic `endpoint`, deployment `name: 'pe-${name}-blob'`
  * `infra/modules/keyvault.bicep:60`: symbolic `endpoint`, deployment `name: 'pe-${name}'`
  * `infra/modules/registry.bicep:55`: symbolic `endpoint`, deployment `name: 'pe-${name}'`
  * `infra/modules/foundry.bicep:99`: symbolic `endpoint`, deployment `name: 'pe-${name}'`
  * `infra/modules/iothub.bicep:189,201`: symbolic `hubEndpoint` (`name: 'pe-${name}'`) and `telemetryEndpoint` (`name: 'pe-eh-${name}'`)
  * `infra/modules/monitoring.bicep:69`: symbolic `endpoint`, deployment `name: 'pe-ampls'`
  In addition, standard `az bicep build --stdout` emits `Microsoft.Resources/deployments` resources keyed by ARM `name` expressions (`[format('pe-{0}', parameters('name'))]`, `'pe-ampls'`, etc.) rather than Bicep symbolic names.
* Impact: Recording fabricated `peModuleName` strings in `infra/network-posture-inventory.json` and `docs/architecture/network-posture.md` introduces immediate documentation-to-Bicep drift or forces `test_network_posture.py` to skip verifying `peModuleName`.
* Smallest useful change: Replace the invented `peModuleName` values in `P01-T01` with the exact Bicep module symbolic names (`endpoint`, `blobEndpoint`, `queueEndpoint`, `hubEndpoint`, `telemetryEndpoint`) alongside their compiled ARM deployment name patterns (`pe-${name}`, `pe-${name}-blob`, `pe-${name}-queue`, `pe-eh-${name}`, `pe-ampls`), and require `P03-T01` to assert both against the Bicep module source and compiled `Microsoft.Resources/deployments` entry.
* Action owner: Planning parent
* Exact resolving evidence: Updated `P01-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md` using the exact symbolic and deployment names from the eight `privateEndpoint.bicep`-calling modules.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `P01-T01` secret-binding specification conflates Container App `secretName` with Key Vault secret names in `infra/secret-inventory.json` and omits conditional ARM secret expressions

* Related IDs: FR-02, AC-02, P01-T01, P03-T01, C2, C16, C17
* Evidence: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md (`P01-T01`, `P03-T01`); infra/secret-inventory.json; infra/resident-demo.bicep; infra/modules/containerapps.bicep
* Concern: `P03-T01` requires cross-checking Container App `configuration.secrets` against both `infra/network-posture-inventory.json` and `infra/secret-inventory.json`. In `infra/resident-demo.bicep` (lines 34-35, 118-119), the Container App `configuration.secrets[].name` values are `demo-password-verifier` and `demo-session-key`, while their `keyVaultUrl` targets Key Vault secret names `resident-demo-password-verifier` and `resident-demo-session-key` (matching `infra/secret-inventory.json`). `P01-T01` lists only `demo-password-verifier` and `demo-session-key` without a separate `keyVaultSecretName` field. Furthermore, in `infra/modules/containerapps.bicep` (lines 65, 146-163), `configuration.secrets` compiles to an ARM `concat(if(...), if(...))` expression because `entraClientSecretName` (default `entra-client-secret`) is conditional on `requireEntraAuth && entraCredentialStore == 'keyVault'` (`entraCredentialStore == 'app'` uses app credentials without a Key Vault secret) and `entra-token-store-sas` is conditional on `enableEntraTokenStore`.
* Impact: Without distinct `containerSecretName` and `keyVaultSecretName` fields and explicit handling for ARM `concat`/`if` expressions on `configuration.secrets`, `test_network_posture.py` will either fail cross-checking `resident-demo.bicep` against `infra/secret-inventory.json` or fail to parse `containerapps.bicep`'s compiled `configuration.secrets` expression.
* Smallest useful change: Update `P01-T01` so each secret-binding entry records both `containerSecretName` and `keyVaultSecretName` (mapping `demo-password-verifier` -> `resident-demo-password-verifier` and `demo-session-key` -> `resident-demo-session-key`, plus `entraClientSecretName` default `entra-client-secret` gated by `requireEntraAuth && entraCredentialStore == 'keyVault'` and `entra-token-store-sas` gated by `enableEntraTokenStore`), and note in `P03-T01` that `test_network_posture.py` must inspect both static list items and ARM `concat`/`if` secret objects in compiled `configuration.secrets`.
* Action owner: Planning parent
* Exact resolving evidence: Updated `P01-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md` specifying `containerSecretName`, `keyVaultSecretName`, gating conditions, and compiled ARM expression inspection.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Strong architectural pattern choice: Adding `docs/architecture/network-posture.md` as a machine-parsed Mermaid + Markdown companion specification and updating `docs/architecture/README.md` (`two subnets` -> two base subnets plus conditional `snet-aca-demo`) mirrors `docs/architecture/environment-region-quota-strategy.md` (`#137`) while preserving immutable historical `.excalidraw` hashes verified by `docs/architecture/update-architecture.mjs --check`.
* Preserves existing `#136` and `#142` contracts: `P02-T02` explicitly protects the structured Markdown tables in `infra/README.md` parsed by `infra/scripts/bicep_inventory.py` (`test_bicep_architecture_inventory_136.py`), and `P03-T01` cross-checks rather than duplicates `infra/secret-inventory.json` (`test_secret_lifecycle.py`).
* Honest tracker attribution and governance alignment: Explicitly records `Refs #119, #143, #142` (never `Closes #119`) because GitHub `#119` tracks map tiles while `#143` and `#142` own private networking and secret lifecycle.
* Accepted residual risk: Offline Bicep compilation and AST/Markdown parity tests prove template topology, guards, and managed-identity secret wiring, not live Azure VNet DNS resolution or Front Door Shared Private Link approval (explicitly scoped out as non-goals and follow-up items).

## Questions or Blocking Evidence Gaps

* None. All four findings are fully resolved by existing repository files already within the supplied boundary; no user clarification or additional research cycle is required.

## Limitations

* Critique is bounded to offline static inspection of `.copilot-tracking/` artifacts, `infra/`, `src/`, `.github/workflows/src-ci.yml`, and `docs/architecture/`; no live Azure CLI control-plane queries or test executions were needed to verify the plan claims.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md` and `.copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md` to incorporate `PC-001` through `PC-004`, mark the critique disposition resolved, and finalize the plan for implementation without running a second critique pass.
* User response required: No

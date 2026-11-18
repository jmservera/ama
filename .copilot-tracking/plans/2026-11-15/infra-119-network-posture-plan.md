<!-- markdownlint-disable-file -->
# RPI Plan: Issue #119 Network Posture, Private Endpoints and Secret Store

## Task Metadata

* Task ID: issue-119-network-posture-2026-11-15
* Task slug: infra-119-network-posture
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/infra-119-network-posture-plan-critique.md

## Executive Summary

This plan delivers a deterministic, offline-verifiable network-posture and secret-store contract for the Zava Forward Azure infrastructure Bicep codebase and architecture documentation on branch `feat/infra-119-network-posture`. It introduces `infra/network-posture-inventory.json` as the machine-readable source of truth for data-store private endpoints, bounded exercise exceptions, VNet subnets, NSGs, private DNS zones, VNet links, and Key Vault managed-identity secret references; synchronizes `docs/architecture/` (`docs/architecture/network-posture.md` and `docs/architecture/README.md`) plus `infra/README.md` with the exact Bicep topology; and proves all three acceptance criteria plus fail-closed negative mutations in `infra/tests/test_network_posture.py`.

### User Decisions and Requirements Highlights

* Prove every data store (`SQL`, `Storage`, `Key Vault`, `ACR`, `IoT Hub` / `Event Hub`, plus adjacent stateful/model/telemetry stores) has either a Bicep private endpoint resource or an explicit documented exercise exception with owner and rationale (`infra/network-posture-inventory.json` + `infra/tests/test_network_posture.py`).
* Prove secrets are read from Key Vault through user-assigned managed identity (`keyVaultUrl` + `identity` and `secretRef` / Easy Auth setting references) with zero literal secret values in Bicep `appSettings`/`env`, `.bicepparam`, or runtime Python code (`infra/tests/test_network_posture.py`).
* Synchronize `docs/architecture/` network posture documentation so every subnet, VNet link, private DNS zone, and private endpoint in `infra/modules/network.bicep` and `infra/main.bicep` matches the documented diagram and tables and is verified by `infra/tests/test_network_posture.py`.
* Validate at the Focused tier (`python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`, `ruff check`, `python3 -m ruff format --isolated --line-length 100 --check infra/tests`), explicitly excluding `tools/rpi-checks.py`, remote push, and PR creation.

### What You May Not Know

* **Architecture inventory cross-check (`#136`)**: Commit `252125ad2` implemented the Bicep architecture inventory in `infra/scripts/bicep_inventory.py` (`REQUIRED_ARCHITECTURE_COMPONENTS` and `scan_bicep_tree`) rather than a standalone `infra/bicep-architecture-inventory.json` file (`C1`). `test_network_posture.py` cross-checks `infra/network-posture-inventory.json` against both `az bicep build` compiled ARM templates and `bicep_inventory.py`'s `scan_bicep_tree()` so no new Bicep store can bypass either contract.
* **Subnets and conditional DNS zones**: `docs/architecture/README.md` currently mentions `"two subnets"` (`C18`), whereas `infra/modules/network.bicep` defines **two base subnets** (`snet-aca` `10.40.0.0/23`, `snet-pe` `10.40.4.0/24`) plus a **conditional third subnet** (`snet-aca-demo` `10.40.6.0/23` when `demoDirectIngress` is true) and **14 core private DNS zones + VNet links**, complemented by a **conditional 15th private DNS zone + VNet link** in `infra/modules/envDns.bicep` (`C4`, `C5`).
* **Honest tracker attribution**: On GitHub, `#119` is titled `"Licensed map tile provider and accessible map alternative"`, while `#143` and `#142` hold private networking and Key Vault secret lifecycle (`C1`). Following AMA repository commit policy, commits and artifacts use `Refs #119, #143, #142` and never `Closes #119`.

### Unresolved Decisions or Blockers

* None. All evidence required for planning is verified in `.copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md` (`C1`–`C20`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Work in worktree `/home/azureuser/source/ama-demo-wt/feat-119-network-posture` on branch `feat/infra-119-network-posture` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641) (caller prompt).
* Write dated RPI tracking artifacts under `.copilot-tracking/research/2026-11-15/`, `.copilot-tracking/plans/2026-11-15/`, `.copilot-tracking/details/2026-11-15/`, `.copilot-tracking/changes/2026-11-15/`, `.copilot-tracking/reviews/2026-11-15/`, and `.copilot-tracking/reviews/logs/2026-11-15/` (caller prompt).
* Add a deterministic network-posture contract (`infra/network-posture-inventory.json` + `infra/tests/test_network_posture.py`) verifying every data store (`SQL`, `Storage`, `Key Vault`, `ACR`, `IoT Hub` / `Event Hub`) across `infra/main.bicep`, `infra/modules/*.bicep`, standalone `infra/*.bicep`, and the `#136` Bicep architecture inventory (`infra/scripts/bicep_inventory.py`) has either a Bicep private endpoint resource or an explicit documented exercise exception with owner and rationale (caller prompt AC1; research `C1`, `C6`–`C15`).
* Verify in `infra/tests/test_network_posture.py` that Container Apps and modules read secrets from Key Vault via user-assigned managed identity (`keyVaultUrl` + `identity` and `secretRef` / Easy Auth setting references) with no literal secret values in Bicep `appSettings`/`env`, `.bicepparam`, or runtime code (caller prompt AC2; research `C2`, `C16`, `C17`, `C19`, `C20`).
* Verify or update `docs/architecture/` network posture documentation so every subnet, VNet link, private DNS zone, and private endpoint in `infra/modules/network.bicep` and `infra/main.bicep` matches the documented diagram and is checked by `infra/tests/test_network_posture.py` (caller prompt AC3; research `C4`–`C13`, `C18`).
* Run Focused validation (`python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`, `ruff check`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests`); do NOT run `tools/rpi-checks.py` (caller prompt).
* Commit all changes and `.copilot-tracking/` RPI artifacts locally on `feat/infra-119-network-posture` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and `Refs #119, #143, #142` (never `Closes #119`), without pushing or opening a PR (caller prompt; `.github/copilot-instructions.md`).

## Goals

* Establish a single fail-closed, machine-readable network-posture and secret-binding inventory (`infra/network-posture-inventory.json`) covering every stateful resource and network primitive in `infra/`.
* Synchronize `docs/architecture/` (`docs/architecture/network-posture.md` and `docs/architecture/README.md`) and `infra/README.md` with the exact Bicep VNet, subnets, NSGs, private DNS zones, VNet links, private endpoints, managed-identity Key Vault secret flows, and exercise exceptions.
* Prove AC1, AC2, and AC3 plus negative mutation detection in `infra/tests/test_network_posture.py` using compiled ARM output, `bicep_inventory.py` AST scanning, runtime code checks, and Markdown/Mermaid diagram parity assertions.

## Scope and Non-Goals

### In Scope

* Creating `infra/network-posture-inventory.json`.
* Creating `docs/architecture/network-posture.md` and reconciling `docs/architecture/README.md` and `infra/README.md`.
* Creating `infra/tests/test_network_posture.py` with positive contract assertions and negative fail-closed mutation tests.
* Running Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`) and committing locally on `feat/infra-119-network-posture`.

### Non-Goals

* Modifying `docs/architecture/*.excalidraw` historical continuation canvases.
* Provisioning or mutating live Azure resources.
* Running `tools/rpi-checks.py`, pushing to GitHub, or opening/merging a pull request.
* Closing GitHub issue `#119`, `#142`, `#143`, or `#118`.

## Functional Requirements

* FR-01: `infra/network-posture-inventory.json` catalogs every stateful data store and private-link endpoint across all 30 Bicep files (`10` top-level `infra/*.bicep` and `20` `infra/modules/*.bicep`), recording either its Bicep private endpoint (`module`, `peSymbolicName`, `peDeploymentName`, `groupId`, `dnsZoneKeys`, `publicNetworkAccess`, `subnet`, plus AMPLS `scopedResources` for `Microsoft.OperationalInsights/workspaces` and `Microsoft.Insights/components`), an `existingStoreReferences` entry mapping `existing` resource declarations to their private-endpoint-backed store or bounded exercise exception, or an explicit `exerciseException` (`id`, `owner`, `rationale`, `scope`, `compensatingControls`).
  * Observable acceptance criteria: `infra/tests/test_network_posture.py` discovers all `(bicepPath, resourceType, mode)` data-store declarations across all 30 `infra/**/*.bicep` files via compiled ARM and `bicep_inventory.scan_bicep_tree()`, confirms 100% fail-closed coverage in `infra/network-posture-inventory.json`, verifies exact Bicep symbolic and compiled ARM deployment names, and rejects unmapped stores, missing `privateEndpoint.bicep` resources, or exceptions lacking non-empty `owner` or `rationale`.
* FR-02: `infra/network-posture-inventory.json` and `infra/tests/test_network_posture.py` verify managed-identity Key Vault secret access across all Bicep templates, all 4 `infra/*.bicepparam` files, and `src/` runtime modules.
  * Observable acceptance criteria: `infra/tests/test_network_posture.py` proves every Container App/Job `configuration.secrets` entry (unwrapping both static arrays and conditional ARM `concat`/`if` expressions) defines `keyVaultUrl` + user-assigned `identity` (never literal `value`) with distinct `containerSecretName` and `keyVaultSecretName` matching `infra/secret-inventory.json`, every secret-bearing `env`/`appSettings` or Easy Auth setting uses `secretRef` / `clientSecretSettingName` / `sasUrlSettingName`, zero `FORBIDDEN_KEY_FUNCTIONS` (`listKeys`, `listAccountSas`, `listCredentials`, `listSecrets`, `administratorLoginPassword`) exist in any `infra/**/*.bicep`, all 4 `infra/*.bicepparam` files contain zero secrets while all 3 `infra/main*.bicepparam` files set `allowPublicNetworkAccess = false`, and `src/` Azure secret/data clients use `ManagedIdentityCredential` (`ZF_SQL_AUTH='msi'` in Azure).
* FR-03: `docs/architecture/network-posture.md` (and updated `docs/architecture/README.md`) renders a Mermaid network diagram and structured tables matching every subnet, NSG, VNet link, private DNS zone, private endpoint, and exercise exception in `infra/modules/network.bicep`, `infra/modules/envDns.bicep`, and `infra/main.bicep`.
  * Observable acceptance criteria: `infra/tests/test_network_posture.py` parses both the Mermaid flowchart block and Markdown tables in `docs/architecture/network-posture.md` and asserts exact 1:1 parity against compiled `network.bicep`, `envDns.bicep`, `main.bicep`, and `infra/network-posture-inventory.json`.

## Non-Functional Requirements

* NFR-01: Offline determinism and execution speed.
  * Objective threshold or evaluation condition: `python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` completes offline with zero network calls and zero failures.
  * Operating condition or verification approach, if needed: Local Linux environment with `python3` and `az bicep` CLI installed.
  * Observable acceptance criteria: Full `infra/tests` suite passes deterministically in a clean local shell.
* NFR-02: Static lint, formatting, and type-check conformance matching `.github/workflows/src-ci.yml`.
  * Objective threshold or evaluation condition: Zero diagnostics from `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy`.
  * Observable acceptance criteria: `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_network_posture.py` and `python3 -m ruff format --isolated --line-length 100 --check infra/tests` exit `0`.

## Acceptance Criteria

* AC-01: Every data store (`SQL`, `Storage`, `Key Vault`, `ACR`, `IoT Hub` / `Event Hub`, plus `Auth Token Store`, `Foundry`, `AMPLS`, and standalone exercise resources) has either a verified Bicep private endpoint resource in `snet-pe` or an explicit documented exercise exception with non-empty `owner` and `rationale` in `infra/network-posture-inventory.json`, enforced with positive and negative mutation tests in `infra/tests/test_network_posture.py`.
* AC-02: Secrets are read from Key Vault through user-assigned managed identity (`keyVaultUrl` + `identity` -> `secretRef` / Easy Auth secret setting names); zero literal secrets or ARM key-listing functions exist in Bicep `appSettings`/`env`, `.bicepparam`, or `src/` runtime code, enforced with positive and negative mutation tests in `infra/tests/test_network_posture.py`.
* AC-03: `docs/architecture/network-posture.md` and `docs/architecture/README.md` accurately depict every VNet subnet (`snet-aca`, `snet-pe`, conditional `snet-aca-demo`), NSG, VNet link (`14` static + `1` conditional `envDns`), private DNS zone (`14` static + `1` conditional `envDns`), private endpoint (`10` `Microsoft.Network/privateEndpoints` + optional Front Door `sharedPrivateLinkResource`), and exercise exception, and `infra/tests/test_network_posture.py` verifies exact diagram-and-table parity and fails on synthetic drift mutations.
* AC-04: Focused validation commands exit `0` and all code, docs, and `.copilot-tracking/` artifacts are committed cleanly on `feat/infra-119-network-posture` without pushing.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-15/infra-119-network-posture-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md |
| Latest critique | .copilot-tracking/reviews/2026-11-15/infra-119-network-posture-plan-critique.md with Revise disposition (PC-001..PC-004 all resolved via direct planner corrections) |
| Relevant research | .copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation |
| Continuation context | Confirmed automatic RPI Agent parent return -> automatic transition to rpi-implement |

## Sources

* `.copilot-tracking/research/2026-11-15/infra-119-network-posture-research.md`: Cycle 1 codebase evidence `C1`–`C20` across the 30 Bicep files (`10` top-level `infra/*.bicep` and `20` `infra/modules/*.bicep`), 4 `infra/*.bicepparam` files, `bicep_inventory.py`, `secret-inventory.json`, `src/` runtime credential paths, and `docs/architecture/`.
* `infra/main.bicep` and `infra/modules/*.bicep`: Canonical Azure infrastructure definitions for VNet, subnets, NSGs, private DNS zones, VNet links, private endpoints, parameter guards, and Container Apps managed-identity Key Vault secrets.
* `infra/scripts/bicep_inventory.py`, `infra/secret-inventory.json`, `infra/policy-exceptions.json`: Existing `#136` architecture inventory, `#142` secret lifecycle inventory, and historical `EX-001` exception metadata.
* `docs/architecture/README.md` and `docs/architecture/environment-region-quota-strategy.md`: Existing architecture documentation index and companion specification pattern.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Author deterministic network-posture and secret-binding inventory contract

* Intent: Establish `infra/network-posture-inventory.json` as the canonical machine-readable contract for VNet subnets, NSGs, private DNS zones, VNet links, data-store private endpoints, owned exercise exceptions, and Key Vault managed-identity secret references.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create `infra/network-posture-inventory.json` covering all network primitives, data stores, exercise exceptions, and Key Vault secret bindings

* Requirement and evidence: FR-01, FR-02, FR-03; AC-01, AC-02, AC-03; research `C1`–`C17`.
* Expected result: `infra/network-posture-inventory.json` defines valid JSON for VNet (`vnet-${prefix}`, `10.40.0.0/16`), 3 subnets (`snet-aca`, `snet-pe`, conditional `snet-aca-demo`) + standalone `private-proof-publisher.bicep` child-subnet record, 3 NSGs, 14 core + 1 conditional (`envDns`) private DNS zones and `link-${prefix}` VNet links, all 10 `privateEndpoint.bicep` data-store endpoints + optional Front Door `sharedPrivateLinkResource`, all 7 bounded exercise exceptions with explicit non-empty `owner` and `rationale`, and all Container App Key Vault `keyVaultUrl` + user-assigned `identity` secret bindings.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Synchronize architecture network-posture diagram and infrastructure docs

* Intent: Author `docs/architecture/network-posture.md` with a 1:1 Bicep-accurate Mermaid network diagram and structured tables, and update `docs/architecture/README.md` and `infra/README.md` so documentation and Bicep agree without drift.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create `docs/architecture/network-posture.md` with Mermaid topology diagram and canonical tables

* Requirement and evidence: FR-03; AC-03; research `C4`–`C15`, `C18`; `.github/copilot-instructions.md` Markdown style rules (YAML frontmatter without redundant H1, `*` bullets, ASCII punctuation, no em dashes).
* Expected result: `docs/architecture/network-posture.md` contains YAML frontmatter (`title`, `description`, `ms.date: 2026-11-15`), a Mermaid `flowchart` showing every subnet (`snet-aca`, `snet-pe`, conditional `snet-aca-demo`), NSG, private DNS zone (`14` core + `1` conditional `envDns`), VNet link (`link-${prefix}`), private endpoint (`10` `privateEndpoints` + optional Front Door `sharedPrivateLinkResource`), and bounded outside-core exercise boundary, plus exact tables for subnets/NSGs, private DNS zones/VNet links, data-store private endpoints, managed-identity Key Vault secret bindings, and exercise exceptions.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile `docs/architecture/README.md` and `infra/README.md` references

* Requirement and evidence: FR-03; AC-03; research `C1`, `C18`.
* Expected result: `docs/architecture/README.md` links `docs/architecture/network-posture.md` alongside `environment-region-quota-strategy.md` and `resident-assistant-prototype.md` and updates the `"two subnets"` prose to reflect `snet-aca`, `snet-pe`, and conditional `snet-aca-demo`; `infra/README.md` documents `infra/network-posture-inventory.json` and `infra/tests/test_network_posture.py`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Implement offline network-posture, secret-store, and diagram-parity test suite and validate

* Intent: Implement `infra/tests/test_network_posture.py` with positive and fail-closed mutation tests proving AC-01, AC-02, and AC-03, and pass Focused-tier validation.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Implement `infra/tests/test_network_posture.py` with compiled-Bicep, runtime secret-store, diagram-parity, and mutation tests

* Requirement and evidence: FR-01, FR-02, FR-03, NFR-01, NFR-02; AC-01, AC-02, AC-03; research `C1`–`C20`; critique `PC-001`–`PC-004`.
* Expected result: `infra/tests/test_network_posture.py` compiles `infra/main.bicep`, `infra/modules/*.bicep`, standalone `infra/*.bicep`, and all 4 `infra/*.bicepparam` files, loads `infra/scripts/bicep_inventory.py` via `importlib.util.spec_from_file_location`, cross-checks `infra/secret-inventory.json`, asserts AC-01 (100% `(bicepPath, resourceType, mode)` data-store coverage via PE, AMPLS `scopedResources`, `existingStoreReferences`, or owned exception + `guard.bicep` and `infra/main*.bicepparam` `allowPublicNetworkAccess == false` invariants), AC-02 (Key Vault `keyVaultUrl` + `identity` unwrapping ARM `concat`/`if` expressions, distinct `containerSecretName` vs `keyVaultSecretName`, `secretRef`/Easy Auth bindings, zero literal secrets in all 4 `.bicepparam` files, zero `FORBIDDEN_KEY_FUNCTIONS`, and `src/` `ManagedIdentityCredential`/`msi` checks), and AC-03 (exact Mermaid + Markdown table parity in `docs/architecture/network-posture.md` and `docs/architecture/README.md` link/prose check), plus fail-closed negative mutation tests.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute Focused validation suite (`unittest`, `ruff check`, `ruff format --check`, `mypy`)

* Requirement and evidence: NFR-01, NFR-02; AC-04; `.github/workflows/src-ci.yml`.
* Expected result: `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` (`637` tests `OK`), `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_network_posture.py`, `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_network_posture.py` (with 12 pre-existing untouched `infra/tests/*.py` files left unedited per repository surgical-diff rules), `python3 -m mypy infra/tests/test_network_posture.py`, and `python3 infra/scripts/bicep_inventory.py --check` all exit `0` without invoking `tools/rpi-checks.py`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/infra-119-network-posture-phase-details.md

## Dependencies

* `az bicep` CLI (verified available in workspace environment) and Python 3.12 standard library (`unittest`, `json`, `re`, `subprocess`, `pathlib`) plus `ruff` for formatting/linting.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| Run 1 (`2026-11-15`): `PC-001` [High] — AMPLS-scoped monitoring types and `existing` store declarations across all 30 `.bicep` files | resolved | Revised `FR-01`, `Sources`, `P01-T01`, and `P03-T01` to catalog AMPLS `scopedResources` (`Microsoft.OperationalInsights/workspaces` and `Microsoft.Insights/components` in `monitoring.bicep`), all `existing` store declarations across the 30 `.bicep` files (`existingStoreReferences`), both callers of `edge.bicep` (`main.bicep` and `public-edge-existing.bicep`), and `importlib.util.spec_from_file_location` loading for `bicep_inventory.py`. |
| Run 1 (`2026-11-15`): `PC-002` [High] — `iot-hub-live.bicepparam` lacks `allowPublicNetworkAccess` | resolved | Revised `FR-02`, `P01-T01`, and `P03-T01` to compile all 4 `infra/*.bicepparam` files for AC-02 zero-secret verification while scoping `allowPublicNetworkAccess == false` to the 3 `infra/main*.bicepparam` files. |
| Run 1 (`2026-11-15`): `PC-003` [Medium] — Use exact Bicep symbolic and ARM deployment names for private endpoints | resolved | Replaced placeholder `peModuleName` values in `FR-01`, `P01-T01`, and `P03-T01` with exact Bicep symbolic names (`endpoint`, `blobEndpoint`, `queueEndpoint`, `hubEndpoint`, `telemetryEndpoint`) and compiled ARM deployment names (`pe-${name}`, `pe-${name}-blob`, `pe-${name}-queue`, `pe-eh-${name}`, `pe-ampls`). |
| Run 1 (`2026-11-15`): `PC-004` [Medium] — Distinguish `containerSecretName` vs `keyVaultSecretName` and unwrap conditional ARM secret expressions | resolved | Updated `FR-02`, `P01-T01`, and `P03-T01` to record both `containerSecretName` (`demo-password-verifier`, `demo-session-key`) and `keyVaultSecretName` (`resident-demo-password-verifier`, `resident-demo-session-key`) plus gating conditions and ARM `concat`/`if` secret expression inspection. |
| Residual risk (offline verification scope) | accepted_with_risk | Offline compiled-ARM, AST, runtime code, and diagram-parity tests do not execute live Azure VNet DNS queries or Front Door Shared Private Link approval; tracked in `## Follow-Up Items` under `#143` / `#118`. |

## Follow-Up Items

* Live Azure Front Door Premium Shared Private Link approval and VNet private DNS resolution smoke test: outside offline Bicep/documentation scope; tracked under `#143` / `#118` for owner-approved Azure deployment window.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/infra-119-network-posture-changes.md
* Ready phase or task: P01 (P01-T01 -> P02-T01 -> P02-T02 -> P03-T01 -> P03-T02)
* Remaining provisional question or blocker: none

---
description: "Primary evidence artifact for issue #136 Bicep architecture resource inventory, module delivery matrix, and from-empty reproducibility verification"
---
<!-- markdownlint-disable-file -->

# Task Research: infra-136-bicep-inventory

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | rpi-research (coordinated by RPI Agent)                                  |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md |

## Research Brief

* What to research: Map every proposed Azure and tenant/external resource across ADR 0001, ADR 0002, and ADR 0003 against `infra/main.bicep`, standalone Bicep entrypoints, and `infra/modules/*.bicep`; inspect `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and `infra/README.md` (including existing `Resource coverage register (issue 136, 2026-11-04)`, `Layout`, `Rebuild authoring`, and `From-empty rebuild`) to design a machine-verifiable architecture-to-Bicep inventory, current module delivery matrix, and from-empty reproducibility verifier plus unit tests.
* Why it matters: Proves the three unticked engineering Acceptance Criteria of Epic `#136`: (1) every resource in the proposed architecture is either in Bicep or recorded as intentionally manual with owner, (2) a from-empty deployment is reproducible from the repository without undocumented steps, and (3) delivered versus missing status for each module is kept current.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this automatic RPI loop, plus maintainers/reviewers inspecting `#136` evidence.
* Scope: `infra/main.bicep`, `infra/*.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/scripts/bicep_inventory.py` (new candidate), `infra/README.md`, `infra/tests/test_bicep_architecture_inventory_136.py` (new), `infra/tests/test_*.py`, and `docs/adrs/0001-azure-architecture.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`.
* Non-goals: Live Azure deployment, `az deployment group what-if`, modifying Bicep resource topology unless required, closing `#440` epic stabilization checkpoint or child feature human acceptance gates, or pushing to remote.
* Criteria: Every claim grounded in workspace-relative `path:line` codebase evidence; strict `ruff check`, `ruff format --line-length 100 --check`, `mypy --strict`, and `unittest` compatibility verified against existing `infra/` conventions.
* Requested outputs: Converged design and exact inventory/reproducibility contract ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | How do all proposed resources in ADRs 0001-0003 map to `infra/` Bicep modules or manual/external owned items, how do `deploy.py`/`pipeline.py`/`infra/README.md` define the from-empty deployment sequence and module status table, and what contract should `infra/scripts/bicep_inventory.py` and `infra/tests/test_bicep_architecture_inventory_136.py` enforce? |
| Codebase scope                   | `infra/`, `docs/adrs/`, `.github/workflows/src-ci.yml`                  |
| External scope                   | none                                                                    |
| Initial internal candidate areas | `infra/main.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/README.md`, `infra/tests/`, `docs/adrs/0001-*.md`, `0002-*.md`, `0003-*.md` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | caller-specified (bounded internal task with named source targets and focused validation tier) |
| Explicit limits / deadline       | Focused validation tier (`infra/tests` + `ruff` + `mypy`); do not push; leave clean frozen HEAD |
| Posture-specific completion basis | focused scope and materiality: all ADR 0001-0003 resources, all `infra/modules/*.bicep` files, and all from-empty rebuild steps inspected and reconciled |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | No `.copilot-tracking/` references in production code, comments, docstrings, or commit message body if prohibited by skill rules (commit tracking files cleanly per caller instruction) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches all workspace inputs | Defines `infra/` ruff/mypy/unittest rules, Focused validation tier, Markdown style, and ADR/evidence conventions | Selected: governs code quality, Markdown conventions, and honest evidence boundaries |
| Skill               | `python-foundational` / `architecture-diagrams` | Partial domain overlap | General Python practices / diagram rendering | Skipped: existing `infra/scripts/*.py` and `infra/tests/*.py` provide exact local stdlib + typing patterns; no diagram requested |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general research lane worker | Independent subagent lane artifact | Skipped (inline execution): tightly coupled cross-checking between ADRs, `infra/modules/*.bicep`, `infra/README.md`, and `deploy.py`/`pipeline.py` fits direct parallel reads with lower latency |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with explicit caller specification of files, script path (`infra/scripts/bicep_inventory.py`), test path (`infra/tests/test_bicep_architecture_inventory_136.py`), README updates, and validation commands | No interaction available or needed | Proceed with focused inline Cycle 1 across all named targets |
| Direction change | None required; Cycle 1 covered all named ADRs, Bicep templates, scripts, and CI rules | N/A | Keep focused scope |
| Convergence      | All five research questions answered with exact `path:line` evidence; single converged verifier/README/test contract established | Converged without ambiguity | Mark `Research disposition: executed` and `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: Inspect ADRs 0001-0003, `infra/*.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/README.md`, and existing `infra/tests/` to establish complete evidence for `bicep_inventory.py`, `infra/README.md` updates, and `test_bicep_architecture_inventory_136.py`.
* Assumptions: Existing `infra/README.md` already contains partial `#136` and `#148` sections (`Resource coverage register (issue 136, 2026-11-04)`, `Layout`, `Rebuild authoring and local rehearsal (Refs #148)`) that must be preserved/reconciled rather than duplicated or contradicted.
* Success criteria:
  * Every research question is answered with exact `path:line` evidence.
  * Every `infra/modules/*.bicep` file (all 20 modules) and top-level Bicep template is accounted for.
  * Every proposed resource in ADR 0001, ADR 0002, and ADR 0003 is mapped.
  * Every step in the from-empty deployment sequence is traced to scripts/templates.
  * Existing `infra/` typing (`mypy --strict`) and formatting (`ruff`, line-length 100) conventions are verified.

## Task Research Requests

* Explicit requests:
  1. Inspect `infra/main.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/README.md`, and `docs/adrs/0001-azure-architecture.md`, `0002-pilot-readiness-architecture.md`, `0003-journey-derived-capabilities-runtime-fit.md`.
  2. Design `infra/scripts/bicep_inventory.py` and `infra/README.md` updates covering the ADR-to-Bicep/manual-owner inventory, module delivery matrix, and reproducible from-empty deployment sequence.
  3. Design `infra/tests/test_bicep_architecture_inventory_136.py` proving all three unticked engineering ACs of `#136`.
* Inferred research questions:
  * What existing tests in `infra/tests/` already parse `infra/README.md`, `infra/main.bicep`, `deploy.py`, or `pipeline.py` (to avoid breaking existing assertions and to reuse parsing idioms)?
  * How is `mypy` configured for `infra/` in `pyproject.toml` or `.github/workflows/src-ci.yml`?
* Caller constraints and non-goals: Focused tier validation; commit locally with Copilot trailer; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow | Target the three engineering ACs of `#136` via `infra/scripts/bicep_inventory.py`, `infra/README.md`, and `infra/tests/test_bicep_architecture_inventory_136.py` | Caller prompt / Intake | Focuses Cycle 1 on static Bicep/ADR/README/script verification without live Azure calls |
| exclude | Do not push to remote; leave clean frozen HEAD | Caller prompt / Intake | Constrains final git operations in Implement/Review |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What resources and capabilities are proposed across ADR 0001, ADR 0002, and ADR 0003 (including conditional, deferred, and tenant/external items)? | breadth | H | answered |
| Q2 | What resources, modules, and entrypoints exist across `infra/main.bicep`, `infra/*.bicep`, and all 20 `infra/modules/*.bicep` files, and what is delivered vs missing/placeholder? | breadth | H | answered |
| Q3 | What does `infra/README.md` currently record in `Layout`, `Resource coverage register (issue 136, 2026-11-04)`, `Rebuild authoring`, and `From-empty rebuild`, and what gaps exist relative to `#136` ACs? | depth | H | answered |
| Q4 | How do `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and companion `infra/scripts/*` implement the from-empty deployment sequence, and are every stage and prerequisite backed by repository artifacts? | depth | H | answered |
| Q5 | What conventions, existing tests, and CI checks (`ruff`, `mypy --strict`, existing `infra/tests/test_*.py`) constrain new scripts, tests, and `infra/README.md` edits? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, GitHub issue `#136` body.
* Reused (verified) findings: Issue `#136` body (updated 2026-11-12) notes that IoT Hub and optional edge modules are wired in `infra/main.bicep`, parameter files exist, `.github/workflows/src-deploy.yml` defines image release/deployment, and worker jobs still use placeholder images by default.
* Superseded / stale: Earlier blanket missing-source claims prior to 2026-11-12; must still distinguish static Bicep definition from placeholder runtime images or unactivated optional flags.

## Cycle 1 Execution

### Wave 1: Wider (Architecture, Bicep Inventory, and Entrypoints)

* Executed inline across `docs/adrs/0001-azure-architecture.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `infra/*.bicep` (10 top-level entrypoints), and `infra/modules/*.bicep` (20 modules).
* Identified the complete set of proposed Azure, tenant, external, and explicitly deferred architecture components across ADRs 0001-0003 (`C1`, `C2`, `C3`):
  * **Core platform & compute (ADR 0001)**: Azure Container Apps Environment + `api` Container App + Container Apps Jobs (`agents`, `orchestrator`, `import`, `auth-renewal`, `ledger-verify`, `ranking-publish`); Azure Container Registry (Premium, private); User-Assigned Managed Identities (`api`, `agents`, `orchestrator`, `import`, conditional `auth-maintenance`).
  * **Data, storage, messaging & secrets (ADR 0001 + ADR 0003)**: Azure SQL logical server (Entra-only) + `retrofit` database with SQL Ledger (`enableLedger: true`), server audit, Defender alert policy, and PITR retention; Azure Storage Account (`StorageV2`) with 7 base blob containers (`evidence`, `reports`, `exports`, `audit-archive`, `ledger-digests`, `m365-fallback`, `staff-results`) + optional `ranking-archive`, WORM immutability policies, lifecycle management, and 4 Storage Queues (`agent-jobs`, `agent-jobs-poison`, `import-jobs`, `import-jobs-poison`); conditional Entra token-store Storage Account (`auth-tokens`); Azure Key Vault (RBAC, soft-delete, purge protection, `CanNotDelete` lock, expiry/denied alerts).
  * **AI & IoT (ADR 0001 + ADR 0003)**: Microsoft Foundry (`Microsoft.CognitiveServices/accounts` kind `AIServices`, project, `gpt-4.1-mini` and `gpt-4.1` model deployments, private endpoint); Azure IoT Hub (`B1` default, `enableIotHub`) + Standard Event Hubs namespace/hub/consumer group keyless egress adapter + private endpoints + transport budget (`Microsoft.Consumption/budgets`, conditional `enableIotTransportBudget`).
  * **Networking & observability (ADR 0001 + ADR 0002)**: VNet (`snet-aca`, `snet-pe`, optional `snet-aca-demo`), NSGs, 14 Private DNS zones + VNet links, reusable `privateEndpoint.bicep`; Log Analytics workspace, Application Insights, Azure Monitor Private Link Scope (AMPLS), Action Group (email + optional Teams webhook), operational workbook, and metric/scheduled-query alerts (`operationalMonitoring.bicep` + ledger digest alerts in `main.bicep`).
  * **Pilot readiness additions (ADR 0002)**: Optional public edge (`Microsoft.Cdn/profiles` Front Door Premium, endpoint, origin group, Private Link origin, route, managed TLS domain when `edgeCustomDomain` set, `Microsoft.Network/FrontDoorWebApplicationFirewallPolicies` WAF with `Microsoft_DefaultRuleSet` 2.1 + `Microsoft_BotManagerRuleSet` 1.1 + rate limit); subscription-scope governance (`infra/governance.bicep`: Azure Policy assignment in `DoNotEnforce` audit mode + conditional `Microsoft.Security/pricings` Defender plans when `enableDefenderPlans=true`); GIS tile configuration (`tileUrl` parameter wired to `api` container env `ZF_MAP_TILE_URL`, licensed provider deferred).
  * **Standalone/scoped operational & synthetic demo entrypoints (`infra/*.bicep`)**: `governance.bicep` (subscription), `main.bicep` (primary stack), `public-edge-existing.bicep` (standalone edge over existing CAE), `iot-hub-live.bicep` (scoped live IoT Hub proof), `staff-initializer-rbac.bicep` (scoped temporary staff-init RBAC), `live-receiver-job.bicep` & `live-simulator-job.bicep` (authored/compiled synthetic IoT jobs, not deployed by default), `private-proof-publisher.bicep` (ephemeral ACR publisher VM), `resident-demo.bicep` & `resident-assistant.bicep` (isolated synthetic resident showcase).
  * **Intentionally manual / external / deferred items requiring explicit owner mapping**:
    1. Resource group `ama` & pre-existing Entra SQL administrator security group/principal (`sqlAdminLogin` / `sqlAdminObjectId`) — manual prerequisite in Azure subscription/Entra (`C4`, `C11`); owner: `Juan Manuel Servera (@jmservera)`.
    2. Microsoft Entra ID tenant app registration, app roles, service principal assignment requirement, redirect URIs, and client credential (`infra/entra/app-registration.json`, reconciled via `infra/scripts/setup-entra.py`) — Graph/Entra tenant plane outside ARM Bicep (`C12`, `C15`); owner: `Juan Manuel Servera (@jmservera)`.
    3. Key Vault secret values (`entra-client-secret`, `entra-token-store-sas`, optional resident-demo secrets) and SQL contained database users (`create-sql-users.py` / `initialize-workbench-staff.py`) — data-plane provisioning out of band of ARM templates so secrets never enter Bicep state (`C13`, `C14`, `C16`); owner: `Juan Manuel Servera (@jmservera)`.
    4. Custom domain DNS records (`_dnsauth` TXT validation + CNAME to Front Door endpoint when `edgeCustomDomain` is set, plus custom hostname binding on direct ingress if applicable) — external DNS zone outside Azure resource group (`C2`, `C7`); owner: `Juan Manuel Servera (@jmservera)`.
    5. Microsoft 365 Teams channel & Workflows incoming webhook URL (`teamsWebhookUrl` secure parameter consumed by `monitoring.bicep`) — external M365 tenant configuration (`C1`, `C8`); owner: `Juan Manuel Servera (@jmservera)`.
    6. WORM immutability policy irreversible locking (`lockImmutabilityPolicy` on `audit-archive`, `ledger-digests`, `ranking-archive`) — intentionally unlocked in Bicep pending Legal/Housing retention sign-off (`C9`, `C11`); owner: `Juan Manuel Servera (@jmservera)`.
    7. Microsoft Defender for Cloud paid plan activation (`enableDefenderPlans=false` by default in `governance.bicep`, tracked in `infra/defender-decision.json`) & Azure Policy `Default` enforcement promotion — owner cost/governance gate (`C2`, `C17`); owner: `Juan Manuel Servera (@jmservera)`.
    8. IoT Hub per-device identities and X.509/SAS device credentials (`#185`, ADR 0003 decision 6) — IoT Hub data-plane registry managed outside ARM (`C3`, `C11`); owner: `Juan Manuel Servera (@jmservera)`.
    9. Licensed GIS/map tile provider subscription (`ADR 0002` decision 5: `tileUrl` parameter defaults to OSM demo tiles; Azure Maps / OS Data Hub PSGA key deferred until pilot traffic requires commercial SLA) — external commercial/public-sector licensing (`C2`, `C6`); owner: `Juan Manuel Servera (@jmservera)`.
    10. Controlled egress (`Azure Firewall` / `NAT Gateway`) for private outbound Microsoft Graph / SharePoint Online connector (`ADR 0001` Hybrid M365 Integration open item; `m365-fallback` Blob import active) and deferred Phase 2+ services (`Azure AI Search`, `Azure Document Intelligence`, `Azure Content Understanding`, `Azure Service Bus`, `Power BI Embedded`) — explicitly deferred in ADR 0001/0003 with owner `Juan Manuel Servera (@jmservera)` (`C1`, `C3`, `C11`).

### Wave 2: Deeper (README Register Drift, Module Delivery Status, and Reproducible Sequence)

* Inspected `infra/README.md` (`Layout` at `18-39`, `Rebuild authoring and local rehearsal` at `3694-3773`, `From-empty rebuild observed on 2026-10-12` at `3774-3851`, `Resource coverage register (issue 136, 2026-11-04)` at `3852-3890`, and `Ledger digest immutability and scheduled verification wiring` at `3892-3915`), `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and `src/orchestrator/src/zava_forward/orchestrator/rebuild.py` + `rebuild_azure.py`.
* Discovered four concrete gaps in `infra/README.md`'s existing `#136` coverage (`C11`):
  1. **Explicitly unverified**: `infra/README.md:3858` states *"This is a documentation record, not machine-checked and not live Azure evidence."*
  2. **Stale ledger digest row**: `infra/README.md:3884` still lists `Ledger digest upload and scheduled verification | none | Not built; open item in ADR 0001`, contradicting `infra/README.md:3892-3915`, `infra/modules/storage.bicep:117-155`, `infra/modules/containerapps.bicep:434-508`, and `infra/main.bicep:444-525` where `ledger-digests` WORM container, `job-{prefix}-ledger-verify`, and scheduled query rules (`alert-{prefix}-ledger-digest-mismatch`, `alert-{prefix}-ledger-verify-missing`) ARE delivered in Bicep (`C4`, `C6`, `C9`).
  3. **Incomplete module status table**: Only 14 of the 20 `infra/modules/*.bicep` files appear in `Layout` (`infra/README.md:20-35`) or the coverage register (`infra/README.md:3862-3887`). Six actual modules in `infra/modules/` are missing from module status tracking: `authTokenStore.bicep`, `guard.bicep`, `iothub-scope-guard.bicep`, `edge-existing-auth.bicep`, `edge-existing-guard.bicep`, and `staff-initializer-guard.bicep` (`C5`, `C11`). Furthermore, the register lacked an explicit `Named owner` column on manual/deferred rows and lacked an explicit `Delivered vs missing` module matrix covering all 20 `infra/modules/*.bicep` modules (including honest recording of placeholder default images on `agents`, `orchestrator`, and `import` jobs in `containerapps.bicep`, conditional flags like `enablePublicEdge` / `enableEntraTokenStore` / `enableIotTransportBudget`, and audit-only/deferred Defender flags in `governance.bicep`).
  4. **From-empty deployment sequence traceability**: While `src/orchestrator/src/zava_forward/orchestrator/rebuild.py:34-66` defines the 17 ordered rebuild stages (`parameters` through `restart`) and `infra/scripts/deploy.py` + `infra/scripts/pipeline.py` + `.github/workflows/src-deploy.yml` implement the operator and CI deployment flows, `infra/README.md` did not have a machine-checked from-empty deployment step table tying every prerequisite and deployment step to its exact repository template/script (`infra/governance.bicep`, `infra/parameters/*.bicepparam`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/scripts/credential_arm.py`, `infra/scripts/create-sql-users.py`, `src/core` store seed, `infra/scripts/setup-entra.py`, `infra/scripts/initialize-workbench-staff.py`, `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`) with zero undocumented steps (`C18`, `C19`, `C20`).

### Wave 3: Contrarian (Fragility, Existing Test Invariants, and Lint/Type Tooling Traps)

* Challenged assumptions against existing `infra/tests/*.py`, `.github/workflows/src-ci.yml`, and local tool execution (`C21`, `C22`, `C23`, `C24`):
  1. **Existing `infra/README.md` substring assertions**: `infra/tests/test_governance.py:82` asserts `"DoNotEnforce"` and `"until the owner accepts a cost"` exist in `infra/README.md`; `infra/tests/test_container_hosting_completeness.py:137-161` splits `infra/README.md` on `"Revision rollback:"` and `"Load run, from"` and checks `"not at declared scale"` and `"makes no production"`. Contrarian rule: preserve all existing prose outside the updated `Layout` and `Resource coverage register (issue 136, ...)` sections so zero existing README-parsing tests break (`C21`, `C22`).
  2. **Ruff configuration & cache trap**: Running bare `python3 -m ruff check infra/scripts infra/tests` and `ruff format --check infra/scripts infra/tests` across the entire directory flagged 114 lint rules (e.g., `FURB162`, `SIM102`, `SIM117`, `EXE001`) and 21 unformatted legacy files that pre-date `src-ci.yml`'s targeted ruff lists (`C23`), AND created `.ruff_cache` in the worktree (which `tools/rpi-checks.py:310` rejects as an ignored scratch file if left behind!). Contrarian resolution:
     * Never reformat unrelated legacy `infra/` files (`<rules_for_code_changes>` forbids unrelated edits).
     * Author `infra/scripts/bicep_inventory.py` and `infra/tests/test_bicep_architecture_inventory_136.py` so they pass **both** bare `python3 -m ruff check` (zero `SIM`/`FURB`/`EXE` warnings; no `#!/usr/bin/env python3` on non-executable files unless `chmod +x` or omit shebang like `setup-entra.py`) **and** `src-ci.yml`'s `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `python3 -m ruff format --isolated --line-length 100 --check`, and `python3 -m mypy --strict`.
     * Use `RUFF_CACHE_DIR=/tmp/...`, `MYPY_CACHE_DIR=/tmp/...`, and `PYTHONDONTWRITEBYTECODE=1` (and verify `git status --ignored --short` is empty before committing).
  3. **Full `infra/tests` import environment**: Running `python3 -m unittest discover -s infra/tests -p "test_*.py" -q` requires `zava_forward` source packages importable (`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src` or installed distributions) because `test_bicep_policy.py`, `test_staff_azure.py`, and `test_resident_demo_*.py` import `zava_forward.core.*` (`C24`). Also `infra/tests` runs ~482 tests in ~200s because `test_bicep_policy.py` compiles Bicep templates via `az bicep build`; use `initial_wait: 300` when running the full `infra/tests` suite.
  4. **Over-claiming trap**: Issue `#136` explicitly warns that static Bicep definitions do not prove live Azure deployment, worker runtime wiring (`#144`), or epic stabilization (`#440`). Both `bicep_inventory.py` and `infra/README.md` must distinguish *Delivered in Bicep*, *Delivered in Bicep (conditional / placeholder runtime / audit-only)*, and *Intentionally manual or deferred with named owner*, without claiming live Azure verification.

## Evidence Log

| ID  | Source (`path:line`) | Summary of Verified Fact |
|-----|----------------------|--------------------------|
| C1  | `docs/adrs/0001-azure-architecture.md:33-165` | Proposes ACA + Jobs, Foundry (`gpt-4.1`, `gpt-4.1-mini`), Azure SQL + Ledger, Blob + Queues, IoT Hub, Key Vault, ACR, VNet + Private Endpoints, Log Analytics + App Insights + Action Group, Entra ID + UAMIs, M365 Teams/Blob fallback, and records open/deferred items (controlled egress for Graph/SharePoint, AI Search, Document Intelligence, Content Understanding, Service Bus, Power BI). |
| C2  | `docs/adrs/0002-pilot-readiness-architecture.md:19-145` | Proposes optional Azure Front Door Premium + WAF (`enablePublicEdge`) with Private Link origin and managed TLS (`edgeCustomDomain` requiring manual DNS `_dnsauth` TXT + CNAME), GIS `tileUrl` configuration (OSM demo default, licensed provider deferred), and subscription-scope Azure Policy (`DoNotEnforce`) + conditional Defender for Cloud (`enableDefenderPlans=false`). |
| C3  | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:27-198` | Confirms existing 6-service topology fits 5 core journeys; adds queue-backed ranking/import jobs, WORM containers, and IoT Hub B1 + Event Hubs Standard keyless adapter (`enableIotHub`) with explicit owner `Juan Manuel Servera` for IoT exercise device credentials (`#185`). |
| C4  | `infra/main.bicep:1-547` | Wires `guard`, `network`, `monitoring`, `identity`, `registry`, `storage`, `authTokenStore` (conditional), `keyvault`, `sql`, `foundry`, `iotHub`, `apps` (`containerapps`), `operationalMonitoring`, `edge` (conditional), and ledger digest scheduled-query alerts (`ledgerDigestMismatch`, `ledgerVerifyMissing`). |
| C5  | `infra/modules/` (20 `.bicep` files) | Exact module set: `authTokenStore.bicep`, `containerapps.bicep`, `edge.bicep`, `edge-existing-auth.bicep`, `edge-existing-guard.bicep`, `envDns.bicep`, `foundry.bicep`, `guard.bicep`, `identity.bicep`, `iothub.bicep`, `iothub-scope-guard.bicep`, `keyvault.bicep`, `monitoring.bicep`, `network.bicep`, `operationalMonitoring.bicep`, `privateEndpoint.bicep`, `registry.bicep`, `sql.bicep`, `staff-initializer-guard.bicep`, `storage.bicep`. |
| C6  | `infra/modules/containerapps.bicep:1-590` | Defines CAE (`cae-{prefix}`), `ca-{prefix}-api`, `authConfigs/current`, `job-{prefix}-auth-renewal`, `job-{prefix}-agents`, `job-{prefix}-orchestrator`, `job-{prefix}-ledger-verify`, `job-{prefix}-ranking-publish`, and `job-{prefix}-import`; defaults worker job images to placeholder unless digest images are supplied (`#144`). |
| C7  | `infra/modules/edge.bicep:1-248` | Defines `Microsoft.Cdn/profiles` (`Premium_AzureFrontDoor`), `FrontDoorWebApplicationFirewallPolicies` (DRS 2.1, Bot Manager 1.1, rate limit), endpoint, origin group, Private Link origin, custom domain + managed certificate (when `customDomain` non-empty), route, security policy, and diagnostics. |
| C8  | `infra/modules/monitoring.bicep:1-155` | Defines Log Analytics workspace, App Insights, AMPLS (`ampls-{prefix}`) + scoped resources + private endpoint, and Action Group (`ag-{prefix}`) with email receiver and conditional Teams webhook receiver (`teamsWebhookUrl`). |
| C9  | `infra/modules/storage.bicep:1-315` | Defines StorageV2 account, 7 base containers (`evidence`, `reports`, `exports`, `audit-archive`, `ledger-digests`, `m365-fallback`, `staff-results`) + conditional `ranking-archive`, unlocked WORM immutability policies on `audit-archive`, `ledger-digests`, and `ranking-archive`, `staff-results/` expiry rule, 4 queues, `CanNotDelete` lock, RBAC, diagnostics, and blob/queue private endpoints. |
| C10 | `infra/governance.bicep:1-148` | Subscription-scope template deploying `Microsoft.Authorization/policyAssignments` (`DoNotEnforce` default) and conditional `Microsoft.Security/pricings` for `StorageAccounts`, `SqlServers`, `KeyVaults`, and `Containers` (`enableDefenderPlans=false` default). |
| C11 | `infra/README.md:18-39,3852-3915` | `Layout` omits 6 of 20 modules; `Resource coverage register (issue 136, 2026-11-04)` says it is not machine-checked, omits `authTokenStore.bicep` and helper/guard modules, lacks an explicit owner column on all manual/deferred entries, and has a stale `Ledger digest upload and scheduled verification | none | Not built` row contradicted by lines `3892-3915`. |
| C12 | `infra/entra/app-registration.json:1-95` | Versioned Entra application registration manifest (roles, scopes, redirect conventions) applied outside ARM by `infra/scripts/setup-entra.py`. |
| C13 | `infra/secret-inventory.json:1-36` | Records all 4 Key Vault secrets (`entra-client-secret`, `entra-token-store-sas`, `resident-demo-password-verifier`, `resident-demo-session-key`) with named owner `Juan Manuel Servera` and rotation/alert intervals. |
| C14 | `infra/scripts/create-sql-users.py:1-58` | Idempotently creates contained Entra SQL users (`id-{workload}-{env}-api`, `id-{workload}-{env}-import`) via Entra access token after SQL private/admin path is available. |
| C15 | `infra/scripts/setup-entra.py:1-120` | Reconciles Entra app registration, service principal `appRoleAssignmentRequired`, Key Vault secret handoff (`credential_arm.py`), and Container Apps auth configuration without secret CLI arguments. |
| C16 | `infra/scripts/initialize-workbench-staff.py:1-100` | Reconciles app-scoped Entra role assignments and SQL workbench roster from private mode-0600 operator roster input. |
| C17 | `infra/defender-decision.json:1-35` | Records owner `Juan Manuel Servera` decision keeping Azure Policy in `DoNotEnforce` and `enableDefenderPlans: false` until unit pricing/cost is approved. |
| C18 | `infra/scripts/deploy.py:1-340` | Operator wrapper enforcing parameter validation, immutable/resolved orchestrator image check, existing auth lock preservation (`zava-forward-auth-lock`), `what-if` preview by default, and `--apply` creation. |
| C19 | `infra/scripts/pipeline.py:1-360` | CI deployment helper (`parameters`, `release`, `what-if`, `deploy`, `smoke`, `verify-environment`) invoked by `.github/workflows/infra-plan.yml` and `.github/workflows/src-deploy.yml`. |
| C20 | `src/orchestrator/src/zava_forward/orchestrator/rebuild.py:34-66` & `rebuild_azure.py:141-520` | Canonical 17-stage reproducible from-empty rebuild sequence (`parameters`, `dependencies`, `discover`, `images`, `credential`, `sql-users`, `seed`, `applications`, `authentication`, `staff`, `health`, `api-denial`, `browser-redirect`, `workload-sql`, `model-standard`, `model-capable`, `restart`). |
| C21 | `infra/tests/test_governance.py:70-90` | Asserts `"DoNotEnforce"` and `"until the owner accepts a cost"` remain in `infra/README.md`. |
| C22 | `infra/tests/test_container_hosting_completeness.py:137-161` | Asserts `"Revision rollback:"`, `"Load run, from"`, `"not at declared scale"`, and `"makes no production"` remain intact in `infra/README.md`. |
| C23 | `.github/workflows/src-ci.yml:228-265` | Runs offline `az bicep build` + `az bicep lint` on `infra/*.bicep` and `infra/modules/*.bicep`, `unittest discover -s infra/tests -v`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict`. |
| C24 | `infra/tests/test_bicep_policy.py:1196,2126` | Imports `zava_forward.core.ledger_digest_blob`; running full `infra/tests` requires `src/*/src` on `PYTHONPATH` (or editable installs) and `az bicep` CLI. |

## Parent Synthesis and Recommendations

### Converged Design Decision (Accepted)

1. **Create `infra/scripts/bicep_inventory.py`** (`--strict` typed, stdlib-only, formatted to 100 chars, clean under both bare `ruff check` and `--isolated` CI rules):
   * Parses `infra/main.bicep`, top-level `infra/*.bicep` (`governance.bicep`, `public-edge-existing.bicep`, `iot-hub-live.bicep`, `staff-initializer-rbac.bicep`, `live-receiver-job.bicep`, `live-simulator-job.bicep`, `private-proof-publisher.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), and every `infra/modules/*.bicep` file (`resource <sym> '<type>@<api>'` and `module <sym> '<path>'` declarations, ignoring `existing` references when counting provisioned resource types while tracking `existing` dependencies separately).
   * Parses the three structured Markdown tables in `infra/README.md` under the updated `## Resource coverage register and module delivery matrix (issue 136)` section (anchored by deterministic subheadings so parsing is unambiguous and human-readable):
     1. `### Proposed architecture resource inventory (ADRs 0001, 0002, 0003)` — maps every proposed resource/capability across ADRs 0001-0003 to either `bicep` (with exact Bicep file(s) and ARM resource type(s) verified to exist in those `.bicep` files) or `manual` / `deferred` (with non-empty rationale and explicit named owner, e.g., `Juan Manuel Servera (@jmservera)`).
     2. `### Bicep module delivery matrix` — 1-to-1 row equality with `sorted(Path("infra/modules").glob("*.bicep"))` (all 20 modules) plus top-level entrypoints summary, verifying each module's wired entrypoint(s), provisioned ARM resource types (or compile-time deployment guard role for parameter-guard modules), delivery status (`delivered`, `delivered-conditional`, or `delivered-placeholder-workers`), and honest remaining gap/owner reference.
     3. `### Reproducible from-empty deployment sequence` — ordered step-by-step sequence covering subscription governance, prerequisite RG/Entra admin check, Stage 1 infrastructure (`deployApplications=false`), discovery, ACR workload image build/digest release, Entra registration & Key Vault secret handoff, SQL contained user creation, synthetic SQL store seed, Stage 2 workload rollout (`deployApplications=true`), staff roster/role initialization, and post-deployment smoke/auth/SQL/AI/restart verification, where **every** step maps to an existing repository template/script path verified on disk (or an explicitly bounded manual prerequisite with named owner) with zero undocumented steps, and cross-checks alignment with `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and the 17 stages in `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`.
   * Exposes pure verification functions (`parse_bicep_file`, `load_readme_tables`, `verify_architecture_inventory`, `verify_module_delivery_matrix`, `verify_from_empty_sequence`, `verify_all`) plus a deterministic CLI (`python3 infra/scripts/bicep_inventory.py --check` / `--json`) returning exit code `0` on full alignment and `1` with actionable error diagnostics on any drift.
2. **Update `infra/README.md`**:
   * Update `## Layout` (`infra/README.md:18-39`) so all 20 `infra/modules/*.bicep` files and top-level templates/scripts (`bicep_inventory.py` included) are accurately listed.
   * Replace the stale unverified `## Resource coverage register (issue 136, 2026-11-04)` section (`infra/README.md:3852-3890`) with the machine-verified `## Resource coverage register (issue 136)` section containing the three canonical tables (`Proposed architecture resource inventory`, `Bicep module delivery matrix`, `Reproducible from-empty deployment sequence`), fixing the stale ledger-digest row, adding `authTokenStore.bicep` and all guard/helper modules, naming explicit owners on every manual/deferred item, and preserving the honest boundary statement that offline Bicep/script verification proves repository reproducibility and coverage rather than live Azure runtime health or `#440` epic closure.
   * Preserve every existing substring required by `test_governance.py` and `test_container_hosting_completeness.py`.
3. **Create `infra/tests/test_bicep_architecture_inventory_136.py`**:
   * Positive end-to-end verification tests proving all three `#136` engineering ACs against live repository files (`infra/main.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `docs/adrs/0001-*.md`..`0003-*.md`, `infra/README.md`).
   * Focused negative/mutation tests proving the verifier fails closed when: (a) an ADR-proposed resource is neither in Bicep nor recorded as manual/deferred with a named owner (or its manual owner is blank), (b) a `bicep`-disposition row references a missing Bicep file or unprovisioned ARM resource type, (c) a module `.bicep` file exists on disk without a matching module-matrix row (or vice versa, or has wrong status), or (d) a from-empty deployment step omits its repository script/template or points to a nonexistent file, or a `rebuild.py` stage is unrepresented.
   * CLI subprocess/entrypoint test confirming `bicep_inventory.py --check` exits `0` and `--json` emits structured inventory output.

### Alternatives Considered and Rejected

* **Embed inventory only inside `infra/scripts/pipeline.py`**: Rejected in favor of dedicated `infra/scripts/bicep_inventory.py` (the first option named by caller prompt item 2) because `pipeline.py` is a runtime Azure CLI CI release/deploy wrapper (`360` lines with strict `az` command mocking in `test_pipeline.py`), whereas `bicep_inventory.py` is a pure offline static architecture/module/reproducibility verifier with zero `az` runtime side effects.
* **Require `az bicep build` on every `bicep_inventory.py` invocation**: Rejected for the fast path because compiling 30 Bicep files takes ~45 seconds (`test_bicep_policy.py` already runs `az bicep build` across the templates); deterministic Bicep declaration parsing runs in <50ms while accurately extracting `targetScope`, `param`, `module`, and `resource` (provisioned vs `existing`) declarations, and `test_bicep_architecture_inventory_136.py` can also cross-check against `main.bicep` module wiring.

### Risks, Open Items, and Further Research

* **Pre-existing untouched `infra/` files under non-isolated `ruff`**: 21 legacy files in `infra/scripts` and `infra/tests` are not formatted with `ruff format` and trigger non-isolated `SIM`/`FURB` lint rules. Mitigation: keep unrelated files untouched per repository rules; verify `bicep_inventory.py` and `test_bicep_architecture_inventory_136.py` pass both bare `ruff check` and `src-ci.yml`'s `--isolated` lint/format checks plus `mypy --strict`; document the exact command outputs in the implementation changes artifact.
* **No further research cycles needed**: Cycle 1 answered Q1-Q5 completely with zero unresolved blockers.

## Readiness and Handoff

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Blockers**: None
* **Canonical evidence IDs**: `C1`-`C24`
* **Next phase**: `rpi-plan` (automatic continuation owned by RPI Agent)


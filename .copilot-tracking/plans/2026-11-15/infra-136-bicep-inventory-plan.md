<!-- markdownlint-disable-file -->
# RPI Plan: Issue 136 Bicep Architecture Inventory and Reproducibility Verifier

## Task Metadata

* Task ID: issue-136-bicep-inventory-2026-11-15
* Task slug: infra-136-bicep-inventory
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md

## Executive Summary

This plan delivers machine-checked repository evidence for the three unticked engineering acceptance criteria of Epic `#136` ("Epic: Bicep infrastructure as code and deployment pipeline"): (1) every resource proposed in ADRs 0001, 0002, and 0003 is either defined in Bicep or recorded as intentionally manual or deferred with a named owner, (2) a from-empty deployment sequence is reproducible from repository templates and scripts without undocumented steps, and (3) delivered-versus-missing status for every module in `infra/modules/*.bicep` is kept current and verified against disk.

Implementation adds a pure-stdlib, `--strict`-typed offline verifier (`infra/scripts/bicep_inventory.py`), updates `infra/README.md` (`## Layout` and `## Resource coverage register (issue 136)`) to replace the stale unverified 2026-11-04 documentation table with three canonical machine-checked tables, and adds `infra/tests/test_bicep_architecture_inventory_136.py` with positive end-to-end and fail-closed mutation tests.

### User Decisions and Requirements Highlights

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) in order under `.copilot-tracking/.../2026-11-15/` on branch `feat/infra-136-bicep-inventory` targeting parent branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`).
* Implement a machine-verifiable architecture-to-Bicep inventory, module delivery matrix checker, and from-empty reproducibility verifier in `infra/scripts/bicep_inventory.py`, paired with `infra/README.md` updates and `infra/tests/test_bicep_architecture_inventory_136.py`.
* Validate at the Focused tier (`ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --strict` on modified `infra/` files, and `unittest discover -s infra/tests -p "test_*.py" -q`), then commit all code, tests, docs, and `.copilot-tracking/` artifacts locally with the Copilot trailer without pushing.

### What You May Not Know

* `infra/README.md` already had an unverified `## Resource coverage register (issue 136, 2026-11-04)` section that omitted 6 of the 20 `infra/modules/*.bicep` modules (`authTokenStore.bicep` and 5 guard/auth helper modules) and contained a stale row claiming SQL Ledger digest upload/verification was "Not built", even though `ledger-digests`, `job-{prefix}-ledger-verify`, and scheduled-query alerts were subsequently wired (`Refs #115`).
* Existing tests (`infra/tests/test_governance.py` and `infra/tests/test_container_hosting_completeness.py`) assert specific prose anchors in `infra/README.md` (`"DoNotEnforce"`, `"until the owner accepts a cost"`, `"Revision rollback:"`, `"Load run, from"`, `"not at declared scale"`, `"makes no production"`), which must remain untouched.
* Twenty-one pre-existing untouched Python files in `infra/scripts` and `infra/tests` pre-date `src-ci.yml`'s targeted Ruff lists; keeping edits strictly scoped to `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py`, and `infra/README.md` preserves repository scope discipline while ensuring all new Python files pass both bare `ruff check` and `src-ci.yml` `--isolated` lint/format plus `mypy --strict`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for issue `#136` under `2026-11-15/` (caller prompt).
* Work in `/home/azureuser/source/ama-demo-wt/feat-136-bicep-repro` on branch `feat/infra-136-bicep-inventory` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) and leave a clean frozen `HEAD` without pushing (caller prompt).
* Prove the three unticked engineering Acceptance Criteria of `#136`: (a) every resource in the proposed architecture is either in Bicep or recorded as intentionally manual with owner, (b) a from-empty deployment is reproducible from the repository without undocumented steps, and (c) delivered versus missing status for each module is kept current (caller prompt; GitHub issue `#136`).
* Inspect `infra/main.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/README.md`, and `docs/adrs/0001-azure-architecture.md`, `0002-pilot-readiness-architecture.md`, `0003-journey-derived-capabilities-runtime-fit.md` (caller prompt item 1; completed in Research `C1`-`C24`).
* Add `infra/scripts/bicep_inventory.py` and update `infra/README.md` with the current module delivery matrix, ADR 0001/0002/0003 resource-to-Bicep or manual-owner mapping, and reproducible from-empty deployment sequence (caller prompt item 2).
* Add `infra/tests/test_bicep_architecture_inventory_136.py` parsing `infra/main.bicep`, `infra/modules/*.bicep`, and `infra/README.md` to prove all three criteria (caller prompt item 3).
* Validate with `ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --strict` on modified `infra/` files, and `unittest discover -s infra/tests -p "test_*.py" -q`, then commit code, tests, docs, and `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (caller prompt items 4-5).

## Goals

* Establish a deterministic, offline, stdlib-only verifier (`infra/scripts/bicep_inventory.py`) that parses Bicep templates, deployment scripts, rebuild stages, ADRs 0001-0003, and `infra/README.md` tables without live Azure calls.
* Reconcile `infra/README.md` so every ADR 0001-0003 proposed resource, all 20 `infra/modules/*.bicep` modules, and every step of the from-empty deployment sequence are current, accurate, and owner-attributed without over-claiming live Azure deployment or runtime worker readiness.
* Enforce drift-proof regression coverage in `infra/tests/test_bicep_architecture_inventory_136.py` covering positive repository verification and fail-closed mutation cases across all three `#136` engineering criteria.

## Scope and Non-Goals

### In Scope

* Creating `infra/scripts/bicep_inventory.py` with typed data structures, Bicep parser (`resource`, `existing`, `module`, `targetScope`), Markdown section/table parser, ADR/script/stage cross-checkers, and `--check` / `--json` CLI modes.
* Updating `infra/README.md` (`## Layout` and `## Resource coverage register (issue 136)`) with complete 20-module coverage, corrected SQL Ledger digest status, explicit named owners for every manual/deferred item, and the ordered reproducible from-empty deployment sequence mapped to repository scripts/templates.
* Creating `infra/tests/test_bicep_architecture_inventory_136.py` with positive and mutation tests, and running Focused tier validation.
* Recording RPI tracking artifacts and creating one clean local commit on `feat/infra-136-bicep-inventory`.

### Non-Goals

* Modifying any `.bicep` or `.bicepparam` template or changing live Azure infrastructure.
* Replacing placeholder runtime worker container images (`#144`), activating paid Defender plans (`#147`), or closing epic stabilization checkpoint `#440`.
* Reformatting or modifying unrelated pre-existing `infra/scripts/*.py` or `infra/tests/*.py` files.
* Pushing commits or opening/updating remote pull requests.

## Functional Requirements

* FR-1: Parse Bicep entrypoints (`infra/main.bicep` and standalone `infra/*.bicep` templates) and all `infra/modules/*.bicep` files to extract `targetScope`, `module` wiring references across both `infra/*.bicep` and sibling `infra/modules/*.bicep`, case-normalized provisioned ARM `resource` types (`microsoft.*`), and `existing` resource references.
  * Observable acceptance criteria: `bicep_inventory.py` accurately resolves all 20 `infra/modules/*.bicep` files, normalizes ARM provider/resource type casing (including lowercase `microsoft.insights/...` in `monitoring.bicep`), distinguishes provisioned resources from `existing` references and zero-resource parameter-guard modules, and maps module references from both top-level and sibling Bicep files.
* FR-2: Verify the proposed architecture resource inventory across ADR 0001, ADR 0002, and ADR 0003 (preserving all non-stale capabilities from the prior `infra/README.md` register, including Contractor B2B guest policy, M365/SharePoint permission grants, GitHub OIDC/environments/branch protection, and `#1258` ranking-archive Blob wiring) against `infra/README.md` and Bicep definitions.
  * Observable acceptance criteria: Every canonical proposed capability across ADRs 0001-0003 appears in `### Proposed architecture resource inventory (ADRs 0001, 0002, 0003)`; `bicep` / `bicep-conditional` rows cite existing `.bicep` files that provision the listed ARM resource types; `manual` / `deferred` rows cite a non-placeholder named owner and rationale; missing components, unprovisioned types, or blank manual owners fail verification.
* FR-3: Verify the `infra/modules/*.bicep` module delivery matrix in `infra/README.md`.
  * Observable acceptance criteria: `### Bicep module delivery matrix` has exact 1-to-1 path coverage of `infra/modules/*.bicep` (all 20 modules), verified caller module wiring across `infra/*.bicep` and `infra/modules/*.bicep`, exact case-normalized provisioned ARM resource type parity (or explicit guard designation), valid status (`delivered`, `delivered-conditional`, `delivered-placeholder-workers`, `delivered-guard`), and honest detection of `#144` placeholder worker image defaults (`mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep` and missing worker `command` overrides in `infra/modules/containerapps.bicep`).
* FR-4: Verify the reproducible from-empty deployment sequence in `infra/README.md` against `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, companion `infra/scripts/*`, and `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`.
  * Observable acceptance criteria: Every ordered step in `### Reproducible from-empty deployment sequence` maps to existing repository templates/scripts (or the explicitly owner-attributed Azure subscription/RG/Entra-admin prerequisite) with a documented verification check, covers all 17 canonical `STAGES` from `rebuild.py` in order, accounts for `deploy.py` (`--apply` and default `what-if`) and `pipeline.py`'s actual CLI `operation` choices (`plan`, `deploy`, `publish`, `changed-images`, `verify-environment`, noting how `rebuild.py`'s `"infra/scripts/pipeline.py release"` stage label maps to `pipeline.py publish` / `az acr build`), and has zero undocumented steps.
* FR-5: Provide automated unit and mutation regression tests in `infra/tests/test_bicep_architecture_inventory_136.py`.
  * Observable acceptance criteria: Unit tests pass against the live repository and prove fail-closed rejection on synthetic mutations for missing ADR resource rows, missing manual owners, false Bicep resource claims, missing/extra module rows, undocumented deployment steps, missing script paths, and missing rebuild stages.

## Non-Functional Requirements

* NFR-1: Fast, deterministic, offline static execution with zero secret or network access.
  * Objective threshold or evaluation condition: `python3 infra/scripts/bicep_inventory.py --check` completes in under 1 second offline using Python 3.12 standard library only, performing zero subprocess/`az`/network calls.
  * Observable acceptance criteria: `bicep_inventory.py` imports only Python stdlib modules and runs deterministically in unit tests.
* NFR-2: Strict type safety, lint cleanliness, formatting, and clean git worktree hygiene.
  * Objective threshold or evaluation condition: Zero errors from `mypy --strict`, bare `ruff check`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, and `ruff format --isolated --line-length 100 --check` on all new/modified Python files; zero existing `infra/tests` regressions; zero untracked or ignored cache artifacts left in the worktree.
  * Observable acceptance criteria: All validation commands exit `0` on target files, full `infra/tests` discovery passes (`0` failures, `0` errors), and `git status --ignored --short` is clean after commit.
* NFR-3: Tracking path isolation.
  * Objective threshold or evaluation condition: Zero `.copilot-tracking/` substrings in `infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py`, commit messages, and the modified/added sections (`## Layout` and `## Resource coverage register (issue 136)`) of `infra/README.md` (preserving untouched historical notes elsewhere in `infra/README.md`).
  * Observable acceptance criteria: Content and diff checks confirm zero `.copilot-tracking/` substrings in new Python files, modified `infra/README.md` sections, or commit messages.

## Acceptance Criteria

* AC-1: `python3 infra/scripts/bicep_inventory.py --check` exits `0` and confirms every proposed architecture resource from ADRs 0001, 0002, and 0003 is either provisioned in the cited Bicep file(s) or recorded as `manual`/`deferred` with a named owner in `infra/README.md`.
* AC-2: `python3 infra/scripts/bicep_inventory.py --check` confirms exact 20-of-20 parity between `infra/modules/*.bicep` and the `### Bicep module delivery matrix` table in `infra/README.md`, including entrypoint wiring and provisioned ARM resource types, and corrects the stale ledger-digest coverage record.
* AC-3: `python3 infra/scripts/bicep_inventory.py --check` confirms every step in `### Reproducible from-empty deployment sequence` maps to verified repository templates/scripts and covers all 17 canonical rebuild stages plus `deploy.py`/`pipeline.py` entrypoints with zero undocumented steps.
* AC-4: `infra/tests/test_bicep_architecture_inventory_136.py` passes alongside the full `infra/tests` suite (`test_governance.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_deploy.py`, `test_pipeline.py`, etc. unbroken) and passes `ruff` and `mypy --strict`.
* AC-5: All changes and `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`, `rpi-sessions`) under `2026-11-15/` are committed cleanly on `feat/infra-136-bicep-inventory` with the privacy-safe noreply git email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/infra-136-bicep-inventory-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md with Revise disposition (PC-001..PC-006 directly resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md                                                              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Complete and Ready for implementation after incorporating PC-001..PC-006                                                                 |
| Continuation context             | Confirmed automatic RPI Agent parent continues to rpi-implement after critique disposition                                                |

## Sources

* .copilot-tracking/research/2026-11-15/infra-136-bicep-inventory-research.md: Cycle 1 findings `C1`-`C24` across ADRs, Bicep files, deployment scripts, README gaps, and CI constraints.
* docs/adrs/0001-azure-architecture.md: Baseline Azure platform, data, AI, security, M365 fallback, and deferred Phase 2+ components.
* docs/adrs/0002-pilot-readiness-architecture.md: Public edge (Front Door Premium + WAF + custom domain DNS), GIS tile configuration, and subscription Policy/Defender baseline.
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md: Journey runtime fit, ranking/import/WORM storage additions, IoT Hub B1 + Event Hubs Standard adapter, and IoT credential ownership.
* infra/main.bicep and infra/modules/*.bicep: Canonical ARM resource and module wiring definitions.
* infra/scripts/deploy.py, infra/scripts/pipeline.py, and src/orchestrator/src/zava_forward/orchestrator/rebuild.py: Canonical operator, CI, and 17-stage from-empty deployment contracts.
* infra/README.md: Target documentation register (`Layout` and `Resource coverage register (issue 136)`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Architecture-to-Bicep and Reproducibility Verifier

* Intent: Create `infra/scripts/bicep_inventory.py` to parse Bicep templates, ADRs 0001-0003, deployment scripts/stages, and `infra/README.md` tables and fail closed on any missing coverage, missing owner, module drift, or undocumented deployment step.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Author `infra/scripts/bicep_inventory.py` parser, verifiers, and CLI

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2 (`C1`-`C20`, `C23`)
* Expected result: `infra/scripts/bicep_inventory.py` parses `.bicep` files, `infra/README.md` tables, ADR references, `deploy.py`/`pipeline.py` subcommands, and `rebuild.py` stages, providing programmatic APIs and `--check` / `--json` CLI flags with `--strict` mypy compliance.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile `infra/README.md` Layout, Coverage Register, Module Matrix, and Rebuild Sequence

* Intent: Update `infra/README.md` so all 20 `infra/modules/*.bicep` files, all ADR 0001-0003 proposed resources (with named owners for manual/deferred items), and the reproducible from-empty deployment sequence are current and pass `bicep_inventory.py --check` without disturbing existing README test anchors.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update `## Layout` and `## Resource coverage register (issue 136)` in `infra/README.md`

* Requirement and evidence: FR-2, FR-3, FR-4, AC-1, AC-2, AC-3 (`C5`, `C11`, `C20`, `C21`, `C22`)
* Expected result: `infra/README.md` accurately lists all 20 modules and `bicep_inventory.py` in `## Layout`, replaces the stale 2026-11-04 register with the three canonical machine-checked tables, fixes the ledger-digest status, preserves existing governance and container-hosting substrings, and passes `python3 infra/scripts/bicep_inventory.py --check`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add Unit and Mutation Tests and Run Focused Tier Validation

* Intent: Prove all three `#136` engineering criteria and fail-closed drift detection in `infra/tests/test_bicep_architecture_inventory_136.py` and verify full `infra/tests`, `ruff`, and `mypy --strict` cleanliness.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `infra/tests/test_bicep_architecture_inventory_136.py`

* Requirement and evidence: FR-5, NFR-2, NFR-3, AC-4 (`C1`-`C24`)
* Expected result: Unit test suite verifies live `infra/main.bicep`, `infra/modules/*.bicep`, `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `docs/adrs/0001-*.md`..`0003-*.md`, and `infra/README.md` alignment, plus fail-closed rejection across mutations for each of the three `#136` criteria and CLI execution.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute Focused validation suite and clean cache hygiene check

* Requirement and evidence: NFR-2, NFR-3, AC-4, AC-5 (`C23`, `C24`)
* Expected result: `ruff check`, `ruff format --isolated --line-length 100 --check`, `mypy --strict`, and `unittest discover -s infra/tests -p "test_*.py" -q` pass with zero regressions and zero leftover cache directories in the worktree.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/infra-136-bicep-inventory-phase-details.md

## Dependencies

* Python 3.12, `ruff`, `mypy`, and `az bicep` CLI: Installed in the worktree environment (`ruff 0.17.3`, `mypy 2.4.1`, `Bicep CLI 0.48.1`).
* Local `zava_forward` source packages (`src/*/src`): Added to `PYTHONPATH` when running full `infra/tests` discovery so existing cross-project tests (`test_bicep_policy.py`, `test_staff_azure.py`, `test_resident_demo_*.py`) resolve cleanly without mutating shared user site-packages.

## Critique Disposition

Single final-candidate critique executed in `.copilot-tracking/reviews/plans/2026-11-15/infra-136-bicep-inventory-plan-critique.md` (`Verdict: Revise`; 6 findings `PC-001`..`PC-006`, all planner-owned direct corrections).

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (`pipeline.py` CLI choices mismatch) | resolved | Updated FR-4, P01-T01, P02-T01, and P03-T01 to verify actual `pipeline.py` CLI `operation` choices `("plan", "deploy", "publish", "changed-images", "verify-environment")` and document how `rebuild.py` stage `images` (`"infra/scripts/pipeline.py release"`) maps to `pipeline.py publish` / `az acr build`. |
| PC-002 (`#144` placeholder worker image location/string) | resolved | Updated FR-3, P01-T01, P03-T01, and Follow-Up Items to detect `#144` placeholder worker status from `mcr.microsoft.com/k8se/quickstart:latest` defaults in `infra/main.bicep` plus missing `command` overrides on `orchestrator` and `importJob` in `infra/modules/containerapps.bicep`. |
| PC-003 (lowercase `microsoft.insights/...`, sibling callers, verified container/queue/IoT names) | resolved | Updated FR-1, P01-T01, and P02-T01 to normalize ARM resource types case-insensitively, scan `module` callers across both `infra/*.bicep` and `infra/modules/*.bicep`, and use verified container (`evidence`, `imports`, `quarantine`, `exports`, `audit-archive`, `ledger-digests`, `staff-results`, `ranking-archive`), queue (`agent-tasks*`, `import-jobs*`), and IoT (`iotHubRoutingReady`, unconditional `iotHub`/budget) identifiers. |
| PC-004 (pre-existing `.copilot-tracking/` lines in untouched `infra/README.md`) | resolved | Scoped NFR-3 and P03-T02 so `.copilot-tracking/` is forbidden across new Python files, commit messages, and modified/added sections of `infra/README.md` without editing unrelated historical lines (`1652`, `4421`). |
| PC-005 (retain existing manual rows from `infra/README.md:3862-3887`) | resolved | Updated FR-2, P01-T01, and P02-T01 to retain Contractor Entra B2B guest policy, M365/SharePoint `Sites.Selected` permission grants (`infra/scripts/grant-sharepoint-access.sh`), GitHub environments/OIDC/branch protection, RG budget (`infra/main.bicep`), and `#1258` ranking-archive Blob wiring in `REQUIRED_ARCHITECTURE_COMPONENTS` and Table 1. |
| PC-006 (cacheless `ruff` and `mypy` flags instead of `/tmp`) | resolved | Updated P03 and P03-T02 validation commands to use `ruff check --no-cache`, `ruff format --no-cache`, `mypy --no-incremental --cache-dir=/dev/null`, and `PYTHONDONTWRITEBYTECODE=1`. |

## Follow-Up Items

* Issue `#144`: Replace default placeholder worker image parameters (`mcr.microsoft.com/k8se/quickstart:latest` in `infra/main.bicep`) and wire runtime container `command` definitions for `orchestrator` and `importJob` plus active `agents` result routing in `infra/modules/containerapps.bicep`. Outside `#136` static inventory scope; recorded transparently as `delivered-placeholder-workers` in the module delivery matrix.
* Issue `#147`: Obtain owner cost sign-off (`infra/defender-decision.json`) before switching `enableDefenderPlans` to `true` or promoting `infra/governance.bicep` Policy enforcement from `DoNotEnforce` to `Default`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/infra-136-bicep-inventory-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

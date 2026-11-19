<!-- markdownlint-disable-file -->
# RPI Plan: Issue #144 Container Hosting Completeness and Hardening Contracts

## Task Metadata

* Task ID: issue-144-container-hardening
* Task slug: container-hardening-144
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/container-hardening-144-plan-critique.md

## Executive Summary

This plan completes the remaining local engineering contracts and deterministic verification suite for **Issue #144** ("Container hosting completeness: workers, scaling, revisions and load test") across Dockerfiles, Azure Container Apps Bicep templates, CI/CD release manifest orchestration, and offline test suites while strictly preserving live Azure deployment boundaries.

Specifically, the plan closes five concrete gaps discovered in Cycle 1 research and refined via single-pass `rpi-plan-critique`:
1. Adds a bounded `run` job subcommand to `zava_forward.importer` (mirroring `zava_forward.orchestrator run` while preserving bare no-arg version output for `src/check-container.py`) and wires explicit `command` + `args: ['run']`, `ZF_STORE: 'mssql'`, and `@minLength(1)` image constraints into `infra/modules/containerapps.bicep`.
2. Makes `TMPDIR=/tmp` explicit in the `ENV` contract of all six `src/` Dockerfiles (`api`, `agents`, `orchestrator`, `importer`, `Dockerfile.resident-demo`, `live-simulator.Dockerfile`) alongside non-root `USER 10001:10001`, root-owned immutable `/app`, and writable `/state`, and aligns dynamic `job-staff-*` Container Apps Job specifications in `infra/scripts/staff_azure.py` plus worker startup in `infra/scripts/staff-azure-worker.py` with `ZF_CONTAINER_HARDENING=enforced`, `enforce_from_env()`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` scratch mounts.
3. Adds deterministic aggregated image release manifest assembly and verification (`build_release_manifest` / `verify_release_manifest` writing `release-manifest.json` during release admission and embedding `release_manifest` in `deployment()` summary output) in `infra/scripts/pipeline.py`, tightens PR `plan` image validation to require valid 64-hex `@sha256:` digests and reject `quickstart` placeholders, and blocks placeholder or `:latest` non-blank `--orchestrator-image` and image `--parameter` overrides on `--apply` in `infra/scripts/deploy.py`.
4. Extends deterministic tests in `infra/tests/` (`test_container_hosting_144.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, `test_staff_azure.py`) and `src/importer/tests/` to verify worker/job image tag binding, `activeRevisionsMode: Single`, HTTP and Azure Queue scaling rules, `demoDirectIngress` parity, `importer run` OS-subprocess hardening refusal, and container hardening invariants across `src/*/Dockerfile` and `infra/`.

### User Decisions and Requirements Highlights

* Run the full RPI loop (`research`, `plan` with independent `rpi-plan-critique`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/*/2026-11-15/` on branch `feat/infra-144-container-hardening` without pushing or opening a PR.
* Enforce real, versioned, non-placeholder worker (`orchestrator`) and job (`importer`) Dockerfiles, Bicep definitions, and pipeline image release manifests with container hardening (`USER` non-root, read-only root filesystem compatibility with explicit writable `/tmp` volume mounts, dropped Linux capabilities / security context contract) while preserving live Azure deployment boundaries.
* Use the Focused validation tier: prefix Python test commands with `TMPDIR=/dev/shm`, run targeted test modules plus `ruff check`, `ruff format --check`, and `mypy`, and leave a clean frozen worktree committed with the Copilot co-author trailer.

### What You May Not Know

* Azure Container Apps ARM API `2025-07-01` does not accept Kubernetes `securityContext.readOnlyRootFilesystem` or `capabilities.drop` fields in ARM template containers; Zava Forward therefore enforces hardening across three complementary layers: Dockerfile + CI `docker run --read-only --cap-drop=ALL --security-opt=no-new-privileges` (`src/check-container.py`), Bicep `hardeningEnv` (`ZF_CONTAINER_HARDENING=enforced`, `TMPDIR=/tmp`, `ZF_STATE=/state`) + `EmptyDir` `/tmp` and `/state` mounts, and startup fail-closed kernel inspection in `zava_forward.core.container_hardening.enforce_from_env()`.
* `infra/main.bicep` intentionally retains stage-1 dependency bootstrap parameter defaults (`mcr.microsoft.com/k8se/quickstart:latest` / empty-to-quickstart forwarding on `orchestratorImage`) enforced by `infra/tests/test_bicep_policy.py` and `infra/tests/test_bicep_architecture_inventory_136.py` so `deployApplications=false` bootstrap compilation works before ACR exists, while `pipeline.py` and `containerapps.bicep` enforce real versioned workloads and explicit commands at release and runtime.

### Unresolved Decisions or Blockers

* None for local engineering scope. Live Azure rollout and deployed runtime smoke verification remain explicitly operator-gated (`Refs #144`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan` with independent `rpi-plan-critique`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `reviews/2026-11-15/`, `changes/2026-11-15/`, `reviews/logs/2026-11-15/`) for Issue #144 (caller prompt).
* Work on branch `feat/infra-144-container-hardening` (stacked over `feat/demo-164-chat-grounding-provenance-0900`) under Focused validation tier without running `tools/rpi-checks.py --all`, pushing, or opening a PR (caller prompt).
* Verify and enforce that worker (`orchestrator`) and job (`importer`) Dockerfiles, Bicep definitions, and pipeline image release manifests are versioned, real (non-placeholder), and enforce container hardening (`USER` non-root, read-only root filesystem compatibility with explicit writable `/tmp` volume mounts, dropped Linux capabilities / security context contract) while preserving live Azure deployment boundaries (caller prompt; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md`).
* Add or extend deterministic tests in `infra/tests/` verifying worker/job image tag binding, revision mode, scaling rules, and container hardening invariants across `src/*/Dockerfile` and `infra/modules/` (caller prompt).
* Prefix all Python test commands with `TMPDIR=/dev/shm`, run targeted test modules only (plus `ruff check`, `ruff format --check`, and `mypy`), commit all implementation, tests, docs, and `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and leave `git status --short` empty (caller prompt).

## Goals

* Complete the bounded runtime job entrypoint and Bicep invocation contract for `importer` (`importJob`) so both `orchestrator` and `importer` run explicit, hardened, non-placeholder commands in Azure Container Apps Jobs.
* Make container hardening invariants self-contained and uniform across all `src/` Dockerfiles, Bicep workload modules, and dynamic `staff_azure.py` job definitions.
* Enforce deterministic, versioned, non-placeholder `@sha256:` image release manifests and PR `plan` / `--apply` digest guards in `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`.
* Deliver fast, deterministic offline test coverage in `infra/tests/` and `src/importer/tests/` proving every `#144` hosting, scaling, revision, release-manifest, and hardening invariant without regressing `#136` or `test_bicep_policy.py`.

## Scope and Non-Goals

### In Scope

* Bounded `run` subcommand in `src/importer/src/zava_forward/importer/__main__.py` and unit tests in `src/importer/tests/`.
* Explicit `importJob` `command` + `args: ['run']` and `@minLength(1)` image parameters in `infra/modules/containerapps.bicep`, plus accurate `infra/README.md` status notes preserving `#136` inventory checks.
* Explicit `TMPDIR=/tmp` `ENV` parity across all six `src/` Dockerfiles and scratch-volume / hardening-env parity on dynamic `job-staff-*` jobs in `infra/scripts/staff_azure.py`.
* Aggregated `release-manifest.json` generation and verification in `infra/scripts/pipeline.py`, strict 64-hex `@sha256:` + non-placeholder checks in `pipeline.deployment()` PR `plan` mode, and `--apply` placeholder/`:latest` rejection on explicit `--orchestrator-image` in `infra/scripts/deploy.py`.
* Deterministic test additions/extensions in `infra/tests/test_container_hosting_144.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, and `infra/tests/test_staff_azure.py`.

### Non-Goals

* Live Azure resource-group deployments, ACR builds, or claiming live Azure acceptance for Issue #144.
* Removing stage-1 dependency bootstrap parameter defaults from `infra/main.bicep` (which are required by `test_bicep_policy.py` and `test_bicep_architecture_inventory_136.py` before ACR exists).
* Pushing commits to `origin`, opening or modifying GitHub pull requests, or running `tools/rpi-checks.py --all`.

## Functional Requirements

* FR-1: `python -m zava_forward.importer run` enforces `enforce_from_env()`, validates required `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT` and `BLOB_ENDPOINT` (when present), `SQL_SERVER` and `SQL_DATABASE` whenever `ZF_STORE` is `"mssql"` or unset (allowing omission only when `ZF_STORE` is explicitly `"json"` or `"sqlite"`), and gated `ZF_IMPORT_DISPATCH` (`""`, `"standby"`, `"off"`), emitting deterministic sorted standby JSON while bare `python -m zava_forward.importer` continues printing `zava-forward-import 0.1.0`.
  * Observable acceptance criteria: `src/importer/tests/test_cli_run.py` and `infra/tests/test_container_hosting_144.py` pass both positive standby and fail-closed exit-code-2 checks (including OS-subprocess `ZF_CONTAINER_HARDENING=enforced` refusal).
* FR-2: `infra/modules/containerapps.bicep` enforces `@minLength(1)` on `apiImage`, `agentImage`, `orchestratorImage`, and `importImage`, and configures `importJob` with `{ name: 'ZF_STORE', value: 'mssql' }`, `command: ['python', '-m', 'zava_forward.importer']`, and `args: ['run']`, causing `bicep_inventory.scan_bicep_tree` `apps_missing_worker_cmd` to evaluate to `False`.
  * Observable acceptance criteria: `az bicep build --file infra/main.bicep` succeeds and compiled Bicep tests verify explicit commands, args, `ZF_STORE=mssql`, scaling rules, and `activeRevisionsMode: Single` across standard and `demoDirectIngress` modes (`ca-{prefix}-api`, `ca-{prefix}-agents`, `job-{prefix}-orch`, `job-{prefix}-auth`, `job-{prefix}-audit`, `job-{prefix}-rank`, `job-{prefix}-load`).
* FR-3: All six `src/` Dockerfiles declare `TMPDIR=/tmp` alongside `PYTHONDONTWRITEBYTECODE=1`, `USER 10001:10001`, and root-owned `/app`, `infra/scripts/staff_azure.py` configures dynamic `job-staff-*` jobs with `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` scratch mounts, and `infra/scripts/staff-azure-worker.py` enforces `enforce_from_env()` fail-closed (`exit 2`) at startup.
  * Observable acceptance criteria: Static/unit checks in `test_container_hosting_144.py` and `test_staff_azure.py` verify image, dynamic job, and worker fail-closed hardening invariants.
* FR-4: `infra/scripts/pipeline.py` builds and verifies a canonical `release-manifest.json` (`manifest["tag"] == release_tag()`, eager Python 3.12 annotations without `@dataclass` + `from __future__ import annotations`) binding all four non-placeholder `@sha256:` workload digests (`api`, `agents`, `orchestrator`, `importer`) to all seven hosted apps/jobs and their hardening contract while embedding `release_manifest` in `deployment()` summary JSON, rejects malformed or `quickstart` images in PR `plan` mode, and `infra/scripts/deploy.py` rejects `quickstart` or `:latest` non-blank `--orchestrator-image` or image `--parameter` overrides when `--apply` is set.
  * Observable acceptance criteria: `test_pipeline.py`, `test_deploy.py`, and `test_container_hosting_144.py` verify valid manifest admission and fail-closed rejection on mutable tags, placeholders, SHA drift, and digest drift without breaking coupled fixtures.

## Non-Functional Requirements

* NFR-1: Deterministic offline execution and RAM-backed temporary I/O.
  * Objective threshold or evaluation condition: Zero network or live Azure CLI calls during tests; every test run executes under `TMPDIR=/dev/shm` and targeted suites complete within 60 seconds.
  * Operating condition or verification approach, if needed: Run targeted `unittest` modules with `TMPDIR=/dev/shm`.
  * Observable acceptance criteria: All targeted `infra/tests/` and `src/importer/tests/` modules exit 0 deterministically.
* NFR-2: Static type and style conformance across touched Python and Bicep artifacts.
  * Objective threshold or evaluation condition: Zero `ruff check`, `ruff format --check`, `mypy`, or `bicep_inventory.py --check` diagnostics.
  * Operating condition or verification approach, if needed: Run `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `ruff format --isolated --line-length 100 --check`, bare `python3 -m mypy` in `src/importer`, and `bicep_inventory.py --check`.
  * Observable acceptance criteria: All four static commands exit 0.

## Acceptance Criteria

* AC-1: Worker (`orchestrator`) and job (`importer`) Dockerfiles, `infra/modules/containerapps.bicep`, and `infra/scripts/pipeline.py` release manifests are versioned, real (non-placeholder), and enforce non-root `USER 10001:10001`, read-only rootfs compatibility with explicit writable `/tmp` + `/state` `EmptyDir` mounts, and dropped Linux capabilities / `NoNewPrivs` security context contracts.
* AC-2: Deterministic tests in `infra/tests/` and `src/importer/tests/` verify worker/job image tag and digest binding, `activeRevisionsMode: Single`, HTTP and Azure Queue scaling rules, `demoDirectIngress` naming/scaling parity, and container hardening invariants across `src/*/Dockerfile`, `infra/modules/`, and `infra/scripts/`.
* AC-3: Coupled repository invariants (`test_bicep_policy.py`, `test_bicep_architecture_inventory_136.py`, `test_from_empty_reproducibility_136.py`, `ruff`, `mypy`) pass with zero regressions and honest live-Azure boundary documentation in `infra/README.md`.
* AC-4: All code, tests, documentation, and `.copilot-tracking/` artifacts are committed cleanly on `feat/infra-144-container-hardening` with the Copilot trailer and `git status --short` is empty, without pushing or opening a PR.

## Test Ownership and Bounds Lock

* Canonical test targets: `src/importer/tests/test_cli_run.py` (new focused unit module, max 4 tests), `infra/tests/test_container_hosting_144.py` (extended, max 8 added test methods), `infra/tests/test_container_hosting_completeness.py` (extended inventory assertion, 0 added methods), `infra/tests/test_bicep_policy.py` (extended job tuple to include `ranking-publish`, 0 added methods), `infra/tests/test_pipeline.py` (extended, max 2 added test methods), `infra/tests/test_deploy.py` (extended `--apply` placeholder/`:latest` guard, max 1 added test method), `infra/tests/test_staff_azure.py` (extended scratch/hardening + worker `enforce_from_env()` assertion, max 2 added test methods), plus targeted regression execution of `infra/tests/test_bicep_architecture_inventory_136.py`, `infra/tests/test_from_empty_reproducibility_136.py`, and `infra/tests/test_container_contract.py`.
* Exact test removals: `none`.
* Maximum total new test methods across suite: 17.
* Semantic vs regression coverage: Semantic tests prove bounded `importer run` validation, release-manifest digest/hardening binding, PR `plan` and `deploy.py --apply` placeholder rejection, `demoDirectIngress` compiled Bicep parity (`ca-{prefix}-agents`, `job-{prefix}-rank`, etc.), dynamic `job-staff-*` worker startup hardening, and Dockerfile/Bicep hardening invariants; regression checks verify `#136` inventory/reproducibility (`delivered-placeholder-workers` preserved while `main.bicep` keeps bootstrap `quickstart:latest`) and `test_bicep_policy.py` / `test_deploy.py` bootstrap contracts remain green.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md                                                                 |
| Phase details                    | .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md                                                      |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/container-hardening-144-plan-critique.md (`Revise`; all 5 planner findings `PC-001`..`PC-005` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/container-hardening-144-research.md                                                          |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md is created by implementation as its evidence record        |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement`                                                                                           |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                                         |

## Sources

* `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md`: Cycle 1 evidence (`C1`-`C19`) covering Dockerfiles, `containerapps.bicep`, `pipeline.py`, `deploy.py`, `bicep_inventory.py`, `staff_azure.py`, and existing test suites.
* `infra/modules/containerapps.bicep` and `infra/main.bicep`: Current Container Apps & Jobs ARM definitions, `hardeningEnv`, `scratchVolumes`, scaling rules, and stage-1 bootstrap parameter contract.
* `src/orchestrator/src/zava_forward/orchestrator/__main__.py` and `src/importer/src/zava_forward/importer/__main__.py`: Reference bounded `run` mode pattern vs importer CLI entrypoint.
* `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`, and `infra/scripts/bicep_inventory.py`: Release digest publishing, PR planning checks, orchestrator image discovery, and `#136` Bicep module matrix checks.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Dockerfiles, Importer Bounded Job Entrypoint, and Dynamic Staff Job Spec

* Intent: Ensure `importer` supports a bounded, hardened `run` job mode matching `orchestrator` while preserving bare version probes, declare `TMPDIR=/tmp` explicitly across all six `src/` Dockerfiles, and add scratch mounts + hardening env to dynamic `job-staff-*` specs.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add bounded `run` subcommand to `zava_forward.importer` and unit tests

* Requirement and evidence: FR-1; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C9`, `C10`, `C11`)
* Expected result: `python -m zava_forward.importer run` enforces `enforce_from_env()`, validates `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, `SQL_SERVER`/`SQL_DATABASE` when `ZF_STORE=mssql`, and gated `ZF_IMPORT_DISPATCH` standby, outputting deterministic JSON while no-arg invocation still outputs `zava-forward-import 0.1.0`; unit tests in `src/importer/tests/test_cli_run.py` pass and `mypy` passes cleanly.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce `TMPDIR=/tmp` across `src/` Dockerfiles and full runtime hardening parity in `staff_azure.py` and `staff-azure-worker.py`

* Requirement and evidence: FR-3; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C1`-`C4`, `C7`, `C15`)
* Expected result: All six `src/` Dockerfiles (`api`, `agents`, `orchestrator`, `importer`, `Dockerfile.resident-demo`, `live-simulator.Dockerfile`) include `TMPDIR=/tmp` in `ENV` alongside `USER 10001:10001` and root-owned `/app`, `infra/scripts/staff_azure.py` attaches `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` mounts to `job-staff-*`, and `infra/scripts/staff-azure-worker.py` calls `enforce_from_env()` fail-closed (`exit 2`) at startup.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Complete Bicep Worker/Job Contracts and Pipeline Image Release Manifests

* Intent: Wire `importJob` explicit `command` + `args: ['run']` and `@minLength(1)` image constraints in `infra/modules/containerapps.bicep`, enforce deterministic `release-manifest.json` generation/verification and PR `plan` / `--apply` placeholder guards in `pipeline.py` and `deploy.py`, and align `infra/README.md`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Wire `importJob` explicit `run` command and `@minLength(1)` image constraints in `containerapps.bicep` and update `infra/README.md`

* Requirement and evidence: FR-2, AC-1, AC-3; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C5`, `C6`, `C14`, `C16`, `C19`)
* Expected result: `infra/modules/containerapps.bicep` sets `@minLength(1)` on all four image parameters and `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']` on `importJob` while preserving `infra/main.bicep` stage-1 bootstrap parameter defaults; `infra/README.md` accurately documents delivered `containerapps.bicep` worker/job commands and remaining live Azure boundary while `bicep_inventory.py --check` exits 0.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce deterministic release manifest bundle and non-placeholder digest guards in `pipeline.py` and `deploy.py`

* Requirement and evidence: FR-4, AC-1; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C12`, `C13`, `C17`)
* Expected result: `infra/scripts/pipeline.py` adds `build_release_manifest` and `verify_release_manifest` (persisting `release-manifest.json` during `release_images` with workload-to-digest mappings for all 7 apps/jobs and container hardening metadata), `pipeline.deployment()` PR `plan` mode requires `<registry>/<repo>@sha256:[0-9a-f]{64}` and rejects `quickstart` placeholders, and `infra/scripts/deploy.py` rejects `quickstart` or `:latest` explicit `--orchestrator-image` values when `--apply` is specified.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Expand Deterministic Hosting, Scaling, Revision, and Hardening Tests in `infra/tests/`

* Intent: Extend `infra/tests/` so every worker/job image tag/digest binding, revision mode, scaling rule, `demoDirectIngress` variant, Dockerfile hardening invariant, and dynamic job mount contract is deterministically verified offline.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Extend `test_container_hosting_144.py`, `test_container_hosting_completeness.py`, and `test_bicep_policy.py`

* Requirement and evidence: AC-2, AC-3; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C16`, `C18`)
* Expected result: Deterministic tests verify `importer run` CLI behavior, `importJob` compiled `command`/`args`, `demoDirectIngress=true` shortened names and scaling/revision parity, all 10 Bicep workload symbols in `test_container_hosting_completeness.py`, `ranking-publish` in `test_bicep_policy.py`, `TMPDIR=/tmp` + root-owned `/app` across all six `src/` Dockerfiles, and security context / Linux capability / `NoNewPrivs` parity across `check-container.py`, `acr-cutover.yaml`, and `container_hardening.py`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Extend `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py` for release manifests, placeholder rejection, and job scratch mounts

* Requirement and evidence: FR-3, FR-4, AC-2; `.copilot-tracking/research/2026-11-15/container-hardening-144-research.md` (`C12`, `C13`, `C15`, `C17`)
* Expected result: Unit tests verify `release-manifest.json` creation and tamper rejection, PR `plan` rejection of `quickstart` and malformed digests, `deploy.py` `rank-publish` discovery and `--apply` placeholder/`:latest` rejection, and `staff_azure.py` scratch volume mounts + hardening environment variables.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Run Focused Validation Suite and Reconcile Implementation Evidence

* Intent: Verify all targeted tests (`TMPDIR=/dev/shm`), `ruff check`, `ruff format --check`, `mypy`, and `#136` inventory/reproducibility checks pass with zero regressions and record complete implementation evidence.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Execute RAM-backed targeted tests, `ruff`, `mypy`, and `#136` regression checks

* Requirement and evidence: NFR-1, NFR-2, AC-3, AC-4; caller validation rules
* Expected result: All targeted `unittest` suites under `TMPDIR=/dev/shm`, `ruff check`, `ruff format --check`, `mypy` in `src/importer`, and `bicep_inventory.py --check` exit 0 cleanly, with outputs recorded in `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md

## Dependencies

* Azure CLI with Bicep compiler (`az bicep build`): Installed in environment and used by `test_bicep_policy.py` and `test_container_hosting_144.py` to verify compiled ARM JSON offline.
* Stage-1 bootstrap contracts in `infra/main.bicep` (`#136`): Preserved intact so `test_bicep_policy.py`, `test_bicep_architecture_inventory_136.py`, and `test_from_empty_reproducibility_136.py` remain green.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 `PC-001` (`High`): `importJob` omitted `ZF_STORE=mssql` in `containerapps.bicep` | Applied directly | Updated `FR-1`, `FR-2`, `P01-T01`, `P02-T01`, and `P03-T01` to wire `{ name: 'ZF_STORE', value: 'mssql' }` on `importJob`, require `SQL_SERVER` + `SQL_DATABASE` in `importer run` unless `ZF_STORE` is `"json"`/`"sqlite"`, and assert `ZF_STORE == "mssql"` on compiled `importJob`. |
| 2026-11-15 `PC-002` (`High`): `P03-T01` listed wrong `demoDirectIngress` names `ca-*-work` and `job-*-rank-publish` | Applied directly | Updated `FR-2` and `P03-T01` to assert exact compiled `containerapps.bicep` names (`ca-{prefix}-api`, `ca-{prefix}-agents`, `job-{prefix}-orch`, `job-{prefix}-auth`, `job-{prefix}-audit`, `job-{prefix}-rank`, `job-{prefix}-load` with `enableEntraTokenStore` / `enableRankingArchiveBlob` enabled). |
| 2026-11-15 `PC-003` (`Medium`): `staff_azure.py` omitted `ZF_CONTAINER_HARDENING=enforced` and `staff-azure-worker.py` startup `enforce_from_env()` | Applied directly | Updated `FR-3`, `P01-T02`, `P03-T02`, and `P04-T01` to add `ZF_CONTAINER_HARDENING="enforced"` in `staff_azure.py`, startup `enforce_from_env()` (`exit 2` on `ContainerHardeningError`) in `staff-azure-worker.py`, unit tests in `test_staff_azure.py`, and `mypy`/`ruff` checks matching `src-ci.yml`. |
| 2026-11-15 `PC-004` (`Medium`): Coupled fixtures in `test_container_hosting_144.py`, `test_pipeline.py`, and `test_deploy.py` | Applied directly | Updated `FR-4`, `P02-T02`, `P03-T02`, and `Test Ownership and Bounds Lock` to check `manifest["tag"] == release_tag()`, embed `release_manifest` in `deployment()` summary JSON, avoid `from __future__ import annotations` + `@dataclass` in `pipeline.py` (`mypy --strict`), reject `PLACEHOLDER`/`:latest` on non-blank `--orchestrator-image` and image `--parameter` overrides under `--apply` without enforcing 64-hex CLI digest lengths, and run `infra/tests/test_deploy.py`. |
| 2026-11-15 `PC-005` (`Medium`): `#136` `bicep_inventory.py` `delivered-placeholder-workers` guardrail and `importer run` subprocess refusal test | Applied directly | Updated `P03-T01` to include `["-m", "zava_forward.importer", "run"]` in `test_all_deployed_entrypoints_fail_closed_under_enforced_hardening_violation`, and updated `P02-T01` / `P04-T01` to preserve `` `delivered-placeholder-workers` `` in `infra/README.md` while refreshing `#144` notes and running `test_bicep_architecture_inventory_136.py`. |
| Accepted platform boundary (non-blocking) | Accepted residual risk | Azure Container Apps ARM API `2025-07-01` omits container `securityContext` properties and live Azure VNet/ACR/25-user load rollout remains operator-gated (`Refs #144`), documented honestly in `infra/README.md`. |

## Follow-Up Items

* Authorized live Azure deployment and runtime smoke verification for Issue #144: Outside local offline scope and prohibited without explicit operator authorization and live Azure environment execution; owned by Juan Manuel Servera (@jmservera).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

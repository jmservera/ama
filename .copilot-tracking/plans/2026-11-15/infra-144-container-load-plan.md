<!-- markdownlint-disable-file -->
# RPI Plan: Issue #144 Container Hosting Completeness

## Task Metadata

* Task ID: issue-144
* Task slug: infra-144-container-load
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-144-container-load-plan-critique.md

## Executive Summary

This plan delivers and proves the four remaining unticked acceptance criteria on Issue #144 (`Container hosting completeness: workers, scaling, revisions and load test`) on branch `feat/infra-144-container-load`:

1. **Real, versioned worker and job images deployed through the pipeline**: Completes maintenance-job image consistency and discovery parity across `infra/scripts/pipeline.py` and `infra/scripts/deploy.py` by adding `rank-publish` (`job-forward-{environment}-rank-publish`) alongside `auth-renewal` and `ledger-verify`, promotes `zava_forward.orchestrator` from a version-only stub to a bounded `run` scheduled-job subcommand (`args: ['run']` in `infra/modules/containerapps.bicep`, while preserving bare no-arg version output for `src/check-container.py`), and verifies end-to-end versioned tag (`sha-<40hex>-r<run_id>-a<attempt>`) + immutable `@sha256:<64hex>` digest wiring across `.github/workflows/src-deploy.yml`, `infra/scripts/pipeline.py`, `infra/main.bicep`, and all seven workload containers in `infra/modules/containerapps.bicep`.
2. **Container hardening enforced in the deployed app, not only in CI**: Pairs deployed Bicep resource specifications (`ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, and explicit `EmptyDir` ephemeral scratch mounts for `/tmp` and `/state` across `infra/modules/containerapps.bicep` including `tokenRenewal` inline `env` and `publicSimulationRecipe`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep`) with a `mypy --strict` stdlib runtime guard (`zava_forward.core.container_hardening`) wired at the top of `main()` before `argparse` and outside broad `except` blocks across all deployed application and job entrypoints (`api`, `agents`, `orchestrator`, `importer`, `resident_demo`, `live_receiver`, `live_simulator`). At startup in deployed containers, the guard enforces `UID/GID 10001:10001` (never root), sets `os.umask(0o077)` and Linux `prctl(PR_SET_NO_NEW_PRIVS, 1)`, verifies zero `CapEff`/`CapPrm`/`CapInh`/`CapAmb` and `NoNewPrivs == 1` in `/proc/self/status`, rejects writes to `/` and `/app` (`EROFS` or `EACCES`), and confirms bounded ephemeral scratch mounts are writable.
3. **Declared-scale fixture load test executed and recorded without claiming production scale**: Executes `src/api/tests/scale_load.py` and `src/api/tests/test_scale_fixture_load_and_restart.py` against the deterministic 60,000-home SQLite `SqlStore` scale fixture (`SEED=11`, 53,821 events, 20 sessions, 5.0 target requests/s) on the updated codebase (with `ZF_CONTAINER_HARDENING` unset on the non-10001 host UID, paired with isolated subprocess fail-closed hardening verification), recording dated outputs (`docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`) that preserve `meets_declared_workload: false` and explicit non-production-scale disclaimers.
4. **Single-replica and restart behaviour verified with audit persistence**: Verifies Bicep single-revision and single-replica bounds (`activeRevisionsMode: 'Single'`, simulation-lane `maxReplicas: 1`, `resident-demo.bicep` `maxReplicas: 1`, job `parallelism: 1`), `agents` worker `SIGTERM` graceful drain and lease redelivery across crashes, and separate-process API `SIGKILL` hard restart with durable SHA-256 `/api/audit-check` chain integrity across process death and post-restart writes, all locked by `infra/tests/test_container_hosting_144.py` and documented in `infra/README.md`.

### User Decisions and Requirements Highlights

* Execute the full automatic RPI loop (`research`, `plan`, `implement`, `review`) with dated artifacts under `2026-11-15` for Issue #144 without pushing to remote.
* Deliver and prove all four unticked Issue #144 criteria via `infra/tests/test_container_hosting_144.py` and updated evidence documentation under Focused validation (`unittest` + `ruff check` + `ruff format --check`).
* Record declared-scale fixture load test results honestly without claiming production scale, autoscaling/SLA proof, or live Azure execution.

### What You May Not Know

* **Azure Container Apps ARM schema constraint**: `Microsoft.App/containerApps@2025-07-01` and `Microsoft.App/jobs@2025-07-01` reject Kubernetes `securityContext` properties (`BCP037`), and ACA's hypervisor guest omits `ST_RDONLY` on `/` while retaining the default non-root capability bounding set `CapBnd`. Furthermore, `infra/tests/test_container_contract.py` explicitly forbids Docker `ENTRYPOINT` wrappers. Enforcing `UID/GID 10001`, `prctl(PR_SET_NO_NEW_PRIVS, 1)`, zero effective/permitted/inheritable/ambient capabilities, DAC/ROFS write rejection on `/` and `/app`, and explicit Bicep `EmptyDir` mounts inside the Python application entrypoints enforces all three hardening pillars in both Docker (`--read-only --cap-drop=ALL`) and Azure Container Apps without breaking ACA startup.
* **Resident showcase environment isolation**: `zava_forward.core.resident_showcase` rejects `ZF_STATE*` environment variables by design (`FORBIDDEN_ENV_PREFIXES`), and `Dockerfile.resident-demo` carries no `/state` directory. Accordingly, `infra/resident-demo.bicep` mounts only `tmp` (`EmptyDir` at `/tmp`) and omits `ZF_STATE`, whereas `containerapps.bicep`, `live-receiver-job.bicep`, and `live-simulator-job.bicep` mount both `/tmp` and `/state` `EmptyDir` volumes.

### Unresolved Decisions or Blockers

* None. All design choices are resolved by repository evidence (`C1`-`C19`) and caller instructions.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `changes/2026-11-15/`, `reviews/logs/2026-11-15/`) for Issue #144 (`Container hosting completeness: workers, scaling, revisions and load test`) in `/home/azureuser/source/ama-demo-wt/feat-144-container-load` on branch `feat/infra-144-container-load` (user prompt).
* Deliver and prove the four unticked Issue #144 acceptance criteria: (1) worker and job images are real, versioned, and deployed through the pipeline; (2) container hardening (non-root, read-only file system, dropped capabilities) is enforced in the deployed app, not only in CI; (3) a load test against the declared scale fixture is run and recorded without claiming production scale; and (4) single-replica and restart behaviour is verified with audit persistence (user prompt; GitHub Issue #144).
* Add a dedicated test module `infra/tests/test_container_hosting_144.py` and evidence documentation verifying container hardening in the deployed app spec, versioned worker/job image wiring, declared-scale fixture load test execution/recording (without claiming production scale), and single-replica restart audit persistence (user prompt).
* Validate under Focused tier using `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q` and `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py`, plus regression checks across existing `infra/tests` and `src/` suites (user prompt; `.github/copilot-instructions.md`).
* Commit all changes and `.copilot-tracking/` artifacts locally with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer and privacy-safe `users.noreply.github.com` Git author email, and do not push (user prompt; `.github/copilot-instructions.md`).

## Goals

* Ensure all seven main-stack Container App and Job workloads (`api`, `agents`, `orchestrator`, `import`, `auth-renewal`, `ledger-verify`, `ranking-publish`) consume real, version-tagged, immutable `@sha256:`-pinned images through `src-deploy.yml` and `infra/scripts/pipeline.py`, including PR-plan consistency checks across all three orchestrator maintenance jobs.
* Enforce non-root execution (`10001:10001`), dropped capabilities + `NoNewPrivs=1`, read-only `/` and `/app` immutability, bytecode suppression, and bounded `EmptyDir` ephemeral scratch mounts (`/tmp`, `/state`) in deployed Container Apps/Jobs specs and runtime startup, not only in CI `docker run` harnesses.
* Execute and record dated 60,000-home scale-fixture load and separate-process `SIGKILL` restart runs (`docs/architecture/scale-load-2026-11-15.json`, `docs/architecture/scale-restart-2026-11-15.json`) with explicit non-production-scale framing (`meets_declared_workload: false`).
* Lock all four Issue #144 criteria with deterministic semantic and mutation/negative tests in `infra/tests/test_container_hosting_144.py` and accurate evidence documentation in `infra/README.md`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/container_hardening.py` and startup wiring in `api` (`server.py`, `resident_demo/__main__.py`, `live_receiver.py`, `live_simulator.py`), `agents` (`worker.py`), `orchestrator` (`__main__.py` including bounded `run` subcommand, `token_store.py`, `digest_blob.py`, `ranking_publish.py`, `source_monitor.py`, `document_rescan.py`), and `importer` (`__main__.py`).
* Deployed container hardening environment settings and `EmptyDir` volume declarations in `infra/modules/containerapps.bicep` (including `tokenRenewal` inline `env`, `publicSimulationRecipe` startup guard, and `orchestrator` `args: ['run']`), `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep`.
* Maintenance-job digest consistency check and target discovery updates (`rank-publish`) in `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`.
* Fresh dated 60,000-home scale-fixture load and single-replica `SIGKILL` restart JSON artifacts under `docs/architecture/` and updated hosting evidence documentation in `infra/README.md` (`#118` and `#144` sections).
* Dedicated test suite `infra/tests/test_container_hosting_144.py` (max 1 new test file, 0 test removals).

### Non-Goals

* Mutating live Azure resources, running cloud deployments, or claiming live Azure rollout / autoscaling / production scale.
* Modifying `src/*/Dockerfile` `ENTRYPOINT` directives, workflow permissions, or `main.bicep` `orchestratorImage` empty-string bootstrap fallback (`test_container_contract.py` and `test_bicep_policy.py` invariants).
* Pushing commits or opening/updating remote GitHub PRs or issue checkboxes before merge.

## Functional Requirements

* **FR-1 (Pipeline versioned worker and job image wiring)**: `infra/scripts/pipeline.py` builds, tags (`sha-<40hex>-r<run_id>-a<attempt>`), pushes, digest-pins (`@sha256:<64hex>`), pull-verifies, and binds `apiImage`, `agentImage`, `orchestratorImage`, and `importImage` across all seven main-stack containers; PR-plan `deployment()` checks `job-forward-{env}-rank-publish` alongside `auth-renewal` and `ledger-verify` for matching `orchestratorImage` (with matching `"rank-publish"` target discovery in `infra/scripts/deploy.py`); and `job-${prefix}-orchestrator` runs `python -m zava_forward.orchestrator run` as a real bounded standby/diagnostic job rather than a version-only stub.
  * Observable acceptance criteria: `pipeline.py` rejects conflicting `orchestratorImage` on `rank-publish` during PR planning, `deploy.py` includes `rank-publish` in `orchestratorImage` job discovery, `zava_forward.orchestrator` preserves bare no-arg version output while handling `run`, and compiled `modules/containerapps.bicep` binds every workload container to its versioned image parameter.
* **FR-2 (Deployed Bicep container hardening spec)**: Every deployed Container App and Job in `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep` sets `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, and `TMPDIR=/tmp` (plus `ZF_STATE=/state` for stateful-scratch workloads, excluding `resident-demo`) and mounts explicit `EmptyDir` ephemeral volumes for `/tmp` (and `/state` where used), while keeping certificate AzureFile mounts read-only (`mountOptions: 'ro'`).
  * Observable acceptance criteria: `az bicep build` and `az bicep lint` succeed with zero errors across all modified Bicep templates, and compiled ARM templates contain the expected `ZF_CONTAINER_HARDENING`, `EmptyDir` `volumes`, and `volumeMounts` on every container.
* **FR-3 (In-process deployed container hardening guard)**: When `ZF_CONTAINER_HARDENING=enforced`, `zava_forward.core.container_hardening.enforce_from_env()` enforces `UID == EUID == 10001` and `GID == EGID == 10001`, sets `umask(0o077)`, invokes `prctl(PR_SET_NO_NEW_PRIVS, 1)` on Linux, verifies `CapEff == CapPrm == CapInh == CapAmb == 0` and `NoNewPrivs == 1` from `/proc/self/status`, verifies `PYTHONDONTWRITEBYTECODE=1` / `sys.dont_write_bytecode`, verifies `/` and `/app` reject write attempts with `EROFS` or `EACCES`, and verifies configured scratch directories (`/tmp`, and `ZF_STATE` when set) are writable; when unset in developer test processes, `enforce_from_env()` is a safe no-op.
  * Observable acceptance criteria: All deployed workload entrypoints call `enforce_from_env()` before serving traffic or executing job work and exit non-zero / raise `ContainerHardeningError` when any hardening invariant is violated.
* **FR-4 (Declared-scale fixture load test execution and honest recording)**: Execute `src/api/tests/scale_load.py` and `src/api/tests/test_scale_fixture_load_and_restart.py` against the 60,000-home scale fixture (`DECLARED["homes"] = 60000`, `sessions = 20`) and record `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` with zero HTTP errors, populated latency/memory/CPU/SQL cost drivers, `meets_declared_workload: false`, and explicit non-production-scale scope statements.
  * Observable acceptance criteria: Both dated JSON reports exist, parse cleanly, record 60,000 homes with 0 route errors, and explicitly state `Not production scale` with `meets_declared_workload: false`.
* **FR-5 (Single-replica and restart audit persistence verification)**: Verify single-revision and single-replica hosting rules (`activeRevisionsMode: 'Single'`, simulation-lane and `resident-demo` `maxReplicas: 1`), standalone worker crash/drain lease redelivery without message loss, and separate-process API `SIGKILL` restart over SQLite `SqlStore` with intact SHA-256 `/api/audit-check` chain before and after post-restart audit mutations.
  * Observable acceptance criteria: `infra/tests/test_container_hosting_144.py` executes both live bounded load/SIGKILL-restart audit verification and worker crash-redelivery verification and passes deterministically.

## Non-Functional Requirements

* **NFR-1 (Zero regression across existing infrastructure and package contracts)**
  * Objective threshold or evaluation condition: 100% pass rate on `infra/tests/test_container_hosting_144.py`, full `infra/tests` discovery (`test_container_contract.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, `test_resident_demo_deploy.py`), and affected `src/` unit tests (`core`, `agents`, `orchestrator`, `importer`, `api` restart/load).
  * Operating condition or verification approach, if needed: Offline local execution with `az bicep` installed (`v0.48.1`) and standard library Python 3.12 packages installed in editable/local PYTHONPATH.
  * Observable acceptance criteria: Zero test failures, zero Bicep lint warnings/errors, and clean `ruff check infra` + `ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py`.
* **NFR-2 (Strict test budget and dependency isolation)**
  * Objective threshold or evaluation condition: Test removals = `none`; new test files <= 1 (`infra/tests/test_container_hosting_144.py`, plus focused unit assertions in `infra/tests/test_pipeline.py` if needed); `zava_forward.core.container_hardening` uses Python standard library only so `zava-forward-agents` preserves zero SQL/Azure SDK dependencies (`C6`).
  * Operating condition or verification approach, if needed: Verified via `importlib` inspection and `ruff` checks.
  * Observable acceptance criteria: `zava_forward.core.container_hardening` imports only stdlib modules and runs in `< 5 ms` per startup check.

## Acceptance Criteria

* Worker (`agents`) and all five job containers (`orchestrator`, `import`, `auth-renewal`, `ledger-verify`, `ranking-publish`) plus `api` are backed by real multi-stage non-root Dockerfiles, versioned (`sha-<40hex>-r<run_id>-a<attempt>`), digest-pinned (`@sha256:<64hex>`), and checked end-to-end in `pipeline.py` (including `rank-publish` maintenance consistency) and `infra/tests/test_container_hosting_144.py`.
* Deployed Bicep templates (`modules/containerapps.bicep`, `resident-demo.bicep`, `live-receiver-job.bicep`, `live-simulator-job.bicep`) compile cleanly with `ZF_CONTAINER_HARDENING=enforced` and explicit `EmptyDir` ephemeral scratch mounts, and all deployed workload entrypoints enforce non-root `10001:10001`, `NoNewPrivs=1` + zero active/permitted/inheritable/ambient capabilities, read-only `/` and `/app` write rejection, and writable ephemeral scratch at startup.
* Dated 60,000-home scale-fixture load and separate-process restart benchmarks (`docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json`) are executed and recorded with `meets_declared_workload: false` and explicit non-production-scale framing.
* Single-replica hosting boundaries, worker crash/drain lease redelivery, and API `SIGKILL` hard restart with durable SHA-256 audit-chain persistence (`/api/audit-check`) are verified by `infra/tests/test_container_hosting_144.py` and documented accurately in `infra/README.md`.
* Exact user-requested validation commands (`unittest` on `infra/tests/test_container_hosting_144.py`, `ruff check infra`, `ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py`) pass cleanly, and all changes + `.copilot-tracking/` artifacts are committed locally without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md                                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md                                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/infra-144-container-load-plan-critique.md (`Complete`, `Revise`, `PC-001`..`PC-005` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/infra-144-container-load-research.md                                                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement` after applying single-pass critique findings `PC-001` through `PC-005`                          |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to `Implement` (`P01-T01`)                                        |

## Sources

* `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md`: Primary three-wave research synthesis and verified codebase evidence `C1`-`C19`.
* `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep`: Deployed Container Apps and Jobs Bicep resource templates.
* `infra/scripts/pipeline.py` and `.github/workflows/src-deploy.yml`: Release build, container check, digest pinning, PR plan, and incremental deployment pipeline.
* `src/check-container.py`, `infra/tests/test_container_contract.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_resident_demo_deploy.py`: Existing container hardening and hosting invariants that must remain green.
* `src/api/tests/scale_load.py`, `src/api/tests/test_scale_fixture_load_and_restart.py`, `src/agents/tests/test_worker.py`: Declared-scale load benchmark, separate-process `SIGKILL` restart + `/api/audit-check` verifier, and worker replica restart / `SIGTERM` drain suite.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement in-process container hardening runtime and entrypoint wiring

* Intent: Enforce non-root UID/GID `10001:10001`, Linux `NoNewPrivs=1` + zero active capability sets, bytecode suppression, immutable `/` and `/app` write rejection, and bounded scratch directory writability inside deployed container processes.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add stdlib `zava_forward.core.container_hardening` guard module

* Requirement and evidence: FR-3, NFR-2; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C5`-`C7`, `C10`, `C14`)
* Expected result: `src/core/src/zava_forward/core/container_hardening.py` provides `ContainerHardeningError`, `enforce_container_hardening(...)`, and `enforce_from_env(env=None)` with deterministic dependency-injectable hooks for unit testing and zero external dependencies.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire `enforce_from_env()` into all deployed container and job entrypoints and add `orchestrator run`

* Requirement and evidence: FR-1, FR-3; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C1`, `C11`, `C15`); `PC-001`, `PC-004`
* Expected result: `api` (`server.main`, `resident_demo/__main__.main`, `live_receiver.main`, `live_simulator.main`), `agents` (`worker.main`), `orchestrator` (`__main__.main` with bounded `run` subcommand and `if __name__ == "__main__":` guard, `token_store.main`, `digest_blob.main`, `ranking_publish.main`, `source_monitor.main`, `document_rescan.main`), and `importer` (`__main__.main` with `if __name__ == "__main__":` guard) invoke `enforce_from_env(env)` at the top of `main()` before `argparse` and outside broad `except` blocks, failing closed with sanitized stderr + exit code `2` when `ZF_CONTAINER_HARDENING=enforced` detects any violation.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Harden deployed Bicep workload specifications and pipeline image consistency

* Intent: Enforce `ZF_CONTAINER_HARDENING=enforced` and explicit `EmptyDir` ephemeral scratch mounts across all deployed Container App and Job specs, wire `orchestrator` `args: ['run']`, and ensure both `pipeline.py` and `deploy.py` handle all three orchestrator maintenance jobs.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `ZF_CONTAINER_HARDENING=enforced`, `EmptyDir` scratch mounts, `publicSimulationRecipe` guard, and `orchestrator` `run` args to Bicep templates

* Requirement and evidence: FR-1, FR-2, NFR-1; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C1`, `C14`, `C15`, `resident_showcase.py` `FORBIDDEN_ENV_PREFIXES`); `PC-002`, `PC-004`
* Expected result: `infra/modules/containerapps.bicep` (including `commonEnv`, `tokenRenewal` inline `env`, `publicSimulationRecipe` startup `enforce_from_env()` without forbidden substrings, and `orchestrator` `args: ['run']`), `infra/resident-demo.bicep` (`/tmp` only, preserving `ZF_STATE` exclusion), `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep` declare `ZF_CONTAINER_HARDENING: 'enforced'`, `PYTHONDONTWRITEBYTECODE: '1'`, `TMPDIR: '/tmp'` (and `ZF_STATE: '/state'` on stateful-scratch containers) plus matching `EmptyDir` `volumes` and `volumeMounts`, compiling and linting cleanly via `az bicep`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Include `rank-publish` in `pipeline.py` maintenance-job digest check and `deploy.py` target discovery

* Requirement and evidence: FR-1; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C3`, `C4`, `C13`); `PC-004`
* Expected result: `infra/scripts/pipeline.py` checks `job-forward-{environment}-rank-publish` alongside `auth-renewal` and `ledger-verify` for conflicting `orchestratorImage` during PR `what-if` planning, and `infra/scripts/deploy.py` includes `"rank-publish"` in existing `orchestratorImage` job discovery.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Execute and record declared-scale load and single-replica restart benchmarks

* Intent: Run the 60,000-home scale fixture load harness and separate-process `SIGKILL` restart + audit-persistence harness on the updated codebase and record dated evidence artifacts without claiming production scale.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run 60,000-home `scale_load.py` and `test_scale_fixture_load_and_restart.py` and save dated JSON artifacts

* Requirement and evidence: FR-4, FR-5; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C16`, `C17`, `C18`)
* Expected result: `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` record clean 60,000-home SQLite `SqlStore` load metrics, `SIGKILL` hard restart recovery, intact SHA-256 `/api/audit-check` chain before and after post-restart writes, `meets_declared_workload: false`, and explicit non-production-scale scope disclaimers.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Author `infra/tests/test_container_hosting_144.py`, update evidence docs, and run Focused validation

* Intent: Prove all four unticked Issue #144 acceptance criteria with semantic and negative/mutation tests in `infra/tests/test_container_hosting_144.py`, document exact evidence and live-vs-local boundaries in `infra/README.md`, and pass all required test and lint checks.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Create `infra/tests/test_container_hosting_144.py` covering all four Issue #144 criteria

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, FR-5, NFR-1, NFR-2; caller instructions
* Expected result: `infra/tests/test_container_hosting_144.py` verifies: (1) versioned worker/job Dockerfile, `src-deploy.yml`, `pipeline.py` (including `rank-publish` conflict rejection), and compiled Bicep image bindings; (2) deployed Bicep `ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` mounts across all Container Apps/Jobs plus live positive and negative/mutation enforcement tests for `zava_forward.core.container_hardening` and workload entrypoints (`api`, `agents`, `orchestrator`, `importer`); (3) live bounded `scale_load` execution + validation of recorded 60,000-home `2026-11-15` JSON artifacts (`meets_declared_workload is False`, non-production disclaimers); and (4) Bicep single-replica/single-revision rules + live separate-process API `SIGKILL` restart with `/api/audit-check` persistence + `agents` worker crash redelivery.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Update `infra/README.md` hosting completeness evidence and run Focused validation suite

* Requirement and evidence: FR-1..FR-5, NFR-1; `.copilot-tracking/research/2026-11-15/infra-144-container-load-research.md` (`C8`, `C9`)
* Expected result: `infra/README.md` accurately documents the deployed-spec + in-process container hardening controls, `rank-publish` pipeline consistency check, and dated `2026-11-15` 60,000-home load and `SIGKILL` restart audit-persistence runs while preserving all existing contract phrases (`test_container_hosting_completeness.py`) and stating honestly that live Azure rollout/SLA remains deployment-time scope; `unittest`, existing `infra/tests` + `src/` regressions, `ruff check infra`, and `ruff format --check` all pass.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md

## Dependencies

* `az bicep` CLI (`v0.48.1` verified locally): Required to compile and lint `infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep` in `test_bicep_policy.py`, `test_resident_demo_deploy.py`, and `test_container_hosting_144.py`.
* Python 3.12 workspace packages (`src/core/src`, `src/agents/src`, `src/api/src`, `src/orchestrator/src`, `src/importer/src`) and `ruff`: Required for Focused validation and benchmark execution.

## Critique Disposition

Single-pass critique completed in `.copilot-tracking/reviews/plans/2026-11-15/infra-144-container-load-plan-critique.md` (`Critique execution: Complete`, `Verdict: Revise`). All five findings (`PC-001` through `PC-005`) are planner-owned direct corrections and have been applied in full.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (High: broad `except` blocks swallowing `ContainerHardeningError`, missing `orchestrator/__main__.py:main`, unguarded `importer/__main__.py` `sys.exit`, `mypy --strict` / `ruff format` exclusions) | Applied directly | Updated `P01-T01` and `P01-T02` so `enforce_from_env(env)` runs at the top of `main()` before `argparse` and outside broad `try/except` blocks (returning/exiting `2` with sanitized stderr), added `main()` + `if __name__ == "__main__":` guards in `orchestrator/__main__.py` and `importer/__main__.py`, enforced `mypy --strict` typing on `container_hardening.py`, and avoided whole-file `ruff format` on excluded legacy files (`server.py`, `digest_blob.py`, `token_store.py`). |
| `PC-002` (High: `publicSimulationRecipe` `/state` write before hardening check, `test_bicep_policy.py` forbidden substrings, `tokenRenewal` inline `env`, `/healthz` handler preservation) | Applied directly | Updated `P01-T02` and `P02-T01` to prepend `from zava_forward.core.container_hardening import enforce_from_env; enforce_from_env()` in `publicSimulationRecipe` without `os.environ`/`getenv` substrings, add hardening env vars to both `commonEnv` and `tokenRenewal` inline `env`, and leave `server.py` `/healthz` untouched. |
| `PC-003` (High: host-UID `ApiProcess` conflict under `ZF_CONTAINER_HARDENING=enforced`, irreversible in-process `prctl`/`umask` side effects, PEP 420 `sys.path` setup) | Applied directly | Updated `P01-T01`, `P03-T01`, and `P04-T01` to keep `umask_fn`/`prctl_fn` injectable for side-effect-free unit tests, verify real kernel `prctl(PR_SET_NO_NEW_PRIVS, 1)` + `umask` in a child subprocess, keep `ZF_CONTAINER_HARDENING` unset for host-UID `ApiProcess` / `P03-T01` runs while testing enforced startup refusal in separate child subprocesses, and append `src/orchestrator/src` + `src/importer/src` to `sys.path` with `importlib.invalidate_caches()`. |
| `PC-004` (Medium: `orchestrator` version-only stub documented in `infra/README.md:1338` and `deploy.py` `rank-publish` discovery parity) | Applied directly | Updated `FR-1`, `P01-T02`, `P02-T01`, and `P02-T02` to add a bounded `run` subcommand on `zava_forward.orchestrator` (`args: ['run']` on `job-${prefix}-orchestrator`, preserving bare no-arg version output for `src/check-container.py`) and add `"rank-publish"` to `infra/scripts/deploy.py` `orchestratorImage` job targets. |
| `PC-005` (Medium: `infra/README.md` `#118` startup-guard paragraph contradiction risk and pinned rollback/scale phrases) | Applied directly | Updated `P04-T02` to cover `infra/README.md` (`## Hardened source image rollout (#118)` and `## Container hosting completeness (#144)`), reconciling the `#118` startup-guard explanation with the ACA-compatible `ZF_CONTAINER_HARDENING=enforced` runtime guard while preserving all `test_container_hosting_completeness.py` pinned strings and local-vs-Azure honesty boundaries. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

<!-- markdownlint-disable-file -->
# RPI Changes: Issue #144 Container Hosting Completeness and Hardening Contracts

## Metadata

* Task ID: issue-144-container-hardening
* Related plan: .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01` through `P04`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`
* All remaining active-plan markers: none
* Status basis: Every phase and task (`P01-T01` through `P04-T01`) completed and verified against Focused-tier static, Bicep, inventory, and 274-test unit/integration checks (`TMPDIR=/dev/shm`).

## Execution Summary

Delivered complete local container hardening, worker/job execution contracts, release manifest verification, and deterministic test coverage for Issue #144 across `src/`, `infra/modules/`, `infra/scripts/`, `infra/README.md`, and `infra/tests/`:
* Added bounded, fail-closed `python -m zava_forward.importer run` execution mode (validating `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, `SQL_SERVER`/`SQL_DATABASE` under `ZF_STORE=mssql`, and gated `ZF_IMPORT_DISPATCH`) while preserving no-arg version probes, and wired `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']`, `{ name: 'ZF_STORE', value: 'mssql' }`, and `@minLength(1)` image constraints in `infra/modules/containerapps.bicep`.
* Added explicit `TMPDIR=/tmp` across all six `src/` Dockerfiles (`api`, `agents`, `orchestrator`, `importer`, `Dockerfile.resident-demo`, `live-simulator.Dockerfile`) and enforced `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, `EmptyDir` `/tmp` + `/state` scratch mounts, and startup `enforce_from_env()` (`exit 2` fail-closed) on dynamic `job-staff-*` runs in `infra/scripts/staff_azure.py` and `infra/scripts/staff-azure-worker.py`.
* Added consolidated `release-manifest.json` generation and tamper-resistant `verify_release_manifest` in `infra/scripts/pipeline.py` (binding all 4 project images, all 7 deployed Container Apps/Jobs, and `HARDENING_CONTRACT` metadata, plus embedding `release_manifest` in deployment summary JSON when present), upgraded PR `plan` mode to enforce `<registry>/<repo>@sha256:[0-9a-f]{64}` and reject `quickstart` placeholders, and hardened `infra/scripts/deploy.py --apply` to reject `quickstart` or `:latest` explicit image overrides.
* Added 12 focused deterministic tests (within the locked `<= 17` cap) across `src/importer/tests/test_cli_run.py` and `infra/tests/`, and refreshed `infra/README.md` `#144` boundary notes while preserving `infra/main.bicep` stage-1 bootstrap defaults and `#136` `bicep_inventory.py --check` reproducibility.

## Completed Work

### Phase P01: Importer Bounded Job Entrypoint, Dockerfile `TMPDIR=/tmp`, and Staff Job Hardening (`P01-T01`, `P01-T02`)

* `src/importer/src/zava_forward/importer/__main__.py`: Added `_valid_url`, `_run_job`, optional `env` mapping injection on `main()`, and `run` subcommand enforcing `enforce_from_env()`, queue/blob HTTPS endpoint validation, `SQL_SERVER`/`SQL_DATABASE` checks unless `ZF_STORE` is `"json"`/`"sqlite"`, and deterministic standby JSON output while preserving bare `zava-forward-import 0.1.0`.
* `src/importer/tests/test_cli_run.py`: Added 4 deterministic unit tests covering bare version probe, valid `mssql` and `json` `run` mode standby output, fail-closed invalid config (`exit 2`), and `ZF_CONTAINER_HARDENING=enforced` refusal (`exit 2`).
* `src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`: Added `TMPDIR=/tmp` alongside `PYTHONDONTWRITEBYTECODE=1`, `USER 10001:10001`, and root-owned `/app`.
* `infra/scripts/staff_azure.py` and `infra/scripts/staff-azure-worker.py`: Added `ZF_CONTAINER_HARDENING="enforced"`, `PYTHONDONTWRITEBYTECODE="1"`, `TMPDIR="/tmp"`, `ZF_STATE="/state"`, and `EmptyDir` `/tmp` + `/state` mounts on `job-staff-*`, plus startup `enforce_from_env()` (`exit 2` before secret consumption) in `staff-azure-worker.py`.

### Phase P02: Bicep `importJob` Contract, Release Manifest Bundle, and Placeholder Guards (`P02-T01`, `P02-T02`)

* `infra/modules/containerapps.bicep`: Added `@minLength(1)` on `apiImage`, `agentImage`, `orchestratorImage`, and `importImage`, and added `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']`, and `{ name: 'ZF_STORE', value: 'mssql' }` on `importJob` while keeping `infra/main.bicep` bootstrap defaults intact.
* `infra/README.md`: Updated `#144` notes on `container-apps-hosting-and-jobs` and `infra/modules/containerapps.bicep` while preserving `` `delivered-placeholder-workers` `` for `#136` inventory checks and keeping live Azure rollout honestly gated.
* `infra/scripts/pipeline.py`: Added `RELEASE_MANIFEST_FILE`, `PLAN_IMMUTABLE_IMAGE_RE`, `WORKLOAD_IMAGE_PARAMETERS`, `HARDENING_CONTRACT`, `build_release_manifest`, and `verify_release_manifest`; persisted `release-manifest.json` during `release_images`, embedded `release_manifest` in `deployment()` summary JSON when `release-manifest.json` exists, and enforced 64-hex digest + non-`quickstart` validation in PR `plan` mode.
* `infra/scripts/deploy.py`: Added `_is_disallowed_apply_image` and internal-whitespace checks so `--apply` rejects `quickstart` or `:latest` explicit `--orchestrator-image` and workload image `--parameter` overrides while preserving offline `what-if` and stage-1 bootstrap contracts.

### Phase P03: Deterministic Container Hosting, Scaling, Revision, and Hardening Tests (`P03-T01`, `P03-T02`)

* `infra/tests/test_container_hosting_144.py`: Updated `import` compiled contract (`command`/`args`/`ZF_STORE == 'mssql'`/`minLength == 1`) and `importer_run` subprocess hardening refusal check, and added 4 focused test methods covering `importer` bare vs `run` CLI modes, all six `src/` Dockerfiles (`TMPDIR=/tmp`, `USER 10001:10001`, immutable `/app`), compiled Bicep `demoDirectIngress` (`False` vs `True`) workload names + scaling/cron rules, and `check-container.py` / `acr-cutover.yaml` / `container_hardening.py` security-context parity, plus `release-manifest.json` tamper rejection.
* `infra/tests/test_container_hosting_completeness.py` and `infra/tests/test_bicep_policy.py`: Added `tokenRenewal`, `rankingPublish`, `live-receiver-job`, and `live-simulator-job` to workload inventory checks and added `ranking-publish` to `assert_hosting_limits_and_rollout`.
* `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, and `infra/tests/test_staff_azure.py`: Added 4 focused unit tests covering `release-manifest.json` persistence/verification, PR `plan` placeholder/malformed-digest rejection, `deploy.py --apply` placeholder/`:latest` refusal, and `staff_azure.py` / `staff-azure-worker.py` hardening mounts + fail-closed startup.

### Phase P04: Focused Validation Execution and Evidence Reconciliation (`P04-T01`)

* Ran all Focused-tier static, Bicep, inventory, and RAM-backed (`TMPDIR=/dev/shm`) unit/integration suites to green completion.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P02-T02` in `infra/scripts/pipeline.py`): Guarded reading `digest_dir / RELEASE_MANIFEST_FILE` inside `pipeline.deployment()` with `if manifest_path.is_file():` so unit tests that monkeypatch `pipeline.release_images` without writing disk artifacts continue operating cleanly while real runs embed `release_manifest` in `summary.json`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` | 12 touched Python files across `src/importer/` and `infra/` | Passed | `All checks passed!` (exit 0) |
| `ruff format --isolated --line-length 100 --check` | 12 touched Python files across `src/importer/` and `infra/` | Passed | `12 files already formatted` (exit 0) |
| `(cd src/importer && PYTHONPATH=../core/src python3 -m mypy)` | `src/importer` package & tests | Passed | `Success: no issues found in 16 source files` |
| `python3 -m mypy --strict infra/scripts/pipeline.py` | `infra/scripts/pipeline.py` | Passed | `Success: no issues found in 1 source file` |
| `PYTHONPATH=src/core/src python3 -m mypy --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff_blob.py infra/scripts/staff-azure-worker.py infra/scripts/credential_arm.py` | Staff Azure job & worker scripts | Passed | `Success: no issues found in 4 source files` |
| `python3 -m compileall -q` | `src/{core,agents,api,orchestrator,importer}/src` | Passed | Exit 0 |
| `az bicep build` + `az bicep lint` | `infra/modules/containerapps.bicep`, `infra/main.bicep` | Passed | Exit 0, zero lint errors/warnings on module contracts |
| `python3 infra/scripts/bicep_inventory.py --check` | Issue `#136` architecture & module matrix | Passed | `29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)` |
| `TMPDIR=/dev/shm python3 -m unittest ... -q` | `test_cli_run`, `test_cli_and_privacy_boundaries`, `test_container_hosting_144`, `test_container_hosting_completeness`, `test_container_contract`, `test_bicep_policy`, `test_pipeline`, `test_deploy`, `test_staff_azure`, `test_bicep_architecture_inventory_136`, `test_from_empty_reproducibility_136` | Passed | `Ran 274 tests in 169.585s — OK` |
| Full `tools/rpi-checks.py --all` local gate | Repository-wide full gate | Skipped (by caller rule) | Caller specified Focused validation tier (`infra/tests/` and `src/` targeted unit/static checks; no full `tools/rpi-checks.py --all` gate) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01` all checked `[x]`).
* Completed-work evidence and handoff prose: Reconciled across `container-hardening-144-changes.md`, `container-hardening-144-plan.md`, and `container-hardening-144-phase-details.md`.
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan tasks, `12` new test methods within `<= 17` cap).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None.

## Remaining Work

* None within declared scope (`P01` through `P04` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md, `## Follow-Up Items`
* Authorized live Azure deployment and runtime smoke verification for Issue #144: Outside local offline scope and prohibited without explicit operator authorization and live Azure environment execution; owned by Juan Manuel Servera (@jmservera).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`..`P04`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`; remaining: none
* Validation coverage: 274 targeted unit/integration tests (`TMPDIR=/dev/shm`), `ruff check`, `ruff format --check`, `mypy` (`src/importer`, `--strict pipeline.py`, `staff_azure.py`/`staff-azure-worker.py`), `compileall`, `az bicep build`/`lint`, and `bicep_inventory.py --check` all passed
* Blockers: None
* Current plan and detail updates: Guarded optional `release-manifest.json` embed in `pipeline.deployment()` when `release_images` is monkeypatched in unit tests
* Planning and critique state: Ready (`PC-001`..`PC-005` applied directly)
* Follow-up items: Live Azure deployment and runtime smoke verification for Issue #144
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent continues automatically to `rpi-review`

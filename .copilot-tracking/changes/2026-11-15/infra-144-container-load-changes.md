<!-- markdownlint-disable-file -->
# RPI Changes: Issue #144 Container Hosting Completeness

## Metadata

* Task ID: issue-144
* Related plan: .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01` through `P04`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`), `P04` (`P04-T01`, `P04-T02`)
* All remaining active-plan markers: None
* Status basis: All four phases (`P01` through `P04`) and all seven tasks (`P01-T01` through `P04-T02`) completed with verified Focused validation evidence.

## Execution Summary

Delivered and verified all four unticked Issue #144 container-hosting criteria: (1) completed `rank-publish` maintenance-job `orchestratorImage` consistency and target discovery in `infra/scripts/pipeline.py` and `infra/scripts/deploy.py` and wired a bounded `zava_forward.orchestrator run` job command (`args: ['run']` in `infra/modules/containerapps.bicep`); (2) added stdlib `zava_forward.core.container_hardening` and wired startup enforcement across all 12 deployed container/job entrypoints paired with `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, and `EmptyDir` ephemeral scratch mounts across `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep`; (3) executed and recorded 60,000-home scale-fixture load and separate-process `SIGKILL` restart runs in `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` with explicit non-production-scale framing (`meets_declared_workload: false`); and (4) authored `infra/tests/test_container_hosting_144.py` (15 tests covering all four criteria) and updated `infra/README.md`.

## Completed Work

### P01 Runtime Container Hardening and Entrypoint Wiring (`P01-T01`, `P01-T02`)

* Created `src/core/src/zava_forward/core/container_hardening.py` implementing stdlib `ContainerHardeningError`, `HardeningReport`, `enforce_container_hardening(...)`, and `enforce_from_env(env=None)` enforcing non-root UID/GID `10001:10001`, restrictive `umask(0o077)`, `sys.dont_write_bytecode = True`, Linux `prctl(PR_SET_NO_NEW_PRIVS, 1)` + `/proc/self/status` `NoNewPrivs == 1` and zero `CapEff`/`CapPrm`/`CapInh`/`CapAmb`, immutable `/` and `/app` write rejection, and bounded scratch path writability.
* Wired `enforce_from_env(...)` at the top of `main()` (before `argparse` and outside broad `try/except` blocks, exiting `2` with sanitized stderr) across all 12 deployed entrypoints in `src/api` (`server.py`, `resident_demo/__main__.py`, `live_receiver.py`, `live_simulator.py`), `src/agents` (`worker.py`), `src/orchestrator` (`__main__.py` with bounded `run` subcommand while preserving bare no-arg version print for `src/check-container.py`, plus `token_store.py`, `digest_blob.py`, `ranking_publish.py`, `source_monitor.py`, `document_rescan.py`), and `src/importer` (`__main__.py`).

### P02 Bicep Hardening Specifications and Pipeline Consistency (`P02-T01`, `P02-T02`)

* Updated `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, and `infra/live-simulator-job.bicep` with `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state` (excluding `ZF_STATE` on `resident-demo` per `FORBIDDEN_ENV_PREFIXES`), matching `EmptyDir` scratch `volumes` and `volumeMounts`, `publicSimulationRecipe` startup `enforce_from_env()`, and `orchestrator` `args: ['run']`.
* Added `rank-publish` (`job-forward-<env>-rank-publish`) to `infra/scripts/pipeline.py` maintenance-job digest conflict verification and `infra/scripts/deploy.py` existing `orchestratorImage` target discovery.

### P03 Declared-Scale Load and Single-Replica Restart Benchmarks (`P03-T01`)

* Executed `src/api/tests/scale_load.py` (`--homes 60000 --concurrency 20 --seconds 60`) and `src/api/tests/test_scale_fixture_load_and_restart.py` (`--homes 60000 --concurrency 20 --seconds 60`), saving `docs/architecture/scale-load-2026-11-15.json` (`252` requests, `0` errors, `3.87 req/s` in-window, `715.6 MiB` RSS after run, `meets_declared_workload: false`, `"Not production scale"`) and `docs/architecture/scale-restart-2026-11-15.json` (`448` requests, `0` errors, `6.97 req/s`, `614.9 MiB` RSS after load / `626.9 MiB` high-water, `3` audit entries intact across separate-process `SIGKILL` + `1` post-restart write -> `4` intact entries, `meets_declared_workload: false`, `"Not production scale"`).

### P04 Verification Suite, Evidence Documentation, and Focused Validation (`P04-T01`, `P04-T02`)

* Created `infra/tests/test_container_hosting_144.py` with 15 tests across four `unittest.TestCase` classes (`VersionedWorkerAndJobPipelineTests`, `DeployedContainerHardeningTests`, `DeclaredScaleFixtureLoadTestTests`, `SingleReplicaRestartAndAuditPersistenceTests`), bootstrapping workspace `sys.path` via `importlib` so discovery succeeds both with the user-supplied `PYTHONPATH` and with `env -u PYTHONPATH` (`python -m unittest discover -s infra/tests`).
* Updated `infra/README.md` (`## Hardened source image rollout (#118)` and `## Container hosting completeness (#144)`) to document deployed Bicep + in-process startup hardening, `rank-publish` pipeline consistency, `orchestrator run`, and the `2026-11-15` 60,000-home load and `SIGKILL` restart results while preserving all `test_container_hosting_completeness.py` contract phrases and explicit local-vs-Azure / non-production disclaimers.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P04-T01`): Added `importlib`-based workspace `sys.path` and child `PYTHONPATH` setup in `infra/tests/test_container_hosting_144.py` so hosted CI (`python -m unittest discover -s infra/tests -v` without `PYTHONPATH`) and direct local runs both succeed without `E402` or `noqa` suppressions.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q` | `P04-T01` (all 4 Issue #144 criteria) | Passed | `Ran 15 tests in 28.493s -> OK` (also verified with `env -u PYTHONPATH REQUIRE_AZ_BICEP=1` alongside `test_container_hosting_completeness.py`: `Ran 26 tests in 26.829s -> OK`). |
| `infra/tests` suite (`test_bicep_policy.py`, `test_container_contract.py`, `test_container_hosting_completeness.py`, `test_deploy.py`, `test_pipeline.py`, `test_resident_demo_deploy.py`, `test_container_hosting_144.py`) | Full `infra/tests` regression | Passed | `611/613` passed under `env -u PYTHONPATH` and the remaining 2 subprocess-import tests (`test_pipeline.py` and `test_container_hosting_144.py`) passed `45/45` with workspace `PYTHONPATH` (`613/613` total). |
| `az bicep build` + `az bicep lint` across `infra/*.bicep` and `infra/modules/*.bicep` | `P02-T01` Bicep compilation | Passed | All templates compiled and linted cleanly with `0` errors/warnings (`az bicep v0.48.1`). |
| `ruff` & `mypy --strict` across touched `infra` and all 5 `src/*` distributions | Code style, lint, and strict typing | Passed | `ruff check infra/tests/test_container_hosting_144.py` (`0` errors), `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` + `ruff format --isolated --line-length 100 --check` on `infra/tests/test_container_hosting_144.py`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py` (`0` errors), all 5 `src/*` `ruff check` + `ruff format --check` (`0` errors), and `mypy --strict` across `231` `src/*` files + `infra/scripts/pipeline.py` (`0` issues). Note: bare unconfigured `python3 -m ruff check infra` on `ruff 0.17.3` reports 112 pre-existing warnings (`SIM117`, `FURB167`, `EXE001`, etc.) solely in untouched legacy lines/files outside `src-ci.yml`'s `--select E,F,I,B,UP` contract; left untouched per repository surgical-change rules. |
| Touched `src/` unit suites + `python3 tools/rename-zava-tests.py` | Runtime entrypoints & branding | Passed | `python3 -m zava_forward.{core,agents,orchestrator,importer}` exited `0`; `src/api` live/resident/restart/scale tests (`112` tests, `OK`), `src/agents` `test_dispatch` (`15` tests, `OK`), `src/orchestrator` functional tests (`140` tests, `OK`), `src/importer` functional tests (`115/115` functional tests `OK`), and `tools/rename-zava-tests.py` (`25` tests, `OK`). |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01` through `P04` and `P01-T01` through `P04-T02` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled and current
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md, `## Follow-Up Items`
* None

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`), `P04` (`P04-T01`, `P04-T02`); remaining: none
* Validation coverage: Focused validation complete across `infra/tests/test_container_hosting_144.py`, `infra/tests` regression, `az bicep build/lint`, `ruff`, `mypy --strict`, touched `src/` unit suites, and `tools/rename-zava-tests.py`
* Blockers: None
* Current plan and detail updates: Local judgment recorded for `importlib` workspace `sys.path` bootstrap in `infra/tests/test_container_hosting_144.py`
* Planning and critique state: Ready (`PC-001`..`PC-005` applied directly)
* Follow-up items: None
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

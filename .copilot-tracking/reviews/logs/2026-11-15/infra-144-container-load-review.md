<!-- markdownlint-disable-file -->
# Review: Issue #144 Container Hosting Completeness

## Scope and Evidence

* Task ID: issue-144
* Review date: 2026-11-15
* Review scope: Full task (`P01` through `P04`, `P01-T01` through `P04-T02`)
* Assessed boundary: Versioned worker/job image pipeline consistency (`rank-publish` + `orchestrator run`), deployed Container Apps/Jobs hardening specifications (`ZF_CONTAINER_HARDENING=enforced` + `EmptyDir` scratch volumes) paired with stdlib `zava_forward.core.container_hardening` runtime startup enforcement across all 12 deployed entrypoints, dated 60,000-home scale-fixture load and `SIGKILL` restart JSON artifacts with non-production-scale disclaimers, `infra/tests/test_container_hosting_144.py` verification suite, and `infra/README.md` evidence documentation under Focused validation.
* Plan: .copilot-tracking/plans/2026-11-15/infra-144-container-load-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-144-container-load-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-144-container-load-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/infra-144-container-load-research.md; `docs/architecture/scale-load-2026-11-15.json`; `docs/architecture/scale-restart-2026-11-15.json`; `infra/tests/test_container_hosting_144.py`; `git diff` across `infra/` and `src/`

## Opening Review State

* Interpreted review goal: Verify once, from repository diffs, compiled Bicep templates, benchmark artifacts, and Focused test/lint execution, whether the completed full-plan implementation satisfies all four unticked Issue #144 acceptance criteria, `FR-1` through `FR-5`, `NFR-1` and `NFR-2`, and critique dispositions `PC-001` through `PC-005` without overclaiming production scale or live Azure execution.
* Review scope: Full task (`P01` through `P04`)
* Evidence readiness: Ready — plan, phase details, single-pass plan critique, changes log, research synthesis, dated benchmark JSON outputs, and Focused validation outputs are complete and reconciled.
* Acceptance basis: User prompt four unticked Issue #144 acceptance criteria, plan `FR-1`..`FR-5` and `NFR-1`..`NFR-2`, critique dispositions `PC-001`..`PC-005`, and repository Focused-tier validation rules.
* First comparison boundary: Plan-to-change reconciliation across `P01`-`P04` and critique dispositions `PC-001`-`PC-005`, bounded to local repository code, compiled ARM templates, local 60,000-home SQLite benchmarks, and unit/contract tests (excluding live Azure deployment).
* Active read-only boundaries: Read-only across production source, infrastructure templates, tests, documentation, and prior RPI artifacts; write authority restricted solely to this canonical review log (`.copilot-tracking/reviews/logs/2026-11-15/infra-144-container-load-review.md`).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-15 across all four plan phases (`P01` through `P04`, `P01-T01` through `P04-T02`), full `git diff` across `src/` and `infra/`, compiled ARM templates from `az bicep v0.48.1`, dated 60,000-home load and `SIGKILL` restart JSON reports, and Focused validation runs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01 Runtime Container Hardening and Entrypoint Wiring` | Reconciled | Stdlib `container_hardening.py` and all 12 deployed entrypoints (plus bounded `orchestrator run`) match `FR-1`, `FR-3`, `NFR-2`, `PC-001`, `PC-003`, and `PC-004`. |
| `P02` (`P02-T01`, `P02-T02`) | `P02 Bicep Hardening Specifications and Pipeline Consistency` | Reconciled | All 4 Bicep templates declare `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, and `EmptyDir` scratch volumes (`resident-demo.bicep` omits `ZF_STATE`); `pipeline.py` and `deploy.py` include `rank-publish`. |
| `P03` (`P03-T01`) | `P03 Declared-Scale Load and Single-Replica Restart Benchmarks` | Reconciled | `docs/architecture/scale-load-2026-11-15.json` and `docs/architecture/scale-restart-2026-11-15.json` record 60,000-home runs (`0` errors, `meets_declared_workload: false`, `"Not production scale"`). |
| `P04` (`P04-T01`, `P04-T02`) | `P04 Verification Suite, Evidence Documentation, and Focused Validation` | Reconciled | `infra/tests/test_container_hosting_144.py` (15 tests across all 4 Issue #144 criteria) and `infra/README.md` (`#118` and `#144` sections) match `FR-1`..`FR-5` and `PC-005`. |
| `Follow-Up Items` | `None` in active plan | Reconciled | Plan and changes record remain aligned with zero deferred active-scope items; external/live rollout items remain explicit non-goals. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/container_hardening.py` | Added pure-stdlib runtime hardening guard (`UID/GID 10001:10001`, `umask(0o077)`, `sys.dont_write_bytecode`, Linux `prctl(PR_SET_NO_NEW_PRIVS, 1)` + `/proc/self/status` capability/no-new-privs verification, `/` and `/app` write rejection, scratch writability). | File created and typed cleanly under `mypy --strict` with injectable test hooks. | `mypy --strict`, `ruff`, and positive/negative + Linux child kernel tests in `test_container_hosting_144.py` passed. | Reconciled |
| `P01-T02` | `src/api/src/zava_forward/api/server.py`, `resident_demo/__main__.py`, `live_receiver.py`, `live_simulator.py`, `src/agents/src/zava_forward/agents/worker.py`, `__main__.py`, `src/orchestrator/src/zava_forward/orchestrator/__main__.py`, `token_store.py`, `digest_blob.py`, `ranking_publish.py`, `source_monitor.py`, `document_rescan.py`, `src/importer/src/zava_forward/importer/__main__.py` | Wired `enforce_from_env(...)` at top of `main()` before `argparse` and outside broad `except` blocks (exiting `2` on violation), guarded `__main__.py` entrypoints, and added bounded `zava_forward.orchestrator run` standby check while preserving bare version print. | Verified across all 12 entrypoints in `git diff`. | OS-process exit-code-`2` refusal tests (`test_container_hosting_144.py`), `python3 -m zava_forward.{core,agents,orchestrator,importer}`, and package unit tests passed. | Reconciled |
| `P02-T01` | `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`, `infra/live-simulator-job.bicep` | Declared `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp` (plus `ZF_STATE=/state` outside `resident-demo`), matching `EmptyDir` scratch `volumes` and `volumeMounts`, `publicSimulationRecipe` startup guard, and `orchestrator` `args: ['run']`. | Compiled ARM JSON verified across all 7 main-stack workloads + 3 auxiliary templates without forbidden substrings. | `az bicep build` + `az bicep lint` across all `.bicep` files (`0` warnings/errors) and `test_bicep_policy.py` + `test_resident_demo_deploy.py` passed. | Reconciled |
| `P02-T02` | `infra/scripts/pipeline.py`, `infra/scripts/deploy.py` | Added `rank-publish` (`job-forward-<env>-rank-publish`) to PR-plan `orchestratorImage` consistency verification and `deploy.py` job discovery. | Verified in `git diff` and mutation tests. | `test_pipeline.py` (`30/30`), `test_deploy.py`, `mypy --strict infra/scripts/pipeline.py`, and `test_container_hosting_144.py` passed. | Reconciled |
| `P03-T01` | `docs/architecture/scale-load-2026-11-15.json`, `docs/architecture/scale-restart-2026-11-15.json` | Executed 60,000-home open-loop `scale_load.py` and separate-process closed-loop + `SIGKILL` restart `test_scale_fixture_load_and_restart.py` runs and recorded dated JSON artifacts. | Both JSON files parse cleanly with `homes == 60000`, `0` route errors, intact pre/post-`SIGKILL` SHA-256 audit chain (`3` -> `4` entries), `meets_declared_workload: false`, and `"Not production scale"`. | Asserted directly in `DeclaredScaleFixtureLoadTestTests` and `SingleReplicaRestartAndAuditPersistenceTests`. | Reconciled |
| `P04-T01`, `P04-T02` | `infra/tests/test_container_hosting_144.py`, `infra/README.md` | Authored 15-test verification module proving all 4 unticked Issue #144 criteria and updated `infra/README.md` (`#118` and `#144` sections) while preserving all `test_container_hosting_completeness.py` pinned phrases and non-production/non-Azure disclaimers. | `infra/tests/test_container_hosting_144.py` (1 new test file, 0 removals) and `infra/README.md` diff inspected. | `test_container_hosting_144.py` (`15/15` with and without `PYTHONPATH`), `test_container_hosting_completeness.py`, `ruff`, and `rename-zava-tests.py` passed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P04-T01` (`infra/tests/test_container_hosting_144.py`) | Bootstrapped workspace `src/*/src`, `src/*/tests`, and `infra/tests` paths via `importlib` after stdlib imports and propagated `src/{core,agents,api}/src` `PYTHONPATH` into the child `ApiProcess` inside `test_live_separate_process_sigkill_restart_preserves_sqlite_audit_chain`. | `.github/workflows/src-ci.yml` runs `python -m unittest discover -s infra/tests -v` without setting `PYTHONPATH` on `src/*/tests`; local judgment preserved approved scope without needing a user decision. | Recorded in `.copilot-tracking/changes/2026-11-15/infra-144-container-load-changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed (ordinary local judgment preserving `P04-T01` intent and `PC-003` guidance). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five single-pass critique findings (`PC-001` through `PC-005` in `.copilot-tracking/reviews/plans/2026-11-15/infra-144-container-load-plan-critique.md`) were planner-owned compatible corrections applied before implementation and verified in the final diff (`enforce_from_env` outside broad `except` blocks, `publicSimulationRecipe` without forbidden substrings, `tokenRenewal` inline `env`, host-UID `ApiProcess` compatibility + child-process kernel `prctl` proof, `orchestrator run` + `deploy.py` `rank-publish` parity, and `infra/README.md` `#118`/`#144` consistency).
* Material revisions: None occurred during implementation; no second critique was run or needed.
* Dependent-work pause assessment: No dependent-work pause was triggered because no divergent or scope-changing discovery arose.
* Justification assessment: Fully supported by repository code, compiled ARM output, and test execution evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| None in active plan | Live Azure deployment, full 1,800 s / 600,000-event Azure SQL load testing, and ARM schema additions are declared plan non-goals. | Handled as optional post-Review follow-up candidates in RPI Agent `Follow-up` state. | Resolved for current task scope; operational follow-ups surfaced at post-Review checkpoint without treating them as task defects. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were identified within the approved Issue #144 repository boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No corrective `rpi-implement`, `rpi-plan`, or `rpi-research` pass required | All `FR-1`..`FR-5`, `NFR-1`..`NFR-2`, `PC-001`..`PC-005`, and user prompt acceptance criteria are satisfied. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* None inside the local repository scope of this task. External/follow-up operational candidates (live staging `src-deploy.yml` deployment receipt once Azure environment approvals run, activating API result-route wiring `ZF_AGENT_RESULT_ROUTE` when live worker post-back is enabled, and adopting native ARM `securityContext` if exposed in a future `Microsoft.App` API version) are recorded in the RPI session `prioritized_follow_ups` list and explicitly disclosed in `infra/README.md`.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01` through `P04` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests:infra/tests python3 -m unittest infra/tests/test_container_hosting_144.py -q` | `infra/tests/test_container_hosting_144.py` | Passed | `Ran 15 tests in 28.493s -> OK` (also verified under `env -u PYTHONPATH REQUIRE_AZ_BICEP=1` with `test_container_hosting_completeness.py`: `Ran 26 tests in 26.829s -> OK`). |
| `python3 -m ruff check infra/tests/test_container_hosting_144.py && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py` | New test module lint and formatting | Passed | `All checks passed!` and `1 file already formatted`. |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_container_hosting_144.py infra/scripts/pipeline.py infra/scripts/deploy.py && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_container_hosting_144.py infra/scripts/pipeline.py infra/scripts/deploy.py` | Hosted CI (`src-ci.yml`) `infra` ruff rules on all touched `infra` Python files | Passed | `All checks passed!` and `3 files already formatted`. Note: bare unconfigured `python3 -m ruff check infra` on `ruff 0.17.3` reports 112 pre-existing warnings (`SIM117`, `FURB167`, `EXE001`, etc.) solely on untouched legacy files/lines outside `src-ci.yml`'s `--select E,F,I,B,UP` contract; left untouched to preserve surgical diff boundaries. |
| `for pkg in core agents api orchestrator importer; do (cd "src/$pkg" && python3 -m ruff check . && python3 -m ruff format --check . && MYPYPATH=... python3 -m mypy --strict src); done && python3 -m mypy --strict infra/scripts/pipeline.py` | All 5 `src/*` packages + `pipeline.py` lint, format, and strict type checks | Passed | `0` ruff or formatting issues; `mypy --strict` succeeded across all `231` `src/*` source files + `infra/scripts/pipeline.py`. |
| `for file in infra/*.bicep infra/modules/*.bicep; do az bicep build --file "$file" --stdout > /dev/null && az bicep lint --file "$file"; done` | All Bicep templates | Passed | Clean compilation and lint (`0` warnings/errors, `az bicep v0.48.1`). |
| Full `infra/tests` discovery + touched `src/` unit suites + `python3 tools/rename-zava-tests.py` | Infrastructure, runtime entrypoint, restart/load, and branding regressions | Passed | `613/613` `infra/tests` passed (`611/613` without `PYTHONPATH`, plus `test_pipeline.py` `30/30` and `test_container_hosting_144.py` `15/15` with workspace `PYTHONPATH`); `src/api` targeted tests (`112` tests `OK`), `src/agents` `test_dispatch` (`15` tests `OK`), `src/orchestrator` functional tests (`140` tests `OK`), `src/importer` functional tests (`115` tests `OK`), `python3 -m zava_forward.{core,agents,orchestrator,importer}` (`0` exit), and `rename-zava-tests.py` (`25` tests `OK`). |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01-T01` through `P04-T02`), critique disposition (`PC-001` through `PC-005`), and all four unticked Issue #144 acceptance criteria are implemented cleanly, verified by deterministic semantic and negative/mutation tests in `infra/tests/test_container_hosting_144.py` and existing regression suites, backed by dated `2026-11-15` 60,000-home load and `SIGKILL` restart JSON artifacts, and documented honestly in `infra/README.md` without overclaiming production scale or live Azure execution.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | None in local repo scope (external/live follow-ups surfaced at RPI Agent post-Review checkpoint) | User selects follow-up work item, Stop, or manual mode after commit |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`infra/tests/test_container_hosting_144.py` `15/15`, full `infra/tests` `613/613`, `az bicep build/lint`, `ruff`, `mypy --strict`, touched `src/` unit suites, and `tools/rename-zava-tests.py`)
* Blockers: None

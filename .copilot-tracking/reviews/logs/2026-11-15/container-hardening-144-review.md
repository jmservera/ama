<!-- markdownlint-disable-file -->
# Review: Issue #144 Container Hosting Completeness and Hardening Contracts

## Scope and Evidence

* Task ID: issue-144-container-hardening
* Review date: 2026-11-15
* Review scope: Full task (`P01` through `P04`)
* Assessed boundary: Local container hardening, bounded `importer run` job entrypoint, compiled `containerapps.bicep` worker/job contracts and `demoDirectIngress` parity, `pipeline.py` `release-manifest.json` and PR `plan` / `deploy.py --apply` non-placeholder digest guards, dynamic `staff_azure.py` / `staff-azure-worker.py` hardening parity, deterministic unit/integration coverage, and `#136` bootstrap/inventory preservation (excluding live Azure rollout, which remains operator-gated).
* Plan: .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/container-hardening-144-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/container-hardening-144-research.md, git diff across `src/` and `infra/`, and Focused-tier validation execution outputs (`ruff`, `mypy`, `compileall`, `az bicep build`/`lint`, `bicep_inventory.py --check`, and 274 `TMPDIR=/dev/shm` `unittest` cases).

## Opening Review State

* Interpreted review goal: Independently verify once whether the completed `P01`..`P04` implementation satisfies `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-3`, all five critique dispositions (`PC-001`..`PC-005`), and the `Test Ownership and Bounds Lock` (`<= 17` added test methods, `0` removals) while preserving live Azure deployment boundaries (`AC-4` commit/clean-worktree closeout completes post-review).
* Review scope: Full task (`P01` through `P04`)
* Evidence readiness: Complete and reconciled (`container-hardening-144-plan.md`, `container-hardening-144-phase-details.md`, `container-hardening-144-plan-critique.md`, `container-hardening-144-changes.md`, and `container-hardening-144-research.md` are all present and synchronized).
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-4`, `## Critique Disposition` (`PC-001`..`PC-005`), and `## Test Ownership and Bounds Lock` in .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md.
* First comparison boundary: Reconcile `P01`..`P04` markers, implementation-time local judgment update, and source/test diffs against requirements and critique dispositions without mutating production code or planning artifacts.
* Active read-only boundaries: Read-only across repository source, tests, documentation, research, plan, details, critique, and changes record; write authority restricted exclusively to .copilot-tracking/reviews/logs/2026-11-15/container-hardening-144-review.md (and parent RPI Agent state JSON).
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass evidence comparison on 2026-11-15 across .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md, .copilot-tracking/details/2026-11-15/container-hardening-144-phase-details.md, .copilot-tracking/reviews/2026-11-15/container-hardening-144-plan-critique.md, .copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md, .copilot-tracking/research/2026-11-15/container-hardening-144-research.md, and the full 20-file repository diff (`19` modified + `src/importer/tests/test_cli_run.py`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Phase P01: Importer Bounded Job Entrypoint, Dockerfile `TMPDIR=/tmp`, and Staff Job Hardening | Reconciled | Checked `[x]` in plan; changes record documents `zava_forward.importer run`, `src/importer/tests/test_cli_run.py`, `TMPDIR=/tmp` across all 6 `src/` Dockerfiles, and `staff_azure.py` / `staff-azure-worker.py` hardening parity. |
| `P02` (`P02-T01`, `P02-T02`) | Phase P02: Bicep `importJob` Contract, Release Manifest Bundle, and Placeholder Guards | Reconciled | Checked `[x]` in plan; changes record documents `@minLength(1)`, `importJob` `command`/`args`/`ZF_STORE: 'mssql'`, `infra/README.md` notes, `pipeline.py` `release-manifest.json` + PR `plan` digest guard, and `deploy.py --apply` placeholder/`:latest` refusal. |
| `P03` (`P03-T01`, `P03-T02`) | Phase P03: Deterministic Container Hosting, Scaling, Revision, and Hardening Tests | Reconciled | Checked `[x]` in plan; changes record documents deterministic test additions across `test_container_hosting_144.py`, `test_container_hosting_completeness.py`, `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, and `test_staff_azure.py` (`12` total new test methods within `<= 17` cap, `0` removals). |
| `P04` (`P04-T01`) | Phase P04: Focused Validation Execution and Evidence Reconciliation | Reconciled | Checked `[x]` in plan; changes record documents passed `ruff check`, `ruff format --check`, `mypy`, `compileall`, `az bicep build`/`lint`, `bicep_inventory.py --check`, and 274 `TMPDIR=/dev/shm` `unittest` cases. |
| `## Follow-Up Items` | Follow-Up Items: Authorized live Azure deployment and runtime smoke verification for Issue #144 | Reconciled | Kept explicitly outside active `Pxx`/`Pxx-Txx` completion and acceptance claims in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/importer/src/zava_forward/importer/__main__.py`, `src/importer/tests/test_cli_run.py` | Added bounded `run` subcommand validating `enforce_from_env()`, `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, `SQL_SERVER`/`SQL_DATABASE` under `ZF_STORE=mssql`, and standby dispatch gate while preserving no-arg version print. | Diff verified; 4 unit tests in `test_cli_run.py` + subprocess tests in `test_container_hosting_144.py`. | `mypy` (`16` source files clean) + `test_cli_run.py` + `test_cli_and_privacy_boundaries.py` passed. | Reconciled (`FR-1`, `PC-001`, `PC-005`). |
| `P01-T02` | `src/api/Dockerfile`, `src/agents/Dockerfile`, `src/orchestrator/Dockerfile`, `src/importer/Dockerfile`, `src/api/Dockerfile.resident-demo`, `src/api/live-simulator.Dockerfile`, `infra/scripts/staff_azure.py`, `infra/scripts/staff-azure-worker.py` | Added `TMPDIR=/tmp` to runtime `ENV` across all 6 `src/` Dockerfiles while keeping `/app` root-owned (`0:0`) and `USER 10001:10001`; added `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, and `EmptyDir` `/tmp` + `/state` mounts in `staff_azure.py`, plus fail-closed `enforce_from_env()` (`exit 2`) in `staff-azure-worker.py`. | Diff verified across all 6 Dockerfiles and both staff Azure scripts. | `mypy` (`4` staff files clean), `test_container_hosting_144.py`, and `test_staff_azure.py` passed. | Reconciled (`FR-3`, `AC-1`, `PC-003`). |
| `P02-T01` | `infra/modules/containerapps.bicep`, `infra/README.md` | Added `@minLength(1)` on all 4 workload image parameters and explicit `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']`, and `{ name: 'ZF_STORE', value: 'mssql' }` on `importJob`; updated `#144` notes in `infra/README.md` while preserving `delivered-placeholder-workers` and `infra/main.bicep` stage-1 bootstrap defaults. | Compiled Bicep ARM JSON verified; `infra/main.bicep` untouched. | `az bicep build` + `az bicep lint` + `bicep_inventory.py --check` + `#136` tests passed. | Reconciled (`FR-2`, `AC-1`, `AC-3`, `PC-001`, `PC-005`). |
| `P02-T02` | `infra/scripts/pipeline.py`, `infra/scripts/deploy.py` | Added `build_release_manifest` and `verify_release_manifest` writing `release-manifest.json` (4 projects, 7 workloads, `HARDENING_CONTRACT`) and optional `summary["release_manifest"]` embed; strengthened PR `plan` to enforce `<registry>/<repo>@sha256:[0-9a-f]{64}` and reject `quickstart`; hardened `deploy.py --apply` against `quickstart` and `:latest` image overrides. | Diff verified; strict typing and offline unit fixtures confirmed. | `mypy --strict infra/scripts/pipeline.py`, `test_pipeline.py`, and `test_deploy.py` passed. | Reconciled (`FR-4`, `AC-1`, `PC-004`). |
| `P03-T01` | `infra/tests/test_container_hosting_144.py`, `infra/tests/test_container_hosting_completeness.py`, `infra/tests/test_bicep_policy.py` | Extended `#144` suite with 4 new methods covering all 6 Dockerfiles, `importer run`, `demoDirectIngress` (`False`/`True`) compiled workload names + scaling/cron rules, and `check-container.py`/`acr-cutover.yaml`/`container_hardening.py` parity; expanded Bicep workload inventory to all 10 symbols and added `ranking-publish` to `test_bicep_policy.py`. | Diff verified; exact added method count = `4` in `test_container_hosting_144.py`, `0` in `test_container_hosting_completeness.py`, `0` in `test_bicep_policy.py`. | Passed in combined 274-test `TMPDIR=/dev/shm` run. | Reconciled (`AC-2`, `AC-3`, `PC-002`, `PC-005`). |
| `P03-T02` | `infra/tests/test_pipeline.py`, `infra/tests/test_deploy.py`, `infra/tests/test_staff_azure.py` | Added 2 manifest/PR-plan tests in `test_pipeline.py`, 1 `--apply` refusal test in `test_deploy.py`, and 1 worker fail-closed hardening test + `job-staff-*` mount assertions in `test_staff_azure.py`. | Diff verified; total new test methods across entire task = `12` (`<= 17` cap), `0` removals. | Passed in combined 274-test `TMPDIR=/dev/shm` run. | Reconciled (`FR-3`, `FR-4`, `AC-2`, `PC-003`, `PC-004`). |
| `P04-T01` | `.copilot-tracking/changes/2026-11-15/container-hardening-144-changes.md`, `.copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md` | Executed full Focused-tier static, Bicep, inventory, and RAM-backed unittest validation and reconciled checklists and evidence record. | Recorded outputs in `container-hardening-144-changes.md`. | All commands exited `0`. | Reconciled (`NFR-1`, `NFR-2`, `AC-3`). |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T02` (`infra/scripts/pipeline.py` `deployment()`) | Guarded `summary["release_manifest"]` loading with `if manifest_path.is_file():` so unit tests that monkeypatch `pipeline.release_images` without writing disk files do not fail with `FileNotFoundError`, while real `release_images` runs write and embed `release-manifest.json`. | Unit test execution of existing `test_pipeline.py` `deployment` fixtures (`none` user decision needed; ordinary local judgment preserving `PC-004` intent). | Documented in `container-hardening-144-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (`PC-004` intent and `Ready` plan state preserved without scope or architectural change). | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five findings (`PC-001`..`PC-005`) from .copilot-tracking/reviews/2026-11-15/container-hardening-144-plan-critique.md have explicit direct dispositions recorded in `## Critique Disposition` of .copilot-tracking/plans/2026-11-15/container-hardening-144-plan.md and are verified in code and tests (`ZF_STORE=mssql` on `importJob`, exact `demoDirectIngress` names, `staff_azure.py`/`staff-azure-worker.py` `ZF_CONTAINER_HARDENING=enforced`, `release_tag()` / `--strict` typing / `deploy.py --apply` compatibility, and `#136` `delivered-placeholder-workers` + `importer run` subprocess refusal).
* Material revisions: None occurred during implementation; no second critique was needed or run.
* Dependent-work pause assessment: No material discovery required pausing dependent phases; `P01` -> `P02` -> `P03` -> `P04` executed in strict dependency order.
* Justification assessment: Supported by compiled ARM JSON, static analysis, and 274 passing tests.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Authorized live Azure rollout and runtime smoke/load verification for Issue #144 | Requires operator authorization, live Azure VNet/ACR/Container Apps environment access, and post-deploy smoke/25-user load execution outside offline repository scope. | Juan Manuel Servera (@jmservera): run authorized ACR release + Container Apps rollout and live load/hardening smoke verification when scheduled. | Open outside active local scope; routed as distinct follow-up work (not an implementation defect). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No implementation defects, decision gaps, or material evidence gaps were identified within the assessed Issue #144 local task boundary.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | No `rpi-implement`, `rpi-plan`, or `rpi-research` remediation required | All active-scope requirements (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), critique dispositions (`PC-001`..`PC-005`), and acceptance criteria (`AC-1`..`AC-3`; `AC-4` commit closeout owned by caller workflow) are conformant. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Authorized live Azure deployment, ACR digest promotion, and live 25-user load/hardening verification for Issue #144 (`Refs #144` boundary in `infra/README.md`): Distinct operator-gated follow-up owned by Juan Manuel Servera (@jmservera).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none (`P01`..`P04` complete; final local git commit on `feat/infra-144-container-hardening` executes immediately at task closeout per caller instructions).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 ...` | 12 touched Python files in `src/importer/` and `infra/` | Passed | `All checks passed!` (exit 0) |
| `python3 -m ruff format --isolated --line-length 100 --check ...` | 12 touched Python files in `src/importer/` and `infra/` | Passed | `12 files already formatted` (exit 0) |
| `(cd src/importer && PYTHONPATH=../core/src python3 -m mypy)` | `src/importer` package & tests | Passed | `Success: no issues found in 16 source files` |
| `python3 -m mypy --strict infra/scripts/pipeline.py` | `infra/scripts/pipeline.py` | Passed | `Success: no issues found in 1 source file` |
| `PYTHONPATH=src/core/src python3 -m mypy --follow-imports=silent --ignore-missing-imports infra/scripts/staff_azure.py infra/scripts/staff_blob.py infra/scripts/staff-azure-worker.py infra/scripts/credential_arm.py` | Staff Azure job & worker scripts | Passed | `Success: no issues found in 4 source files` |
| `python3 -m compileall -q src/core/src src/agents/src src/api/src src/orchestrator/src src/importer/src` | All 5 `src/` packages | Passed | Exit 0 |
| `az bicep build` & `az bicep lint` | `infra/modules/containerapps.bicep`, `infra/main.bicep` | Passed | Compiled and linted cleanly (exit 0) |
| `python3 infra/scripts/bicep_inventory.py --check` | Issue `#136` architecture & module inventory | Passed | `29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)` |
| `TMPDIR=/dev/shm PYTHONPATH=... python3 -m unittest ... -q` | 11 targeted unittest suites across `src/importer/tests/` and `infra/tests/` | Passed | `Ran 274 tests in 169.585s — OK` |
| `python3 tools/rpi-checks.py --all` | Full repository gate | Skipped | Explicitly excluded by caller validation tier (`Focused` tier requested) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01-T01` through `P04-T01`), requirement (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), critique refinement (`PC-001`..`PC-005`), and test-bounds constraint (`12 <= 17` added test methods, `0` removals) is implemented cleanly, reconciled across tracking artifacts, and backed by passing static, Bicep, inventory, and 274-test `TMPDIR=/dev/shm` unit/integration checks while preserving stage-1 bootstrap reproducibility and live Azure deployment boundaries.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | Distinct follow-up (`Refs #144` live Azure rollout & load verification) | Operator-gated live Azure ACR/Container Apps rollout and 25-user load smoke verification owned by Juan Manuel Servera (@jmservera) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused-tier `ruff check`, `ruff format --check`, `mypy` (`src/importer`, `--strict pipeline.py`, `staff_azure.py`/`staff-azure-worker.py`), `compileall`, `az bicep build`/`lint`, `bicep_inventory.py --check`, and 274 `TMPDIR=/dev/shm` `unittest` cases passed; full `tools/rpi-checks.py --all` skipped per caller Focused-tier instruction.
* Blockers: none

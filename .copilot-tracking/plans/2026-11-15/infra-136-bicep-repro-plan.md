<!-- markdownlint-disable-file -->
# RPI Plan: Issue 136 From-Empty Bicep Deployment Reproducibility

## Task Metadata

* Task ID: infra-136-bicep-repro
* Task slug: infra-136-bicep-repro
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/infra-136-bicep-repro-plan-critique.md

## Executive Summary

This plan delivers deterministic code, Bicep parameter templates, documentation, and unit/mutation test proofs for the Issue `#136` acceptance criterion *"A from-empty deployment is reproducible from the repository without undocumented steps"* across three machine-verified guarantees:

1. **Canonical Step Registration and Documentation (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`)**: Registers the ordered 6-step from-empty deployment contract (`FROM_EMPTY_STEP_ORDER` and `FROM_EMPTY_STEPS`) in `infra/scripts/pipeline.py`, documents the matching `### Canonical from-empty pipeline step registry` table in `infra/README.md` with zero undocumented manual steps, and verifies 1-to-1 alignment with checked-in repository templates/scripts and all 17 canonical `rebuild.py` stages while keeping `bicep_inventory.py`'s existing 12-row sequence and 5 CLI `operation` choices unbroken.
2. **Defaultless Parameter Coverage (`infra/main.bicep` vs `infra/parameters/*.bicepparam` + `pipeline.py`)**: Adds `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (`using '../main.bicep'`, non-deployable placeholder templates with private-by-default isolation), declares and AST-verifies `pipeline.INJECTED_PARAMETERS`, and statically verifies that every parameter in `infra/main.bicep` without a default (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`, discovered dynamically) is supplied in `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (as well as `pipeline.PARAMETER_FILES`) or explicitly injected by `infra/scripts/pipeline.py`.
3. **Deterministic Offline Full-Sequence Dry-Run**: Implements `execute_from_empty_dry_run` and `verify_from_empty_deployment_reproducibility` in `infra/scripts/reproducibility_check.py` (re-exported cleanly from `infra/scripts/pipeline.py`), executing all 6 canonical steps (`preflight` -> `what-if` -> `deploy` -> `sql-init` -> `seed` -> `smoke`) offline from repository files alone while exercising `pipeline.verify_environment`, `pipeline.parameters`, `pipeline.summarize_plan`, `pipeline.deployment`, `pipeline.check_sql`, and `pipeline.smoke` in-memory to produce a bit-for-bit deterministic SHA-256 sequence receipt.

### User Decisions and Requirements Highlights

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) in order under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, and `reviews/logs/2026-11-15/`) on branch `feat/infra-136-bicep-repro` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`).
* Deliver `verify_from_empty_deployment_reproducibility` (accessible from both `infra/scripts/pipeline.py` and `infra/scripts/reproducibility_check.py`) and `infra/tests/test_from_empty_reproducibility_136.py` proving sub-criteria (a), (b), and (c).
* Validate at the Focused tier (`python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`, `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check`, plus `mypy --strict` and `az bicep build-params`) without running `tools/rpi-checks.py`, then commit cleanly with the Copilot trailer without pushing.

### What You May Not Know

* `infra/scripts/bicep_inventory.py` AST-parses `parser.add_argument("operation", choices=...)` in `infra/scripts/pipeline.py` and `infra/tests/test_bicep_architecture_inventory_136.py` asserts those positional CLI choices equal `("plan", "deploy", "publish", "changed-images", "verify-environment")`; registering `FROM_EMPTY_STEPS` and `verify_from_empty_deployment_reproducibility` on `pipeline.py` while keeping positional `operation` choices intact preserves 100% compatibility with existing `#136` tests.
* Both `infra/tests/test_pipeline.py` and `infra/tests/test_environment_quota_parameters.py` load `infra/scripts/pipeline.py` via `importlib.util.spec_from_file_location` without `infra/scripts` on `sys.path` and without registering `"pipeline"` in `sys.modules`; keeping eager Python 3.12 annotations (omitting `from __future__ import annotations` in `pipeline.py`) and registering `sys.modules[spec.name] = mod` before `exec_module` in custom loaders prevents Python 3.12 `@dataclass` `AttributeError` crashes (`PC-001`).
* `infra/main.bicep` restricts `@allowed(['dev', 'test', 'pilot']) param environmentName` and `@allowed(['production', 'development']) param deploymentProfile`, so `infra/parameters/prod.bicepparam` targets the production profile with `environmentName = 'pilot'`, `deploymentProfile = 'production'`, `enableLocks = true`, and `allowPublicNetworkAccess = false`, while `execute_from_empty_dry_run` patches `PARAMETER_FILES` to route `"dev"`/`"pilot"` through `infra/parameters/{dev,prod}.bicepparam` under isolated `os.environ` (`clear=True`, omitting `GITHUB_STEP_SUMMARY`) (`PC-003`).

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, and `reviews/logs/2026-11-15/`) for Issue `#136` (caller prompt).
* Operate in worktree `/home/azureuser/source/ama-demo-wt/feat-136-bicep-repro` on branch `feat/infra-136-bicep-repro` targeting base branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) (caller prompt).
* Inspect `infra/scripts/pipeline.py`, `infra/main.bicep`, `infra/parameters/*.bicepparam`, and `infra/README.md` (caller prompt; completed in Research `C1`-`C22`).
* Add deterministic reproducibility verifier `verify_from_empty_deployment_reproducibility` (`infra/scripts/pipeline.py` / `infra/scripts/reproducibility_check.py`) and unit test suite `infra/tests/test_from_empty_reproducibility_136.py` verifying:
  * (a) Every step required for a from-empty deployment (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) is registered in `infra/scripts/pipeline.py` and documented in `infra/README.md` with zero undocumented manual steps;
  * (b) Every parameter in `infra/main.bicep` without a default is supplied in `infra/parameters/dev.bicepparam` / `prod.bicepparam` or explicitly injected by `infra/scripts/pipeline.py`;
  * (c) Dry-run / offline execution of the full from-empty pipeline sequence succeeds deterministically from repository files alone (caller prompt).
* Validate at Focused tier (`unittest discover -s infra/tests -p 'test_*.py' -q`, `ruff check`, `ruff format --isolated --line-length 100 --check`) without running `tools/rpi-checks.py` (caller prompt).
* Commit all changes and `.copilot-tracking/` RPI artifacts on `feat/infra-136-bicep-repro` with trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing or opening a PR (caller prompt).

## Goals

* Provide canonical, machine-checked registration and documentation of the 6-step from-empty deployment pipeline (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) across `infra/scripts/pipeline.py` and `infra/README.md` with zero undocumented manual steps.
* Guarantee complete defaultless parameter coverage for `infra/main.bicep` across `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, existing `infra/main*.bicepparam` files, and AST-verified `infra/scripts/pipeline.py` parameter injections.
* Prove deterministic, repeatable offline dry-run execution of the complete 6-step pipeline sequence from repository files alone, backed by positive and fail-closed mutation unit tests in `infra/tests/test_from_empty_reproducibility_136.py`.

## Scope and Non-Goals

### In Scope

* Adding `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (`using '../main.bicep'`) with non-deployable placeholder safeguards, private-by-default network settings, and `az bicep build-params` compatibility.
* Registering `FromEmptyStep`, `FROM_EMPTY_STEP_ORDER`, `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, `execute_from_empty_dry_run`, and `verify_from_empty_deployment_reproducibility` in `infra/scripts/pipeline.py` while preserving all existing CLI operations and contracts.
* Implementing `infra/scripts/reproducibility_check.py` with offline Bicep/`.bicepparam`/AST/Markdown verifiers, deterministic 6-step dry-run execution over real `pipeline.py` functions, and `--check` / `--dry-run` / `--json` CLI entrypoints.
* Updating `infra/README.md` (`## Layout` and `### Canonical from-empty pipeline step registry`) while preserving the 12-row `### Reproducible from-empty deployment sequence` table and all existing README test anchors.
* Authoring `infra/tests/test_from_empty_reproducibility_136.py` with positive and fail-closed mutation tests, running Focused validation, and committing locally.

### Non-Goals

* Running live Azure CLI commands against an Azure subscription or modifying `infra/main.bicep` resource definitions.
* Running `tools/rpi-checks.py` (explicitly excluded by caller prompt).
* Modifying `.github/workflows/*.yml` or reformatting unrelated pre-existing legacy files in `infra/`.
* Pushing to a remote repository or opening a pull request.

## Functional Requirements

* FR-1: Register the canonical 6-step from-empty deployment pipeline (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) in `infra/scripts/pipeline.py` and document it in `infra/README.md` (`### Canonical from-empty pipeline step registry`) with zero undocumented manual steps.
  * Observable acceptance criteria: `pipeline.FROM_EMPTY_STEPS` contains all 6 steps in exact canonical order `("preflight", "what-if", "deploy", "sql-init", "seed", "smoke")`; `infra/README.md` documents the exact 6 steps with matching repository script/template paths verified to exist on disk, matches per-step ordered `rebuild_stages` tuples and forms a disjoint 17-stage set partition across `rebuild.py` `STAGES`, bounds any pre-deployment human prerequisite (`preflight` subscription/`ama` RG/Entra SQL admin/CI reviewers) to named owner `Juan Manuel Servera (@jmservera)`, and rejects any missing step, reordered step, placeholder cell, missing script, or undocumented manual step.
* FR-2: Supply or explicitly inject every parameter in `infra/main.bicep` without a default value across `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, and `infra/scripts/pipeline.py`.
  * Observable acceptance criteria: `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` compile cleanly via `az bicep build-params`, declare only valid `infra/main.bicep` parameters without secret literals, and `verify_from_empty_deployment_reproducibility` dynamically extracts all defaultless parameters from `infra/main.bicep`, AST-verifies `pipeline.INJECTED_PARAMETERS` against `pipeline.parameters()` / `pipeline.deployment()`, and fails closed whenever a defaultless parameter is neither supplied in both `dev.bicepparam` and `prod.bicepparam` nor explicitly injected by `pipeline.py`.
* FR-3: Execute the full 6-step from-empty deployment sequence offline and deterministically from repository files alone.
  * Observable acceptance criteria: `execute_from_empty_dry_run(repo_root, environment)` runs `preflight` -> `what-if` -> `deploy` -> `sql-init` -> `seed` -> `smoke` for both `"dev"` and `"prod"` using only checked-in repository files and in-process `pipeline.py` execution adapters (zero network sockets, zero live `az`/`gh`/`docker` subprocesses, zero wall-clock or random state), returning `ok == True`, all 6 step statuses `"succeeded"`, and an identical SHA-256 `sequence_digest` across repeated calls and clean `os.environ` contexts.
* FR-4: Expose `verify_from_empty_deployment_reproducibility` seamlessly from both `infra/scripts/pipeline.py` and `infra/scripts/reproducibility_check.py` (plus CLI `--check`, `--dry-run`, `--json`).
  * Observable acceptance criteria: Calling `verify_from_empty_deployment_reproducibility(ROOT)` from either module returns `ReproducibilityReport(ok=True, errors=(), ...)` against the repository, works when loaded via `importlib.util.spec_from_file_location` without `infra/scripts` on `sys.path`, and `python3 infra/scripts/reproducibility_check.py --check --dry-run` exits `0`.
* FR-5: Prove criteria (a), (b), and (c) and fail-closed drift detection in `infra/tests/test_from_empty_reproducibility_136.py`.
  * Observable acceptance criteria: Unit tests cover live repository conformance, `az bicep build-params` compilation of `infra/parameters/{dev,prod}.bicepparam`, offline dry-run determinism across environments and stripped `os.environ`, and negative mutation cases for unregistered/missing steps, undocumented manual steps in `infra/README.md`, uncovered defaultless `main.bicep` parameters (plus positive coverage via `.bicepparam` alone or `pipeline.py` injection alone), AST drift in `pipeline.INJECTED_PARAMETERS`, and broken dry-run repository artifacts. All existing tests remain untouched (`none` removed; 1 new test file added with <= 16 focused test methods).

## Non-Functional Requirements

* NFR-1: Fast, pure-stdlib, offline reproducibility verification.
  * Objective threshold or evaluation condition: `verify_from_empty_deployment_reproducibility(ROOT)` completes in under 500 ms using Python 3.12 standard library modules only, with zero network or `az` subprocess invocations during the verifier/dry-run call.
  * Operating condition or verification approach, if needed: Verified via unit tests with stripped environment variables and subprocess guard assertions.
  * Observable acceptance criteria: Dry-run and verifier pass deterministically with subprocess execution forbidden inside `execute_from_empty_dry_run`.
* NFR-2: Strict type checking, formatting, lint compliance, and zero regression across existing `infra/tests`.
  * Objective threshold or evaluation condition: Zero issues from `mypy --strict`, bare `ruff check`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, and `ruff format --isolated --line-length 100 --check` on all created/modified Python files; 100% pass rate across `infra/tests` (`test_*.py`); zero `.ruff_cache`, `.mypy_cache`, or untracked scratch files left in the worktree.
  * Observable acceptance criteria: Validation commands exit `0` and `git status --ignored --short` shows no cache pollution.
* NFR-3: Tracking-artifact isolation from production files.
  * Objective threshold or evaluation condition: Zero `.copilot-tracking/` substrings in `infra/parameters/*.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/reproducibility_check.py`, `infra/tests/test_from_empty_reproducibility_136.py`, the `infra/README.md` diff, or commit messages.
  * Observable acceptance criteria: Automated substring scan confirms zero leaks.

## Acceptance Criteria

* AC-1: `verify_from_empty_deployment_reproducibility` confirms `preflight`, `what-if`, `deploy`, `sql-init`, `seed`, and `smoke` are registered in canonical order in `infra/scripts/pipeline.py` and documented in `infra/README.md` with verified repository artifacts and zero undocumented manual steps, while `python3 infra/scripts/bicep_inventory.py --check` continues to exit `0`.
* AC-2: `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` compile cleanly with `az bicep build-params`, and `verify_from_empty_deployment_reproducibility` confirms every defaultless parameter in `infra/main.bicep` is supplied in `dev.bicepparam`/`prod.bicepparam` or explicitly injected by `infra/scripts/pipeline.py`.
* AC-3: `execute_from_empty_dry_run` executes all 6 steps (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) offline from repository files alone for both `"dev"` and `"prod"` and yields identical deterministic `sequence_digest` values across repeated runs.
* AC-4: `infra/tests/test_from_empty_reproducibility_136.py` and the full `infra/tests` suite pass (`0` failures, `0` errors), and all touched/created `infra/` Python files pass `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict`.
* AC-5: All repository changes and `.copilot-tracking/` artifacts (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, `reviews/logs/2026-11-15/`, `rpi-sessions/2026-11-15/`) are committed cleanly on `feat/infra-136-bicep-repro` with the privacy-safe GitHub noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/infra-136-bicep-repro-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/infra-136-bicep-repro-plan-critique.md with Revise disposition resolved across PC-001 through PC-004 |
| Relevant research                | .copilot-tracking/research/2026-11-15/infra-136-bicep-repro-research.md                                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md is created by implementation as its evidence record                |
| Planning execution and readiness | Complete; Planning status Ready after applying PC-001 through PC-004                                                                     |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to rpi-implement                                                                 |

## Sources

* .copilot-tracking/research/2026-11-15/infra-136-bicep-repro-research.md: Cycle 1 findings `C1`-`C22` covering `pipeline.py` AST contracts, defaultless `main.bicep` parameters, `spec_from_file_location` loading, README table boundaries, and deterministic dry-run design.
* infra/scripts/pipeline.py: Existing CI deployment, parameter compilation/override, SQL private-access check, and post-deploy HTTP smoke implementation.
* infra/main.bicep and infra/modules/guard.bicep: Primary Bicep template parameter contracts and compile-time isolation guards.
* infra/main.bicepparam, infra/main.test.bicepparam, and infra/main.pilot.example.bicepparam: Existing environment parameter files and placeholder conventions.
* infra/scripts/bicep_inventory.py and infra/tests/test_bicep_architecture_inventory_136.py: Sibling `#136` verifier and test invariants that must remain unbroken.
* src/orchestrator/src/zava_forward/orchestrator/rebuild.py: Canonical 17-stage from-empty rebuild contract.
* infra/README.md: Infrastructure layout and `#136` reproducibility documentation register.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Add Environment Parameter Templates (`infra/parameters/*.bicepparam`)

* Intent: Create `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` targeting `../main.bicep` with non-deployable placeholder safety headers, private-by-default isolation, complete defaultless parameter coverage, and clean `az bicep build-params` compilation.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Author `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`

* Requirement and evidence: FR-2, AC-2 (`C7`, `C8`, `C9`, `C10`, `C14`, `C15`, `C16`)
* Expected result: Both parameter files exist under `infra/parameters/`, supply `alertEmail`, `sqlAdminGroupName`, and `sqlAdminGroupObjectId` alongside explicit dev/production-profile settings (`allowPublicNetworkAccess = false`, `apiMinReplicas = 0`, `enableLocks = true` in `prod.bicepparam`), contain zero secrets, and compile cleanly via `az bicep build-params`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Register Canonical Steps and Implement Deterministic Reproducibility Verifier & Dry-Run

* Intent: Register the 6 canonical from-empty pipeline steps and parameter injection metadata in `infra/scripts/pipeline.py` and implement `verify_from_empty_deployment_reproducibility` and `execute_from_empty_dry_run` in `infra/scripts/reproducibility_check.py` (re-exported in `pipeline.py`).
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Register `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, and verifier entrypoints in `infra/scripts/pipeline.py`

* Requirement and evidence: FR-1, FR-2, FR-4, NFR-2 (`C1`, `C2`, `C11`, `C12`, `C17`, `C18`)
* Expected result: `infra/scripts/pipeline.py` exposes `FromEmptyStep`, `FROM_EMPTY_STEP_ORDER`, `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, `execute_from_empty_dry_run`, and `verify_from_empty_deployment_reproducibility` using lazy `spec_from_file_location` delegation while keeping positional `operation` choices unchanged.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Implement `infra/scripts/reproducibility_check.py` static verifiers, deterministic offline dry-run executor, and CLI

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, NFR-3 (`C1`-`C9`, `C13`, `C17`-`C20`)
* Expected result: `infra/scripts/reproducibility_check.py` verifies step registration & README parity with zero undocumented manual steps, defaultless `main.bicep` parameter coverage across `.bicepparam` and AST-inspected `pipeline.py` injections, and deterministic 6-step offline dry-run execution across `"dev"` and `"prod"` with `--check`, `--dry-run`, and `--json` CLI flags.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Document Canonical From-Empty Step Registry in `infra/README.md`

* Intent: Update `infra/README.md` (`## Layout` and `### Canonical from-empty pipeline step registry`) so every canonical step (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) and parameter template is documented with zero undocumented manual steps and zero regressions in `bicep_inventory.py` or README-parsing tests.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update `## Layout` and add `### Canonical from-empty pipeline step registry` in `infra/README.md`

* Requirement and evidence: FR-1, AC-1, NFR-3 (`C12`, `C13`, `C22`)
* Expected result: `infra/README.md` lists `parameters/dev.bicepparam`, `parameters/prod.bicepparam`, and `scripts/reproducibility_check.py` in `## Layout`, documents the 6-row `### Canonical from-empty pipeline step registry` table immediately after `### Reproducible from-empty deployment sequence`, preserves all existing governance/container-hosting/inventory anchors, and passes both `bicep_inventory.py --check` and `reproducibility_check.py --check --dry-run`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Author Focused Unit & Mutation Tests, Validate, and Commit Cleanly

* Intent: Create `infra/tests/test_from_empty_reproducibility_136.py` proving criteria (a), (b), and (c) plus fail-closed mutations, run Focused validation (`unittest`, `ruff`, `mypy --strict`, `az bicep build-params`), and prepare the clean local handoff commit after Review.
* Dependencies: P01, P02, P03.

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Author `infra/tests/test_from_empty_reproducibility_136.py` and run Focused validation

* Requirement and evidence: FR-5, NFR-1, NFR-2, NFR-3, AC-1, AC-2, AC-3, AC-4 (`C12`, `C15`-`C21`)
* Expected result: `infra/tests/test_from_empty_reproducibility_136.py` passes both standalone (`env -u PYTHONPATH`) and within full `infra/tests` discovery (`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src`), and all touched/created Python files pass bare `ruff check`, `--isolated` CI `ruff check` + `ruff format --check`, and `mypy --strict` with zero leftover caches.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md

## Dependencies

* Existing Issue `#136` inventory baseline (`infra/scripts/bicep_inventory.py`, `infra/tests/test_bicep_architecture_inventory_136.py`, and `infra/README.md` tables from commit `252125ad2`): Must remain 100% green alongside the new reproducibility verifier.
* Azure CLI Bicep compiler (`az bicep build-params`): Available locally (`az bicep` installed) to validate `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` compilation in `P01-T01` and `P04-T01`, while `verify_from_empty_deployment_reproducibility` itself executes in pure Python stdlib without requiring `az` at runtime.
* Workspace `src/*/src` paths on `PYTHONPATH` during full `infra/tests` runs: Required by pre-existing `SmokeTests.test_installed_local_api_denies_unauthenticated_requests` (`test_pipeline.py`) when wheels are not installed into system site-packages.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 [High]            | resolved    | Prohibited `from __future__ import annotations` in `infra/scripts/pipeline.py`, required `sys.modules[spec.name] = mod` prior to `exec_module` in custom loaders (`P02-T01`, `P02-T02`), and added an unregistered-`sys.modules` `spec_from_file_location` regression assertion in `P04-T01`. |
| PC-002 [High]            | resolved    | Updated `FR-1`, `P02-T02` Check (a), and `P03-T01` to verify per-step ordered `rebuild_stages` parity between `pipeline.FROM_EMPTY_STEPS` and `infra/README.md` plus a disjoint 17-stage partition (`len` + `frozenset` with zero duplicates) across `rebuild.py` `STAGES`, while explaining two-pass Bicep consolidation in `infra/README.md`. |
| PC-003 [Medium]          | resolved    | Updated `P02-T02` Check (c) and `P04-T01` so `execute_from_empty_dry_run` patches `PARAMETER_FILES` to route `"dev"` -> `"parameters/dev.bicepparam"` and `"pilot"` -> `"parameters/prod.bicepparam"`, parses the exact `--file` argument in the in-memory `build-params` stub, isolates `os.environ` via `patch.dict(os.environ, synthetic_env, clear=True)` omitting `GITHUB_STEP_SUMMARY`, and tests non-pollution of `GITHUB_STEP_SUMMARY` and ambient env vars. |
| PC-004 [Medium]          | resolved    | Updated `P01-T01`, `P02-T02`, and `P04-T01` to specify multi-line `[]`/`{}`/`()` depth-tracked Bicep array/object literal parsing in `parse_bicepparam_file`, enforce zero `"chat"`, zero `"AutoPause"` in `prod.bicepparam`, and zero retired `mvp/`/`prototype/`/`zavaforward_mvp` tokens, cross-check offline parsed values against `az bicep build-params`, and construct synthetic secret test strings dynamically so `test_iot_credential_hygiene.py` stays clean. |

## Follow-Up Items

* Add `infra/scripts/reproducibility_check.py`, `infra/scripts/bicep_inventory.py`, `infra/tests/test_from_empty_reproducibility_136.py`, and `infra/tests/test_bicep_architecture_inventory_136.py` to the explicit `ruff` and `mypy --strict` file lists in `.github/workflows/src-ci.yml` during the next CI workflow maintenance PR (excluded here to keep Focused-tier scope strictly within `infra/`).
* Replace default placeholder quickstart images in `infra/main.bicep` once ACR digest bootstrap defaults are retired under Issue `#144`.
* Record owner cost sign-off in `infra/defender-decision.json` before enabling paid Microsoft Defender for Cloud plans or switching Azure Policy from `DoNotEnforce` to `Default` under Issue `#147`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md
* Ready phase or task: P01 (`P01-T01`)
* Remaining provisional question or blocker: None

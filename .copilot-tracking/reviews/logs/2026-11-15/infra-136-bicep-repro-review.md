<!-- markdownlint-disable-file -->
# Review: Issue 136 From-Empty Bicep Deployment Reproducibility

## Scope and Evidence

* Task ID: infra-136-bicep-repro
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Assessed boundary: Issue `#136` acceptance criterion *"A from-empty deployment is reproducible from the repository without undocumented steps"* across criteria (a) 6-step registration & `infra/README.md` parity with zero undocumented manual steps, (b) defaultless `infra/main.bicep` parameter coverage across `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, and `infra/scripts/pipeline.py` injection, (c) deterministic offline dry-run execution from repository files alone, and Focused-tier validation without running `tools/rpi-checks.py`.
* Plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-repro-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/infra-136-bicep-repro-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/infra-136-bicep-repro-research.md, `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/reproducibility_check.py`, `infra/README.md`, `infra/tests/test_from_empty_reproducibility_136.py`, and Focused-tier validation outputs.

## Opening Review State

* Interpreted review goal: Verify once, read-only, that completed phases `P01`-`P04` satisfy `FR-1`..`FR-5`, `NFR-1`..`NFR-3`, `AC-1`..`AC-4`, and critique dispositions `PC-001`..`PC-004`, with reconciled tracking artifacts and complete Focused validation evidence.
* Review scope: Full task (`P01` through `P04`)
* Evidence readiness: Ready; plan (`P01`-`P04` `[x]`), phase details (`Complete`), single-pass plan critique (`PC-001`..`PC-004` `resolved`), and reconciled changes record are all present and aligned.
* Acceptance basis: `FR-1`..`FR-5`, `NFR-1`..`NFR-3`, `AC-1`..`AC-4`, `PC-001`..`PC-004`, and caller validation constraints.
* First comparison boundary: Compare `git status` and `git diff` across `infra/` against `P01`-`P04` specifications, critique resolutions, and repository hygiene boundaries (read-only).
* Active read-only boundaries: Read-only comparison across repository sources and prior RPI artifacts; write authority restricted solely to `.copilot-tracking/reviews/logs/2026-11-15/infra-136-bicep-repro-review.md`.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-task read-only review on 2026-11-15 across `P01`-`P04`, `PC-001`-`PC-004`, `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/reproducibility_check.py`, `infra/README.md`, `infra/tests/test_from_empty_reproducibility_136.py`, and Focused-tier validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | `Environment Parameter Templates (P01, P01-T01)` | Reconciled | `[x]` in plan, `Complete` in phase details, and compiled via `az bicep build-params` |
| `P02`, `P02-T01`, `P02-T02` | `Canonical Step Registry, Offline Verifier, and Deterministic Dry-Run (P02, P02-T01, P02-T02)` | Reconciled | `[x]` in plan, `Complete` in phase details, and verified via both `pipeline.py` and `reproducibility_check.py` |
| `P03`, `P03-T01` | `Infrastructure Documentation Parity (P03, P03-T01)` | Reconciled | `[x]` in plan, `Complete` in phase details; `bicep_inventory.py --check` and `reproducibility_check.py --check` both pass |
| `P04`, `P04-T01` | `Focused Unit and Fail-Closed Mutation Test Suite (P04, P04-T01)` | Reconciled | `[x]` in plan, `Complete` in phase details; `11/11` focused tests and `642/642` `infra/tests` pass |
| `## Follow-Up Items` | `## Follow-Up Items` (3 distinct entries) | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` scope and mirrored accurately in the changes record |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` (`P01`) | `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam` | Added canonical dev (`environmentName = 'dev'`, `deploymentProfile = 'development'`) and production-profile (`environmentName = 'pilot'`, `deploymentProfile = 'production'`, `enableLocks = true`, `sqlTier = 'provisioned'`) parameter templates (`using '../main.bicep'`) supplying all 3 defaultless `main.bicep` parameters (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`) with safe placeholders and `allowPublicNetworkAccess = false`. | Both files compile cleanly via `az bicep build-params --stdout` and match offline `_BicepValueParser` 1:1. | Passed (`az bicep build-params`, `test_criterion_b_bicepparam_compiles_via_az_bicep_and_matches_offline_parser`, `test_governance.py`, `test_iot_credential_hygiene.py`, `test_cutover_audit.py`) | Reconciled |
| `P02-T01` (`P02`) | `infra/scripts/pipeline.py` | Registered `FromEmptyStep` (without `from __future__ import annotations` for Python 3.12 `spec_from_file_location` compatibility), `FROM_EMPTY_STEP_ORDER`, `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, `execute_from_empty_dry_run`, and `verify_from_empty_deployment_reproducibility` while keeping positional CLI `operation` choices untouched. | `unregistered_pipeline.verify_from_empty_deployment_reproducibility(ROOT)` succeeds and equals `reproducibility_check.verify_from_empty_deployment_reproducibility(ROOT)`. | Passed (`test_from_empty_reproducibility_136.py`, `test_pipeline.py`, `test_bicep_architecture_inventory_136.py`, `ruff`, `mypy --strict`) | Reconciled |
| `P02-T02` (`P02`) | `infra/scripts/reproducibility_check.py` | Implemented pure-stdlib static verification for Criteria (a) and (b) plus deterministic 6-step offline dry-run (`execute_from_empty_dry_run`) for Criterion (c) with `os.environ` `clear=True` isolation, `subprocess.run` prohibition, `PARAMETER_FILES` routing to `parameters/{dev,prod}.bicepparam`, and `--check`/`--dry-run`/`--json` CLI flags. | `reproducibility_check.py --check` exits `0` (`74` total params, `3` defaultless covered, `6` steps partitioning `17` rebuild stages, repeatable `dev`/`prod` SHA-256 digests). | Passed (`11/11` `test_from_empty_reproducibility_136.py`, `ruff`, `mypy --strict`) | Reconciled |
| `P03-T01` (`P03`) | `infra/README.md` | Listed `parameters/dev.bicepparam`, `parameters/prod.bicepparam`, and `scripts/reproducibility_check.py` in `## Layout` and documented `### Canonical from-empty pipeline step registry` with explicit `@jmservera` preflight ownership and `none (automated from repository files)` on all 5 automated steps while preserving the 12-row `bicep_inventory.py` sequence table. | Both `bicep_inventory.py --check` and `reproducibility_check.py --check` exit `0` with zero undocumented manual steps. | Passed (`bicep_inventory.py --check`, `reproducibility_check.py --check`, `test_documentation_links.py`, `test_governance.py`) | Reconciled |
| `P04-T01` (`P04`) | `infra/tests/test_from_empty_reproducibility_136.py` | Authored 11 positive and fail-closed mutation tests proving Criteria (a), (b), and (c), `az bicep build-params` parity, unregistered-`sys.modules` loading, AST injection drift detection, dynamic secret-literal rejection, and ambient environment isolation. | `11/11` tests pass standalone (`env -u PYTHONPATH`) and within full `642`-test `infra/tests` discovery. | Passed (`11/11` standalone, `642/642` `infra/tests`, `ruff`, `mypy --strict`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T02`, `P04-T01` | Recorded exact comment-aware `infra/main.bicep` parameter count (`74` total top-level `param` declarations rather than early `61` prose estimate, with the identical `3` defaultless parameters `alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`) and `.to_dict()` structural comparison across independently loaded module instances in `test_live_repository_passes_via_pipeline_and_reproducibility_check`. | Direct execution of `parse_bicep_parameters` and `unittest`; no user decision needed (local factual/assertion refinement). | Recorded in `.copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md` under `## Implementation-Time Plan and Detail Updates`; `Phase Index` and plan markers reconciled. | Not needed (preserves `Ready` plan and `PC-001`..`PC-004` resolutions without scope or acceptance change). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001` High Python 3.12 `@dataclass` without `from __future__ import annotations` + `sys.modules` registration; `PC-002` High ordered per-step `rebuild_stages` + disjoint 17-stage partition; `PC-003` Medium `PARAMETER_FILES` dry-run routing + `os.environ` `clear=True` isolation without `GITHUB_STEP_SUMMARY`; `PC-004` Medium multi-line bracket-depth `.bicepparam` parser + `az bicep build-params` parity + dynamic secret test strings + cutover hygiene) are marked `resolved` in `## Critique Disposition` and verified in code and tests.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause was required; phases executed strictly in dependency order (`P01` -> `P02` -> `P03` -> `P04`).
* Justification assessment: Supported by direct code, compiler, static-analysis, and unit-test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Add `reproducibility_check.py`, `bicep_inventory.py`, `test_from_empty_reproducibility_136.py`, and `test_bicep_architecture_inventory_136.py` to explicit `ruff` and `mypy --strict` file lists in `.github/workflows/src-ci.yml` | Focused-tier task deliberately kept edits inside `infra/` rather than altering `.github/workflows/src-ci.yml` | Next CI workflow maintenance PR | Distinct follow-up route (`prioritized_follow_ups` rank 1) |
| Replace remaining placeholder quickstart default images in `infra/main.bicep` once ACR digest bootstrap defaults are retired (`#144`) | Tracked separately under Issue `#144` container release automation | Issue `#144` implementation | Distinct follow-up route (`prioritized_follow_ups` rank 2) |
| Record owner cost sign-off in `infra/defender-decision.json` before enabling Defender for Cloud pricing plans or `Default` Azure Policy enforcement (`#147`) | Human budget and governance gate owned by `@jmservera` | `@jmservera` under Issue `#147` | Distinct follow-up route (`prioritized_follow_ups` rank 3) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

None. Zero defects, decision gaps, or material evidence gaps were identified across `P01`-`P04`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No defect or gap remediation required | All active plan requirements and acceptance criteria are Conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Distinct plan follow-ups only (not defects in `P01`-`P04`): explicit `src-ci.yml` `ruff`/`mypy` file-list registration, Issue `#144` placeholder image retirement, and Issue `#147` owner Defender/policy cost sign-off.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`-`P04` complete; local commit handoff owned by parent workflow).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `az bicep build-params --file infra/parameters/{dev,prod}.bicepparam --stdout` | `infra/parameters/dev.bicepparam`, `infra/parameters/prod.bicepparam` | Passed | Both compile cleanly (`dev`: 26 params, `prod`: 27 params) and match offline `_BicepValueParser` 1:1 |
| `python3 infra/scripts/reproducibility_check.py --check` & `--dry-run --environment {dev,prod}` | `infra/` reproducibility contract | Passed | Exit 0; 6 canonical steps, 3/74 defaultless params covered, repeatable `dev`/`prod` sequence digests |
| `python3 infra/scripts/bicep_inventory.py --check` | `infra/README.md` & 20-module inventory | Passed | Exit 0; zero regressions in existing Issue `#136` architecture inventory |
| `env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m unittest infra/tests/test_from_empty_reproducibility_136.py -v` | `infra/tests/test_from_empty_reproducibility_136.py` | Passed | `Ran 11 tests in 14.781s - OK` without `src/*` on `PYTHONPATH` |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` | Full `infra/tests` suite | Passed | `Ran 642 tests in 230.400s - OK (skipped=4)` |
| `test_iot_credential_hygiene.py`, `test_cutover_audit.py`, `tools/rename-zava-tests.py` | Repo-wide secret & cutover scanners | Passed | `21/21` and `25/25` passed (`OK`) |
| `python3 -m ruff check --no-cache` & `python3 -m ruff format --no-cache --isolated --line-length 100 --check` | Modified/created `infra/` Python files and directory-wide `infra/` | Passed | `0` issues on all new files under bare `ruff check` and `0` issues across all 3 touched/created files (`pipeline.py`, `reproducibility_check.py`, `test_from_empty_reproducibility_136.py`) under `src-ci.yml`'s `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` (`3 files already formatted`); pre-existing lint/format findings in untouched legacy `infra/` files left untouched |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m mypy --strict --no-incremental --cache-dir=/dev/null infra/scripts/pipeline.py infra/scripts/reproducibility_check.py infra/tests/test_from_empty_reproducibility_136.py` | Touched/created `infra/` Python files | Passed | `Success: no issues found in 3 source files` |
| `python3 tools/rpi-checks.py` | Full RPI gate | Skipped | Explicitly prohibited by caller instructions (Focused validation tier) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases (`P01`-`P04`), functional and non-functional requirements (`FR-1`..`FR-5`, `NFR-1`..`NFR-3`), acceptance criteria (`AC-1`..`AC-4`), and single-pass critique dispositions (`PC-001`..`PC-004`) are implemented, reconciled across tracking artifacts, and proven by deterministic static checks, `az bicep build-params` compilation, offline 6-step dry-run execution, `11/11` focused unit/mutation tests, and `642/642` `infra/tests` suite execution with zero open defects and zero `.copilot-tracking/` leaks in production files.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Plan `## Follow-Up Items` (`src-ci.yml` file-list registration, Issue `#144`, Issue `#147`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`az bicep build-params`, `reproducibility_check.py --check --dry-run`, `bicep_inventory.py --check`, `11/11` `test_from_empty_reproducibility_136.py`, `642/642` `infra/tests`, cross-suite hygiene/cutover tests, `ruff check`, `ruff format --check`, `mypy --strict`; `tools/rpi-checks.py` skipped per caller constraint)
* Blockers: None

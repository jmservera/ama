<!-- markdownlint-disable-file -->
# RPI Changes: Issue 136 From-Empty Bicep Deployment Reproducibility

## Metadata

* Task ID: infra-136-bicep-repro
* Related plan: .copilot-tracking/plans/2026-11-15/infra-136-bicep-repro-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-136-bicep-repro-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`), `P04` (`P04-T01`)
* All remaining active-plan markers: None
* Status basis: All four phases (`P01`-`P04`) and five tasks (`P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`, `P04-T01`) are implemented, reconciled, and verified under the Focused validation tier.

## Execution Summary

Implemented deterministic offline proof that a Zava Forward from-empty Azure deployment is reproducible from repository artifacts alone without undocumented manual steps (Issue `#136`). Added `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` (`using '../main.bicep'`), registered the 6 canonical from-empty pipeline steps (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`) and parameter injection metadata in `infra/scripts/pipeline.py`, created the pure-stdlib verifier and deterministic offline dry-run executor in `infra/scripts/reproducibility_check.py`, documented the canonical 6-step registry in `infra/README.md`, and verified positive and fail-closed mutation coverage in `infra/tests/test_from_empty_reproducibility_136.py` alongside the full 642-test `infra/tests` suite.

## Completed Work

### Environment Parameter Templates (`P01`, `P01-T01`)

* Created `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam` targeting `using '../main.bicep'` with explicit non-deployable placeholder headers (`00000000-0000-0000-0000-000000000000`, `invalid.example`), `allowPublicNetworkAccess = false`, `apiMinReplicas = 0`, `enableLocks = true` in `prod.bicepparam`, `sqlComputeTier = 'Provisioned'` in `prod.bicepparam` (zero `'AutoPause'`), explicit `openAiModelDeployments` (`gpt-4.1-mini` and `text-embedding-3-large`, zero `'chat'`), and explicit values for all 3 defaultless `infra/main.bicep` parameters (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`).
* Verified both `.bicepparam` files compile cleanly via `az bicep build-params --stdout` and match the pure-Python offline `.bicepparam` literal parser 1:1.

### Canonical Step Registry, Offline Verifier, and Deterministic Dry-Run (`P02`, `P02-T01`, `P02-T02`)

* Updated `infra/scripts/pipeline.py` (preserving Python 3.12 runtime type objects without `from __future__ import annotations` and keeping positional CLI `operation` choices unchanged) to export `FromEmptyStep`, `FROM_EMPTY_STEP_ORDER`, `FROM_EMPTY_STEPS`, `ENVIRONMENT_PARAMETER_FILES`, `INJECTED_PARAMETERS`, `execute_from_empty_dry_run`, and `verify_from_empty_deployment_reproducibility`.
* Created `infra/scripts/reproducibility_check.py` providing:
  * Criterion (a) verification: exact 6-step order (`preflight`, `what-if`, `deploy`, `sql-init`, `seed`, `smoke`), backing repository artifact existence, ordered per-step `rebuild_stages` parity between `pipeline.FROM_EMPTY_STEPS` and `infra/README.md`, disjoint 17-stage partition across `src/orchestrator/src/zava_forward/orchestrator/rebuild.py`, and fail-closed regex scanning of from-empty `infra/README.md` sections for undocumented manual portal/ClickOps steps.
  * Criterion (b) verification: comment-aware Bicep `param` parser (`parse_bicep_parameters`, verifying all 74 `param` declarations and 3 defaultless parameters in `infra/main.bicep`), multi-line bracket-depth `.bicepparam` parser (`parse_bicepparam_file`) across `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`, secret-like literal and safety invariants (`allowPublicNetworkAccess is False`, no `chat` OpenAI deployment, no `AutoPause` in `prod.bicepparam`, no retired `mvp/`/`prototype/`/`zavaforward_mvp` tokens), and AST verification of `pipeline.INJECTED_PARAMETERS` against `deployment_parameters()` in `infra/scripts/pipeline.py`.
  * Criterion (c) deterministic offline dry-run (`execute_from_empty_dry_run`): executes all 6 canonical steps in order across `"dev"` and `"prod"` (mapping `"prod"` to `pipeline.py`'s `"pilot"` deployment slot with `PARAMETER_FILES` patched to `infra/parameters/dev.bicepparam` and `infra/parameters/prod.bicepparam`), isolating `os.environ` (`clear=True`, omitting `GITHUB_STEP_SUMMARY`) and stubbing external Azure/SQL/HTTP boundaries from repository files alone to produce deterministic SHA-256 sequence digests (`dev`: `7d8561e48548f1492a6e22b83dd383391650af2bccfa7879448b6ae6bb5831d6`, `prod`: `192f278ed08bee80e7f96053c84d89070bd51ed022ee296eb38d82387f8de1e1`).
  * CLI entrypoint supporting `--repo-root`, `--check`, `--dry-run`, `--environment {dev,prod,both}`, and `--json`.

### Infrastructure Documentation Parity (`P03`, `P03-T01`)

* Updated `infra/README.md` `## Layout` to list `parameters/dev.bicepparam`, `parameters/prod.bicepparam`, and `scripts/reproducibility_check.py`.
* Added `### Canonical from-empty pipeline step registry` immediately beneath `### Reproducible from-empty deployment sequence`, documenting the exact 6-row step table (`Step`, `Pipeline operation`, `Backing script / module`, `Rebuild stages`, `Purpose`) and explaining how `rebuild.py`'s two-pass `bicep-foundation` / `bicep-workloads` model consolidates into the single `deploy` (`deploy-rg`) step over `infra/main.bicep` while preserving the existing 12-row `bicep_inventory.py` sequence table unchanged.

### Focused Unit and Fail-Closed Mutation Test Suite (`P04`, `P04-T01`)

* Created `infra/tests/test_from_empty_reproducibility_136.py` (`11` test methods in `FromEmptyReproducibility136Tests`) covering live-repository parity (`pipeline.verify_from_empty_deployment_reproducibility()` vs `reproducibility_check.verify_from_empty_deployment_reproducibility()` and `bicep_inventory.verify_all()`), unregistered-`sys.modules` `spec_from_file_location` safety (`PC-001`), Criterion (a) step/artifact/stage-partition/README manual-step fail-closed mutations (`PC-002`), Criterion (b) defaultless parameter resolution via `.bicepparam` or `pipeline.py` injection, AST drift/unknown param/secret literal fail-closed mutations, and exact `az bicep build-params` value parity (`PC-004`), Criterion (c) deterministic offline dry-run repeatability, `GITHUB_STEP_SUMMARY` & ambient env isolation, `.bicepparam` sensitivity (`PC-003`), and CLI `--check`/`--dry-run --json` exit codes.

## Implementation-Time Plan and Detail Updates

* Local factual refinement (`P02-T02` / `P04-T01`): Comment-aware parsing of `infra/main.bicep` (`parse_bicep_parameters`) identifies `74` total top-level `param` declarations (rather than the rough `61` estimate in early research prose) with the exact same `3` defaultless parameters (`alertEmail`, `sqlAdminGroupName`, `sqlAdminGroupObjectId`). No plan architecture, scope, or acceptance criteria changed.
* Local test comparison refinement (`P04-T01`): Compared `from_pipeline.to_dict()` and `from_repro.to_dict()` in `test_live_repository_passes_via_pipeline_and_reproducibility_check` because the test suite loads a separate module instance (`_test_reproducibility_check_136`) from `pipeline._load_reproducibility_module()` (`_ama_infra_reproducibility_check`), making their `ReproducibilityReport` classes distinct runtime class objects with identical serialized payloads, and passed `ROOT` to `INVENTORY_MOD.verify_all(ROOT)`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `az bicep build-params` (`dev.bicepparam`, `prod.bicepparam`) | `P01-T01` | Passed | Both compile cleanly (`dev`: 9 params, `prod`: 20 params) with zero errors |
| `python3 infra/scripts/reproducibility_check.py --check` and `--dry-run --environment {dev,prod}` | `P02`, `P03` | Passed | Exit 0; `total_bicep_params=74`, `defaultless_params=['alertEmail', 'sqlAdminGroupName', 'sqlAdminGroupObjectId']`, `steps=6`, `dev` and `prod` deterministic sequence digests verified |
| `python3 infra/scripts/bicep_inventory.py --check` | `P03-T01` | Passed | Exit 0; existing 10-module and 12-row `infra/README.md` inventory parity preserved |
| `env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m unittest infra/tests/test_from_empty_reproducibility_136.py -v` | `P04-T01` | Passed | 11/11 tests passed in 14.781s without `src/*` on `PYTHONPATH` (matches hosted `src-ci.yml` `infra-tests` environment) |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` | Full `infra/tests` suite | Passed | 642 tests ran in 230.400s: `OK (skipped=4)` |
| Cross-suite credential & cutover scanners (`test_iot_credential_hygiene.py`, `test_cutover_audit.py`, `tools/rename-zava-tests.py`) | Repo-wide scanner safety (`PC-004`) | Passed | `21/21` (`test_iot_credential_hygiene` + `test_cutover_audit`) and `25/25` (`rename-zava-tests.py`) passed |
| `ruff check --no-cache` & `ruff format --no-cache --isolated --line-length 100 --check` on touched/created files | `pipeline.py`, `reproducibility_check.py`, `test_from_empty_reproducibility_136.py` | Passed | `0` issues on `reproducibility_check.py` and `test_from_empty_reproducibility_136.py` under bare `ruff check`; `0` issues across all 3 files under `src-ci.yml`'s `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` (`3 files already formatted`). (Directory-wide `ruff check infra/` and `ruff format --check infra/` report pre-existing findings in untouched legacy files, including 2 pre-existing root-config rules on untouched lines 1 and 451 of `pipeline.py` and 21 untouched files for formatting, intentionally left untouched to avoid unrelated diff churn.) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m mypy --strict --no-incremental --cache-dir=/dev/null` | `pipeline.py`, `reproducibility_check.py`, `test_from_empty_reproducibility_136.py` | Passed | `Success: no issues found in 3 source files` |
| `tools/rpi-checks.py` | Full RPI gate | Skipped | Explicitly prohibited by user prompt (`Focused` validation tier; do NOT run `tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`-`P04` and all `P01-T01`..`P04-T01` checked `[x]` in plan; `Phase Index` marked `Complete` in phase details)
* Completed-work evidence and handoff prose: Reconciled in `.copilot-tracking/changes/2026-11-15/infra-136-bicep-repro-changes.md` with zero `.copilot-tracking/` substrings in production `infra/` diff
* Validation, blockers, remaining work, and follow-up items: Reconciled; all Focused checks green, zero blockers, zero remaining active-plan markers
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in active plan (`P01`-`P04` complete). Post-implementation `rpi-review` and local frozen-HEAD commit remain in the parent RPI loop.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/infra-136-bicep-repro-plan.md, `## Follow-Up Items`
* Add `infra/scripts/reproducibility_check.py`, `infra/scripts/bicep_inventory.py`, `infra/tests/test_from_empty_reproducibility_136.py`, and `infra/tests/test_bicep_architecture_inventory_136.py` to explicit `ruff` and `mypy --strict` file lists in `.github/workflows/src-ci.yml`.
* Replace default placeholder quickstart images in `infra/main.bicep` once ACR digest bootstrap defaults are retired under Issue `#144`.
* Record owner cost sign-off in `infra/defender-decision.json` before enabling paid Microsoft Defender for Cloud plans or switching Azure Policy from `DoNotEnforce` to `Default` under Issue `#147`.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`-`P04`); all markers (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P04`, `P04-T01`) completed
* Validation coverage: Focused tier complete (`az bicep build-params`, `11/11` `test_from_empty_reproducibility_136.py`, `642/642` `infra/tests`, cross-suite hygiene/cutover tests, `ruff check`, `ruff format --check`, `mypy --strict`)
* Blockers: None
* Current plan and detail updates: Minor factual note (`74` total `param` declarations in `infra/main.bicep` with the same `3` defaultless parameters); `Phase Index` and checklist markers updated to `Complete` / `[x]`
* Planning and critique state: Ready (`PC-001` through `PC-004` resolved)
* Follow-up items: 3 follow-up items tracked in plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

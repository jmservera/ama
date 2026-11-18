<!-- markdownlint-disable-file -->
# RPI Plan: Environment Strategy, Region and Quota Parameterization, Recorded Checks, and Architecture Documentation (Issue #137)

## Task Metadata

* Task ID: issue-137
* Task slug: infra-137-env-quotas
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md

## Executive Summary

This plan delivers and proves the repository-verifiable engineering, guard, documentation, and deterministic test contract for the remaining acceptance criterion of Issue `#137` (`Environment strategy and parameter sets (dev, test, pilot)`): `- [ ] Region and quota choices are parameters with recorded checks, not assumptions`, on branch `feat/infra-137-env-quotas` (stacked on `origin/feat/demo-164-chat-grounding-provenance-0900`, PR `#1641`).

Research (`C1`-`C19`, `W1`-`W2`) and single-pass plan critique (`PC-001`-`PC-006`) confirmed that `infra/main.bicep` and `infra/modules/guard.bicep` already expose region (`location`, `sqlLocation`, `zoneRedundant`), recorded-check reference (`regionCheckReference`, `quotaCheckReference`), and service quota parameters (`sqlTier`, `sqlVCores`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas`, `modelDeployments`/`chatModel*`, `iotHub*`, `monthlyBudget = 300`), alongside 29 `guard.bicep` controls and 17 dated read-only Azure capability/quota receipts (`R1`-`R17`) in `infra/README.md`. Five concrete gaps currently allow assumptions, placeholders, implicit defaults, or stale documentation to slip past review:

1. **Unbounded quota parameters and weak Bicep recorded-check/region guards (`infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`)**: `sqlVCores` (`main.bicep`) / `maxVCores` (`modules/sql.bicep`) and `monthlyBudget` (`main.bicep`) lack numeric `@minValue`/`@maxValue` constraints, and `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, and `deploymentLocationsMustBeSelected` rely solely on `!empty(...)`, allowing whitespace-only strings, placeholder/assumption words (`placeholder`, `todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `n/a`, `na`, `skip`, `example.invalid`), bare 36-character `8-4-4-4-12` subscription/tenant UUIDs, and malformed/assumed `sqlLocation` inputs to pass ARM/Bicep template validation.
2. **Implicit quota omissions across `dev`, `test`, and `pilot` `.bicepparam` sets (`infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam`)**: While all three files already declare `apiMinReplicas = 0`, `dev` and `test` omit explicit `sqlVCores`, `sqlAutoPauseDelayMinutes`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` lines, and `pilot` omits explicit `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` lines (while `test_bicep_policy.py` forbids `"chat"` in `main.bicepparam`/`main.pilot.example.bicepparam` and `test_sql_tier.py` forbids `"AutoPause"` in `main.pilot.example.bicepparam`).
3. **CLI preflight check-reference and region validation gaps (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`)**: `pipeline.py` checks `OVERRIDES` only for empty or uppercase `"PLACEHOLDER"` (missing word-bounded assumption markers, embedded subscription/tenant UUIDs, `location == "uksouth"`, and lowercase assumption slugs on `sqlLocation` such as `"placeholder"` or `"assumed"`), and `deploy.py` performs no check-reference or region-slug validation on `--parameter` overrides.
4. **Missing `docs/architecture/` specification and stale SKU/model rows in `infra/README.md`**: `docs/architecture/` lacks a canonical specification of the `dev`/`test`/`pilot` parameter sets, region/quota parameter bounds, fail-closed recorded-check guards, and `R1`-`R17` check ledger; meanwhile `infra/README.md` (`## Environments`) erroneously states that `pilot` shares `GP_S_Gen5` serverless SQL (contradicting `sqlTier = 'provisioned'` -> `GP_Gen5` in `main.pilot.example.bicepparam`) and lists `gpt-4.1-mini`/`gpt-4.1` capacity `30` as the live template default instead of `gpt-4.1-nano` (`2025-04-14`, `GlobalStandard`, capacity `1`), without explicitly distinguishing historical `2026-10-18` `612cbed7` `R4`/`R8`/`R9` receipts from current unverified `GP_Gen5` and `gpt-4.1-nano` SKUs.
5. **Dedicated deterministic test suite (`infra/tests/test_environment_quota_parameters.py`)**: Needed as a standalone, stdlib-only test module (avoiding cross-worktree conflicts with `test_monitoring_alerts.py`) to verify compiled Bicep parameter bounds, explicit `dev`/`test`/`pilot` `.bicepparam` parity, fail-closed Bicep + CLI check-reference/region rejection (including word-boundary non-collision on valid anchors like `spending`/`jtbd` and negative template mutations), and machine-checked consistency between compiled Bicep contracts, `docs/architecture/environment-region-quota-strategy.md`, and `infra/README.md` (`R1`-`R17`).

### User Decisions and Requirements Highlights

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated `2026-11-15` artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `changes/2026-11-15/`, `reviews/logs/2026-11-15/`).
* Ensure region and quota choices across `dev`, `test`, and `pilot` are parameterized, guarded against assumptions, validated deterministically in `infra/tests/test_environment_quota_parameters.py` (new test file to avoid conflicts with `test_monitoring_alerts.py`), and documented in `docs/architecture/`.
* Run Focused validation (`python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, related `infra/tests`, `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict` on touched scripts) and commit locally with the Copilot trailer without pushing.

### What You May Not Know

* `infra/tests/test_bicep_policy.py` evaluates compiled ARM expressions from `main.bicep` using a restricted Python `scope` and a single lambda rewrite `(remaining, digit) => replace(remaining, digit, '')` (`C15`, `C16`). All new Bicep guard expressions in `main.bicep` are designed around that exact `reduce`/`split`/`trim`/`toLower` subset so `test_bicep_policy.py` passes with zero evaluator modifications.
* `infra/tests/test_governance.py` and `test_bicep_policy.py` require `main.bicepparam`, `main.test.bicepparam`, and `main.pilot.example.bicepparam` to remain non-deployable as committed (`regionCheckReference = '' // PLACEHOLDER`, `quotaCheckReference = '' // PLACEHOLDER`, and blank `location`/`sqlLocation` in `pilot`) (`C15`, `C17`).
* Live Azure capacity reservations, private pilot subscription binding, and named human sizing/cost sign-off remain external operational gates (`R5`, `R7`, `R11`, `R14`-`R17`); commit messages and documentation preserve strict repository honesty (`Refs #137`) rather than fabricating live Azure quota headroom.

### Unresolved Decisions or Blockers

* None blocking implementation. Live pilot subscription binding, fresh Azure SQL/Foundry/Container Apps/IoT quota headroom checks, availability-zone verification, and named human approval remain documented operational prerequisites before completing a private pilot `.bicepparam` copy (`Refs #137`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Execute the full RPI loop (`research`, `plan`, `implement`, `review`) in order for Issue `#137`, writing dated `2026-11-15` artifacts under `.copilot-tracking/` (caller prompt).
* Work in `/home/azureuser/source/ama-demo-wt/feat-137-env-quotas` on branch `feat/infra-137-env-quotas` based on `origin/feat/demo-164-chat-grounding-provenance-0900` (PR `#1641`) under the Focused validation tier (caller prompt).
* Target unticked acceptance criterion: `- [ ] Region and quota choices are parameters with recorded checks, not assumptions` (caller prompt, Issue `#137`).
* Inspect `infra/` Bicep parameter sets (`dev`, `test`, `pilot`), region/quota parameter definitions, and `infra/tests/`, and ensure region and quota choices are parameterized, validated by deterministic checks in new file `infra/tests/test_environment_quota_parameters.py` (avoiding conflicts with `test_monitoring_alerts.py`), and documented in `docs/architecture/` (caller prompt).
* Run `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` and `python3 -m ruff check infra && python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py` (plus targeted regression checks), and commit all changes and `.copilot-tracking/` artifacts locally with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (caller prompt, `.github/copilot-instructions.md`).

## Goals

* Ensure every region choice (`location`, `sqlLocation`, `zoneRedundant`, plus explicit regional boundaries on standalone templates) and every service quota/capacity/SKU choice (`sqlTier`, `sqlVCores`, `sqlAutoPauseDelayMinutes`, `apiMinReplicas`, `chatModelName`, `chatModelVersion`, `chatModelSku`, `chatModelCapacity`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubMonthlyCost`, `monthlyBudget`) has explicit compile-time bounds and explicit per-environment parameter declarations across `dev`, `test`, and `pilot`.
* Harden mechanical recorded-check and location guards in both Bicep (`infra/main.bicep`, `infra/modules/guard.bicep`) and Python CLI helpers (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`) so blank, whitespace, placeholder, assumption (`assumed`, `assumption`, `tbd`, `todo`, `unverified`, `pending`, `unknown`, `none`, `n/a`, `na`, `skip`, `example.invalid`), and subscription/tenant UUID strings fail closed before deployment.
* Document the canonical architecture-level environment, region/quota parameter, guard, and `R1`-`R17` recorded-check specification in `docs/architecture/environment-region-quota-strategy.md` (indexed in `docs/architecture/README.md`) and reconcile stale SKU/model rows in `infra/README.md`.
* Validate all parameter definitions, `.bicepparam` sets, fail-closed guards, negative template mutations, CLI helpers, and documentation/ledger parity deterministically in `infra/tests/test_environment_quota_parameters.py`.

## Scope and Non-Goals

### In Scope

* `infra/main.bicep`, `infra/modules/sql.bicep`, and `infra/modules/guard.bicep`: add `@minValue(1) @maxValue(80)` on `sqlVCores` (`infra/main.bicep`) and `maxVCores` (`infra/modules/sql.bicep`), and `@minValue(1)` on `monthlyBudget` (`300` default in `infra/main.bicep`); tighten `regionCheckMustBeRecorded`, `quotaCheckMustBeRecorded`, and `deploymentLocationsMustBeSelected` across the 29 existing `guard.bicep` parameters against whitespace, word-bounded assumption/skip tokens, `placeholder`/`example.invalid`/`n/a`/`00000000-0000-0000-0000-000000000000` substrings, bare 36-char `8-4-4-4-12` UUIDs, and malformed/assumed `sqlLocation` slugs using `test_bicep_policy.evaluate`-compatible expressions; update guard `@description` text while keeping `"Empty means"` intact.
* `infra/main.bicepparam`, `infra/main.test.bicepparam`, and `infra/main.pilot.example.bicepparam`: retain existing `apiMinReplicas = 0` in place without duplication; explicitly declare `sqlVCores`, `modelDeployments` (`[{ name: 'standard', model: 'gpt-4.1-nano', version: '2025-04-14', skuName: 'GlobalStandard', capacity: 1 }]`), `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` across all three environment parameter sets plus `sqlAutoPauseDelayMinutes = 60` in serverless `dev` and `test` only (keeping zero occurrences of `"chat"` in `main.bicepparam`/`main.pilot.example.bicepparam` per `test_bicep_policy.py:759-760`, zero occurrences of `"AutoPause"` in `main.pilot.example.bicepparam` per `test_sql_tier.py:48`, and keeping `PLACEHOLDER` check-reference and pilot location/sizing markers non-deployable).
* `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`: enforce fail-closed validation of `regionCheckReference`, `quotaCheckReference`, `location`, and `sqlLocation` overrides against whitespace, word-bounded assumption/skip tokens, `placeholder`/`example.invalid`/`n/a`, invalid region slugs (and `location == "uksouth"`), and bare or embedded UUIDs, iterating all `--parameter` pairs in `deploy.py` without reading `--parameters` from disk and never echoing raw rejected parameter values in exception messages.
* `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, and `infra/README.md`: author the canonical architecture document, index it in `docs/architecture/README.md`, cross-link from `infra/README.md`, and fix the stale `Service SKUs` (`GP_Gen5` for pilot `provisioned`) and `modelDeployments` (`gpt-4.1-nano` capacity `1`) rows in `infra/README.md` while explicitly preserving `2026-10-18` (`612cbed7`) `R1`-`R17` provenance and marking `GP_Gen5` and `gpt-4.1-nano` as `Unknown` pending fresh `R4`/`R8`/`R9` runs.
* `infra/tests/test_environment_quota_parameters.py`: create a deterministic, stdlib-only (no shebang, no `zava_forward` runtime dependency) offline unit, compiled-Bicep, negative-mutation, CLI-guard, and documentation/ledger parity test suite.

### Non-Goals

* Modifying any existing file in `infra/tests/` (including `infra/tests/test_monitoring_alerts.py` touched by parallel Issue `#146` work).
* Changing locked `containerapps.bicep` replica expressions (`maxReplicas: enablePublicSimulationLane ? 1 : 4` and `maxReplicas: 5`).
* Editing `.github/workflows/` or 30+ unrelated `infra/` files with pre-existing non-`--isolated` Ruff 0.17.3 default-rule notices.
* Executing live Azure cloud writes, fabricating live quota reservations, or pushing commits to `origin`.

## Functional Requirements

* FR-1: All quota-bearing and region parameters in `infra/main.bicep` and `infra/modules/sql.bicep` must enforce explicit type/domain/range constraints (`@allowed`, `@minValue`, `@maxValue`, `@minLength`), including `@minValue(1) @maxValue(80)` on `sqlVCores` (`infra/main.bicep`) and `maxVCores` (`infra/modules/sql.bicep`) and `@minValue(1)` on `monthlyBudget` (`300` default in `infra/main.bicep`), while preserving `"Empty means"` in `infra/main.bicep` and across all 29 `infra/modules/guard.bicep` parameters and forwarding cleanly to `sql`, `foundry`, `iothub`, `containerapps`, and `monitoring` modules.
  * Observable acceptance criteria: `az bicep build` and `az bicep lint` succeed with zero warnings across `infra/main.bicep` and `infra/modules/*.bicep`, and compiled ARM JSON reflects exact bounds and forwarding expressions.
* FR-2: `infra/main.bicepparam` (`dev`), `infra/main.test.bicepparam` (`test`), and `infra/main.pilot.example.bicepparam` (`pilot`) must explicitly declare every environment-varying and quota-bearing parameter (`location`, `sqlLocation`, `zoneRedundant`, `sqlTier`, `sqlVCores`, single in-place `apiMinReplicas = 0`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, `monthlyBudget`, `regionCheckReference`, `quotaCheckReference`, plus serverless-only `sqlAutoPauseDelayMinutes = 60` in `dev` and `test`), keeping zero `"chat"` occurrences in `main.bicepparam`/`main.pilot.example.bicepparam`, zero `"AutoPause"` occurrences in `main.pilot.example.bicepparam`, and keeping committed files non-deployable (`PLACEHOLDER` check references; blank `location`/`sqlLocation` and `PLACEHOLDER`-annotated sizing in `pilot`).
  * Observable acceptance criteria: `az bicep build-params` compiles all three `.bicepparam` files cleanly; `dev`/`test` fail exclusively `{"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded"}` and `pilot` fails exclusively `{"regionCheckMustBeRecorded", "quotaCheckMustBeRecorded", "deploymentLocationsMustBeSelected", "primaryLocationMustBeUKSouth"}`.
* FR-3: Both Bicep (`parameter-guard` in `infra/main.bicep`) and Python deployment helpers (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`) must reject blank, whitespace-only, substring (`placeholder`, `example.invalid`, `n/a`, `00000000-0000-0000-0000-000000000000`), and word-bounded assumption/skip (`todo`, `tbd`, `assumed`, `assumption`, `unverified`, `pending`, `unknown`, `none`, `na`, `skip`) values in `regionCheckReference`/`quotaCheckReference` without false positives on valid words such as `spending` or `jtbd`; Bicep must reject bare 36-char `8-4-4-4-12` UUIDs (and embedded all-zero GUIDs) while `pipeline.py` and `deploy.py` reject all bare and embedded UUIDs without echoing raw values in error messages; and all three layers must reject blank, whitespace, placeholder/assumption-word, or malformed `location` and `sqlLocation` values (enforcing `location == "uksouth"`, lowercase hyphenated slugs in Bicep compatible with `'offline-sql-region'`, and `^[a-z][a-z0-9]+$` in `pipeline.py`/`deploy.py`).
  * Observable acceptance criteria: Evaluating compiled `parameter-guard` expressions and invoking `pipeline.parameters()` / `deploy.main()` reject every invalid/assumed/UUID check reference and malformed/assumed location while accepting valid synthetic and dated document/record references (`synthetic-region-check`, `reviewed-region-record`, `infra/README.md#cost-proposal-not-a-quote-or-spending-approval`, `docs/reference/research/ux/resident-demo-redesign-2026-11-04.md#jobs-to-be-done-jtbd-analysis`).
* FR-4: `docs/architecture/environment-region-quota-strategy.md` (indexed in `docs/architecture/README.md`) and `infra/README.md` must document the exact compiled `dev`/`test`/`pilot` parameter matrix, standalone regional template boundaries (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep` `swedencentral`), mechanical fail-closed guards (`29` `guard.bicep` controls), `R1`-`R17` recorded check ledger (preserving `2026-10-18` `612cbed7` historical provenance and marking current `GP_Gen5` and `gpt-4.1-nano` defaults as `Unknown` pending fresh `R4`/`R8`/`R9` queries), and deterministic verification rules without drift or new `.copilot-tracking/` links in production docs.
  * Observable acceptance criteria: Automated parity assertions in `infra/tests/test_environment_quota_parameters.py` verify that documented parameter defaults (`monthlyBudget = 300`, `apiMinReplicas = 0`, etc.), `.bicepparam` values, SQL SKUs (`GP_S_Gen5` vs `GP_Gen5`), model deployment defaults (`gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1`), locked `infra/README.md` governance phrases, and all 17 `R1`-`R17` check rows match compiled Bicep templates.

## Non-Functional Requirements

* NFR-1: Zero regression across untouched `infra/tests` suites and cross-worktree isolation.
  * Objective threshold or evaluation condition: `test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, `test_pipeline.py`, `test_container_hosting_completeness.py`, and `test_iothub_module.py` pass with `0` edits to existing test files.
  * Operating condition or verification approach: Run standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` under system `python3`, and run full `REQUIRE_AZ_BICEP=1` `infra/tests` discovery in a workspace-external/cleaned-up Python environment with editable `src/*` (`core`, `agents`, `api`, `orchestrator`, `importer`) installed per `src-ci.yml`.
  * Observable acceptance criteria: `0` failures and `0` errors across `test_environment_quota_parameters.py` and all existing `infra/tests` suites.
* NFR-2: Static analysis, formatting, privacy-safe errors, and Markdown hygiene on all touched files.
  * Objective threshold or evaluation condition: `infra/tests/test_environment_quota_parameters.py` has `0` diagnostics under both bare `python3 -m ruff check` and hosted CI `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`; `infra/scripts/pipeline.py` and `infra/scripts/deploy.py` have `0` diagnostics under hosted CI `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `0` new bare-ruff diagnostics on modified lines; all three touched Python files pass explicit `ruff format --isolated --line-length 100 --check` and `mypy --strict`; CLI error messages never echo raw rejected parameter values; and new/edited Markdown adheres strictly to repository Markdown rules.
  * Operating condition or verification approach: Run `ruff check --isolated`, bare `ruff check`, unchained `ruff format --isolated --line-length 100 --check`, `mypy --strict`, `az bicep lint`, and `git diff --check`.
  * Observable acceptance criteria: All isolated lint, format, type, Bicep lint, and Markdown checks exit `0`; pre-existing non-`--isolated` Ruff 0.17.3 notices (`EXE001`, `SIM102`, `SIM117`, `FURB167`) on untouched `infra/` lines remain untouched and transparently documented.

## Acceptance Criteria

* AC-1: `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, and `infra/main.pilot.example.bicepparam` compile and lint cleanly with `az bicep`, explicitly parameterizing all region and quota choices with compile-time bounds and fail-closed recorded-check guards while preserving all `test_bicep_policy.py` and `test_sql_tier.py` invariants.
* AC-2: `parameter-guard`, `infra/scripts/pipeline.py`, and `infra/scripts/deploy.py` deterministically reject blank, whitespace, placeholder, word-bounded assumption/skip tokens, and UUIDs (bare `8-4-4-4-12` UUIDs + all-zero GUIDs in Bicep; all bare and embedded UUIDs in Python without echoing raw values) in `regionCheckReference` / `quotaCheckReference` without false positives on words like `spending` or `jtbd`, and reject blank, whitespace, placeholder/assumption-word, or invalid-slug `location` / `sqlLocation` inputs.
* AC-3: `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, and `infra/README.md` accurately document the `dev`/`test`/`pilot` parameter sets, region/quota parameter contracts, standalone regional template boundaries, 29 mechanical guards, `R1`-`R17` recorded check ledger (preserving `2026-10-18` `612cbed7` provenance and marking `GP_Gen5` and `gpt-4.1-nano` as `Unknown`), and live-pilot governance boundaries with zero drift against compiled templates.
* AC-4: `infra/tests/test_environment_quota_parameters.py` passes standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, full `infra/tests` discovery passes with editable `src/*` installed, and explicit `ruff check --isolated`, `ruff format --isolated --line-length 100 --check`, and `mypy --strict` all pass.
* AC-5: All repository changes and dated `2026-11-15` `.copilot-tracking/` artifacts are committed locally on `feat/infra-137-env-quotas` with repository-local privacy-safe GitHub noreply email, `Refs #137`, no leaked identifiers, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing.

## Test Ownership and Validation Lock

* Canonical targets created or modified:
  * `infra/main.bicep`
  * `infra/modules/sql.bicep`
  * `infra/modules/guard.bicep`
  * `infra/main.bicepparam`
  * `infra/main.test.bicepparam`
  * `infra/main.pilot.example.bicepparam`
  * `infra/scripts/pipeline.py`
  * `infra/scripts/deploy.py`
  * `docs/architecture/environment-region-quota-strategy.md` (new)
  * `docs/architecture/README.md`
  * `infra/README.md`
  * `infra/tests/test_environment_quota_parameters.py` (new)
* Generated targets: `none` (`az bicep build` and `az bicep build-params` run into stdout/memory during tests).
* Test ownership, removals, and additions bound:
  * Exact test removals: `none` (`0` existing tests removed or weakened; existing test files left untouched to prevent cross-branch merge conflicts).
  * Maximum new test methods added: `<= 14` focused, high-signal test methods in `infra/tests/test_environment_quota_parameters.py`.
  * Semantic vs regression coverage:
    * Semantic tests in `infra/tests/test_environment_quota_parameters.py` cover: (1) compiled region and quota parameter inventory, bounds (`sqlVCores` `1..80`, `monthlyBudget >= 1`, `apiMinReplicas` `0..4`, `chatModelCapacity >= 1`, `modelDeployments` `minLength 1`, `iotHubSku == ['B1']`, `iotHubUnits` `1..1`, `iotHubRetentionDays` `1..7`, `iotHubMonthlyCost` `1..700`), and child-module forwarding; (2) explicit region and quota parameter declarations and fail-closed non-deployable states across `main.bicepparam` (`dev`), `main.test.bicepparam` (`test`), and `main.pilot.example.bicepparam` (`pilot`); (3) standalone regional template boundaries (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`); (4) `parameter-guard` rejection of whitespace, placeholder, assumption, skip-word, and 36-char UUID strings on `regionCheckReference`/`quotaCheckReference` and invalid `location`/`sqlLocation`; (5) negative ARM template mutation tests verifying guard tamper detection; (6) `pipeline.py` and `deploy.py` CLI rejection of assumed/placeholder/UUID check references and invalid region slugs; and (7) parity between compiled Bicep contracts, `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, and `infra/README.md` (`## Environments` + `R1`-`R17` check ledger).
    * Regression coverage runs `test_bicep_policy.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, `test_pipeline.py`, and `test_iothub_module.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                    |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md                                               |
| Phase details                    | .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md                                    |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md (`Complete`, `Revise` -> applied `PC-001`..`PC-006`) |
| Relevant research                | .copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md (`executed`, `Ready`)                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md is created by `rpi-implement`            |
| Planning execution and readiness | Complete; `Ready` for `rpi-implement`                                                                         |
| Continuation context             | Confirmed automatic RPI Agent session; continues automatically to `rpi-implement` and `rpi-review`            |

## Sources

* `.copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md`: `C1`-`C19` codebase findings, `W1`-`W2` GitHub Issue `#137` findings, and contrarian `test_bicep_policy` / `test_governance` checks.
* `.copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md`: Single-pass critique findings `PC-001` through `PC-006`, all applied directly below.
* `docs/adrs/0002-pilot-readiness-architecture.md`: Pilot region (`uksouth`) and `@jmservera` subscription owner decision delta and `2026-10-18`/`19` capability boundary (`Refs #137`).
* `infra/README.md`: `## Environments` comparison table and `R1`-`R17` dated read-only capability and quota ledger.
* `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/sql.bicep`, `infra/main*.bicepparam`, `infra/scripts/pipeline.py`, `infra/scripts/deploy.py`: Active IaC and CLI contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Bicep Region/Quota Bounds, Parameter Sets, and Recorded-Check Guards

* Intent: Enforce numeric bounds on quota/budget parameters, declare explicit quota parameters across `dev`, `test`, and `pilot` `.bicepparam` sets without violating locked `"chat"` / `"AutoPause"` / `apiMinReplicas` policy tests, and harden Bicep and CLI recorded-check and location guards against whitespace, placeholders, word-bounded assumptions, invalid slugs, and UUID leakage.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden Bicep quota bounds, `.bicepparam` quota declarations, and `parameter-guard` check-reference/location validation

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, AC-1, AC-2 (`C1`, `C2`, `C3`, `C7`, `C8`, `C9`, `C15`, `C16`, `C17`, `PC-001`, `PC-002`, `PC-003`, `PC-004`)
* Expected result: `sqlVCores` (`main.bicep`) and `maxVCores` (`modules/sql.bicep`) carry `@minValue(1) @maxValue(80)` and `monthlyBudget` (`300` default) carries `@minValue(1)`; `main.bicepparam`, `main.test.bicepparam`, and `main.pilot.example.bicepparam` retain single in-place `apiMinReplicas = 0` and explicitly declare `sqlVCores`, `modelDeployments`, `iotHubSku`, `iotHubUnits`, `iotHubRetentionDays`, `iotHubMonthlyCost`, and `monthlyBudget` (plus serverless-only `sqlAutoPauseDelayMinutes = 60` in `dev`/`test`), with zero `"chat"` in `dev`/`pilot` and zero `"AutoPause"` in `pilot`; `main.bicep` `parameter-guard` rejects blank, whitespace, placeholder, word-bounded assumption/skip, and bare `8-4-4-4-12` UUID check references plus malformed/assumed `sqlLocation` values using `test_bicep_policy.evaluate`-compatible ARM expressions.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce recorded-check and region-slug validation in `infra/scripts/pipeline.py` and `infra/scripts/deploy.py`

* Requirement and evidence: FR-3, NFR-1, NFR-2, AC-2, AC-5 (`C10`, `C11`, `C19`, `PC-003`, `PC-004`)
* Expected result: Both `pipeline.py` (`OVERRIDES` validation) and `deploy.py` (iterating every `--parameter NAME=VALUE` pair without reading `--parameters` from disk) reject empty/whitespace strings, word-bounded assumption/skip tokens, `placeholder`/`example.invalid`/`n/a`, and bare or embedded UUIDs in `regionCheckReference` / `quotaCheckReference`, plus non-slug or assumption-word values on `location` / `sqlLocation` and `location != "uksouth"`, never echoing raw rejected values in exception messages and passing `mypy --strict` and `ruff --isolated`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Architecture Documentation and Runbook Parity

* Intent: Document the canonical environment strategy, region and quota parameter contract, 29 mechanical guards, standalone regional template boundaries, and `R1`-`R17` recorded-check ledger in `docs/architecture/`, and eliminate stale SKU/model drift in `infra/README.md` while preserving `2026-10-18` `612cbed7` historical receipt provenance.
* Dependencies: P01-T01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Author `docs/architecture/environment-region-quota-strategy.md`, index in `docs/architecture/README.md`, and reconcile `infra/README.md`

* Requirement and evidence: FR-4, NFR-2, AC-3, AC-5 (`C12`, `C13`, `C14`, `W1`, `W2`, `PC-001`, `PC-002`, `PC-006`)
* Expected result: `docs/architecture/environment-region-quota-strategy.md` specifies the `dev`/`test`/`pilot` parameter matrix (`apiMinReplicas = 0`, `monthlyBudget = 300`, `modelDeployments` `gpt-4.1-nano` capacity `1`, pilot `GP_Gen5`), region/quota parameter bounds, standalone regional entry points (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), 29 fail-closed Bicep guards + CLI check-reference guards, `R1`-`R17` recorded-check ledger with `2026-10-18` `612cbed7` provenance and explicit `Unknown` classification for `GP_Gen5` and `gpt-4.1-nano`, and deterministic verification; `docs/architecture/README.md` links to it; `infra/README.md` fixes the stale `Service SKUs` and `modelDeployments` rows while preserving locked governance phrases and historical `612cbed7` SHA-256 attribution.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Deterministic Verification Suite, Focused Validation, and Local Commit

* Intent: Implement stdlib-only `infra/tests/test_environment_quota_parameters.py`, run Focused-tier standalone + full `infra/tests` (`src/*` editable venv), `az bicep`, `ruff`, and `mypy` checks, complete single-pass `rpi-review`, and commit locally without pushing.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `infra/tests/test_environment_quota_parameters.py` and run Focused validation (`unittest`, `az bicep`, `ruff`, `mypy`)

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, AC-4, AC-5 (`C15`, `C17`, `C19`, `PC-001`..`PC-006`)
* Expected result: `infra/tests/test_environment_quota_parameters.py` (`<= 14` test methods, no shebang, stdlib-only) passes standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`; full `REQUIRE_AZ_BICEP=1` `infra/tests` discovery passes in a cleaned-up editable `src/*` venv; `az bicep lint`, explicit `ruff check --isolated`, bare `ruff check` on `test_environment_quota_parameters.py` (plus inspection of `ruff check infra`), unchained `ruff format --isolated --line-length 100 --check`, and `mypy --strict` all pass cleanly.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md

## Dependencies

* Azure CLI with Bicep (`az bicep` `v0.48.1`): Verified available in environment for `az bicep build`, `az bicep build-params`, and `az bicep lint`.
* Python 3.12 toolchain (`unittest`, `ruff`, `mypy`, `PyYAML`): System `python3` runs standalone `infra/tests/test_environment_quota_parameters.py`, `ruff`, and `mypy`; full `infra/tests/` discovery (`test_bicep_policy.py` and `test_pipeline.py`) requires editable `pip install -e src/core -e src/agents -e src/api -e src/orchestrator -e src/importer` plus `PyYAML==6.0.3` and `src/api/requirements.txt` in a transient non-committed virtual environment removed before `git status` verification (`PC-005`).

## Critique Disposition

Single-pass critique `.copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md` completed with verdict `Revise` (`1` Critical, `4` High, `1` Medium, `0` Low; user response required: `no`). Every finding was applied directly in this final plan and matching phase details:

* `PC-001` (Critical, applied directly): Replaced `chatModel*` in `.bicepparam` files with explicit `modelDeployments = [{ name: 'standard', model: 'gpt-4.1-nano', version: '2025-04-14', skuName: 'GlobalStandard', capacity: 1 }]` plus `sqlVCores = 2`, `monthlyBudget = 300`, `iotHubSku = 'B1'`, `iotHubUnits = 1`, `iotHubRetentionDays = 1`, and `iotHubMonthlyCost = 60` across all three `.bicepparam` sets, declared `sqlAutoPauseDelayMinutes = 60` only in serverless `dev`/`test`, retained single in-place `apiMinReplicas = 0` without duplication, and preserved zero `"chat"` in `main.bicepparam`/`main.pilot.example.bicepparam` (`test_bicep_policy.py:759-760`) and zero `"AutoPause"` in `main.pilot.example.bicepparam` (`test_sql_tier.py:48`).
* `PC-002` (High, applied directly): Targeted `param maxVCores int = 2` in `infra/modules/sql.bicep:20` (preserving `maxVCores: sqlVCores` required by `test_sql_tier.py:37`), corrected `monthlyBudget` default to `300` and `guard.bicep` parameter count to `29` existing parameters, and locked preservation of `"Empty means"` in `infra/main.bicep` and `infra/modules/guard.bicep` (`test_bicep_policy.py:2391`).
* `PC-003` (High, applied directly): Replaced raw substring stripping with delimiter-tokenized word-array matching (`split` after replacing `-`, `_`, `/`, `#`, `.`, `:`, `,`, `;`, `(`, `)` with `' '`, using only `test_bicep_policy.evaluate`-supported `replace`/`split`/`contains`/`reduce` functions) plus `8-4-4-4-12` UUID hyphen-index checks in Bicep and word-bounded regexes in Python so valid anchors containing `spending` or `jtbd` pass, and clarified Bicep (bare 36-char UUID + embedded all-zero GUID) vs Python (all bare and embedded UUIDs) detection scope.
* `PC-004` (High, applied directly): Added lowercase-letter-started `[a-z0-9-]+` slug, non-empty hyphen-segment (`!contains(split(normalizedSqlLocation, '-'), '')`), non-UUID, and forbidden-assumption-word checks on `sqlLocation` in `main.bicep` (preserving `'offline-region'` and `'offline-sql-region'`); added `location == "uksouth"` and forbidden-assumption-word rejection on `location`/`sqlLocation` in `pipeline.py` and `deploy.py`; iterated all `args.parameter` items in `deploy.py` without reading `--parameters` from disk; and forbade echoing raw rejected parameter values in `PipelineError`/`DeploymentError` messages.
* `PC-005` (High, applied directly): Specified no-shebang, stdlib-only authoring for `infra/tests/test_environment_quota_parameters.py`, separated explicit `ruff check --isolated` and `ruff format --isolated --line-length 100 --check` executions from bare `python3 -m ruff check infra` inspection so `ruff format --check` is never short-circuited by pre-existing `EXE001`/`SIM102` notices on untouched lines, and added transient editable `src/*` venv setup/cleanup for full `infra/tests` regression discovery.
* `PC-006` (Medium, applied directly): Scoped `.copilot-tracking/` leak assertions to `docs/architecture/environment-region-quota-strategy.md`, the `## Environments` section of `infra/README.md`, and the new bullet in `docs/architecture/README.md`; preserved `2026-10-18` (`612cbed7`) SHA-256 provenance while explicitly classifying `GP_Gen5` and `gpt-4.1-nano` as `Unknown` pending fresh `R4`/`R8`/`R9` queries; and locked `infra/README.md` governance/hosting substrings checked by `test_governance.py` and `test_container_hosting_completeness.py`.

## Follow-Up Items

* Execute fresh read-only Azure SQL (`GP_Gen5`), Foundry/OpenAI (`gpt-4.1-nano`), Container Apps Consumption-core, IoT Hub, and availability-zone queries (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`) on the bound pilot subscription and record named human sizing/cost approval before completing a private pilot `.bicepparam` copy (`Refs #137`).
* Triage pre-existing non-`--isolated` Ruff `0.17.3` default-rule notices (`SIM117`, `FURB167`, `EXE001`, `SIM102`) across older untouched `infra/scripts/` and `infra/tests/` files in a dedicated repository-hygiene slice once parallel infrastructure branches merge.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md
* Ready phase or task: P01, P02, P03 (`Planning status: Ready`)
* Remaining provisional question or blocker: None

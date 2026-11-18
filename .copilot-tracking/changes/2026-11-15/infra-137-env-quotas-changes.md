<!-- markdownlint-disable-file -->
# RPI Changes: Environment Strategy, Region and Quota Parameterization, Recorded Checks, and Architecture Documentation (Issue #137)

## Metadata

* Task ID: issue-137
* Related plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Every phase and task (`P01`–`P03`) is implemented and verified under Focused validation (`unittest`, full `REQUIRE_AZ_BICEP=1` `infra/tests` `606` tests, `az bicep`, `ruff`, `mypy --strict`, and `git diff --check`).

## Execution Summary

Delivered full-plan implementation (`P01`, `P02`, `P03`) for Issue `#137` Criterion 4 (`Region and quota choices are parameters with recorded checks, not assumptions`):

* Bounded `sqlVCores` (`1..80`), `maxVCores` (`1..80`), and `monthlyBudget` (`>= 1`, default `300`), explicitly declared service quota parameters across `dev`, `test`, and `pilot` `.bicepparam` sets without violating locked `"chat"` / `"AutoPause"` / `apiMinReplicas` policy invariants, and hardened Bicep `parameter-guard` plus `pipeline.py` and `deploy.py` against blank, whitespace, placeholder, word-bounded assumption/skip, UUID, and malformed-location overrides without echoing raw rejected values.
* Authored canonical architecture specification `docs/architecture/environment-region-quota-strategy.md`, indexed it in `docs/architecture/README.md`, and reconciled `infra/README.md` (`## Environments`) while preserving `2026-10-18` `612cbed7` historical provenance and marking `GP_Gen5` and `gpt-4.1-nano` as `Unknown` pending fresh target-subscription checks.
* Added deterministic offline verification suite `infra/tests/test_environment_quota_parameters.py` (`8` test methods, stdlib-only, zero conflicts with `test_monitoring_alerts.py`) and verified both standalone execution and all `606` `infra/tests/` tests under `REQUIRE_AZ_BICEP=1`.

## Completed Work

### Bicep Region/Quota Bounds, Parameter Sets, and Recorded-Check Guards (`P01`, `P01-T01`, `P01-T02`)

* Added `@minValue(1)` on `monthlyBudget` (`300` default) and `@minValue(1) @maxValue(80)` on `sqlVCores` (`infra/main.bicep`) and `maxVCores` (`infra/modules/sql.bicep`).
* Declared explicit `sqlVCores = 2`, `modelDeployments` (`gpt-4.1-nano`, `2025-04-14`, `GlobalStandard`, capacity `1`), `iotHubSku = 'B1'`, `iotHubUnits = 1`, `iotHubRetentionDays = 1`, `iotHubMonthlyCost = 60`, and `monthlyBudget = 300` across `infra/main.bicepparam`, `infra/main.test.bicepparam`, and `infra/main.pilot.example.bicepparam`, plus serverless-only `sqlAutoPauseDelayMinutes = 60` in `dev` and `test`, while preserving single `apiMinReplicas = 0`, zero `"chat"` in `dev`/`pilot`, and zero `"AutoPause"` in `pilot`.
* Hardened `parameter-guard` (`regionCheckRecorded`, `quotaCheckRecorded`, `sqlLocationSelected` in `infra/main.bicep` and `@description` docs in `infra/modules/guard.bicep`) and Python CLI preflight validation (`infra/scripts/pipeline.py`, `infra/scripts/deploy.py`) to reject empty, whitespace, placeholder, word-bounded assumption/skip, UUID, and malformed-location values without echoing raw rejected values.

### Architecture Documentation and Runbook Parity (`P02`, `P02-T01`)

* Authored `docs/architecture/environment-region-quota-strategy.md` and indexed it in `docs/architecture/README.md`.
* Reconciled `infra/README.md` (`## Environments`) to reflect `pilot` `GP_Gen5` provisioned SQL, `gpt-4.1-nano` capacity `1` `modelDeployments`, hardened mechanical check-reference rules, and explicit `Unknown` classification for `GP_Gen5` and `gpt-4.1-nano` relative to historical `2026-10-18` (`612cbed7`) `R4`/`R8`/`R9` receipts.

### Deterministic Verification Suite and Focused Validation (`P03`, `P03-T01`)

* Created `infra/tests/test_environment_quota_parameters.py` (`8` focused test methods, stdlib-only, no shebang) covering compiled Bicep bounds and forwarding, standalone regional template boundaries (`iot-hub-live.bicep`, `resident-demo.bicep`, `resident-assistant.bicep`), `dev`/`test`/`pilot` `.bicepparam` parity and fail-closed sets, Bicep + CLI check-reference/region rejection (including positive `spending`/`jtbd` anchors and value redaction), negative ARM template mutations, and documentation/`R1`-`R17` parity.
* Verified standalone `unittest`, full `REQUIRE_AZ_BICEP=1` `infra/tests` discovery (`606` tests in cleaned-up external venv), `az bicep lint`/`build`/`build-params`, `ruff`, `mypy --strict`, and `git diff --check`.

## Implementation-Time Plan and Detail Updates

* Local judgment (applied in `docs/architecture/environment-region-quota-strategy.md` and `infra/tests/test_environment_quota_parameters.py`): Verified exact downstream parameter targets in `infra/main.bicep` (`monthlyBudget` feeds top-level `Microsoft.Consumption/budgets` resource `budget` and `modules/resourceAlerts.bicep`; `iotHubMonthlyCost` feeds `modules/iothub.bicep` `monthlyCostEstimate`; `sqlTier` feeds `modules/sql.bicep` `sqlTier`) and reflected those exact compiled names in the architecture parameter table and test assertions.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` | Standalone new test suite (`8` tests) | Passed | `Ran 8 tests in 84.810s - OK` (exit `0`) |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` | Full `infra/tests` discovery (`test_bicep_policy.py`, `test_pipeline.py`, `test_governance.py`, `test_sql_tier.py`, `test_deploy.py`, `test_monitoring_alerts.py`, `test_environment_quota_parameters.py`, etc.) in cleaned-up external venv | Passed | `Ran 606 tests in 340.694s - OK (skipped=4)` (exit `0`; external venv removed) |
| `az bicep lint` & `az bicep build` & `az bicep build-params` | All `infra/*.bicep`, `infra/modules/*.bicep`, and `infra/*.bicepparam` | Passed | `All Bicep lint/build/build-params passed!` (`0` errors, `0` lint warnings) |
| `python3 -m ruff check infra/tests/test_environment_quota_parameters.py` | Bare Ruff `0.17.3` default rules on new test file | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` | Hosted CI Ruff lint rules on all touched Python files | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` | Explicit unchained Ruff format check (`--line-length 100`) | Passed | `3 files already formatted` (exit `0`) |
| `python3 -m ruff check infra` | Non-isolated whole-directory Ruff inspection | Inspected | Exits `1` on `112` pre-existing diagnostics in untouched older `infra/` files (`EXE001`/`SIM102`/`SIM117`/`FURB167`); `0` diagnostics in `test_environment_quota_parameters.py` and `0` new diagnostics on modified lines of `deploy.py`/`pipeline.py` |
| `python3 -m mypy --strict infra/scripts/pipeline.py infra/scripts/deploy.py infra/tests/test_environment_quota_parameters.py` | Strict static type checking on touched Python files | Passed | `Success: no issues found in 3 source files` (exit `0`) |
| Markdown link, frontmatter, style, and `git --no-pager diff --check` | `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, `infra/README.md`, and workspace diff | Passed | `0` broken links, `0` whitespace/conflict errors, strict Markdown rules satisfied |
| Hosted GitHub Actions CI | Branch not pushed (`Do NOT push` instruction) | Skipped | Explicit caller instruction forbids `git push`; local Focused validation (`infra/tests` + `az bicep` + `ruff` + `mypy`) executed directly |

## Pre-Review Reconciliation

* Plan markers and phase details: Synchronized (`[x] P01`, `[x] P01-T01`, `[x] P01-T02`, `[x] P02`, `[x] P02-T01`, `[x] P03`, `[x] P03-T01`; all three phases `Complete` in phase details)
* Completed-work evidence and handoff prose: Synchronized with actual workspace files and diffs
* Validation, blockers, remaining work, and follow-up items: Synchronized (`0` blockers, `0` remaining active-plan items)
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md, `## Follow-Up Items`
* Execute fresh read-only Azure SQL (`GP_Gen5`), Foundry/OpenAI (`gpt-4.1-nano`), Container Apps Consumption-core, IoT Hub, and availability-zone queries (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`) on the bound pilot subscription and record named human sizing/cost approval before completing a private pilot `.bicepparam` copy (`Refs #137`).
* Triage pre-existing non-`--isolated` Ruff `0.17.3` default-rule notices (`SIM117`, `FURB167`, `EXE001`, `SIM102`) across older untouched `infra/scripts/` and `infra/tests/` files in a dedicated repository-hygiene slice once parallel infrastructure branches merge.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier passed (`8` standalone tests, `606` full `REQUIRE_AZ_BICEP=1` `infra/tests` tests, `az bicep lint/build/build-params`, `ruff`, `mypy --strict`, `git diff --check`)
* Blockers: none
* Current plan and detail updates: Local judgment aligning downstream resource target descriptions (`budget` + `resourceAlerts.bicep`, `iothub.bicep` `monthlyCostEstimate`, `sql.bicep` `sqlTier`)
* Planning and critique state: Ready (`PC-001`..`PC-006` applied and verified)
* Follow-up items: Live pilot subscription capability/quota checks (`Refs #137`); pre-existing untouched `infra/` non-isolated Ruff hygiene
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`confirmed automatic RPI Agent`)

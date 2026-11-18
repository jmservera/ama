<!-- markdownlint-disable-file -->
# RPI Changes: Resolve Routed Review Findings RV-001, RV-002, and RV-003 for Issue #137

## Metadata

* Task ID: issue-137-rv-fixes
* Related plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: none
* Status basis: Completed `P01-T01` and `P01-T02` resolving `RV-001`, `RV-002`, and `RV-003` and passed Focused validation (`unittest` `8/8`, full `REQUIRE_AZ_BICEP=1` `infra/tests` `606` tests, `az bicep`, `ruff`, `mypy --strict`, and `git diff --check`).

## Execution Summary

Resolved all three routed parent review defects (`RV-001`, `RV-002`, `RV-003`) while keeping `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` immutable:

* Replaced Python `\b` word boundaries in `FORBIDDEN_CHECK_PATTERN` and `EMBEDDED_UUID_PATTERN` in `infra/scripts/deploy.py` and `infra/scripts/pipeline.py` with explicit ASCII non-alphanumeric (`(?<![a-z0-9])...(?![a-z0-9])`) and non-hex (`(?<![0-9a-f])...(?![0-9a-f])`) lookarounds so underscore-delimited assumption tokens and underscore/alphanumeric-embedded UUIDs fail closed without rejecting `spending_*`, `jtbd_*`, or 40/64-char hex digests.
* Added `@minValue(-1)` on `sqlAutoPauseDelayMinutes` in `infra/main.bicep` and reconciled `docs/architecture/environment-region-quota-strategy.md` (`modules/operationalMonitoring.bicep`, `main.bicep` definition scope and `modelDeployments` wiring for `chatModel*` without `enableDemoChat`, explicit `modules/*.bicep` prefixes in the `zoneRedundant` bullet, and lookaround regex documentation).
* Hardened all 8 test methods in `infra/tests/test_environment_quota_parameters.py` (`0` additions, `0` removals) to test all five `AC-1` negative vectors, both `AC-1` positive vectors + 40-char commit SHA, non-hyphenated and hyphenated CLI redaction probes across all four keys, `sqlAutoPauseDelayMinutes`/`chatModel*` bounds + negative bound-removal mutation, `operational-monitoring` `monthlyBudget` forwarding, disk existence of every backticked `.bicep` path in `ARCH_DOC`, and catalog-row-scoped compiled-default parity.

## Completed Work

### CLI Regex Lookarounds, `sqlAutoPauseDelayMinutes` Bound, and Architecture Catalog Alignment (`P01`, `P01-T01`)

* Updated `FORBIDDEN_CHECK_PATTERN` and `EMBEDDED_UUID_PATTERN` in `infra/scripts/deploy.py` and `infra/scripts/pipeline.py`.
* Added `@minValue(-1)` above `param sqlAutoPauseDelayMinutes int = 60` in `infra/main.bicep`.
* Updated `docs/architecture/environment-region-quota-strategy.md` to cite `modules/operationalMonitoring.bicep`, `main.bicep`-only `chatModel*` feeding default `modelDeployments`, explicit `modules/{storage,registry,sql,containerapps}.bicep` paths, and the ASCII non-alphanumeric / non-hex lookarounds.

### Regression Suite Hardening and Focused Validation (`P01`, `P01-T02`)

* Updated `infra/tests/test_environment_quota_parameters.py` within its existing `8` test methods (`0` additions, `0` removals) to enforce all `RV-001`..`RV-003` and `PC-001`..`PC-002` invariants.
* Verified standalone `unittest`, full `REQUIRE_AZ_BICEP=1` `infra/tests` (`606` tests in cleaned-up external venv), `az bicep lint`/`build`/`build-params`, bare + `--isolated` `ruff check`, `ruff format --check`, `mypy --strict`, and `git diff --check`.

## Implementation-Time Plan and Detail Updates

* Local judgment (applied in `docs/architecture/environment-region-quota-strategy.md`): The new Bicep path-existence check in `P01-T02` detected four bare module filenames (`storage.bicep`, `registry.bicep`, `sql.bicep`, `containerapps.bicep`) in the `zoneRedundant` bullet of `docs/architecture/environment-region-quota-strategy.md`; normalized them to `modules/storage.bicep`, `modules/registry.bicep`, `modules/sql.bicep`, and `modules/containerapps.bicep` so every backticked `.bicep` reference resolves unambiguously on disk.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` | Standalone regression suite (`8` tests) | Passed | `Ran 8 tests in 34.052s - OK` (exit `0`) |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` | Full `infra/tests` discovery in cleaned-up external venv | Passed | `Ran 606 tests in 270.186s - OK (skipped=4)` (exit `0`; external venv removed) |
| `az bicep lint` & `az bicep build` & `az bicep build-params` | All `infra/*.bicep`, `infra/modules/*.bicep`, and `infra/*.bicepparam` | Passed | `All Bicep + git diff --check OK` (`0` errors, `0` lint warnings) |
| `python3 -m ruff check infra/tests/test_environment_quota_parameters.py` | Bare Ruff `0.17.3` default rules on new test file | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` | Hosted CI Ruff lint rules on touched Python files | Passed | `All checks passed!` (exit `0`) |
| `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_environment_quota_parameters.py infra/scripts/deploy.py infra/scripts/pipeline.py` | Unchained Ruff format check (`--line-length 100`) | Passed | `3 files already formatted` (exit `0`) |
| `python3 -m ruff check infra` | Whole-directory Ruff baseline check | Inspected | Unchanged `112` pre-existing diagnostics in untouched older `infra/` files; `0` diagnostics in `test_environment_quota_parameters.py` and `0` new diagnostics in `deploy.py`/`pipeline.py` |
| `python3 -m mypy --strict infra/scripts/pipeline.py infra/scripts/deploy.py infra/tests/test_environment_quota_parameters.py` | Strict static type checking | Passed | `Success: no issues found in 3 source files` (exit `0`) |

## Blockers and Open Decisions

* None.

## Remaining Work and Handoff

* None in `Implement`. Ready for single-pass `Review` (`rpi-review`) of child task `issue-137-rv-fixes`.

## Follow-Up Work

* Execute fresh read-only Azure SQL (`GP_Gen5`), Foundry/OpenAI (`gpt-4.1-nano`), Container Apps, IoT Hub, and availability-zone queries (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`) on the bound pilot subscription and record human sign-off before completing a private pilot `.bicepparam` copy (`Refs #137`).
* Triage pre-existing non-`--isolated` Ruff `0.17.3` notices (`EXE001`, `SIM102`, `SIM117`, `FURB167`) across older untouched `infra/` files in a standalone hygiene PR after stacked branches merge.

<!-- markdownlint-disable-file -->
# Review: Environment Strategy, Region and Quota Parameterization, Recorded Checks, and Architecture Documentation (Issue #137)

## Scope and Evidence

* Task ID: issue-137
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Requirements `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, acceptance criteria `AC-1`..`AC-5`, single-pass plan critique `PC-001`..`PC-006`, Bicep/CLI region and quota bounds and recorded-check guards, `docs/architecture/environment-region-quota-strategy.md` and `infra/README.md` parity, `infra/tests/test_environment_quota_parameters.py`, Focused validation evidence, and non-blocking `## Follow-Up Items`
* Plan: .copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md, workspace git diff, standalone and full `infra/tests` (`REQUIRE_AZ_BICEP=1`, `606` tests) execution, `az bicep`, `ruff`, and `mypy --strict`

## Opening Review State

* Interpreted review goal: Verify that completed implementation (`P01`–`P03`) satisfies Issue `#137` Criterion 4 (`Region and quota choices are parameters with recorded checks, not assumptions`), resolves every single-pass critique disposition (`PC-001`–`PC-006`), preserves repository policy invariants and historical `2026-10-18` `612cbed7` receipt provenance, and passes Focused validation without material defects or unrouted gaps.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, finalized plan, phase details, plan critique, completed changes record, and workspace source/test/doc artifacts are present and synchronized.
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, `PC-001`..`PC-006`, and Focused validation expectations in `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md`.
* First comparison boundary: Reconcile `P01`, `P02`, and `P03` markers, implementation-time local judgments, and critique dispositions against the actual Git diff and validation outputs before grading findings.
* Active read-only boundaries: Review creates and updates only `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` (plus parent RPI session state transitions); no source, plan, detail, critique, research, or changes-record files may be mutated in this phase.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary review on `2026-11-15` across `.copilot-tracking/plans/2026-11-15/infra-137-env-quotas-plan.md`, `.copilot-tracking/details/2026-11-15/infra-137-env-quotas-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md`, `.copilot-tracking/research/2026-11-15/infra-137-env-quotas-research.md`, workspace diff (`10` modified files + `2` added files), Focused validation evidence, and an independent read-only `code-review` diff audit.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01`, `P01-T01`, `P01-T02` | Bicep Region/Quota Bounds, Parameter Sets, and Recorded-Check Guards | Partial | Bicep bounds (`sqlVCores`, `maxVCores`, `monthlyBudget`), `.bicepparam` quota sets, and Bicep `parameter-guard` word/UUID checks are implemented, but Python CLI regexes in `pipeline.py`/`deploy.py` use `\b` which treats `_` as a word character (`RV-001`), and `main.bicep` `sqlAutoPauseDelayMinutes` omits `@minValue(-1)` (`RV-002`). |
| `P02`, `P02-T01` | Architecture Documentation and Runbook Parity | Partial | `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, and `infra/README.md` are authored and style-clean with zero `.copilot-tracking/` leaks, but `environment-region-quota-strategy.md` cites nonexistent `modules/resourceAlerts.bicep` instead of `modules/operationalMonitoring.bicep` and overstates module definitions for `chatModel*` (`RV-002`). |
| `P03`, `P03-T01` | Deterministic Verification Suite and Focused Validation | Partial | `infra/tests/test_environment_quota_parameters.py` passes standalone (`8` tests) and full `REQUIRE_AZ_BICEP=1` `infra/tests` (`606` tests), `az bicep`, `ruff`, and `mypy --strict`, but omits underscore-delimited assumption/UUID cases, per-branch raw-value redaction checks, `chatModel*`/`sqlAutoPauseDelayMinutes` bounds, and backticked module-path existence checks (`RV-003`). |
| `## Follow-Up Items` | Live pilot subscription capability/quota checks (`Refs #137`) and pre-existing untouched `infra/` non-isolated Ruff hygiene | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` scope and mirrored accurately in `.copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01-T01` | `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`, `infra/main.bicepparam`, `infra/main.test.bicepparam`, `infra/main.pilot.example.bicepparam` | Added `sqlVCores`/`maxVCores` (`1..80`) and `monthlyBudget` (`>= 1`) bounds, explicit quota declarations across `dev`/`test`/`pilot`, and `test_bicep_policy.evaluate`-compatible `regionCheckRecorded`, `quotaCheckRecorded`, and `sqlLocationSelected` variables | Compiled ARM templates and `.bicepparam` JSON verified | `az bicep lint`/`build`/`build-params` and `606` `infra/tests` passed | Reconciled with minor gap (`sqlAutoPauseDelayMinutes` top-level `@minValue(-1)` omitted in `main.bicep`, `RV-002`) |
| `P01-T02` | `infra/scripts/pipeline.py`, `infra/scripts/deploy.py` | Added CLI check-reference and region-slug preflight validation with value-redacted error messages | `validate_parameter_overrides` in `deploy.py` and `parameters()` checks in `pipeline.py` | `ruff`, `mypy --strict`, `test_deploy.py`, `test_pipeline.py` passed | Defect found (`\b` regex misses `_`-delimited assumption tokens and `_`/alphanumeric-adjacent embedded UUIDs, `RV-001`) |
| `P02-T01` | `docs/architecture/environment-region-quota-strategy.md`, `docs/architecture/README.md`, `infra/README.md` | Documented canonical `dev`/`test`/`pilot` parameter matrix, bounds, 29 guards, standalone regional templates, and `R1`-`R17` check ledger; fixed stale `infra/README.md` rows while preserving `2026-10-18` `612cbed7` attribution | Relative links, Markdown rules, and `R1`-`R17` rows verified | Markdown link/style script, `test_governance.py`, `test_container_hosting_completeness.py` passed | Defect found (`modules/resourceAlerts.bicep` typo for `modules/operationalMonitoring.bicep` and `chatModel*` module attribution, `RV-002`) |
| `P03-T01` | `infra/tests/test_environment_quota_parameters.py` | Created stdlib-only deterministic verification suite (`8` test methods, no shebang, zero conflicts with `test_monitoring_alerts.py`) | Standalone and full `infra/tests` runs recorded | `unittest` (`8/8` standalone, `606/606` full), `ruff`, `mypy --strict` passed | Defect found (missing `_`-delimiter, per-case redaction, `chatModel*`/`sqlAutoPauseDelayMinutes` bounds, and module-path parity assertions, `RV-003`) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P02-T01`, `P03-T01` (`docs/architecture/environment-region-quota-strategy.md`, `infra/tests/test_environment_quota_parameters.py`) | Local judgment updated downstream resource target notes when inspecting `infra/main.bicep` budget wiring, inadvertently writing `modules/resourceAlerts.bicep` instead of `modules/operationalMonitoring.bicep` | Direct inspection of `infra/main.bicep` during `P03-T01` (no user decision needed) | Recorded in `.copilot-tracking/changes/2026-11-15/infra-137-env-quotas-changes.md` under `## Implementation-Time Plan and Detail Updates` | Preserved `PC-001`..`PC-006`, but introduced `modules/resourceAlerts.bicep` naming error | Defect routed in `RV-002` and `RV-003` (`rpi-implement`) |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` through `PC-006` from `.copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-plan-critique.md` are all explicitly recorded in `## Critique Disposition` and substantively honored (zero `"chat"` in `dev`/`pilot`, zero `"AutoPause"` in `pilot`, `maxVCores` bounded in `modules/sql.bicep`, `spending`/`jtbd` accepted without false positives, `--isolated` Ruff + external venv `infra/tests` executed, `2026-10-18` `612cbed7` provenance preserved with `GP_Gen5` and `gpt-4.1-nano` marked `Unknown`), save for the Python `_` boundary edge case identified in `RV-001`.
* Material revisions: No architectural, scope, or user-decision divergence occurred during implementation.
* Dependent-work pause assessment: Phases executed in strict dependency order (`P01` -> `P02` -> `P03`) with no premature resumption.
* Justification assessment: Confirmed user intent and repository governance boundaries were preserved throughout.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Fresh read-only Azure SQL (`GP_Gen5`), Foundry/OpenAI (`gpt-4.1-nano`), Container Apps, IoT Hub, and availability-zone queries (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`) + named human pilot sizing/cost approval (`Refs #137`) | Requires live target-subscription access and human governance approval outside offline repository work | Subscription owner (`@jmservera`) / operator before private pilot `.bicepparam` completion | Open distinct operational follow-up (non-defect) |
| Triage pre-existing non-`--isolated` Ruff `0.17.3` default-rule notices (`EXE001`, `SIM102`, `SIM117`, `FURB167`) across older untouched `infra/` files | Unrelated pre-existing warnings across 30+ untouched files; touching them risks cross-worktree merge conflicts | Repository maintainer in a dedicated lint-hygiene PR after stacked branches merge | Open distinct maintenance follow-up (non-defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Python CLI check-reference regexes miss underscore-delimited assumption tokens and underscore/alphanumeric-adjacent embedded UUIDs

* Related scope: `P01-T02`
* Evidence: `infra/scripts/deploy.py` (`FORBIDDEN_CHECK_PATTERN`, `EMBEDDED_UUID_PATTERN`), `infra/scripts/pipeline.py` (`FORBIDDEN_CHECK_PATTERN`, `EMBEDDED_UUID_PATTERN`), and `docs/architecture/environment-region-quota-strategy.md` (`## Mechanical Fail-Closed Guards`)
* Impact: Because Python `re` treats `_` as a word character (`\w`), `\b` does not match adjacent to `_` (or alphanumeric prefixes/suffixes on a UUID). Values such as `assumed_uksouth_2026`, `todo_check`, `tbd_later`, and `sub_<uuid>_uksouth` bypass CLI preflight validation in both `deploy.py` and `pipeline.py`, and `sub_<uuid>_uksouth` also passes Bicep's 36-char bare-UUID check, violating `AC-2` ("all bare and embedded UUIDs in Python").
* Destination: `rpi-implement`
* Smallest useful next action: Replace `\b` with `(?<![a-z0-9])...(?![a-z0-9])` on `FORBIDDEN_CHECK_PATTERN` and `(?<![0-9a-f])...(?![0-9a-f])` on `EMBEDDED_UUID_PATTERN` in `infra/scripts/deploy.py` and `infra/scripts/pipeline.py`, and update the documented regex in `docs/architecture/environment-region-quota-strategy.md`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Architecture quota catalog cites nonexistent `modules/resourceAlerts.bicep`, misattributes `chatModel*` to `modules/foundry.bicep`, and `main.bicep` `sqlAutoPauseDelayMinutes` omits `@minValue(-1)`

* Related scope: `P01-T01`, `P02-T01`
* Evidence: `docs/architecture/environment-region-quota-strategy.md` (`## Quota, SKU, and Capacity Parameter Catalog`) and `infra/main.bicep` (`param sqlAutoPauseDelayMinutes int = 60`, `module operationalMonitoring 'modules/operationalMonitoring.bicep'`)
* Impact: `infra/modules/resourceAlerts.bicep` does not exist (`infra/main.bicep` forwards `monthlyBudget` to `modules/operationalMonitoring.bicep`); `chatModelName`, `chatModelVersion`, `chatModelSku`, and `chatModelCapacity` are defined only in `infra/main.bicep` (while `modules/foundry.bicep` takes `deployments`); and `sqlAutoPauseDelayMinutes` in `infra/main.bicep` lacks `@minValue(-1)` despite the architecture table claiming `@minValue(-1)` in both `main.bicep` and `modules/sql.bicep`.
* Destination: `rpi-implement`
* Smallest useful next action: Add `@minValue(-1)` to `sqlAutoPauseDelayMinutes` in `infra/main.bicep` and update the `sqlAutoPauseDelayMinutes`, `chatModel*`, and `monthlyBudget` rows in `docs/architecture/environment-region-quota-strategy.md` to cite `modules/operationalMonitoring.bicep` and `main.bicep` accurately.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: `test_environment_quota_parameters.py` omits underscore-delimited negative cases, per-branch CLI value-redaction checks, `chatModel*`/`sqlAutoPauseDelayMinutes` bounds, and backticked module-path parity checks

* Related scope: `P03-T01`
* Evidence: `infra/tests/test_environment_quota_parameters.py` (`_assert_contract`, `test_pipeline_parameters_enforce_recorded_checks_and_redact_values`, `test_deploy_cli_rejects_invalid_check_and_region_overrides_before_az`, `test_architecture_doc_and_infra_readme_match_compiled_templates_and_r1_r17`)
* Impact: Without underscore-delimited negative inputs, per-case raw-value redaction assertions across `location`/`sqlLocation`/`regionCheckReference`/`quotaCheckReference` (checking `SYNTHETIC_UUID` substring redaction as well as full override strings), `chatModelCapacity`/`chatModelSku`/`sqlAutoPauseDelayMinutes` bound checks, and verification that every `modules/*.bicep` path cited in `docs/architecture/environment-region-quota-strategy.md` exists on disk and matches compiled parameter defaults, regressions of `RV-001` and `RV-002` went undetected.
* Destination: `rpi-implement`
* Smallest useful next action: Extend the existing 8 test methods in `infra/tests/test_environment_quota_parameters.py` to cover underscore-delimited assumption/UUID inputs, per-case raw-value and `SYNTHETIC_UUID` redaction in both `pipeline.py` and `deploy.py`, `chatModelCapacity`/`chatModelSku`/`sqlAutoPauseDelayMinutes` bounds, `modules/*.bicep` file existence in `ARCH_DOC`, and compiled-default parity.

## Defects

* `RV-001` (`High`, destination `rpi-implement`): Underscore-adjacent boundary bypass in `FORBIDDEN_CHECK_PATTERN` and `EMBEDDED_UUID_PATTERN` (`infra/scripts/deploy.py`, `infra/scripts/pipeline.py`).
* `RV-002` (`Medium`, destination `rpi-implement`): Nonexistent `modules/resourceAlerts.bicep` reference and `chatModel*` module attribution in `docs/architecture/environment-region-quota-strategy.md`, plus missing `@minValue(-1)` on `sqlAutoPauseDelayMinutes` in `infra/main.bicep`.
* `RV-003` (`Medium`, destination `rpi-implement`): Missing underscore-delimiter, per-branch value-redaction, `chatModel*`/`sqlAutoPauseDelayMinutes` bound, and `modules/*.bicep` path/compiled-default parity assertions in `infra/tests/test_environment_quota_parameters.py`.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| `RV-001` | `rpi-implement` | Fix regex boundaries in `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, and `docs/architecture/environment-region-quota-strategy.md` | Bounded implementation defect within approved plan direction |
| `RV-002` | `rpi-implement` | Add `@minValue(-1)` on `sqlAutoPauseDelayMinutes` in `infra/main.bicep` and fix `operationalMonitoring.bicep` / `chatModel*` attribution in `docs/architecture/environment-region-quota-strategy.md` | Bounded template/documentation parity defect |
| `RV-003` | `rpi-implement` | Strengthen assertions in `infra/tests/test_environment_quota_parameters.py` to catch `RV-001` and `RV-002` | Bounded regression-test gap |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live target-subscription capability and quota verification (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`, including `GP_Gen5` and `gpt-4.1-nano`) and named human pilot sizing/cost approval (`Refs #137`).
* Standalone repository-wide lint hygiene pass for pre-existing non-`--isolated` Ruff `0.17.3` notices across untouched `infra/` files after stacked branches merge.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none inside completed `issue-137` loop (`RV-001`..`RV-003` routed to follow-up child implementation)

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q` | `infra/tests/test_environment_quota_parameters.py` (`8` tests) | Passed | `Ran 8 tests in 84.810s - OK` |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` | Full `infra/tests/` suite (`606` tests) in cleaned-up external venv | Passed | `Ran 606 tests in 340.694s - OK (skipped=4)` |
| `az bicep lint` / `build` / `build-params` | All `infra/*.bicep`, `infra/modules/*.bicep`, `infra/*.bicepparam` | Passed | `0` lint warnings, `0` build errors |
| `python3 -m ruff check infra/tests/test_environment_quota_parameters.py` | Bare Ruff `0.17.3` on new test module | Passed | `All checks passed!` |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 ...` | Touched Python files (`test_environment_quota_parameters.py`, `deploy.py`, `pipeline.py`) | Passed | `All checks passed!` |
| `python3 -m ruff format --isolated --line-length 100 --check ...` | Touched Python files | Passed | `3 files already formatted` |
| `python3 -m mypy --strict ...` | Touched Python files | Passed | `Success: no issues found in 3 source files` |
| Hosted GitHub Actions CI | Unpushed local branch (`feat/infra-137-env-quotas`) | Skipped | Caller explicitly forbade `git push` (`Do NOT push`) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned work (`P01`–`P03`) executed completely and passed Focused validation (`606` `infra/tests` tests, `az bicep`, `ruff`, `mypy --strict`), but independent exact-head diff review identified one High-severity regex boundary bypass on underscore-delimited assumption/UUID strings (`RV-001`) and two Medium-severity documentation/bound/assertion gaps (`RV-002`, `RV-003`) that are routed to `rpi-implement`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | `rpi-implement` | Resolve `RV-001`, `RV-002`, and `RV-003` in follow-up child task |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Target-subscription live `R4`/`R5`/`R7`/`R8`/`R9`/`R11`/`R14`-`R17` checks + human pilot sign-off (`Refs #137`); untouched `infra/` non-isolated Ruff hygiene |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused tier passed (`8` standalone tests, `606` full `REQUIRE_AZ_BICEP=1` `infra/tests`, `az bicep`, `ruff`, `mypy --strict`); hosted CI skipped per `Do NOT push` instruction
* Blockers: none


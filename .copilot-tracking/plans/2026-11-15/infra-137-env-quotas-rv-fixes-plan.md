<!-- markdownlint-disable-file -->
# RPI Plan: Resolve Routed Review Findings RV-001, RV-002, and RV-003 for Issue #137

## Task Metadata

* Task ID: issue-137-rv-fixes
* Task slug: infra-137-env-quotas-rv-fixes
* Parent task: issue-137 (`infra-137-env-quotas`)
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan-critique.md

## Executive Summary

This child plan resolves all three defects (`RV-001` High, `RV-002` Medium, `RV-003` Medium) routed to `rpi-implement` by the parent post-implementation review `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` while keeping the original parent review log immutable:

1. **Close underscore-adjacent CLI regex boundary bypass (`RV-001`)**: Replace `\b` in `FORBIDDEN_CHECK_PATTERN` and `EMBEDDED_UUID_PATTERN` in `infra/scripts/deploy.py` and `infra/scripts/pipeline.py` with explicit ASCII non-alphanumeric (`(?<![a-z0-9])...(?![a-z0-9])`) and non-hex (`(?<![0-9a-f])...(?![0-9a-f])`) lookarounds so underscore-delimited assumption tokens (`assumed_uksouth_2026`, `todo_check`, `tbd_later`) and underscore/alphanumeric-adjacent UUIDs (`sub_<uuid>_uksouth`) fail closed without false positives on `spending_review` or `jtbd_notes`.
2. **Align `sqlAutoPauseDelayMinutes` `@minValue(-1)` bound and architecture parameter catalog (`RV-002`)**: Add `@minValue(-1)` on `param sqlAutoPauseDelayMinutes int = 60` in `infra/main.bicep`, and update `docs/architecture/environment-region-quota-strategy.md` to reference `modules/operationalMonitoring.bicep` (replacing nonexistent `modules/resourceAlerts.bicep`), state that `chatModelName`/`chatModelVersion`/`chatModelSku`/`chatModelCapacity` are defined in `main.bicep` (feeding `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep`), and update the documented CLI UUID regex.
3. **Lock regression coverage in `infra/tests/test_environment_quota_parameters.py` (`RV-003`)**: Within the existing `8` test methods (`0` test-method additions/removals), add underscore-delimited assumption and embedded-UUID negative test cases, assert per-case raw override value and `SYNTHETIC_UUID` redaction across all `location`, `sqlLocation`, `regionCheckReference`, and `quotaCheckReference` CLI failures, assert `sqlAutoPauseDelayMinutes` (`minValue == -1`), `chatModelCapacity` (`minValue == 1`), and `chatModelSku` (`allowedValues`) bounds in `_assert_contract` (plus negative mutation), and verify every backticked `modules/*.bicep` path and compiled default in `docs/architecture/environment-region-quota-strategy.md`.

### User Decisions and Requirements Highlights

* Deliver and prove `- [ ] Region and quota choices are parameters with recorded checks, not assumptions` for Issue `#137` under the Focused validation tier, preserve original critique/review evidence under `.copilot-tracking/`, and commit locally with the Copilot trailer without pushing.

### What You May Not Know

* Parent review `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` remains untouched as historical RPI evidence (`Defects found`); this child RPI loop produces its own plan, critique, changes, and review artifacts under `.copilot-tracking/*/2026-11-15/infra-137-env-quotas-rv-fixes-*`.

### Unresolved Decisions or Blockers

* None.

## User Decisions and Requirements

* Resolve routed defects `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/infra-137-env-quotas-review.md` without modifying existing `infra/tests/test_monitoring_alerts.py` or rewriting parent review outcomes.
* Re-verify Focused validation (`python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, `REQUIRE_AZ_BICEP=1` `test_bicep_policy.py` + `test_pipeline.py` + `test_sql_tier.py` + `test_deploy.py` + `test_governance.py`, `az bicep lint/build`, `ruff`, and `mypy --strict`) and commit locally without pushing.

## Goals

* Eliminate underscore-delimited assumption-token and embedded-UUID bypasses in `deploy.py` and `pipeline.py` (`RV-001`).
* Align `infra/main.bicep` (`@minValue(-1)` on `sqlAutoPauseDelayMinutes`) and `docs/architecture/environment-region-quota-strategy.md` (`modules/operationalMonitoring.bicep`, `chatModel*` top-level scope, updated lookaround regex) with exact repository source (`RV-002`).
* Prove every fixed edge case and module-path/compiled-default parity check deterministically inside `infra/tests/test_environment_quota_parameters.py` (`RV-003`).

## Scope and Non-Goals

* In scope: `infra/scripts/deploy.py`, `infra/scripts/pipeline.py`, `infra/main.bicep`, `docs/architecture/environment-region-quota-strategy.md`, `infra/tests/test_environment_quota_parameters.py`, child `.copilot-tracking/*/2026-11-15/infra-137-env-quotas-rv-fixes-*` artifacts, and local git commit.
* Non-goals: Mutating parent `.copilot-tracking/*infra-137-env-quotas-*` review/plan artifacts, touching `infra/tests/test_monitoring_alerts.py`, or pushing to `origin`.

## Functional Requirements

* `FR-1` (`RV-001`): `FORBIDDEN_CHECK_PATTERN` in `deploy.py` and `pipeline.py` must reject case-insensitively `(?<![a-z0-9])(?:todo|tbd|assumed|assumption|unverified|pending|unknown|none|na|skip)(?![a-z0-9])|placeholder|example\.invalid|n/a`, and `EMBEDDED_UUID_PATTERN` must reject `(?<![0-9a-f])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![0-9a-f])`, while accepting underscore- and hyphen-delimited valid anchors containing `spending` and `jtbd` and 40/64-char hex commit/image digests.
* `FR-2` (`RV-002`): `infra/main.bicep` must annotate `sqlAutoPauseDelayMinutes` with `@minValue(-1)`, and `docs/architecture/environment-region-quota-strategy.md` must cite `modules/operationalMonitoring.bicep` (never `modules/resourceAlerts.bicep`), state `main.bicep` as the definition site of `chatModelName`/`chatModelVersion`/`chatModelSku`/`chatModelCapacity` (with `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep`), and document the non-hex lookaround UUID regex.
* `FR-3` (`RV-003`): `infra/tests/test_environment_quota_parameters.py` (keeping `8` test methods, `0` removals, `0` new test methods) must test underscore-delimited assumption and UUID inputs, assert per-case raw override value and `SYNTHETIC_UUID` redaction across all rejected CLI branches, assert `sqlAutoPauseDelayMinutes`, `chatModelCapacity`, and `chatModelSku` bounds (including negative bound-removal mutation), and verify all backticked `modules/*.bicep` paths and compiled parameter defaults in `docs/architecture/environment-region-quota-strategy.md`.

## Non-Functional Requirements

* `NFR-1`: Zero regressions across `test_bicep_policy.py`, `test_pipeline.py`, `test_deploy.py`, `test_sql_tier.py`, `test_governance.py`, `az bicep lint`, `ruff --isolated`, bare `ruff check infra/tests/test_environment_quota_parameters.py`, and `mypy --strict`.
* `NFR-2`: Preserve strict Markdown conventions (`*` lists, no H1 when `title` in frontmatter, no em dashes, no bolded-prefix list items, no `.copilot-tracking/` links in production docs/code).

## Acceptance Criteria

* `AC-1`: `deploy.py` and `pipeline.py` reject `assumed_uksouth_2026`, `todo_check`, `tbd_later`, `unverified_quota`, and `sub_<uuid>_uksouth` without echoing raw rejected override values or UUID substrings, while accepting `spending_review_2026` and `jtbd_notes_2026`.
* `AC-2`: `infra/main.bicep` compiles `sqlAutoPauseDelayMinutes` with `minValue == -1`, and every `modules/*.bicep` path cited in `docs/architecture/environment-region-quota-strategy.md` resolves to an existing file under `infra/` and matches compiled template defaults.
* `AC-3`: Standalone `python3 -m unittest infra/tests/test_environment_quota_parameters.py -q`, `REQUIRE_AZ_BICEP=1` policy/pipeline/SQL/deploy/governance suites, `az bicep lint`, `ruff`, and `mypy --strict` all exit `0`.

## Test Ownership and Validation Lock

* Canonical test owner: `infra/tests/test_environment_quota_parameters.py` (`8` existing methods updated in place; exact removals: `none`; maximum new test methods: `0`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fix RV-001..RV-003 Across CLI Scripts, Bicep, Architecture Doc, and Regression Suite

* Intent: Apply surgical fixes for `RV-001`, `RV-002`, and `RV-003` and re-run Focused validation.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update CLI regex lookarounds (`deploy.py`, `pipeline.py`), `sqlAutoPauseDelayMinutes` bound (`main.bicep`), and architecture catalog (`environment-region-quota-strategy.md`)

* Requirement and evidence: FR-1, FR-2, NFR-2, AC-1, AC-2 (`RV-001`, `RV-002`)
* Expected result: `deploy.py` and `pipeline.py` enforce `(?<![a-z0-9])...(?![a-z0-9])` and `(?<![0-9a-f])...(?![0-9a-f])`; `main.bicep` sets `@minValue(-1)` on `sqlAutoPauseDelayMinutes`; `docs/architecture/environment-region-quota-strategy.md` cites `modules/operationalMonitoring.bicep`, `main.bicep`-only `chatModel*`, and the lookaround UUID pattern.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden `infra/tests/test_environment_quota_parameters.py` assertions and run Focused validation

* Requirement and evidence: FR-3, NFR-1, AC-1, AC-2, AC-3 (`RV-003`)
* Expected result: All 8 test methods in `test_environment_quota_parameters.py` verify underscore-delimited negative cases, per-branch value/UUID redaction, `sqlAutoPauseDelayMinutes`/`chatModel*` bounds + mutation, `modules/*.bicep` file existence, and compiled-default doc parity, and Focused validation passes cleanly.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/infra-137-env-quotas-rv-fixes-phase-details.md

## Critique Disposition

Single-pass critique executed in `.copilot-tracking/reviews/plans/2026-11-15/infra-137-env-quotas-rv-fixes-plan-critique.md` (`Execution status: Complete`, `Verdict: Revise`, `User response required: no`). Both planner-owned findings were applied directly without re-running critique:

* `PC-001` (`Medium`, applied): Updated `P01-T02` to include non-hyphenated redaction probes (`location="ukwestleakedregion"`, `sqlLocation="placeholdersqlsecret"`), test all five `AC-1` rejected tokens (`assumed_uksouth_2026`, `todo_check`, `tbd_later`, `unverified_quota`, `sub_<uuid>_uksouth`) and both `AC-1` accepted tokens (`spending_review_2026`, `jtbd_notes_2026`) across CLI and Bicep guard suites, and scope compiled-default parity assertions to each parameter's catalog table row (`| \`<param>\` ... |`) while checking both `infra/*.bicep` and `modules/*.bicep` paths on disk.
* `PC-002` (`Low`, applied): Updated `P01-T01` to clarify in `docs/architecture/environment-region-quota-strategy.md` that `chatModel*` populate the default `standard` entry of `modelDeployments` forwarded as `deployments` to `modules/foundry.bicep` (removing the inaccurate `enableDemoChat` reference) and to document both `(?<![a-z0-9])...(?![a-z0-9])` and `(?<![0-9a-f])...(?![0-9a-f])` in `## Mechanical Fail-Closed Guards`.

## Dependencies

* `az bicep`, `python3`, `ruff`, `mypy`, and transient external venv with `PyYAML==6.0.3`, `src/api/requirements.txt`, and `./src/*` installed for `REQUIRE_AZ_BICEP=1` `test_bicep_policy.py` and `test_pipeline.py`.

## Follow-Up Items

* Execute fresh read-only Azure SQL (`GP_Gen5`), Foundry/OpenAI (`gpt-4.1-nano`), Container Apps, IoT Hub, and availability-zone queries (`R4`, `R5`, `R7`, `R8`, `R9`, `R11`, `R14`-`R17`) on the bound pilot subscription and record human sign-off before completing a private pilot `.bicepparam` copy (`Refs #137`).
* Triage pre-existing non-`--isolated` Ruff `0.17.3` notices (`EXE001`, `SIM102`, `SIM117`, `FURB167`) across older untouched `infra/` files in a standalone hygiene PR after stacked branches merge.

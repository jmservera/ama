<!-- markdownlint-disable-file -->
# RPI Plan: Issue #163 Explicit Deployment Attestation in Actual Mode and IaC Mismatch Disclosure (Cycle 4)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c4
* Parent Task ID: issue-163-chat-privacy-region-c3
* Task slug: issue-163-chat-privacy-region-c4
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan-critique.md

## Executive Summary

Cycle 4 closes Cycle 3 post-implementation review finding `RV-001` (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md`): requiring explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` attestation whenever `ZF_DATA_PROCESSING=actual` (`unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`), surfacing `deployment_attested: bool` in `ProviderPositionEvaluation` and `MODEL_PROVIDER_CONTRACT` across all modes, and documenting the current `infra/main.bicep` `chatModelSku = 'GlobalStandard'` default and omitted `containerapps.bicep` settings in `docs/reference/research/chat-memory-dpia.md` and `src/core/README.md` while keeping `infra/` untouched under Focused validation.

### User Decisions and Requirements Highlights

* **Fail closed on omitted deployment settings in `ZF_DATA_PROCESSING=actual` (`RV-001`)**: Even if a future PR flips `DPO_LEGAL_APPROVED = True`, `ZF_DATA_PROCESSING=actual` refuses unattested deployments where `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE` was omitted rather than silently assuming `uksouth` / `Standard` over `infra/main.bicep`'s `GlobalStandard` default.
* **Preserve `constructed`-mode synthetic defaults (`#281`, `#891`) with explicit `deployment_attested: False`**: Synthetic test fixtures (`APPROVED`, `REAL`) and the owner-approved synthetic demo (`#891`) continue to use `uksouth` / `Standard` defaults in `constructed` mode, with `deployment_attested: False` making the unattested fallback explicit.

### What You May Not Know

* Editing `infra/main.bicep` or `infra/modules/containerapps.bicep` would trigger the Full RPI gate (`tools/rpi-checks.py --all`), which the caller explicitly prohibited (`Validation tier: Focused; do not run tools/rpi-checks.py --all`). Enforcing explicit attestation in `src/core` for `actual` mode plus recording `deployment_attested: False` for `constructed` defaults closes the runtime safety gap inside Focused scope while routing the Bicep default update as an explicit Full-tier follow-up item.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the RPI loop for Issue #163 on `feat/chat-163-privacy-region` under Focused validation (`src/core`, `src/api`, `docs/reference/`; do not run `tools/rpi-checks.py --all`), preserving human DPO/Legal gating (`DPO_LEGAL_APPROVED = False`, `D1` to `D8` `"Not recorded"`) and prior Cycle 1–3 artifacts, and commit locally without pushing or opening a PR.

## Goals

* Close Cycle 3 finding `RV-001` with deterministic unit tests and verify `Outcome: Conformant` in Cycle 4 `rpi-review`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, and `src/core/tests/test_chat_provider_position.py`.

### Non-Goals

* Modifying `infra/` Bicep files (routed as Full-tier follow-up), modifying Cycle 1–3 RPI artifacts, altering `constructed`-mode `valid=True` synthetic fixture defaults, running `tools/rpi-checks.py --all`, pushing, or opening a PR.

## Functional Requirements

* Require explicit region and deployment-SKU attestation in `ZF_DATA_PROCESSING=actual` and expose `deployment_attested` across all modes (`RV-001`).
  * Observable acceptance criteria:
    * `MODEL_PROVIDER_CONTRACT["deployment_attested"]` (and `chat_privacy.MODEL_PROVIDER_POSITION["deployment_attested"]`) is `False`.
    * `evaluate_provider_position()` sets `deployment_attested = True` only when both region (`region` arg or `CHAT_PROVIDER_REGION` in `env`) and deployment SKU (`deployment_type` arg or `CHAT_DEPLOYMENT_TYPE` in `env`) are explicitly supplied and neither `"unapproved_region"` nor `"unapproved_deployment_residency"` (including `uksouth` + `DataZoneStandard`) is triggered; when either is omitted in `constructed` mode (`not is_actual`), `evaluate_provider_position()` falls back to `uksouth` / `Standard` with `deployment_attested = False`.
    * When `is_actual` is `True` (`ZF_DATA_PROCESSING=actual`), omitting `region` and `CHAT_PROVIDER_REGION` sets `region="unapproved"`, `residency_zone="unapproved"`, and appends `"unattested_region_in_actual_mode"` to `violations`; omitting `deployment_type` and `CHAT_DEPLOYMENT_TYPE` sets `deployment_type="unapproved"` and appends `"unattested_deployment_in_actual_mode"` to `violations`.
* Document the `infra/main.bicep` `chatModelSku = 'GlobalStandard'` mismatch and `deployment_attested` / actual-mode attestation rule in `docs/reference/research/chat-memory-dpia.md` and `src/core/README.md` (`RV-001`).
  * Observable acceptance criteria: Both documents explain that `infra/main.bicep` currently defaults `chatModelSku` to `GlobalStandard` without injecting `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE`, that `constructed` mode reports `deployment_attested = false` when defaulted, and that `ZF_DATA_PROCESSING=actual` fails closed unless both settings are explicitly attested alongside `DPO_LEGAL_APPROVED`.

## Non-Functional Requirements

* `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, `ChatDpiaRecordGuard`, `test_content_standard.py`, and `git diff --check` all exit `0` (`0` test removals, `0` new test methods, keeping `13` methods in `test_chat_provider_position.py`).

## Acceptance Criteria

* Cycle 3 `RV-001` is closed in code, documentation, and unit tests, and all focused suites pass with exit code `0`.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan-critique.md (Execution: Complete; Verdict: Revise; PC-001 applied directly) |
| Relevant research | .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md and .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c4-changes.md (Complete; P01-T01 and P01-T02 verified) |
| Planning execution and readiness | Complete and reconciled for Review |
| Continuation context | Confirmed automatic RPI Agent parent continues after critique disposition |

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md: Cycle 3 finding `RV-001`.
* infra/main.bicep and infra/modules/containerapps.bicep: Current `chatModelSku = 'GlobalStandard'` default and container environment variables.
* src/core/src/zava_forward/core/chat_provider_position.py: `ProviderPositionEvaluation`, `MODEL_PROVIDER_CONTRACT`, and `evaluate_provider_position()`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce Actual-Mode Deployment Attestation, Document IaC Default Mismatch, and Verify (`RV-001`)

* Intent: Close Cycle 3 `RV-001` in `chat_provider_position.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, and `src/core/tests/test_chat_provider_position.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Require explicit region and deployment SKU in `actual` mode, expose `deployment_attested`, and update docs (`RV-001`)

* Requirement and evidence: Cycle 3 `RV-001`; `infra/main.bicep:136`; `infra/modules/containerapps.bicep:237`.
* Expected result: `evaluate_provider_position()` exposes `deployment_attested: bool` (`False` when defaulted in `constructed` mode, `True` when both region and deployment type are explicitly supplied and approved) and fails closed in `ZF_DATA_PROCESSING=actual` with `"unattested_region_in_actual_mode"` / `"unattested_deployment_in_actual_mode"` whenever omitted; `docs/reference/research/chat-memory-dpia.md` and `src/core/README.md` document this posture and the `infra/main.bicep` `GlobalStandard` mismatch.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Expand unit assertions and run focused validation (`RV-001`)

* Requirement and evidence: Cycle 3 `RV-001`.
* Expected result: `test_chat_provider_position.py` asserts `deployment_attested is False` on defaulted `constructed` evaluations, `deployment_attested is True` when both `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` are explicitly set to approved values, and `"unattested_region_in_actual_mode"` / `"unattested_deployment_in_actual_mode"` when omitted in `ZF_DATA_PROCESSING="actual"` (versus absent when explicitly provided); focused unit suites, `ruff`, `mypy`, and `git diff --check` exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md

## Dependencies

* Cycle 1–3 RPI artifacts: Preserved unchanged.
* Named human DPO/Legal `D1` to `D8` sign-off and Full-tier `infra/main.bicep` SKU alignment: Tracked in `## Follow-Up Items`.

## Critique Disposition

Single-pass candidate critique `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan-critique.md` (`Execution: Complete`, `Verdict: Revise`) returned one compatible planner-owned correction:

* `PC-001` [Medium] (Applied directly): Updated `P01-T01` so `deployment_attested` requires `region_explicit and deployment_explicit and residency_zone != "unapproved" and safe_deployment != "unapproved" and "unapproved_deployment_residency" not in violations` (ensuring `uksouth` + `DataZoneStandard` reports `deployment_attested = False`), and updated `P01-T02` to assert `MODEL_PROVIDER_CONTRACT["deployment_attested"] is False` (`MODEL_PROVIDER_POSITION["deployment_attested"] is False`) and `uksouth` + `DataZoneStandard` `deployment_attested is False`.

## Follow-Up Items

* Obtain named DPO and Legal sign-off on decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention: Reserved to named human DPO and Legal owners under Issue #163 criterion 2.
* Align `infra/main.bicep` (`chatModelSku` default currently `GlobalStandard`) and inject explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` after DPO/Legal `D6` confirmation: Separate Full-tier IaC change requiring `tools/rpi-checks.py --all` outside Issue #163 Focused scope.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c4-changes.md
* Ready phase or task: Complete (`P01`); ready for single-pass Cycle 4 `rpi-review`
* Remaining provisional question or blocker: None

<!-- markdownlint-disable-file -->
# RPI Plan: Issue #163 Actual-Mode Provider Gate, Expiry Hold, and Retention Bound Hardening (Cycle 3)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c3
* Parent Task ID: issue-163-chat-privacy-region-c2
* Task slug: issue-163-chat-privacy-region-c3
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan-critique.md

## Executive Summary

Cycle 3 closes the three narrow residual findings (`RV-001` Medium, `RV-002` Low, `RV-003` Low) identified by Cycle 2 post-implementation review (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c2-review.md`): enforcing `DPO_LEGAL_APPROVED` directly inside `evaluate_provider_position()` for `ZF_DATA_PROCESSING=actual` (blocking actual-mode cross-border and Foundry queries across all entrypoints), gating `ChatPrivacy.purge_expired()` on `self.decision()["retention_days"]`, and bounding `len(days) <= 5` before `int(days)` to prevent Python `int_max_str_digits` `ValueError`.

### User Decisions and Requirements Highlights

* **Actual-mode DPO/Legal gate across all provider entrypoints (`RV-001`)**: `evaluate_provider_position()` appends `"actual_mode_dpo_legal_unapproved"` when `is_actual and not DPO_LEGAL_APPROVED`, while preserving `constructed`-mode synthetic fixture simulation (`test_chat_privacy.py`).
* **Expiry and digit-length safety (`RV-002`, `RV-003`)**: `ChatPrivacy.purge_expired()` returns `0` whenever `self.decision()["retention_days"]` is `None`, and `ChatPrivacy.decision()` checks `1 <= len(days) <= 5` before `int(days)`.

### What You May Not Know

* Keeping `ChatPrivacy._require()` check order as `missing` -> `synthetic_refs_in_actual_mode` -> `actual_mode_unapproved` -> `provider_position` preserves existing `ChatNotApproved` diagnostic specificity while `evaluate_provider_position` simultaneously enforces `"actual_mode_dpo_legal_unapproved"` for `require_provider_position`, `regulatory_privacy.readiness_report`, `regulatory_privacy.build_foundry_query`, and `GET /api/chat/status`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the RPI loop for Issue #163 on `feat/chat-163-privacy-region` with Focused validation and a clean local `Refs #163` commit without pushing or opening a PR, preserving the human DPO/Legal gate on `D1`–`D8` and preserving Cycle 1 and Cycle 2 RPI artifacts intact.

## Goals

* Close Cycle 2 findings `RV-001`, `RV-002`, and `RV-003` with deterministic unit tests and verify `Conformant` in Cycle 3 `rpi-review`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/chat_provider_position.py` (`RV-001`) and `src/core/src/zava_forward/core/chat_privacy.py` (`RV-002`, `RV-003`).
* `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md` one-phrase alignment if needed for `"actual_mode_dpo_legal_unapproved"`.
* Regression assertions in `src/core/tests/test_chat_provider_position.py` and `src/core/tests/test_chat_privacy.py`.

### Non-Goals

* Modifying Cycle 1 or Cycle 2 tracking artifacts, altering `constructed`-mode synthetic fixture behavior, running `tools/rpi-checks.py --all`, pushing, or opening a PR.

## Functional Requirements

* Block `ZF_DATA_PROCESSING=actual` directly in `evaluate_provider_position()` while `DPO_LEGAL_APPROVED` is `False` (`RV-001`).
  * Observable acceptance criteria: `evaluate_provider_position` appends `"actual_mode_dpo_legal_unapproved"` to `violations` (and sets `transfer_ref_recorded=False` when `is_actual and not DPO_LEGAL_APPROVED`) so `evaluate_provider_position`, `require_provider_position`, `regulatory_privacy.readiness_report`, and `regulatory_privacy.build_foundry_query` all fail closed (`valid=False` / `permitted=False`) under `ZF_DATA_PROCESSING=actual`—including `westeurope` with non-synthetic `CHAT_TRANSFER_REF="TRA-2026-99"`—while `constructed` mode remains unchanged.
* Gate `ChatPrivacy.purge_expired()` on an active approved retention period (`RV-002`).
  * Observable acceptance criteria: When `self.decision()["retention_days"]` is `None` (including when approval or provider checks fail after memory rows were stored), `ChatPrivacy.purge_expired()` returns `0` without deleting stored memory rows.
* Prevent oversized ASCII digit strings from raising `ValueError` in `ChatPrivacy.decision()` (`RV-003`).
  * Observable acceptance criteria: `ChatPrivacy.decision()` checks `1 <= len(days) <= 5 and days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` so `"9" * 5000` returns `retention_days=None` without raising `ValueError`.

## Non-Functional Requirements

* Zero lint, format, type, or whitespace errors (`ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, and `git diff --check` all exit `0`).
* Bounded deterministic test additions (`0` test removals; expand existing test methods in `test_chat_provider_position.py` and `test_chat_privacy.py`, keeping `test_chat_provider_position.py` at `13` methods `<= 16`).

## Acceptance Criteria

* Cycle 2 findings `RV-001` through `RV-003` are closed and covered by deterministic assertions that fail without Cycle 3's changes.
* Focused `src/core` and `src/api` test suites, `ruff`, `mypy`, and `git diff --check` exit `0`.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan-critique.md (Execution: Complete; Verdict: Pass; 0 findings) |
| Relevant research | .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md and .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c2-review.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c3-changes.md (Complete; P01-T01 and P01-T02 verified) |
| Planning execution and readiness | Complete and reconciled for Review |
| Continuation context | Confirmed automatic RPI Agent parent continues after critique disposition |

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c2-review.md: Cycle 2 findings `RV-001` through `RV-003`.
* src/core/src/zava_forward/core/chat_provider_position.py: `evaluate_provider_position()`.
* src/core/src/zava_forward/core/chat_privacy.py: `ChatPrivacy.decision()` and `ChatPrivacy.purge_expired()`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Actual-Mode Provider Gate, Expiry Hold, Oversized-Days Bound, and Tests (`RV-001`–`RV-003`)

* Intent: Apply the three surgical runtime fixes in `chat_provider_position.py` and `chat_privacy.py`, align doc notes, expand unit assertions, and pass focused validation.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Enforce `actual_mode_dpo_legal_unapproved` in `evaluate_provider_position()`, gate `purge_expired()`, and bound `len(days) <= 5` (`RV-001`–`RV-003`)

* Requirement and evidence: Cycle 2 `RV-001`, `RV-002`, `RV-003`.
* Expected result: `evaluate_provider_position()` appends `"actual_mode_dpo_legal_unapproved"` when `is_actual and not DPO_LEGAL_APPROVED`; `ChatPrivacy.purge_expired()` returns `0` when `not self.decision()["retention_days"]`; `ChatPrivacy.decision()` checks `1 <= len(days) <= 5` before `int(days)`; `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md` note `"actual_mode_dpo_legal_unapproved"`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression assertions and run focused validation (`RV-001`–`RV-003`)

* Requirement and evidence: Cycle 2 `RV-001`, `RV-002`, `RV-003`.
* Expected result: `test_chat_provider_position.py` and `test_chat_privacy.py` cover `ZF_DATA_PROCESSING="actual"` in `evaluate_provider_position` / `build_foundry_query` / `readiness_report` (both `uksouth` and `westeurope` with non-synthetic `CHAT_TRANSFER_REF`), `purge_expired()` no-op during retention hold on pre-populated expiring memory, and `"9" * 5000` in `CHAT_RETENTION_DAYS`; focused `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check` exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md

## Dependencies

* Cycle 1 and Cycle 2 artifacts: Preserved unchanged.
* Named human DPO and Legal review (`D1`–`D8`): Remains intentionally gated (`DPO_LEGAL_APPROVED = False`).

## Critique Disposition

Single-pass candidate critique `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan-critique.md` completed with `Critique execution status: Complete` and `Verdict: Pass` (`0` findings). No revisions required.

## Follow-Up Items

* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention: Reserved to named human DPO and Legal owners under Issue #163 criterion 2.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c3-changes.md
* Ready phase or task: Complete (`P01`); ready for single-pass Cycle 3 `rpi-review`
* Remaining provisional question or blocker: None

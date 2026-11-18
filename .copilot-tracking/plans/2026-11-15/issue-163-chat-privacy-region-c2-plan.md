<!-- markdownlint-disable-file -->
# RPI Plan: Issue #163 Model Provider Data-Handling and Region Position Remediation (Cycle 2)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c2
* Parent Task ID: issue-163-chat-privacy-region
* Task slug: issue-163-chat-privacy-region-c2
* Planning status: finalized
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan-critique.md

## Executive Summary

Cycle 2 surgically resolves all five findings (`RV-001` through `RV-005`) recorded by the Cycle 1 post-implementation review (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md`) before freezing the `Refs #163` local commit on `feat/chat-163-privacy-region`. It closes the `ZF_DATA_PROCESSING=actual` pre-DPO-approval gap (`RV-001`), ensures `regulatory_privacy.build_foundry_query` and `readiness_report` honor ambient `os.environ` when `env` is omitted and fail closed on malformed non-mapping `env` (`RV-002`), enforces ASCII `1..36500` bounds on `CHAT_RETENTION_DAYS` (`RV-003`), preserves conservative unverified abuse-monitoring disclosures (`RV-004`), and fixes `src/core/README.md` no-echo phrasing, EOF whitespace hygiene, and HTTP `/api/chat/status` test coverage (`RV-005`).

### User Decisions and Requirements Highlights

* **Human DPO/Legal gate strictly blocks live actual-mode storage and retention (`RV-001`)**: While repository-recorded `DPO_LEGAL_APPROVED` is `False` (`D1`–`D8` `"Not recorded"`), `ZF_DATA_PROCESSING=actual` refuses chat/memory storage and keeps `retention_days` `None` even if non-synthetic environment reference strings are supplied, while preserving `constructed` fixture test behavior.
* **Ambient `os.environ` fail-closed parity (`RV-002`)**: Omitting `env` (`env=None`) in `build_foundry_query` or `readiness_report` evaluates `os.environ` rather than `{}` and fails closed on non-`None`, non-`Mapping` `env` values.
* **Focused validation and clean local commit**: Re-verify unit suites across `src/core` and `src/api`, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check`, then commit locally without pushing or opening a PR.

### What You May Not Know

* In Python 3, `"\u00b2".isdigit()` is `True` (raising `ValueError` in `int("\u00b2")`) and `"\u0663\u0660".isdigit()` is `True`; checking `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` matches `regulatory_privacy._parse_retention_days` (`RV-003`).
* Recording `CHAT_ABUSE_MONITORING_MODIFIED_REF` in an environment variable does not verify Microsoft's subscription-level Modified Abuse Monitoring approval; keeping `default_sample_retention_days: 30`, `modified_abuse_monitoring_verified: False`, and `human_review_possible: True` under `mode="modified_recorded_unverified"` prevents unverified config strings from asserting zero-day retention (`RV-004`).

### Unresolved Decisions or Blockers

* None for Cycle 2 engineering remediation; named human DPO and Legal review of `D1`–`D8` remains an intentional external governance follow-up (`Refs #163`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the full RPI loop for Issue #163 on `feat/chat-163-privacy-region` (stacked onto `feat/demo-164-chat-grounding-provenance-0900`, PR #1641) with Focused validation and a clean local commit (`Refs #163`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`) without pushing or opening a PR (caller prompt; Cycle 1 review `RV-001`–`RV-005`).
* Keep `Lawful basis, staff notice and a DPIA decision are recorded by the DPO and Legal; no retention period is set before approval` explicitly gated on human DPO/Legal sign-off, ensuring no environment reference string alone activates live (`ZF_DATA_PROCESSING=actual`) chat/memory storage or retention while `D1`–`D8` remain `"Not recorded"` (caller prompt; `RV-001`).
* Remediate all Cycle 1 review findings (`RV-001` through `RV-005`) while preserving Cycle 1 RPI artifacts intact (owner correction-cycle grant 2026-11-09 / `#1798`).

## Goals

* Eliminate all five Cycle 1 defects (`RV-001` through `RV-005`) across `chat_provider_position.py`, `chat_privacy.py`, `regulatory_privacy.py`, `docs/reference/`, and `src/core/README.md`.
* Expand deterministic unit tests in `src/core/tests/` and `src/api/tests/` to cover every remediated edge case within locked test bounds and achieve `Conformant` post-implementation review.

## Scope and Non-Goals

### In Scope

* Surgical updates to `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/src/zava_forward/core/chat_privacy.py`, and `src/core/src/zava_forward/core/regulatory_privacy.py` (`RV-001` through `RV-004`).
* Surgical documentation and whitespace cleanup in `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, and `docs/reference/log.md` (`RV-004`, `RV-005`).
* Targeted regression tests in `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, and `src/api/tests/test_chat_panel.py` (`RV-001` through `RV-005`).

### Non-Goals

* Modifying Cycle 1 tracking artifacts (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md` remains preserved as historical Cycle 1 evidence).
* Simulating human DPO/Legal sign-off on `D1`–`D8`, running `tools/rpi-checks.py --all`, pushing, or opening a PR.

## Functional Requirements

* Block `ZF_DATA_PROCESSING=actual` chat/memory approval and retention while `DPO_LEGAL_APPROVED` is `False` (`RV-001`).
  * Observable acceptance criteria: `DPO_LEGAL_APPROVED: Final[bool] = False` is exported by `chat_provider_position.py`; under `ZF_DATA_PROCESSING=actual` with `DPO_LEGAL_APPROVED is False`, `ChatPrivacy.decision()` returns `approved=False`, `actual_mode_unapproved=True`, and `retention_days=None` even when non-synthetic `CHAT_*_REF` strings and `CHAT_RETENTION_DAYS="30"` are supplied, and `ChatPrivacy` write/opt-in methods raise `ChatNotApproved`; `constructed` fixture mode behavior remains unchanged.
* Evaluate ambient `os.environ` when `env=None` and fail closed on non-mapping `env` in `regulatory_privacy` (`RV-002`).
  * Observable acceptance criteria: Calling `regulatory_privacy.build_foundry_query(...)` or `regulatory_privacy.readiness_report()` with `env=None` reads `os.environ` (failing closed with `permitted=False` / `live_data_permitted=False` when ambient `CHAT_PROVIDER_REGION` or `CHAT_PROVIDER_TRAINING` is invalid); passing a non-`None`, non-`Mapping` `env` fails closed (`unapproved_region`) without echoing input.
* Enforce ASCII `1..36500` bounds on `CHAT_RETENTION_DAYS` in `ChatPrivacy.decision()` (`RV-003`).
  * Observable acceptance criteria: `ChatPrivacy.decision()` checks `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` without raising `ValueError` on superscript Unicode (`"\u00b2"`), rejecting non-ASCII digits (`"\u0663\u0660"`), `"0"`, negative values, and `"36501"` (`retention_days=None`, `purge_retention()["applied"]=False`).
* Preserve conservative abuse-monitoring disclosures when `CHAT_ABUSE_MONITORING_MODIFIED_REF` is unverified (`RV-004`).
  * Observable acceptance criteria: `AbuseMonitoringDisclosure` includes `modified_abuse_monitoring_verified: False` and keeps `default_sample_retention_days: 30` and `human_review_possible: True` under `mode="modified_recorded_unverified"`, without claiming zero-day retention or disabled human review from an unverified reference string.
* Align `src/core/README.md` no-echo prose, EOF whitespace hygiene, and HTTP `GET /api/chat/status` test coverage (`RV-005`).
  * Observable acceptance criteria: `src/core/README.md` scopes no-echo claims to `provider_position` and `regulatory_privacy.readiness_report()`; `docs/reference/research/chat-memory-dpia.md` reflects conservative unverified modified abuse-monitoring posture; `git diff --check` exits `0` with zero output; and `src/api/tests/test_chat_panel.py` verifies `GET /api/chat/status` exposes `provider_position`, flips `storage_approved` to `False` on unapproved regions, and never echoes raw ref/env canary values.

## Non-Functional Requirements

* Zero lint, format, type, or whitespace errors.
  * Objective threshold or evaluation condition: `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`, plus `git diff --check`, all exit `0`.
  * Observable acceptance criteria: Clean exit code `0` across all four static/hygiene checks.
* Bounded deterministic unit test delta.
  * Objective threshold or evaluation condition: `0` test removals; `<= 4` additional/updated test methods across `src/core/tests/test_chat_provider_position.py` and `src/core/tests/test_chat_privacy.py` (keeping `test_chat_provider_position.py` `<= 16` total methods) and `1` new test method in `src/api/tests/test_chat_panel.py`.
  * Observable acceptance criteria: 100% pass rate across focused `src/core` and `src/api` chat/privacy/regulatory suites.

## Acceptance Criteria

* All five Cycle 1 findings (`RV-001` through `RV-005`) are closed with deterministic unit test coverage.
* `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` remain `"Not recorded"`, `DPO_LEGAL_APPROVED` remains `False`, and `ZF_DATA_PROCESSING=actual` cannot activate chat/memory storage or retention before human DPO/Legal approval is committed.
* `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, focused unit test suites, and `git diff --check` all exit `0`.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan-critique.md (Complete; Verdict: Revise -> PC-001 and PC-002 resolved in finalized plan) |
| Relevant research | .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md and .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c2-changes.md is created by Cycle 2 implementation |
| Planning execution and readiness | Finalized and completed across P01 and P02; ready for Cycle 2 Review |
| Continuation context | Confirmed automatic RPI Agent parent continues after critique disposition |

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md: Cycle 1 findings `RV-001` through `RV-005`.
* .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md: Baseline privacy, DPIA, and test-guard findings `C1` through `C16`.
* src/core/src/zava_forward/core/chat_provider_position.py: Provider/region contract and `AbuseMonitoringDisclosure`.
* src/core/src/zava_forward/core/chat_privacy.py: `ChatPrivacy.decision()` and `ChatPrivacy._require()` approval and retention gates.
* src/core/src/zava_forward/core/regulatory_privacy.py: `readiness_report()` and `build_foundry_query()` provider enforcement.
* src/api/tests/test_chat_panel.py: HTTP `/api/chat/status` test suite.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Remediate Core Privacy, Retention, Foundry Ambient-Env, and Disclosure Defects (`RV-001`–`RV-004`)

* Intent: Close all four Cycle 1 runtime defects in `chat_provider_position.py`, `chat_privacy.py`, and `regulatory_privacy.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Gate `ZF_DATA_PROCESSING=actual` on `DPO_LEGAL_APPROVED`, enforce ASCII `1..36500` retention bounds, and preserve conservative unverified abuse-monitoring disclosure (`RV-001`, `RV-003`, `RV-004`)

* Requirement and evidence: Cycle 1 `RV-001`, `RV-003`, `RV-004`.
* Expected result: `chat_provider_position.py` exports `DPO_LEGAL_APPROVED: Final[bool] = False` and keeps `default_sample_retention_days: 30`, `modified_abuse_monitoring_verified: False`, and `human_review_possible: True` under `mode="modified_recorded_unverified"`; `chat_privacy.py` blocks `approved` and `retention_days` when `actual_mode(self.env)` and `not DPO_LEGAL_APPROVED` (`actual_mode_unapproved=True`) and validates `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce ambient `os.environ` when `env=None` and fail closed on non-mapping `env` in `regulatory_privacy.py` (`RV-002`)

* Requirement and evidence: Cycle 1 `RV-002`.
* Expected result: `regulatory_privacy.readiness_report(env=None)` and `regulatory_privacy.build_foundry_query(..., env=None)` pass `None` to `evaluate_provider_position` so ambient `os.environ` is checked, and reject non-`None`, non-`Mapping` `env` values fail-closed (`{"CHAT_PROVIDER_REGION": ""}`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Align Documentation, Whitespace Hygiene, and Regression Tests (`RV-001`–`RV-005`)

* Intent: Synchronize `src/core/README.md` and `docs/reference/` hygiene (`RV-004`, `RV-005`), add deterministic core and API HTTP tests covering `RV-001`–`RV-005`, and run focused validation.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Fix `src/core/README.md` no-echo claim, `chat-memory-dpia.md` unverified modified-abuse wording, and EOF blank lines (`RV-004`, `RV-005`)

* Requirement and evidence: Cycle 1 `RV-004`, `RV-005`.
* Expected result: `src/core/README.md` scopes no-echo guarantees to `provider_position` and `regulatory_privacy.readiness_report()`; `docs/reference/research/chat-memory-dpia.md` states that `CHAT_ABUSE_MONITORING_MODIFIED_REF` records `"modified_recorded_unverified"` while preserving conservative `30`-day / `human_review_possible: True` defaults until DPO/Legal subscription verification; trailing EOF blank lines in `docs/reference/log.md` and `docs/reference/research/chat-memory-dpia.md` are removed so `git diff --check` exits `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add core and HTTP `/api/chat/status` regression tests and run focused validation (`RV-001`–`RV-005`)

* Requirement and evidence: Cycle 1 `RV-001` through `RV-005`.
* Expected result: `test_chat_provider_position.py`, `test_chat_privacy.py` (`test_storage_refused_when_provider_or_region_unapproved`), and `src/api/tests/test_chat_panel.py` deterministically test non-synthetic refs in `ZF_DATA_PROCESSING=actual` mode, omitted-`env` ambient `os.environ` and non-mapping `env` blocking/no-echo in both `readiness_report()` and `build_foundry_query(...)`, non-ASCII (`"\u00b2"`, `"\u0663\u0660"`) and `>36500` `CHAT_RETENTION_DAYS`, conservative unverified abuse-monitoring fields, and HTTP `GET /api/chat/status` `provider_position` no-echo exposure; focused `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check` all exit `0`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md

## Dependencies

* Cycle 1 artifacts (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md`): Preserved unchanged as parent-task evidence.
* Named human DPO and Legal review (`D1`–`D8` in `docs/reference/research/chat-memory-dpia.md`): Remains intentionally gated (`DPO_LEGAL_APPROVED = False`).

## Critique Disposition

Single-pass critique executed at `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan-critique.md` (`Execution status: Complete`, `Verdict: Revise`, `0 Critical, 0 High, 1 Medium, 1 Low`). Both compatible planner-owned findings were applied directly without re-critique:

* `PC-001` [Medium] (Adopted directly): Expanded `P02-T02` to test both `regulatory_privacy.readiness_report()` and `regulatory_privacy.build_foundry_query(...)` with omitted `env` (`env=None` under `patch.dict(os.environ, ...)`) and malformed non-mapping `env` (`"PRIVATE-CANARY"` fail-closed and no-echo).
* `PC-002` [Low] (Adopted directly): Updated `P02-T02` to reference the exact existing method name `test_storage_refused_when_provider_or_region_unapproved` in `src/core/tests/test_chat_privacy.py`.

## Follow-Up Items

* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention: Outside engineering scope because repository legal/regulatory rules and Issue #163 criterion 2 reserve lawful-basis, staff-notice, DPIA, and retention approval to named human DPO and Legal owners.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c2-changes.md
* Ready phase or task: All Cycle 2 phases (`P01`, `P02`) complete and reconciled; ready for single-pass Cycle 2 `rpi-review`
* Remaining provisional question or blocker: None

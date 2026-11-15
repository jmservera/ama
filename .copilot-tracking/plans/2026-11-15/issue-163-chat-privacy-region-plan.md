<!-- markdownlint-disable-file -->
# RPI Plan: Issue #163 Model Provider Data-Handling and Region Position Contract

## Task Metadata

* Task ID: issue-163-chat-privacy-region
* Task slug: issue-163-chat-privacy-region
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md

## Executive Summary

This plan delivers the remaining engineering acceptance criterion on Issue #163 ("Model provider data handling and region position is recorded") by turning Zava Forward's passive vendor-position notes into a strictly typed, machine-enforced contract across `src/core`, `/api/chat/status`, and the canonical DPIA reference record in `docs/reference/research/chat-memory-dpia.md`. It codifies and enforces UK South (`uksouth` `Standard`) domestic residency and the bounded EU data-zone (`DataZoneStandard` / EEA) residency posture, zero foundation-model training on customer prompts and completions, structured synchronous content-filtering and abuse-monitoring disclosures, cross-border transfer prohibition without recorded DPO/Legal sign-off, and a hard block preventing any retention period from activating before DPO/Legal approval.

### User Decisions and Requirements Highlights

* **Issue #163 criterion 2 stays human-gated**: Lawful basis, staff notice, DPIA decision sign-off, and retention approval (`D1`–`D8`) remain explicitly `"Not recorded"` pending named human DPO and Legal review; engineering controls record and enforce the provider/region contract without claiming legal acceptance.
* **Fail-closed residency, zero-training, transfer, and pre-approval retention enforcement**: Unapproved Azure regions, global inference SKUs (`GlobalStandard`), enabled provider training flags, unapproved cross-border transfers outside `uksouth`, and pre-approval retention settings all fail closed.
* **Focused validation and local-only commit**: Verification runs `src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, and `mypy` without `tools/rpi-checks.py --all`, ending in a clean local commit on `feat/chat-163-privacy-region` (no push or PR).

### What You May Not Know

* `src/core/pyproject.toml` excludes legacy `chat_privacy.py` and `test_chat_privacy.py` from `ruff format` and `mypy`. Introducing a dedicated `chat_provider_position.py` module and `test_chat_provider_position.py` test suite ensures strict `mypy` and `ruff format --check` verify the new contract while preserving backward-compatible exports in `chat_privacy.py`.
* `PortabilityTests` in `src/core/tests/test_chat_privacy.py` forbids SQL keywords inside `chat_privacy.py`, `ChatDpiaRecordGuard` in `src/core/tests/test_chat_dpia_record.py` enforces `"Unknown"` retention cells and `"Not recorded"` `D1`–`D8` status in `docs/reference/research/chat-memory-dpia.md`, `Readiness` in `src/core/tests/test_regulatory_privacy.py` enforces the 8-item Issue #217 `CRITERIA` tuple and forbids echoing raw reference or arbitrary `env` strings in `readiness_report(env)`, and `src/api/tests/test_content_standard.py` forbids standalone `"human-approved"` phrasing across `src/core` and `src/api`.
* Container Apps synthetic demo templates set `ZF_ENV=production` alongside `ZF_DEPLOYMENT_PROFILE=demo` and synthetic/demo `CHAT_*_REF` pointers; therefore live personal-data enforcement keys off `data_protection.actual_mode(env)` (`ZF_DATA_PROCESSING` != `"constructed"`), rejecting `SYNTH-*`, `SYN-*`, `SYNTHETIC-*`, and demo/draft Markdown pointers in `actual` mode (and bare placeholder tokens like `"yes"`/`"true"` in all modes) without breaking synthetic demo fixtures.

### Unresolved Decisions or Blockers

* Human DPO and Legal review of `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` remains an intentional governance gate on Issue #163 criterion 2 (non-blocking for this engineering slice; PR/commit uses `Refs #163`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop (`rpi-research`, `rpi-plan` with independent critique, `rpi-implement`, and `rpi-review`) with dated artifacts under `2026-11-15` on branch `feat/chat-163-privacy-region` (stacked onto `feat/demo-164-chat-grounding-provenance-0900`, PR #1641) (caller prompt).
* Deliver the remaining engineering criterion on Issue #163: `Model provider data handling and region position is recorded`, while keeping `Lawful basis, staff notice and a DPIA decision are recorded by the DPO and Legal; no retention period is set before approval` explicitly gated on human DPO/Legal sign-off (caller prompt; GitHub Issue #163).
* Record and enforce in both `src/core` and canonical privacy reference documentation: Azure OpenAI / Foundry UK South / EU data-zone residency posture, zero model training on customer prompts/completions, abuse-monitoring and content-filtering data-handling disclosure, cross-border transfer prohibition without DPO/Legal sign-off, and no retention period active before DPO/Legal approval (caller prompt Objective 2).
* Add deterministic unit tests in `src/core/tests/` verifying exposure, validation, fail-closed rejection on unapproved regions or provider training flags, and preservation of the DPO/Legal human gate (caller prompt Objective 3).
* Use the Focused validation tier (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`) and commit all changes plus `.copilot-tracking/` artifacts cleanly on `feat/chat-163-privacy-region` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing or opening a PR (caller prompt Objective 4).

## Goals

* Establish one strictly typed, fail-closed model provider data-handling and region position contract in `src/core` and expose it consistently through `chat_privacy`, `regulatory_privacy`, and `/api/chat/status`.
* Align `docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` with the enforced residency, zero-training, abuse-monitoring/content-filtering, cross-border transfer, and pre-approval retention controls without fabricating human DPO/Legal approval.
* Prove fail-closed enforcement and regression safety through deterministic unit tests, `ruff`, and strict `mypy`.

## Scope and Non-Goals

### In Scope

* New strictly typed module `src/core/src/zava_forward/core/chat_provider_position.py` and integration into `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`, and `src/api/src/zava_forward/api/server.py`.
* Closing the pre-approval retention gap in `ChatPrivacy.decision()` and enforcing `actual_mode` (`ZF_DATA_PROCESSING=actual`) rejection of synthetic/demo references.
* Updating `docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Deterministic unit tests in `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, and `src/core/tests/test_chat_dpia_record.py`, plus focused validation across `src/core` and `src/api`.

### Non-Goals

* Recording or simulating human DPO or Legal sign-off on `D1`–`D8` or ticking Issue #163 criterion 2.
* Editing Bicep templates under `infra/`, Dockerfiles, workflows, or web UI assets under `src/api/src/zava_forward/api/web/`.
* Running `tools/rpi-checks.py --all`, pushing to `origin`, or opening a GitHub pull request.

## Functional Requirements

* Expose a structured model provider data-handling and region position contract (`MODEL_PROVIDER_CONTRACT` / `MODEL_PROVIDER_POSITION` / `evaluate_provider_position`) in `src/core` and `/api/chat/status`.
  * Observable acceptance criteria: `ChatPrivacy.provider_position()`, `ChatPrivacy.decision()["provider_position"]`, `regulatory_privacy.readiness_report()["provider_position"]`, and `GET /api/chat/status` return residency zone, deployment type, zero-training posture, content-filtering and abuse-monitoring disclosures, cross-border transfer status, violation codes, and `dpo_legal_approved: False`.
* Enforce the UK South / EU data-zone residency posture and cross-border transfer gate fail-closed.
  * Observable acceptance criteria: `uksouth` permits only regional `Standard` (`residency_zone="uk_south"`, `cross_border_transfer=False`, rejecting `DataZoneStandard` on `uksouth` as `unapproved_deployment_residency`); EU data-zone regions (`swedencentral`, `westeurope`, `northeurope`, `francecentral`, `germanywestcentral`, `italynorth`, `polandcentral`, `spaincentral`) permit `Standard` or `DataZoneStandard` (`residency_zone="eu_data_zone"`, unconditionally deriving `cross_border_transfer=True`) and fail closed (`cross_border_transfer_unapproved`) unless a valid `CHAT_TRANSFER_REF` is recorded; any non-UK/non-EU region (e.g. `eastus`, `westus`, empty) fails closed (`unapproved_region`, `residency_zone="unapproved"`) and any global SKU (`GlobalStandard`, `GlobalBatch`) fails closed (`unapproved_deployment_residency`), raising `ChatNotApproved` on `ChatPrivacy` write/opt-in paths and returning `permitted=False` in `regulatory_privacy.build_foundry_query`.
* Enforce zero model training on customer prompts, completions, and opt-in memory fail-closed.
  * Observable acceptance criteria: `zero_model_training` is `True` and `customer_data_training` is `False`; setting `CHAT_PROVIDER_TRAINING` to any truthy or unrecognized value (or `customer_data_training=True`) produces `valid=False` with `"provider_training_prohibited"` and blocks `ChatPrivacy` thread/message/memory operations with `ChatNotApproved`.
* Record structured synchronous content-filtering and abuse-monitoring data-handling disclosures.
  * Observable acceptance criteria: The exposed contract distinguishes stateless synchronous `Azure AI Content Safety` filtering from default 30-day encrypted flagged-sample storage and Microsoft human review (`mode="platform_default_unverified"` unless `CHAT_ABUSE_MONITORING_MODIFIED_REF` is recorded; `uk_reviewer_residency_verified=False`, `eea_reviewer_residency_documented=True`).
* Block any active retention period before DPO/Legal approval and reject synthetic/demo references in live personal-data mode (`ZF_DATA_PROCESSING=actual`).
  * Observable acceptance criteria: `ChatPrivacy.decision()["retention_days"]` is `None` and `purge_retention()["applied"]` is `False` whenever any approval gate (`CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF`, or `provider_position["valid"]`) is unsatisfied, `CHAT_RETENTION_REF` is missing, `CHAT_RETENTION_DAYS` is non-ASCII or outside `1..36500`, or `SYNTH-*` / demo Markdown references are used under `ZF_DATA_PROCESSING=actual`.
* Document the enforced contract in canonical knowledge-base and module docs while preserving human-review boundaries.
  * Observable acceptance criteria: `docs/reference/research/chat-memory-dpia.md` documents the residency posture matrix, zero-training rule, content-filtering and abuse-monitoring disclosures, cross-border transfer prohibition, environment variables, and pre-approval retention gate while `D1`–`D8` remain `"Not recorded"` and chat/memory data-map retention rows remain `"Unknown ..."`.

## Non-Functional Requirements

* Strict static typing and formatting compliance on new and typed modules.
  * Objective threshold or evaluation condition: Zero `mypy` errors and zero `ruff check` / `ruff format --check` findings across `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run `python3 -m ruff check`, `python3 -m ruff format --check`, and `python3 -m mypy` in `src/core` and `src/api`.
  * Observable acceptance criteria: All lint, format, and strict type checks exit `0`.
* Regression and guard invariance across SQL portability, plain-language content standard, and DPIA record guards.
  * Objective threshold or evaluation condition: 100% pass rate across `src/core` and `src/api` unit test suites, with `0` removed tests and bounded test additions (`<= 15` new tests in `src/core/tests/test_chat_provider_position.py`, `<= 6` new tests across `test_chat_privacy.py` and `test_chat_dpia_record.py`).
  * Operating condition or verification approach, if needed: Run focused chat, memory, privacy, DPIA, regulatory, content-standard, and dependency-rule `unittest` suites across `src/core`, `src/agents`, and `src/api`.
  * Observable acceptance criteria: Every existing and newly added affected unit test passes deterministically without network or external DB access.

## Acceptance Criteria

* `src/core/src/zava_forward/core/chat_provider_position.py` exists, passes strict `mypy` and `ruff format --check`, and is integrated into `chat_privacy.py`, `regulatory_privacy.py`, and `src/api/src/zava_forward/api/server.py` (`/api/chat/status`).
* Unapproved regions, `GlobalStandard` deployments, provider training flags, unapproved cross-border transfers, pre-approval retention configurations, and `SYNTH-*`/demo references under `ZF_DATA_PROCESSING=actual` all fail closed deterministically.
* `MODEL_PROVIDER_POSITION["documented_terms"]["status"]` remains `"vendor_documentation_not_dpo_accepted"`, `dpo_legal_approved` / `dpo_reviewed` remains `False`, `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` remain `"Not recorded"`, and Issue #163 criterion 2 remains unticked/human-gated.
* `docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` are updated cleanly following repository Markdown rules and contain zero `.copilot-tracking/` references.
* All unit tests in `src/core` and `src/api`, `ruff check`, `ruff format --check`, and `mypy` pass, and all changes plus `.copilot-tracking/` artifacts are committed locally on `feat/chat-163-privacy-region` with the `Co-authored-by` trailer and without pushing or opening a PR.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md                                                                 |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md                                                      |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md with Revise disposition resolved across PC-001 through PC-005 |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md                                                          |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; Ready for implementation after resolving PC-001 through PC-005                                                                 |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to rpi-implement                                                                 |

## Sources

* .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md: Cycle 1 findings `C1`–`C16` covering `chat_privacy.py`, `regulatory_privacy.py`, `data_protection.py`, `server.py`, `infra/`, `chat-memory-dpia.md`, and test/lint/type guards.
* src/core/src/zava_forward/core/chat_privacy.py: Existing `DATA_MAP`, `MODEL_PROVIDER_POSITION`, `ChatNotApproved`, and `ChatPrivacy` storage, retention, and memory controls.
* src/core/src/zava_forward/core/regulatory_privacy.py: Existing strictly typed 8-item `CRITERIA` tuple, no-echo `readiness_report(env)`, `retention_alignment`, and `build_foundry_query` controls.
* src/core/src/zava_forward/core/data_protection.py: Existing `actual_mode(env)` helper distinguishing constructed/synthetic processing from live personal-data processing.
* docs/reference/research/chat-memory-dpia.md: Canonical privacy and draft DPIA document guarded by `src/core/tests/test_chat_dpia_record.py`.
* src/core/pyproject.toml: Lint, format, and `mypy` configuration explaining why a dedicated new module and test file are needed for strict static checks.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Enforceable Provider Data-Handling and Region Contract

* Intent: Introduce the strictly typed provider/region contract module and enforce fail-closed residency, zero-training, abuse-monitoring/content-filtering disclosure, cross-border transfer, and pre-approval retention invariants across `src/core` and `/api/chat/status`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create typed `chat_provider_position.py` contract and fail-closed validator

* Requirement and evidence: Caller Objective 2; Research `C1`, `C5`, `C9`, `C10`, `C11`, `C15`, `C16`.
* Expected result: `src/core/src/zava_forward/core/chat_provider_position.py` defines residency constants (`uksouth` primary and bounded `EU_DATA_ZONE_REGIONS`), `APPROVED_DEPLOYMENT_TYPES` (`Standard`, `DataZoneStandard`), zero-training enforcement, structured content-filtering and abuse-monitoring disclosures, cross-border transfer sign-off validation (`CHAT_TRANSFER_REF`), `actual_mode` synthetic/demo ref rejection, `evaluate_provider_position()`, and `require_provider_position()`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire provider contract and pre-approval retention gate into `chat_privacy.py`, `regulatory_privacy.py`, and `server.py`

* Requirement and evidence: Caller Objective 2; Research `C1`, `C2`, `C3`, `C6`, `C12`, `C13`, `C15`, `C16`; Critique `PC-001`, `PC-004`, `PC-005`.
* Expected result: `MODEL_PROVIDER_POSITION` preserves all legacy keys while exposing structured residency/handling fields; `ChatPrivacy` entrypoints carry PEP 484 type annotations and fail closed on invalid provider/region/training/transfer settings while keeping `retention_days` `None` before DPO/Legal approval (or with synthetic/demo refs in `ZF_DATA_PROCESSING=actual` mode); `regulatory_privacy.readiness_report(env)` attaches no-echo `provider_position` while preserving the 8-item `CRITERIA` tuple, `regulatory_privacy.build_foundry_query` fails closed when `provider_position` is invalid, and `/api/chat/status` surfaces `provider_position`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Update Canonical Privacy and DPIA Reference Documentation

* Intent: Record the enforced model provider data-handling and region position contract in canonical documentation and the knowledge-base index/changelog while preserving the human DPO/Legal gate.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Record residency matrix, data-handling disclosures, transfer gate, and retention gate in `chat-memory-dpia.md`

* Requirement and evidence: Caller Objective 2; Research `C7`, `C8`, `C14`.
* Expected result: `docs/reference/research/chat-memory-dpia.md` (`ms.date: 2026-11-15`) documents the UK South / EU data-zone residency posture, prohibited `GlobalStandard` and third-country regions, zero-training enforcement, synchronous content-filtering vs 30-day abuse-monitoring disclosure, cross-border transfer prohibition without `CHAT_TRANSFER_REF`, and pre-approval retention gate while keeping `D1`–`D8` `"Not recorded"` and chat/memory retention `"Unknown ..."`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Synchronize `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`

* Requirement and evidence: Knowledge Base Conventions; Research `Q5`, `C7`.
* Expected result: `src/core/README.md` documents `chat_provider_position.py` and environment gates; `docs/reference/README.md` updates the `chat-memory-dpia.md` index description; `docs/reference/log.md` appends a dated `2026-11-15` entry without rewriting earlier entries.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add Deterministic Unit Tests and Run Focused Validation

* Intent: Prove contract exposure, fail-closed validation, pre-approval retention blocking, DPO/Legal human-gate preservation, and zero lint/format/type/regression issues across `src/core` and `src/api`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add deterministic unit tests in `src/core/tests/`

* Requirement and evidence: Caller Objective 3; Research `C11`, `C12`, `C13`, `C14`.
* Expected result: New strictly typed `src/core/tests/test_chat_provider_position.py` (`<= 15` tests; `0` removals) plus targeted additions in `src/core/tests/test_chat_privacy.py` and `src/core/tests/test_chat_dpia_record.py` (`<= 6` tests; `0` removals) deterministically verify residency posture, fail-closed rejection on unapproved regions/SKUs/training flags/transfers, abuse-monitoring and content-filtering disclosures, pre-approval retention blocking, `ZF_DATA_PROCESSING=actual` synthetic/demo ref rejection, and DPO/Legal gate preservation.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run focused test, lint, format, and type-check suite across `src/core` and `src/api`

* Requirement and evidence: Caller Objective 4; Research `C11`, `C15`.
* Expected result: Focused chat, memory, privacy, DPIA, regulatory, content-standard, and dependency-rule `unittest` suites across `src/core`, `src/agents`, and `src/api`, plus full `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api`, all exit `0` without running `tools/rpi-checks.py --all`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md

## Dependencies

* Stacked parent branch `feat/demo-164-chat-grounding-provenance-0900` (PR #1641): Already checked out as the base of `feat/chat-163-privacy-region` in this worktree; must not be rebased or pushed.
* Named human DPO and Legal review (`D1`–`D8` in `docs/reference/research/chat-memory-dpia.md`): Remains an external governance dependency for Issue #163 criterion 2 and live personal-data chat/memory activation; preserved as `"Not recorded"` / `dpo_legal_approved=False`.

## Critique Disposition

Independent one-pass candidate critique executed in `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md` (verdict: `Revise`, `0 Critical, 2 High, 2 Medium, 1 Low`; `User response required: No`). All five planner-owned findings are resolved below.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` (High)    | resolved    | Preserved `regulatory_privacy.CRITERIA` at its 8 Issue #217 4-tuples, normalized `readiness_report(env)` input, gated `live_data_permitted` on `provider_position["valid"]`, and prohibited echoing raw reference strings or unallowlisted `env` values inside `provider_position`. |
| Run 1 `PC-002` (High)    | resolved    | Removed non-existent `data_protection.is_synthetic_ref` import; defined local `is_demo_or_synthetic_ref` (`SYNTH-*`, `SYN-*`, `SYNTHETIC-*`, `chat-demo-storage-approval-*`, `chat-demo-breakglass-disclaimer-*`, `chat-memory-dpia.md`) and `is_valid_governance_ref` rejecting bare placeholder tokens (`"yes"`, `"true"`, `"approved"`, etc.). |
| Run 1 `PC-003` (Medium)  | resolved    | Scoped `DataZoneStandard` exclusively to `EU_DATA_ZONE_REGIONS` (rejecting `DataZoneStandard` on `uksouth` as `unapproved_deployment_residency`) and unconditionally derived `cross_border_transfer=True` whenever `region != "uksouth"`. |
| Run 1 `PC-004` (Medium)  | resolved    | Added PEP 484 type annotations to `ChatPrivacy` methods invoked from strictly typed `test_chat_provider_position.py` so `mypy` passes without `[no-untyped-call]` or new exclusions. |
| Run 1 `PC-005` (Low)     | resolved    | Enforced `evaluate_provider_position(env)` fail-closed check inside `regulatory_privacy.build_foundry_query` and added unit test coverage in `P03-T01`. |

## Follow-Up Items

* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention: Outside engineering scope because repository legal/regulatory rules and Issue #163 criterion 2 reserve lawful-basis, staff-notice, DPIA, and retention approval to named human DPO and Legal owners.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None for engineering criterion 5; human DPO/Legal sign-off on criterion 2 remains intentionally gated.

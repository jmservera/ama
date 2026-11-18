<!-- markdownlint-disable-file -->
# RPI Plan: Issue #220 Criterion 5 — No Retaliation, Inferred Refusal or Delayed Hazard Response

## Task Metadata

* Task ID: issue-220-no-retaliation-2026-11-15
* Task slug: 220-no-retaliation
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/220-no-retaliation-plan-critique.md

## Executive Summary

This plan delivers the remaining acceptance criterion of Issue #220 (**No retaliation, inferred refusal or delayed hazard response**) across both `src/core` and `src/api`. When a resident, their representative or nominee, or a staff member records, updates, reopens, escalates, or resolves a challenge or correction request across digital, phone, letter, in-person, assisted-visit, trusted-intermediary, or AI/assistant proposal channels, the system will enforce at runtime that **case priority and ranking never drop**, **no refusal, no-access, sanction, withdrawal, or negative engagement flag is ever recorded or inferred**, **no unrelated work item is closed**, and **no statutory or emergency hazard or safeguarding clock is paused, reset, or delayed**. Any hazard concern raised inside a challenge immediately creates a receipt-dated hazard referral and, when intake details are supplied, immediately routes an active independent case safety record without waiting for challenge review, backed by a machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` contract in records, views, API responses, and audit logs.

### User Decisions and Requirements Highlights

* **All challenge/correction entrypoints covered**: Enforces invariants across `ChallengeRegister`, store-backed `resident_action` / `followup_action` (`challenge_open`, `challenge_update`, `challenge_reopen`, `challenge_escalate`, `challenge_resolve`, `nomination_*`, `service_*`), `ai_task` and `form_review` suggestions, SQLite `Assistants.challenge`, HTTP API routes, and `web/panels.js`.
* **Conflict boundary with UX parent #1639**: Leaves `src/api/src/zava_forward/api/web/role-screens.js` completely untouched.
* **Plain-language content standard preserved**: Keeps `src/api/tests/test_content_standard.py` green by avoiding prohibited phrases in Python and prohibited internal nouns in `web/*.js` while formatting panel/assistant errors with `"Owner: ... Next action: ..."`.
* **Focused Tier local validation and frozen commit**: Runs `ruff check`, `ruff format --check`, `mypy`, and targeted/suite tests in `src/core` and `src/api` using `pip`/`python3` only, then commits code, tests, docs, and `.copilot-tracking/` artifacts locally without pushing.

### What You May Not Know

* Existing regression suites (`src/core/tests/test_resident_decisions.py`, `src/core/tests/test_issue_220_challenge_route.py`, and `src/api/checks/challenge_browser_check.py`) pop `affected_challenges` after standard challenge operations and assert exact equality with the prior case dictionary (`after == before`), and also test a challenge update containing `"while damp repair continues"` while asserting exact hazard count `2`. Because of those regression locks, `non_retaliation_assurance` and `hazard_clock_preserved` are stored directly on each challenge record (and projected cleanly on `followup_view` / assistant views), while appending a new `c["hazards"]` entry occurs deterministically when explicit `hazard_intake` accompanies `hazard_concern=True` rather than via free-text keyword heuristics.
* `src/core/tests/test_resident_decisions.py` explicitly verifies that unverified `nomination_record(..., hazard_concern=True)` raises `ValueError` directing immediate safety reporting; this plan preserves that fail-closed guard unchanged while wrapping `nomination_record`, `nomination_correct`, and `nomination_review` in runtime non-retaliation verification.
* `SqlStore` replays `_res_*` handlers on a detached case dictionary inside `validate_resident_sql` during `save()` (`PC-001`) and indexes `priority_correction` across `sqlstore.py` and `mssqlstore.py` (`PC-002`); immediate `hazard_intake` audit persistence skips detached replay validation, and reopened `"Correction recorded"` challenges stay indexed across JSON, SQLite, and MSSQL stores as well as blocking stale `ai_tasks.review` acceptance (`PC-003`).
* ADR 0006 excludes legacy modules (`resident_decisions.py`, `sqlstore.py`, `mssqlstore.py`, `ai_tasks.py`, `assistants.py`, `server.py`) from `ruff format`; formatting applies only to non-excluded Python modules (`challenges.py` and the two new test files) while `ruff check`, `ruff format --check`, and `mypy --strict` validate the full `src/core` and `src/api` packages.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan` with single-pass `rpi-plan-critique`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` for `220-no-retaliation` on branch `feat/ai-220-no-retaliation` in `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation` (caller prompt).
* Inspect challenge and correction paths across `src/core` and `src/api` without modifying `src/api/src/zava_forward/api/web/role-screens.js` to avoid conflicts with `#1639` (caller prompt).
* Enforce and prove end-to-end across resident digital, staff-recorded non-digital, representative/nominee, and AI proposal challenge/dispute entrypoints that raising, updating, reopening, escalating, or resolving a challenge or correction request never lowers priority/ranking score, never sets or infers `refusal`, `no_access`, `sanction`, `withdrawn`, or negative engagement flags, never closes unrelated work items, and never delays, pauses, or extends statutory or emergency hazard response clocks (`awaiting_hazard_action`, Awaab's Law 24h/7d/14d clocks, or safeguarding clocks) (caller prompt; Issue #220 Criterion 5; Closure Audit Batch 014).
* Ensure any hazard concern mentioned in a challenge or correction request across any channel immediately routes/preserves independent hazard intake without waiting for challenge review, and exposes an explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` audit and view contract (caller prompt).
* Add comprehensive unit and integration tests in `src/core/tests/test_challenge_no_retaliation_220.py` and `src/api/tests/test_challenge_no_retaliation_api_220.py` (caller prompt).
* Ensure `src/api/tests/test_content_standard.py` passes cleanly with zero forbidden phrases (caller prompt).
* Validate at the Focused Tier (`ruff check`, `ruff format --check`, `mypy`, focused and suite `unittest` runs in `src/core` and `src/api` via `pip` only, no `uv`), commit all code, tests, docs, and `.copilot-tracking/` artifacts with the Copilot trailer, and do not push (caller prompt).

## Goals

* Enforce runtime fail-closed non-retaliation, non-refusal, non-closure, and statutory/emergency clock preservation across every challenge, correction, reopen, escalation, resolution, representative/nominee, and AI/assistant proposal dispute route.
* Provide immediate receipt-dated hazard referral and optional atomic independent case hazard intake routing whenever `hazard_concern=True` is raised on any challenge or correction channel without waiting for challenge review.
* Expose a uniform machine-checkable `non_retaliation_assurance` dictionary and `hazard_clock_preserved: True` contract across core records, person-facing/staff views, assistant proposal views, HTTP responses, and audit logs.
* Prove end-to-end conformance and tamper rejection across JSON `Store`, SQLite `SqlStore`, `ChallengeRegister`, `Assistants`, HTTP endpoints, and workbench UI assets while keeping all existing regression and content-standard suites passing.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/challenges.py`: expanded `FORBIDDEN_ADVERSE_FIELDS`, `build_non_retaliation_assurance`, upgraded `assert_no_adverse_challenge_effects`, `ChallengeRegister.reopen`, representative/nominee fields (`submitted_by`, `representative_ref`), and `non_retaliation_assurance` / `hazard_clock_preserved` on records and `.view()`.
* `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, and `src/core/src/zava_forward/core/ai_tasks.py`: expanded `CHALLENGE_CHANNELS` (`"Assisted visit"`, `"Trusted intermediary"`), `_res_challenge_reopen` (`challenge_reopen`), optional `submitted_by` / `representative_ref` / `hazard_concern` / `hazard_intake`, replay-safe immediate independent hazard intake routing (`PC-001`), reopened-correction SQL indexing (`PC-002`), `ai_task` and `form_review` challenge target support plus `ai_tasks.review` stale-correction guard (`PC-003`), runtime `assert_no_adverse_challenge_effects` + `_ranking()` guard across challenge/nomination/service mutations, `non_retaliation_assurance` / `hazard_clock_preserved` on records and `followup_view`, and audit tags.
* `src/core/src/zava_forward/core/assistants.py`: `Assistants.challenge(user, tid, body)` (`open`, `update`, `reopen`, `escalate`, `resolve`) on SQLite `assistant_tasks` proposals with immediate hazard referral/intake, correction staleness (`challenged_stale`), runtime `assert_no_adverse_challenge_effects`, transient `_view` key stripping + `_withhold_sensors` challenge-note redaction (`PC-004`), and `non_retaliation_assurance` / `hazard_clock_preserved` in `_view` and event history.
* `src/api/src/zava_forward/api/server.py` and `src/api/src/zava_forward/api/web/panels.js`: `POST /api/assistants/proposals/<tid>/challenge` and non-breaking workbench challenge panel support for non-digital intermediary channels, representative/nominee submission, safety-concern flag, challenge reopen (`#challenge-reopen-<id>`), and plain-language non-retaliation & safety-clock-preserved status.
* `src/core/tests/test_challenge_no_retaliation_220.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, `src/core/README.md`, and `src/api/README.md`.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js`.
* Infrastructure, Bicep, Dockerfile, workflow YAML, or package-manifest changes.
* Pushing commits to `origin` or altering branch protection.

## Functional Requirements

* **FR-1 (Lifecycle & Reopen Across All Channels)**: Support `open`/`submit`, `update`, `reopen`, `escalate`, and `resolve` across resident digital (`Digital`), staff-recorded non-digital (`Phone`, `Letter`, `In person`, `Assisted visit`, `Trusted intermediary`), representative/nominee (`submitted_by` in `The resident`, `Their representative`, `Nominee` with `representative_ref`), `ai_task` and `form_review` case suggestions, and SQLite `assistant_tasks` proposals.
  * Observable acceptance criteria: Every channel and target kind completes open, update, escalate, resolve, and reopen in JSON `Store`, SQLite `SqlStore`, `ChallengeRegister`, and `Assistants` while rejecting unknown fields (`400`) and preserving prior resolution history and `"Correction recorded"` staleness upon reopen.
* **FR-2 (Runtime Non-Retaliation, Non-Refusal, and Non-Closure Guard)**: Enforce `assert_no_adverse_challenge_effects` and case `_ranking()` invariance across every challenge, correction, nomination, service-dispute, and assistant-challenge write path.
  * Observable acceptance criteria: Priority/ranking (`score`, `urgent`, `priority`, `_ranking()`), engagement/consent (`refusal`, `no_access`, `non_access`, `sanction`, `withdrawn`, `negative_engagement`, `decision`, `measure_decisions`, `resident`), and unrelated work items (`tasks`, `returns`, `service_requests`, `work_orders`, `packages`, `handoff`, `resident_update`, `closed`) remain unchanged; injected adverse mutations fail closed with `ChallengeSafeguardError`.
* **FR-3 (Zero Hazard/Safeguarding Delay & Immediate Independent Hazard Intake)**: Preserve all statutory and emergency clocks (`awaiting_hazard_action`, Awaab's Law 24h emergency and 7d/14d investigation/summary/make-safe deadlines, `safeguarding` clocks, and active safety holds) across all challenge actions, and route `hazard_concern=True` immediately without waiting for challenge review.
  * Observable acceptance criteria: Pre-existing hazards and safeguarding clocks remain byte-for-byte unchanged (`hazards[:N] == before_hazards`); `hazard_concern=True` immediately records `hazard_referral` (`status="referred_on_receipt"`, `independent_intake=True`, `waits_for_challenge_review=False`) without resetting `received_on` on subsequent updates, and when `hazard_intake` is provided on store-backed routes, immediately appends an active independent case hazard (`released=False`, `hold.status="Active"`) with `safety_raised` / `safety_emergency` audit evidence.
* **FR-4 (Machine-Checkable `non_retaliation_assurance` & `hazard_clock_preserved` Contract)**: Expose explicit `non_retaliation_assurance` booleans and `hazard_clock_preserved: True` on challenge records, `.view()`, `followup_view` / `detail()`, `Assistants._view` / `.challenge()`, HTTP API responses, and challenge audit log entries, with plain-language rendering in `web/panels.js`.
  * Observable acceptance criteria: Unit and HTTP API tests assert exact boolean fields on `non_retaliation_assurance` and `hazard_clock_preserved is True` across records, views, responses, and verified hash-chained audit logs.

## Non-Functional Requirements

* **NFR-1 (Backward Compatibility & Regression Safety)**
  * Objective threshold or evaluation condition: Zero regressions across existing `src/core/tests` and `src/api/tests` suites, preserving strict `after.pop("affected_challenges"); after == before` and `challenge_browser_check.py` form contracts.
  * Operating condition or verification approach: Run full `unittest discover` suites in `src/core` and `src/api`.
  * Observable acceptance criteria: All existing and new tests in `src/core` and `src/api` pass with `0` failures and `0` errors.
* **NFR-2 (Type Safety, Lint Cleanliness, and Plain-Language Compliance)**
  * Objective threshold or evaluation condition: Zero errors from `ruff check`, `ruff format --check`, `mypy` (`strict = true`), and `test_content_standard.py`, with `git diff --name-only` confirming `web/role-screens.js` is untouched.
  * Operating condition or verification approach: Run `ruff check`, `ruff format --check`, and `mypy` inside `src/core` and `src/api`, plus `test_content_standard.py`.
  * Observable acceptance criteria: All linters, format checks, strict type checks, and content-standard tests exit `0`.

## Acceptance Criteria

* Raising, updating, reopening, escalating, or resolving a challenge or correction request across resident digital, staff-recorded non-digital, representative/nominee, `ai_task`/`form_review`, and `Assistants` proposal routes never lowers case priority or `_ranking()`, never sets or infers `refusal`, `no_access`, `sanction`, `withdrawn`, or negative engagement flags, never closes unrelated work items, and never delays, pauses, or resets `awaiting_hazard_action`, Awaab's Law 24h/7d/14d clocks, or `safeguarding` clocks.
* Any hazard concern flagged on a challenge or correction request across any channel immediately records receipt-dated `hazard_referral` (`waits_for_challenge_review: False`) and, when `hazard_intake` details are supplied on store-backed routes, atomically creates an active independent case hazard entry without waiting for challenge review or altering existing hazard clocks.
* Challenge records, views (`ChallengeRegister.view`, `Store.detail`/`SqlStore.detail`, `Assistants.detail`), HTTP responses, and audit entries expose machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved: True`.
* Test ownership and scope lock: exact test file removals = `none`; maximum new test files = `2` (`src/core/tests/test_challenge_no_retaliation_220.py` for core semantic & tamper-guard invariants across `ChallengeRegister`/`Store`/`SqlStore`/`Assistants`, and `src/api/tests/test_challenge_no_retaliation_api_220.py` for HTTP endpoint, audit, and workbench static-asset integration contracts); canonical source targets only (no generated artifacts); `test_content_standard.py`, `ruff`, `mypy`, and full `src/core` + `src/api` unit suites pass cleanly; `web/role-screens.js` remains unmodified.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md                                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md                                                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/220-no-retaliation-plan-critique.md with Revise verdict; PC-001..PC-004 resolved directly |
| Relevant research                | .copilot-tracking/research/2026-11-15/220-no-retaliation-research.md                                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md is created or continued by implementation as its evidence record       |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                        |
| Continuation context             | Confirmed automatic RPI Agent parent continues to rpi-implement automatically                                                             |

## Sources

* `.copilot-tracking/research/2026-11-15/220-no-retaliation-research.md`: Cycle 1 `C1`-`C18` codebase evidence, regression locks, and converged architecture.
* `src/core/src/zava_forward/core/challenges.py`: Existing `ChallengeRegister`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, and `assert_no_adverse_challenge_effects`.
* `src/core/src/zava_forward/core/resident_decisions.py`: Existing `ResidentDecisionMixin` challenge, nomination, representative-authority, and service-dispute handlers.
* `src/core/src/zava_forward/core/assistants.py` and `src/core/src/zava_forward/core/ai_tasks.py`: Existing AI task recommendation and SQLite assistant proposal lifecycle handlers.
* `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`, and `src/api/tests/test_content_standard.py`: HTTP routing, workbench challenge panel, and plain-language content constraints.
* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, and GitHub Issue #220: Governance, Awaab's Law hazard duties, resident/representative redress, and Criterion 5 acceptance boundary.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Upgrade Core Challenge Safeguards, Reopen, Representative Metadata, and Assurance Contract

* Intent: Establish canonical non-retaliation, non-refusal, non-closure, and statutory/emergency clock invariants plus `reopen`, representative metadata, and `non_retaliation_assurance` / `hazard_clock_preserved` in `challenges.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Expand adverse-effect invariants and build canonical `non_retaliation_assurance` helper

* Requirement and evidence: FR-2, FR-3, FR-4; research `C1`, `C3`, `C4`, `C10`, `C12` in `.copilot-tracking/research/2026-11-15/220-no-retaliation-research.md`
* Expected result: `challenges.py` defines `build_non_retaliation_assurance(...)`, expands `FORBIDDEN_ADVERSE_FIELDS` (`no_access`, `non_access`, `withdrawn_flag`, `negative_engagement`, `engagement_penalty`, `safeguarding_delay`, `safeguarding_clock_paused`, `awaabs_clock_delayed`), and strengthens `assert_no_adverse_challenge_effects` to guard priority/ranking, refusal/no-access/sanction/withdrawn/negative-engagement inferences across case/`resident`/`decision`/`measure_decisions`, unrelated closures across `tasks`/`returns`/`service_requests`/`work_orders`/`packages`/`handoff`/`resident_update`, and `awaiting_hazard_action` + Awaab's Law 24h/7d/14d + `safeguarding` clocks (with `allow_new_independent_hazard` verifying `hazards[:N] == before_hazards` and active intake on new hazards).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `ChallengeRegister.reopen`, representative submission, and assurance fields on records and views

* Requirement and evidence: FR-1, FR-3, FR-4; research `C1`, `C5`, `C12`
* Expected result: `ChallengeRegister` supports `reopen(...)` (preserving prior resolution history and keeping `"corrected"` staleness active until separate human re-review), accepts `submitted_by` and `representative_ref` on `submit`, `update`, and `reopen`, records `independent_intake: True` and `waits_for_challenge_review: False` on `hazard_referral` without resetting `received_on`, and attaches `non_retaliation_assurance` + `hazard_clock_preserved: True` to every record and `.view()`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Enforce Store-Backed Case Challenge, Reopen, Representative, AI-Task/Form, and Immediate Hazard Routing

* Intent: Extend `ResidentDecisionMixin` (`Store` and `SqlStore`) with `challenge_reopen`, representative/nominee channels, `ai_task` and `form_review` targets, immediate independent hazard referral/intake, runtime safeguard enforcement, and audit/view assurance contracts.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `challenge_reopen`, representative/nominee fields, and expanded non-digital channels

* Requirement and evidence: FR-1; research `C2`, `C5`, `C11`, `C15`
* Expected result: `CHALLENGE_CHANNELS` includes `"Assisted visit"` and `"Trusted intermediary"`; `_res_challenge_reopen` is registered in `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`; `challenge_open`, `challenge_update`, and `challenge_reopen` accept optional `submitted_by`, `representative_ref`, `hazard_concern`, and `hazard_intake` while rejecting unknown keys (`ValueError`), preserving prior resolutions on reopen, and retaining `"Correction recorded"` staleness until human re-review.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Wire immediate independent hazard intake, runtime invariant guards, and audit/view assurance contract

* Requirement and evidence: FR-2, FR-3, FR-4; research `C4`, `C9`, `C10`, `C11`, `C12`, `C14`
* Expected result: `hazard_concern=True` immediately records `hazard_referral` on the challenge record and, when `hazard_intake` is provided, atomically appends an active independent case hazard (`c["hazards"]`) with `safety_raised` / `safety_emergency` audit persistence; runtime `assert_no_adverse_challenge_effects` and `_ranking()` invariance wrap `_res_challenge_*`, `_res_nomination_*` (keeping `nomination_record(hazard_concern=True)` fail-closed per `C14`), and `_res_service_*`; challenge records, `followup_view`, and audit details expose `non_retaliation_assurance` and `hazard_clock_preserved: True` while preserving `after.pop("affected_challenges"); after == before` on standard challenges.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Extend `challenge_catalog` and staleness tracking to `ai_task` and `form_review` suggestions

* Requirement and evidence: FR-1, FR-2; research `C6`, `C11`
* Expected result: `challenge_catalog`, `_priority_record`, `_dependency`, and `priority_challenge_state` index recorded `ai_task` recommendations (`kind == "ai_task"` for `case_id in rec.get("case_ids", [])`) and `form_review` extraction suggestions (`form:<id>`) alongside priority suggestions without mutating `store.data["recommendations"]`.
* Detail section: P02-T03 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add Assistant Proposal Challenge Route, HTTP API Endpoint, and Plain-Language Workbench Support

* Intent: Extend non-retaliatory challenge/correction/reopen/hazard-routing and assurance contracts to SQLite `Assistants`, HTTP `/api/assistants/proposals/<tid>/challenge`, and `web/panels.js` without touching `web/role-screens.js`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Implement `Assistants.challenge` and assurance projection in `assistants.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4; research `C7`, `C9`
* Expected result: `Assistants.challenge(user, tid, body)` supports `open`, `update`, `reopen`, `escalate`, and `resolve` across resident digital, staff non-digital, and representative/nominee channels on SQLite `assistant_tasks`, routes immediate `hazard_referral` and optional `hazard_intake` on the linked case without waiting for challenge review, marks corrected assistant proposals stale (`stale=True`, `actionable=False`) until fresh verification/work, enforces `assert_no_adverse_challenge_effects` on the linked case, and projects `challenges`, `non_retaliation_assurance`, and `hazard_clock_preserved: True` in `Assistants._view`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Expose `/api/assistants/proposals/<tid>/challenge` in `server.py` and update `web/panels.js`

* Requirement and evidence: FR-1, FR-4, NFR-1, NFR-2; research `C8`, `C13`, `C16`, `C17`
* Expected result: `server.py` dispatches `POST /api/assistants/proposals/<tid>/challenge` with bounded JSON validation, error mapping, and `non_retaliation_assurance` / `hazard_clock_preserved` output; `web/panels.js` (`renderChallengePanel`, after loading `web-design-guidelines`) adds `"Assisted visit"` / `"Trusted intermediary"` channels, `submitted_by` (default `"The resident"`) + optional `representative_ref`, `hazard_concern` selector (default `"No"`), `#challenge-reopen-<id>` for resolved challenges, and plain-language non-retaliation & safety-clock-preserved status while keeping `challenge_browser_check.py` and `test_content_standard.py` green and leaving `web/role-screens.js` untouched.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Deliver Core & API Test Suites, Update Module READMEs, and Pass Focused Tier Validation

* Intent: Prove every Criterion 5 invariant end-to-end in the two required test modules, update directly related documentation, and verify clean Focused Tier checks.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Create `src/core/tests/test_challenge_no_retaliation_220.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2; caller prompt Objective 3
* Expected result: Comprehensive `mypy --strict`-clean unit and SQL integration suite testing `ChallengeRegister`, JSON `Store`, SQLite `SqlStore`, `ai_task` & `form_review` challenges, `Assistants.challenge`, representative/nominee submissions, open/update/reopen/escalate/resolve flows, Awaab's Law 24h/7d/14d + safeguarding + `awaiting_hazard_action` clock preservation, immediate independent hazard intake routing, `non_retaliation_assurance` / `hazard_clock_preserved` records & audit entries, and adverse-mutation tamper detection (`ChallengeSafeguardError`).
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Create `src/api/tests/test_challenge_no_retaliation_api_220.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2; caller prompt Objective 3 & 4
* Expected result: Comprehensive `mypy --strict`-clean HTTP integration suite testing `/api/cases/<cid>/resident`, `/api/cases/<cid>/followup`, `/api/assistants/proposals/<tid>/challenge`, `/api/cases/<cid>/hazard-raise`, digital/non-digital/representative/assistant challenge lifecycles (including reopen and immediate hazard intake), `non_retaliation_assurance` / `hazard_clock_preserved` responses & audit verification, and workbench static-asset/content-standard checks.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

<!-- rpi:task id=P04-T03 -->
#### [x] P04-T03: Update `src/core/README.md` and `src/api/README.md` and execute Focused Tier validation

* Requirement and evidence: NFR-1, NFR-2; AMA Repository Instructions Focused Tier rules
* Expected result: `src/core/README.md` and `src/api/README.md` document challenge reopen, representative/assistant coverage, immediate hazard intake, and the `non_retaliation_assurance` / `hazard_clock_preserved` contract; `ruff check`, `ruff format --check`, `mypy`, and targeted + full `unittest` suites (including `test_content_standard.py`) exit `0` across `src/core` and `src/api` with `web/role-screens.js` untouched.
* Detail section: P04-T03 in .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md

## Dependencies

* `P01` (`challenges.py` canonical safeguard and assurance helpers) precedes `P02` (`resident_decisions.py`) and `P03` (`assistants.py`, `server.py`, `web/panels.js`).
* `P02` and `P03` precede `P04` end-to-end test execution and Focused Tier validation.
* AMA Web Development Guidance requires loading `web-design-guidelines` prior to editing `src/api/src/zava_forward/api/web/panels.js` in `P03-T02`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `2026-11-15` `PC-001` [High]: Prevent duplicate `hazard.persist_event` side effects during `SqlStore` replay validation | Resolved (direct planner correction) | Updated `P02-T02` so `_route_challenge_hazard` skips `hazard.persist_event` when `resident_validation.validating` is `True` during detached SQLite validation replay. |
| `2026-11-15` `PC-002` [High]: Align `sqlstore.py` and `mssqlstore.py` `priority_correction` indexing when reopening a corrected challenge | Resolved (direct planner correction) | Added `sqlstore.py` and `mssqlstore.py` to `P02` (`P02-T01`/`P02-T02`) so `priority_correction` and `_priority_correction_rows()` match `prior_correction_preserved = true` alongside `resolution.outcome = 'Correction recorded'`. |
| `2026-11-15` `PC-003` [Medium]: Enforce `"Correction recorded"` staleness fence in `ai_tasks.review` | Resolved (direct planner correction) | Added `ai_tasks.py` to `P02-T03` so `ai_tasks.review` rejects `accept`/`edit` (still allowing `reject`) when `priority_challenge_state(store, rec)["stale"]` is `True`. |
| `2026-11-15` `PC-004` [Medium]: Strip transient `_view` assurance keys on `assistant_tasks` writes and scrub challenge notes under `_withhold_sensors` | Resolved (direct planner correction) | Updated `P03-T01` so `Assistants.review` and `Assistants.challenge` strip transient `_view` keys before SQLite persistence and `_withhold_sensors` redacts free-text challenge notes while preserving assurance/status fields. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md
* Ready phase or task: Complete (ready for rpi-review)
* Remaining provisional question or blocker: None

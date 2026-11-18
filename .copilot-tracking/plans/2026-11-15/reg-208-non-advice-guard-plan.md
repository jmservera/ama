<!-- markdownlint-disable-file -->
# RPI Plan: Regulatory Non-Advice, Duty-Satisfaction, and Future-Law Output Guard (#208)

## Task Metadata

* Task ID: issue-208-non-advice-guard
* Task slug: reg-208-non-advice-guard
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/reg-208-non-advice-guard-plan-critique.md

## Executive Summary

This plan delivers the Issue `#208` regulatory non-advice and future-law output-validation guard across `src/core/`, `src/agents/`, and `src/api/`. While existing Zava Forward regulatory paths restrict user questions (`refuse_question` in `regulatory_eval_gates.py`) and generic operational words (`FORBIDDEN` in `ai.py`), rendered regulatory watch summaries, assistant responses, and legal/compliance views do not yet share an explicit, deterministic output-validation guard with structured telemetry.

We will introduce `zava_forward.core.regulatory_output_guard` as a zero-model deterministic validator with Unicode/confusable normalization, clause-scoped negation handling, contextual status/effective-date/human-activation rules (`consultation`, `future_phase`, future `effective` dates, unactivated rule cards), deterministic advisory review-item rewriting, and process-safe telemetry counters. We will extend `LawStore` and `RuleEngine` to recognize `"future_phase"`, add a guarded `SourceMonitor.watch_summary` exposed at `GET /api/law/watch` alongside workbench/compliance telemetry (`/api/law/*`, `/api/chat/regulatory/status`, `/api/chat/regulatory/threads/{id}/ask`, `/api/me`), enforce the guard across `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `core/chat_panel.py`, `core/assistants.py`, and `api/plain_language.py`, and prove every requirement with unit and loopback HTTP integration tests.

### User Decisions and Requirements Highlights

* Prove Issue `#208` criterion `- [ ] No output states that a duty is satisfied, gives legal advice or applies future law as active` across `src/core/`, `src/agents/`, and `src/api/` with deterministic blocking/rewriting and advisory review-item replacement.
* Expose guard telemetry and check status in the regulatory watch API/workbench payload (`GET /api/law/watch`, `/api/law/*`, `/api/chat/regulatory/*`, `/api/me`).
* Run focused validation (`ruff check`, `mypy`, unit tests in `src/core`, `src/agents`, `src/api`, and `python3 tools/rename-zava-tests.py`) and commit all code, tests, and `.copilot-tracking/` artifacts on `feat/reg-208-non-advice-guard` without pushing to `main`.

### What You May Not Know

* Existing lawful outputs and frozen test suites (`test_regulatory_answers.py`, `evals/regulatory_chat_results.json`, `regulatory_eval_gates.py:grade_chat_turn`, `resident_demo/chat.py`) contain mandatory negative disclaimers (`"not legal advice or approval"`, `"Legal applicability and satisfaction of any duty are not assessed"`, `"I cannot decide that a legal duty is met"`). Clause-scoped negation prevents false positives while still catching disclaimer-stuffing attacks (`"Not legal advice, your statutory duty is satisfied"`).
* `src/api/tests/test_role_endpoint_inventory.py` parses `server.py` for every `"/api/..."` literal; adding `GET /api/law/watch` requires registering `/api/law/watch` in `GET_ENDPOINTS` and enforcing `projection.allowed(user, "law")`.
* `test_dependency_rule.py` enforces strict package layering (`core -> {core}`, `agents -> {agents, core}`, `api -> {api, core, agents}`), requiring the shared deterministic guard to live in `zava_forward.core`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` for Issue `#208` on branch `feat/reg-208-non-advice-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (`cedc723a30bf2e38f23900b6f8343b6dffce8e61`).
* Ensure an explicit, deterministic output-validation guard and API/agent enforcement across regulatory watch summaries, assistant responses, and legal/compliance views in `src/core/`, `src/agents/`, and `src/api/` that blocks or rewrites any claim that: (a) states a legal or statutory duty is satisfied, (b) gives legal advice, or (c) applies future/consultative law or uncommenced phases (`consultation`, `future_phase`, or future effective date without human rule activation) as active operational rules.
* Expose guard telemetry/check status in the regulatory watch API/workbench payload and prove with comprehensive unit and API integration tests that: (1) duty-satisfied outputs are rejected/flagged and replaced with advisory review-item language, (2) legal-advice outputs are rejected/flagged, (3) outputs applying future/uncommenced law or consultation material as active operational rules are rejected/flagged, and (4) legitimate cited summaries with source date, retrieval date, provision, and human-activation status pass cleanly.
* Run focused validation (`ruff check` and `mypy` in `src/core`, `src/agents`, `src/api`; unit tests in `src/core`, `src/agents`, `src/api`; `python3 tools/rename-zava-tests.py`) and commit on `feat/reg-208-non-advice-guard` with the Copilot co-author trailer without pushing to `main`.

## Goals

* Guarantee deterministically that no rendered regulatory watch summary, assistant response, or legal/compliance API view states that a legal/statutory duty is satisfied, gives legal advice, or applies unactivated/future/consultative law as an active operational rule.
* Provide transparent, queryable guard telemetry and per-payload check status in the regulatory watch API and workbench status surfaces.
* Preserve 100% compatibility with existing frozen regulatory evaluations, audit metering schemas, role-projection boundaries, and safe negative disclaimers.

## Scope and Non-Goals

### In Scope

* New core guard module `src/core/src/zava_forward/core/regulatory_output_guard.py` with deterministic lexical + contextual validation, clause-scoped disclaimer handling, Unicode/homoglyph normalization, advisory review-item rewriting, and thread-safe telemetry counters.
* Support for `"future_phase"` source status in `lawstore.py`, `source_monitor.py`, and `rule_engine.py`, plus `SourceMonitor.watch_summary` generating cited watch summaries with provision IDs, source/effective dates, retrieval dates, and human rule-activation status.
* Agent and core assistant enforcement in `src/agents/src/zava_forward/agents/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/assistants.py`, and `src/api/src/zava_forward/api/plain_language.py`.
* HTTP API enforcement and telemetry exposure in `src/api/src/zava_forward/api/server.py` (`GET /api/law/watch`, `/api/law/sources*`, `/api/law/provisions/*`, `/api/law/search`, `/api/law/cards*`, `/api/law/alerts`, `/api/chat/regulatory/status`, `/api/chat/regulatory/threads/{id}/ask`, `/api/me`).
* Unit and HTTP API integration test suites across `src/core/tests/`, `src/agents/tests/`, and `src/api/tests/` (plus `GET_ENDPOINTS` registration in `src/api/tests/test_role_endpoint_inventory.py`).

### Non-Goals

* Live internet scraping of external government websites or mutating immutable snapshots under `docs/reference/regulatory/`.
* Changing `src/api/src/zava_forward/api/web/*.js` front-end screens, Azure Bicep templates, or deployment pipelines.
* Pushing directly to `main` or opening/merging a pull request unless separately requested.

## Functional Requirements

* Deterministic three-category claim detection (`duty_satisfied`, `legal_advice`, `future_law_applied_as_active`) with Unicode NFKC, invisible-format (`Cf`) stripping, and Cyrillic/Greek homoglyph folding.
  * Observable acceptance criteria: Prohibited claims (including homoglyph and disclaimer-stuffed variants) return `passed=False` with matching category codes in `violations`, while safe negated disclaimers (`"not legal advice"`, `"satisfaction of any duty are not assessed"`, `"cannot decide that a legal duty is met"`) return `passed=True` and `violations=[]`.
* Contextual future-law and human-activation enforcement across regulatory sources, watch items, and rule cards.
  * Observable acceptance criteria: Any output or watch/compliance summary backed by `status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated is False` that claims active operational status or sets `active_operational_rule=True` is flagged (`future_law_applied_as_active`), forced to `active_operational_rule=False`, and rewritten to advisory review-item language.
* Advisory review-item replacement and assistant blocking/rewriting across regulatory watch, regulatory chat, employee case chat, and programme assistants.
  * Observable acceptance criteria: Unsafe regulatory watch summaries and regulatory chat responses are flagged and replaced with deterministic advisory review-item language naming human compliance review; unsafe `ChatPanel` replies become `"withheld"` and unsafe `Assistants` outputs raise validation failure / withhold visibility.
* Regulatory watch API and workbench telemetry exposure.
  * Observable acceptance criteria: `GET /api/law/watch` returns guarded watch summaries (citing provision IDs, source/effective date, retrieval date, and human rule-activation state) plus `output_guard` check status and cumulative telemetry (`checked_total`, `passed_total`, `flagged_total`, `rewritten_total`, `rejected_total`, `by_category`), and `/api/chat/regulatory/status` and `/api/me` expose the non-advice guard status/telemetry to the workbench.

## Non-Functional Requirements

* Zero model calls and deterministic O(n) execution in the output guard.
  * Objective threshold or evaluation condition: `model_calls == 0` for all guard checks and bounded input inspection without backtracking regex blowup.
  * Operating condition or verification approach, if needed: Verified in unit tests and `RegulatoryApi` with `store.ai.evidence` patched to fail on any outbound model call.
  * Observable acceptance criteria: All unit and HTTP integration tests pass offline with zero provider calls.
* Architectural layering, static typing, lint cleanliness, and role-based access isolation.
  * Objective threshold or evaluation condition: Zero errors in `ruff check`, `mypy`, `test_dependency_rule.py`, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py`.
  * Operating condition or verification approach, if needed: Run per-package `ruff`, `mypy`, `unittest discover`, and `rename-zava-tests.py`.
  * Observable acceptance criteria: Contractor and unprovisioned roles receive `403` on `/api/law/watch`; frozen eval `src/agents/evals/regulatory_chat_results.json` and `test_regulatory_gates.py` pass unchanged.

## Acceptance Criteria

* `src/core/src/zava_forward/core/regulatory_output_guard.py` deterministically inspects and blocks/rewrites `duty_satisfied`, `legal_advice`, and `future_law_applied_as_active` claims while passing legitimate cited summaries and mandatory disclaimers cleanly.
* `LawStore`, `SourceMonitor`, and `RuleEngine` support `"future_phase"` alongside `"consultation"` and future `effective` dates, and `SourceMonitor.watch_summary` emits cited summaries with source date, retrieval date, provision IDs, human-activation status, and `output_guard` status.
* `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `core/chat_panel.py`, `core/assistants.py`, `api/plain_language.py`, and `api/server.py` enforce the guard across regulatory watch summaries, assistant responses, and legal/compliance views, exposing guard status/telemetry in `/api/law/watch`, `/api/law/*`, `/api/chat/regulatory/*`, and `/api/me`.
* Unit and HTTP API integration tests prove: (1) duty-satisfied outputs are rejected/flagged and replaced with advisory review-item language, (2) legal-advice outputs are rejected/flagged, (3) future/uncommenced law or consultation material applied as active operational rules is rejected/flagged, and (4) legitimate cited summaries with source date, retrieval date, provision, and human-activation status pass cleanly.
* Test ownership and budget lock: exact test removals = `none`; maximum new test files = `3` (`src/core/tests/test_regulatory_output_guard.py`, `src/agents/tests/test_regulatory_non_advice_guard.py`, `src/api/tests/test_regulatory_watch_guard_api.py`) plus 1 route entry in `src/api/tests/test_role_endpoint_inventory.py`; canonical source targets only (zero generated files mutated, `src/agents/evals/regulatory_chat_results.json` preserved verbatim); semantic behavior tests cover all 4 Issue `#208` scenarios + adversarial bypasses while existing suites provide regression coverage.
* Focused validation (`ruff check`, `mypy`, and `unittest` across `src/core`, `src/agents`, `src/api`, plus `python3 tools/rename-zava-tests.py`) passes 100%, and all artifacts/code/tests are committed on `feat/reg-208-non-advice-guard` with the required Copilot trailer.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/reg-208-non-advice-guard-plan-critique.md with Revise disposition (PC-001..PC-004 resolved in batch) |
| Relevant research                | .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md is created by implementation as its evidence record        |
| Planning execution and readiness | Complete and Ready for Implement                                                                                                   |
| Continuation context             | Confirmed automatic RPI Agent parent return                                                                                        |

## Sources

* .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md: Codebase evidence `C1`-`C20` mapping regulatory store, watch, chat, assistant, API, and test constraints.
* docs/adrs/0005-regulatory-compliance-assistant.md: Non-advice, non-compliance-verdict, and human-owned rule-activation architectural contract.
* docs/reference/regulatory/README.md: Authority hierarchy, snapshot immutability, and citation requirements (source date, retrieval date, provision, human activation).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Deterministic Regulatory Output Guard and Future-Law Support

* Intent: Create the canonical `regulatory_output_guard` module in `src/core`, extend `LawStore` and `RuleEngine` for `"future_phase"`, and add guarded `SourceMonitor.watch_summary` with core unit tests.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `zava_forward.core.regulatory_output_guard` and telemetry registry

* Requirement and evidence: Issue `#208` deterministic non-advice / duty-satisfaction / future-law guard (`C1`, `C8`, `C9`, `C15`, `C20`, `PC-001`, `PC-003`, `PC-004`).
* Expected result: `src/core/src/zava_forward/core/regulatory_output_guard.py` inspects rendered strings and structured regulatory items (`on_violation="rewrite" | "reject"`), normalizes Unicode/confusables, applies clause-scoped disclaimer exemptions across both lexical and contextual active-rule prose while keeping `active_operational_rule=True`/`active_control=True` unconditionally forbidden under unactivated metadata, emits compact envelope dicts (`to_status_dict()` omitting `rewritten_text` to respect `MAX_CONTENT`), rewrites unsafe outputs to advisory review-item language, and tracks thread-safe telemetry (`checked_total`, `passed_total`, `flagged_total`, `rewritten_total`, `rejected_total`, `by_category`).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend `LawStore`, `RuleEngine`, and `SourceMonitor.watch_summary` with guard enforcement

* Requirement and evidence: Support `"future_phase"` and guarded regulatory watch summaries with source date, retrieval date, provision IDs, and human-activation status (`C2`, `C3`, `C4`, `C5`).
* Expected result: `lawstore.STATUSES` and `LawStore._caveats` support `"future_phase"`; `rule_engine.citation_eligibility` treats `"future_phase"` as `"not applicable"`; `SourceMonitor.watch_summary` builds cited watch items for held sources and detected changes, runs every summary through `regulatory_output_guard`, demotes any unactivated/future/consultation active claim, and returns per-item + aggregate `output_guard` telemetry.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Add comprehensive `src/core` unit tests for `regulatory_output_guard` and `watch_summary`

* Requirement and evidence: Prove all 4 Issue `#208` guard scenarios plus disclaimer false-positive and confusable/disclaimer-stuffing resistance (`C2`, `C3`, `C9`, `C18`, `C20`).
* Expected result: `src/core/tests/test_regulatory_output_guard.py` covers duty-satisfaction rewrites, legal-advice rejection/rewriting, lexical + metadata-driven `consultation` / `future_phase` / future `effective` / unactivated rule blocking, Unicode confusables, and clean cited summaries with source date, retrieval date, provision, and human-activation status.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Agents and Core Assistant Output Guard Enforcement

* Intent: Wire deterministic output-guard enforcement across `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `core/chat_panel.py`, and `core/assistants.py` without breaking frozen evaluations or extractive citation contracts, and prove with agent unit tests.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Enforce output guard in `agents/regulatory_chat.py` and `core/regulatory_chat.py`

* Requirement and evidence: Assistant regulatory responses must never claim duty satisfaction, give legal advice, or apply future/consultative law as active (`C6`, `C11`, `C17`, `C18`, `C19`, `PC-001`, `PC-002`).
* Expected result: `agents/regulatory_chat.py:answer` preserves `refusal`/`conflict`/empty-source `unknown` branches first, gates candidate `kind="answer"` turns on both active commenced source status AND non-empty active/approved `bundle["cards"]`, validates non-quote prose across `reply` and `sections`, and attaches compact `output_guard`; `core/regulatory_chat.py:RegulatoryChat.ask` acts as the single telemetry-recording gate for chat turns (preserving upstream `output_guard.passed=False` without double-counting, sanitizing both `reply`/`answer` and non-quote `sections` prose, and preserving `SECTION_KEYS`, `cards`, `usage`, and `MAX_CONTENT`).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce output guard in `core/chat_panel.py` and `core/assistants.py`

* Requirement and evidence: General employee case chat and the five programme assistants must also reject/withhold model outputs containing prohibited legal-advice, duty-satisfied, or future-law-as-active claims and record `rejected_total` telemetry (`C8`, `C9`, `C10`, `PC-004`).
* Expected result: `ChatPanel._ask` and `assistants.validate_output` / `_output_violates_visibility` inspect candidate prose with `on_violation="reject"` (recording `rejected_total` into optional `guard_telemetry`), withholding unsafe `ChatPanel` replies as `"withheld"` and rejecting unsafe `Assistants` proposal texts.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Add `src/agents` unit tests proving agent-layer guard enforcement and frozen-eval stability

* Requirement and evidence: Prove agent regulatory composer blocks/rewrites prohibited claims and passes legitimate cited summaries + frozen evals (`C11`, `C17`, `C18`).
* Expected result: `src/agents/tests/test_regulatory_non_advice_guard.py` proves duty-satisfied, legal-advice, and unactivated `consultation`/`future_phase`/future-effective bundles are flagged and replaced with advisory review-item language, while legitimate cited summaries and `test_regulatory_answers.py` + `test_regulatory_gates.py` pass cleanly.
* Detail section: P02-T03 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: API Regulatory Watch, Legal/Compliance View Enforcement, Workbench Telemetry, and Validation

* Intent: Expose `GET /api/law/watch` and guard/telemetry fields across legal/compliance endpoints, regulatory chat HTTP routes, and `/api/me`, prove end-to-end via HTTP integration tests, run focused validation, and commit on `feat/reg-208-non-advice-guard`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `GET /api/law/watch`, guard legal/compliance and `plain_language` responses, and expose workbench telemetry in `server.py`

* Requirement and evidence: Expose guard telemetry/check status in the regulatory watch API/workbench payload and enforce across all legal/compliance views/exports and assistant HTTP endpoints (`C12`, `C13`, `C14`, `C16`, `PC-001`, `PC-003`, `PC-004`).
* Expected result: `server.py` wires `app.guard_telemetry` into `RegulatoryChat`, `ChatPanel`, `Assistants`, and `SourceMonitor`, serves `GET /api/law/watch` (role-gated by `projection.allowed(user, "law")`), enforces `regulatory_output_guard` inside shared serializers covering `/api/law/sources`, `/api/law/sources.csv`, `/api/law/sources/{id}`, `/api/law/provisions/{id}`, `/api/law/search`, `_rulecards` (`/api/law/cards*`, passing each card's true active state), `_rule_alerts` (`/api/law/alerts*` and `/api/law/checks/*`), and `/api/chat/regulatory/threads/{id}/ask` (guarding `plain_summary` and merging without clobbering `RegulatoryChat.ask`'s `output_guard`), and exposes `output_guard` telemetry in `/api/law/watch`, `/api/chat/regulatory/status`, `/api/chat/status`, and top-level `regulatory_output_guard` on `/api/me` (preserving `me["services"]` exact-key contract).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Register `/api/law/watch` in `test_role_endpoint_inventory.py` and add `test_regulatory_watch_guard_api.py`

* Requirement and evidence: Prove all 4 Issue `#208` scenarios and telemetry over HTTP and keep full role-matrix route coverage green (`C12`, `C13`, `C16`).
* Expected result: `src/api/tests/test_role_endpoint_inventory.py` includes `/api/law/watch` in `GET_ENDPOINTS`; `src/api/tests/test_regulatory_watch_guard_api.py` proves over loopback HTTP that duty-satisfied claims are flagged and rewritten to advisory review-item language, legal-advice claims are flagged/rejected, `consultation` / `future_phase` / future-effective unactivated claims are flagged/rejected, legitimate cited summaries pass cleanly, and telemetry increments accurately in `/api/law/watch`, `/api/chat/regulatory/status`, and `/api/me`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Run focused validation suite across `src/core`, `src/agents`, `src/api`, and `rename-zava-tests.py`

* Requirement and evidence: Focused validation tier (`ruff check`, `mypy`, unit tests in `src/core`, `src/agents`, `src/api`, and `python3 tools/rename-zava-tests.py`).
* Expected result: All linters, strict/configured `mypy` checks, existing + new unit/integration tests across all three packages, and migration regression tests pass with zero failures; changes are recorded in `.copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md`.
* Detail section: P03-T03 in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md

## Dependencies

* `zava-forward-core`, `zava-forward-agents`, and `zava-forward-api` editable/local Python packages (`src/core`, `src/agents`, `src/api`): `core` must implement `regulatory_output_guard` before `agents` and `api` wire imports (`test_dependency_rule.py`).
* `src/api/tests/test_role_endpoint_inventory.py`: must list `/api/law/watch` alongside adding the route in `server.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]: Post-rewrite re-validation clobbering, telemetry double-counting, unsanitized `sections`, and `MAX_CONTENT` risk | resolved | `GuardDecision.to_status_dict()` omits `rewritten_text`; `RegulatoryChat.ask` is the single chat-turn telemetry gate preserving upstream `passed=False` and sanitizing non-quote `sections` strings; `server.py` guards `plain_summary` and merges into `output_guard` without re-checking `reply`. |
| Run 1 `PC-002` [High]: Contradictory `in_force`/`guidance` card-activation predicate vs frozen `refusal`/`conflict`/`unknown` eval branches | resolved | `P02-T01` preserves `refusal`/`conflict`/empty-source `unknown` branches first (lexically validated) and gates candidate `kind="answer"` turns on BOTH active commenced source status AND non-empty active/approved `bundle["cards"]`. |
| Run 1 `PC-003` [Medium]: Clause-negation vs boolean-flag precedence on negated caveats and inactive draft cards | resolved | Under unactivated metadata, boolean `active_operational_rule=True`/`active_control=True` fails unconditionally while contextual active-rule text patterns use clause-scoped negation, and `_rulecards` passes each card's actual activation flag. |
| Run 1 `PC-004` [Medium]: `/api/law/sources.csv`, `_rule_alerts` subroutes, and `rejected_total` telemetry wiring in `ChatPanel`/`Assistants` | resolved | Shared source serializer guards `/api/law/sources` and `/api/law/sources.csv`; `_rule_alerts` and `_rulecards` guard all alert/card routes; `ChatPanel` and `Assistants` use `on_violation="reject"` wired to `app.guard_telemetry`. |

## Follow-Up Items

* Optional interactive regulatory watch UI tab in `src/api/src/zava_forward/api/web/law.js`: outside `#208`'s deterministic guard and JSON API/workbench payload scope; owned by a future UX issue if visual diff browsing is requested.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md
* Ready phase or task: Review (all phases `P01`, `P02`, `P03` complete)
* Remaining provisional question or blocker: none

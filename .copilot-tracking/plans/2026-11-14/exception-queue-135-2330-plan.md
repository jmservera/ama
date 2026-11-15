<!-- markdownlint-disable-file -->
# RPI Plan: Issue #135 Data Steward and Digital Operator Exception Queue

## Task Metadata

* Task ID: issue-135-2330
* Task slug: exception-queue-135-2330
* Planning status: Ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/exception-queue-135-2330-plan-critique.md

## Executive Summary

This plan completes end-to-end enforcement across core, API, and employee workbench UI for **Issue #135** (*Data steward and digital operator exception queue*). Existing commits on the parent stack already provide `ExceptionQueue`, read-only exception feeds, `ExceptionRegisterMixin` (`GET /api/exceptions` and `POST /api/exceptions/recovery`), and the `#229` read-only specialist register screen. This plan closes the remaining contract, routing, audit-trail, outage-honesty, correlation-context, and interactive operator-recovery gaps without breaking existing read-only screen or plain-language guards.

Specifically, the implementation enriches conflict items with an explicit top-level `resolution_owner`, adds `failure_category`, `correlation_id`, and structured `recovery_context` to exception items, connects rejected importer batches from `import_batches` alongside refused import files, preserves full per-item recovery `audit_trail` records (actor, reason, timestamp, and no-replay/no-release guarantees), reflects active AI continuity suspensions and recorded service outages honestly in `outage_banner` with plain-language `next_steps`, and delivers an accessible `#/exceptions` workbench route in `src/api/src/zava_forward/api/web/app.js` for scoped viewing and controlled human recovery requests.

### User Decisions and Requirements Highlights

* **All five Issue #135 acceptance criteria enforced end-to-end**: Conflicting source values, owned failure routing, controlled audited recovery without replay or release, preserved `Unknown` eligibility and `original_source`, and scoped operator access with honest outage next steps are verified across `src/core`, `src/api`, and `web/app.js`.
* **Frozen workbench browser check preserved**: `src/api/checks/workbench_browser_check.py` and `src/api/src/zava_forward/api/workbench.py` (`me.navigation`) remain unchanged so `scenario-manifest.json` recipe SHA is not disturbed.
* **Focused validation and local-only commit**: Validation runs `mypy`, `ruff check .`, `ruff format --check .`, and focused unit tests in `src/core` and `src/api`, followed by a clean local commit referencing `Refs #135` with the Copilot trailer and no remote push.

### What You May Not Know

* **Read-only specialist screen lock (`#229`)**: Four existing tests (`test_role_screens.py`, `test_data_operator_screen.py`, `test_exception_register_screen.py`, and `data_operator_browser_check.py`) forbid any write control or `POST` call in `src/api/src/zava_forward/api/web/role-screens.js`. Interactive recovery controls must therefore live on a dedicated workbench route (`#/exceptions`) in `src/api/src/zava_forward/api/web/app.js` rather than mutating `role-screens.js`.
* **Lexical copy guard (`test_content_standard.py`)**: Every line of every served `.js` and `.html` file in `src/api/src/zava_forward/api/web/` is scanned for banned internal stems (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), with `"Keep on hold"` explicitly whitelisted. All new UI code and comments in `web/app.js` and `web/index.html` must avoid bare banned stems.
* **Read-only register view invariants (`test_exception_register.py`)**: `GET /api/exceptions` must never mutate `self.data`, must keep `access.roles` limited to the signed-in caller, and must keep `banner.state == "unknown"` when no active outage or AI suspension is recorded.

### Unresolved Decisions or Blockers

* None blocking implementation. Naming real organisational post-holders to `data_steward` and `digital_operator` remains an owner configuration via `ZF_EXCEPTION_STAFF`; when unset, the system deterministically reports `roles_not_named` without silent fallback assignment.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) with dated artifacts under `.copilot-tracking/` for Issue #135 on branch `feat/ux-135-exception-queue-2330` stacked on `origin/feat/demo-233-same-home-tensions-0825` (user prompt).
* Conflicting source values must retain and display both values with `source`, `date` (`recorded_at`/`as_of`), and `version`, plus a named `resolution_owner` (Issue #135 criterion 1; user prompt).
* Failed imports, failed model calls, and stranded tasks must surface in an owned exception queue with explicit owner, failure category, correlation IDs, and recovery context (Issue #135 criterion 2; user prompt).
* Recovery actions must require an explicit controlled, audited operator action recording actor, reason, timestamp, and audit trail, and must never perform automatic replay or automatic external/resident release (Issue #135 criterion 3; user prompt).
* Unresolved eligibility (`Unknown` / `Unverified`) and original source records must remain preserved without silent overwrite during exception handling or recovery (Issue #135 criterion 4; user prompt).
* Operator access scope must be explicitly surfaced in the exception queue view and API, and service/model outage states must be shown honestly to staff with plain-language next steps (Issue #135 criterion 5; user prompt).
* Activate required web skills (`redesign-existing-projects` and `web-design-guidelines`, fetching the current guidelines source) before editing `src/api/src/zava_forward/api/web/` files, and preserve Fluent 2 tokens, WCAG 2.2 AA semantics, and the plain-language content standard (`.github/copilot-instructions.md`).
* Do not modify `src/api/checks/workbench_browser_check.py` unless also updating `scenario-manifest.json` recipe SHA (user prompt).
* Validate under the Focused tier (`python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and focused unit tests in modified project directories `src/core` and `src/api`), then commit cleanly with `Refs #135` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (user prompt).

## Goals

* Deliver a complete, deterministic exception-queue contract across `src/core` and `src/api` covering conflicting source values, owned failure categories, correlation IDs, recovery context, full per-item recovery audit trails, scoped access visibility, and honest outage/suspension banners with plain-language next steps.
* Provide an accessible, plain-language interactive workbench exception queue view (`#/exceptions` in `web/app.js` with discoverable entry links) enabling authorised stewards and operators to inspect exceptions and submit controlled, audited recovery requests without touching read-only `role-screens.js`.
* Prove all five Issue #135 acceptance criteria end-to-end across core, HTTP API (both SQLite and JSON stores), and shipped JavaScript UI while keeping all existing regression, WCAG, design-system, and lexical content guards green.

## Scope and Non-Goals

### In Scope

* Additive contract enhancements in `src/core/src/zava_forward/core/exception_queue.py`, `src/core/src/zava_forward/core/exception_feeds.py`, and `src/core/src/zava_forward/core/exception_register.py`.
* Interactive `#/exceptions` workbench view, in-flight `mutationKey` support for `body.key`, and plain-language entry links in `src/api/src/zava_forward/api/web/app.js` (and `src/api/src/zava_forward/api/web/index.html` / `style.css` only if required by Fluent 2 layout tokens).
* Focused unit, API, and Node-VM UI tests in `src/core/tests/` and `src/api/tests/` covering all five Issue #135 acceptance criteria plus regression guards.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js` to add write controls, modifying `src/core/src/zava_forward/core/sqlstore.py` (preserving Focused validation tier), or modifying `src/api/checks/workbench_browser_check.py` / `src/api/src/zava_forward/api/workbench.py` top-level `me.navigation`.
* Implementing automatic task replay, automatic source reconciliation, silent latest-wins conflict resolution, or automatic resident/external release.
* Pushing commits to a remote or opening/updating a GitHub pull request.

## Functional Requirements

* **FR-1 (Conflict Dual-Value & Resolution Owner)**: Every `identity_conflict` and `source_conflict` item in `ExceptionQueue` and `GET /api/exceptions` retains at least two distinct competing values with `value`, `source`, `date`, and `version`, plus a top-level `resolution_owner` matching the named `data_steward` owner, and renders both values and `resolution_owner` in `#/exceptions`.
  * Observable acceptance criteria: Core, API, and UI tests confirm both competing values, `source`, `date`, `version`, and `resolution_owner` are returned and rendered with no winner selected.
* **FR-2 (Owned Failure Routing, Correlation IDs & Recovery Context)**: Failed imports (both refused import files and rejected `import_batches`), failed model calls (`failed_ai_run` from fallback or quarantined AI task records), and stranded tasks (`stranded_task` from unowned overdue tasks and overdue unaccepted handoffs) surface in the owned queue with explicit `owner`, `owner_role`, `failure_category`, deterministic `correlation_id`, and `recovery_context`.
  * Observable acceptance criteria: Core, API, and UI tests verify all three failure categories route to their named owner role (`data_steward` for `failed_import`; `digital_operator` for `failed_ai_run` and `stranded_task`) with `failure_category`, `correlation_id`, and `recovery_context` visible.
* **FR-3 (Controlled, Audited Human Recovery Without Replay or Release)**: Recovery requests (`hold`, `request_rerun`, `resolve_by_owner`) require named-staff role scope, owner match for `resolve_by_owner`, and a non-empty reason (1-400 chars), record `by`, `at`, `action`, `reason`, `replayed: False`, `released: False`, `automatic_replay: False`, `automatic_release: False`, append to the tamper-evident audit ledger, and return an ordered per-item `audit_trail` rendered in `#/exceptions`.
  * Observable acceptance criteria: Submitting recovery via `POST /api/exceptions/recovery` and the `#/exceptions` UI updates item status (`held`, `rerun_requested`, `closed`), appends an audit trail entry with actor/timestamp/action/reason, refuses unauthorised/invalid requests (`403`/`400`), and leaves underlying AI/import/case records unreplayed and unreleased.
* **FR-4 (Preserved Unresolved Eligibility & Original Source)**: Every exception item preserves `eligibility: "Unknown"`, `unresolved_eligibility: True`, and deep-copied `original_source` before and after recovery actions, without mutating underlying store records (`cases`, `stock_reconciliation`, `recommendations`, `import_refusals`, `import_batches`).
  * Observable acceptance criteria: Store JSON/SQLite snapshots before and after `exception_register` and `request_exception_recovery` remain unchanged outside the audit ledger, and UI renders `Unknown` unresolved eligibility and original source references before and after recovery.
* **FR-5 (Scoped Operator Access & Honest Outage Banner With Next Steps)**: `GET /api/exceptions` and `#/exceptions` explicitly display the viewer's scoped roles (`access.roles`, `access.viewer_roles`, `access.allowed_kinds`, `access.scope`) and an honest `banner` (`state`, `text`, `components`, `last_checked`, and plain-language `next_steps`) that stays `unknown` when unverified and transitions to `outage` when an AI continuity suspension or recorded service outage is active.
  * Observable acceptance criteria: Steward and operator viewers see only their scoped items and explicit access scope; active continuity suspension or `service_outages` produces `banner.state == "outage"` with plain-language `next_steps` in API and UI, while absence of health checks without active outage produces `banner.state == "unknown"` with `"Do not assume it is healthy"` and plain-language `next_steps`.

## Non-Functional Requirements

* **NFR-1 (Accessibility, Fluent 2 & Plain-Language Conformance)**: `#/exceptions` in `web/app.js` uses native semantic HTML (`<h1>`–`<h3>`, `<section>`, `<table>` with `<caption>` and `<th scope="col">`, explicit `<label for>`, `role="status"` / `role="alert"`, `aria-invalid` + `aria-describedby`), Fluent 2 CSS tokens, non-colour status prefixes, and zero banned terms under `test_content_standard.py`.
  * Objective threshold or evaluation condition: Zero violations in `test_content_standard.py`, `test_design_system.py`, `test_app_js_notices_content.py`, and web-design-guidelines review.
  * Operating condition or verification approach, if needed: Run unit suites in `src/api/tests/` and inspect changed web lines against fetched Web Interface Guidelines.
  * Observable acceptance criteria: All copy-audit, design-system, and Node-VM UI tests pass with exit code `0`.
* **NFR-2 (Type Safety, Formatting & Store Parity)**: All Python changes pass strict static typing, linting, formatting, and both `SqlStore` and `Store` execution paths without mutating `self.data` on reads.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Execute tools directly in `src/core` and `src/api` project directories.
  * Observable acceptance criteria: Both `src/core` and `src/api` checks exit `0`.
* **NFR-3 (Test Discipline & Frozen Manifest Preservation)**: Lock test ownership to existing core/API test files plus at most one focused Node-VM UI test module for `#/exceptions`, with `none` removed tests and zero edits to `src/api/checks/workbench_browser_check.py` or `scenario-manifest.json`.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `1` (`src/api/tests/test_exception_queue_ui.py`), maximum new test methods across existing/new files <= `18`; `git diff -- src/api/checks/workbench_browser_check.py` is empty.
  * Operating condition or verification approach, if needed: Verify via `git status` / `git diff` and unittest runner output.
  * Observable acceptance criteria: Existing and new focused unit tests pass without touching frozen browser check manifests.

## Acceptance Criteria

* AC-1: Conflict items in `ExceptionQueue`, `GET /api/exceptions`, and `#/exceptions` retain and display both competing values with `source`, `date`, and `version`, plus named `resolution_owner`, selecting no automatic winner.
* AC-2: Failed imports (refused files and rejected `import_batches`), failed AI model calls (`failed_ai_run`), and stranded tasks (`stranded_task`) appear in the owned exception queue with explicit `owner`, `failure_category`, `correlation_id`, and `recovery_context`.
* AC-3: Recovery actions (`hold`, `request_rerun`, `resolve_by_owner`) require authorised scoped operator/steward action with a reason, record actor (`by`), timestamp (`at`), action, reason, and ordered per-item `audit_trail`, and never replay a run or release resident/external output.
* AC-4: `eligibility` (`"Unknown"`), `unresolved_eligibility` (`True`), original source metadata, and underlying store records remain preserved without overwrite across queue viewing and recovery in both `SqlStore` and `Store`.
* AC-5: Operator/steward access scope (`roles`, `viewer_roles`, `allowed_kinds`, `scope`) and honest service/model outage state (`unknown` vs active `outage` from continuity suspensions or recorded outages, with plain-language `next_steps`) are surfaced in `GET /api/exceptions` and `#/exceptions`.
* AC-6: `mypy`, `ruff check .`, `ruff format --check .`, and focused unit/UI/copy-audit tests pass in `src/core` and `src/api`, with `role-screens.js` read-only tests and `workbench_browser_check.py` untouched.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md                                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md                                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/exception-queue-135-2330-plan-critique.md with Revise verdict; PC-001..PC-006 applied |
| Relevant research                | .copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md                                                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation (all six critique findings resolved in plan and phase details)                                     |
| Continuation context             | Confirmed automatic RPI Agent session continues directly to rpi-implement                                                                |

## Sources

* .copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md: Cycle 1 Wider/Deeper/Contrarian gap analysis and `C1`–`C14` codebase evidence.
* docs/case_study_48_original.md and docs/case_study_48_addendum.md: Human-in-the-loop governance, non-silent failure handling, and safety/consent boundaries.
* docs/reference/research/ux/design-system.md, docs/reference/research/ux/wcag-conformance-baseline.md, and docs/reference/research/ux/content-standard.md: Fluent 2 tokens, WCAG 2.2 AA semantics, non-colour status signals, and banned internal vocabulary.
* src/core/src/zava_forward/core/exception_queue.py, src/core/src/zava_forward/core/exception_feeds.py, and src/core/src/zava_forward/core/exception_register.py: Existing core exception queue, feeds, and store-backed exception register/recovery mixin.
* src/api/src/zava_forward/api/server.py, src/api/src/zava_forward/api/web/app.js, and src/api/src/zava_forward/api/web/role-screens.js: Existing `/api/exceptions` and `/api/exceptions/recovery` endpoints, workbench router, and `#229` read-only specialist view.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Exception Queue, Feeds, and Store Register Enrichment

* Intent: Enrich `src/core` exception models, feeds, and store register so all 5 Issue #135 criteria (conflict `resolution_owner`, failure categories, correlation IDs, recovery context, full recovery `audit_trail` with timestamps, rejected `import_batches` routing, scoped `access` summary, and continuity/service outage `banner` with plain-language `next_steps`) are deterministically produced without mutating store records.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Enrich ExceptionQueue and exception_feeds contracts

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, FR-5; research evidence `C1`, `C2`.
* Expected result: `ExceptionQueue` items carry `resolution_owner` (on conflict kinds), `failure_category` (on failure kinds), deterministic `correlation_id`, `recovery_context`, `at` timestamp and ordered `audit_trail` on `request_recovery`, and plain-language `next_steps` on `outage_banner`; `feed_failed_ai_runs` preserves `correlation_id` when present on AI records.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Connect rejected import batches, full recovery audit trail, access scope, and honest outage states in ExceptionRegisterMixin

* Requirement and evidence: FR-2, FR-3, FR-4, FR-5; research evidence `C3`, `C6`, `C12`.
* Expected result: `ExceptionRegisterMixin` routes rejected `import_batches` alongside `import_refusals` (keeping `NOT_CONNECTED` when neither is present), overlays ordered per-item recovery `audit_trail` from `audit_entries()`, adds `viewer_roles` and `allowed_kinds` to `access` while keeping `access.roles` caller-only, and feeds active `continuity` AI suspensions and recorded `service_outages` into `queue` so `banner` reports honest `outage` vs `unknown` state with plain-language `next_steps`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Strengthen src/core unit tests for all five Issue #135 invariants

* Requirement and evidence: AC-1 through AC-5, NFR-2, NFR-3; research evidence `C1`, `C2`.
* Expected result: Focused tests in `src/core/tests/test_exception_queue.py` and `src/core/tests/test_exception_feeds.py` verify `resolution_owner`, `failure_category`, `correlation_id`, `recovery_context`, timestamped `audit_trail`, preserved `Unknown` eligibility and `original_source`, and `outage_banner` `next_steps`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Interactive Employee Workbench Exception Queue UI and API Contract Verification

* Intent: Load required web design skills, implement the accessible `#/exceptions` workbench view and controlled recovery workflow in `src/api/src/zava_forward/api/web/app.js` without modifying read-only `role-screens.js` or `workbench.py`, and verify end-to-end API and UI behavior across SQLite and JSON stores.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Activate web skills and implement accessible #/exceptions view and controlled recovery in web/app.js

* Requirement and evidence: FR-1 through FR-5, NFR-1; research evidence `C4`, `C5`, `C7`, `C8`, `C9`, `C10`, `C11`, `C13`, `C14`.
* Expected result: `redesign-existing-projects` and `web-design-guidelines` (with current guidelines fetched) guide implementation of `#/exceptions` (`exceptionsView`) in `src/api/src/zava_forward/api/web/app.js`, `body.key` deduplication in `mutationKey`, and plain entry links from `handoffWaitingView` and `importView`, rendering outage banner + `next_steps`, scoped operator access, dual-value conflicts with `resolution_owner`, owned failure items with `failure_category`/`correlation_id`/`recovery_context`, preserved `Unknown` eligibility and `original_source`, and controlled `POST /api/exceptions/recovery` forms with `audit_trail` display and zero banned copy terms.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add focused API register and Node-VM UI tests for end-to-end #135 enforcement

* Requirement and evidence: AC-1 through AC-6, NFR-1, NFR-3; research evidence `C9`, `C12`, `C13`.
* Expected result: Extended tests in `src/api/tests/test_exception_register.py` verify rejected `import_batches`, continuity/service `outage` banner + `next_steps`, multi-step recovery `audit_trail`, `resolution_owner`, `correlation_id`, `recovery_context`, and HTTP `/api/exceptions` + `/api/exceptions/recovery` responses; new `src/api/tests/test_exception_queue_ui.py` executes the shipped `#/exceptions` view in `app.js` via Node VM across conflict, failure, outage, denied (`403`), `roles_not_named`, and controlled recovery submission states.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Tier Validation, Web Guidelines Review, and Clean Local Commit

* Intent: Run all Focused-tier static, lint, format, unit, UI, and lexical/design-system checks across `src/core` and `src/api`, audit changed web files against fetched Web Interface Guidelines, reconcile tracking artifacts, and prepare the clean local commit after `rpi-review`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run mypy, ruff, and focused unittest suites in src/core and src/api and record implementation evidence

* Requirement and evidence: AC-6, NFR-1, NFR-2, NFR-3; repository Focused validation tier rules.
* Expected result: `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and targeted unittest suites in `src/core` and `src/api` (including `test_content_standard.py`, `test_design_system.py`, `test_role_screens.py`, `test_data_operator_screen.py`, `test_exception_register_screen.py`, `test_handoff_waiting_view.py`, `test_case_journey.py`, `test_epic149_role_workbench_heading_hierarchy.py`, `test_exception_register.py`, and `test_exception_queue_ui.py`) pass cleanly, recorded in `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md

## Dependencies

* `src/core` editable package installation in current Python environment: `src/api` imports `zava_forward.core.exception_queue`, `exception_feeds`, and `exception_register` directly.
* Node.js (`node`) binary on `PATH`: Used by `src/api/tests/` VM-based JavaScript UI contract tests (`test_exception_register_screen.py`, `test_case_journey.py`, and `test_exception_queue_ui.py`).
* Web skills (`redesign-existing-projects` and `web-design-guidelines`): Must be loaded and Web Interface Guidelines fetched before editing `src/api/src/zava_forward/api/web/app.js`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-14 PC-001 [High] | Applied     | Updated `P01-T02` and `P02-T02` to detect active continuity suspensions via `not continuity.history_valid(doc)` and `s.get("status") == "Suspended" or s.get("actual_hold", True)`, apply detected outages on both `ok` and `roles_not_named` banners, and keep `NO_HEALTH_CHECK` exact when zero outages are active while stating recorded outage count without claiming live health probing when outages exist. |
| 2026-11-14 PC-002 [High] | Applied     | Kept `sqlstore.py` out of scope (preserving Focused validation tier) and updated `P01-T02` and `P02-T02` to accept rejected batches from both `self.data.get("import_batches")` and `self.data.get("import_exceptions", {}).get("rejected_batches")` (persisted in `SqlStore.DOCS`) and persist `continuity` suspensions via `store.suspend(...)` / `store.save()` in `SqlStore` parity tests. |
| 2026-11-14 PC-003 [High] | Applied     | Updated `P02-T01` to keep `me.services?.cases === false` unchanged, match `hash.split("?")[0] === "#/exceptions"`, define plain-ASCII `EXCEPTIONS_DENIED` (with `Owner: the programme owner.`) and `EXCEPTIONS_READ_ERROR` outside the `WAITING_READ_ERROR`..`listView` VM slice, use pure ASCII copy, map both `<select>` and `audit_trail` actions through one `"Keep on hold"` helper with zero bare banned stems, and enforce `<h1>`-first `h1 -> h2 -> h3` order across all states. |
| 2026-11-14 PC-004 [Medium] | Applied   | Added `tests/test_handoff_waiting_view.py`, `tests/test_case_journey.py`, and `tests/test_epic149_role_workbench_heading_hierarchy.py` to `P02` and `P03-T01` validation, plus structural `<h1>`-first and `<table>` `<caption>`/`scope` assertions in `test_exception_queue_ui.py` (`P02-T02`). |
| 2026-11-14 PC-005 [Medium] | Applied   | Updated `P01-T02` so `_with_recoveries` works on `deepcopy(item)` and replaces `audit_trail` idempotently across double-invocation in `request_exception_recovery`, verified by `POST`/`GET` `audit_trail` length parity in `P02-T02`. |
| 2026-11-14 PC-006 [Low]  | Applied     | Updated `P01-T01` so sourceless `stranded_task` items use deterministic `f"task:{case_id}:{task}"` fallback `ref` (preserving `recovery_key` and stable `correlation_id`), `feed_failed_ai_runs` checks `envelope.meter_id`, and `feed_failed_imports` extracts `batch`/`refusal` `correlation_id`. |

## Follow-Up Items

* Connect standalone importer process rejected-batch storage directly to the shared database without manual refusal-ledger transfer once importer storage topology is unified (outside `#135` workbench/register scope; owner: data engineering / programme support).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md
* Ready phase or task: P01-T01 (critique PC-001..PC-006 resolved; ready for rpi-implement)
* Remaining provisional question or blocker: none

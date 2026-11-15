<!-- markdownlint-disable-file -->
# Review: Issue #154 Representative Task-Limited Views and Session Expiry

## Scope and Evidence

* Task ID: issue-154-rep-expiry-views
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue #154 Criterion 3 (`Representative views show only task-limited authority and expire as recorded`) covering `FR-045`, `FR-046`, `NFR-008`, `NFR-009`, `FR-REP-01` through `FR-REP-03`, `NFR-REP-01` through `NFR-REP-03`, `AC1` through `AC5`, and resolved plan critique findings `PC-001` through `PC-006` across `src/core` and `src/api` without editing `src/api/src/zava_forward/api/web/role-screens.js`.
* Plan: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md (`C1`–`C16`), direct inspection of `src/core/src/zava_forward/core/resident_journey_design.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/resident_showcase.py`, `src/api/src/zava_forward/api/resident_demo/app.py`, `src/api/src/zava_forward/api/server.py`, `src/core/tests/test_resident_journey_design.py`, `src/api/tests/test_representative_expiry_api.py`, `src/api/tests/test_role_endpoint_inventory.py`, `git diff --stat`, and CLI validation outputs (`ruff`, `mypy`, `unittest`).

## Opening Review State

* Interpreted review goal: Verify in a single post-implementation review pass that `P01`, `P02`, and `P03` deliver task-limited representative view projection and request/mid-session representative expiry (`FR-045`, `FR-046`, `NFR-008`, `NFR-009`) across `src/core` and `src/api` in conformance with all requirements, acceptance criteria, critique dispositions, and static/runtime gates while keeping `role-screens.js` untouched.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — plan, phase details, plan critique, changes log, research artifact, git diff, and `ruff`/`mypy`/`unittest` outputs are complete and reconciled.
* Acceptance basis: `FR-REP-01`..`FR-REP-03`, `NFR-REP-01`..`NFR-REP-03`, `AC1`..`AC5`, `Test Ownership and Change Budget Lock`, and resolved critique items `PC-001`..`PC-006`.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`, `P02`, `P03`, and `## Follow-Up Items`, followed by code-and-test verification of task-scope isolation and exact-second `expires_at` / mid-session state transitions.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md` during Review; do not mutate production code, tests, plan, phase details, critique, research, or changes artifacts.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across all 3 phases (`P01`, `P02`, `P03`), 8 tasks (`P01-T01`..`P03-T03`), 6 critique dispositions (`PC-001`..`PC-006`), 5 acceptance criteria (`AC1`..`AC5`), and full `src/core` + `src/api` lint, format, strict type-check, and unit/HTTP loopback test results.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | `### Core Representative View Projection, Expiry Evaluation, and Session State Machine (P01: P01-T01, P01-T02, P01-T03)` | Reconciled | All three core modules (`resident_journey_design.py`, `resident_decisions.py`, `resident_showcase.py`) match plan markers and phase details. |
| `P02` (`P02-T01`, `P02-T02`) | `### HTTP Resident-Session and Case API Representative Expiry Enforcement (P02: P02-T01, P02-T02)` | Reconciled | `resident_demo/app.py` and `server.py` enforce task-limited representative views and immediate request/mid-session expiry without touching `role-screens.js`. |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | `### Domain Unit Tests, HTTP Loopback Expiry Tests, Role Inventory, and Static Analysis (P03: P03-T01, P03-T02, P03-T03)` | Reconciled | Exact 3-file test budget respected (`test_resident_journey_design.py`, `test_representative_expiry_api.py`, `test_role_endpoint_inventory.py`); all lint, format, `mypy`, and `unittest` checks passed. |
| `## Follow-Up Items` | `## Follow-Up Items` (parent Issue #154 sibling criteria `C2` and `C5` / #155) | Reconciled | Kept outside active C3 scope in both plan Non-Goals and changes Follow-Up Items without claiming full Issue #154 closure. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/resident_journey_design.py`, `src/core/pyproject.toml` | Created typed representative authority evaluator, UTC `expires_at` / `review_date` ceiling calculator, positive-allowlist task projector (`Receive information`, `Communicate`, `Attend`, `Works decision`), `Offered - not booked` vs three-party `Visit confirmed` separation (`FR-046`), thread-safe `RepresentativeSessionStore`, and `enforce_representative_action`. | Module inspected; `ShowcaseRow`, `home`, `sensors`, out-of-scope measures, household `documents`, unrelated complaints/handover/decisions, sibling representative grants, and sensitive household notes omitted. | `ruff check`, `ruff format --check`, `mypy` (335 files), and 16 tests in `test_resident_journey_design.py` passed. | Reconciled (`AC1`, `AC3`, `FR-REP-01`..`03`, `NFR-REP-01`..`03`). |
| `P01-T02` | `src/core/src/zava_forward/core/resident_decisions.py` | Added optional UTC `expires_at` validation in `_res_representative_record`, UTC `expires_at` ceiling enforcement in `authority_for(..., now=None)` alongside `controls.today()`, and lock-guarded `representative_view` / `representative_action_check` store helpers. | Preserves existing `authority_date`/`review_date` callers while rejecting expired `expires_at` timestamps at exact-second precision. | `test_resident_decisions.py` (434 tests) and `test_resident_journey_design.py` passed; `mypy` passed. | Reconciled (`AC2`, `PC-002`, `PC-003`). |
| `P01-T03` | `src/core/src/zava_forward/core/resident_showcase.py` | Added frozen `RepresentativeShowcaseGrant` (with `revoked`), `admit_representative_grant`, `representative_grant_evaluation`, and `representative_showcase_view` without altering `ShowcaseRow` or `ROW_KEYS`. | `ROW_KEYS` and `ShowcaseRow` untouched; `RepresentativeShowcaseGrant(expires_at=None)` fails closed as `missing_expiry`. | `test_resident_showcase.py` and `test_resident_preview_api.py` passed; `mypy` passed. | Reconciled (`AC4`, `PC-001`, `PC-002`, `PC-005`). |
| `P02-T01` | `src/api/src/zava_forward/api/resident_demo/app.py` | Wired representative login admission, disjoint `rep:<case_id>:<representative_ref>` handle lookup, additive `/demo/session` state preserving `csrf`/`session_id`, task-limited `/demo/view` (`200` active / `403` `expired` or `held`), `TASK_ASSISTANT_TOPICS` + `grant.documents` enforcement on `/demo/assistant`, and isolated callback owner keys + live `authorised()` checks on `/demo/agenda`. | Verified representative sessions transition immediately mid-session when `now >= expires_at` or `revoked=True`, returning `403` with `expires_at` and `renewal_route` and zero `@example.com` or household canary leaks. | `test_representative_expiry_api.py` and `test_resident_*.py` (275 tests in `src/api`) passed. | Reconciled (`AC3`, `AC4`, `PC-001`, `PC-005`, `PC-006`). |
| `P02-T02` | `src/api/src/zava_forward/api/server.py` | Added `GET` and `POST /api/cases/<id>/representative-view` gated by `projection.allowed(u, "case")` and `controls.RESIDENT_VIEW_ROLES` prior to `s._case(cid)`, keeping `src/api/src/zava_forward/api/web/role-screens.js` untouched. | `git diff --stat` confirms `0` edits to `role-screens.js`; unauthorized roles receive `403` before case lookup/rule checks. | `CaseRepresentativeViewApi` and `test_role_endpoint_inventory.py` (24 tests) passed. | Reconciled (`AC3`, `AC4`, `PC-003`). |
| `P03-T01`..`P03-T03` | `src/core/tests/test_resident_journey_design.py`, `src/api/tests/test_representative_expiry_api.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/pyproject.toml` | Added 7 domain projection/expiry/session unit tests (preserving all 9 Markdown design tests), 3 end-to-end HTTP loopback expiry/isolation tests, and role-endpoint inventory registration; executed `ruff`, `mypy`, and `unittest` across `src/core` and `src/api`. | Exact change budget lock satisfied (`7` production files, `3` test files, `0` test removals, `0` edits to `role-screens.js`). | All `ruff check`, `ruff format --check`, `mypy`, and resident/representative/role-inventory/dependency `unittest` runs exited `0`. | Reconciled (`AC1`..`AC5`, `NFR-REP-03`). |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`ResidentDemo._live_grant_for_handle`) | Local judgment refinement: matched live resolver grants via `self.codec.handle(candidate.principal_subject) == handle` instead of comparing raw `principal_subject` to hashed `session.handle`. | Caught by `ResidentDemoRepresentativeExpiryApi` HTTP test when live `revoked=True` mutation ran against an open session; no user decision needed. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md` under `### Domain Unit Tests, HTTP Loopback Expiry Tests, Role Inventory, and Static Analysis`. | Not needed — preserves approved `P02-T01` / `PC-001` intent. | Reconciled. |
| `P01-T01` (`TASK_ASSISTANT_TOPICS`) | Local judgment refinement: excluded `"documents"` and `"appointments"` from `TASK_ASSISTANT_TOPICS["Receive information"]` and `TASK_ASSISTANT_TOPICS["Communicate"]` so household document checklists remain blocked (`403` `task_out_of_scope`) unless explicitly scoped. | Caught by `test_task_limited_projection_scopes_view_assistant_and_agenda_isolation` verifying `PC-005` / `FR-045` non-disclosure; no user decision needed. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md` and verified across both `src/core` and `src/api` suites. | Not needed — directly enforces `PC-005` and `FR-REP-01`. | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six critique findings (`PC-001` through `PC-006`) from `.copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-plan-critique.md` were applied as direct planner corrections prior to implementation and are verified in production code and tests (`rep:<case_id>:<representative_ref>` handles and isolated `Agenda` callback keys, additive `/demo/session` CSRF preservation, `review_dateT00:00:00Z` vs `missing_expiry` fail-closed semantics, `versions[-1]` precedence, `controls.RESIDENT_VIEW_ROLES` + `with self.lock:` + `server.py` route ordering, `appointments.py` `resident_bindings`/three-party confirmations/`appointment_authorities` window checks, `TASK_ASSISTANT_TOPICS` + `grant.documents` scoping, and `"Unknown"` `representative_ref` rejection + denied `case_id` omission).
* Material revisions: None. Implementation required only two ordinary local-judgment refinements that strengthened approved intent.
* Dependent-work pause assessment: No material discovery occurred; phases executed cleanly in dependency order (`P01` -> `P02` -> `P03`).
* Justification assessment: Supported by complete static and runtime test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Parent Issue #154 remaining criteria (`C2` remaining resident portal journey screens and `C5` empirical resident usability validation under Issue #155) | Caller explicitly scoped this branch/worktree to Criterion 3 (`Representative views show only task-limited authority and expire as recorded`) while avoiding conflicting edits to `role-screens.js`. | Parent backlog / UX workstream (#154, #155) | Distinct follow-up work outside active `P01`–`P03` scope; keep Issue #154 linked with `Refs #154` rather than `Closes #154` until `C2` and `C5` (#155) are also proven. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were found within the assessed Issue #154 Criterion 3 boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No `rpi-implement`, `rpi-plan`, or `rpi-research` remediation required for Issue #154 Criterion 3 | All `FR-REP-01`..`03`, `NFR-REP-01`..`03`, `AC1`..`AC5`, and `PC-001`..`PC-006` requirements are verified conformant. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Parent Issue #154 sibling criteria outside Criterion 3 (`C2` remaining resident-portal screen coverage and `C5` empirical usability validation tracked by Issue #155) remain distinct follow-up backlog items; link PRs for this branch with `Refs #154`.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `ruff check .` | `src/core` | Passed | `All checks passed!` (exit `0`) |
| `ruff format --check .` | `src/core` | Passed | `282 files already formatted` (exit `0`) |
| `mypy` | `src/core` | Passed | `Success: no issues found in 335 source files` (exit `0`) |
| `python -m unittest discover -s tests -p "test_resident_journey_design.py" -v` & `test_resident_*.py` + `test_dependency_rule.py` | `src/core/tests` | Passed | `16` tests in `test_resident_journey_design.py` (`0.015s`) and `614` tests across `test_resident_*.py` (`skipped=181`) + `test_dependency_rule.py` passed (exit `0`) |
| `ruff check .` | `src/api` | Passed | `All checks passed!` (exit `0`) |
| `ruff format --check .` | `src/api` | Passed | `197 files already formatted` (exit `0`) |
| `mypy` | `src/api` | Passed | `Success: no issues found in 281 source files` (exit `0`) |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest discover` (`test_representative_expiry_api.py`, `test_role_endpoint_inventory.py`, `test_resident_*.py`, `test_dependency_rule.py`) | `src/api/tests` | Passed | `3` tests in `test_representative_expiry_api.py`, `24` tests in `test_role_endpoint_inventory.py`, `275` tests in `test_resident_*.py` (`skipped=9`), and `2` tests in `test_dependency_rule.py` passed (exit `0`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01`, `P02`, `P03`) is complete, reconciled, strictly typed, lint-clean, and verified by both domain unit tests and live loopback HTTP session/case API tests proving positive-allowlist task-limited representative projection (`FR-045`, `FR-046`), immediate as-recorded `expires_at` and mid-session revocation/dispute/context-change enforcement (`NFR-008`, `NFR-009`), non-disclosure of household PII and sibling measures/representatives, and zero modifications to `role-screens.js` or `ShowcaseRow`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up (`Refs #154` / `#155`) | Progress parent Issue #154 Criterion 2 resident portal screens and Criterion 5 (#155) usability validation in separate follow-up workstreams |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `ruff check`, `ruff format --check`, `mypy`, and resident/representative/role-inventory/dependency `unittest` suites passed in `src/core` and `src/api`
* Blockers: None

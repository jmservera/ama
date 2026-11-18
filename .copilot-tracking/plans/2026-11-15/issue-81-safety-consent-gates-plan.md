<!-- markdownlint-disable-file -->
# RPI Plan: Issue #81 Exercise-Scenario Safety and Resident Consent Gate Verification

## Task Metadata

* Task ID: issue-81-safety-consent-gates
* Task slug: issue-81-safety-consent-gates
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-81-safety-consent-gates-plan-critique.md

## Executive Summary

This plan proves the two exercise-scenario Acceptance Criteria of GitHub issue `#81` ("Epic: Safety, resident consent and controlled lifecycle") in `src/core`: zero controlled progressions with unresolved safety evidence (`BRD BG-003`, `RULE-001`, `PRD FR-008`) and zero work started without a valid active resident agreement or an explicitly authorised exception (`BRD BG-005`, `RULE-002`, `BRD FR-011`, `BRD FR-014`, `PRD FR-008`). Rather than creating a duplicate lifecycle simulator, the plan hardens fail-closed edge cases discovered in `gates.py`, `store.py`, `sqlstore.py`, and `resident_decisions.py`, implements a deterministic verifier module `src/core/src/zava_forward/core/safety_consent_exercise_gate.py` (`verify_exercise_safety_and_consent_gates` and `verify_store_safety_and_consent_invariants`) that executes against authoritative `Store` and `SqlStore` transitions across all seeded and synthetic exercise scenario suites, proves the invariants in `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, and documents the verifier and its offline evidence boundaries in `src/core/README.md`.

### User Decisions and Requirements Highlights

* Prove both exercise-scenario Acceptance Criteria of `#81` (`No controlled progression with unresolved safety evidence in the exercise scenarios` and `No work started without valid resident agreement or authorised exception in the exercise scenarios`) via a deterministic verifier in `src/core` and dedicated test `src/core/tests/test_safety_consent_exercise_scenarios_81.py`.
* Validate under the Focused validation tier (`ruff check`, `mypy`, and `unittest` in `src/core`), update `src/core/README.md`, and commit all source, test, documentation, and `.copilot-tracking/` artifacts locally on `feat/safety-81-exercise-gates` without pushing.

### What You May Not Know

* The prompt's illustrative module names (`lifecycle.py`, `safety.py`, `consent.py`, `learning_bundles.py`) map to `gates.py`, `store.py`, `procurement.py`, `appointments.py`, `signoffs.py`, `quality.py`, `hazard.py`, `workflows.py`, `taskqueues.py`, `resident_decisions.py`, and `learning_test_bundles.py` in `src/core`.
* Contrarian inspection uncovered three fail-closed gaps to close alongside the verifier: standalone `safeguarding_items` were not checked in `gates.booking_gates`, missing or non-list `hazards`/`safeguarding_items` were not normalized to a `GateError`-producing blocker in `Store._open_safety_items`, and `resident_decisions.py` lacked a structured fail-closed validator (`validate_authorised_works_exception`) for the `BG-005` / `RULE-002` / `FR-014` (`AC-018`) authorised-exception path.
* In `synthetic/resident_preview_fixture.py`, `SYN-C3` sits at display stage `"Works under way"` with an active P1 `Damp` hazard (`released=False`), `decision.status == "Waiting"`, and zero issued or appointed work orders; only `SYN-C1` holds an `Appointed` work order (with valid scoped acceptance and zero hazards).

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) under `2026-11-15/` for issue `#81` (caller prompt).
* Work on branch `feat/safety-81-exercise-gates` in `/home/azureuser/source/ama-demo-wt/feat-81-safety-consent-gates` targeting parent branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) under the Focused validation tier in `src/core` (caller prompt).
* Add a deterministic exercise-scenario gate verifier (`verify_exercise_safety_and_consent_gates` in `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`) verifying across all exercise scenarios that every controlled progression attempt with unresolved safety evidence is blocked with an explicit safety-gate refusal (`RULE-001` / `FR-008`) and every attempt to start work without a valid active resident agreement or an explicitly authorised exception is blocked with an explicit consent-gate refusal (`RULE-002` / `FR-011`) (caller prompt; issue `#81`).
* Add dedicated unit/integration test `src/core/tests/test_safety_consent_exercise_scenarios_81.py` proving both exercise-scenario invariants across all seeded and exercise scenarios (caller prompt).
* Update `src/core/README.md` to document the `#81` exercise-scenario verifier and its offline evidence boundary (caller prompt; `.github/copilot-instructions.md`).
* Run `ruff check`, `mypy`, and `unittest` in `src/core`, then commit all code, tests, documentation, and `.copilot-tracking/` artifacts locally with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing (caller prompt; `.github/copilot-instructions.md`).

## Goals

* Close fail-closed edge cases in `gates.py`, `store.py`, and `resident_decisions.py` so safety holds (including standalone safeguarding items and missing/malformed safety collections) and resident consent / authorised works exceptions behave deterministically across every controlled transition.
* Deliver `safety_consent_exercise_gate.py` (`verify_exercise_safety_and_consent_gates`) exercising all `src/core` exercise scenario suites (`constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`, and `learning_bundles`) against authoritative `Store` and `SqlStore` gates.
* Prove zero unblocked safety progressions and zero unconsented/unauthorised work starts across positive, negative, unknown, scope-drift, representative-authority, repaired-unreleased, safeguarding, authorised-exception, and tamper-detection test cases in `test_safety_consent_exercise_scenarios_81.py`, and document the capability in `src/core/README.md`.

## Scope and Non-Goals

### In Scope

* Fail-closed standalone safeguarding, strict boolean `released`, and malformed-safety hardening in `src/core/src/zava_forward/core/gates.py` and `src/core/src/zava_forward/core/store.py`, plus legacy non-dict `appointments` row-projection tolerance in `src/core/src/zava_forward/core/sqlstore.py` so `resident_preview_fixture.build` datasets load cleanly under `SqlStore`.
* Fail-closed `validate_authorised_works_exception`, `RESIDENT_FIELDS` retention inclusion (`"authorised_works_exceptions"`), and optional `now` deterministic clock threading in `resident_gate` / `_resident_decision_gate` in `src/core/src/zava_forward/core/resident_decisions.py` enforcing `BRD RULE-002` (`AC-004`), `BRD FR-008` (`AC-011`), `BRD FR-011` (`AC-015`), and `BRD FR-014` (`AC-018`).
* New deterministic verifier module `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`.
* New test module `src/core/tests/test_safety_consent_exercise_scenarios_81.py`.
* Documentation section in `src/core/README.md`.

### Non-Goals

* Closing epic `#81` as a whole (`#440` stabilization checkpoint and remaining child issues stay outside this slice).
* Editing `src/api` web templates, `infra/`, `.github/workflows/`, or SQL schema DDL.
* Claiming live legal sign-off, live resident-engagement validation, or production operational authority from synthetic exercise checks.
* Pushing commits to any remote or opening/updating a GitHub pull request in this session.

## Functional Requirements

* `FR-PLAN-01`: `gates.booking_gates` and `Store._open_safety_items` / `Store.require_safety_clear` fail closed (`FAIL` / `UNKNOWN` / `GateError` citing safety review / `RULE-001; PRD FR-008`) whenever a case has any unreleased hazard (`released is not True`, including repaired-but-unreleased), any open standalone safeguarding item (`safeguarding_items` or item-shaped `safeguarding`), or missing/non-list/non-dict safety records, while leaving emergency hazard referral (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `record_repair`) open (`BRD FR-002`).
  * Observable acceptance criteria: Every controlled progression entrypoint (`advance`, `technical_action("signoff_give")`, `issue_work_order`, `reissue_work_order`, `record_wo_appointment("Booked")`, `appointment_control("confirm")`, `complete_work_order`, `correct_work_order`, `accept_quality`, `hand_over_quality`) raises `GateError` without mutating case state, work orders, or the audit ledger when safety evidence is unresolved.
* `FR-PLAN-02`: `resident_decisions.validate_authorised_works_exception` and `resident_decisions.resident_gate` block work-order issuance, contractor appointment activation (`Issued` -> `Appointed`), booking progression (`advance` -> `Install booked`), completion, quality acceptance, and handover unless each bound measure has either (a) a current `Accepted` resident or confirmed `Works decision` representative decision on the active `context_revision` and `design_version`, or (b) an explicit `Authorised` human-approved (`Building Safety Liaison` or `Retrofit Programme Manager`, rejecting automated/AI tokens), dated (`effective_date <= check_day < review_date` and unexpired `expires_at` per `RULE-002`), current-scope (`measure`, `context_revision`, `design_version` per `FR-008`), resident-notified (`resident_notified is True` + `notification_ref` per `FR-014` `AC-018`) `authorised_works_exceptions` record, and no tenure hold, expired retention, or open `"Needs human review"`.
  * Observable acceptance criteria: Consultation notes, silence, legacy case-wide `decision.status = "Accepted"`, survey access, appointment offers, `Attend`/`Communicate`/`Receive information` representative permissions, paused/withdrawn/declined decisions, design-version drift, and expired/unnotified/AI-approved/revoked exceptions all fail closed with explicit consent-gate refusals and zero state or audit mutation.
* `FR-PLAN-03`: `safety_consent_exercise_gate.verify_exercise_safety_and_consent_gates` deterministically evaluates all built-in `src/core` exercise scenario suites (`constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`, and `learning_bundles`), plus optional caller-supplied scenario overrides or `SqlStore` mode, returning structured counts, rule references (`RULE-001`, `RULE-002`, `FR-008`, `FR-011`), per-attempt refusal records, and violation lists.
  * Observable acceptance criteria: Running `verify_exercise_safety_and_consent_gates()` on both JSON `Store` and SQLite `SqlStore` returns `passed is True`, `controlled_progressions_with_unresolved_safety == 0`, `work_started_without_agreement_or_exception == 0`, and `violations == []`, while running it against tampered scenarios with an unconsented `Appointed` work order or bypassed gate reports `passed is False` with concrete violation entries.

## Non-Functional Requirements

* Determinism and Offline Execution
  * Objective threshold or evaluation condition: Zero network calls, zero wall-clock nondeterminism (`as_of` / reference date pinned deterministically), identical output across repeated invocations.
  * Operating condition or verification approach: Verified in `test_safety_consent_exercise_scenarios_81.py` by asserting structural equality across repeated runs and checking both `Store` and `SqlStore`.
  * Observable acceptance criteria: `verify_exercise_safety_and_consent_gates(as_of="2026-11-15")` produces identical deterministic summaries across runs and completes within the `src/core` unit suite without external dependencies.
* Type, Lint, and Existing-Suite Regression Safety
  * Objective threshold or evaluation condition: Zero `ruff check` issues, zero `mypy` errors, and 100% pass rate across existing and new `src/core` `unittest` discovery.
  * Operating condition or verification approach: Run `python3 -m ruff check`, `python3 -m mypy`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` in `src/core`.
  * Observable acceptance criteria: All three commands exit `0` with zero regressions, zero `.copilot-tracking/` references in production/test code or commit messages, and explicit exercise-only disclaimers preserved.

## Acceptance Criteria

* `AC-1` (`#81` Exercise Safety Gate): Across all `src/core` exercise scenarios (`constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`), 100% of controlled progression attempts on cases with unresolved safety evidence (open hazard, unaccepted referral, repaired-but-unreleased hazard, open standalone safeguarding item, or missing/malformed safety state) are blocked with an explicit safety-gate refusal (`RULE-001` / `FR-008`) and leave case state, work orders, and audit entries unchanged (`controlled_progressions_with_unresolved_safety == 0`).
* `AC-2` (`#81` Exercise Consent Gate): Across all `src/core` exercise scenarios (including `learning_bundles` zero-breach stop rules), 100% of work-start and work-order activation attempts without a valid active resident agreement (or confirmed in-window `Works decision` representative agreement) or a valid human-approved, resident-notified, current-scope `authorised_works_exceptions` record are blocked with an explicit consent-gate refusal (`RULE-002` / `FR-008` / `FR-011`) and leave case state, work orders, and audit entries unchanged (`work_started_without_agreement_or_exception == 0`).
* `AC-3` (Dedicated Test & Tamper Proof): `src/core/tests/test_safety_consent_exercise_scenarios_81.py` verifies `AC-1` and `AC-2` across JSON `Store` and SQLite `SqlStore`, tests positive independent safety release and positive valid resident/representative/authorised-exception paths, and proves the verifier flags violations when synthetic state is deliberately corrupted.
* `AC-4` (Documentation & Validation): `src/core/README.md` documents `safety_consent_exercise_gate` and `validate_authorised_works_exception` with honest offline exercise boundaries, `ruff check`, `mypy`, and `unittest` all pass in `src/core`, and all work plus `.copilot-tracking/` artifacts are committed locally on `feat/safety-81-exercise-gates` with the Copilot trailer and clean `git status --short`.

## Test Ownership and Coverage Lock

* Canonical production targets:
  * `src/core/src/zava_forward/core/gates.py` (update)
  * `src/core/src/zava_forward/core/store.py` (update)
  * `src/core/src/zava_forward/core/sqlstore.py` (update)
  * `src/core/src/zava_forward/core/resident_decisions.py` (update)
  * `src/core/src/zava_forward/core/safety_consent_exercise_gate.py` (new)
* Canonical documentation target:
  * `src/core/README.md` (update)
* Canonical test target:
  * `src/core/tests/test_safety_consent_exercise_scenarios_81.py` (new; owned by this task)
* Generated targets: `none`
* Exact test removals: `none`
* Maximum test additions: 1 new test module (`src/core/tests/test_safety_consent_exercise_scenarios_81.py`, <= 12 focused `unittest.TestCase` methods covering semantic gate refusal invariants, SQL parity, authorised-exception fail-closed boundaries, learning-bundle stop rules, and verifier tamper detection; existing `test_gates.py`, `test_hazard_referral.py`, `test_resident_decisions.py`, and `test_learning_test_bundles.py` remain untouched as regression coverage).
* Validation evidence commands (from `src/core`):
  * `python3 -m ruff check`
  * `python3 -m mypy`
  * `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-81-safety-consent-gates-plan.md                                                                 |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md                                                      |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-81-safety-consent-gates-plan-critique.md (`Revise` resolved: `PC-001`–`PC-005` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-81-safety-consent-gates-research.md (`executed`, `Ready`, `C1`–`C18`)                        |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-81-safety-consent-gates-changes.md is created by implementation as its evidence record        |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement`                                                                                                 |
| Continuation context             | Active automatic RPI Agent parent continues to `rpi-implement` once plan critique and readiness gates pass                               |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-81-safety-consent-gates-research.md`: Code-backed `C1`–`C18` mapping of controlled transitions, safety holds, resident consent, synthetic exercise suites, and contrarian edge cases.
* `docs/brds/agentic-retrofit-programme-brd.md`: Defines `BG-003`, `BG-005`, `FR-001`, `FR-002`, `RULE-001`, `RULE-002`, `RULE-003`, `FR-008`, `FR-011` (`AC-015`), and `FR-014` (`AC-018`).
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Defines `FR-008` (`AC-011`), `FR-014` (`AC-017`), `FR-015` (`AC-018`), `FR-045`, and `FR-046`.
* `src/core/src/zava_forward/core/gates.py`, `store.py`, `procurement.py`, `appointments.py`, `signoffs.py`, `quality.py`, `workflows.py`, `taskqueues.py`, `resident_decisions.py`, `learning_test_bundles.py`, and `synthetic/`: Authoritative runtime gate and exercise-scenario modules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fail-Closed Safety and Authorised-Exception Gate Hardening

* Intent: Close the three contrarian fail-closed gaps in `gates.py`, `store.py`, and `resident_decisions.py` without breaking any existing `src/core` contract.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden standalone safeguarding, strict boolean `released`, and SQLite row tolerance in `gates.py`, `store.py`, `sqlstore.py`, and `taskqueues.py`

* Requirement and evidence: `FR-PLAN-01`; research `C1`, `C2`, `C8`, Contrarian Findings 1 and 2; critique `PC-001`, `PC-002`.
* Expected result: `gates.booking_gates`, `Store._open_safety_items`, and `taskqueues.has_open_safety` / `is_open_safety_item` enforce strict boolean `released` semantics (rejecting truthy strings/ints) and fail closed on open or malformed `safeguarding_items`, legacy `safeguarding`, and `hazards=None` values while preserving absent-key behavior on minimal hazard-only dicts and note-only canary dicts; `SqlStore._row` tolerates legacy string `appointments` entries (`isinstance(a, dict)`) so `resident_preview_fixture.build` datasets load cleanly under `SqlStore`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add fail-closed `validate_authorised_works_exception` and deterministic `now` clock support in `resident_decisions.py`

* Requirement and evidence: `FR-PLAN-02`; research `C9`, `C11`, `C17`, Contrarian Finding 3; critique `PC-003`.
* Expected result: `validate_authorised_works_exception` validates explicit `authorised_works_exceptions` records against `RULE-002` (`AC-004`), `FR-008` (`AC-011`), `FR-011` (`AC-015`), and `FR-014` (`AC-018`) (including memory/sensor-reference rejection), `"authorised_works_exceptions"` is added to `RESIDENT_FIELDS` for retention purge, and `resident_gate` / `_resident_decision_gate` accept optional `*, now=None` and honor only valid human-authorised, resident-notified, current-scope, in-window exceptions while preserving tenure, retention, human-review, and safety holds.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Exercise-Scenario Safety and Consent Verifier

* Intent: Implement `safety_consent_exercise_gate.py` (`verify_exercise_safety_and_consent_gates`) covering every `src/core` exercise scenario suite across `Store` and `SqlStore`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`

* Requirement and evidence: `FR-PLAN-03`, `AC-1`, `AC-2`; research `C1`–`C18`.
* Expected result: `verify_exercise_safety_and_consent_gates` deterministically verifies static work-order invariants and dynamic progression/work-start refusals (`RULE-001` / `FR-008` and `RULE-002` / `FR-011`) with state and audit-chain immutability checks across `constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`, and `learning_bundles`, supporting both JSON `Store` and SQLite `SqlStore` plus caller-supplied scenario inspection.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Verification Suite, Core Documentation, and Focused Validation

* Intent: Prove `#81` invariants in `test_safety_consent_exercise_scenarios_81.py`, update `src/core/README.md`, and pass `ruff check`, `mypy`, and `unittest` in `src/core`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `src/core/tests/test_safety_consent_exercise_scenarios_81.py`

* Requirement and evidence: `AC-1`, `AC-2`, `AC-3`; caller prompt item 3.
* Expected result: Dedicated unit/integration test suite verifies zero unblocked safety progressions and zero unconsented/unauthorised work starts across all exercise scenario suites in both `Store` and `SqlStore`, exercises positive independent safety release and valid agreement/authorised-exception transitions, tests all fail-closed rejection vectors, and verifies tamper detection when corrupted state or a simulated bypass is injected.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Document verifier in `src/core/README.md` and run `src/core` validation

* Requirement and evidence: `AC-4`; caller prompt items 4 and 5; `.github/copilot-instructions.md`.
* Expected result: `src/core/README.md` documents `safety_consent_exercise_gate` and `validate_authorised_works_exception` with `Refs #81` and explicit synthetic-exercise boundaries; `python3 -m ruff check`, `python3 -m mypy`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` pass cleanly in `src/core`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md

## Dependencies

* `zava_forward.core` editable/local source layout (`src/core/src` and `src/core/tests`): Required for `ruff check`, `mypy`, and `unittest` discovery.
* Existing gate, store, workflow, procurement, appointment, signoff, quality, resident-decision, synthetic, and learning-bundle modules in `src/core`: Exercised directly by `safety_consent_exercise_gate.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `2026-11-15` `PC-001` (High: `resident_preview_fixture.build`, `SqlStore._row` legacy string `appointments`, `docs_dir`, initial-seed `contract_authorities`, and coverage lock) | Applied | Added `sqlstore.py` (`isinstance(a, dict)` guard in `SqlStore._row`) to `Canonical production targets` and `P01-T01`, and updated `P02-T01` to use `resident_preview_fixture.build(preview_dir)` with `docs_dir=str(preview_dir / "docs")` and initial-seed `contract_authorities`. |
| `2026-11-15` `PC-002` (High: strict boolean `released` semantics and malformed legacy `case["safeguarding"]` fail-closed guard) | Applied | Updated `P01-T01` and `P03-T01` so `gates.booking_gates` and `Store._open_safety_items` require strict boolean `released` (`type(val) is bool` when not `None`) and fail closed on malformed legacy `safeguarding` while preserving note-only canary dicts. |
| `2026-11-15` `PC-003` (High: `as_of` / `now` deterministic clock propagation, wall-clock-free summaries, memory/sensor ref rejection, and `RESIDENT_FIELDS` retention entry) | Applied | Updated `P01-T02` and `P02-T01` to add `"authorised_works_exceptions"` to `RESIDENT_FIELDS`, reject memory/sensor references, thread optional `*, now=None` into `resident_gate` and `_resident_decision_gate`, and omit wall-clock timestamps and temp paths from verifier summaries. |
| `2026-11-15` `PC-004` (Medium: align `ZF-3` with `tests/dataset.py` `DATA`, `sensor_scenarios` `SEED = 190` `C01`–`C11`, and `learning_test_bundles.run_report` contract) | Applied | Updated `P02-T01` and `P03-T01` to align `ZF-3` with `dataset.DATA` (using an explicit `ZF-3-LEGACY` variant for legacy case-wide `Accepted`), project `sensor_scenarios` `C01`–`C11`, and call `learning_test_bundles.run_report` across `story-once`, `pre-visit-pack`, and `change-impact`. |
| `2026-11-15` `PC-005` (Medium: expand static and isolated-dynamic tamper checks in `verify_store_safety_and_consent_invariants`) | Applied | Updated `P02-T01` and `P03-T01` so static checks inspect `Issued`/`Appointed`/`Completed` work orders, `returns` `advance` events, and accepted/handed-over quality checklists, plus isolated dynamic probes on unsafe/unconsented cases. |
| Residual risk (synthetic exercise scope) | Accepted | Rules and scenarios are synthetic offline exercise fixtures (`Unreviewed exercise rule`) and do not claim live legal sign-off or close epic `#81` overall (`Refs #81`). |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-81-safety-consent-gates-changes.md
* Ready phase or task: `P01`, `P02`, and `P03` (`Planning status: Ready`)
* Remaining provisional question or blocker: None

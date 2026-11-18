<!-- markdownlint-disable-file -->

# Task Research: core-1238-stale-pending-2346

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                 |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                    |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md |

## Research Brief

* What to research: Inspect `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, and adjacent consumers across `src/` to verify the first four acceptance criteria of Issue #1238 (outcome write single retry on failure after `Acknowledged` receipt, `receipt_ref` logging when write still fails, regression test for failed-write path, safety of `attempts[-1]` use after reservation) and determine the exact design and status vocabulary to mark a stale `Pending` attempt as superseded (remaining un-ticked AC, low F3) while preserving audit history and idempotency invariants.
* Why it matters: Issue #1238 tracks follow-ups from the independent diff review of #86 (`6ff492ad`). Four criteria are ticked on #1238 and must be verified against current branch code; the fifth criterion (`Mark a stale Pending attempt superseded`) remains un-ticked and must be implemented cleanly without breaking reservation safety, idempotency, projections, or tests.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases of the `core-1238-stale-pending-2346` task.
* Scope: `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, and any callers/projections/schemas in `src/core`, `src/api`, `src/agents`, `src/orchestrator`, `src/importer`, or `docs/` that read or constrain resident-decision attempt statuses.
* Non-goals: Unrelated resident-decision features, UI overhauls, bulk `del sys.modules[...]` in test files, pushing to remote, or modifying unrelated pre-existing modules.
* Criteria: Verify ACs 1-4 with exact `path:line` evidence; identify the canonical status vocabulary and state machine for resident-decision delivery/dispatch attempts; design an unambiguous, audit-preserving transition from stale `Pending` to superseded when an explicit retry/superseding attempt is recorded; ensure compatibility with `mypy`, `ruff`, and `unittest`.
* Requested outputs: Synthesized evidence log, verification of ACs 1-4, comparison of alternatives and convergence recommendation for AC 5 (low F3), and planning readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How are ACs 1-4 currently implemented and tested, what attempt-status vocabulary and invariants govern `resident_decisions.py` and its callers, and how should a stale `Pending` attempt transition to superseded on explicit retry/superseding reservation? |
| Codebase scope                       | `src/core/`, `src/api/`, `src/agents/`, `src/orchestrator/`, `src/importer/`, `docs/`                                               |
| External scope                       | none                                                                                                                                |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, callers in `src/api/` and `src/core/` |
| Initial external candidate areas     | none                                                                                                                                |
| Research posture                     | balanced                                                                                                                            |
| Posture provenance                   | default (bounded internal task with named source targets, checking adjacent callers/projections across `src/` for status consumers) |
| Explicit limits / deadline           | Do not use bulk `del sys.modules[...]` in tests; do not push to remote                                                              |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across `resident_decisions.py`, its tests, and any cross-package attempt-status readers |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                        |
| Known constraints / excluded sources | Codebase-only domain logic; preserve audit history, human/reviewer checks, and idempotency invariants                               |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                            | Scoped authority or output contract                                         | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`              | `applyTo: "**"` matches repository inputs and tracking artifacts | Adds validation-tier rules, Python test/lint rules, and branch/commit rules | Selected automatically as repository-wide instruction                                     |
| Skill               | `python-foundational`                          | Python codebase match                                           | General Python testing/typing patterns                                      | Skipped: existing repository conventions in `src/core` (`unittest`, `mypy`, `ruff`) suffice |
| Research specialist | `hve-core-all:rpi-researcher`                  | Registered general RPI research lane worker                     | Independent subagent lane artifact                                          | Skipped: tightly coupled single-module + cross-ref inspection fits inline execution cleanly |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                          |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with complete caller brief, named files, branch, target, and validation commands               | N/A (non-interactive)| Proceed with `balanced` posture and `convergence` output mode                            |
| Direction change | None; scope remained bounded to `resident_decisions.py`, `test_resident_decisions.py`, and `src/core/README.md`        | N/A                  | Retain active scope and controls                                                         |
| Convergence      | All five research questions answered with high-confidence codebase evidence (`C1`-`C14`)                               | N/A                  | Select atomic stale-`Pending` supersession inside `_res_service_forward` (`retry_unresolved=True`) |

## Scope and Success Criteria

* Scope: `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, and cross-package references to resident-decision attempts/statuses in `src/` and `docs/`.
* Assumptions: ACs 1-4 of Issue #1238 were implemented in an earlier commit (likely #86 or a follow-up commit) and remain intact on `fix/core-1238-stale-pending-2346` — must be verified directly in source and tests rather than assumed.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Inspect `src/core/src/zava_forward/core/resident_decisions.py` and `src/core/tests/test_resident_decisions.py` (or related tests).
  * Verify AC 1: Outcome write is retried once on failure after an `Acknowledged` receipt.
  * Verify AC 2: `receipt_ref` is logged when the write still fails.
  * Verify AC 3: Regression test covers the failed-write path.
  * Verify AC 4: `attempts[-1]` use after reservation is safe.
  * Design AC 5 (low F3): Mark a stale `Pending` attempt as `Superseded` (or `"superseded"` per the module's status vocabulary) when an explicit retry or superseding attempt is recorded after a stale/failed `Pending` reservation, preserving full audit history and idempotency invariants, with focused unit tests.
* Inferred research questions:
  * Which exact status casing/constants (`"Pending"`, `"Superseded"`, etc.) exist in `resident_decisions.py` and across `src/`?
  * What code paths create, inspect, block on, or supersede `Pending` attempts (e.g., explicit retry flag, new decision revision, cancellation, UI/API projections, validation schemas)?
  * Does marking an older `Pending` attempt `Superseded` affect idempotency keys, attempt ordering, `attempts[-1]`, blocking checks, audit events, or UI/API serialization?
* Caller constraints and non-goals: Convergence for RPI implementation on `fix/core-1238-stale-pending-2346`; no bulk `del sys.modules[...]` in tests; no remote push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                    | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|--------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Deliver remaining AC 5 of #1238 and verify ACs 1-4 in `resident_decisions` | Caller intake brief | Focuses design on stale `Pending` supersession and ACs 1-4 verification   |
| exclude                                                  | Do not use bulk `del sys.modules[...]` in test files; do not push branch | Caller intake brief | Constrains test structure and final git operations                        |

## Research Questions

|  # | Sub-question                                                                                                                | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How did earlier commits (#86 and follow-ups) implement ACs 1-4 in `resident_decisions.py` and `test_resident_decisions.py`? | straightforward | H        | answered |
| Q2 | What is the exact attempt data model, status vocabulary/casing, and state machine in `resident_decisions.py`?               | depth           | H        | answered |
| Q3 | Where across `src/` and `docs/` are resident-decision `attempts` and their statuses read, filtered, projected, or displayed? | breadth         | H        | answered |
| Q4 | Through which exact entrypoints can an explicit retry or superseding attempt occur after a stale/failed `Pending` attempt?   | depth           | H        | answered |
| Q5 | What invariants (audit history, idempotency key stability, `attempts[-1]` safety, resend blocking, metadata timestamps/actor) must hold when marking a stale `Pending` attempt superseded? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Issue #1238 body (`gh issue view 1238`), `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `src/core/README.md`, commits `b613276e9` (#1332) and `0385ad6a5` (#1346).
* Reused (verified) findings: Issue #1238 confirms ACs 1-4 were delivered and verified in `b613276e9` (#1332), while `0385ad6a5` (#1346) added `SupersessionBinding` and `service_supersede_authorize` (`manual_verified` two-person supersession without resending) and left AC 5 (`(low F3) Mark a stale Pending attempt superseded`) open on the explicit retry reservation path.
* Superseded / stale: Pre-F3 expectation in `test_resident_decisions.py:4027` (`["Pending", "Acknowledged"]` after `self.forward(retry_unresolved=True)`) reflects the pre-supersession behavior where stale `Pending` attempts stayed `"Pending"` forever after an explicit retry reserved a superseding attempt.

## Research Cycle Log

### Cycle 1

* Active direction controls: `narrow` (Issue #1238 ACs 1-4 verification + AC 5 stale-`Pending` supersession), `exclude` (no bulk `del sys.modules[...]` in test files; no remote push).
* Active research posture and completion basis: `balanced`; verify ACs 1-4 directly in code and tests, check all cross-package `formal_route` / `attempts` consumers across `src/`, and evaluate alternatives for stale `Pending` supersession against audit, idempotency, and `manual_verified` invariants.
* Explicit limits or deadline effect: Keeps test design pure `unittest` without `sys.modules` deletion and keeps git operations local-only.

#### Wave 1: Wider

* Plan and independent lanes: Sweep `src/` (`core`, `api`, `agents`, `orchestrator`, `importer`) and `docs/` for `formal_route`, `service_forward`, `retry_unresolved`, `Superseded`, and `complaints_route.STATUSES` to map every producer and consumer of formal-route attempt statuses.
* Worker evidence relationships or inline fallback: Inline execution (`C1`-`C4`, `C13`-`C14`) because all hits reside in three tightly coupled files under `src/core/`.
* Reflection: `formal_route.attempts` is owned exclusively by `src/core/src/zava_forward/core/resident_decisions.py`, with status constants in `complaints_route.py`, tests in `src/core/tests/test_resident_decisions.py`, and component documentation in `src/core/README.md`. No external package in `src/api`, `src/agents`, `src/orchestrator`, or `src/importer` inspects attempt status strings (`C4`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect `_forward`, `_record_outcome`, `_outcome_recorded`, `_res_service_forward`, `_res_service_forward_outcome`, `_res_service_supersede_authorize`, `resident_retention_delete`, and corresponding unit tests (`JsonResidentDecisions` and `SqlResidentDecisions`).
* Plan and independent lanes: Verify ACs 1-4 line-by-line and trace the exact state machine when an outcome save fails (leaving an attempt `Pending` after `_IN_FLIGHT` clears) and an operator subsequently invokes `service_forward` with `retry_unresolved=True`.
* Worker evidence relationships or inline fallback: Inline execution (`C5`-`C12`).
* Reflection:
  * ACs 1-4 are fully implemented and covered across both JSON and SQLite backends (`C5`-`C9`, `C14`).
  * Title-case `"Superseded"` is already the module's canonical status string (`C3`, `C11`), intentionally excluded from `complaints_route.STATUSES[1:]` so receiver outcomes cannot inject `"Superseded"` (`C3`, `C10`).
  * Critical gap identified (`C10`, `C12`): When `_res_service_forward` executes with `retry_unresolved=True` after an earlier failed outcome write left attempt 1 in `status == "Pending"` (and `not in_flight`), it appends attempt 2 (`Pending`) while leaving attempt 1 in `status == "Pending"` indefinitely (`test_resident_decisions.py:4027` currently observes `["Pending", "Acknowledged"]`). Consequently, stale attempt 1 never transitions to `"Superseded"`, and `_res_service_forward_outcome` would still see `attempts[0]["status"] == "Pending"` if a delayed outcome write targeted attempt 1.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether marking prior `"Pending"` attempts `"Superseded"` inside `_res_service_forward` (`retry_unresolved=True`) conflicts with Owner Decision Q6 (`manual_verified` two-person `service_supersede_authorize`), corrupts `"Unconfirmed"` / `"Failed"` / already-`"Superseded"` attempts, weakens age-based resend blocking, breaks reservation-id lookup (`F2`), or breaks retention deletion.
* Plan and independent lanes: Check all `supersede` tests (`test_resident_decisions.py:4104-4518`), `Unconfirmed`/`Failed` retry tests (`3748-3780`, `3920-3975`), reservation-binding test (`3840-3879`), and retention-deletion logic (`resident_decisions.py:1099-1104`).
* Worker evidence relationships or inline fallback: Inline execution (`C9`-`C13`).
* Reflection:
  * Blocking `retry_unresolved=True` until `service_supersede_authorize` runs is falsified: `store.supersession_binding` defaults to `None` unless explicitly configured, and both existing code and tests (`test_resident_decisions.py:4026`, `4213`) intentionally permit authorized redress owners / named independent reviewers to retry explicitly via `retry_unresolved=True` once `not in_flight`.
  * Age alone still never marks `Pending` as `Superseded` and never authorizes resend: omitting `retry_unresolved=True` fails closed at `resident_decisions.py:1701` before any mutation (`C10`, `C12`).
  * Transitioning only `prior["status"] == "Pending"` inside `_res_service_forward` (after all version, route, closed-status, `retry_unresolved`, `not in_flight`, actor-identity, and `resident_request_ref` checks pass) preserves `"Unconfirmed"`, `"Failed"`, and prior `manual_verified` `"Superseded"` attempts (including their `supersession` dual-approval dict) untouched, while omitting `"supersession"` on retry-superseded attempts and recording `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=attempt` so audit provenance distinguishes `manual_verified` two-person supersession from explicit retry supersession (`C10`, `C11`).
  * Deferring supersession until after `_send` or `_record_outcome` is rejected because two `"Pending"` attempts would coexist while the retry is in flight and late attempt-1 outcomes would remain unfenced during the send window.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| ACs 1-4 are already implemented and regression-tested across JSON and SQLite stores | `C5`, `C6`, `C7`, `C8`, `C9`, `C14` | accepted | Verified directly in `_forward`, `_record_outcome`, `_outcome_recorded`, and `test_resident_decisions.py` | Recorded as verified findings for Q1 |
| Canonical status vocabulary uses title-case `"Superseded"` outside `complaints_route.STATUSES` | `C3`, `C4`, `C10`, `C11` | accepted | Matches existing `"Pending"`, `"Unconfigured"`, `"Failed"`, `"Unconfirmed"`, `"Acknowledged"`, and `_res_service_supersede_authorize` | Selected status vocabulary for Q2/Q3 |
| Atomically transition prior `Pending` attempts to `"Superseded"` inside `_res_service_forward` when `retry_unresolved=True` reserves a superseding attempt | `C10`, `C11`, `C12`, `C13` | accepted | Satisfies AC 5 (low F3), preserves full attempt history and `route_key`, fences late outcomes on stale attempts, and keeps `manual_verified` dual-authorization metadata distinct | Selected convergence recommendation |
| Require `service_supersede_authorize` before `service_forward(retry_unresolved=True)` | `C10`, `C11`, `C12` | rejected | `supersession_binding` is optional (`None` by default); blocking `retry_unresolved=True` would break existing explicit-retry workflows and tests (`4026`, `4213`) | Recorded as rejected alternative |
| Mark stale `Pending` attempts `"Superseded"` only after the new attempt's outcome write succeeds | `C5`, `C6`, `C10` | rejected | Leaves multiple `"Pending"` attempts active during send and fails to supersede attempt 1 if attempt 2's send or outcome write also fails | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Scope saturated; all five research questions are answered with direct `path:line` evidence across code, tests, and docs, and contrarian challenges confirmed invariant compatibility.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C14`)

## Evidence Log

* Delegation: inline: bounded single-module state-machine investigation (`resident_decisions.py`, `complaints_route.py`, `test_resident_decisions.py`, `src/core/README.md`) plus repository-wide `grep` sweep required no separate subagent context.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | Issue #1238 defines 5 ACs from the #86 (`6ff492ad`) diff review: ACs 1-4 are checked and AC 5 (`(low F3) Mark a stale Pending attempt superseded`) is the sole remaining unchecked criterion | `src/core/README.md:555` | read / gh | high | Confirmed against `gh issue view 1238` and `src/core/README.md:537-595` |
| C2  | Commit `b613276e9` (#1332) delivered `_record_outcome` single retry, `_outcome_recorded` lost-commit reconciliation, `receipt_ref` warning logging, and reservation-id binding lookup; commit `0385ad6a5` (#1346) added `SupersessionBinding` and `service_supersede_authorize` | `src/core/src/zava_forward/core/resident_decisions.py:131` | read / bash | high | Verified via `git log` and direct source inspection |
| C3  | `complaints_route.STATUSES` defines `("Pending", "Unconfigured", "Failed", "Unconfirmed", "Acknowledged")`; `"Superseded"` is title-cased and excluded from `STATUSES[1:]` so receiver outcome writes cannot set `"Superseded"` | `src/core/src/zava_forward/core/complaints_route.py:16` | read | high | Paired with `_res_service_forward_outcome` check at `resident_decisions.py:1730` |
| C4  | Repository-wide search across `src/` shows `formal_route`, `service_forward`, `retry_unresolved`, and `"Superseded"` appear only in `src/core/` (`resident_decisions.py`, `test_resident_decisions.py`, `README.md`) | `src/core/src/zava_forward/core/resident_decisions.py:1687` | grep | high | Sweep terms: `formal_route`, `service_forward`, `retry_unresolved`, `Superseded` |
| C5  | **AC 4 verified**: `_forward` generates `reservation = uuid.uuid4().hex`, commits `service_forward`, then resolves `matches = [a for a in route["attempts"] if a.get("reservation_id") == reservation]` (raising `ResidentCommittedError` if `len(matches) != 1`) rather than indexing `attempts[-1]` | `src/core/src/zava_forward/core/resident_decisions.py:824` | read | high | Lines `824-836`; covered by `test_forward_send_is_bound_to_the_attempt_it_reserved` (`test_resident_decisions.py:3840`) |
| C6  | **AC 1 verified**: `_record_outcome` loops `for _ in range(2):` around `_operation(store, user, case_id, outcome)` without re-invoking `_send`, breaks immediately on `_UNVERIFIED` recovery/restoration failure notes, and checks `_outcome_recorded` before retrying | `src/core/src/zava_forward/core/resident_decisions.py:854` | read | high | Lines `854-895` |
| C7  | **AC 2 verified**: When `_record_outcome` exhausts its retry (or aborts on unverified recovery), it logs `"Formal-route outcome not recorded: %s; case %s request %s attempt %s status %s receipt_ref %r"` with `outcome.get("receipt_ref")` at `WARNING` level and raises `ResidentCommittedError` | `src/core/src/zava_forward/core/resident_decisions.py:874` | read | high | Lines `874-881` |
| C8  | **AC 3 verified**: Regression tests cover persistent outcome-write failure (`handler.call_count == 2`, `receipt_ref` logged, `ResidentCommittedError` raised, single send), transient first-write failure retried once without resending, lost commit acknowledgement reconciliation, and unverified recovery non-retry | `src/core/tests/test_resident_decisions.py:4007` | read | high | Lines `4007-4102` |
| C9  | `test_forward_send_is_bound_to_the_attempt_it_reserved` injects a competing `Pending` attempt after reservation and proves `_forward` sends and records against its own `reservation_id` (`attempt == 1`) | `src/core/tests/test_resident_decisions.py:3840` | read | high | Lines `3840-3879` |
| C10 | `_res_service_forward` blocks resends when `unresolved` (`Pending`, `Unconfirmed`, `Superseded`, or legacy `Failed` without `not_sent`) is non-empty unless `body.get("retry_unresolved") is True` and `not in_flight(...)`, then appends a new `Pending` attempt without updating prior `Pending` attempts; `_res_service_forward_outcome` only accepts attempts where `status == "Pending"` | `src/core/src/zava_forward/core/resident_decisions.py:1699` | read | high | Lines `1699-1736` |
| C11 | `_res_service_supersede_authorize` transitions a single `Pending` attempt via `attempt.update(status="Superseded", superseded_from="Pending", superseded_at=_time())` alongside `attempt["supersession"]` after two distinct bound role approvals on `evidence_ref` | `src/core/src/zava_forward/core/resident_decisions.py:1738` | read | high | Lines `1738-1780` |
| C12 | `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` currently asserts `[a["status"] for a in self.route()["attempts"]] == ["Pending", "Acknowledged"]` after `self.forward(retry_unresolved=True)`, proving stale `Pending` attempt 1 was left `"Pending"` after attempt 2 superseded it; `test_supersede_refuses_aged_pending_and_non_pending_attempts` verifies age alone leaves attempt 1 `"Pending"` before `retry_unresolved=True` | `src/core/tests/test_resident_decisions.py:4026` | read | high | Lines `4020-4031` and `4202-4229` |
| C13 | `resident_retention_delete` scrubs `resident_request_ref` and `requested_by` across every dict in `formal_route.attempts` regardless of status while preserving attempt status and supersession metadata | `src/core/src/zava_forward/core/resident_decisions.py:1099` | read | high | Lines `1099-1104` |
| C14 | `SqlResidentDecisions` subclasses `JsonResidentDecisions`, executing every resident-decision unit test against both the JSON file store and SQLite store | `src/core/tests/test_resident_decisions.py:4521` | read | high | Ensures backend parity without `sys.modules` manipulation |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | ACs 1-4 are fully implemented and tested: `_record_outcome` retries failed outcome writes once (`range(2)`), reconciles lost commit acks via `_outcome_recorded`, logs `receipt_ref` on failure, and `_forward` binds sends/outcomes by `reservation_id` instead of `attempts[-1]`. | `C2`, `C5`, `C6`, `C7`, `C8`, `C9` | high | No code fix needed for ACs 1-4; preserve all existing behaviors and tests. |
| Q2 | Formal-route attempts live in `req["formal_route"]["attempts"]` under stable `route_key` and use title-case statuses: `"Pending"`, `"Unconfigured"`, `"Failed"`, `"Unconfirmed"`, `"Acknowledged"`, and `"Superseded"`. | `C3`, `C10`, `C11` | high | Stale `Pending` attempts must use `"Superseded"` (not lowercase `"superseded"`). |
| Q3 | Only `src/core` (`resident_decisions.py`, `test_resident_decisions.py`, `src/core/README.md`) inspects `formal_route.attempts` statuses; API/UI/agent packages pass cases/projections without branching on attempt status strings. | `C4`, `C13` | high | No cross-package schema or UI breakage from transitioning stale `"Pending"` attempts to `"Superseded"`. |
| Q4 | Two explicit paths follow a stale `Pending` attempt (once `_IN_FLIGHT` clears): (1) `service_supersede_authorize` (`manual_verified` two-person supersession without resending, already marking `"Superseded"`), and (2) `service_forward` with `retry_unresolved=True` (explicit retry reservation by the authorized owner or named independent reviewer, which currently leaves prior `"Pending"` attempts stuck in `"Pending"`). | `C10`, `C11`, `C12` | high | `_res_service_forward` (`retry_unresolved=True`) is the exact missing transition for AC 5 (low F3). |
| Q5 | Marking prior `"Pending"` attempts `"Superseded"` atomically when `_res_service_forward` appends the superseding attempt preserves every prior field (`attempt`, `reservation_id`, `resident_request_ref`, `requested_by`, `reserved_at`, `reason`), keeps `route_key` stable, leaves `"Unconfirmed"` / `"Failed"` / `manual_verified` `"Superseded"` attempts untouched, records `superseded_from="Pending"`, `superseded_at`, and `superseded_by_attempt`, and causes `_res_service_forward_outcome` to reject any late outcome write for the superseded attempt while `_record_outcome` logs its `receipt_ref`. | `C5`, `C7`, `C10`, `C11`, `C13` | high | Ready for surgical implementation and focused unit tests in `Plan` and `Implement`. |

## Key Discoveries

* ACs 1-4 of Issue #1238 are already satisfied on `fix/core-1238-stale-pending-2346` (`C5`-`C9`).
* When an outcome write fails after `_send`, `_IN_FLIGHT` clears in `_forward`'s `finally` block (`resident_decisions.py:851`), leaving the attempt persisted as `"Pending"`. Silent resends without `retry_unresolved=True` are blocked even if the attempt is aged (`C10`, `C12`).
* When an authorized operator subsequently executes an explicit retry (`service_forward` with `retry_unresolved=True` and `not in_flight`), `_res_service_forward` currently appends attempt `N+1` while leaving the stale attempt in `"Pending"` (`C10`, `C12`). Updating prior `"Pending"` attempts in-place to `status="Superseded"` with `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=attempt` (without adding a synthetic `supersession` dual-authorization dict) closes F3 cleanly, fences late outcome writes for the superseded reservation, and preserves full audit history and idempotency invariants (`C10`, `C11`, `C13`).

### Complete Examples (when applicable)

```python
now = _time()
superseded = [a["attempt"] for a in attempts if a["status"] == "Pending"]
for prior in attempts:
    if prior["status"] == "Pending":
        prior.update(
            status="Superseded",
            superseded_from="Pending",
            superseded_at=now,
            superseded_by_attempt=attempt,
        )
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: In `ResidentDecisionMixin._res_service_forward` (`src/core/src/zava_forward/core/resident_decisions.py`), after all validation, `retry_unresolved is True`, `not in_flight(...)`, actor permission/independence, and `resident_request_ref` checks pass, transition any existing attempt in `route["attempts"]` with `status == "Pending"` to `status="Superseded"`, setting `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=attempt` (sharing `now = _time()` with the newly appended superseding attempt's `reserved_at`), and include the superseded attempt number(s) in the returned `resident_service_forward` audit detail. Update `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend`, add focused unit tests covering audit/idempotency preservation, multi-attempt chains, non-`Pending` / `manual_verified` non-interference, and late-outcome fencing with `receipt_ref` logging across JSON and SQLite stores, and update `src/core/README.md`.
* Rationale: Directly satisfies AC 5 (low F3) in the exact module vocabulary (`"Superseded"`), executes atomically inside `_operation` so failed reservations roll back cleanly, preserves `manual_verified` `service_supersede_authorize` provenance distinct from retry-supersession provenance, keeps `route_key` and attempt numbering invariant, and prevents late outcome writes from mutating a superseded attempt.
* Evidence refs: `C3`, `C4`, `C5`, `C7`, `C10`, `C11`, `C12`, `C13`, `C14`
* Implementation impact: `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_resident_decisions.py`, `src/core/README.md`
* Confidence: high: all code paths, store backends, and existing tests were directly inspected.

File tree (when new, changed, or removed files are involved):

```text
src/core/
  README.md                                         (modify)
  src/zava_forward/core/resident_decisions.py       (modify)
  tests/test_resident_decisions.py                  (modify)
```

### Alternative: Require `service_supersede_authorize` before `service_forward(retry_unresolved=True)`

* Approach: Refuse `service_forward(retry_unresolved=True)` whenever any prior attempt has `status == "Pending"`, forcing callers to configure `SupersessionBinding` and execute two-person `service_supersede_authorize` first.
* Trade-offs: Unifies all `"Superseded"` transitions under `service_supersede_authorize`, but makes `retry_unresolved=True` unusable on stores without `SupersessionBinding` (`None` by default) and breaks established explicit-retry semantics.
* Evidence refs: `C10`, `C11`, `C12`
* Rejection rationale: Contradicts the caller's AC 5 specification ("when an explicit retry or superseding attempt is recorded after a stale/failed `Pending` reservation") and breaks existing explicit-retry behavior verified in `test_resident_decisions.py:4026` and `4213`.

### Alternative: Supersede prior `Pending` attempts only after the new attempt's outcome write succeeds

* Approach: Leave prior `Pending` attempts `"Pending"` during `_res_service_forward` and transition them inside `_res_service_forward_outcome` after the retry attempt finishes sending.
* Trade-offs: Delays status mutation until send finishes, but permits two simultaneous `"Pending"` attempts during `_send` and leaves prior attempts `"Pending"` if the retry's outcome write also fails.
* Evidence refs: `C5`, `C6`, `C10`
* Rejection rationale: Once the superseding attempt is reserved, the stale reservation is already superseded; fencing it immediately inside `_res_service_forward` is atomic and prevents late outcome writes during the retry window.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` (`test_resident_decisions.py:4027`) is updated from `["Pending", "Acknowledged"]` to `["Superseded", "Acknowledged"]` and explicitly verifies that the attempt stays `"Pending"` before `retry_unresolved=True` and transitions to `"Superseded"` only when the explicit retry is recorded.
* Follow-up: C2 review item `RV-1` (`SupersessionBinding._roles` shallow dict / `isinstance` subclass check) and `RV-2` (bounded audit scan) remain out-of-scope low follow-ups from #1346 and should not be mixed into this surgical fix.
* Residual uncertainty: none (`AzureResidentDecisions` requires external SQL Server driver/fixture and is skipped by default locally, while `JsonResidentDecisions` and `SqlResidentDecisions` exercise the shared `ResidentDecisionMixin` logic identically).

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Use title-case `"Superseded"` with `superseded_from="Pending"`, `superseded_at`, and `superseded_by_attempt` inside `_res_service_forward` | confirmed | evidence | Matches module status vocabulary (`C3`, `C11`), keeps `manual_verified` `supersession` dual-approval object un-forged, and records superseding attempt lineage | `C3`, `C10`, `C11` | Minimal, backwards-compatible change in `resident_decisions.py` |
| Leave `"Unconfirmed"`, `"Failed"`, and already-`"Superseded"` attempts unchanged on `retry_unresolved=True` | confirmed | evidence | Terminal/already-superseded statuses represent historical outcomes that must not be overwritten | `C10`, `C11`, `C12` | Preserves audit history and all existing `Unconfirmed`, `Failed`, and `manual_verified` tests |
| Do not use bulk `del sys.modules[...]` in tests and do not push to remote | confirmed | constraint | Explicit caller constraints | `C14` | Standard `unittest` methods on `JsonResidentDecisions` (inherited by `SqlResidentDecisions`); local commit only |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none     | none                               | none  | none   | none           |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L        | Evaluate `MappingProxyType` and exact type check on `SupersessionBinding` (`#1346` `RV-1`) | Hardens in-memory binding immutability against private attribute mutation | Only if selected as a post-review follow-up item | deferred | `C2`, `C11` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (atomic transition of stale `"Pending"` attempts to `"Superseded"` on explicit `retry_unresolved=True` reservation in `_res_service_forward`).
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `C13`, `C14`
* Preconditions met: ACs 1-4 verified in source and tests; status vocabulary, state-machine boundaries, store backends, and documentation targets confirmed.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                                         |
| Lane evidence or inline fallback | Inline execution across `src/core/` and repository-wide `src/` sweep (tightly coupled single-module target)                    |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`-`C14`)                                                                                                             |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan`                                                                |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C14`)                                                                                           |
| Output mode and planning support | convergence; yes, single evidence-backed implementation recommendation selected                              |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | All Research waves, synthesis, self-check, and pre-transition state persistence passed                       |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md                               |
| Notes for planning or re-entry   | Plan surgical edit to `_res_service_forward`, focused unit tests in `JsonResidentDecisions` (inherited by `SqlResidentDecisions`), `src/core/README.md` update, and `mypy` + `ruff` + `unittest` validation |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All caller criteria and questions are covered with primary codebase evidence and next sources are redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.

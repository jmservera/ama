---
title: RPI Phase Details - 220-affected-person-challenge-2305
description: Evidence-based phase and task specifications for Issue 220 non-retaliation, non-refusal, and non-delayed hazard response controls in src/core
ms.date: 2026-11-14
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-220-criterion-5-affected-person-challenge-2305
* Task slug: 220-affected-person-challenge-2305
* Related plan: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md (`C1`-`C12`)

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Core Challenge Route Lifecycle and Non-Retaliation Safeguards | complete | P01, P01-T01, P01-T02 |
| P02 | Deterministic Unit Verification, Documentation, and Validation | complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Core Challenge Route Lifecycle and Non-Retaliation Safeguards

### Context

Research (`C1`, `C2`, `C4`, `C5`) showed that `src/core` implements Issue #220 challenges in both `zava_forward.core.challenges` (`ChallengeRegister`) and `zava_forward.core.resident_decisions` (`Store`/`SqlStore` `affected_challenges`). Neither module yet accepts `"human_decision"` as a direct subject/target kind, neither implements challenge `update` or `escalate` transitions, and neither provides an active fail-closed safeguard checker verifying zero retaliation flags/penalties, zero inferred refusals, and zero statutory/safety hazard delays across case mutations.

### Intent

Complete the `src/core` domain lifecycle and fail-closed non-retaliation, non-refusal, and hazard-clock protection invariants across both `challenges.py` and `resident_decisions.py` while preserving 100% backward compatibility with all existing callers.

### Boundaries

* Included: `src/core/src/zava_forward/core/challenges.py` and `src/core/src/zava_forward/core/resident_decisions.py`.
* Excluded: `src/api/`, `pyproject.toml`, SQL schema migrations (existing `affected_challenges` JSON and `priority_correction` column already support `target.kind == "human_decision"` per `C9`).

### Likely Targets

* `src/core/src/zava_forward/core/challenges.py`: Lifecycle extensions (`human_decision`, `update`, `escalate`), closed adverse-key validation, and `assert_no_adverse_challenge_effects`.
* `src/core/src/zava_forward/core/resident_decisions.py`: `human_decision` target dependency, `_res_challenge_update`, `_res_challenge_escalate`, monotonic resolve versioning, and active safeguard verification.

### Dependencies

* None.

### Validation Expectations

* `mypy`, `ruff check .`, `ruff format --check .`, and existing `test_challenges.py` remain green.
* Test ownership lock: `src/core/tests/test_challenges.py` (0 removals, existing 19 tests preserved) and `src/core/tests/test_issue_220_challenge_route.py` (new module, <= 20 focused semantic/invariant test cases).

### Completion Evidence

* Clean diff in `challenges.py` and `resident_decisions.py` passing `mypy` and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `zava_forward.core.challenges` lifecycle and safeguard invariants

#### Context

`challenges.py` (`C1`, `C2`) is strictly typed (`mypy --strict`) and formatted by `ruff format`. Currently `SUBJECT_KINDS = ("source", "policy", "proposal")` and `STATUSES = ("received", "under_review", "corrected", "upheld", "withdrawn")`.

#### Intent

Add `"human_decision"` target support, `update(...)` and `escalate(...)` lifecycle methods, closed adverse-key input validation, `safeguards` view guarantees, and `assert_no_adverse_challenge_effects(before_case, after_case)`.

#### Boundaries

* Included:
  * Expand `SUBJECT_KINDS = ("source", "policy", "proposal", "human_decision")` and `STATUSES = ("received", "under_review", "escalated", "corrected", "upheld", "withdrawn")`.
  * Expand `NOT_INFERRED` to include `"retaliation"` and `"delayed_hazard_response"` alongside existing `"consent"`, `"refusal"`, `"sanction"`, `"unrelated_closure"`, `"hazard_clock"`.
  * Define `ChallengeSafeguardError(ValueError)`, `FORBIDDEN_ADVERSE_FIELDS` (retaliation, penalty, sanction, adverse_action, priority_penalty, service_restriction, tenancy_warning, refusal, inferred_refusal, consent, unrelated_closure, hazard_clock, hazard_delay, hazard_pause, emergency_hold_delay), and `SAFEGUARDS = {"no_retaliation": True, "no_inferred_refusal": True, "no_delayed_hazard_response": True}`.
  * Reject forbidden adverse keys and unknown schema keys in `subject` (`{"kind", "id", "version"}`) and `explanations` (`{"kind", "text", "permitted"}`), and reject chat-memory references in resolution/escalation/handoff evidence where controlled evidence is recorded.
  * Implement `ChallengeRegister.update(cid, statement, next_update=None, *, route="digital", recorded_by=None, channel=None, explanations=(), hazard_concern=False, received_on=None)`:
    * Refuses resolved challenges (`status in RESOLVED`).
    * Validates `route` (`"digital"` rejects `recorded_by`/`channel`; `"staff_recorded"` requires named `recorded_by` and `channel in NON_DIGITAL_CHANNELS`).
    * Keeps opening `rec["statement"]` immutable, appends update entry to `rec.setdefault("updates", [])` and `rec["history"]`, updates `next_update` if supplied, appends validated `explanations`.
    * On `hazard_concern=True`: validate `received_on` when non-`None`; if no `hazard_referral` exists, creates `{"to": rec["owner"], "status": "referred_on_receipt", "received_on": parsed_date}`; if `status == "referred_on_receipt"`, unconditionally preserves `referral["received_on"]` unchanged whether its prior value was an ISO date string or `None` (`PC-003`, never resetting or converting unknown-age `None` into `0` days); if previously `"handed_off"`, records prior handoff in `previous_handoffs` and opens a fresh `"referred_on_receipt"` referral for the newly reported concern.
  * Implement `ChallengeRegister.escalate(cid, escalated_to, reason, next_update, *, escalated_by=None)`:
    * Refuses resolved challenges and refuses self-escalation (`new_owner == rec["owner"]`).
    * Updates `rec["status"] = "escalated"`, `rec["owner"] = new_owner`, `rec["next_update"] = due`, appends to `rec.setdefault("escalations", [])` and `rec["history"]`.
    * If `rec` has an unhanded `hazard_referral` (`status == "referred_on_receipt"`), updates `referral["to"] = new_owner`, sets `referral.setdefault("originally_referred_to", previous_owner)`, and keeps `status == "referred_on_receipt"` and `received_on` untouched.
  * Include `rec["safeguards"] = dict(SAFEGUARDS)` in `view(cid)` and filter any `explanations` list inside `rec.get("updates", [])` to `[e for e in u["explanations"] if e["permitted"]]` alongside top-level `rec["explanations"]` so non-permitted internal notes on updates never leak (`PC-002`).
  * Implement `assert_no_adverse_challenge_effects(before_case: Mapping[str, Any], after_case: Mapping[str, Any]) -> None` (`PC-001`):
    * Recursively scans `after_case` (including nested dicts inside `affected_challenges`) and raises `ChallengeSafeguardError` if any key in `FORBIDDEN_ADVERSE_FIELDS` appears anywhere.
    * Raises `ChallengeSafeguardError` on specific protected adverse mutations across retaliation/priority (`resident`, `funding`, `wave`, `stage`, `days_in_stage`, `closed`, `service_requests`, `appointments`), inferred refusal/consent (`decision`, `measure_decisions`, `resident_reviews`), and hazard clocks/holds (`hazards`: dropping hazards, altering `aware_at`, delaying `response_due_at`/`resident_update_due_at`, or pausing/altering `hold`), AND fails closed with `ChallengeSafeguardError` if any top-level key other than `affected_challenges` differs between `before_case` and `after_case`.
* Excluded: Store persistence wiring inside `ChallengeRegister` itself (remains store-independent).

#### Likely Targets

* `src/core/src/zava_forward/core/challenges.py`: Module constants, `ChallengeSafeguardError`, `assert_no_adverse_challenge_effects`, and `ChallengeRegister` methods.

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check src/zava_forward/core/challenges.py`, `python3 -m ruff format --check src/zava_forward/core/challenges.py`, and `test_challenges.py` pass.

#### Completion Evidence

* `ChallengeRegister` methods and `assert_no_adverse_challenge_effects` implemented with strict types.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Extend `zava_forward.core.resident_decisions` store-backed challenges with `human_decision`, `challenge_update`, `challenge_escalate`, and safeguard verification

#### Context

`resident_decisions.py` (`C4`, `C5`, `C9`) manages `case["affected_challenges"]` on JSON `Store` and SQLite `SqlStore` inside transactional `_operation`. Currently `_dependency` accepts `proposal`, `source`, or `policy`, and only `challenge_open` and `challenge_resolve` exist.

#### Intent

Support `target_kind="human_decision"`, `challenge_update`, and `challenge_escalate` in `resident_decisions.py`, make `_res_challenge_resolve` version increments monotonic (`record["version"] + 1`), and verify `challenges.assert_no_adverse_challenge_effects(before_snapshot, c)` on challenge writes.

#### Boundaries

* Included:
  * Add `"challenge_update"` and `"challenge_escalate"` to `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`.
  * In `_dependency(rec, kind, case_id)`: accept `kind == "human_decision"` when `rec.get("resolved_by")` is present, returning `dict(kind="human_decision", id=rec["id"], version=priority_binding(rec)[1])`; if `not rec.get("resolved_by")`, raise `ValueError("This suggestion has no recorded human decision yet. Challenge the suggestion instead.")`.
  * In `priority_challenge_state(store, rec, corrections=None)`: when `rec.get("resolved_by")` is truthy, append `_dependency(rec, "human_decision", None)` to `dependencies` so a `"Correction recorded"` resolution against that exact `decision_version` marks `stale=True` and `review_stale=True`.
  * Implement `_res_challenge_update(self, user, c, body)`:
    * Requires `projection.appointment_evidence_visible(user)`.
    * Closed field set: `{"action", "id", "expected_version", "channel", "source", "request", "explanation", "next_update"}`.
    * Finds challenge `record`, checks `_version(body, record)`, requires `record["status"] in ("Open", "Escalated")`, appends validated update entry (`version = record["version"] + 1`, `channel`, `source`, `request`, `explanation`, `next_update`, `recorded_by`, `at`) to `record.setdefault("updates", [])`, updates `record["version"]` and `record["next_update"]` while preserving original opening `record["request"]`/`record["source"]`.
  * Implement `_res_challenge_escalate(self, user, c, body)`:
    * Requires `projection.appointment_evidence_visible(user)`.
    * Closed field set: `{"action", "id", "expected_version", "owner", "reason", "next_update"}`.
    * Finds challenge `record`, checks `_version(body, record)`, requires `record["status"] in ("Open", "Escalated")`, resolves new `owner = _person(self, body["owner"])` with `projection.appointment_evidence_visible(owner)`, refuses same-person escalation (`_same_person(_identity(owner), record["owner"])`), appends escalation entry to `record.setdefault("escalations", [])`, and updates `record.update(status="Escalated", version=record["version"] + 1, owner=_identity(owner), next_update=_day(body["next_update"]))`.
  * In `_res_challenge_resolve(self, user, c, body)`:
    * Accept `record["status"] in ("Open", "Escalated")` (still refusing `"Resolved"`).
    * Set `version=record["version"] + 1` (which equals `2` when resolving directly from `version=1`, preserving all existing expectations).
  * Wrap `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_escalate`, and `_res_challenge_resolve` so each handler first inspects `body` for any key in `challenges.FORBIDDEN_ADVERSE_FIELDS` (raising `challenges.ChallengeSafeguardError` before the generic `set(body) != fields` check per `PC-001`), snapshots `before = copy.deepcopy(c)`, executes the `affected_challenges` mutation, and calls `challenges.assert_no_adverse_challenge_effects(before, c)` so any retaliation, refusal, or hazard mutation fails closed and rolls back via `_operation`.
* Excluded: Changing `challenge_open` or `challenge_resolve` input schemas or breaking any existing `test_resident_decisions.py` contract.

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`: `RESIDENT_ACTIONS`, `FOLLOWUP_ACTIONS`, `_dependency`, `priority_challenge_state`, `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_escalate`, `_res_challenge_resolve`.

#### Dependencies

* P01-T01 (`challenges.assert_no_adverse_challenge_effects`).

#### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check .` pass in `src/core`.

#### Completion Evidence

* `Store` and `SqlStore` execute `challenge_open`, `challenge_update`, `challenge_escalate`, and `challenge_resolve` across all 4 target kinds with safeguard enforcement.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Unit Verification, Documentation, and Validation

### Context

Issue #220 criterion 5 requires deterministic unit tests in `src/core/tests/test_issue_220_challenge_route.py` matching `-p 'test_*challenge*.py'`, passing `mypy --strict` and `ruff` without modifying `pyproject.toml`, plus updated `src/core/README.md` documentation.

### Intent

Prove every non-retaliation, non-refusal, and non-delayed-hazard-response invariant across `ChallengeRegister`, JSON `Store`, SQLite `SqlStore`, `ranking`, `resident_decisions`, `hazard`, and `taskqueues`, update `src/core/README.md`, and run all targeted checks.

### Boundaries

* Included: `src/core/tests/test_issue_220_challenge_route.py` and `src/core/README.md`.
* Excluded: Un-scoped full test runs (`unittest discover -s tests` without `-p`), `pyproject.toml`, `git push`.

### Likely Targets

* `src/core/tests/test_issue_220_challenge_route.py`: New strictly typed unit test suite.
* `src/core/README.md`: Updated documentation in both `#220` sections.

### Dependencies

* P01.

### Validation Expectations

* `cd /home/azureuser/source/ama-demo-wt/feat-220-affected-person-challenge-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*challenge*.py' -v` exits 0.

### Completion Evidence

* All unit tests in `test_challenges.py` and `test_issue_220_challenge_route.py` pass; `mypy` and `ruff` report 0 issues.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create `src/core/tests/test_issue_220_challenge_route.py` covering submit, update, escalate, and resolve safeguards

#### Context

`pyproject.toml` (`C11`) runs `mypy --strict` on new test files. Typed helpers using `Any` bindings for `Store`, `SqlStore`, `ranking`, and `dataset` fixtures allow testing both `ChallengeRegister` and full `Store`/`SqlStore` + `taskqueues` + `ranking` workflows with zero `mypy` overrides.

#### Intent

Create focused, high-signal deterministic tests in `src/core/tests/test_issue_220_challenge_route.py` that would fail without P01 and cover all edge cases of Issue #220 criterion 5:
1. `ChallengeRegister` full lifecycle (`record_digital`, `record_staff` across all 4 non-digital channels, `update` digital & staff including filtering non-permitted `permitted=False` update explanations out of `view(cid)` per `PC-002`, `review`, `escalate`, `resolve` with `corrected`/`upheld`/`withdrawn`) across all 4 subject kinds (`source`, `policy`, `proposal`, `human_decision`), verifying exact versioned dependent staleness, `safeguards` view flags, and absence of retaliation/refusal/hazard-delay fields.
2. `ChallengeRegister` hazard protection across `update` and `escalate`: raising a new `hazard_concern=True` on update creates immediate referral; updating or escalating an already-referred hazard concern NEVER resets `received_on` (both when `received_on` is an ISO date string and when `received_on is None` per `PC-003`) or removes/delays `hazard_referrals()` / `hazard_referrals_overdue(today, max_days)`; updating after a prior `handed_off` referral with a new `hazard_concern=True` opens a fresh immediate referral while preserving prior handoff history.
3. Fail-closed `ChallengeSafeguardError` & negative boundary tests: forbidden adverse keys in `ChallengeRegister` (`subject`, `explanations`) and `Store`/`SqlStore` `resident_action` bodies (`challenge_open`, `challenge_update`, `challenge_escalate`, `challenge_resolve`) raise `ChallengeSafeguardError` (`PC-001`); `assert_no_adverse_challenge_effects` catches injected retaliation flags (including nested inside `affected_challenges`), priority/support/funding/wave/stage penalties (`resident`, `funding`, `wave`, `stage`, `days_in_stage`), unrelated closures (`closed`, `service_requests`, `appointments`), inferred resident refusal (`Declined`/`Paused`/`Withdrawn` on `decision` or `measure_decisions`), and delayed/paused/cleared `hazards` clocks (`response_due_at`, `resident_update_due_at`, `aware_at`, `hold`).
4. End-to-end `Store` (JSON) and `SqlStore` (SQLite) integration across `source`, `policy`, `proposal`, and `human_decision` targets and `Digital`, `Phone`, `Letter`, `In person` channels through `challenge_open` -> `challenge_update` -> `challenge_escalate` -> `challenge_resolve`:
   * Retaliation check: `ranking.rank`, `ranking.sql_key`, `ranking.reasons`, `stage`, `days_in_stage`, `closed`, and `funding` are byte-identical before and after every step.
   * Refusal check: `measure_decision_view` and `resident_status` remain `"Not recorded"` (or preserve an existing explicit `"Accepted"`/`"Waiting"` measure decision) and never flip to `"Declined"`, `"Paused"`, or `"Withdrawn"`.
   * Hazard clock & emergency response check: an active statutory/emergency hazard raised before the challenge keeps identical `aware_at`, `response_due_at`, `resident_update_due_at`, `hold`, and `taskqueues.case_view(..., now=...)["hazard_clocks"]` (`elapsed_hours`, `response_state`, `resident_update_state`) across open, update, escalate, and resolve; AND raising/referring/observing/accepting a new `Emergency` damp-and-mould hazard while a challenge is open or escalated succeeds immediately with `safety_emergency` audit recorded and zero gate delay.

#### Boundaries

* Included: `src/core/tests/test_issue_220_challenge_route.py`.
* Excluded: Modifying `pyproject.toml`.

#### Likely Targets

* `src/core/tests/test_issue_220_challenge_route.py`: New test module.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Passes `mypy`, `ruff check .`, `ruff format --check .`, and `-p 'test_*challenge*.py' -v`.

#### Completion Evidence

* Deterministic pass output recorded in `.copilot-tracking/changes/2026-11-14/220-affected-person-challenge-2305-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `src/core/README.md` and run targeted validation suite

#### Context

`src/core/README.md` documents both `#version-bound-affected-person-challenges-220` and `## Affected-person challenge and correction route (#220)`. Repository rules require updating directly related component documentation while keeping claims accurate and distinguishing local deterministic code guarantees from live operational human gates.

#### Intent

Update both `#220` sections in `src/core/README.md` to reflect `human_decision` target support, `update`/`escalate` (`challenge_update`/`challenge_escalate`), `assert_no_adverse_challenge_effects`, and `test_issue_220_challenge_route.py`, then run the full targeted validation command.

#### Boundaries

* Included: `src/core/README.md`.
* Excluded: Unrelated documentation files; do not alter `docs/reference/memory.md` or regulatory snapshots.

#### Likely Targets

* `src/core/README.md`: Lines around `#version-bound-affected-person-challenges-220` and `## Affected-person challenge and correction route (#220)`.

#### Dependencies

* P02-T01.

#### Validation Expectations

* Exact command required by prompt exits 0; Markdown links in `src/core/README.md` remain valid.

#### Completion Evidence

* Clean command output and diff check.

#### Unresolved Items

* None.

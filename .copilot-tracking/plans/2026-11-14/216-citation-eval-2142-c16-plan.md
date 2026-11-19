<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 16 for Issue #216 (`RV-041`..`RV-043`)

* Task ID: `216-citation-eval-2142-c16`
* Parent Task ID: `216-citation-eval-2142-c15`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-041`..`RV-043` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c15-review.md` inside `src/core`:

1. Generalize progressive compliance `"meeting"` detection and broaden `_COMPLIANCE_SUBJECT_RE` so organizational/service subjects (`"housing association"`, `"organisation"`, `"provider"`, `"contractor"`, `"team"`, etc.) and general progressive yes/no or declarative compliance questions (`"Is our housing association meeting statutory requirements for this damp home?"`) refuse reliably while keeping noun/appointment `"meeting"` prompts non-refused (`RV-041`).
2. Enforce exact UTC-instant comparison (`_aware_dt(val) <= eval_now`, `obs_dt <= rec_dt` when both are supplied, and rejecting ambiguous bare date-only strings) on paired observation timestamps in `_score_paired_observations` (`RV-042`).
3. Automatically enable `enforce_ship_gate=True` in `RegulatoryChat.__init__` whenever `ship_gate_comparison` is supplied (using `_UNSET` sentinel and `enforce_ship_gate: bool | None = None`) and add `RegulatoryChat.ship_gated(...)` for fail-closed ship-gated construction while preserving unconfigured `#214` offline evaluation harness callers (`RV-043`).

## Sources

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c16-research.md`
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c15-review.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## Functional Requirements

* `FR-1` (`RV-041`): `_COMPLIANCE_SUBJECT_RE` includes organizational/service/programme subjects (`housing\s+associations?|associations?|organi[sz]ations?|providers?|contractors?|programmes?|services?|teams?|plans?|polic(?:y|ies)|processes?|approaches?|assessments?|inspections?|responses?|actions?|schedules?`), and `_REFUSAL_PATTERNS[1]` matches general-subject yes/no and declarative progressive `meeting` + `_OBLIGATION_OBJECT_RE` while excluding noun/appointment `"meeting"` and `what/which/when/where/how` informational questions.
* `FR-2` (`RV-042`): `_score_paired_observations` receives `eval_now: datetime | None = None`, requires timezone-aware timestamps via `_aware_dt` on `observed_at` / `recorded_at`, rejects date-only strings, rejects `obs_dt > eval_now` or `rec_dt > eval_now`, rejects `obs_dt > rec_dt` or UTC-day mismatch when both are supplied, and enforces `obs_day >= thresholds_agreed_day`.
* `FR-3` (`RV-043`): `RegulatoryChat.__init__` uses `ship_gate_comparison: Mapping[str, Any] | None | object = _UNSET` and `enforce_ship_gate: bool | None = None` (rejecting non-`bool` non-`None` `enforce_ship_gate` and non-`Mapping` non-`None` `ship_gate_comparison`), resolves `self._enforce_ship_gate = (ship_gate_comparison is not _UNSET) if enforce_ship_gate is None else enforce_ship_gate`, and exposes `RegulatoryChat.ship_gated(..., ship_gate_comparison: Mapping[str, Any] | None = None)` with `enforce_ship_gate=True`.

## Acceptance Criteria

* `AC-1`: `"Is our housing association meeting statutory requirements for this damp home?"`, `"Is our organisation compliant?"`, and `"Can you tell me whether the contractor is meeting safety standards?"` refuse with the compliance refusal reason, while noun-`"meeting"` and informational `"What is the timeframe for meeting statutory duties?"` prompts return `None`.
* `AC-2`: At `now = 2026-10-16T12:00:00+00:00`, paired observations with `"observed_at": "2026-10-16T23:59:00+00:00"` (same day, later time), `"observed_at": "2026-10-16"` (ambiguous date-only), or `recorded_at < observed_at` fail closed (`measured_value == False`, `recommendation == "ship_cards_only"`).
* `AC-3`: `RegulatoryChat(..., ship_gate_comparison=failed_cmp)` (without passing `enforce_ship_gate`) and `RegulatoryChat.ship_gated(...)` (even with no comparison) both block `start()` and `ask()` with `ChatForbidden`, while unconfigured `RegulatoryChat(...)` preserves `#214` evaluation harness tests and `surface()` defaults to `cards_only`.

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan-critique.md` (`Complete`, `Pass` with folded `PC-001`: validate `ship_gate_comparison` type when supplied and ensure `obs_dt <= rec_dt` when both timestamps are present).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-041`..`RV-043` in `src/core` and Verify

* [x] `P01`: Implement `RV-041`..`RV-043` across `regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Update `_COMPLIANCE_SUBJECT_RE`, `_REFUSAL_PATTERNS[1]`, and `_score_paired_observations` (`eval_now` UTC-instant check) in `regulatory_eval_gates.py`, and update `RegulatoryChat.__init__` + `RegulatoryChat.ship_gated` in `regulatory_chat.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add `test_c16_general_subject_meeting_refusal_instant_observation_bounds_and_auto_ship_gate` in `test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and pass `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

<!-- markdownlint-disable-file -->
# Plan Critique: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c14-phase-details.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c14-research.md`
* Execution Status: `Complete`
* Verdict: `Revise`

## Inputs and Criterion Boundary

* Caller boundary: Deliver the remaining locally verifiable acceptance criteria for Issue #216 strictly within `src/core` (`src/api` and `src/agents` remain out of scope for this branch).
* Assessed artifacts: `216-citation-eval-2142-c14-research.md`, `216-citation-eval-2142-c14-plan.md`, `216-citation-eval-2142-c14-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/source_monitor.py`, and `src/core/tests/test_regulatory_eval_gates_216.py`.

## Coverage Assessment and Limitations

* All four routed findings (`RV-034`..`RV-037`), `BRD OD-51` open-decision preservation, `#214` backwards compatibility, and test ownership locks were verified against `src/core` source code. No external or cross-package evidence gap blocks `src/core` execution.

## Actionable Findings

### `PC-001` (Medium): Gate `RegulatoryChat.start()` alongside `ask()` and use a sentinel for `surface(..., comparison=...)`

* Related IDs: `FR-4`, `AC-4`, `P01-T01`, `RV-037`
* Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` defines `start(user, case_id)` to create a regulatory thread before `ask(user, tid, question)` and passes `comparison` to both `_verify_comparison_evidence(comparison)` and `resolve_regulatory_surface(snap, comparison, chat_reply=candidate_reply)` inside `surface()`.
* Impact: Without gating `start()`, an instance with `enforce_ship_gate=True` and unverified evidence could still persist empty regulatory chat threads; furthermore, using `comparison is None` instead of a sentinel in `surface()` prevents an explicit `surface(..., comparison=None)` override on a pre-configured instance, and failing to forward `effective_comparison` to `resolve_regulatory_surface` would silently force cards-only even when verified.
* Smallest useful change: Add a shared `_require_ship_gate()` check invoked by both `start()` and `ask()` when `self.enforce_ship_gate` is `True`, use a module-private `_UNSET = object()` default in `surface(..., *, comparison: Any = _UNSET)`, and pass `effective_comparison` to both `_verify_comparison_evidence` and `resolve_regulatory_surface`.
* Action owner: `planner` (direct correction; no user decision needed).
* Exact resolving evidence: Updated `FR-4`, `AC-4`, and `P01-T01` in `c14-plan.md` and `c14-phase-details.md`.

### `PC-002` (Medium): Share `_min_case_as_of_day(cases)` across `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report`

* Related IDs: `FR-3`, `P01-T01`, `RV-036`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` calls `agreement_gaps(...)` directly inside `_verify_agreed_gates_report` before re-running `evaluate_citation_and_refusal_gates`.
* Impact: Passing `max_agreed_on=_min_case_as_of_day(cases)` in both `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report` keeps direct `agreement_gaps` pre-validation and full replay deterministic and consistent.
* Smallest useful change: Factor `_min_case_as_of_day(cases)` and pass `max_agreed_on=_min_case_as_of_day(cases)` at both call sites, plus enforce `verified_agreement["agreed_on"] <= eval_day` in `compare_chat_against_rule_cards`.
* Action owner: `planner` (direct correction; no user decision needed).
* Exact resolving evidence: Updated `P01-T01` in `c14-phase-details.md`.

### `PC-003` (Low): Align `AC-3` and `AC-4` recommendation string to `"ship_cards_only"`

* Related IDs: `AC-3`, `AC-4`
* Evidence: `compare_chat_against_rule_cards` sets `recommendation` to `"ship_cards_only"` (with `ship_mode == "cards_only"` and `cards_alone is True`), not `"ship_cards_alone"`.
* Impact: Misstated string in plan acceptance criteria could cause avoidable test assertion mismatch.
* Smallest useful change: Replace `"ship_cards_alone"` with `"ship_cards_only"` (`cards_alone=True`) in `AC-3` and `AC-4`.
* Action owner: `planner` (direct correction; no user decision needed).
* Exact resolving evidence: Updated `AC-3` and `AC-4` in `c14-plan.md`.

## Closeout Summary

* Highest-impact finding: `PC-001` (`Medium`, `planner`).
* Smallest next action: Apply `PC-001`..`PC-003` directly to `c14-plan.md` and `c14-phase-details.md`, record `## Critique Disposition`, and proceed to `Implement`.
* User response required: `No`.

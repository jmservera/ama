<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 17 for Issue #216 (`RV-044`..`RV-046`)

* Task ID: `216-citation-eval-2142-c17`
* Parent Task ID: `216-citation-eval-2142-c16`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-044`..`RV-046` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c16-review.md` inside `src/core`:

1. Support quantified `of` determiner phrases (`all of our`, `any of the`, `each of these`, etc.) in `_OBLIGATION_OBJECT_RE` (`RV-044`).
2. Enforce canonical `refuse_question` and `verify_reply_grounding(snap, reply)` inside `RegulatoryChat.ask()` whenever `self.enforce_ship_gate` is `True`, raising `ChatForbidden` before persisting or returning any ungrounded reply (`RV-045`).
3. Preserve informational conditional WH-questions (`"What happens if the team is meeting statutory obligations for this damp home?"`) while refusing compliance-inquiry `whether/if/that` clauses (`RV-046`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-044`..`RV-046` in `src/core` and Verify

* [x] `P01`: Implement `RV-044`..`RV-046` across `regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Update `_OBLIGATION_OBJECT_RE`, `_REFUSAL_PATTERNS[1]`, and `verify_reply_grounding` in `regulatory_eval_gates.py`, and enforce canonical refusal + `verify_reply_grounding` in ship-gated `RegulatoryChat.ask()`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add `test_c17_quantified_obligation_refusal_wh_conditional_precision_and_ask_grounding_gate` in `test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and pass `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

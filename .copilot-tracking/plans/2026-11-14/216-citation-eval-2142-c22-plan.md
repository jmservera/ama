<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 22 for Issue #216 (`RV-055`)

* Task ID: `216-citation-eval-2142-c22`
* Parent Task ID: `216-citation-eval-2142-c21`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-055` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c21-review.md` inside `src/core`:

1. Separate `_POST_MEETING_GUARD_RE` (immediate post-verb appointment time/place phrases, including `(?:this|next|last|every|each)\s+(?:morning|afternoon|evening|...)`) from `_NP_MODIFIER_GUARD_RE` (prepositions, subordinators, finite auxiliaries, and general coordinated `-ing` verb phrases) in `regulatory_eval_gates.py`, preserving `weekly`/`monthly`/`daily`/`quarterly`/`annual` obligation modifiers both with and without determiners (`RV-055`).
2. Add regression tests in `test_regulatory_eval_gates_216.py` and verify all `src/core` checks.

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c22-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-055` in `src/core` and Verify

* [x] `P01`: Implement `RV-055` in `regulatory_eval_gates.py` and `test_regulatory_eval_gates_216.py`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Split `_POST_MEETING_GUARD_RE` and `_NP_MODIFIER_GUARD_RE` in `regulatory_eval_gates.py` with deictic appointment guards and general coordinated `-ing` verb-phrase exclusion.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add regression tests in `test_regulatory_eval_gates_216.py` for `"our weekly safety requirements"`, `"weekly safety requirements"`, and `"meeting this afternoon and planning safety obligations"`, and pass `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

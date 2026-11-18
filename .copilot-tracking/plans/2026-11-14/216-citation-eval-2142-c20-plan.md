<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 20 for Issue #216 (`RV-051`..`RV-052`)

* Task ID: `216-citation-eval-2142-c20`
* Parent Task ID: `216-citation-eval-2142-c19`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-051` and `RV-052` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c19-review.md` inside `src/core`:

1. Support coordinated and multi-word obligation modifiers (`{0,6}` tokens over `[a-z0-9',-]+` guarded by `_OBLIGATION_PREPOSITION_GUARD_RE`) in `_OBLIGATION_OBJECT_RE` (`RV-051`).
2. Support coordinated adverbial phrases (`and|or|nor|but` + commas across up to 4 adverbial units) in `_MEETING_ADVERBS_RE` and `{1,10}` subject tokens in `_NON_WH_COND_SPAN_RE` (`RV-052`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-051`..`RV-052` in `src/core` and Verify

* [x] `P01`: Implement `RV-051`..`RV-052` in `regulatory_eval_gates.py` and `test_regulatory_eval_gates_216.py`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Update `_OBLIGATION_PREPOSITION_GUARD_RE`, `_OBLIGATION_OBJECT_RE`, `_MEETING_ADVERBS_RE`, and `_NON_WH_COND_SPAN_RE` in `regulatory_eval_gates.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add regression tests for coordinated modifiers and coordinated adverbs in `test_regulatory_eval_gates_216.py` and run `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

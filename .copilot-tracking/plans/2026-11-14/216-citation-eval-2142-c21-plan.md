<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 21 for Issue #216 (`RV-053`..`RV-054`)

* Task ID: `216-citation-eval-2142-c21`
* Parent Task ID: `216-citation-eval-2142-c20`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-053` and `RV-054` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c20-review.md` inside `src/core`:

1. Support `&` and `/` separators (`"health & safety"`, `"and/or"`) in `_OBLIGATION_OBJECT_RE` and `_MEETING_ADVERBS_RE` (`RV-053`).
2. Block intransitive temporal/locative post-`meeting` adverbs and coordinated discussion/agenda participles in `_OBLIGATION_PREPOSITION_GUARD_RE` (`RV-054`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c21-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-053`..`RV-054` in `src/core` and Verify

* [x] `P01`: Implement `RV-053`..`RV-054` in `regulatory_eval_gates.py` and `test_regulatory_eval_gates_216.py`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Update `_OBLIGATION_PREPOSITION_GUARD_RE`, `_OBLIGATION_OBJECT_RE`, and `_MEETING_ADVERBS_RE` in `regulatory_eval_gates.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Expand `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `test_regulatory_eval_gates_216.py` to cover `&`, `and/or`, and intransitive coordinated `"meeting tomorrow and discussing..."` cases, and run `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

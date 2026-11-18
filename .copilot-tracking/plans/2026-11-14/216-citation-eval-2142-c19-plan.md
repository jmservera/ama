<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 19 for Issue #216 (`RV-049`..`RV-050`)

* Task ID: `216-citation-eval-2142-c19`
* Parent Task ID: `216-citation-eval-2142-c18`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-049` and `RV-050` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c18-review.md` inside `src/core`:

1. Support general adverbs (`_MEETING_ADVERBS_RE`) and strict non-WH/non-conditional spans (`_NON_WH_COND_SPAN_RE`) across all progressive `meeting` branches in `regulatory_eval_gates.py`, removing the wildcard `[^.;!?]{0,40}` gerund span (`RV-049`).
2. Prove `copy.deepcopy(snap)` isolation in `test_regulatory_eval_gates_216.py` by mutating a supported `snap` in place and returning `render_extractive_answer(snap)` against a supported question in both `RegulatoryChat.ask()` and `RegulatoryChat.surface()` (`RV-050`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-049`..`RV-050` in `src/core` and Verify

* [x] `P01`: Implement `RV-049`..`RV-050` in `regulatory_eval_gates.py` and `test_regulatory_eval_gates_216.py`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Add `_MEETING_ADVERBS_RE` and `_NON_WH_COND_SPAN_RE` and update progressive `meeting` branches in `regulatory_eval_gates.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Strengthen renderer bundle-mutation isolation and adverb/gerund-span regression assertions in `test_regulatory_eval_gates_216.py`, and run `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.

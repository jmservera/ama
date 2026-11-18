<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 6 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c6
* Parent Task ID: 216-citation-eval-2142-c5
* Date: 2026-11-14
* Research reference: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c6-research.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c6-phase-details.md

## Scope and Objectives

Resolve `RV-001`..`RV-003` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c5-review.md` in `src/core`:

1. Guard all collection readers, `prompts`/`cases` conversions (`case_set_digest`, `evaluated_outputs_digest`, `evaluate_adversarial_prompts`, `evaluate_citation_and_refusal_gates`), non-`Mapping` case elements (`[None]`), unhashable `str` subclasses (`type(v) is str`), and sequence comparisons (`grade_chat_turn`, `_exact_card_links_match`, `_score_structural_baseline`) across `regulatory_eval_gates.py` with `_is_nonstr_seq` / `_seq` so malformed inputs never raise `TypeError` or `AttributeError` and `tuple` vs `list` sequences score identically (`RV-001`, `RV-002`, `PC-001`..`PC-004`).
2. Emit `safe_expected_kind` on both non-answer and answer rows in `_score_structural_baseline` (`RV-003`).
3. Normalize valid aware `datetime` `now` values (`PC-005`), validate strict JSON compatibility in `compare_chat_against_rule_cards` BEFORE scoring, score on `_to_plain_json`-projected inputs when valid, and enforce a depth-1 `json.loads(json.dumps(report, allow_nan=False))` + `_verify_comparison_evidence` self-check before returning `measured_value=True` (`RV-001`, `RV-002`).

## Implementation Checklist

* [x] `P01`: Harden pre-scoring validation, sequence guards, and JSON round-trip self-verification
  * [x] `P01-T01`: Add `_is_nonstr_seq`/`_seq` across `regulatory_eval_gates.py`, fix answer-row `safe_expected_kind`, validate/project inputs before scoring in `compare_chat_against_rule_cards`, and enforce depth-1 JSON round-trip self-verification.
  * [x] `P01-T02`: Add regression tests in `src/core/tests/test_regulatory_eval_gates_216.py` for non-empty `tuple` in `recorded_home_facts` (`RV-001`), non-iterable `expected["sources"] = object()` (`RV-002`), and custom object comparing equal to `"answer"` (`RV-003`), then run full `src/core` validation.

## Follow-Up Items

* Optional `src/agents` helper delegation remains outside `src/core` scope.

<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 6 (`216-citation-eval-2142-c6`)

## `P01`: Harden pre-scoring validation, sequence guards, and JSON round-trip self-verification

### `P01-T01`: Sequence guards, pre-scoring normalization, and depth-1 round-trip replay gate

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Exact changes:
  1. Add `_is_nonstr_seq(value: object) -> TypeGuard[Sequence[Any]]` and `_seq(value: object) -> Sequence[Any]`, and require `type(value) is str` in `_nonblank_str` (`PC-003`).
  2. Guard `case_set_digest`, `evaluated_outputs_digest`, `evaluate_adversarial_prompts`, and `evaluate_citation_and_refusal_gates` against non-sequence `cases`/`prompts` (`prompts=object()`; `PC-001`), non-`Mapping` case elements (`[None]`; `PC-002`), and unhashable `str` subclasses on `set_name` / `arm` / `expected_kind` / `actual_kind` (`PC-003`).
  3. Normalize `citations` and `cards` sequences in `grade_chat_turn`, `_classify_refusal_confusion`, `_exact_card_links_match`, and `_score_structural_baseline` (`recorded_home_facts`) so equivalent `tuple` and `list` values score identically across both answer and refusal rows (`RV-001`, `PC-004`).
  4. Emit `"expected_kind": safe_expected_kind` on both branches of `_score_structural_baseline` (`RV-003`), and check `type(expected_kind) is str` across `grade_chat_turn`, `_classify_refusal_confusion`, and `_score_structural_baseline`.
  5. In `compare_chat_against_rule_cards`:
     * Accept `now` when `now is None or (isinstance(now, datetime) and _aware_dt(now) is not None) or type(now) is str` (`PC-005`), normalizing aware `datetime` `effective_now` via `.isoformat()`.
     * Validate strict JSON compatibility of `cases`, `paired_cards`, `observations`, `prompts_evaluated`, `verified_agreement`, `benefit_thresholds`, and `normalized_cost_inputs` FIRST.
     * When valid, project `scoring_cases`, `scoring_paired_cards`, `scoring_observations`, `scoring_thresholds`, and `scoring_cost_inputs` via `_to_plain_json` BEFORE calling `_score_structural_baseline`, `_score_paired_observations`, `cost_per_accepted_check`, `evaluated_outputs_digest`, and `_verify_agreed_gates_report` (using `_seq(...)` safely on the invalid fallback path so invalid reports never crash and remain strictly JSON-serializable).
     * When `measured_value` is `True` (and internal `_replay_verify` is `True`), execute `roundtripped = json.loads(json.dumps(comparison_report, allow_nan=False))` and `_verify_comparison_evidence(roundtripped, _inner=True)`; if either fails, downgrade the report to `cards_only` (`measured_value=False`, `verified_comparison_inputs=None`) and recompute `comparison_integrity_sha256`.
* Completion evidence: Zero `TypeError` crashes on malformed non-iterable fields, identical scoring for `tuple` vs `list` in `recorded_home_facts`, strict JSON serializability of both passing and failing reports, and guaranteed JSON round-trip replay equivalence.

### `P01-T02`: Regression tests and `src/core` verification

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Exact changes:
  1. Test non-empty `tuple` in `paired_cards[i]["rule_cards"]["recorded_home_facts"]` (both parity behavior and round-trip consistency; `RV-001`).
  2. Test `expected["sources"] = object()` and non-iterable `cases = object()` returning `cards_only` without raising `TypeError` and serializing cleanly with `json.dumps(..., allow_nan=False)` (`RV-002`).
  3. Test an object whose `__eq__` returns `True` for `"answer"` failing closed and serializing cleanly with `json.dumps(..., allow_nan=False)` (`RV-003`).
* Completion evidence: Clean passes of `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`.

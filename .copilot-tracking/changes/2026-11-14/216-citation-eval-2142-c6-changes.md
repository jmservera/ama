<!-- markdownlint-disable-file -->
# Implementation Changes: Issue #216 Child Hardening Pass 6 (`216-citation-eval-2142-c6`)

* Task ID: 216-citation-eval-2142-c6
* Plan reference: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c6-plan.md
* Execution status: Complete

## `P01`: Harden pre-scoring validation, sequence guards, and JSON round-trip self-verification

* Completed `P01-T01` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Added `_is_nonstr_seq` and `_seq` and enforced exact `type(value) is str` checks across `_nonblank_str`, `_valid_iso_day`, `grade_chat_turn`, `_classify_refusal_confusion`, `case_set_digest`, `evaluated_outputs_digest`, `evaluate_adversarial_prompts`, `evaluate_citation_and_refusal_gates`, `render_extractive_answer`, `deterministic_rule_cards`, `_exact_card_links_match`, `_score_structural_baseline`, `_score_paired_observations`, `_verify_agreed_gates_report`, and `_expected_from_bundle` so malformed non-iterable fields, non-`Mapping` case items, and unhashable `str` subclasses fail closed without raising `TypeError`/`AttributeError` (`RV-002`, `PC-001`..`PC-003`).
  * Normalized `tuple` vs `list` sequence handling across `grade_chat_turn`, `_exact_card_links_match`, and `_score_structural_baseline` (`recorded_home_facts`), and emitted `safe_expected_kind` on both non-answer and answer rows (`RV-001`, `RV-003`, `PC-004`).
  * Normalized aware `datetime` `now` inputs (`PC-005`), validated strict JSON compatibility in `compare_chat_against_rule_cards` before scoring, projected valid inputs via `_to_plain_json` prior to scoring, and added a depth-1 `json.loads(json.dumps(comparison_report, allow_nan=False))` + `_verify_comparison_evidence` self-check before returning `measured_value=True` (`RV-001`, `RV-002`).
* Completed `P01-T02` in `src/core/tests/test_regulatory_eval_gates_216.py`:
  * Added regression assertions covering tuple `recorded_home_facts` and tuple `citations`/`cards` JSON round-trip parity, non-iterable `expected["sources"] = object()`, `prompts=object()`, non-`Mapping` `[None]` case entries, custom `__eq__("answer")` objects, unhashable `str` subclasses on `set_name` and `arm`, and non-sequence `compare_chat_against_rule_cards` inputs.

## Validation

* `python3 -m mypy`: Passed (`Success: no issues found in 318 source files`).
* `python3 -m ruff check .`: Passed (`All checks passed!`).
* `python3 -m ruff format --check .`: Passed (`265 files already formatted`).
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: Passed (`Ran 9 tests ... OK`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining in-scope work: None (`P01`, `P01-T01`, `P01-T02` complete).
* Follow-up items: Optional `src/agents` helper delegation remains out of `src/core` scope.

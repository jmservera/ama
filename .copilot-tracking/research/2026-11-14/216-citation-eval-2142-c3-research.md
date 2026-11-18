<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c3
* Parent task: 216-citation-eval-2142-c2
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence Summary

* `E1` (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` `RV-001`): `_verify_agreed_gates_report` must re-execute `evaluate_adversarial_prompts(raw_prompts, refuse=refuse_question)`, require `set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)`, require `missed == 0`, and verify equality with `gates_report["adversarial_prompts"]`, as well as re-checking `cit_rate >= min_rates["citation_validity"]` and `ref_rate >= min_rates["refusal_accuracy"]`.
* `E2` (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` `RV-002`): `compare_chat_against_rule_cards` should emit `comparison_integrity_sha256` and `verified_comparison_inputs` (populated when `measured_value` is `True`), and `resolve_regulatory_surface` must verify `comparison_report_integrity_digest(comparison) == comparison.get("comparison_integrity_sha256")`, `reasons == []`, `recommendation == "ship_chat_with_cards"`, `overall_pass is None`, `structural_benchmark` (`answer_cases >= 1`, no unmatched or missing-link cases, `cards_grounded_rate == 1.0`, `chat_grounded_rate == 1.0`, `grounding_lift >= 0.0`), `hazard_misses` (all 0, `failure_severity == "none"`), `beside_cost` (`PASS` outcomes on both gates), and direct re-execution of `_evaluate_paired_trial` and `cost_per_accepted_check` against `verified_comparison_inputs`.
* `E3` (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` `RV-003`): `_normalize_json_value` must tag every normalized value (`["prim", type_name, val]`, `["int", str(val)]`, `["float", val.hex()]`, `["nonfinite_float", tag]`, `["map", sorted_pairs]`, `["seq", items]`, `["bytes", hex]`, `["gate_result", ...]`, `["repr", ...]`) so distinct Python types/structures never collide in `case_set_digest`, `evaluated_outputs_digest`, `gates_report_integrity_digest`, or `comparison_report_integrity_digest`.

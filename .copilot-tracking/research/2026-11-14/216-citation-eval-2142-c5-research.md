<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Hardening Pass 5 (`RV-001`..`RV-002`)

* Task ID: 216-citation-eval-2142-c5
* Parent Task ID: 216-citation-eval-2142-c4
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence

1. `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c4-review.md` (`RV-001`, `RV-002`):
   * `projected_cases` in `compare_chat_against_rule_cards` copied `scenario` and `question` without strict JSON validation or `_to_plain_json` projection.
   * When replayable inputs (`cases`, `paired_cards`, `prompts`, `agreement`, `observations`, `benefit_thresholds`, `cost_inputs`) contain non-JSON-compatible values (`bytes`, non-`str` mapping keys, non-finite floats, custom objects) or primitive subclasses whose `type(value).__name__` differs after JSON round-trip, `_to_plain_json` alters digest semantics between initial evaluation and replay in `resolve_regulatory_surface`.
2. `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_normalize_json_value`, `_to_plain_json`, `compare_chat_against_rule_cards`, `_verify_comparison_evidence`):
   * Adding `_is_strict_json_value(value)` (accepting only `None`, `bool`, `int`, finite `float`, `str`, non-bytes `Sequence`s of strict JSON values, and `Mapping`s with `str` keys and strict JSON values), rejecting non-JSON-compatible replay inputs in `compare_chat_against_rule_cards` before `measured_value` can be `True`, projecting all six case keys via `_to_plain_json`, normalizing `-0.0` to `0.0`, and tagging canonical primitives by base JSON category (`null`, `bool`, `str`, `int`, `float`) guarantees strict `json.dumps(..., allow_nan=False)` serializability and exact digest/replay invariance across all accepted inputs.

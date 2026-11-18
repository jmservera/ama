<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c4
* Parent task: 216-citation-eval-2142-c3
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence Summary

* `E1` (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c3-review.md` `RV-001`, `RV-002`): Storing JSON-native replay inputs (`cases` projected to `{id, set_name, scenario, question, expected, actual}` via recursive plain-JSON conversion, `paired_cards`, `prompts`, `agreement`, `observations`, `observation_count`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, and `now`) in `verified_comparison_inputs` keeps `compare_chat_against_rule_cards` 100% `json.dumps`-serializable and `json.loads`-round-trippable while letting `_verify_comparison_evidence` reconstruct `re_gates` and `re_comparison` and enforce exact `dict(comparison) == re_comparison` parity across every field (including all `beside_cost` scalars), and letting `_verify_agreed_gates_report` enforce exact `dict(gates_report) == re_gates` parity across every field of `gates_report`.

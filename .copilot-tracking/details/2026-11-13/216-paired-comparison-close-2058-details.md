<!-- markdownlint-disable-file -->
# Details: 216 paired comparison close

## Phase 2

* `regulatory_gates.beside_cost(economics, checks, hazard)` returns
  `dict(ai_cost_per_accepted_check, cost, missing_inputs, citation_validity, refusal_accuracy,
  hazard_misses)`; each gate is a view `dict(status, matched, total, failed_case_ids)` or
  `dict(status="not_evaluated")` when the result is absent. Never estimates cost.
* `comparison(baselines, answers=None, rules=None)` adds `beside_cost` using
  `answers["checks"]` and `rules["hazard_misses"]`; `run()` passes both. Verdict unchanged
  (`cards_only`, no staff observations).
* `evaluate_paired_trial(..., gates=None)`: `gates` is the `answers["checks"]` mapping.
  Reasons are added when cost is not a known authorised number ("AI cost per accepted check
  Unknown; value at cost not measured") and when citation validity or refusal accuracy is
  not supplied or its status is not `met_provisional_target`. Any reason keeps `cards_only`.
  Result gains `beside_cost`.

## Phase 3

* `price_source.as_of` must be an ISO date not after `now`; `id` and `currency` non-blank
  strings; otherwise Unknown naming the field.

## Tests

* cards tie or beat chat with links -> `cards_only`.
* chat adds measured value, known dated cost, passing gates, zero misses -> owner decision
  required, `beside_cost` carries cost 0.06 beside gates and hazard result.
* missing price/usage/ledger -> `"Unknown"` naming exact inputs, never a number.
* chat value but cost Unknown, gate failed or absent, or hazard miss -> `cards_only`.
* undated/future price -> Unknown.
* committed `comparison` has `beside_cost` with Unknown cost beside gate results.

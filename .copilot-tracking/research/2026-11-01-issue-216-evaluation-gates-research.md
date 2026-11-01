# Research: #216 evaluation gates

* Disposition: executed. Planning Readiness: Ready.
* Evidence: the harness shipped earlier (#355, #506): `src/agents/src/zava_forward/agents/regulatory_gates.py`, `evals/run_regulatory_gates.py`, recorded `evals/regulatory_gates_results.json`, README section "Regulatory evaluation gates (#216)".
* Baseline run on this branch: `test_regulatory_gates test_regulatory_answers test_eval_registry` 32 tests OK; the 60,000-home report reproduces.
* Already proven: per-check results (no overall pass), hazard misses critical, recall baseline unset target, stale-source label, comparison `cards_only` with cost Unknown (`regulatory_usage.economics()`).
* Gaps against acceptance criteria:
  * Owner-agreed thresholds, graded/adversarial owner sign-off: need real owners; cannot be delivered by code.
  * Measured staff comparison value: needs staff trial; cards ship alone stays.
  * Tokenomics AC2: no executable guard stating that a model-calling eval run must carry a finite owner-authorised call/token/budget/expiry limit. Only the zero-limit report fields exist.
* Smallest in-scope slice: a pure `authorise_model_run` guard plus tests; no model dispatch, no spend authority assumed.

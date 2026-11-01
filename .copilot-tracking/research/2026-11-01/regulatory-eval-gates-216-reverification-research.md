<!-- markdownlint-disable-file -->
# Research: #216 regulatory evaluation gates re-verification (2026-11-01)

Research disposition: executed (targeted, local). Planning Readiness: Ready.

## Question

What of #216 is already delivered on main, what still fails its acceptance
criteria, and what is the smallest demo-ready slice?

## Evidence

* Gates exist: `src/agents/src/zava_forward/agents/regulatory_gates.py`, driver
  `src/agents/evals/run_regulatory_gates.py`, fixture `src/agents/tests/regulatory_gate_fixture.py`,
  report `src/agents/evals/regulatory_gates_results.json` (merged #355, extended #506).
* Cadence labels delivered in core (README "Read-only source-cadence labels (#216)").
* Re-run on 2026-11-01 at `80673b0d`: `test_regulatory_gates`, `test_regulatory_answers`,
  `test_eval_registry` 32 tests OK; regenerated 60,000-home report is byte-identical to the
  committed report; ruff check, ruff format --check and mypy clean for `src/agents`.
* Tokenomics: report economics carry `ai_cost_per_accepted_check: Unknown` with four named
  missing inputs and a zero model-call/token/budget limit with `paid_authority: none`.
* `src/agents/README.md` "Acceptance audit (2026-10-16)" lists unmet boundaries.

## Criteria status (issue body)

| Criterion | Status |
| --- | --- |
| Citation/refusal gates set with owners, graded and adversarial set | Unmet: owner agreement and independent held-out grading need humans |
| Hazard misses critical | Met locally |
| Recall baseline before thresholds | Met locally (stateless seeded); continuing-stock baseline not run |
| Paired comparison / cards alone | Unmet: no staff trial; `cards_only` recommended |
| Out-of-cadence labelled | Met locally |
| Per check, no overall pass | Met |
| Tokenomics cost per accepted check or Unknown | Partial: Unknown cost recorded with inputs named (verified); paired comparison and cards-alone shipment unproven, no measured comparison |
| Finite owner-authorised model-run limits | Partial: zero-call offline limits verified (zero limits, no authority); no owner-authorised model evaluation exists |

## Conclusion

No code defect or drift. Smallest slice: record the dated re-verification (README audit
note, knowledge-base log) and publish with `Refs #216`, naming the unmet criteria.

---
title: Changes for issue 216 paired comparison close
ms.date: 2026-11-13
---

* `src/agents/src/zava_forward/agents/regulatory_gates.py`: `beside_cost`, `gate_view`, `gate_passed`, `hazard_view`; `comparison()` gains `beside_cost`.
* `src/agents/src/zava_forward/agents/paired_trial.py`: `gates` argument, `beside_cost`, strictly positive improvement per role, Unknown cost and unmet or provisional gates keep cards only, dated and identified price validation, hazard `total`.
* `src/agents/tests/regulatory_gate_fixture.py`: passes answers and rules to `comparison`.
* `src/agents/evals/regulatory_gates_results.json`: regenerated, additive `comparison.beside_cost` only.
* Tests: `test_paired_trial.py` (new `CardsAloneAndBesideCost`, updated positive case), `test_regulatory_gates.py`.
* `src/agents/README.md`: 2026-11-13 section.

## Validation (focused tier, pip venv removed afterwards)

* ruff check and format --check clean for core, agents, api; mypy clean in all three.
* Passing: paired_trial, paired_report_command, regulatory_gates, chat tests (agents), rulecards and ai_consumption (core), api chat_eval and ai_consumption.
* `test_ai_call_site_inventory`, `test_content_standard`, `test_accessibility_baseline` do not exist under those names in this tree; nothing they cover was touched.
* Not run: full local gate, hosted CI. Failing-first confirmed (19 failures or errors before implementation).
* Divergence: none from plan.

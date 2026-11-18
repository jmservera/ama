# Research: #219 model-option comparison

* Disposition: executed. Planning Readiness: Ready.
* Finding: `src/agents` has `ai_eval.py` (workflow-only vs AI recall per scenario) and `candidate_comparison.py` (model/routing/caching candidates vs a baseline). Neither models the four-tier ladder (workflow-only, rule-cards, small-model, large-model) or selects the simplest option meeting a bar. `src/core` has no comparison module.
* Note: the GitHub title of #219 is "RAI release record bound to each AI task activation", while the task brief names model-option comparison; the brief was followed. Flag for owner.
* Decision: add a pure module `model_option_comparison.py` in `src/agents` with caller-supplied bar (no thresholds invented), shared-case enforcement, unknown cost fails a cost bar.

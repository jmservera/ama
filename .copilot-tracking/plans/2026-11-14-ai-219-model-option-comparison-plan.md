# Plan: #219 model-option comparison

* [x] Add `src/agents/src/zava_forward/agents/model_option_comparison.py`: score accuracy, unsafe cases, p95 latency, cost per case per option; select the simplest meeting the bar.
* [x] Add `src/agents/tests/test_model_option_comparison.py` (selection, safety/latency/cost gating, mismatched cases, unknown cost, input validation).
* [x] Run mypy, ruff check, ruff format --line-length 100 --check, focused tests.
* Critique: one pass, self-applied; no conflicts with decisions.

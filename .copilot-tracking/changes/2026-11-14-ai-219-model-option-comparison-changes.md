# Changes: #219 model-option comparison

* Added `src/agents/src/zava_forward/agents/model_option_comparison.py`.
* Added `src/agents/tests/test_model_option_comparison.py` (5 tests).
* Validation: mypy clean (65 files); ruff check and format clean; focused tests OK. Full tier gate not run (additive offline module, no deployment, permissions or gate change; focused tier). Not pushed.
* Not delivered: no real-model observations, no wiring into a CLI or eval registry, no price source.

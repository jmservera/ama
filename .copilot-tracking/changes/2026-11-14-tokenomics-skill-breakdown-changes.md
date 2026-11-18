# Changes: per-skill tokenomics breakdown

* `src/core/src/zava_forward/core/ai_consumption.py`: reasoning-token parsing, `token_breakdown`, `tariff_basis`, new report fields.
* `src/core/tests/test_ai_consumption_skill_breakdown.py`: new, 5 tests.
* `src/core/tests/test_ai_consumption.py`: per-assistant test updated for the new row keys.
* Validation: core unittest 43 OK; API `test_ai_consumption_api` 40 OK; ruff check and format clean. Run with `PYTHONPATH=src` because the installed editable package points at another checkout.
* Divergence: none. Not pushed.

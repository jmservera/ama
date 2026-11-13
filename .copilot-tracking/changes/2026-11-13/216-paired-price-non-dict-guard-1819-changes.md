# Changes: paired price non-Mapping guard

* `paired_trial.py`: truthy non-Mapping `price_source`/`usage` named "not a mapping"; per-field non-negative numeric validation; overflow-safe costing.
* `test_paired_trial.py`: tests for non-Mapping, falsy, missing nested keys, non-numeric/negative/huge values, overflowing product.
* Validation: test_paired* 35 OK; ruff check/format OK; mypy OK (venv removed before commit).

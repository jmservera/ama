# #129 AC1 changes

* `src/core/tests/test_learning_test_bundles.py`: added `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure`.
* No production change: bundle definitions, validation and comparators already exist.
* Validation: `ruff check src/core` and `ruff format --line-length 100 --check src/core` pass; `test_learning_test_bundles` (22 tests, absolute PYTHONPATH needed for subprocess cases) and `test_governance` (71, 16 skipped) pass.
* Tier: focused (test-only, no gate/security change). Hosted CI not observed; branch not pushed.

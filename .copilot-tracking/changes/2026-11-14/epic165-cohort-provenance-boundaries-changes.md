# Changes: Epic #165 cohort provenance and boundary tests

* Added `src/core/tests/test_epic165_synthetic_provenance_boundaries.py`.
* No source, manifest or dependency change.

Validation: unittest across the three modules (31 tests) OK; `ruff check`, `ruff format --check` and `mypy` clean. Hosted CI not observed; not pushed.

Divergence: `needs_inventory.py` does not exist, so needs coverage relies on `needs-inventory.json` and its existing test.

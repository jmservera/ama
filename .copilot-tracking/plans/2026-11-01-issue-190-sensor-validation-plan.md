# Plan: sensor validation consumer contract (issue 190)

* [ ] Add `src/core/tests/test_sensor_retrofit_consumer_contract.py`: per-profile checks that observation-only `retrofit_comparison` deltas classify to the truth label using exercise tolerances; truth never passed to the consumer; per-check subTests (no aggregate pass).
* [ ] Add a short pointer in `src/core/README.md` simulator section naming the contract test as the fixture for #111/#133.
* [ ] Validate: unit tests, ruff check, ruff format --check, mypy on `src/core`.
* [ ] Commit, push, open PR with `Refs #190` naming unmet criteria.

Critique (single pass, self-applied): the classifier is a test oracle, not a product rule (label exercise value); delayed effect needs early~0 and late>0 improvement; do not claim #133/#111 consumption (Refs only).

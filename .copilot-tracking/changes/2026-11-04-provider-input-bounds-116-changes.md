# Changes: provider input bounds for issue 116

* src/core/src/zava_forward/core/ai.py: InputRefused, MAX_TEXT_BYTES, MAX_IMAGE_BYTES, IMAGE_TYPES; guard in _request; evidence outcome input-refused; look_at image check.
* src/core/tests/test_ai_input_bounds.py: new behavioural tests.

## Validation

* Run: 56 focused unit tests pass; ruff clean; mypy (CI config, tests included) clean.
* Not run: complete gate, full suites, benchmarks, hosted CI.

## Unmet criteria after this slice

Criterion 3 partly advanced (size and image-type bounds only; unknown task/field not covered). Criteria 1, 2, 4, 5, 6 and OD-14/OD-19 remain unmet. Issue stays open: Refs #116.

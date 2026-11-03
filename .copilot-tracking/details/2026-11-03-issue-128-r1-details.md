# Details: issue 128 R1

* Phase 1: `src/core/src/zava_forward/core/journey_register.py`: `draft`, `evaluate`, `human_review_route`, `route_cases`. Uses `rai_release.named` and `digest`.
* Phase 2: `src/core/tests/test_journey_register.py` (7 tests).
* Phase 3: `docs/reference/research/ux/equity-journey-test-plan.md`, `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Phase 4: unit test, `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-128`.

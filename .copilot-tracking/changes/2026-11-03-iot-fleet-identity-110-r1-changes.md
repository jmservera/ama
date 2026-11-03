# Changes: IoT fleet identity evidence slice (issue 110 r1)

## Added

* `src/api/tests/test_iot_stream.py`: `FleetIdentityTests` (2 test methods). No production source, dependency, workflow or knowledge-base file changed.

## Validation run (focused)

* `test_iot_stream` plus `test_iot_credential_hygiene`: 48 tests pass (includes the 2 new).
* `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-110` on the changed file: pass.
* Dependencies installed with pip into an external venv (`/tmp/venv110`); generated egg-info removed.

## Not run

Complete local gate, benchmarks, full API suite, hosted CI, Azure, live Hub, independent exact-head review.

## Divergences

None.

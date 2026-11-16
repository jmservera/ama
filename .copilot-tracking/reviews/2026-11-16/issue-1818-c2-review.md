# Issue 1818 c2 review

Executed once. Outcome: conformant. Diff is limited to `src/api/tests/test_map_sensors.py`; behaviour unchanged (all 13 tests pass with identical call defaults); all four reported mypy errors are gone and both mypy runs are clean; ruff clean. No open findings. The single targeted ignore stays because `test_assistants.request` is untyped and outside this fix's scope.

# Changes: same-home journey trace, slice 1 (Refs #134, R1)

## Added

* src/core/src/zava_forward/core/journey_trace.py
* src/core/tests/test_journey_trace.py

## Modified

* src/core/README.md: "Same-home journey trace" section.

## Validation (focused tier)

Run with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH set to this worktree's src folders (installed distributions point at another worktree).

* `tests.test_journey_trace`: 8 pass.
* `tests.test_stock_reconciliation`, `tests.test_buildings`, `tests.test_scenario_manifest`: 47 pass.
* `ruff check` on src/core: pass; `ruff format --check` on the new files: pass; `mypy --cache-dir=/tmp/mypy-134` on journey_trace.py: pass.
* Not run: gate, benchmarks, full suites, SQL Server, browser tests.

## Divergences

None.

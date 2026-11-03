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

## Correction cycle (PR #872 review findings)

* journey_trace.py: `finance_payment_status` closes the journey only when the detail ends `payment noted as Paid outside this system`; `Not payable yet` and `Awaiting payment run` do not.
* journey_trace.py: `finance_disposition` counts as an independent decision only for `Accept for payment`; `Reject and return to provider` and `Keep on hold` do not.
* Tests: two regression tests added, later-stage fixture uses the real payment detail; `tests.test_journey_trace` 10 pass, with `test_stock_reconciliation` and `test_buildings` 49 pass; ruff check and format pass.
* README: states closure status and acceptance-only Finance rule; independence needs at least two domains and no actor in more than one domain.

## Divergences

None.

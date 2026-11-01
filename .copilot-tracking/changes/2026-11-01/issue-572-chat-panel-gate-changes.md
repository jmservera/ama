<!-- markdownlint-disable-file -->
# Changes: issue 572 chat-panel gate evidence

Plan: [plan](../../plans/2026-11-01/issue-572-chat-panel-gate-plan.md)

## Added

* RPI research, plan, changes and review artifacts for issue 572 (this set).

## Source changes

* None. Gate wiring and regressions were already merged (#575, #595, #600, #606).

## Validation

* `python3 -m unittest tools.test_rpi_checks`: 55 OK.
* ruff 0.17.1 pinned profile check/format: pass; `mypy --strict` on gate files: pass.
* Exact chat-panel case with `ZF_BROWSER_TESTS=1`: 1 test OK, 0 skips.
* Complete local gate: not run (out of tier; AC4 unmet).

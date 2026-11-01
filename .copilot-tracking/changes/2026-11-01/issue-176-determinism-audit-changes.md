<!-- markdownlint-disable-file -->
# Issue 176 changes: determinism audit slice

Date: 2026-11-01. Plan: `.copilot-tracking/plans/2026-11-01/issue-176-determinism-audit-plan.md`.

## Added

* `src/core/src/zava_forward/core/synthetic/determinism_audit.py`: replay audit CLI.
* `src/core/tests/test_determinism_audit.py`: 5 tests.

## Modified

* `sensor_scenarios.py`: manifest now records `version`.
* `docs/reference/research/retrofit-synthetic-data/README.md` and `docs/reference/log.md`.

## Validation

* unittest (determinism_audit, sensor_scenarios, synthetic_determinism): 27 OK.
* ruff check, ruff format --check, mypy on src/core: clean.

## Divergences

* None. Heavy local gate not run by owner direction; CI is the evidence.

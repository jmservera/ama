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

## PR review correction (2026-11-01)

* `determinism_audit.py`: each result now reports its `window`; `sensor-scenarios` reports its intrinsic 2024-01-01 to 2024-01-29 window, others report the audit as-of date. Top-level `as_of` is qualified by `as_of_applies_to`.
* Revision check now requires a full `sha256:` plus 64 lowercase hex digits, matching `test_synthetic_determinism.py`.
* Tests added: malformed revisions fail, valid revision passes, scenario window is intrinsic. unittest (determinism_audit, synthetic_determinism): 15 OK; ruff check/format and mypy clean.

## PR review correction 2 (2026-11-01)

* `test_determinism_audit.py`: the drift fixture now uses a valid full SHA-256 revision, so only byte drift can cause `FAIL`.

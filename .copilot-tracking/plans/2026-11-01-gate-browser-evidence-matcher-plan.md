# Plan: gate browser evidence matcher (2026-11-01)

* [x] Add `_single_test_passed` in `tools/rpi-checks.py`; use it for `expected_test`.
* [x] Reject FAIL/ERROR/skipped/expected failure/unexpected success tokens, zero or duplicate headers, wrong test name, missing result.
* [x] Unit tests in `tools/test_rpi_checks.py`.
* Tier: focused (unit tests, ruff). Full gate not run. Receipts and verification semantics unchanged.
* Critique: executed once, inline; compatible. No conflicts with owner direction.

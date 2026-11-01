# Plan: employee live acceptance CLI (#570)

Date: 2026-11-01. Research: ../../research/2026-11-01/employee-live-acceptance-570-research.md

## Phases

* [x] 1. Add `src/api/checks/employee_live_acceptance.py`: `main(argv, env)` parses `--cdp-url` (loopback only), `--origin` (default APP), reads `ZF_EXPECTED_TID` and `ZF_EXPECTED_OID` from env, attaches with `connect_over_cdp`, picks the first page on the origin, runs `verify_employee`, prints fixed boolean JSON, returns 0 only if `passed`.
* [x] 2. Add `src/api/tests/test_employee_live_acceptance.py` with a fake Playwright (invalid GUIDs, non-loopback CDP, no page, pass/fail mapping, output contains no identity values).
* [x] 3. Add a short README paragraph. Validate with unittest, ruff check, ruff format --check, mypy.

## Critique (single pass)

Compatible: no credential entry, no sign-in, loopback CDP only so a remote browser cannot be driven, output restricted to booleans. Conflict with confirmed decisions: none. Live criterion 3 stays unclaimed, so the PR uses Refs.

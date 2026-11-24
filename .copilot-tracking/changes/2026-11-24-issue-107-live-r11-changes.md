# Issue 107 live r11 changes (2026-11-24)

Tier FULL (test code under `src/api`); basis: src tests changed. `rpi-checks.py --all` not run, left to the coordinator. Nothing pushed.

## Files

* `src/api/tests/assistant_process_worker.py`: `schema` and `registry` variations.
* `src/api/tests/test_assistant_release.py`: two separate-process tests.
* `docs/reference/research/issue-107-live-r11-schema-registry-2026-11-24.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* SQLite: 109 tests OK (29 skipped). Disposable SQL Server 2022 at 127.0.0.1: 46 tests OK, 0 skipped; container removed. ruff check/format and mypy clean. Mutation check fails as intended.
* Not run: hosted CI, independent exact-head review, live Azure SQL (fixture refuses it by design).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Independent SQL connection/worker and race tests (mismatch, revocation, restart; no restore or replenishment) | Proven for the demo (constructed fixtures, disposable actual SQL Server); not on live Azure SQL |
| Matching approved exercise record permits bounded proposals only; delivered-build acceptance | Unproven: no approved release on deployed build; approver not appointed (OQ-017) |

# Issue 107 live r10 changes (2026-11-24)

## Files

* `src/api/tests/assistant_process_worker.py`: `data`, `provenance`, `model` variations.
* `src/api/tests/test_assistant_release.py`: three separate-process tests (data, provenance, serving model).
* `docs/reference/research/issue-107-live-r10-root-cause-2026-11-24.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* SQLite: 105 tests OK (27 skipped). SQL Server 2022 container, 127.0.0.1: 44 tests OK, 0 skipped; container removed. ruff check/format and mypy clean. Mutation check on the model test fails as intended.
* Tier FULL (test code under `src/api`); `rpi-checks.py --all` not run, left to the coordinator. Nothing pushed.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Independent SQL connection/worker and race tests (mismatch, revocation, restart; no restore or replenishment) | Proven for the demo (constructed fixtures, disposable actual SQL Server); not run on live Azure SQL by fixture design |
| Matching approved exercise record permits bounded proposals only; delivered-build acceptance | Unproven: no approved release on the deployed build, approver not appointed (OQ-017) |

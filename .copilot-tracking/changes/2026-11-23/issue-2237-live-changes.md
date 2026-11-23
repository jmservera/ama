# Issue 2237 live changes (2026-11-23)

Refs #2237. Plan: `.copilot-tracking/plans/2026-11-23/issue-2237-live-plan.md`. Research: `.copilot-tracking/research/2026-11-23/issue-2237-live-research.md`. Note: `docs/reference/research/issue-2237-live-cause-and-fix-2026-11-23.md`.

Tier FULL (src changed). `rpi-checks.py --all` was not run (coordinator runs gates). Witness note: the `implement-start` call reported source already dirty, because the untracked `live_probe.py` under docs counted as source; no `src/` edit predates it.

## Changes

* `src/core/src/zava_forward/core/mssqlstore.py`: `is_write_lock_busy`.
* `src/api/src/zava_forward/api/server.py`: `_unhandled` answers GET and HEAD requests with 503 and `Retry-After: 5` and logs `cause=sql-write-lock-busy` for a timed-out SQL write lock; other failures, and POST, unchanged (a POST may follow a committed step).
* `src/core/tests/test_mssql_startup_lock.py`: 3 helper tests. `src/api/tests/test_error_logging.py`: 2 tests (503 path; unrelated driver error stays 500).
* Docs: new research note and evidence folder `issue-2237-retention-500-live-2026-11-23/`; superseded pointer in the 2026-11-22 note; index row and log entry.

## Validation

| Check | Result |
| --- | --- |
| `src/api` `unittest test_error_logging` (documented PYTHONPATH) | 10 tests OK; the new 503 test fails (500, no header) with the server change stashed |
| `src/core` `unittest test_mssql_startup_lock` | 9 tests OK |
| `python3 -m mypy` in `src/api` (with PYTHONPATH) | no issues |
| `python3 -m mypy` in `src/core` | 3 errors, identical with my changes stashed (missing opentelemetry exporter stubs, one unused ignore in `synthetic/device_provision.py`); none from this change |
| `ruff check` and `ruff format --check` on touched files | pass |
| Not run | `rpi-checks.py --all`, full core and api suites, hosted CI (nothing pushed) |

## Per-criterion table (issue 2237)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce | Proven historically (11 logged 500s of about 15 s); not re-triggerable on demand; deterministic local reproduction added as a test | `law-retention-http-5xx.json`, `law-retention-500s.json` |
| Find the cause in the demo container logs | Proven: SQL write-lock timeout (`sp_getapplock`, 15 s, error 50002) during the audit write of the retention listing. Unproven: which writer held the lock | `law-*.json` files, research note |
| Fix with a regression test | Proven locally (503 mapping plus tests); not deployed | commit diff, tests above |
| Re-prove 200 live | Proven on 0000054 for the Retrofit Programme Manager account (55 of 55 requests 200) | `r54-role-2026-11-23T01.json` |

Owner-gated or out of scope: deploying the fix (no push or deployment authorised); identifying lock holders and shortening write transactions.

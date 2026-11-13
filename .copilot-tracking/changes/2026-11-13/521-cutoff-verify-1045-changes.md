# 521 changes: Criterion 1 cutoff verification

No src/, infra/ or docs/ edits (tracking-only). Base 3b05143179f83235c5b4e80e70aad99bdc44d83f.

## Verdict

Criterion 1 is consistent for the resident authority end (exclusive 2028-01-01T00:00:00Z) across code, SQL template, secret helper, Bicep, browser checks, tests and current-state docs. No stale resident-authority cutoff literal remains in code, SQL, helper, Bicep or fixtures. Two qualifications: (a) the SQL database behaviour (27 of 40 SQL tests) was skipped without MSSQL, so only renderer/template checks ran; (b) infra/README.md:4614-4621 (dated 2026-11-04 entry) still says live move to 2028 is Pending while infra/README.md:1590 records the live app expiry change to 2028-01-01; this is dated history, and live SQL constraint state is unverified here (no cloud access).

## Consistency table

| Layer | file:line | Evidence |
| --- | --- | --- |
| Single source | src/core/src/zava_forward/core/resident-demo.json:2 | maximum_expiry_utc 2028-01-01T00:00:00Z |
| Code | src/core/src/zava_forward/core/resident_showcase.py:42,264,418,628 | loads JSON; `now >= AUTHORITY_END` excluded; session end min(); expires > AUTHORITY_END refused |
| Code (API) | src/api/src/zava_forward/api/resident_demo/app.py:130 | min(expires_at, rs.AUTHORITY_END) |
| SQL | infra/sql/resident-showcase.sql:21,37; infra/scripts/resident_showcase_sql.py:24,35 | CHECK valid_to <= rendered AUTHORITY_END |
| Secret helper | infra/scripts/resident_demo_secrets.py:46,51 | MAX_EXPIRY = AUTHORITY_END; deploy helper delegates to parse_expiry |
| Bicep | infra/resident-demo.bicep:36,38 | loads same JSON; expiresAt <= maximumExpiry |
| Browser/image checks | src/api/checks/resident_demo_browser_check.py:8,113,127; resident_demo_image_check.py:144; resident_sensors_browser_check.py:45,281,290 | use rs.AUTHORITY_END, no literal (comment :8 says January 1, 2028) |
| Tests core | src/core/tests/test_resident_showcase.py:88-103,438-500 | old 2026-11-01, 2027-01-31T23:59:59Z, 2027-02-01 refused; 2028-01-01 accepted; +1s/+1ms refused |
| Tests SQL | src/core/tests/test_resident_showcase_sql.py:203-207,639-666 | renders 2028-01-01T00:00:00, no 2026-11-01; DB checks MSSQL-only |
| Tests api | src/api/tests/test_resident_demo_check.py:83-107; test_resident_demo_api.py:417-441,827 | not run (needs azure packages, installed --no-deps) |
| Tests infra | infra/tests/test_resident_demo_secrets.py:225-241; test_resident_demo_deploy.py:341-342 | old cutoffs refused, +1s/+1ms refused |
| Docs | infra/README.md:4267,4298,4397,4439,4519-4545; src/api/README.md:5630,5676 | state 2028-01-01 exclusive |
| Not authority | src/api/README.md:1835-1983; src/core/.../ai_consumption*.py:27 | 2026-11-01 is the independent model tariff cutoff, intentionally unchanged |

## Execution evidence

Python 3.12.3; /tmp/venv-521-1045 with `pip install --no-deps -e src/core -e src/api`; `zava_forward.core` origin src/core/src/... and `zava_forward.api` path src/api/src/... inside the worktree. `zava_forward.api.resident_demo.app` import fails (no `azure` package, no-deps), so API tests were not run. ZF_TEST_MSSQL unset, PYTHONDONTWRITEBYTECODE=1. Exit codes were captured directly from the unittest producers.

| Suite | Result | rc |
| --- | --- | --- |
| src/core/tests/test_resident_showcase.py | 41 tests OK | 0 |
| src/core/tests/test_resident_showcase_sql.py | 40 tests, OK, 27 skipped (MSSQL) | 0 |
| infra/tests/test_resident_demo_secrets.py | 16 OK | 0 |
| infra/tests/test_resident_demo_deploy.py | 17 OK | 0 |
| infra/tests/test_resident_assistant.py | 3 OK | 0 |

Cleanup: venv, logs and ignored egg-info removed; no Docker, MSSQL, cloud or .env access.

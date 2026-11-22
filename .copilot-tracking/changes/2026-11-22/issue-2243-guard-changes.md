---
title: Changes for issue 2243 diagnosable ledger refusal
ms.date: 2026-11-22
---

Status: complete. Tier: FULL classification (src and infra/sql changed); `rpi-checks.py --all` not run, the coordinator runs gates. Local checks run: `src/api` unit tests for resident aoai, SQL (skipped, opt-in), assistant API and ledger meter (64 tests OK, 8 skipped), bare mypy (no issues), ruff check and format on changed files.

## Files

* `infra/sql/resident-assistant.sql`: `resident_ai.reserve` returns `accepted` plus `refusal`.
* `src/api/src/zava_forward/api/resident_demo/aoai.py`: `SqlAccounting.reserve` raises `ledger_expired`, `budget_spent` or `resident_rate_limit`; new fallback labels.
* `src/api/tests/test_resident_aoai.py`, `test_resident_aoai_sql.py`: new and updated tests.
* `docs/reference/research/issue-2243-guard-2026-11-22.md` plus probe evidence folder; index and log updated.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven (code, unit test, live env value) |
| Add a test | Proven (unit); opt-in SQL test edited, unproven (no SQL Server) |
| Clear diagnosable state | Proven locally; not live until the procedure and image deploy |
| Rebuild and roll the resident image | Unproven (no production change authorised) |
| Resident chat answers with the model | Not met: live probe on 0000025 still `usage_limit`; SQL row private and unreadable |

No divergence from the plan.

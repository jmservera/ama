---
title: Issue 2304 round 2 changes (2026-11-24)
ms.date: 2026-11-24
---

# Changes

Tier: FULL classification (src code), gate left to the coordinator. No deploy, no push.

* `src/core/src/zava_forward/core/forecast_reads.py`: `ForecastReads.once`.
* `src/core/src/zava_forward/core/assistants.py`: `release_reference` memoised inside the forecast view; profile 80 s to 1.4 s at 448 cases, 20 statements.
* `src/api/tests/test_assistants.py`: `test_registry_builds_do_not_grow_with_open_cases` (fails without the fix).
* Evidence: `docs/reference/research/issue-2304-live-2026-11-24-r2.md`, probes and profile script in `docs/reference/research/issue-2304-live-2026-11-24/`.

Validation: `test_assistants` 156 tests OK (65 skipped, MSSQL-only); release tests OK; ruff and format clean; `src/api` mypy clean; `src/core` mypy shows 3 pre-existing environment errors (opentelemetry stubs, unused ignore) identical without the change. The full api and core discover runs were started but not confirmed to completion (log ended without a summary), so they are not claimed.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Profile where time goes | Proven locally; live SQL trace unproven |
| 2 | Answer within a bound or named state | Proven in tests and live (stale/named); fast fresh live answer unproven until deploy |
| 3 | Counting connection test | Proven |
| 4 | Live re-check after deployment | Unproven: no deploy permitted |

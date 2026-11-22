---
title: Details for issue 2243 plan
ms.date: 2026-11-22
---

## Phase 1

`infra/sql/resident-assistant.sql`: compute a refusal in order `ledger_expired`, `budget_spent`, `resident_rate_limit`, `duplicate`; `SELECT accepted, refusal`. Accepted rows return `NULL` refusal. Column 0 is unchanged so old callers keep working.

## Phase 2

`aoai.py`: `_run` returns the full row; `reserve` raises `AssistantUnavailable(reason)` for known reasons; a one-column or unknown row keeps `None` (`usage_limit`). New `FALLBACK_REASONS` entries tell the owner what to change, with no resident-identifying data.

## Phase 3

`test_resident_aoai.py` fake-connection tests for each reason and old-procedure compatibility; update opt-in SQL test assertions.

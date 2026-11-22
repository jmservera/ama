---
title: Research for issue 2243 resident AI exercise guard (2026-11-22)
description: Why the resident chat falls back to rules and which gate is not diagnosable
ms.date: 2026-11-22
---

Research disposition: executed. Planning Readiness: Ready. Full evidence note: [issue-2243-guard-2026-11-22.md](../../../docs/reference/research/issue-2243-guard-2026-11-22.md).

## Findings

* `assistant.py` already derives expiry from `ZF_DEMO_EXPIRES_AT` (merged in #2249). Live revision `ca-resident-demo--0000025` carries `2028-01-01T00:00:00Z`.
* Live probe on revision 0000025 (2026-11-22 ~20:55 UTC): both model-eligible questions return "AI usage limit was reached" (`reason=usage_limit` in console logs).
* The refusal comes from `resident_ai.reserve` (`infra/sql/resident-assistant.sql`), which returns only `accepted=0` for four different causes: spent budget, stored `expires_at` passed (default `2026-11-01` on the existing live row), hourly resident limit, duplicate reservation. The label cannot tell the owner which ledger state to change.
* SQL is private (public access disabled), so the row cannot be read or changed from this client; the cause is inferred, not proven.

## Selected approach

Return a refusal reason column from the procedure; `SqlAccounting.reserve` raises a specific `AssistantUnavailable` reason (`ledger_expired`, `budget_spent`, `resident_rate_limit`); an old procedure returning one column keeps `usage_limit`. Add allowlisted labels, unit tests, and an opt-in SQL test.

---
title: Issue 2256 handoff waiting list omits offers with a timezone-less offered time (2026-11-22)
description: Live probe and code trace showing why the demo Handoff waiting times screen is empty while cases show an offered handoff, with the fix and a per-criterion table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, app `ca-cutover-test-demo-api`, role Retrofit Programme Manager. Sign-in values were read at run time and never printed. No Azure change and no throwaway resource.

## Live probe (2026-11-22, about 15:25 UTC)

| Call | Result |
| --- | --- |
| `GET /api/handoffs` | 200, 4 rows: ZF-2025-0029 to ZF-2025-0032, all `Offered`, `offered_at` `2026-10-13T09:00`, same receiver code |
| `GET /api/handoffs/unaccepted` | 200, 0 rows |
| `GET /api/case/ZF-2025-0030` | 403 (single-case route is not open to this role; the case view is the workspace) |

The pending list and the waiting list disagree for the same four cases.

## Cause

`workflows.py` `handoff_ageing` calls `datetime.fromisoformat(h["offered_at"])` and raises `ValueError("Handoff offered_at needs a timezone.")` for `2026-10-13T09:00`, because the seeded value has no UTC offset. `unaccepted_handoffs` catches that `ValueError` and skips the case with a comment saying it stays visible in the pending queues. The waiting screen has no such fallback, so every seeded offer vanishes and the screen states that none are visible. The SLA code (`handoff_sla`, `_optional_tz_instant`) already treats such a value as unknown instead of failing. A naive `due_at` would additionally raise `TypeError` when compared with an aware `as_of`.

## Fix

`handoff_ageing` now keeps the row when `offered_at` or `due_at` has no timezone: `age_hours` is `null`, a reason says the waiting time is unknown, and the screen shows "Unknown" instead of a number. Rows with a known age keep the longest-first order; unknown ones follow. The offer is never given an invented timezone.

## Per-criterion table (issue 2256)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Offered handoff appears in the waiting list with due time and chase owner, or the case does not describe an open offer | Proven by regression tests (core and API) with a timezone-less `offered_at`; not proven on the deployed host because the fix is not deployed (no push, no deploy in this task) | changes record |
| Live reproduction | Proven: probe table above | this note |
| Web UI tests after web change | Proven locally, see changes record | changes record |

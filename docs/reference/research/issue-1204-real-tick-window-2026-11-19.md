---
title: Issue 1204 real tick window check, 2026-11-19
description: Result of running the tick_log checker on the real local coordinator session log
ms.date: 2026-11-19
---

Scope: synthetic demo, FOCUSED tier, no Azure surface. Refs #1204.

## Evidence

* Three local coordinator sessions hold a `tick_log` table. One (216 rows, ticks 1 to 216, last tick 2026-11-17 11:34:37 UTC) has the count and `action_taken`/`evidence` columns the checker maps.
* Command: `python3 tools/check-tick-log.py <session>/session.db`. Result: `216 ticks, 0 violations`. Raw rows are operational text and are not committed.
* The other two logs use a `classifications` column instead and fail to load (`no such column`), so they are unproven.

## Unproven

* Closure-review batch bound, approval reconciliation and global-stop rules: real rows carry no such fields.
* The criterion box stays unticked.

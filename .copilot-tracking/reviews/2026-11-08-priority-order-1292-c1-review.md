---
title: Issue 1292 C1 review
description: Single original post-implementation review of correction C1 for issue 1292
ms.date: 2026-11-08
---

Review executed once on the uncommitted C1 diff by an independent read-only code-review agent (light evidence only). It is not the coordinator's independent exact-head review, hosted CI or human approval. Original review and addenda are unchanged.

## Outcome

Conformant with one routed Medium residual. No high-confidence defects.

* Verified: no nested `BEGIN` or deadlock path (`_sync` runs outside a transaction from lock entry, `_discard` and post-commit `save`, and inside `_queue_candidates` it reuses the open transaction through the thread-local `writing` flag); after a repair inside `save` the post-commit `_sync` reloads repaired ordinals because an old-binary insert bumps `meta.seq`; repair failures propagate, so a zero ordinal is not served; the new SQL uses constructs the SQL Server adapter supports (`COUNT(*)`, `executemany`, `audit.seq`).
* Residual (Medium, routed to later work, not corrected here): the loopback guard covers the two fixtures named in the finding (`MssqlPriorityOrder`, `MssqlResidentControls`); about twenty other test modules that read `ZF_SQL_SERVER` are unguarded. A shared setup guard is a candidate follow-up and out of this issue's scope.

## Routing

* Native SQL Server red/green, ledger migration, SQL Server scale: next admitted heavy run.
* FULL local gate, receipt verification, independent exact-head review, hosted CI: coordinator.
* Data-owner decision on recorded ambiguity: human.

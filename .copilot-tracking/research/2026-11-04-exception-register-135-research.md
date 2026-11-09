---
title: Exception register research (#135)
ms.date: 2026-11-04
---

## Disposition

Research executed. Planning Readiness: Ready.

## Delivered by merged PRs (do not redo)

* #666: `exception_queue.py` (owned queue, role scope, audit, outage banner, no replay).
* #868, #1007, #1025, #893: read-only feeds for AI runs, stranded tasks, imports, stock conflicts, handoffs.
* #654: web data steward and operator screen (per-home, read-only, both source values).
* Issue comment 2026-11-03: unmet are importer producer, store/API/staff UI, outage state in product, owner approval of roles and runbooks.

## Finding

Nothing calls the feeds; no endpoint returns the queue. `src/api/.../server.py` has no steward route.

## Acceptance criteria status before this slice

* Conflicting values with source, date, version and owner: module only.
* Failed imports, model calls, stranded tasks in an owned queue: module and feeds only, not live.
* Controlled audited recovery: module only; not exposed.
* Unresolved eligibility and original source: module only.
* Scoped visible access and honest outage state: module only; nothing shown to staff.

## Smallest slice

Read-only `Store.exception_register` plus `GET /api/exceptions`, wiring the existing feeds to live records with named staff from configuration. Owner role naming stays open, so nothing is assigned by default. Not infrastructure, SQL, security change or deployment: focused tier.

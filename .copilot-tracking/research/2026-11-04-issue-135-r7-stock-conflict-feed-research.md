# Research: issue 135 round 7, stock conflict feed

Date: 2026-11-04. Disposition: executed (repo, PR history and issue closure audit read).

## Already delivered

* PR 666: core `ExceptionQueue` (conflicts with source, date, version and owner; audited recovery with no replay; outage banner; scoped access).
* PR 868 and later: failed AI run, stranded task and unaccepted handoff feeds.
* PR 1007: failed import feed.
* Issue #84 delivered stock conflict queries (`stock.py`: both assertions with source_id, date, version, owner; terminal events). Nothing routes them to the steward queue.

## Unmet

* No conflict producer (`source_conflict` and `identity_conflict` never raised from real records), no integration producer, no store, API or UI, roles and runbooks not owner-approved.

## Slice

`feed_stock_conflicts` in core: read-only, raises a `source_conflict` item for each unresolved stock query on an open home. Locally testable, no SQL, infra or security surface, so the focused tier applies. Planning Readiness: Ready.

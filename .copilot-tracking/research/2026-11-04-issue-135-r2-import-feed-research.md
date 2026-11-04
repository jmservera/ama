# Research: issue 135 round 2, failed import feed

Date: 2026-11-04. Disposition: executed (repo and PR history read).

## Already delivered

* PR 666: `ExceptionQueue` (core): conflict values with source, date, version and owner; owned failure queue; audited recovery requests with no replay; outage banner; scoped access report.
* PR 868: feeds for failed AI runs, ownerless overdue tasks and unaccepted handoffs.
* Later work on `exception_feeds.py` adds the handoff feed (r1 follow-up).

## Unmet (from the r1 review)

* No importer producer (`failed_import` has no feed).
* No store persistence, API or UI; no integration or conflict producer; roles and runbooks not owner-approved.

## Slice

Add a read-only `feed_failed_imports` in core reading importer batch records (rejected) and refused file records. Locally testable; no API, SQL, infrastructure or security surface, so focused tier applies. Planning Readiness: Ready.

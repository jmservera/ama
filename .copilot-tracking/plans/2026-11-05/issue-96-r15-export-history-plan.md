---
title: Issue 96 r15 export review-history plan
description: Prospective plan, paused at the checkpoint gate before implementation
ms.date: 2026-11-05
---

## Status

PAUSED at Plan. Phase 1 (Research) is complete. Implementation, changes and Review phases are not started and are not claimed. Details: [issue-96-r15-export-history-details.md](../../details/2026-11-05/issue-96-r15-export-history-details.md).

## Phases

* [x] Phase 1: Research, identities, contract compatibility, checkpoint gate assessment.
* [x] Phase 2: Plan and details written before any feature edit.
* [ ] Phase 3: Implementation. BLOCKED on the checkpoint disposition; resume only after the coordinator releases it.
* [ ] Phase 4: Review. Not started.

## Decisions

* Adopt required-history manifest only after checkpoint disposition; legacy copies Invalid, regenerate-Held recovery, no backfill.
* Tier FULL, deferred: fresh images, current main, new external output, independent exact-head and published review. No reuse of receipt `07ae`.
* Light checks only for the later implementation: the four form suites on JSON and SQLite, Ruff check/format, mypy, external caches.
* Out of scope: reviewed-pack approval, approved-schema registration, rule/calculation engines, endpoints/UI, signatures, eligibility, submission.

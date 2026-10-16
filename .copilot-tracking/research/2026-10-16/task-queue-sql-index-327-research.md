---
title: SQL queue membership research
description: Owner-directed follow-up to the merged hot-cache implementation
ms.date: 2026-10-16
---

Task: #327, task-queue-sql-index-327. Research disposition: reused and extended.
Planning Readiness: Ready.

* Read issue #327 and comments first. The owner requires indexed SQL membership
  maintained on every write, retaining the merged ID cache, portable to Azure SQL.
* SqlStore._seed and save own case writes. _migrate owns derived-column upgrades.
  MssqlStore inherits the logic and translates schema/index/dialect hooks.
* Store._queue_candidates currently rebuilds every open work_context after each
  version change. _filtered applies visibility/search/filters after candidate lookup.
* Membership depends on case content, shared building/procurement context, dataset
  as_of, controls.today(), taskqueues.VERSION and the entire ranking policy.
  Building validation can depend on other linked cases.
* Preserve closed-view semantics (queue ignored), contractor denial, redaction,
  sort, cursor, export and globally ranked output. Compare against an independent
  uncached candidate selector.
* Reuse test_sqlreads.queue_cases(60000), seed 5, as_of 2026-10-16.
  This is generated fictional stock, not private or Azure performance evidence.
* Existing SQLite dialect hooks contain legacy SQLite-specific syntax; new shared
  statements must not add it. No private data, Docker, environment files or Azure
  resources are needed for the local evidence.

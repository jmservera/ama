---
title: "Critique: #146 RAI SQL restart reconstruction plan"
ms.date: 2026-11-14
task_slug: 146-rai-sql-reconstruct-0115
---

## Execution and verdict

Independent critique executed once on the final candidate plan. Verdict: proceed with applied findings.

## Findings and dispositions

* Replayed ids matching a persisted id but a different kind could inflate counts: applied; dedupe is by id only, persisted rows win.
* Oversized windows could silently truncate: applied; blocked, never partial.
* Invalid replay id or window must not yield counts: applied; status blocked, metrics null.
* Metrics must stay content-free and staff-only: applied.
* Using the hash-chained `audit` table: rejected, it has no event ids.

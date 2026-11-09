---
title: Quality sensor demo 1288 E1 author review
ms.date: 2026-11-09
---

Author Review, executed once, 2026-11-09, by a read-only `code-review` agent over the uncommitted E1 diff plus the two new files. This is not independent closure: the coordinator's independent exact-head functional assessment remains required. Refs #1288, #107.

## Execution and outcome

* Execution: executed once. Boundary: working tree against C8 `1251c1dcb`.
* Outcome: no High finding. One Medium and two Low findings, routed to later work below. They were not fixed in E1 and the Review was not repeated.
* The agent could not run SQL Server; SQL dialect checks were by reading only. Real-SQL evidence is in the handoff.

## Findings (routed, not closed)

* Medium, `assistants.py` `_due` and `_adopt`: an `incomplete-history` marker is deleted and re-searched on every observing scan, re-reading up to 100 tasks (20 pages of 5) per affected case, and never advances; only a person's request overwrites it. Cost is bounded and the state is explicit (`scan()["incomplete_history"]`), but the case gets no autonomous review until resolved. Routed: persist a paging cursor in the marker or back off, and surface the held state in case status. This is a known and recorded residual of the bounded-adoption design (the old unbounded read was the High defect).
* Low, `_resumes`: a slot adopted or migrated with `seen=''` counts the first scan as an observed change and restarts the quiet timer once; the `COALESCE_MAX` bound still applies. Routed: treat empty `seen` as no observation yet.
* Low, `_provider_sends_nothing`: any carrier setting `sends_no_bytes` skips the physical-send hold. Only a test double sets it today; production `Ai` does not. Routed: assert in the composition root that the real client never declares it.

## Verified by reading (no defect)

* F1: deadline checked before every chunk; timeout capped and restored; the `fenced` wrapper resolves `store.ai` once so the checked object is the called object.
* F2: trigger clock matches `Assistants.now`; old triggers are upgraded; gate DDL is idempotent; SQL Server dialect pieces look valid.
* F3, F4, F6: slot-owner checks, idempotent column migrations on both backends, and `review_flag` state values match what `sensor_view` emits.

## Not proven here

Independent assessment, native assistive technology, human acceptance, real-model behaviour, live or Azure SQL, and TLS-level send behaviour.

---
title: Sensor ten-test MSSQL current-main plan (issue 1297, AC2)
ms.date: 2026-11-11
---

Details: [details](../details/2026-11-11-sensor-ten-current-main-1297-2122-details.md). Research: [research](../research/2026-11-11-sensor-ten-current-main-1297-2122-research.md).

## Scope

One bounded unchanged-source observation of the ten pinned sensor MSSQL tests on one task-owned disposable loopback SQL Server. No source, test, runner or workflow edit; no full gate; no criterion ticked.

## Phases

* [x] Phase 1: pin source/base and compare the runner's ten IDs (research).
* [x] Phase 2: admit the shared heavy lock (non-blocking, actual holder), check resources, start the owned container, prove ownership and loopback binding, run the selector with zero-skip and ten-ID checks, remove the container and verify absence.
* [x] Phase 3: record original evidence, handoff and review; commit locally without push.

## Gates and stop rules

* Blocker before SQL (lock held, insufficient resources, missing Docker/image): record it and stop; do not simulate.
* A missing dependency authorizes only pinned pip after an actual import failure; never uv.
* An unexpected application or test failure is preserved and reported to the existing owner; no retry, no fix.
* Success requires exit 0, exactly the ten IDs run as `ok`, zero skipped, zero failures, and the reopened-store test executed.
* No wait on, interruption of or reuse from another lock holder, existing container or private database.

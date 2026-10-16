---
title: Source monitor retry research
description: Supplied issue and local implementation evidence for issue 332
ms.date: 2026-10-16
---

## Disposition

Task: #332 / source-monitor-retry-332. Research reused from the issue and
direct source inspection. Planning Readiness: Ready.

* src/core/src/zava_forward/core/source_monitor.py stores successful and failed
  observations in one append-only table; body.error distinguishes failures.
* due() currently uses the latest attempt rather than the latest success.
  observe() already enforces chronological attempts.
* src/orchestrator/tests/test_source_monitor.py currently expects a failed
  first attempt to suppress a next-day check. This expectation must change.
* Preserve due()'s rejection of clocks before the latest attempt, even if
  that attempt failed. No schema or dialect-specific JSON SQL is needed.
* Owner permits last-success cadence. No new retry interval or hosted timer
  is required. Retrieval success remains distinct from legal verification.
* ADR 0006 requires installed src distributions and tests outside packages.

## Boundaries

No private datasets, environment files, Azure, Docker or uv. No legal claims,
approval changes, new adapters, schema changes or source verification.

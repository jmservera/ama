---
title: Issue 79 plan, slice 4 (local publication runner)
ms.date: 2026-11-05
---

* [x] Phase 1: `ranking_publication_runner.run` and `main` over `ranking_publication` and `ranking` (schedule, publish, verify; window, run key, refusals, exit codes, exercise mode).
* [x] Phase 2: synthetic-fixture regression tests including a persisted-store round trip; mypy strict override for the new module and test.
* [x] Phase 3: core README, knowledge-base log, RPI evidence.

Details: [details](../../details/2026-11-05/issue-79-r4-details.md). Research: [research](../../research/2026-11-05/issue-79-r4-research.md).

Critique (single pass, self-run, final candidate): the runner writes only through the existing idempotent `publish`; the draft policy fails closed with `approval_missing` and exercise mode never writes. Findings applied directly: (1) a damaged archive blocks publish instead of adding to it; (2) the capacity check uses the exact record size, not an invented margin; (3) `verify` reports a stale latest publication as a problem so a missed schedule is visible. No finding conflicts with a confirmed decision and none is significant or divergent. Tier: FULL, conservatively (scheduler/publication and persisted store integration); no infrastructure, SQL schema, deployment or auth change.

---
title: Issue 2255 research, live re-verification on revision 0000054
date: 2026-11-22
---

# Research

Research disposition: reused (prior backfill evidence) plus executed (live re-probe). Planning Readiness: Ready.

* Prior note: docs/reference/research/issue-2255-backfill-2026-11-22.md (22 of 22 clocks, 6 running, 17 overdue, written to the demo SQL store, not deployment-dependent).
* Live app now serves revision ca-cutover-test-demo-api--0000054 (created 2026-11-22T23:14:23Z, image digest sha256:3f2be664...). The seeded fields live in SQL, so a new revision should keep them; the revision may change clock rendering. A read-only re-probe on this revision is the proof.
* Issue has no tick list; criteria are taken from its Expected paragraph and the prior per-criterion table.
* Tier: focused. No src change planned; no live write, no Azure resource.

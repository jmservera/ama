---
title: Issue 1288 live round 5 changes
ms.date: 2026-11-19
---

Changes: add the research note [issue-1288-live-r5](../../docs/reference/research/issue-1288-live-r5-quality-sensor-evidence-2026-11-19.md), an index row and a log entry. No source change; FOCUSED tier; rpi-checks.py not run.

| Criterion | Status for the demo | Evidence |
| --- | --- | --- |
| 3 snapshot consumes identical IDs | Proven locally (mock provider); not proven live | 272 local tests OK; no live model call |
| 4 proactive deduplicated flag | Unproven (no release record) | Local dedup tests; no live release |
| 5 employee sees finding, IDs, model, status | Proven locally; not live | No live model output |
| 6 explicit insufficient states | Proven locally; stale and unavailable seen live in round 3 | Tests; round 3 screenshot |
| 7 correlating tests | Proven as local engineering evidence | 272 tests OK, 85 skipped (SQL Server and browser) |
| 8 live walkthrough | Unproven, not provable for the demo | No simulator job, release or model call |
| 1, 2, 9 | Already ticked | Unchanged |

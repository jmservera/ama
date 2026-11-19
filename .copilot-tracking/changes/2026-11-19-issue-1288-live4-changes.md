---
title: Issue 1288 live round 4 changes
ms.date: 2026-11-19
---

Changes: add the research note [issue-1288-live-r4](../../docs/reference/research/issue-1288-live-r4-quality-sensor-evidence-2026-11-19.md), an index row and a log entry. No source change; FOCUSED tier; rpi-checks.py not run.

| Criterion | Status for the demo | Evidence |
| --- | --- | --- |
| 3 snapshot consumes identical IDs | Proven locally (mock provider); not proven live | 304 local tests OK; no live model call |
| 4 proactive deduplicated flag | Unproven (release gate held) | Local dedup tests; live no release record |
| 5 employee sees finding, IDs, model, status | Proven locally; not live | No live model output |
| 6 explicit insufficient states | Proven locally; stale and unavailable seen live in round 3 | tests; round 3 screenshot |
| 7 correlating tests | Proven as local engineering evidence | 304 tests OK, 85 skipped (SQL Server and browser) |
| 8 live walkthrough | Unproven, not provable for the demo | No simulator job, no release, no model call |
| 1, 2, 9 | Already ticked | Unchanged |

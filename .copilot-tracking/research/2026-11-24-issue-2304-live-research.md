---
title: Issue 2304 forecast live 503 on revision 65 research (2026-11-24, round 2)
ms.date: 2026-11-24
---

# Research: forecast background job takes about 70 s, so no last-good answer

Disposition: executed. Planning Readiness: Ready. Evidence note: `docs/reference/research/issue-2304-live-2026-11-24-r2.md`.

## Findings

* Revision 0000065 (stale-while-slow fix) is live. Probes show 200 responses at 8 to 9 s with `stale_seconds` growing 12, 21, 30, 38, 47: a last-good answer exists but no fresh job finishes inside the 8 s wait. One joined request answered in 3.39 s when a job finished, so the job takes roughly 60 to 80 s.
* The job is CPU-bound, not SQL-bound. A local SQLite run with 448 open cases issues only 20 statements and still takes 80 s under cProfile.
* Hot path: `_task_id` and `_due` call `release_reference` per case and capability (10304 calls), which calls `runtime_binding` and `rel.assessment`, which call `ai_registry.get`, which rebuilds the whole registry (`tasks()` -> `_entry` -> `monitoring_coverage.task_declaration`, 267969 deep copies). That is 72 of 80 s.
* The outlier values (33.77 s, 135 s AI report) are consistent with this CPU load on a 0.5 vCPU container; the AI report was handled under #2303.
* Warm-up: the cache key is per staff identity and period, and the scope depends on the signed-in user's authorisation, so a start-up warm job has no identity to compute for. With the fix a cold compute is a couple of seconds of CPU, so a warm job is not needed.

## Follow-ups

1. Owner deploys and re-measures the live forecast.
2. Optional: cache `ai_registry.tasks()` build per process.

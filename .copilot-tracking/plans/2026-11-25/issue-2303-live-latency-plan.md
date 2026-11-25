---
title: Issue 2303 latency plan (2026-11-25)
ms.date: 2026-11-25
---

Scope: cache the two report evaluations behind a bounded, named, single-flight state and warm it at server start.

## Phases

* [ ] Phase 1: add `src/api/src/zava_forward/api/eval_report_cache.py` (key = function identity plus golden SHA-256; lock; deep copy on read; `warm()` helper).
* [ ] Phase 2: use it in the `/api/ai/report` handler and start a daemon warm-up thread in `_serve`.
* [ ] Phase 3: tests in `src/api/tests/test_eval_report_cache.py` (second call does not recompute; changed golden recomputes; handler answers in under 5 s after warm-up; mutation of a returned copy does not leak).
* [ ] Phase 4: run `test_ai_tasks`, `test_ai_consumption_api`, mypy and ruff for `src/api`; record evidence and the per-criterion table.

## Success

Warm `GET /api/ai/report` under 5 s locally; existing report tests pass; Full tier gate left to the coordinator.

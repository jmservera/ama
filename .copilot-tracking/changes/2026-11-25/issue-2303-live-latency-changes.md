---
title: Issue 2303 latency changes (2026-11-25)
ms.date: 2026-11-25
---

Status: implemented. Tier FULL (src change); the coordinator runs the complete gate and receipt. `rpi-checks.py --all` was not run.

## Changes

* `src/api/src/zava_forward/api/eval_report_cache.py` (new): bounded, single-flight cache keyed by function and golden SHA-256, deep-copy reads.
* `src/api/src/zava_forward/api/server.py`: `/api/ai/report` reads both evaluations through the cache; `_serve` starts a warm-up daemon thread.
* `src/api/tests/test_eval_report_cache.py` (new) and one handler test in `src/api/tests/test_ai_tasks.py`.
* `docs/reference/research/issue-2303-report-latency-2026-11-25.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `test_eval_report_cache`, `test_ai_tasks.Endpoints`, `test_ai_consumption_api`: OK (52 tests plus 4 cache tests).
* `python3 -m mypy` (src/api): no issues; ruff check and format check clean on new files.
* Cold fill 1.7 s, repeat 0.002 s locally.

## Divergence

The warm-up helper lives in `server.py`, not the cache module, because the strict mypy config cannot import `zava_forward.agents` from a typed module.

## Residual risk

A first request that arrives during the container's warm-up waits for that single computation. Live latency after the fix is unproven (not deployed).

## Per-criterion table (issue #2303)

| Criterion | State | Evidence |
| --- | --- | --- |
| 1 Regression test for missing chat golden | Proven earlier | docs/reference/research/issue-2303-live-2026-11-25-r72.md |
| 2 Dockerfile copies golden and sets `ZF_CHAT_GOLDEN` | Proven earlier | same |
| 3 Live 200 and loaded view | Proven on 0000072; post-fix live latency unproven | same; no deployment authorised |
| 4 Full tier gate and external receipt | Unproven here | coordinator owns the gate |
| Goal: report well under 5 s | Proven locally (warm 0.002 s, test asserts under 5 s); unproven live | docs/reference/research/issue-2303-report-latency-2026-11-25.md |

---
title: Issue 2303 report latency profile and fix (2026-11-25)
description: Code profile of GET /api/ai/report (73.5 s API, 93.4 s UI on revision 0000072), the cache fix and its local proof
ms.date: 2026-11-25
ms.topic: reference
---

Scope: synthetic demo, desktop only. Code profiling and local tests only; no Azure change, no deployment, no push. Refs #2303; follows [the 0000072 proof](./issue-2303-live-2026-11-25-r72.md), which recorded the slow responses.

## Cause

The handler recomputed two golden-file evaluations on every request: `ai_eval.run_eval()` (1.1 to 3.3 s on this host) and `chat_eval.run_eval()` (4 to 8 s; 33 scenarios, 117 chat asks, dominated by staff-detail redaction and store saves). The heldout suite, token comparison and registry cost under 0.4 s together. On the fractional-vCPU demo container, shared with other requests, that CPU work is consistent with the observed 73.5 s. The container itself was not profiled, so the exact multiplier is unproven.

## Fix

`src/api/src/zava_forward/api/eval_report_cache.py` holds a bounded (8 entries), single-flight cache keyed by evaluation function and golden-file SHA-256, returning deep copies. The handler reads through it, and `_serve` warms it in a daemon thread at start. The response shape is unchanged.

## Local evidence

| Check | Result |
| --- | --- |
| Cold fill of both evaluations | 1.7 s (this host, unloaded) |
| Repeat reads | 0.002 s |
| `test_report_repeat_request_reuses_evaluations_and_answers_within_five_seconds` | passes; fails if the handler recomputes (scenario runners patched to raise) |
| `test_eval_report_cache` (4 tests) | pass: reuse, copy isolation, golden change recompute, bound, missing golden still raises |
| `test_ai_tasks.Endpoints` and `test_ai_consumption_api` | 52 tests OK |
| `python3 -m mypy` in `src/api`; `ruff check` and `ruff format --check` on new files | clean |

## Per-criterion table (issue #2303)

| Criterion | State | Evidence |
| --- | --- | --- |
| 1 Local regression test for the missing chat golden | Proven (ticked earlier) | [r72 note](./issue-2303-live-2026-11-25-r72.md) |
| 2 Dockerfile copies the golden and sets `ZF_CHAT_GOLDEN` | Proven (ticked earlier) | r72 note |
| 3 Live 200 and loaded Asset and board view | Proven on 0000072 (earlier); the speed fix is not deployed, so live latency after the fix is unproven | r72 note; no deployment was authorised in this task |
| 4 Full tier: complete local gate and external receipt | Unproven here | `src` changed, so FULL applies; `rpi-checks.py --all` was deliberately not run; the coordinator owns the gate and receipt |

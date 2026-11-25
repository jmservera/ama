---
title: Issue 2303 latency plan details (2026-11-25)
ms.date: 2026-11-25
---

## Phase 1 details

`EvalReportCache.get(func, golden_path)` returns `copy.deepcopy` of the cached value. Key: `(func, sha256(golden bytes))`; golden unreadable raises the underlying error unchanged (the existing 500 path and the Dockerfile contract test stay valid). One `threading.Lock` makes computation single-flight. Entries are bounded to 8 keys (oldest dropped) so tests that patch the function do not grow state.

## Phase 2 details

Handler replaces `ai_eval.run_eval()` and `chat_eval.run_eval()` with cache reads, passing the module attribute at call time so patches apply. `_serve` starts `threading.Thread(target=warm, daemon=True)` after `app.assistants.start()`; warm failures are logged and ignored (first request then computes and raises as before).

## Phase 3 details

Tests use a counting stub for the cached function and a temp golden file; the handler timing test reuses the `test_ai_tasks` HTTP harness.

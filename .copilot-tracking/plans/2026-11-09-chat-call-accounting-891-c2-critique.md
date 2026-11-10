---
title: Issue 891 chat call accounting C2 critique
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c2
---

## Execution

One critique by a read-only `rubber-duck` subagent before any test or source edit. Verdict Revise (2 blocking, 1 significant). Dispositions applied directly; no second critique.

* PC-001: the suite alone restores the original; the leaked started patch is unwound by `mock.patch.stopall()` AFTER the allowing patch, leaving a stale mock. The regression runs in a subprocess: load only `DispatchWitness`, run it, assert the guard is original, call `patch.stopall()`, assert original again, then run `test_ai_input_bounds`. Research corrected below.
* PC-002: the subprocess test selects `test_ai_dispatch_marker.DispatchWitness` explicitly (not the whole module), plus `test_ai_input_bounds`, with a timeout; it lives in a separate class not selected by the subprocess.
* PC-003: the pins assert `DispatchWithdrawn` from stubbed `.open`, one hand-off, one stub invocation, and the outcome (`suspended-before-dispatch`, `timeout`, `provider-unavailable`).

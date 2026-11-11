---
title: Issue 144 main-based slice A port critique
description: One-time self-critique of the E1 plan with dispositions
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Execution

Executed once, as a self-critique (new agents are not authorized). Verdict: proceed with the bounded plan.

## Findings and dispositions

| Finding | Disposition |
| --- | --- |
| Refactoring `fence_send` into a shared helper touches a main safeguard | Accepted with limits: same checks, event and restamp; existing fence tests and `test_assistants.py` must pass unchanged |
| Captured-readings refusal ignores the in-process carrier | Accepted as fail closed; the contract says a real client never carries them |
| Permit restamps the attempt to `sending` before the worker sends | Accepted; mirrors `fence_send`; a never-sent permit leaves the slot held until `active_until`, which is safe |
| Real-SQL lock-crossing tests are not ported or run | Accepted; unobserved gap, reported; deterministic clock test on SQLite substitutes only for logic |
| `complete_result` has no B caller yet | Accepted; it settles the permit meter and prevents unsettled liability |
| Dispatch digest hook dropped | Accepted; deferred with B |
| Ambiguity in consent semantics | Resolved fail closed, no approval invented |

No finding conflicts with a confirmed decision.

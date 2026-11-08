---
title: Issue 164 F2 post-implementation Review
description: One Review of the memory probe scope reporting correction, original outcome preserved
ms.date: 2026-11-08
---

Execution: Complete (one pass, code-review agent, read-only, over the uncommitted diff of `chat_eval.py`, `test_chat_eval.py` and `src/agents/README.md`). Outcome: Residual work (two Medium findings, no outcome change found). Author-side review plus the agent; not the independent exact-head assessment the coordinator still owns. No second Review runs in this task and no finding was fixed in it.

## Findings (original, unaltered)

* RV-001 (Medium): `ChatPanel` sets `memory_used=False` as a literal (`chat_panel.py:402`, also `server.py:911`), not computed from consumed inputs. `memory_scope` therefore proves "not exercised" only as far as that declared receipt field does, and the README phrase "only when receipts support it" overstates it. Route: later user-selected Plan/Implement: soften wording to "receipts declare memory_used false" or cross-check the assembled prompt. Until then the serving statement is receipt-declared, not independently observed (the golden `prompt_forbid` on the seeded text is the only independent check, on one scenario).
* RV-002 (Medium): `memory_scope` pools receipts across scenarios; a scenario that fails by exception leaves missing receipts yet other scenarios' complete receipts still produce "not exercised". Route: later work: report unknown when any scenario ended unexpectedly or receipts are fewer than executed turns. Not reachable with the current golden file, which passes with zero failures.

## Other observations

* Outcome preservation was checked by base-versus-after JSON comparison with the new fields removed (changes record), and held by the 53-test focused run.
* Remaining gaps: hosted CI at the actual head and independent exact-head assessment; #108 and #159 dependencies, held-out, RAI, human, permission and actual-serving-model criteria stay unmet; #164 is Refs only and no criterion is ticked.

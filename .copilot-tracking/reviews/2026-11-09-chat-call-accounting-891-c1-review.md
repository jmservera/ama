---
title: Issue 891 chat call accounting C1 review
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c1
---

## Execution

* One post-implementation Review, run once by a read-only `code-review` subagent on source commit `f466f4997` after the changes record existed. No second review.
* Boundary assessed: `src/core/src/zava_forward/core/ai.py`, `src/agents/src/zava_forward/agents/chat.py`, their tests and the agents README. The subagent also ran `test_ai_dispatch_marker` and `test_chat_model` (21 tests, 23 subtests, pass).
* Outcome: conformant, no blocking finding. The subagent did not read the plan or critique, so accepted-limit conformance was judged from code, tests and README.

## Findings (all non-blocking, routed as follow-ups; none applied in this task)

* R1 a provider that wraps `Ai.evidence` and makes extra calls leaves `witnessed=True` with an undercount: the documented composition trust boundary.
* R2 no test pins fence withdrawal raised from the opener's `.open` as one attempt (documented behaviour, untested).
* R3 the provider-failure test exercises only `OSError`; `TimeoutError` and `HTTPError` take the same increment-first path.
* R4 the unverified fallback shows only as a log; the receipt reads as exact. Needs a provenance field in shared `chat_panel.py` (also critique PC-002).

## Routing

Later user-selected work: receipt provenance (R4/PC-002, needs `chat_panel.py` ownership), the withdrawal and error-type tests (R2/R3). No transition back to Implement or Review inside this cycle.

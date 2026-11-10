---
title: Issue 891 chat call accounting review
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109
---

## Execution

* One post-implementation Review, executed 2026-11-09 at 22:43Z by an independent read-only `code-review` subagent over source commit `da1c49a1c` (base `a04668ae9`) and the RPI evidence. Not repeated.
* Assessed boundary: `src/agents/src/zava_forward/agents/chat.py`, `src/agents/tests/test_chat_model.py`, `src/agents/README.md`. The reviewer ran `test_chat_model` (13 OK) and found no non-ASCII text.

## Outcome

* Conformant. No blocking and no significant finding. Independent verification: `meter_id` is written right after `reserve` and before the transport, so `provider_calls` cannot under-report a real transport; without `meter_id` a hold comes only from the missing meter or `reserve`; `model-mismatch`, `timeout`, `provider-unavailable` and `returned` correctly count 1. README scope is appropriate and disclaims criterion 2.

## Non-blocking findings (routed as later work, not applied in this task)

* N1 In two tests the transport-count assertion sits in a `finally` inside `assertRaises`; assert after the `with` block for clarity.
* N2 `metered_model` starts patches stopped only by `tearDown`; use per-test `addCleanup`.
* N3 The input-refusal test stubs the envelope instead of driving the real `Ai`; acceptable, because `Ai.evidence` raises `InputRefused` before `reserve`.

## Routing

* N1 and N2 are test-hygiene follow-ups for a later user-selected task; no cycle spent (0 of 5). The reviewed commit stays unchanged so the review applies to the exact source head.
* Remaining limitations (unchanged): `dispatch_check` hold and guard-denial over-counts need a core transport marker (coordinator-serialized `core/ai.py`); criterion 2 conjunction not established; independent exact-head assessment, human approval and hosted CI remain required.

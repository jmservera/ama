---
title: Issue 891 chat call accounting C1 details
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c1
---

## Step 1 core marker tests (red first)

New `src/core/tests/test_ai_dispatch_marker.py`, real `Ai`, `urllib.request.urlopen` patched with a counting stub, `_token` patched, guard patched to allow, synthetic ledger with reserve, check and complete outcomes. Assert witness attempts equal the stub call count for:

* unconfigured client: witnessed, 0
* meter missing, reserve held, `dispatch_check` hold, token failure, guard denial, input refusal: 0
* response success, transport error, response then completion hold: 1
* a witness opened in two threads with distinct outcomes (one success, one pre-dispatch hold) keeps separate counts
* no open witness: `Ai.evidence` still works and marks nothing

## Step 2 adapter tests (red first)

In `src/agents/tests/test_chat_model.py`, replace the parent heuristic tests with transport-counted tests of `ChatModel` and the real `ChatPanel` receipt: the same case table as Step 1 expecting reported calls equal to the stub count; a worker whose provider returns a spoofed `meter_id`, `outcome` and any dispatch-like key without being core `Ai` yields the unverified conservative 1 and a log line without provider text.

## Step 3 core change

`ai.py`, near `InputRefused`: add `DispatchWitness`, `DISPATCH` ContextVar, `count_dispatches`. In `evidence`, first statement: mark the open witness as witnessed. In `_request`, directly before `open_request = ...`: `witness = DISPATCH.get()` and increment `attempts` when present, at the line that precedes the `with open_request(...)` call so a failure to open is still an attempt.

## Step 4 adapter change

`chat.py`: remove `provider_calls` and the `typing.Any` import if unused; open `count_dispatches()` around `worker.provider_call`; compute `calls`; log the unverified case with `logging.getLogger(__name__).warning`.

## Step 5 docs and checks

README counting-rule section rewritten to the witness contract with its residual limits. Then run, with the owned venv: agents `test_chat_model`, `test_chat_model test_dispatch test_worker`, `test_chat_*`, full agents suite; core `test_ai_dispatch_marker`, `test_ai_input_bounds`, `test_ai_consumption*`, `test_chat_panel`, `test_*demo*`; API `test_ai_call_site_inventory`, `test_chat_panel`, `test_chat_isolation`, `test_ai_consumption_api`, `test_continuity` and `test_quality_simulation_lane` only if `simulation_lane` use of `evidence` could be touched (it is read-only, so run it as an impacted check). `ruff check`, `ruff format --check`, `mypy` for core and agents.

## Amendments from the critique

* Step 1 also tests: nested witnesses (inner counts only its own invocation), an increment after the witness is closed is ignored, a context copied into a thread while open counts into that invocation, an `evidence` call followed by an independent transport call is documented as outside the witness (composition boundary), and opener construction failure is zero.
* Step 3 placement: increment after `open_request = ...` is built and directly before `with open_request(req, timeout=timeout)`.

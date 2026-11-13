# Research: #432 chat failure meter forwarding (Agents half)

Disposition: executed. Planning Readiness: Ready. Required docs (case study, addendum, reference README, memory) read at start.

## Findings

* `core/ai.py` `Ai._request` writes `meter_id`/`meter_root` into the evidence envelope (`receipt.update`) right after `reserve`, before dispatch. `Ai.evidence` catches every failure and returns that same envelope, so timeout/provider-unavailable/financial-held envelopes keep the ids. No core edit needed.
* `AgentWorker.provider_call` returns the provider dict unchanged on success paths; only a raised exception or non-dict yields `FAILED_ENVELOPE` (no ids exist then). `_bounded` timeout also yields a fresh envelope; ids unrecoverable there (out of scope, recorded as residual).
* Gap: `ChatModel.__call__` raises `ModelUnavailable` on post-dispatch failures without `meter_id`/`meter_root`. `ModelUnavailable.__init__` at base has no such kwargs (sibling adds them), so set attributes on the instance.
* Pre-dispatch denials stay `calls=0`, ids None.

## Decision

Edit only `agents/chat.py` plus `agents/tests/test_chat_model.py`.

---
title: Issue 891 chat call accounting research
ms.date: 2026-11-09
---

## Task identity and scope

* Task `issue-891-chat-call-accounting-1109`, slug `chat-call-accounting-891`. State `.copilot-tracking/rpi-sessions/2026-11-09/chat-call-accounting-891-state.json`.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-891-fresh-accounting-1109`, branch `fix/demo-chat-call-accounting-891-1109`, base and target `main` `a04668ae94b5c2f38e6c55ed789db245e8c71d16`. Clean tree at start (`git status --short` empty).
* Fresh prospective loop owned by this session (research, plan/details, critique, implement, review, in order). Author Sonnet 5.5. Correction cycles: five total, none spent at research time. The Quality1288 grant and the GPT fallback do not apply.
* Requirements data: the owner brief of 2026-11-09 ("Proceed with fresh prospective RPI remediation") and #891 criterion 2 (per-call gate, token/cost admission, privacy refs, retention and refusal stay in force, still unticked). Refs #891 only. This work cannot establish the criterion 2 conjunction.
* Historical candidate `7a5cf8d` is not admissible (preserved C1/C2 records show source edited before stage activation and critique skipped). It was not opened for this research. It stays an untrusted hypothesis to be read, if at all, only after the independent findings below are recorded. No old artifact is relabelled.
* Read first: the external `demo-capacity-rpi-common.md`, repository instructions, `docs/case_study_48_original.md`, the addendum and `docs/reference/README.md` indexes (searched for #891 and call accounting, not read end to end), `docs/reference/memory.md`, and the agents, core and API READMEs for consumption and chat provenance.

## Chronology (actual UTC, 2026-11-09)

* 22:32:24 session start. Research stage active. No source edited.
* 22:34:36 isolated venv `/home/azureuser/source/ama-demo-wt/venv-891-1109` created with `python3 -m venv`; `pip install -e src/core -e src/agents` plus `ruff==0.17.1` and `mypy==2.4.0` (the globally installed `zava-forward-*` editables point at the primary checkout `/home/azureuser/source/ama`, so they cannot test this worktree). No uv, no PYTHONPATH source hack.
* 22:35 external throwaway probe `/tmp/891-fresh/repro.py` (outside the repository, not committed) run against unmodified source. Raw log retained at `/tmp/891-fresh/repro-before.log`.

## Counting contract found in source (read at the base, then probed)

* Panel (`core/chat_panel.py` `ChatPanel.ask`): sets `receipt["model_calls"] = 1` before the model callable, then overwrites it with `ModelReply.calls` on success or `ModelUnavailable.calls` on a typed failure (default `calls=0`). `ModelReply.calls` defaults to 1. The receipt is also the `chat.turn` audit detail. A model call that never reaches transport must therefore not be reported as 1 by the adapter.
* Adapter (`agents/chat.py` `ChatModel.__call__`): returns 0 for the admission-denied paths (`ModelUnavailable` default), but after `worker.provider_call` computes `calls = 0 if envelope.get("outcome") == "disabled" else 1`. Every other outcome, including `financial-held`, `input-refused` and a guard-denied `provider-unavailable`, counts one.
* Provider (`core/ai.py` `Ai.evidence`/`_request`) order of effects: prompt-output guard (`data_protection.dispatch_hold`, raises `DispatchDenied`), input bound (`InputRefused`), meter presence (`DispatchHeld("financial-meter-unavailable")`), `consumption.reserve` (raises `DispatchHeld` for authority, price, budget and call-limit holds), then `receipt.update(meter_id=rid, ...)`, `_token()`, `consumption.dispatch_check(rid)` (raises `DispatchHeld`), and only then `urllib.request.urlopen` (the transport). After a response, `receipt` gains `usage` and `returned_model`, then `consumption.complete(...)`. `evidence` maps `DispatchHeld` to `outcome="financial-held"` with the reason, `InputRefused` to `input-refused`, `TimeoutError` to `timeout`, any other exception to `provider-unavailable`.
* `Consumption._read` can raise `DispatchHeld("meter-capacity-reached" | "meter-evidence-invalid")` and is called by `reserve`, `dispatch_check` and `complete`. `complete` therefore can raise a financial hold AFTER a successful transport, and the `except Exception` block calls `complete` again, which raises the same hold again. That hold surfaces as `financial-held` with a transport already made.
* `meter_id` is the durable provenance that the reservation exists: `_request` sets it immediately after `reserve` returns, and no transport can happen before that. A `financial-held` envelope without `meter_id` was held by the missing meter or by `reserve`, both before any transport.

## Reproduction on current source (probe run 22:35, unmodified tree)

Each row stubs the allowing admission callback and uses the real `Ai` with a counted `urlopen` patch, `_token` patched, so transport is observed directly. `ChatModel.calls` is what the panel records.

| Scenario | Transport count | ChatModel calls | Envelope outcome / meter_id / returned_model |
| --- | --- | --- | --- |
| Meter missing (reported discrepancy) | 0 | 1 | financial-held, no meter_id, none |
| Reserve held (`authority-unknown`) | 0 | 1 | financial-held, no meter_id, none |
| `dispatch_check` held (`liability-unknown`) | 0 | 1 | financial-held, meter_id, none |
| `complete` held after transport returned | 1 | 1 | financial-held, meter_id, returned_model |
| Transport failed, then `complete` held | 1 | 1 | financial-held, meter_id, none |
| Transport failed, ledger fine | 1 | 1 | provider-unavailable, meter_id, none |
| Prompt-output guard denied | 0 | 1 | provider-unavailable, no meter_id, none |

Raw output: `/tmp/891-fresh/repro-before.log` (preserved outside the repository).

## Findings

* F1 Reproduced: with the meter absent (or `reserve` held) the transport records zero calls and `ChatModel` reports 1. The panel receipt and the `chat.turn` audit then overstate provider calls. This is an over-count in a receipt; it does not show an admission bypass, any spend or that every financial hold is pre-dispatch.
* F2 Not every financial hold is pre-dispatch. Row 4 and row 5 made a transport call and a later ledger step held. A blanket `0` for `financial-held` would under-report real attempts, which is the worse error for cost and privacy accounting. Rejected.
* F3 The row 3 (`dispatch_check`) hold is also pre-transport but is indistinguishable in the envelope from row 5 (transport failed, then complete held): identical outcome, reason class and `meter_id`. Exact attribution needs a transport marker set by `Ai._request` between `dispatch_check` and `urlopen`. That marker lives in `core/ai.py`, a shared CoreAI path the owner brief forbids touching without reported overlap and coordinator serialization, so it is not done here. The conservative result is to keep counting 1 whenever a reservation exists (never under-report an attempt).
* F4 The prompt-output guard denial (row 7) is also an over-count but is indistinguishable at the adapter from a worker-caught provider exception (`FAILED_ENVELOPE` has no `meter_id` either). It is not fixed by this change and is recorded as a limitation; the same core-owned marker would resolve it.
* F5 Existing tests assert `calls` for `disabled`, admission denial, completion revocation (calls 1 with usage), and callback-exception receipts vs provider and audit. None covers `financial-held`.
* F6 Default-deny and disclaimer behaviour are outside the counting path: `server.chat_admission` and `ai_registry` own default deny and the demo activation switch; the panel owns the disclaimer and the model-generated label. Existing core, agents and API tests cover them and must remain green; they are re-run, not changed.

## Smallest correct scope

* Source: `src/agents/src/zava_forward/agents/chat.py` only. Treat a `financial-held` envelope with no `meter_id` as provably pre-dispatch (`calls=0`), keep `disabled` at 0, and keep 1 for every other outcome and for a held envelope that carries a reservation. This reuses the existing envelope provenance and needs no new field, no core, server, store, schema or Quality change.
* Tests: `src/agents/tests/test_chat_model.py` (dedicated lane): adapter cases for both sides of the boundary plus one integration of the real `Ai` with a counted transport and the real `ChatPanel` receipt and audit entry.
* Docs: a short statement of the counting contract and its limitation in `src/agents/README.md` (consumption provenance section).
* No dependency changes, no SQL or browser service, no provider, network or Azure.

## Limitations (recorded in advance)

* Criterion 2 stays unticked and the whole issue stays open. The brief's conjunction (per-call, token, cost, privacy, retention and refusal) is not established by a counting-contract fix.
* F3 and F4 over-counts remain until a coordinated core transport marker exists. They err toward reporting a possible attempt, not toward hiding one.
* The probe uses stubs; no real provider, model, network, Azure or spend happened.

## Disposition and readiness

* Research executed (this session, 22:32:24 to 22:35:40). Planning Readiness: Ready. Overlap report: none with 132, 133, 135, 1238 or Quality1288 (agents adapter, its test file and the agents README only); the core marker is reported as a recommended follow-up needing coordinator serialization, not done here.

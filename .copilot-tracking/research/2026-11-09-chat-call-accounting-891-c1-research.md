---
title: Issue 891 chat call accounting C1 research (transport marker)
ms.date: 2026-11-09
---

## Task identity and scope

* Task `issue-891-chat-call-accounting-1109-c1`, slug `chat-call-accounting-891-c1`, parent `issue-891-chat-call-accounting-1109` (head `fb972548480ed83a3c2855e4bae1f1c1f1793f93`, preserved unchanged). State `.copilot-tracking/rpi-sessions/2026-11-09/chat-call-accounting-891-c1-state.json`.
* Corrective cycle C1 of five total (counter 1/5). Same worktree and branch, still unpublished. Author Sonnet 5.5.
* Original research, plan, critique, changes and review of the parent loop, including the honestly recorded implementation-state bookkeeping lag, are not edited.
* Refs #891 only. Criterion 2 stays unticked; this cannot establish its conjunction.

## Main, merge and overlap

* Fetched `origin/main` at 2026-11-09T22:52:31Z: `1b7a1719bee088ce2823bff45242e319bc928295` (Quality PR 1331 merged). Previous base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`.
* Merged `origin/main` into the private branch at 2026-11-09T22:52:34Z with a normal merge (no rebase or force): merge commit `97f0036b573f8d0497c0d67904506f8156c11920`, no conflicts. Neither `chat.py`, its tests nor the agents README changed on main, so the 891 intent and the Quality intent do not collide.
* Coordinator explicitly admits minimal `core/ai.py` transport-marker work for 891 and owns the Core marker and Agents tests. Nothing under server, navigation, store, schema, activation or registry is edited.

## Merged CoreAI contract (read from source)

* `Ai._request` order: simulation seal, prompt-output guard (`DispatchDenied`), input bound (`InputRefused`), meter presence (`DispatchHeld`), send fence, `consumption.reserve`, `receipt.update(meter_id=...)`, then a `try`: `Request` construction (calls `_token`, an identity call, not the provider), `consumption.dispatch_check(rid)`, `open_request(req)`, read, `consumption.complete`.
* `open_request` is `urllib.request.urlopen` or, when a send fence exists, `ai_transport.opener(fence, timeout).open`. That call is the only place a provider request can leave the process. The fenced opener runs the fence at connect and again at the first request byte, so a withdrawn fence can end it before any byte.
* `Ai.evidence` maps `InputRefused`, `ModelMismatch`, `SimulationRefused`, `DispatchWithdrawn`, `DispatchHeld` and any other exception (including `DispatchDenied`, `ValueError`, `OSError`) to a bounded envelope. `DispatchDenied` and a `dispatch_check` hold after reservation both end in `provider-unavailable`, and a `complete` hold after a real call ends in `financial-held`. So outcome plus `meter_id` cannot distinguish pre-dispatch from post-dispatch.
* `AgentWorker.provider_call` runs the provider callable synchronously on the calling thread and returns whatever dict it gets. Any provider can put any key into that dict, so an envelope key is spoofable metadata.
* Contextvars already carry per-invocation state in this module family (`ai_consumption.CURRENT`, `SEND_FENCE`, `SIMULATION_SEAL`).

## Reproduction on merged source (red evidence)

Throwaway probe `/tmp/891-c1/probe.py` (outside the repo; log `logs-891-fresh-accounting-1109/c1-research-probe.log`, not committed) with the real `Ai`, a counted `urlopen` stub and the existing synthetic ledger:

| Case | Transport calls | `ChatModel` calls |
| --- | --- | --- |
| `dispatch_check` hold after reservation | 0 | 1 (wrong) |
| prompt-output guard denied | 0 | 1 (wrong) |

The parent fix still reports both as 1, which its changes record states as known conservative residuals.

## Findings

* Root cause: the adapter infers the transport boundary from the envelope, which has no record of it. Another meter heuristic would stay inexact.
* Smallest root fix: record the dispatch attempt where it happens, in `Ai._request` immediately before `open_request(...)` is called (after `dispatch_check`, `_token` and the send fence). Count an attempt there, so provider failure, refusal and a later completion hold are all counted, and every earlier exit is zero.
* Trust channel: an envelope key can be spoofed by a provider and a shared field or counter on `Ai` would race between concurrent calls. A per-invocation witness held in a `ContextVar` opened by the caller (`with count_dispatches() as witness`) is written only by core `Ai` code and cannot be set by a provider callable; concurrent invocations in separate threads or tasks get separate witnesses.
* Unsupported provenance: only `Ai.evidence` marks the witness as `witnessed`. A provider that is not core `Ai`, or one that runs on another thread, leaves it unwitnessed. The adapter must then say the count is unverified and not report exact zero. Conservative value 1 (an attempt is assumed), logged without prompt or provider text.
* Residual limit that stays: with a send fence, the opener may be withdrawn at connect or first byte before any request byte leaves. The marker counts the hand-off to the transport as an attempt (conservative). Finer exactness needs a transport-level marker in `ai_transport.py`, which is out of this scope.
* Unchanged boundaries: financial reserve/complete/dispatch_check semantics, the prompt-output guard, the input bound, admission and default deny, disclaimers, privacy and retention. No transport, SDK or network call in tests.

## Planning Readiness

Ready. Research disposition `executed`.

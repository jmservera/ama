---
title: Issue 107 R1 agents dispatch details
ms.date: 2026-10-15
---

## Phase 1: core seams

* `assistants.build_request(task, limits)` returns `(system, prompt)` exactly as `execute` builds them today.
* `assistants.shape_result(task, result, limits)` returns `(envelope, output, failure)`; it is the block of `execute` after the provider returns, unchanged (safe fields only, usage validation, output validation, `source` set to `unverified` on failure).
* `Assistants.__init__(store, env=None, provider=None)`; `self.provider = provider or (lambda *a: self.store.ai.evidence(*a))` so tests that replace `store.ai` keep working.
* `execute` calls the two helpers and `self.provider`; no other behaviour changes.

## Phase 2: `agents/dispatch.py`

* `TaskMessage` frozen dataclass with `from_task(task, limits)`, `to_json`, `from_json` and bounds checks (size, required keys). Carries only the permitted inert snapshot already sent to the provider; no staff, resident or secret fields.
* `ResultMessage`: envelope, output, failure, task id, fence, owner; `approved` stays false; JSON round trip.
* `Provider` Protocol `(system, prompt, max_tokens, timeout) -> dict`; `foundry_provider(ai)` adapter.
* `AgentWorker(provider, active_calls, timeout)`: `call(system, prompt, max_tokens)` runs the provider in a daemon thread with a bounded semaphore, watchdog and stop event, returns the raw envelope (timeout, shutdown, malformed outcomes); `handle(message)` builds the result via `shape_result`.
* `TaskQueue` and `ResultSink` Protocols plus in-memory implementations; `run_once` receives one message, handles it and posts the result, acknowledging only after the post succeeds, otherwise leaving it for redelivery (poison handling is #144).
* No SQL, blob, Key Vault or `os.environ` secrets; the worker never mutates a domain record and never approves.

## Phase 3: composition

The API keeps in-process leases and review in SQL; it passes `AgentWorker.provider_call` as the provider so the provider call lives in `agents`. `server.py` change is one line.

## Phase 4: tests

Fake provider; cases: valid output, timeout, malformed text, oversize, forbidden text, uncited finding, provider exception, slot exhaustion, stop before dispatch, round trip, redelivery on failed post, no raw text on failure, envelope `approved` false.

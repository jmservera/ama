---
title: "#164 wire call authorization into chat_eval.Run"
ms.date: 2026-11-13
---

Research disposition: executed (code read of `src/agents/src/zava_forward/agents/chat_eval.py`, its tests and the independent review of `6a4eada14`).

## Evidence

* `_count` and `_amount` accept 0, so `AuthorizedModel(tokens_per_call=0, spend_per_call=0)` never consumes ledger tokens or spend.
* `Run.__init__` takes any `model`; only `Scripted` is built by the harness, so the gate is optional.
* `AuthorizedModel.__call__` reserves the declared bounds and never reads provider usage.

## Selected approach

* `AuthorizedModel` rejects non-positive bounds at construction (`ValueError`) and at call time (fail closed).
* `Run` accepts `model`, plus `authorization` (dict, bounds, optional ledger and clock). Any model that is not `Scripted` or an `AuthorizedModel` is wrapped, or refused with `ValueError` when no authorisation and bounds are supplied.
* Providers may expose `last_usage` (`tokens`, `spend`). The gate charges `max(reserved, actual)`, treats malformed usage as a breach, re-checks the limits and halts the ledger fail closed, withholding the reply.
* Out of scope for this slice (recorded follow-ups): persisted shared ledger and verifiable owner evidence.

## Planning Readiness

Ready.

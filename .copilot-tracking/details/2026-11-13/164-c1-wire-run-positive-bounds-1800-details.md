---
title: "#164 wire gate into Run details"
ms.date: 2026-11-13
---

* Phase 1: `_positive_bounds(tokens, spend)` helper; `AuthorizedModel.__init__` raises `ValueError`; `__call__` raises `ModelUnavailable` if attributes were mutated to non-positive.
* Phase 2: `Run(sc, workdir, model=None, *, authorization=None, tokens_per_call=None, spend_per_call=None, ledger=None, clock=None)`. `Scripted` and `AuthorizedModel` pass through; any other model is wrapped with `AuthorizedModel` or raises `ValueError` without full authorisation inputs.
* Phase 3: after provider return, read `last_usage`; absent keeps the reservation; present values must be a valid count and amount. Charge `max(reserved, actual)`, re-run `call_authorization(auth, 0, 0, ...)` against the ledger; a breach or malformed usage sets `ledger.halted` and raises `ModelUnavailable` withholding the reply. A halted ledger blocks every later call.
* Phase 4: tests for zero bounds, Run wrapping/refusal, underestimate breach and halt; README sentence; ruff, mypy, three unittest modules.

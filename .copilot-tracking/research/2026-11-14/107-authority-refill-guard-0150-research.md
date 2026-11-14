# Research: ZF_ASSIST_AUTHORITY rotation refill (Refs #107)

Planning Readiness: Ready. Research disposition: executed (direct code reading).

## Evidence

* `Limits.pool` is `digest(ZF_ASSIST_AUTHORITY)`, and `assistant_allowance.id` is that digest (`assistants.py`, `Limits`, `_reserve`, `disabled`).
* `_reserve` inserted a zero-consumption row when no row existed for the current digest. Rotating the token therefore created a fresh row with `used_calls=0` and `reserved_tokens=0` and replenished the finite pool. PR #1599 tests only covered an unchanged token.
* No `consumption_allowance_version` field exists in `src/core`; the persisted allowance ledger is the only durable consumption state.
* The installed `zava-forward-*` pip packages point at another checkout; validation must set `PYTHONPATH` to this worktree's `src/*/src`.

## Decision

A new authority digest inherits the most constrained persisted ledger (MIN ceilings and expiry, MAX consumption). It fails closed and never replenishes. Same-token behaviour is unchanged.

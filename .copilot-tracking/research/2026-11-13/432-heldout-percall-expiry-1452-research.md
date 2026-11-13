---
title: Issue 432 held-out runner per-call expiry research
ms.date: 2026-11-13
---

## Research disposition: executed. Planning Readiness: Ready

Scope: `src/agents/src/zava_forward/agents/heldout_batch.py` and its tests (Refs #432, #435), observations O1, O3, O4 of review 432-runner-independent-review-1448.

## Findings

* The authorization field is `expires_utc` (not `expires_at`); `authorization_problems(auth, now)` checks it once, in `_gate_problems`, before the loop.
* `check_freeze(manifest)` runs once in `_gate_problems`. `run_batch` has a `now` parameter but no clock callable, so a long batch never re-checks expiry (O1).
* `run_batch(mode="dry-run")` calls whatever `call` is passed; only the CLI chooses `dry_run_call` (O3).
* `_gate_problems` does `p.get("id")` on each proposal and the loop uses `proposal["id"]`; a non-dict item raises AttributeError (O4). A non-sequence or non-Mapping auth/manifest is out of scope.

## Design

* Add keyword `clock: Callable[[], datetime] | None`; per-call instant is `clock()` when given, else `now`, else real UTC.
* Before each dispatch run `authorization_problems` expiry and `check_freeze`; on failure stop with `stop_reason` `authorization-expired` or `freeze-drift`, outcome `stopped`, no call made.
* Dry-run always substitutes `dry_run_call`, ignoring the supplied callable.
* Gate refuses non-Mapping proposals ("every proposal must be an object") before any `.get`.

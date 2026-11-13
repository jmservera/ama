---
title: Issue 432 per-call expiry plan
ms.date: 2026-11-13
---

## Plan and details

1. `heldout_batch.py`: add `clock` keyword to `run_batch`; helper `_dispatch_problem(auth, manifest, clock, now)` returning a stop reason (`authorization-expired` or `freeze-drift`) or None; call it before every dispatch (after the cap checks, before `call`).
2. Dry-run: `call = dry_run_call` whenever `mode == "dry-run"`.
3. `_gate_problems`: refuse non-Mapping proposal items up front and return early (avoids `.get` on them).
4. Tests: mid-batch expiry stops after N calls with no further dispatch; mid-batch freeze drift (mutating manifest via clock hook) stops; dry-run ignores a spy; non-dict items refuse.
5. Validate: targeted tests, full `src/agents`, ruff check/format, mypy in `/tmp/venv-432-percall`.

## Success

Fail-closed stops are recorded as `stopped` with the reason; existing tests unchanged.

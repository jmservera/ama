# Plan 2244 live r4 (2026-11-23)

Tier FULL (src/core change). The full gate is not run by this worker.

* Phase 1: `SqlStore._seed` counts cases read-only first and returns when populated; the locked path is unchanged and re-counts.
* Phase 2: regression test with a recording DB: a populated store issues no `BEGIN IMMEDIATE`; an empty store still does.
* Phase 3: targeted tests, mypy, ruff.

## Critique (executed once)

Verdict: compatible. Risk: two concurrent first starts on an empty database both see zero and both enter the lock; the locked path re-counts, so only one seeds. No finding conflicts with a confirmed decision. Applied directly: keep the in-lock count.

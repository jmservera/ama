# Review: issue 2245 chat ask timeout

Date 2026-11-22. Executed once. Outcome: conformant with routed follow-ups.

* The memo key covers day label, configuration and limits; failures are not cached; behaviour for the existing meter tests is unchanged (101 tests OK).
* Overclaim check: the note states the 120 s hang as unreproduced and the lock explanation as code-supported only.
* Routed follow-up 1: owner grants telemetry access to name the lock holder (earliest phase: Research).
* Routed follow-up 2: `store.dblock` is held while waiting up to 15 s for the SQL write lock, which also blocks `/healthz`; consider a shorter wait or non-blocking readiness (Plan).
* Routed follow-up 3: owner decision on SUS-1 so the model path can be timed.

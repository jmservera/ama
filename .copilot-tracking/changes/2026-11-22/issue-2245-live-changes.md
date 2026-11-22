# Changes: issue 2245 thread creation 500 (2026-11-22)

Tier: focused (test only; no src, workflow, dependency or Azure change).

## Changes

* `src/core/tests/test_chatthreads.py`: `test_thread_creation_takes_the_write_lock_at_most_twice` (SQL store). 16 SQL chat tests and ruff pass.
* `docs/reference/research/issue-2245-thread500-2026-11-22.md` plus probe folder, `docs/reference/README.md` index entry, `docs/reference/log.md` entry.

## Divergence

The test was first applied and run as a scratch edit before the implement-start witness (reverted, then re-applied after it); the witness records this qualification.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Cause of the first thread-create 500 | Partly proven | ProgrammingError class from the 15 s write-lock timeout; lock holder unproven (no telemetry access) |
| 500 fixed or verified fixed | Unproven | 12 of 12 live creates returned 200, 500 not reproduced; deployed image versus #2267 and #2273 unknown |
| Regression test | Proven | New test passes; bounds exposure only |
| Model call visible or banner states rule-based | Proven for the hold reply and banner | Live reply names the suspension; a model call needs SUS-1 lifted by the owner |
| Which skills and routes call the model | Proven earlier | docs/reference/research/issue-2245-live-2026-11-22.md |

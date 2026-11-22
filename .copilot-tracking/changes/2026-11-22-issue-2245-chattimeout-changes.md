# Changes: issue 2245 chat ask timeout

Date 2026-11-22. Status: complete. Tier: FULL (src change); the coordinator runs the gate. Local checks: `tests.test_continuity` and `tests.test_chat_panel` (101 tests OK), ruff check and format for the changed file, api mypy clean; core mypy reports three errors that exist without this change (missing opentelemetry stubs, one unused ignore). `rpi-checks.py --all` was not run.

## Files

* `src/core/src/zava_forward/core/chat_demo_meter.py`: `ensure` seeds once per day, configuration and limits per ledger.
* `src/api/tests/test_continuity.py`: regression test (fails without the change: 3 price and 3 authorize calls instead of 1 and 1).
* `docs/reference/research/issue-2245-chattimeout-2026-11-22.md`, probe folder, index row, log entry.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce the 120 s no-response ask | Unproven | About 45 asks over five runs; max 56 s; one HTTP 500 after 19.4 s |
| Cause among model, hold, worker, SQL | Partly proven | Model and hold excluded (hold answers in 4 s, no model call), worker excluded (restartCount 0, recovers); SQL write-lock wait supported by code plus the 19.4 s ProgrammingError; lock holder unknown (telemetry denied) |
| Smallest fix with regression test | Proven for avoidable lock traffic only | Test fails then passes; not deployed, live effect unmeasured |
| Thread-create 500 cause | Unproven | Not reproduced; same ProgrammingError class |
| Model call or plain banner; skills and routes | Proven earlier (PR 2249 note) | `issue-2245-live-2026-11-22.md` |
| Dated note, index, log | Proven | Files above |

Divergence: an early source edit was made and reverted before the changes record existed; the witness recorded the dirty-source qualification. The edit was reapplied after `implement-start`.

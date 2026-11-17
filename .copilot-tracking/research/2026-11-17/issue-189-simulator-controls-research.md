# Issue 189 research: simulator cost, scale and run controls

Task: issue-189, mode automatic (worker), tier FOCUSED (source-only, no Azure, SQL, infra or deployment).
Base: origin/main eb51af5c9. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 189 criteria 1 and 2 are ticked (cost estimate, B1 headroom). Criterion 3 (owner, time limit, budget alert) stays unchecked: the live alert is unproven and needs Azure (#146). It cannot be proven in this task.
* Existing delivery: `src/core/.../synthetic/run_plan.py` (pre-run estimate, RunController), `sensor_stream.RunBudget`/`Pacer`, `src/api/.../live_control.py` (owner, approval, 14-day expiry), `simulator_admin.py`, `live_simulator.check_capacity`.
* Baseline measurement: `python3 -m unittest tests.test_run_plan tests.test_sensor_stream` in `src/core`: 42 tests OK.

## Measured gap (reproduced)

`RunPlan` and `RunBudget` reject placeholder, template or over-long owner and alert text through `sensor_stream.accountable_text`. `live_control.parse` (used by the admin API snapshot, the simulator and receiver, and the `live_control start` CLI) uses its own shorter placeholder list and no length bound. Reproduction on base, `live_control.parse` with otherwise valid documents:

| Field value | Result on base |
| --- | --- |
| `nobody` (owner or approval_reference) | accepted |
| `<owner>` (owner or approval_reference) | accepted |
| 5000-character string | accepted |

So the CLI route can start a run whose owner is `nobody`, which weakens the "run has an owner" control (criterion 3) on the path an operator actually uses. The admin HTTP route already refuses these in `_clean`, so the two routes disagree.

## Decision

Smallest fix: `live_control.parse` validates owner and approval_reference with `accountable_text` (single shared rule), keeping the existing `PLACEHOLDERS` behaviour as a subset. One regression test in `src/api/tests/test_live_control.py`.

## Out of scope

Live budget alert, real hub quota consumption, core mssqlstore and chat grounding (#1818, #1641), any Azure action.

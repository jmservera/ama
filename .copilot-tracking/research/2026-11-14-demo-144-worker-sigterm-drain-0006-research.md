# Research: #144 worker SIGTERM drain (slice 0006)

* Disposition: executed. Planning Readiness: Ready.
* `src/orchestrator` has no worker runner (prints version, scheduled jobs only). The standalone worker is `src/agents/src/zava_forward/agents/worker.py` with `dispatch.run_once`; the orchestrator may not import agents (`test_dependency_rule.py`), so tests live in `src/agents/tests/test_worker.py`. Divergence from the brief recorded.
* Gap 1: the signal handler set only `stop`; `AgentWorker.stop_event` was set after the loop, so an in-flight call ran to its full timeout (possibly beyond the container grace period).
* Gap 2: when `stop_event` ended a call, `handle` posted a `timeout` failure result instead of releasing, durably failing a task that should be redelivered.
* Verified existing: nothing acked before post; post/handler failure releases; release/receive faults do not escape `serve`.
* `infra/` untouched (PR #1583 overlap avoided).

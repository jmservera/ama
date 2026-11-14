# Plan: #144 worker SIGTERM drain

Details: [details](../details/2026-11-14-demo-144-worker-sigterm-drain-0006-details.md)

* [x] Phase 1: add `DRAIN_SECONDS` (20 s) and a drain timer in `install_signal_handlers` that sets `worker.stop_event`.
* [x] Phase 2: `AgentWorker.handle` returns None (release) when stop ended a timed-out call.
* [x] Phase 3: tests in `src/agents/tests/test_worker.py`; README line; focused validation.

Critique (single pass): compatible, no conflicts; drain below the 30 s Container Apps default grace period.

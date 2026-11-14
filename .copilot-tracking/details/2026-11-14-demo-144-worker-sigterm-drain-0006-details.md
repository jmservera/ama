# Details: #144 worker SIGTERM drain

* Phase 1: `worker.py` `install_signal_handlers(stop, worker=None, drain=DRAIN_SECONDS)`; `main` passes `runtime.worker`.
* Phase 2: `dispatch.py` `handle` returns None if `stop_event` is set and the envelope outcome is `timeout`; `run_once` then releases.
* Phase 3: `DrainTests` (completes in window; released not failed after window; release fault contained). Run in the venv `/tmp/venv-144-0006`.

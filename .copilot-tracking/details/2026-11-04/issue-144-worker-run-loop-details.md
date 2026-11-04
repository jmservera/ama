# Details: issue 144 worker run loop

* `src/agents/src/zava_forward/agents/worker.py`: `serve(queue, worker, sink, limits, stop, idle, backoff)`, `install_signal_handlers`, `main`.
* `__main__.py` delegates to `worker.main`; no argument keeps the version print, `serve` exits 2 with a stderr message.
* Safeguards kept: ack only after post, release on failure, no database, blob or Key Vault access, no approval or send path.
* Tests: `src/agents/tests/test_worker.py`.

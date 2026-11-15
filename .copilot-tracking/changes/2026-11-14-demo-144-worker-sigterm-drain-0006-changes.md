# Changes: #144 worker SIGTERM drain

* `src/agents/src/zava_forward/agents/worker.py`: drain window timer on SIGTERM/SIGINT.
* `src/agents/src/zava_forward/agents/dispatch.py`: release instead of recording timeout failure on drain expiry.
* `src/agents/tests/test_worker.py`: three `DrainTests`.
* `src/agents/README.md`: drain behaviour.
* Validation: agents 451 OK, orchestrator 115 OK, core scenario manifest 8 OK, ruff (project config) clean, format check clean, mypy clean. `ruff --isolated` flags I001 on test_worker.py imports, pre-existing at HEAD (isolated mode cannot see first-party config).
* Divergence: tests are in `src/agents/tests`, not `src/orchestrator/tests` (dependency rule).

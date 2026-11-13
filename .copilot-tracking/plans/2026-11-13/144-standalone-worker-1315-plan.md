# Plan: issue 144 standalone agents worker (1315)

Refs #144, #136. Tier: Focused. Details: `.copilot-tracking/details/2026-11-13/144-standalone-worker-1315-details.md`.

* [ ] P1 RED tests: `src/agents/tests/test_runtime.py` (env build, token source, API sink, heartbeat, health), `test_worker.py` (serve wiring, refusal names variables only, health exit codes), `infra/tests/test_container_contract.py` (agents CMD is `serve`, others unchanged).
* [ ] P2 Implement `runtime.py`, update `worker.py` `main`, Dockerfile CMD.
* [ ] P3 Docs: `infra/README.md` (two placeholder statements), `src/agents/README.md`.
* [ ] P4 Validate: unittest agents, container contract, deploy tests, ruff, mypy.
* [ ] P5 Independent review, commit.

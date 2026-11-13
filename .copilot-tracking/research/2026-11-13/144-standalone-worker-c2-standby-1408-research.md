# Research: #144 Cycle 2 standby mode

Read the case study, addendum, reference README and memory conventions (context only; the change is worker code and an infra contract test).

Evidence:

* `worker.py main(["serve"])` calls `build_runtime`; `runtime.build_runtime` raises ConfigError when `ZF_AGENT_RESULT_ROUTE != enabled`, so main returns 2 and the deployed Container App (`containerapps.bicep` agents, args `serve`, no route variable set) crash-loops.
* Existing test `test_serve_refuses_naming_missing_settings_only` relies on route-not-enabled returning 2.
* `infra/tests/test_container_contract.py` asserts `args: ['serve']` only.

Decision: add a fail-closed standby in `main`. When the route flag is not exactly `enabled`, never build a queue, print one line to stderr, beat the heartbeat, wait for SIGTERM/SIGINT, exit 0. When enabled with incomplete settings, still exit 2.

Planning Readiness: Ready. Disposition: executed.

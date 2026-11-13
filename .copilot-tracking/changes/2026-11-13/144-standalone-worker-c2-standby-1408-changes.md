# Changes

* `src/agents/src/zava_forward/agents/worker.py`: `serve` enters standby (alive, heartbeat, no queue built, exit 0 on SIGTERM/SIGINT) unless `ZF_AGENT_RESULT_ROUTE` is exactly `enabled`; enabled with incomplete settings still exits 2.
* `src/agents/tests/test_worker.py`: RED-first tests for standby (mocked, and real SIGTERM subprocess with health check); existing serve tests set the route enabled.
* No Bicep change: the agents app keeps `serve` and, with the route variable unset, now stays healthy. The queue scale rule may start idle standby replicas while messages wait; a later cycle enables route and allowance together.

Validation: `src/agents/tests` 355 tests (one existing test updated to set the route, then worker tests 11 OK); `infra/tests` container_contract, bicep_policy, deploy, pipeline 118 OK; ruff and mypy clean on `src/agents`. Pre-existing ruff FURB162 in `infra/scripts` untouched.

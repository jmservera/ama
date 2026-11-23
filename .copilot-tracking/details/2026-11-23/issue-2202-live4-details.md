# Details: issue 2202 live4 (2026-11-23)

* `check_deployment(runner, group, kind, name)`: `az containerapp show` or `az containerapp job show` with a JMESPath query for the first container image and the env entry named ZF_CONTAINER_HARDENING. Result detail: `sha256:<12 hex> hardening=<value>`.
* DEPLOYMENT_TARGETS: apps API, resident, agents; jobs simulator and receiver.
* Wired into `collect` before job executions.

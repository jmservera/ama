# Plan: #144 Cycle 2 standby

* RED: add worker tests (standby when route unset or not "enabled": exit 0 on stop, no `build_runtime` call, no queue built, heartbeat beats, single stderr line; enabled + incomplete env still returns NOT_CONFIGURED). Update existing refuse test to set the route enabled.
* GREEN: in `worker.main`, branch before `build_runtime` on `os.environ.get(ROUTE_FLAG) != "enabled"`; call `standby(heartbeat, stop)`.
* Contract: infra contract test asserts the agents app keeps `serve` and the worker documents standby (no Bicep change needed; the route variable stays unset so the app stays in standby).
* Validate: agents unittest, infra tests, ruff, mypy.

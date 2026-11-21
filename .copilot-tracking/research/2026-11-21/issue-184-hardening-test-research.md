# Research: issue 184 hardening test parameter

Planning Readiness: Ready. Research disposition: executed.

* Cherry-picked 4b8422881 onto b6d215334 (now 904dc3e5f). It added `param containerHardening string = 'enforced'` to infra/live-receiver-job.bicep (line 43) and infra/live-simulator-job.bicep (line 38), used as `ZF_CONTAINER_HARDENING` value.
* The compiled ARM template emits `[parameters('containerHardening')]` for env value, so the test at infra/tests/test_container_hosting_144.py (jobs loop) compares against the literal 'enforced' and fails.
* Fix: in the test, resolve a `[parameters('x')]` env value to the compiled parameter defaultValue and assert the default is 'enforced'. No Bicep or control change.
* Issue 184 criteria: all three are already ticked in the issue; no unticked criteria to prove.

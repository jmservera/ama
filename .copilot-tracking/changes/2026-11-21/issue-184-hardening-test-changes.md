# Changes: issue 184 hardening test parameter

Status: complete. Tier: focused (the only edit by this task is an infra test; the cherry-picked 4b8422881 carries the earlier src and Bicep changes unchanged, reviewed under its own record).

* Cherry-picked 4b8422881 onto b6d215334; squashed with the test fix into one commit.
* infra/tests/test_container_hosting_144.py: new `_resolve_param_default` resolves `[parameters('x')]` to the compiled defaultValue; the jobs loop asserts the resolved `ZF_CONTAINER_HARDENING` equals 'enforced'. Bicep defaults and the control are unchanged.
* Second failure in the same test, found after the first fix: the job `volumes` list carries `[variables('certVolume')]` as an expression. The test now asserts that reference and that the variable's AzureFile branch sets `mountOptions` 'ro' (the Secret branch has no mount option), instead of indexing a string.
* Validation: `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -v` in a venv with src/core, src/agents, src/api installed: 759 tests OK, 4 skipped. ruff format --isolated --line-length 100 --check and ruff check clean on the changed file. Without the venv the module failed to import (missing opentelemetry), an environment issue only.
* Not run: rpi-checks.py --all, hosted CI.

## Acceptance criteria for issue 184

| Criterion | Status |
| --- | --- |
| All child stories closed or deferred | Already ticked in the issue; not re-proven here (no live work in scope of this goal) |
| Simulator never connects to, discovers or represents installed real devices | Already ticked; not re-proven here |
| No device key or connection string in source, logs or telemetry | Already ticked; not re-proven here |

No unticked criteria exist, so no live Azure action was taken and nothing was created or deleted.

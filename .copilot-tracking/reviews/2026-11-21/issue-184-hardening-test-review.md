# Review: issue 184 hardening test parameter

Execution: executed once. Outcome: conformant. Boundary: infra/tests/test_container_hosting_144.py diff plus cherry-pick.

* The control is not relaxed: the resolved value must still equal 'enforced'; Bicep untouched.
* The cert volume assertion is narrower than a literal match but still checks the read-only AzureFile mount option.
* Open item for later: the parameter allows 'off' (demo profile); the test checks only the default, by design of this task.

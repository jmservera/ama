# Details 2244 live r3 (2026-11-23)

* P1: line 263 of `infra/modules/containerapps.bicep`, `failureThreshold: 40` to `80`.
* P2: `test_bicep_policy.py` expected probe list `failureThreshold` 40 to 80; new test in `test_container_hosting_completeness.py` imports `LOCK_RETRY_ATTEMPTS`, `LOCK_RETRY_BASE`, `LOCK_RETRY_CAP` from `zava_forward.core.mssqlstore` if importable, else parses them from the file text, and asserts the window is at least the budget.
* P3: `python3 -m unittest` for the two infra test modules; `bicep build` via the existing helper in the tests.

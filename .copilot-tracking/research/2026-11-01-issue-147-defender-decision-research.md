# Issue 147 research (2026-11-01)

* Disposition: executed. Criteria 2-4 already ticked and backed by infra/governance.bicep, infra/policy-exceptions.json, enableLocks and tests in infra/tests/test_governance.py.
* Open: criterion 1 (policy and Defender decisions recorded with owner and cost). Policy stance, owner and "no charge" are in infra/README.md; Defender cost is "not estimated".
* Resource inventory from templates: 2 storage accounts (storage.bicep, authTokenStore.bicep), 1 SQL server, 1 Key Vault, 1 container registry, 1 Container Apps managed environment.
* Azure pricing page (fetched 2026-11-01) renders unit prices dynamically ("$-"), so no verified price could be retrieved. No figure is invented.
* Planning readiness: Ready. Scope: machine-checkable decision record with owner, cost basis and explicit pending state; cost acceptance stays an owner decision, so the issue stays Refs.

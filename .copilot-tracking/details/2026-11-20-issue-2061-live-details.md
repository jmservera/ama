# Details: issue 2061

## Phase 1
* `main.bicep`: `param demoSingleEnvironment bool = false`; guards `singleEnvironmentRequiresDirectDemo`. Pass `separateInternalIdentity` to identity and apps modules.
* `identity.bicep`: conditional `internal` identity; outputs `ids.internal` fall back to the API identity when disabled.
* `containerapps.bicep`: ledger verify and ranking publish jobs use `identityIds.internal`; output `publicIngressApps`.

## Phase 2
* storage roleAssignments and registry pull gain the internal principal only when enabled; the API keeps its roles (it serves evidence and enqueues tasks).
* `create-sql-users.py` grants `internal` datareader and datawriter and skips an identity that does not exist.
* `role-assignments.json` rows and `sqlGrants` entry; tests updated.

## Phase 3
* `docs/architecture/decisions/` ADR (check existing numbering), `infra/demo-single-environment-runbook.md`, README pointer.

## Phase 4
* `az bicep build`, `python3 -m unittest discover -s infra/tests`, ruff on changed Python.

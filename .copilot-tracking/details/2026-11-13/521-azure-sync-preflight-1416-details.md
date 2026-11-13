# Details: Azure sync preflight

## Phase 1
* Probe: `az account show`, `az containerapp list -g ama`, `az containerapp show -n ca-resident-demo` (only min/max/expiry env). Redact tenant and subscription ids.
* Dry run: `python3 infra/scripts/resident_showcase_sql.py id-cutover-test-resident-demo | grep -n 2028`; requires `pip install -e src/core` into a temporary venv (`/tmp/venv-521`, removed before commit); prints SQL text only, makes no connection.
* Success: render contains `2028-01-01T00:00:00`; exit 0.

## Phase 2
* Go/no-go: (a) NO-GO until #891, #184, #233, #153, #144 merge and the owner approves dispatch/registry window; (b) READY for owner approval (dry-run proven, live SQL state unverified); (c) NO-GO: no live runner, no frozen held-out manifest, no authorisation record.
* Flag README line about Pending app expiry as stale versus live env.

## Phase 3
* Independent `code-review`, `git diff --check`, commit `docs(521): ...` with Refs trailers and Co-authored-by.

# Changes: Azure sync preflight (Refs #521, #360, #891, #435)

Write surface: `.copilot-tracking/*/2026-11-13/521-azure-sync-preflight-1416-*` only. No source, README, Azure or SQL change.

## Checks run (read-only)

* `az account show`, `az containerapp list/show`, `az acr list`, `az sql server list`, `az cognitiveservices account deployment list`, `az consumption budget list` for group `ama`: all succeeded; results in the research file (ids withheld).
* `resident_showcase_sql.py id-cutover-test-resident-demo` (dry run, Python 3.12 temp venv, editable `src/core`): exit 0, renders `2028-01-01T00:00:00` (2 occurrences), no connection made. Temp venv and output removed.
* Issue states via `gh issue view`: #891, #184, #233, #153, #144, #435, #432, #360 open; no open merge PRs found.

## Preflight outcome

| Item | Verdict | Basis |
| --- | --- | --- |
| (a) Build and deploy api + agents | NO-GO | Preceding PRs unmerged; workflow targets `workload=forward`, unverified against live `cutover-test` apps; registry window and dispatch need owner approval |
| (b) SQL 2028-01-01 cutoff | Conditional: ready for owner approval only after a read-only SQL probe | Dry run proven; live app env already `2028-01-01T00:00:00Z`; live SQL constraint and rows unverified; apply re-runs GRANT/DENY batches |
| (c) USD 5 held-out batch | NO-GO | No live runner, frozen manifest, authorisation record, price table or hard cost cap |

## Open items

* Dry-run output was not saved; the result above is the recorded observation.
* `infra/README.md` ~line 4619 says live app expiry is Pending; live env shows 2028. Stale record, not edited here.
* Probe the live SQL constraint from an allowed host with owner approval before closing #521.

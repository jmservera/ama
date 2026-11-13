# Research: Azure demo sync, SQL 2028-01-01 cutoff and held-out batch preflight (Refs #521, #360, #891, #435, #432)

Date: 2026-11-13. Base: origin/main `dafed6a27`. Disposition: executed. Planning Readiness: Ready.
Scope: read-only. No Azure mutation, no SQL access, no `.env` read, no secret or subscription id recorded.

## Read-only Azure observations (2026-11-13)

| Check | Result |
| --- | --- |
| `az account show` | Active session, state Enabled, one subscription (name, subscription and tenant ids withheld) |
| Resource group `ama` visibility | Readable: Container Apps, jobs, ACR, SQL, Cognitive Services, budgets listed |
| Container Apps | `ca-cutover-test-api` (rev 0000008), `ca-cutover-test-agents` (0000001), `ca-cutover-test-demo-api` (0000027), `ca-resident-demo` (0000010); all Succeeded, images pinned by digest in `crcutovertestrzsrg` |
| ACR | `crcutovertestrzsrg` |
| SQL server | `sql-cutover-test-rzsrg` |
| Model deployments | `aif-cutover-test-rzsrg` (AIServices): `standard` gpt-4.1-nano GlobalStandard cap 10; `aoai-resident-469` (OpenAI): `resident-mini` gpt-4.1-mini Standard cap 1 |
| Jobs | Eight `job-cutover-test-*` jobs, all Manual trigger |
| `ca-resident-demo` | Running, min 0, max 1, `ZF_DEMO_EXPIRES_AT` = `2028-01-01T00:00:00Z` |
| Budgets (monthly, USD) | forward-test 300 (spend about 62.1), cutover-test 300 (about 56.7), iot-cutover 25 (about 3.5) |

Not checked: live SQL `ck_allowed_case_window` constraint and row windows (needs SQL Entra access; out of read-only scope), registry tags, role assignments of the caller (the `az role assignment` probe errored on assignee lookup; not retried).

Contradiction to flag: `infra/README.md` (Live state check 2026-11-04, around line 4619) says the live app expiry move to 2028-01-01 is Pending. The live app env now already carries `2028-01-01T00:00:00Z`. Whether the SQL constraint and rows moved is unverified. Update the README only after the owner or a probe confirms; do not close #521 on this metadata alone.

Open issue states: #891, #184, #233, #153, #144, #435, #432, #360 all OPEN; no open PR matched the search (merge precondition not met on 2026-11-13).

## Exact commands and prerequisites

### (a) Build and deploy `api` + `agents` images after the PRs merge

* Canonical path: `.github/workflows/src-deploy.yml` (workflow_dispatch, input `environment` in dev/test/pilot). Jobs: source-ci gate (requires a successful dispatch run of source CI on the same sha), build, publish (environment `<env>-release`, vars `AZURE_REGISTRY_NAME`, `AZURE_PUBLISH_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`), deploy (environment `<env>`, self-hosted runner label `ama-private-deploy`, vars `AZURE_DEPLOY_CLIENT_ID`, `DEPLOY_PARAMETERS`, runs `python3 infra/scripts/pipeline.py verify-environment` then `pipeline.py deploy --environment <env> --images <digests> --output <summary>`). Publish runs under a separate `<env>-release` environment (self-hosted release runner); `pipeline.py verify-environment` checks approval configuration, whose actual state was not read. Needs the owner to dispatch.
* Target caveat (critique finding 2): `pipeline.py` (line 131) forces `workload=forward`, so the workflow addresses the `forward` infrastructure deployment, not the `cutover-test` apps observed live (`ca-cutover-test-*`, budgets `forward-test` and `cutover-test` both exist). The exact target of the workflow is unverified; (a) stays NO-GO until the owner confirms which apps the workflow updates. The direct-ingress demo app `ca-cutover-test-demo-api` is updated by `az containerapp update --image <repo>@sha256:<digest>` after a digest-pinned push inside a short, reverted registry network window (precedent: `infra/README.md` lines 1537, 689-692). The resident app uses `python3 infra/scripts/resident_demo_deploy.py --subscription <id> --expires <ISO Z> --image <repo>@sha256:<digest> --sql-server <fqdn> --sql-database <db> [--apply]` (what-if by default; needs the two vault secrets, resident SQL principal and a cleared budget check).
* Build context is `src/` (`docker build -f src/api/Dockerfile src`, same for agents). `infra/scripts/deploy.py --resource-group ama --parameters <bicep params> --registry <name>` only resolves the orchestrator image and runs what-if.
* Prerequisite: merge of #891, #184, #233, #153, #144 to `main`, then fresh digest, then owner approval; registry window changes are mutations that need explicit approval.

### (b) Apply the 2028-01-01T00:00:00Z SQL cutoff

* Source cap already `AUTHORITY_END` in `zava_forward.core.resident_showcase`; packaged `resident-demo.json` must carry 2028 (assumed built after #590; the digest of the running image was not verified and must be checked first).
* Step 1 (constraint, also re-runs view and GRANT/DENY, so owner approval): `python3 infra/scripts/resident_showcase_sql.py <principal> --client-id <resident MI client id> --apply sql-cutover-test-rzsrg <database>` (no `--create-principal`; exit 2 if neither id flag given). Needs `mssql_python` (`pip install --require-hashes -r src/api/requirements.txt`), the caller as SQL Entra admin, and a host allowed by the private endpoint. Dry run (no `--apply`) is safe and prints batches.
* Step 2: renew only individually approved rows: `UPDATE resident_showcase.allowed_case SET valid_to = '2028-01-01T00:00:00' WHERE case_id = '<approved id>' AND revoked = 0;`.
* The ordering is already inverted: the live app env carries 2028 while the SQL constraint and rows are unverified and may still hold the earlier window, so probe SQL first. Step 3: redeploy the app only if the image digest check fails or the expiry differs with `--expires` no later than the cap (the app refuses at or after `2028-01-01T00:00:00Z`; the documented command uses `2027-12-31T23:59:59Z`). Step 4: verify startup, sign-in, cross-case denial, min replicas 0, metadata only.

### (c) `<= USD 5` held-out token batch (#435, #432)

* No live runner exists. `src/agents/src/zava_forward/agents/chat_heldout.py` (`freeze_problems`, `leaks`, `run_heldout`) is scripted and offline; `src/agents/README.md` states `call_authorization` blocks unless a named owner authorisation gives finite positive call, token and budget limits with currency and an unexpired date, and `actual_calls` stays blocked. Held-out set, independent labeller, thresholds and a real manifest are not supplied.
* Cost basis: deployment `standard` is gpt-4.1-nano (GlobalStandard), `resident-mini` gpt-4.1-mini. Runtime knobs: `ZF_ASSIST_TOKEN_ALLOWANCE` (finite, covers one reservation), `ZF_ASSIST_OUTPUT_TOKENS` (default 600, 100-2000). Monthly budget headroom exists (cutover-test about 243 of 300 remaining), but nothing enforces USD 5: `chat_eval.py` (around line 546) does not compute or compare spend and the repo has no price table. A live batch needs a reviewed runner with pricing, cumulative usage and a hard pre-call cost cap.
* Prerequisite before any run: owner authorisation record (limits, currency USD 5, expiry), frozen held-out manifest passing `check_freeze`, and a runner that supplies real usage. These do not yet exist, so (c) is blocked.

## Evidence

* `infra/scripts/{deploy,resident_showcase_sql,resident_demo_deploy,pipeline}.py`, `.github/workflows/src-deploy.yml`, `infra/README.md` (2026-11-04 and 2026-11-11 entries), `src/agents/README.md`, `chat_heldout.py`.
* Az outputs above (names, states and non-secret settings only).

## Planning Readiness

Ready: produce a preflight record with the observations and gated runbook; no source changes.

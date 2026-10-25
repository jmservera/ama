# Research: synthetic resident Azure showcase with fake-email demo login (issue 462)

Date: 2026-10-25, written from 16:44Z, before any plan, critique or implementation. Worktree `issue-462-resident-azure`, branch `feat/resident-azure-showcase-462`, from main ea5577b2 (still current origin/main at 16:45Z). Refs #462 (never closes it).

Research disposition: executed. Authority now: research and plan only until #444 / PR #455 merges. No runtime code, cherry-pick or copy of the #444 branch, implicit stacking, deploy or cloud mutation occurred. No credential was generated. No private dataset, secret value, email roster or database dump was read.

## Sources read

* Issue 462 body via `gh issue view 462` (metadata in `.copilot-tracking/github-issues/issue-462.md`); repository instructions; `docs/reference/README.md` and `memory.md`; `infra/README.md`, `src/api/README.md` and `src/core/README.md` by targeted search; ADRs 0001 and 0002 titles.
* #444 branch `origin/feat/resident-feedback-preview-444` read only through `git show` (not checked out): `core/resident_preview.py`, `api/resident_preview/app.py`.
* Main: `sqlstore.py`, `mssqlstore.py`, `factory.py`, `scale_fixture.py`, `infra/scripts/credential_arm.py`, `secret_lifecycle.py`, `src/api/Dockerfile`.
* Read-only Azure metadata (resource group `ama`, subscription e51ebc89 prefix, tenant bccd6ad2 prefix): resource list, Container Apps, SQL database SKU, vault network and role metadata, Cost Management query by day and resource type. No secret, SQL row or business record was read.

## Finding 1: dependency state (verified 2026-10-25T16:45Z)

* #444 is open. PR #455 is open and mergeable with one visible check, `rubric/score`, failing at 72/100 against baseline 73/100 (run 40206914304). The coordinator's same-session correction of the threat-model evidence is the route to a pass; this task must not edit scores, rerun unchanged to fish, or bypass the gate.
* The #444 diff on its branch is 3,241 added lines: `core/resident_preview.py` (556), `core/synthetic/resident_preview_fixture.py` (404), `api/resident_preview/{app.py,__main__.py,web/*}` and tests. These files do not exist on main, so the resident projection, UI and tests this issue needs are not available to build on. Overlap with this issue: `src/api/pyproject.toml`, `src/api/README.md`, `src/core/README.md`, `docs/reference/README.md` and `log.md`. Re-check overlap after merge.
* #444's boundary, to be kept unchanged: loopback-only (`LOOPBACK_HOSTS`, Host-header check), refuses `ZF_`, `AI_`, `IDENTITY_`, `MSI_`, `AZURE_`, `MSSQL`, `SQL`, `OPENAI`, `APPLICATIONINSIGHTS` environment (`FORBIDDEN_ENV_PREFIXES`), reads no cookie or header, subject taken from a fixture grant. A cloud composition cannot reuse `safe_start`; it needs its own start-up with different guards. `resident_view(store, grant)` and the `Grant` shape (`grant_id, subject, case_id, kind, fields, actions, valid_from, valid_to, revoked`) are the reusable positive-allowlist core.

## Finding 2: cost preflight (read-only, 2026-10-25T16:45Z)

Result: **spending is blocked, not zero.** The remaining headroom under the cumulative USD 50 incremental cap cannot be computed from available evidence.

* Evidence found: tracked plans repeat "original USD 50 cap and USD 700 ama RG limit unchanged" (360 seed plan) but no tracked artifact states cumulative previous incremental spend or accrual, and no definition of the incremental baseline (the date, run rate or resource set that counts as non-incremental). A search of plans, changes, reviews, infra README and the cutover evidence pack for a cumulative ledger found none.
* Cost Management, `ama` resource group, month to date by resource type (USD, actual cost, data lags): SQL servers about 150.9, CDN/Front Door profiles about 63.4, private endpoints about 27.4, container registries about 24.1, Container Apps environments about 23.2, Container Apps about 20.2, IoT Hub about 3.2, Log Analytics about 3.1, jobs about 2.5, smaller items under 1. Total of these about USD 319. Daily total was about 30 on 18 to 21 October, 26.8 on 22, 18.5 on 23, 19.1 on 24, 3.3 on 25 (partial day, lagging). October USD 700 ceiling (resource group `ama` only) is not at risk at this run rate, but the ceiling gives no incremental headroom, as the issue says.
* Two things this proves and one it does not: the October ceiling is respected so far; existing baseline spend is large and separately attributable; it does not say how much of the USD 50 has been used by earlier owner-authorised changes. The prior ledger must come from the coordinator or owner (named gap G1) before any paid mutation.
* Existing resources relevant to the plan (names only): Container Apps environments `cae-cutover-test` and `cae-cutover-test-demo`; apps `ca-cutover-test-api` (external, min 2), `ca-cutover-test-agents` (no ingress) and `ca-cutover-test-demo-api` (external, min 0, max 4, 0.5 vCPU/1 GiB, port 8088, no IP restrictions at 16:45Z); registry `crcutovertestrzsrg` (Premium, private endpoint); Key Vault `kv-cutovertest-rzsrg` (public access Disabled, RBAC enabled); SQL server `sql-cutover-test-rzsrg` (public access Disabled, Entra-only) with database `retrofit` at Standard S0, 10 DTU, 30 GiB (32,212,254,720 bytes); four user-assigned identities including `id-cutover-test-api` (shared with the demo API); Front Door profile; Foundry account; many private endpoints. Ownership of these is not inferred and none will be changed or cleaned up.
* New finite resource estimate for the later plan, all inside `ama`: one Container App (0.25 vCPU, 0.5 GiB, min 0, max 1) in the existing `cae-cutover-test-demo` environment (no new environment), one user-assigned identity (no charge), one or two Key Vault secrets (operation cost only), one image in the existing registry (storage only), one short kaniko build job run (minutes of consumption compute). Scale-to-zero consumption pricing implies a small cost, but this is an estimate, not a settled figure; it must be priced from the Azure retail price metadata at plan acceptance, not assumed zero. Stop conditions: unknown headroom, any projected incremental above remaining cap, any need for a non-consumption SKU, new environment, private endpoint, Front Door, public backing store, or a change to SQL S0. Cleanup is owned by this task only for the resources it creates and tags (`ama-issue=462`, expiry 2026-10-26T12:00Z); no existing resource is deleted; the resource group is never deleted.

## Finding 3: fake-email provenance (gap, fail closed)

* The case record body has a `resident.email` field (`ai_eval.py:51` and `core/tests/dataset.py:87` build `email=""`). Staff views use `resident.name`, `phone`, `adjustment`, `first_contact_at`, `representative`. No code path on main reads `resident.email` for login, and the test datasets leave it empty. Emails are therefore an optional field whose population in the live database is unknown.
* The authoritative synthetic source is the #360 baseline seed (980 programme cases, seed 20260901, as-of 2026-10-13), generated by a tracked generator under the owner's private `support/` area and merged into `retrofit` through `seed_merge` (case semantics in the 360 plan and review). Its description is "real OSM addresses with fictional people". Whether it populates `resident.email`, with what domain, and whether any email is duplicated, could not be verified without reading private data or the private database (SQL is private-only with public access Disabled), and was deliberately not done.
* Stock and households: `scale_fixture.households()` builds `HH-SYN-`, `R-SYN-` and `TEN-SYN-` refs with `is_synthetic=True` but no email. `stock.py` carries no resident identity. So the existing homes (cases) are the only plausible owner of a resident email; stock does not own one.
* Consequence: no login mapping may be implemented or displayed until a verified read-only probe reports, for the live `retrofit` cases, counts only: cases with a non-empty `resident.email`, distinct normalised emails, duplicates, emails whose domain is not a reserved or owner-approved synthetic domain, and cases lacking the synthetic marker. If the field is empty or not provably synthetic, the work fails closed and reports gap G2. The owner's instruction forbids inventing customer facts, so adding emails to the database is a separate owner decision (it would be a business-data write, excluded here). A mapping held outside the database (server-owned file in the secret store) is an alternative only if the owner approves it as the authoritative source (gap G2 option).
* The cases table indexes `search`, `surname`, `postcode` and `address` but not email. Looking up by email therefore needs either a bounded read-only scan of the JSON body or a derived mapping built at start-up from a narrow query. 980 cases is small enough for a bounded start-up pass.

## Finding 4: deployment and auth patterns on main

* `MssqlStore` (via `factory.open_store`) creates schema, adds columns and appends to the audit ledger on open. A resident app must not use it: it would carry DDL/write capability. A separate read-only reader (single parameterised SELECT, no DDL) under a database principal with SELECT only is required. Creating that principal needs an Entra SQL admin action in a private network path (`infra/scripts/create-sql-users.py`, `grant-application-admin.py` exist). Whether the current operator holds that authority is unknown (gap G3).
* `ca-cutover-test-demo-api` uses the shared `id-cutover-test-api` identity, which has the employee API's SQL access. The resident app must not reuse it. A new user-assigned identity with AcrPull on the registry scope, Key Vault Secrets User on one secret and a SQL read-only user is the least-privilege shape; creating role assignments needs the subscription's role-assignment authority at resource scope only (an `Owner` and a `User Access Administrator` user exist on the vault scope, so this is probably available, but not proven for this operator; gap G3).
* Existing secret mechanism: `credential_arm.py` writes a credential through a bounded SecureString ARM deployment into the selected `ama` vault; the 358 qualification proved a KV-reference secret on a Container App with exact cleanup. The vault is private; local data-plane reads fail, so retrieval needs a private path. The vault's role list shows owners with management Owner/UAA but the issue owner's data-plane secret permission was not verified; Owner does not grant secret read (gap G4).
* Registry is private; image builds use the existing kaniko job route (`job-cutover-test-init`) per the 360 plan. A new image variant needs a Dockerfile that installs `core` and `api` and starts the resident entry point, non-root user 10001 like `src/api/Dockerfile`.
* Edge: `cae-cutover-test-demo` is external. Container Apps terminates TLS and supplies the HTTPS FQDN (`*.azurecontainerapps.io`); no custom domain or Front Door is needed.

## Threat model inputs (to be completed in the plan)

Public fake-email login; one shared credential (anyone knowing it and any listed email sees that case, by design); guessable email enumeration; brute force and credential stuffing against one secret; session fixation, theft, CSRF and logout; cross-case access by changing identifiers; over-broad database reads leaking staff notes, safeguarding, finance or staff identities; raw errors; log leakage of email or password; shared-identity privilege creep; Host/header spoofing behind Envoy; denial of service on a 10 DTU database; confusion of the synthetic demo with a real service.

## Options

1. Dedicated resident-demo Container App in the existing demo environment, own identity, own image, read-only SQL principal, KV references (recommended).
2. Add resident routes to `ca-cutover-test-demo-api`: rejected, mixes employee and resident trust and changes employee configuration.
3. New environment or Front Door: rejected, new recurring cost and unknown headroom.
4. Reuse #444 loopback harness in the cloud: rejected by the issue.

## Gaps and blockers

* G1: cumulative previous incremental spend and the baseline definition are missing: blocks any paid mutation.
* G2: populated, synthetic, unique `resident.email` in live `retrofit` is unverified; need counts-only probe run in a private path (a later paid step) or an owner decision on an external mapping.
* G3: operator authority for the resident identity, role assignments and SQL principal is unverified.
* G4: the owner's own data-plane read path for the one demo secret is unverified.
* G5: #444/PR455 not merged; rubric failing.

## Planning readiness

Ready for planning. Not ready for implementation or cloud action (G1 to G5). Research limits: no live database inspection; cost data lags; estimates are not settled prices.

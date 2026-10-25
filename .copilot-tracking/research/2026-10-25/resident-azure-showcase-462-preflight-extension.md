# Research and plan extension: read-only technical preflight (issue 462)

Date: 2026-10-25, probes run 16:54Z to 16:56Z, written after the probes and before any further change. Extends, and does not rewrite, `.copilot-tracking/research/2026-10-25/resident-azure-showcase-462-research.md` and the plan of the same day.

## Chronology disclosure

Commit `5963fa3f` (research, plan, critique, state, issue record) was pushed to `origin/feat/resident-azure-showcase-462` at about 16:50Z without the required full local gate, contrary to the explicit brief. It stays in history unchanged. No PR exists. No further push until the full gate is actually verified. The deviation is to be disclosed in the future changes artifact. Coordinator/owner disposition is pending and is not permission to ignore the gate. #444's gate (1186925) is active and was not interrupted or queued against.

Scope kept: read-only; no Azure mutation, new resource, job, exec, deployment, role, secret read or generation, password, SQL login or private file read; no cherry-pick or stacking; no runtime code.

## G1: cost bounds (Cost Management query on resource group `ama` only, actual cost)

* Cap start: 2026-10-24T13:39Z. Cost Management daily granularity cannot split a day, so any bound uses whole days.
* Actual cost: 2026-10-24 USD 19.10; 2026-10-25 USD 3.29 (partial day, billing lag). Sum USD 22.39, of which SQL servers 21.87, Container Apps environments 5.63, private endpoints 4.56, registry 3.89, Container Apps 3.83, IoT Hub 0.65, Log Analytics 0.42, jobs 0.34, others under 0.2 (type totals overlap the day sums only approximately because of rounding and lag).
* Baseline comparison: 2026-10-17 to 23 total by type was SQL 74.9, Front Door/CDN 60.8, environments 16.8, private endpoints 13.4, apps 12.6, registry 11.7. Front Door/CDN cost is absent from 24 to 25 October (it appears to have stopped), so spend fell from about 30 a day to about 19 a day.
* Conservative upper bound that treats all `ama` spend after the cap start as incremental: used so far USD 22.39 as reported, lagging. A day-based projection to the authority end at 2026-10-26T12:00Z at the 24 October run rate (19.10 a day) is 19.10 + 19.10 + 9.55 = USD 47.75, leaving at most about USD 2.25. Under that reading the cap is nearly consumed by existing baseline and there is no safe headroom for this showcase.
* Alternative reading (incremental means only resources or changes added by owner-authorised work, excluding the pre-existing baseline): the tracked evidence does not enumerate those added resources or their cost, and the Cost Management API cannot attribute cost to "authorised change" in the available data. The only recorded statements are "original USD 50 cap unchanged" (360 plan) and the worker assertion that no billable consumption beyond the cap occurred, which is not metered. The 24 to 25 October bill includes new `-demo` environment and app, extra jobs and image storage, but their separate cost was not exported.
* Result: remaining headroom is not provable under either reading, and under the conservative reading is at most about USD 2. This does not show that USD 700 is safe: October month-to-date is about USD 319 with a lagging, partial month; this extension makes no ceiling claim from a partial run rate.
* Missing evidence needed: the owner's definition of the incremental baseline (what is excluded), an itemised export of incremental resources since 13:39Z with Cost Management lag allowance, and a priced estimate of this issue's resources. Until then spend is blocked. Pre-lag-bound hint: Azure cost data typically lags up to 24 to 48 hours; the last day's figures are unsettled.

## G2: fake-email provenance (counts only, no values output)

Source: tracked generator `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_names.py` (`resident()` gives about 55 percent of residents an email of the form `first.last<10-99>@example.com`; `example.com` is an IANA reserved example domain) and `build_mvp_dataset.py`. I ran the tracked generator, seed 20260901, as-of 2026-10-13, in a throwaway virtualenv and a mode 0700 temporary directory, printed only aggregate counts, then deleted both. No email, name or case was output or kept.

| Measure | Count |
| --- | --- |
| Cases | 980 (443 open), matching the live 980 after the 12:45Z obsolete-case removal |
| Cases with an email | 524 |
| Distinct normalised emails | 523 |
| Emails shared by more than one case | 1 (2 cases) |
| Cases with a uniquely owned email | 522 |
| Email domains | `example.com` for all 524 |
| Top-level dataset marker | `is_synthetic` true, plus per-case `synthetic_stock_anchor_id`; no per-case `is_synthetic` flag found |

Consequences: the email source is the existing homes, not stock; there is a real duplicate that the fail-closed rule must exclude (both cases); uniqueness is not guaranteed by the generator, so a runtime uniqueness check is mandatory; at most 522 cases are mappable and the planned showcase allowlist (at most 25) is feasible. Per-case provenance is the dataset-level marker and anchor id, so the runtime check must bind to the live store's recorded seed metadata rather than a per-case flag (verify at implementation).

Not proven: that the live `retrofit` database equals this regenerated seed. The live path is private (below), so only a seed-equivalence claim exists, based on the 360 evidence of seed 20260901 and 980 cases. The probe stays pending as a counts-only read in an approved private path, never a paid new job.

## G3: current principal facts

* This VM uses a system-assigned managed identity. It holds Owner at the resource group `ama` scope (only assignment found at its object id with `--all`); no subscription or tenant role seen. Owner includes role-assignment write, so scoped role-assignment creation within `ama` is technically possible but was not exercised. Whether a SQL permission exists is not provable from here.
* SQL server `sql-cutover-test-rzsrg`: Entra-only, public access Disabled; the only Entra administrator is the Application `id-cutover-test-init` (the existing initialisation job's identity). The VM identity is not the SQL admin. Therefore creating the SQL principal and the mandatory allowlist view needs a private-network run as that identity (an existing job route with its own cost and a database change). The view boundary stays mandatory; no create, grant or view was attempted. The server resolves publicly to a gateway address but access is denied by design; no login was attempted.
* Key Vault `kv-cutovertest-rzsrg`: private only, default action Deny, bypass None, one private endpoint, RBAC on, soft delete on with 7 days retention, purge protection NOT enabled. Data-plane list from this host was denied (Forbidden, not a private link), as expected.

## G4: owner secret read route (values-free)

No secret was listed, read or printed. Facts: the vault is private only, so any read, including by the owner, needs a client on the private network or a Key Vault private-link path; Owner or Contributor on the group gives no data-plane secret read; a Key Vault Secrets User assignment is one earlier-observed role on the vault scope for a service principal (principal identity not resolved here). There is no existing documented owner-secret-read route for a human; the nearest pattern is a private job. Route options, none executed: (a) a time-bound Secrets User assignment on the single demo secret to the owner plus a private-network client; (b) a private no-print job with a delivery path chosen by the owner. Either needs a named human approval and role creation, so it is both a technical prerequisite and a human decision, resolved after #444.

## Secret cleanup (revised, supersedes the earlier "purge soft-deleted secrets" wording)

Soft delete is on (7 days) and purge protection is off. Cleanup must not silently purge. Plan: (1) read the vault retention and purge settings and applicable policy again before cleanup; (2) soft-delete only the three exact-named demo secrets this task created; (3) record that a soft-deleted secret persists up to 7 days and its name is reserved until it expires or is purged; (4) purge only on a separate explicit owner approval naming each secret and after confirming policy permits it; (5) every secret and the ARM deployment history carry expiry at or before 2026-10-26T12:00Z and are verified by readback; never alter protection or retention settings. A 7-day retention after soft delete is a residual item the owner must accept.

## What needs live preflight versus local testing after #444 merges

| Item | Can be built and tested locally after #444 | Needs live preflight or named approval |
| --- | --- | --- |
| Domain, session, CSRF, limiter, view, HTTP, browser, Docker, local SQL Server parity, mapping builder with fake data and fail-closed config | Yes, parameterised; no live data needed | None |
| Mapping rule (example.com domain, uniqueness, allowlist cap, duplicate exclusion) | Yes, with a local synthetic fixture including a duplicate and non-example domain | Live counts-only probe confirms the live store matches |
| SQL view and read-only principal | Script and tests against local SQL Server | Creation in the live database as `id-cutover-test-init` through a private job: named owner/coordinator approval and cost |
| Identity, role assignments, Container App, KV secrets | Bicep, what-if fixtures, fake vault tests | Live what-if and apply after cost headroom proven (G1) |
| Credential generation and owner retrieval | Script tested with a fake vault | Not before deploy gates; retrieval route approval |
| Cost headroom | No | Owner baseline definition and itemised ledger (G1): hard block on any paid step |

Conclusion: G1 is a hard block on every cloud step; G2 to G4 do not block local pure implementation after #444 merges, only the live stages. The named human items are limited to: the incremental-cost baseline definition, approval to create the SQL view and principal through the existing private job, the owner's secret-read route, and any soft-delete purge.

## Planning readiness

Local implementation after the #444 merge: ready, parameterised and fail closed. Cloud steps: blocked by G1; approvals above still needed.

## Erratum and cost correction (appended 2026-10-25, probes 17:03Z to 17:12Z; prospective plan `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-cost-correction-plan.md`)

The text above is preserved. The following retracts or corrects it.

Retraction 1: the G1 resource-type breakdown (SQL 21.87, environments 5.63, endpoints 4.56, registry 3.89, apps 3.83 ...) was presented as reconciling to the day total of 22.39. It did not: those type figures sum to about 41.5. They came from a type-grouped daily query. Retracted as an uncorrected breakdown.

Re-query, same scope (group `ama`, ActualCost, USD, 2026-10-24 to 2026-10-25, ungrouped, grouped by ResourceType and by ResourceId; raw JSON kept outside the repository and values-free):

| Query | 24 Oct | 25 Oct | Total |
| --- | --- | --- | --- |
| Ungrouped daily | 19.10 | 3.29 | 22.39 |
| Grouped by ResourceId (60 rows) | not split by day | not split by day | 22.39 |
| Grouped by ResourceType and day | 38.19 | 3.29 | 41.49 |

The ungrouped and ResourceId results agree at 22.39. The type-by-day result is about double for 24 October only (for example SQL servers 21.58 on one day against about 10.7 a day over 17 to 23 October). The cause is unresolved (possible duplicate cost records for the 24th); the 22.39 figure is used as the working total and the discrepancy is an open data-quality item, not a reconciled fact. The same ResourceType ambiguity affects any Cost Management by-type figure above.

Retraction 2: "conservative upper bound ... 47.75". That was a run-rate scenario (19.10 a day extended to 12:00Z on 26 October), not an upper bound and not a proof of future cost or accrual. Lag of unknown size remains. No headroom conclusion rests on it, and the "at most about USD 2.25" statement is withdrawn. The earlier reading that all `ama` spend is incremental is also withdrawn: the owner's cap is explicitly incremental and excludes the pre-existing baseline.

Reconstruction of incremental changes since 2026-10-24T13:39Z (ARM resources API with createdTime and changedTime; names only):

* Created since cap start: none (0 of 91 resources).
* Changed since cap start: `ca-cutover-test-demo-api` (2026-10-24T14:02Z) and database `retrofit` (2026-10-25T00:23Z, the seed and obsolete-case work, with no SKU change).
* Cost Management by ResourceId for the exact resources, 24 to 25 October (reported, lagging): `ca-cutover-test-demo-api` 0.945; job resources used by owner-approved runs (`job-cutover-test-orchestrator` 0.122, `job-cutover-test-init` 0.051, the `job-bind-*` and ledger-verify jobs about 0.02 together). Registry `crcutovertestrzsrg` 2.22 and `retrofit` 11.08 are existing-baseline resources; their change attributable to incremental work (image layers, seeding load) cannot be separated from the data.
* Reconstructed incremental to date: about USD 1.1 reported for the changed app and jobs, plus an unquantified registry and database share and unknown lag (typically up to 24 to 48 hours for the latest day). This is a reconstruction, not a ledger. The owner is not asked to invent one.

Prospective price for this issue (official Azure Retail Prices API, Container Apps consumption, uksouth, queried now): Standard vCPU active 0.000034 USD per second, vCPU idle 0.000004 USD per second, memory idle 0.000004 USD per GiB second. For 0.25 vCPU and 0.5 GiB, min 0 replicas, 8 hours of active serving: vCPU about 0.25 x 28,800 x 0.000034 = USD 0.24; memory active price was not in the first retrieved rows, so memory is bounded at about the idle rate times 0.5 GiB x 28,800 = USD 0.06 (to be confirmed against the active-memory meter at plan acceptance); one kaniko build of about 15 minutes at 1 vCPU/2 GiB under USD 0.1; identity free; Key Vault operations negligible; no new environment or private endpoint. Planned upper estimate about USD 0.5. This is an estimate for stop-condition use, not a measured cost.

Headroom: not claimed. A bounded reading is plausible (reconstructed incremental about USD 1.1 plus unknowns against USD 50), but the unattributed registry and database share and the lag are not proven, so the spend gate stays closed until the cost record at Phase 1 re-reads Cost Management, states the lag and records the margin. No cap reset or new cap is assumed.

Other corrections:

* G2: the 524/523/522 counts describe the regenerated seed only, not the live database. Live equality is unverified.
* SQL view and read-only principal: a named approval from the owner or coordinator for exactly this database change is still required and must be recorded; the current request authorises no broad role or database change.
* Purge: no purge is planned and none is a deployment prerequisite. Default soft delete (7 days) retains the three exact-named secrets; the earlier purge-approval question is withdrawn.
* Withdrawn claim: "secret and the ARM deployment history carry expiry". Secret expiry does not expire ARM deployment history. The SecureString parameter values are not stored in history, but deployment records remain; no cleanup of them is claimed unless a specific, tested deletion of the exact deployment record is added to the plan.

## Addendum: Container Apps consumption meters (appended 2026-10-25T20:02Z; read-only, public sources only)

The text above, including the erratum, is preserved. This closes one gap: the active-memory meter was missing from the first retrieval and the idle-memory rate was substituted. That earlier "about USD 0.5" estimate stays withdrawn; nothing here restores it as an upper bound or as budget clearance.

Cause of the earlier gap: my earlier retrieval printed only the first 12 of 16 returned items, not a pagination fault. Verified now: the API returned Count 16 and NextPageLink null (single page) both without and with `priceType eq 'Consumption'`; every item has type `Consumption`.

Sources and retrieval (2026-10-25T19:59Z to 20:02Z):

* Prices: `https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&currencyCode=USD` with filter `serviceName eq 'Azure Container Apps' and armRegionName eq 'uksouth'` (also run with `and priceType eq 'Consumption'`, identical 16 items).
* Billing rules: `https://learn.microsoft.com/en-us/azure/container-apps/billing` (page `updated_at` 2026-03-25; ms.date 2025-12-09).

Meters (productName Azure Container Apps, UK South, USD, retail price list, not an account-specific or negotiated price):

| Meter | Unit | USD | Effective start | meterId | skuId |
| --- | --- | --- | --- | --- | --- |
| Standard vCPU Active Usage | 1 Second | 0.000034 | 2022-06-01 | 2c27faec-4865-58a4-9bca-4c64327315d3 | DZH318Z0B0NC/000B |
| Standard vCPU Idle Usage | 1 Second | 0.000004 | 2022-06-01 | d95491e7-a951-5eff-a03f-c37ad1a12bc1 | DZH318Z0B0NC/000B |
| Standard Memory Active Usage | 1 GiB Second | 0.000004 | 2022-06-01 | edbe3fc7-4303-5495-a104-88c166efe547 | DZH318Z0B0NC/000B |
| Standard Memory Idle Usage | 1 GiB Second | 0.000004 | 2022-06-01 | 0ed3fcd3-a0ae-57bb-9e09-bf1715ac6989 | DZH318Z0B0NC/000B |
| Standard Requests | 1M | 0.40 | 2022-06-01 | edca2d58-b847-565c-828a-df27aa4bae75 | DZH318Z0B0NC/000B |

All have tierMinimumUnits 0. Environment meters (Management Hour, Private Endpoint, Planned Maintenance Hour, each USD 0.125 per hour, effective 2026-09-01) bill per environment. This plan adds no environment, so it adds none of them; whether the existing environment's meters are already charged is part of the baseline, not this showcase.

Billing rules from the documentation: replicas scaled to zero incur no consumption charge; idle rates apply only when min replicas is above zero, scaled to the minimum and the replica is under 0.01 vCPU and 1,000 bytes per second; otherwise the active rate applies; only requests from outside the environment are billable and health probes are not billable; free grants are per subscription per calendar month: 180,000 vCPU-seconds, 360,000 GiB-seconds and 2 million requests.

Free-grant eligibility: unknown. The grant is shared across every Container App and job in the subscription for October, and the existing apps (for example `ca-cutover-test-api`, min 2 replicas) consume from the same pool. Whether the grant is already exhausted was not queried (no further Cost Management or live reads were made). Estimates below therefore assume no free grant, which is a pricing assumption and not a proof of the actual bill in either direction.

Formula: cost = vCPU x seconds x rate_vCPU + GiB x seconds x rate_GiB + (external requests / 1,000,000) x 0.40, with the active rate while serving and the idle rate for an idle min-replica.

Scenarios for one revision of 0.25 vCPU and 0.5 GiB (no grant, list price, replica count 1; sizing and runtime are assumptions, not plan decisions):

| Scenario | Seconds | vCPU part | Memory part | Requests | Total |
| --- | --- | --- | --- | --- | --- |
| A: min 0, active 8 h | 28,800 | 0.25 x 28,800 x 0.000034 = 0.2448 | 0.5 x 28,800 x 0.000004 = 0.0576 | 10,000 = 0.004 | about 0.307 |
| B: active whole authorised remainder, 20:00Z to 12:00Z (16 h) | 57,600 | 0.4896 | 0.1152 | 10,000 = 0.004 | about 0.609 |
| C: min 1 replica, idle all 16 h | 57,600 | 0.25 x 57,600 x 0.000004 = 0.0576 | 0.1152 | 0 | about 0.173 |
| D: B at 0.5 vCPU and 1 GiB | 57,600 | 0.9792 | 0.2304 | 10,000 = 0.004 | about 1.214 |

Scenario B and D exceed the withdrawn 0.50 figure, which confirms that figure was not a bound. These are scenario arithmetic only. They exclude the one-off image build (job consumption at the active rate, not priced here), registry storage and transfer, Key Vault operations, logging ingestion and egress, none of which was priced. Scenario figures are not an upper bound: real active time, scaling above one replica, request counts, bot traffic and any price change are unbounded by this analysis.

Unknowns that remain: free-grant balance; billing lag for the last day; the allocation of shared SQL, registry and monitoring cost to incremental work; whether any account-specific price applies. The cumulative USD 50 incremental cap is not reset, and no valid remaining-budget proof or budget clearance exists. The spend gate stays closed.

## Addendum 2: deployment-preflight facts and owner-decision dispositions (appended 2026-10-25, probes 21:08Z to 21:20Z; prospective plan `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-preflight2-plan.md`)

All earlier text and errata are preserved. Read-only management-plane queries in group `ama` only. No secret list/read, role/network change, SQL login, job start, install, push or PR. No separate critique was run (read-only research extension, no newly authorised action); that is stated, not faked. Raw JSON is kept outside the repository in `/tmp/ama462-pf2` and holds no secrets.

### Owner decisions received 2026-10-25T20:42Z (dispositions)

* Synthetic-only positive-allowlist SQL view plus a dedicated read-only principal: design approval recorded. It authorises no broad access, no creation yet, and does not authorise starting a billable private job before the budget gate.
* Existing private vault `kv-cutovertest-rzsrg` selected for demo-password storage and private owner retrieval. This names the vault; it is not a role, network grant or proven retrieval path.
* Resident-only window stays to 2026-10-26T12:00Z; the cumulative USD 50 incremental cap is not reset and excludes the pre-existing baseline; USD 700 applies to `ama` for October only. General live repair authority has expired. Ungated planning push `5963fa3f` remains a disclosed, unresolved deviation not covered by the owner's #436/#459 process acceptance. No production resident acceptance is inferred.

### G1: refreshed Cost Management ledger (ActualCost, USD, group `ama`)

Reconcilable dimensions: ungrouped daily and ResourceId by day agree exactly (103 rows). Cost Management is lagging and revising: 24 Oct 19.096 (unchanged); 25 Oct 5.689 now against 3.294 seen at 16:45Z and 21:00Z earlier, so the latest day rose by about 2.4 USD as data arrived. Total 24.785 since the day of the cap start (daily granularity cannot split 13:39Z). The earlier ResourceType-by-day duplicate ambiguity for 24 Oct stays disclosed and unresolved; no by-type figure is used here.

| Resource (ResourceId) | 24 to 25 Oct USD | Classification |
| --- | --- | --- |
| `retrofit` database | 11.233 | pre-existing baseline; incremental share (seed load, no SKU change) unquantified |
| private endpoint group (combined names) | 3.833 | baseline |
| `crcutovertestrzsrg` registry | 2.640 | baseline; incremental image storage share unquantified |
| `ca-cutover-test-api` | 1.610 | baseline |
| `ca-cutover-test-demo-api` | 1.257 | changed 2026-10-24T14:02Z, owner-authorised work: incremental candidate |
| `job-cutover-test-orchestrator` / `job-cutover-test-init` | 0.150 / 0.069 | owner-approved runs: incremental candidates |
| `log-cutover-test` workspace | 0.329 | baseline; logging share unquantified |
| `kv-cutovertest-rzsrg` | 0.000 | none |

Incremental candidates reported: about USD 1.5 (app 1.257, jobs 0.22), up from 1.1 in the earlier reconstruction because of lag. Unquantified, not invented: registry image-storage share of 2.640, database share of 11.233, logging share of 0.329. No resources were created after the cap start (earlier ARM check). These are actual lagging charges, not a forecast; no forecast or scenario value is mixed into them.

### Pricing of proposed incremental components (public retail API, UK South, USD, 2026-10-25T21:1xZ)

* Container Apps compute: meters and scenarios in Addendum 1, unchanged. About 0.609 for 16 h active at 0.25 vCPU/0.5 GiB is compute only and is not a total bound.
* Registry (Premium): Data Stored USD 0.10 per GB-month; Premium Registry Unit 1.6666 per day is a fixed existing cost not added by this work; ACR Task vCPU Duration 0.0 per second to 6,000 seconds then 0.0001 per second. A build of about 15 minutes (900 s at 1 vCPU) falls in the zero-priced tier only if the task free tier has not been used this period: unknown. Image growth of an assumed 0.3 GB is about USD 0.03 a month pro-rated, an assumption not a measurement.
* Log Analytics: ingestion USD 0.00 for the first 5 GB then 2.88 per GB (list; the workspace's actual SKU and commitment are unknown); app console logs are the main source. Volume for one small app is unmeasured: unknown, bounded only by choosing a log cap.
* Key Vault Standard: operations USD 0.03 per 10,000; three secrets with a few hundred reads is well below USD 0.01. The existing vault's standing cost is baseline.
* Egress: the Bandwidth service query returned 0 items for the filter used; I could not prove a UK South egress price. Egress for a small text page is expected to fall inside Azure's monthly free allowance, but that is not proven here: unknown.
* One-off components not priced: image build compute beyond the ACR Task tier, SQL view/principal creation job (explicitly not authorised to start before the budget gate), private retrieval client.

Conclusion: a complete, defensible remaining-headroom proof does not exist. Missing: the incremental shares of registry, SQL and logging, the Cost Management lag on the last day, the free-grant balance, the egress price and log volume. Cloud mutations stay stopped.

### G4: owner retrieval path (ARM metadata and role assignments, no data-plane call)

* Vault `kv-cutovertest-rzsrg`: Standard SKU, RBAC authorisation on, public network access Disabled, ACL default Deny, bypass None, no IP or VNet rules, soft delete on (7 days), purge protection not enabled. A private endpoint `pe-kv-cutovertest-rzsrg` exists, Approved, in subnet `snet-pe` of `vnet-cutover-test`.
* Roles on the vault scope including inherited: one Key Vault Secrets User for a service principal at vault scope (identity not resolved here); Owner for 2 users, 5 service principals at subscription scope and 1 at group scope; no Key Vault Secrets Officer or Administrator assignment found. Owner is a management-plane role and does not confer secret read or write.
* Network: the virtual network has three subnets (`snet-aca`, `snet-pe`, `snet-aca-demo`), no peering, and the group holds no VM, Bastion, VPN or DNS-resolver resource. A person's laptop cannot reach the vault's private endpoint, so there is no usable existing private retrieval path for the owner.
* Minimal missing actions, none taken: (1) a data-plane role at the single secret scope for the owner (Key Vault Secrets User on `resident-demo-password` only, time-bound to 2026-10-26T12:00Z) after the secret exists; (2) a private client to read it, which means either a private job or workload inside the environment that outputs to the owner by a channel the owner designates, or a new private access resource (VM, Bastion, VPN or peering), each of which adds cost and a network change and so needs named owner approval after the budget gate. The vault selection does not supply either. The writer of the secret is the existing secure ARM deployment (management plane), which does not need a data-plane role, so storage is feasible but retrieval is not yet.
* The vault's soft-delete retention (7 days) and absent purge protection are unchanged; no purge is planned.

### Hard gates still open

1. #444/PR #455 merge, with the fresh gate running; coordinator resume.
2. Complete remaining-headroom proof (G1 unknowns above).
3. Named approval for any role at secret scope and for a retrieval client or private job, plus the budget gate before any billable job (the SQL view/principal creation included).
4. Live equality of `retrofit` with the regenerated seed (counts-only, private path).
5. Disposition of the ungated push `5963fa3f`; no push until the full gate is verified.

### Erratum to Addendum 2 (2026-10-25)

Addendum 2 says the raw JSON is kept in `/tmp/ama462-pf2`. That is wrong: the directory was deleted after the addendum was written, in the same command. The raw Cost Management and role-assignment JSON is no longer available. The figures in Addendum 2 are the preserved record. Any later cost refresh must be re-queried and kept outside the repository this time.

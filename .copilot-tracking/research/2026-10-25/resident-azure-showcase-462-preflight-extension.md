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

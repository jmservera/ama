# Issue 462 release preflight evidence (2026-10-25T22:18Z to 22:30Z)

Prospective plan: `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-release-preflight-plan.md`
(written before any probe). Read-only management-plane queries in group `ama` only. No secret list
or read, no Azure write, job start, SQL query, role or network change, push or full gate. No
application source was edited. Candidate `aaee4d32` is assessed separately by the coordinator.

## Private raw evidence (retained, not in the repository)

Directory `/home/azureuser/.ama462-evidence/release-preflight-2026-10-25` (mode 0700, files 0400),
sanitized non-secret metadata only, not to be deleted. Manifest `SHA256SUMS` inside it. Query time
2026-10-25T22:18Z to 22:20Z (`retrieved-at.txt`, `finished-at.txt`). Key hashes (SHA-256):

| File | SHA-256 |
| --- | --- |
| `cost-none.json` | `d770370df8aea71446a14919427747895b9ffe7e7ee54cdf85d27afcee2bd7f2` |
| `cost-ResourceId.json` | `cedc38c2547747f5c894601685895bf0413bfa7d2c39dc43a761b6a3133516d2` |
| `cost-october-mtd.json` | `911c06df9bcd5e34e4e5c0d155081db9cda5fa9087afdc88c276f06376be9752` |
| `resources.json` | `497bd899d50ad10f29bea6bd890ad169c96040610c28ce908bb48e3355b41d3c` |
| `vault-roles.json` | `2d8fe6bc0abca91eda30ea190fa6aec5ec947398fe794ab9d06893d6e9921c7d` |

The coordinator can recompute totals from these files. Earlier deleted-raw summaries are historical
only and are not relied on here.

## Cost ledger (Cost Management, ActualCost, USD, group `ama`)

* Coverage: custom period 2026-10-24 to 2026-10-25 (daily granularity, so the 13:39Z cap start cannot
  be split inside 24 Oct). Ungrouped: 2 rows. By ResourceId by day: 103 rows, one page, no nextLink.
* Reconciliation: both shapes give 24 Oct 19.096 and 25 Oct 6.372, total 25.468. Earlier reading of
  25 Oct was 5.689 (about 21:10Z), so the open day is still rising through lag (about +0.68 in about
  1.2 hours). Day 25 is incomplete and its final value is unknown.
* October month to date (1 to 25 Oct, one row): 303.711. The USD 700 October ceiling applies to `ama`
  only; this is an actual lagging figure, not a ceiling or a forecast.
* By resource (24 to 25 Oct): `retrofit` 11.283 (24 Oct 10.790, 25 Oct 0.493), the managed-environment `privateendpoint` resource 4.017 (eight
  `Microsoft.Network/privateEndpoints` add 3.280; the remaining resources are not itemised here and are in
  `cost-ResourceId.json`), registry 2.779, `ca-cutover-test-api` 1.696, `ca-cutover-test-demo-api` 1.283
  (0.493, 0.790), `log-cutover-test` 0.346, `job-cutover-test-init` 0.069, `job-cutover-test-orchestrator`
  0.160.

## Baseline versus work-created or changed (ARM metadata)

* No resource in `ama` was created after 2026-10-17T11:13Z (`resources.json` createdTime). Nothing
  was created since the cap start.
* Changed since the cap start: `ca-cutover-test-demo-api` revision `--0000006` created
  2026-10-25T12:18Z (min 0, max 4, 0.5 vCPU / 1 GiB, external ingress, 0 replicas now); this
  corrects the earlier "changed 2026-10-24T14:02Z" wording. `retrofit` changedTime 2026-10-25T00:23Z;
  its SKU now is Standard S0, capacity 10 DTU, 30 GiB, zone redundant false (preserved). Its 24 Oct
  cost of 10.79 against 0.49 on 25 Oct shows a higher-cost state on 24 Oct; the exact hours are not
  provable from daily data.
* Executions since the cap start: `job-cutover-test-init` 6 runs, 367 s in total; the 5-minute
  orchestrator cron (baseline, created 16 Oct) 100 runs listed, 2,945 s (the list may be truncated).
  ACR task runs since the cap start: 2, both Failed (24 Oct 20:42Z); durations not returned.

## Incremental-spend bounds (two methods, no ledger asked of the owner)

* Method 1, over-inclusive attribution scenario (not a bound and not used for any gate; the 10.30 is a
  day-to-day difference, not proof of post-cap causation, and the demo app figure spans 24 Oct): `retrofit`
  excess over the 25 Oct day 10.30, demo app 1.283, init job 0.069, two failed ACR builds up to
  about 0.20 (assumed 600 s each at 1 vCPU and 0.0001 per second), registry excess over 25 Oct about
  0.56. Total about USD 12.4 reported. Add a lag reserve of USD 3 (about 25 percent of that and a
  full-day completion of 25 Oct): about USD 15.4.
* Method 2, all-in (counts baseline too, so far stricter than the owner's definition): reported
  25.468, plus completion of 25 Oct to an assumed 8/day (about +1.6), plus the run to 2026-10-26T12:00Z
  at an assumed 8/day for 13.7 hours (about +4.6): about USD 31.7 before any new deployment. The
  earlier projection of 47.75 used the 24 Oct run rate (19.10/day) that contained the database spike;
  it was a scenario, not a bound. The 8/day rate is an assumption read from the 25 Oct pace, not a
  proven ceiling.
* Neither method is a hard monetary ceiling: Cost Management lags and the last-day lag is unbounded.

## Priced minimal deployment to 2026-10-26T12:00Z (list retail, UK South, no free grant assumed)

Bounds to apply: at most 1 replica, min 0, 0.25 vCPU / 0.5 GiB (the 0.5 / 1 GiB case as the upper
variant), existing environment `cae-cutover-test-demo`, existing registry and workspace. Meter
prices are those in Addendum 1 of the preflight extension. Formula in that addendum.

| Component | Conservative USD | Basis |
| --- | --- | --- |
| App compute, 16 h active | 0.609 (0.5 / 1 GiB: 1.214) | Addendum 1 scenarios B and D |
| Requests | 0.40 | 1,000,000 external requests at 0.40 per million; rate limiter and cap bound real use far lower |
| Image builds | 0.27 | 3 builds x 900 s x 1 vCPU x 0.0001, assuming the ACR task free tier is spent |
| SQL view and principal job | 0.05 | init job runs observed at about 60 s each, 6 runs 367 s; padded |
| Key Vault operations | below 0.01 | 0.03 per 10,000 |
| Image storage | 0.03 | 0.3 GB assumed at 0.10 per GB-month, pro-rated |
| Logging | 2.88 | assume 1 GB at 2.88 per GB with the free 5 GB used |
| Egress | 0.44 | assumption: 5 GB at about 0.087 per GB; UK South price not proven (retail query returned none earlier) |
| Subtotal (sum of rows) | about 4.7 (compute variant about 5.3) | |
| Contingency to round up | 0.7 | covers rounding and unpriced small items |
| Lag reserve (100 percent of 5.4) | 5.4 | |
| Deployment total to book | about 11 (5.4 + 5.4, rounded up) | |

Booked against Method 2: 31.7 + 11 = about 43, then a further explicit 5 lag reserve on the shared
baseline accrual gives about 47.7, under 50 with only about 2.3 margin. Against the Method 1 scenario:
15.4 + 11 = about 26.4 (not used for the gate). Both rest on stated assumptions and unbounded lag, so neither is proof.

Enforceable bounds present or absent (facts): workspace `log-cutover-test` is PerGB2018, retention 90
days, daily cap -1 (none) and it is shared, so a log cap cannot be enforced without changing it,
which is out of scope; app-side limits are the only log control (the limiter, the 2 KiB body bound,
no request-body logging). Scale max 1 and min 0 and the container size are enforceable in the app
definition. Budget alerts are notifications, not ceilings.

## Paths and principals (metadata only)

* SQL initialization job `job-cutover-test-init` (identity `id-cutover-test-init`, 0.5 vCPU / 1 GiB,
  600 s replica timeout, manual trigger, environment `cae-cutover-test`). Its role assignments: AcrPull
  and AcrPush on registry `crcutovertestrzsrg`, custom "Staff initializer result tags" on the job and
  "Staff initializer API restart" on `ca-cutover-test-demo-api`. No vault role. Its SQL authority is
  the SQL Entra admin per earlier evidence; not queried now.
* Vault `kv-cutovertest-rzsrg`: Key Vault Secrets User for `id-cutover-test-api` only, at vault scope;
  Owner for service principals and users at subscription or group scope; no Secrets Officer or
  Administrator anywhere. Owner does not confer data-plane write.
* Dedicated workload read path: `id-cutover-test-api` also holds storage, queue, IoT and ACR roles,
  so reusing it for the resident app would be broad. Recommend one new dedicated user-assigned
  identity (no cost) with Key Vault Secrets User scoped to exactly two secret resources
  (`resident-demo-password-verifier`, `resident-demo-session-key`) and AcrPull on the one registry.
* Verifier and session key write path (hypothesis from the repository's `credential_arm.py` pattern,
  not tested): an ARM deployment of the two secrets as `Microsoft.KeyVault/vaults/secrets` with
  secure parameters, which a management-plane Contributor or Owner can do while data-plane access is
  denied by the private network. This needs no human vault access, but it does need the owner to
  pass the verifier through a secure channel to the deployment step, and ARM deployment history
  stores only non-secure parameter values; the secure parameter handling has not been exercised.

## Verdict

* Budget: not a proof, but a defensible conditional release. Under both methods the booked total is
  below USD 50, but with only about 2.3 margin on the strict all-in Method 2 and its added lag reserve. That is a
  thin, conditional release and not a clearance. Lag and the free-grant balance stay unknown.
* Smallest missing owner decision (one): accept Cost Management actuals queried immediately before
  each paid step, with the all-in Method 2 figure as the conservative proxy, and a stop condition: do
  not start, and stop, if the all-in reported total since 2026-10-24 is at or above USD 27.8 (50 minus 11 deployment, 5 lag and 6.2 remaining baseline accrual; the current
  25.5 leaves 2.3), or if October month-to-date for `ama` exceeds USD 600. The owner is not
  asked for a ledger.
* Hard gates still open: coordinator assessment of `aaee4d32`, complete exact-head gate and hosted
  checks, named approval to create the dedicated identity and the two secret-scoped roles, live
  equality and provenance of the at most 25 mappings (G2, private SQL path), and the private job
  start (budget gate above).
* Residuals: lag on the last day, free-grant balance, egress price, the unproven ARM secret-write
  route, the ACR failed-build duration, and the reason for the 24 Oct database cost.

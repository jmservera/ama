<!-- markdownlint-disable-file -->

# Task Research: paid-execution-plan-126

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Research disposition | executed |
| Planning Readiness | Ready (documentation-only; plan for owner approval, no execution) |
| Artifact path | .copilot-tracking/research/2026-10-20/paid-execution-plan-126-research.md |

## Research Brief

Prepare a finite costed execution plan, for separate owner approval, that gives the
shortest safe route to a usable unfinished Azure synthetic demo. Scope: actual-model
evaluation (#108/#222/#223), Azure validation (#117/#122/#358/#360) and sizing
(#137/#360). Non-goals: any deployment, allocation, inference, permission, resource
group or job change; issue acceptance; operational release; new standalone page.

Owner evidence (issue #126 comments 6290697705, 6295338398, 6301554087): USD 500 is the
TOTAL calendar-month cap including accrued charges; authorization expires
2026-10-25T16:02Z; unknown charge/price blocks execution; the plan itself is not approval;
RG `ama` is never deleted; identities/access-bearing resources are preserved.

## Evidence Collected (read-only, 2026-10-20 21:18-21:25 UTC, Azure CLI 2.91.0)

Subscription, tenant, resource IDs and private bindings are intentionally not recorded.

| ID | Query (management plane GET/list/POST-query only) | Result | Limit |
| --- | --- | --- | --- |
| E1 | Cost Management query, RG `ama` scope, ActualCost, 2026-10-01..20, by ServiceName | USD 189.94 total; SQL Database 91.92, Front Door 41.25, Container Apps 21.84, Virtual Network (private endpoints) 16.39, Container Registry 14.55, Log Analytics 1.88, IoT Hub 1.29, others under 0.40 each; Foundry Models 0.034 | Only RG `ama`. Subscription-scope query and `az consumption` returned RBACAccessDenied, so subscription-level or other-RG charges, credits, tax and commitments are UNKNOWN. A `az group list` showed only `ama` |
| E2 | Same, daily | 10-11 3.88, 10-12 14.31, 10-13 15.63, 10-14 16.20, 10-15 16.10, 10-16 16.17, 10-17 29.69, 10-18 30.26, 10-19 30.22, 10-20 17.47 | 10-20 is partial/incomplete at query time. Billing latency bound is not established; reserve covers it |
| E3 | Same, 10-18..19 by resource | SQL `retrofit` 21.32, Front Door profile 21.29, old environment private endpoint 4.80, registry 3.33, demo API 2.11, old API 2.08, IoT 0.65, workspace 0.61, eight private endpoints 0.48 each, orchestrator job 0.19; total 60.49 | Two-day sample; run rate USD 30.245/day |
| E4 | `az resource list -g ama` | 94 resources, including 3 container apps (min replicas 0/2/2, 0.5 vCPU, 1 GiB each), 2 managed environments, 8 jobs (orchestrator schedule every 5 minutes, ledger verify nightly), 1 Front Door Premium profile with WAF, 8 private endpoints, SQL server with `retrofit` `GP_S_Gen5` 2 vCore max, 0.5 min, auto-pause 60 minutes, Premium registry, IoT `B1`, Foundry `S0` AIServices with project, storage LRS, vault, workspace, 5 user-assigned identities | Inventory only; no configuration payloads |
| E5 | Azure Monitor `app_cpu_billed`, SQL `retrofit`, daily | 16 Oct 26,658; 17-19 Oct about 57,860 vCore-seconds/day; 20 Oct 50,640 (partial) | Billed continuously (about 0.67 vCore average); the 5-minute orchestrator job and replicas plausibly prevent auto-pause, not proven |
| E6 | `az cognitiveservices account deployment list` | Empty: no model deployments exist | Inference cannot run until two deployments are created |
| E7 | `az cognitiveservices model list --location uksouth` | `gpt-4.1` and `gpt-4.1-mini`, version `2025-04-14`, lifecycle Legacy, inference deprecation 2027-04-14, GlobalStandard default capacity 10 | Catalog fact only; subscription quota/usage is the unresolved 2026-10-18 R9 Unknown |
| E8 | Azure Retail Prices API (public, no credentials), USD, list price, retrieved 2026-10-20 | gpt-4.1 global input 0.002/1K, output 0.008/1K; gpt-4.1-mini input 0.0004/1K, output 0.0016/1K; Container Apps vCPU 0.000034/s active, 0.000004/s idle, memory 0.000004/GiB-s, environment private endpoint 0.125/h; Premium registry 1.6666/day; IoT B1 10/month; Log Analytics ingestion 2.88/GB over free tier | List prices, not agreement/credit prices. No numeric public rate returned for SQL serverless or Front Door Premium; their cost is taken from observed E3, not a quote |

Repository evidence (all existing, read only): `infra/README.md` (UK South pilot capability
2026-10-18, private-publication blockers 2026-10-17/19, restricted demo staging 2026-10-17,
in-VNet SQL staff step, cost proposal 2026-10-16), `src/agents/README.md` (finite
`ZF_ASSIST_*` call/token allowance and authority), `src/agents/evals/*.json` (10 priority
and 24 chat scenarios, scripted/dev fixtures, not held-out), issue #108 criteria.

## Findings

1. **Headroom is not USD 500 and is negative at the current run rate.** Complete days
   1-19 Oct total USD 172.47. At USD 30.245/day, 12 days (20-31 Oct) add USD 362.94, giving
   a USD 535.41 month-end projection with no new activity (headroom -35.41). Paid
   execution is therefore BLOCKED unless the owner first reduces idle burn.
2. Two lines are 71% of burn: SQL `retrofit` USD 10.66/day (never pausing) and the old
   Front Door Premium edge USD 10.64/day. The #360 direct demo makes Front Door optional;
   `infra/public-edge-existing.bicep` can recreate it.
3. Retiring Front Door from 21 Oct gives USD 418.32 (headroom 81.68). Also pausing SQL
   after the 25 Oct window (conservative 50% saving, USD 33.57) gives USD 384.74
   (headroom 115.26).
4. Inference is small relative to idle infrastructure: the worst case for 300 mini plus
   100 gpt-4.1 calls at the existing 12,000-character input and 600-token output bounds is
   USD 4.61. The cost risk is idle estate, not tokens.
5. A usable demo needs no new resources: the restricted demo API (403 deny-all) exists;
   sign-in is blocked by an invalid managed-identity client sentinel, no tenant
   registration/roster/role evidence, and no private-connected executor (SQL is
   private; ACR publication blocked: B2s `NotAvailableForSubscription`, B2als_v2 and
   D2as_v5 `SkuNotAvailable`, ACR pools not offered in UK South). Known capacity failures
   are not retried here.
6. Both models are Legacy with retirement after the window (2027-04-14); acceptable for a
   five-day exercise but must be restated in approval.
7. Redirects and 403 prove only that ingress is reachable and restricted; they are not
   sign-in evidence.

## Alternatives Considered

* Run everything locally: free, already possible for synthetic data (`ZF_AUTH=password`,
  sqlite store) but cannot satisfy Azure endpoint/identity/SQL/real-AI acceptance
  (CON-007/AC-086). Chosen as the first stage of every tranche.
* Allocate new publisher VM or ACR pool: rejected for this plan; capacity failures known.
* New SQL region or Basic DTU database: not costed from evidence; deferred as T4 analysis.
* Subscription-scope billing for headroom: not permitted for this identity; requires owner.

## Planning Readiness

Ready for a documentation-only plan. Open items are owner decisions, not research gaps:
subscription-level charges, retirement/disposition choice, approvals and human gates.

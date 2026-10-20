<!-- markdownlint-disable-file -->

# Task Research: paid-execution-plan-126-recovery

| Field              | Value |
|--------------------|-------|
| Date               | 2026-10-20 |
| Researcher / agent | rpi-research skill (actually invoked 2026-10-20T21:25Z after coordinator intervention) |
| Status             | In progress |
| Artifact path      | .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md |

## Recovery Disclosure

Before this skill was invoked, the worker authored `paid-execution-plan-126-research.md`, `-plan.md`, `-phase-details.md` and a rubber-duck `-plan-critique.md` directly, without activating rpi-research or rpi-plan. Those four files are preserved unchanged as UNVERIFIED pre-RPI draft material. They are not skill outputs, the critique is not the required rpi-plan critique, and nothing in them is claimed as a previously executed phase. This artifact is the first genuinely executed Research for the task; its evidence rows are re-verified here, not inherited.

## Research Brief

* What to research: what a finite, costed, owner-approvable plan for a usable unfinished Azure synthetic demo must contain; the actual October charges, idle burn, liabilities and USD 500 headroom; whether the draft figures and options survive re-verification.
* Why it matters: owner must separately approve a plan before any paid execution; unknown spend blocks execution.
* Audience or intended use: project owner (approval), then rpi-plan.
* Scope: read-only RG `ama` cost/inventory metadata, public retail prices, existing repository documents (addendum EXA-012, infra/README, src/agents README, issue #126 and cited comments).
* Non-goals: any deployment, allocation, inference, permission, job, resource-group change; acceptance; operational release; new standalone page; editing other loops' documents.
* Criteria: each figure carries provenance, date, currency and limit; unknowns stay explicit; proposals stay proposals.
* Requested outputs: evidence-backed findings and Planning Readiness.
* Output mode: convergence (selects the options the plan should present; not an implementation of paid work).

## Research Parameters

| Field | Value |
|-------|-------|
| Research question(s) | Q1-Q6 below |
| Codebase scope | docs/case_study_48_addendum.md, infra/README.md, src/agents, docs/reference |
| External scope | Azure Retail Prices API (public); Microsoft Learn pricing/billing pages |
| Initial internal candidate areas | addendum EXA-012 cap rows; infra README cost proposal and blockers; src/agents README allowance table |
| Initial external candidate areas | prices.azure.com retail API; Cost Management query API behaviour |
| Research posture | focused |
| Posture provenance | default: bounded internal task with named sources and prior evidence; widening only to billing-scope alternatives |
| Explicit limits / deadline | authorization expiry 2026-10-25T16:02Z; no cloud mutation; no inference; no new resources |
| Posture-specific completion basis | scope and materiality |
| Edits allowed during research? | no, research-only (this artifact only) |
| Resolved evidence root | .copilot-tracking/ default |
| Known constraints / excluded sources | no IDs/secrets; subscription never changed; USD 500 TOTAL cap |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope; repository instructions; rpi-research contract; domain skills; preferences.

| Kind | Candidate | Match and provenance | Scoped authority | Selected / skipped |
|------|-----------|----------------------|------------------|--------------------|
| Instruction | AMA repository instructions (applyTo `**`) | matches all paths | Knowledge-base, regulatory evidence, branch rules | selected |
| Instruction | Coordinator contract /tmp/ama-wave-20261020-2113-common.md | caller | write boundary, no push, gate | selected |
| Skill | rpi-research | actual invocation this session | phase contract | selected |
| Skill | web-design-guidelines etc. | no web/UI change | n/a | skipped: documentation only |
| Research specialist | RPI Researcher | not visible in host agent list | n/a | skipped: lanes small and coupled; inline fallback, no worker evidence claimed |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers | Decision |
|------------|----------------------------------------|---------|----------|
| Intake | Non-interactive session; owner comments and coordinator brief supply scope | n/a | Proceed with recorded assumptions |
| Direction change | Coordinator intervention 2026-10-20T21:25Z: rerun genuine RPI; preserve draft | user direction | Draft demoted to unverified input; revalidate |
| Convergence | No interaction available | n/a | Residual owner decisions recorded as unresolved |

## Scope and Success Criteria

* Scope: as above. Assumption to verify: draft figures E1-E8 in the pre-RPI research file.
* Success: each question answered or marked unanswerable; evidence IDs on every claim; unknowns explicit.

## Task Research Requests

* Explicit: finite costed plan options; actual October accrued charges and caveats; idle burn and liabilities; headroom; first deployment tranche; local-first versus Azure-only; expiry, cleanup, recreation; owner-testable-now statement.
* Constraints: no execution; no acceptance inference.

## Direction Controls

| Control | Direction | Source | Effect |
|---------|-----------|--------|--------|
| change | Treat prior draft as unverified; re-run research via skill | coordinator 2026-10-20T21:25Z | Full cycle below revalidates figures |
| exclude | Do not edit infra/README.md, form packs, map docs, cohort pack | coordinator brief | Domain edits confined to addendum synthesis, index, log |
| exclude | No retries of known capacity failures | coordinator brief | Capacity options not probed |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|--:|--------------|------|----------|--------|
| Q1 | What are actual October accrued charges (RG `ama`), with latency/incompleteness caveats and visible gaps? | depth | H | pending |
| Q2 | What is the current idle burn per resource and are the draft's SQL/Front Door findings true? | depth | H | pending |
| Q3 | What liabilities exist (existing resources, retention, minimums) and what is USD 500 headroom? | breadth | H | pending |
| Q4 | What finite call/token/model/resource bounds are supportable and priced? | breadth | H | pending |
| Q5 | What does a usable unfinished demo need that exists, and what is blocked (private bootstrap, tenant, roster, publisher)? | breadth | H | pending |
| Q6 | What counter-evidence challenges the draft's options (cost model, SQL pause saving, Front Door retirement, reserve)? | depth | H | pending |

## Prior Knowledge Gate

* Existing artifacts reviewed: the four pre-RPI draft files; addendum EXA-012 row; infra/README (2026-10-16 cost proposal, 2026-10-17/19 blockers, 2026-10-18 capability evidence, 2026-10-17 demo staging receipt); src/agents README allowance section.
* Reused (to verify): all draft E1-E8 figures.
* Superseded: none yet.

## Research Cycle Log

### Cycle 1

* Active direction controls: all above. Posture: focused; completion basis scope and materiality. Deadline: no effect on research.

#### Wave 1: Wider

* Plan and lanes: inline (no RPI Researcher worker visible; coupled low-volume reads). Fallback limitation: no independent lane evidence exists.
* Evidence relationships: Q1 to C1, C2, W2; Q2 to C3, C4, C5; Q3 to C1, C6, C7; Q4 to C8, W1; Q5 to C9, C10.
* Reflection: fresh 2026-10-20T21:25Z queries reproduce the draft total exactly (189.94 USD) so the draft cost basis is supported at RG scope. Missing: subscription scope, credits, tax, support. Prioritised for Wave 2: SQL burn mechanics, orchestrator/SQL coupling, Front Door dependency, expiry-window projection.

#### Wave 2: Deeper

* Prioritised: Q2 SQL and Front Door; Q3 headroom arithmetic; Q4 token envelope.
* SQL: `app_cpu_billed` 57,860 vCore-s/day = 16.07 vCore-h/day against a floor of 12.0 (0.5 vCore x 24 h) when online; implied rate 0.663 USD/vCore-h. Online status is Online with no paused date (C4). The orchestrator job (CMD `python -m zava_forward.orchestrator`, 0.25 vCPU, runs every 5 minutes) is in the same module that sets `ZF_STORE=mssql` for workloads (C5, C11), so it plausibly keeps SQL awake; the coupling is inferred, not proven.
* Front Door: profile Premium, one origin and one route both Enabled; the old internal environment (public access Disabled, internal) is its private-link origin; the demo API is on a separate external environment (C3, C12). Front Door is the only Premium-base meter (41.25 of 189.94, 10.64/day). Daily cost stepped from about 16 to about 30 USD on 17 Oct (C2), consistent with the edge and demo environment being added; causation inferred.
* Headroom: complete days 1-19 = 172.47. Run rate 30.245/day (18-19 Oct mean). Projection with no new activity and no change = 172.47 + 12 x 30.245 = 535.41, headroom -35.41 USD (C1, C2). 20 Oct is partial at query time (17.47, still accruing).
* Inference: per-call bound from the existing `ZF_ASSIST_*` defaults (12,000 input characters, 600 output tokens) at list prices gives 0.00576 USD (gpt-4.1-mini) and 0.0288 USD (gpt-4.1); 300 mini plus 100 gpt-4.1 calls = 4.61 USD (W1, C8). No model deployments exist (C13), so inference cannot occur before two deployments are created; their quota is the unresolved Unknown from 2026-10-18 (C14).
* Reflection: idle estate, not tokens, dominates. Two options matter: edge retirement and SQL idling.

#### Wave 3: Contrarian

* Challenge targets: (a) the draft's 50 percent SQL saving; (b) Front Door removal being free of side effects; (c) USD 30 reserve sufficiency; (d) RG-scope total being the whole liability; (e) draft treating subscription denial as a footnote.
* (a) Weakened: the saving is not provably 50 percent. If SQL pauses, compute stops entirely (up to about 10.66 USD/day) but only after 60 idle minutes with no connection from min-2 API replicas, the demo API (min 2) or the 5-minute job; stopping the schedule alone may not suffice. Storage (1.55 USD so far) continues. Evidence: C4, C5, C15. The plan must present the saving as a range with a measured check, not a promise.
* (b) Partly supported: removal does not affect the demo API path but removes the only working historical edge and its rollback value; README requires a separate retirement approval after d (C12). Not an identity or access-bearing resource, but it is an owner disposition, not an assumption.
* (c) Weakened: Cost Management data is estimated until invoiced, excludes credits and support, and can lag; the reserve is an assumption (W2). Billing latency magnitude is not established for this subscription.
* (d) Supported with limit: RG `ama` queries return Usage/OnDemand only (no credit or reversal lines) and September is empty for the RG; the subscription-scope query and `az consumption` were denied and the CLI lists only RG `ama` (C1, C16). Therefore total subscription spend and any other-RG charges are UNKNOWN to this identity. This blocks paid execution until the owner supplies subscription-scope charges, regardless of option chosen.
* (e) Accepted: subscription-scope visibility is promoted to a gating unknown.
* Reflection: counter-evidence changes the draft: saving ranges, explicit gating unknown, and no execution under any option until subscription-scope charges are recorded.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Disposition | Rationale | Treatment |
|------------------|--------------|-------------|-----------|-----------|
| RG `ama` October accrued 189.94 USD (to 20 Oct, partial) | C1, C2, W2 | accepted with caveat | Reproduced twice; estimated, excludes credits/support | Finding F1 |
| Subscription-scope spend unknown | C16 | accepted | Query denied; cannot assume | Blocking unresolved decision |
| Month-end projection 535.41 (headroom -35.41) at current burn | C1, C2 | accepted as projection | Arithmetic from observed burn | F2 |
| Front Door retirement saves about 10.64 USD/day | C3, C12 | accepted as option, needs owner approval | Observed meter, separate approval rule | Option O1 |
| SQL idling saves 50 percent | C4, C5, C15 | rejected as stated; replaced by range 0 to 10.66 USD/day | Contrarian wave | Option O2 with measurement |
| Inference worst case 4.61 USD | W1, C8 | accepted as bound at list price | Pricing public, units explicit | F4 |
| USD 30 reserve | W2 | deferred | Not evidenced; plan must justify or require owner figure | Unresolved |
| Demo usable by sign-in | C9, C10 | rejected as current state | 403 deny-all and invalid sentinel | F5 |

#### Cycle Re-entry Evaluation

* Another complete cycle needed: no.
* Trigger or stop basis: scope coverage and materiality; remaining items are owner-only data (subscription charges, approvals, tenant, roster) that further research by this identity cannot supply. Source redundancy reached on RG cost data.
* Revised brief or revalidation required: none beyond the intervention control.
* Readiness effect: Ready to plan options and gates; Blocked for any execution.

## Evidence Log

* Delegation: inline: no suitable worker visible; no lane artifacts exist.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
|----|-----------------|----------|------|------------|-------|
| C1 | RG `ama` ActualCost 2026-10-01..20 = 189.94 USD, by meter: SQL vCore 90.36, Front Door Premium base 41.25, Standard private endpoint 16.39, Premium registry 14.41, Container Apps meters about 23, Log Analytics 1.89, IoT 1.29 | Azure Cost Management query (private, 2026-10-20T21:25Z) | az rest POST query | high | Usage/OnDemand only; amortized equal; September empty |
| C2 | Daily: 10-11 3.88; 12-16 14.3-16.2; 17-19 29.7-30.3; 20 partial 17.47 | same, daily | az rest | high | 20 Oct incomplete |
| C3 | Front Door Premium profile, one origin and one route, both Enabled | Azure resource state (private) | az afd list | high | |
| C4 | SQL `retrofit` GP_S_Gen5, 2 vCore max, 0.5 min, auto-pause 60 min, Online, not paused | Azure resource state | az sql db show | high | |
| C5 | Orchestrator job schedule `*/5 * * * *`, 0.25 vCPU/0.5 GiB, CMD python -m zava_forward.orchestrator | src/orchestrator/Dockerfile:29 ; Azure job state | read, az containerapp job show | high | SQL coupling inferred |
| C6 | Resource inventory: 94 resources, 3 apps, 2 environments, 8 jobs, 8 private endpoints, Premium registry, IoT B1, Foundry S0, storage, vault, workspace, 5 identities | Azure resource list | az resource list | high | Counts only |
| C7 | Existing liabilities are recurring daily meters; no commitments or reservations appear (all OnDemand) | C1 | query | medium | Subscription-level unknown |
| C8 | `ZF_ASSIST_*` defaults: input 12000 chars, output 600 tokens, call and token allowances finite | src/agents/README.md:389-426 | read | high | |
| C9 | Demo API returns 403 under deny-all; invalid managed-identity client sentinel; no browser credential | infra/README.md:2575-2640 | read | high | Dated 2026-10-17 |
| C10 | Private bootstrap blocked: B2s NotAvailableForSubscription, B2als_v2/D2as_v5 SkuNotAvailable, ACR pools not in UK South; no offline Docker bootstrap | infra/README.md:55-135 | read | high | Not retried |
| C11 | Workloads set ZF_STORE=mssql | infra/modules/containerapps.bicep:148,400 | grep | high | |
| C12 | Old internal environment (public access Disabled) is the origin; retirement needs separate approval after d | infra/README.md:707-733; Azure env state | read, az | high | |
| C13 | No model deployments in the Foundry account | Azure resource state | az cognitiveservices deployment list | high | |
| C14 | gpt-4.1 and gpt-4.1-mini 2025-04-14 listed in UK South, lifecycle Legacy, inference deprecation 2027-04-14; subscription quota Unknown (R9) | infra/README.md:970-1040; model list 2026-10-20 | read, az | high | Catalog only |
| C15 | `app_cpu_billed` 57,860 vCore-s/day on 17-19 Oct against 43,200 floor | Azure Monitor (private) | az monitor metrics | high | |
| C16 | Subscription-scope cost query and `az consumption` return RBACAccessDenied; only RG `ama` visible | Azure responses 2026-10-20 | az | high | Gating unknown |
| C17 | Addendum EXA-012: earlier USD 450 cap, 360 review, 405 pause; superseded for this scope by owner USD 500 total clarification | docs/case_study_48_addendum.md:126,210-220 | read | high | Existing synthesis to extend |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Version/date | Confidence |
|----|-----------------|--------|-----|-----------|--------------|------------|
| W1 | List prices USD: gpt-4.1 in 0.002 and out 0.008 per 1K; gpt-4.1-mini in 0.0004 and out 0.0016 per 1K; Container Apps idle vCPU 0.000004/s, memory 0.000004/GiB-s, environment private endpoint 0.125/h; Premium registry 1.6666/day; IoT B1 10/month; Log Analytics ingestion 2.88/GB | Azure Retail Prices API | https://prices.azure.com/api/retail/prices | 2026-10-20 | effective dates 2022-2026 | medium (list, not agreement price; no numeric public rate for SQL serverless/Front Door) |
| W2 | Costs are estimated until invoiced, exclude credits, and support/other costs are not included; data latency varies | Understand Cost Management data | https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data | 2026-10-20 | updated 2026-06-02 | high |

### Contradictions / Conflicts

* Draft said SQL idle saving 50 percent; fresh evidence supports a 0 to about 10.66 USD/day range depending on connections; resolved by evidence weight (C4, C5, C15): the plan uses the range.
* EXA-012 caps (450/360/405) versus owner USD 500 total: resolved by owner comment 6301554087 (constraint): USD 500 total applies for this scope; EXA-012 remains history.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
|----------|---------|--------------|------------|-------------|
| Q1 | F1: RG `ama` accrued 189.94 USD through partial 20 Oct, estimated, Usage/OnDemand, no credits visible; latency magnitude and subscription scope unknown | C1, C2, C16, W2 | high for RG, unknown for subscription | Gating unknown for execution |
| Q2 | F2: burn 30.245 USD/day; SQL 10.66, Front Door 10.64, old environment private endpoint 2.4, registry 1.67, others small; step on 17 Oct | C1, C2, C3, C4 | high | Two options dominate |
| Q3 | F3: no-change projection 535.41, headroom -35.41; Front Door removed from 21 Oct 418.3 (+81.7); SQL idling range gives up to about 105 further saving only if achieved | C1, C2, C15 | medium (projection) | Paid work blocked unless idle burn reduced and subscription charges known |
| Q4 | F4: finite token bound 4.61 USD for 300+100 calls; deployments absent; quota Unknown; models Legacy | W1, C8, C13, C14 | medium | Tokens cheap; capacity, not cost, is risk |
| Q5 | F5: demo exists but restricted; sign-in blocked by sentinel, tenant/consent/roster and private executor; capacity failures known | C9, C10 | high | Owner may test only with real evidence; redirect/403 is not sign-in |
| Q6 | F6: contrarian wave weakened SQL saving and reserve; promoted subscription scope to gate | C4, C5, C16, W2 | medium | Plan shows ranges and gating unknowns |

## Key Discoveries

* The USD 500 total is already exceeded in the no-change projection (535.41); headroom is negative before any new work.
* Inference is under 5 USD even at 400 calls; idle infrastructure is the cost risk.
* Subscription-level spend is invisible to this identity, so USD 500 compliance cannot be demonstrated here.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: the plan should present (T0) an owner-decided idle-burn reduction and subscription-charge disclosure as an approval prerequisite; (T1) a first deployment tranche with no new resources that moves the existing demo API from deny-all to genuine sign-in only when private/tenant prerequisites are met; (T2) a capped actual-model evaluation; (T3) Azure validation tied to existing scripts; (T4) sizing as analysis only. Each states ceilings, thresholds computed from projected month end, expiry do-not-start time, cleanup and recreation. All remain proposals.
* Rationale: the only options that change feasibility are cost-side (F2, F3); demo access is blocked by non-cost prerequisites (F5).
* Evidence refs: C1-C16, W1, W2.
* Implementation impact: addendum subsection, index, log only.
* Confidence: medium; raised by owner-supplied subscription charges and a measured SQL pause check.

### Alternative: run everything local only

* Approach: synthetic local demo (`ZF_AUTH=password`, sqlite).
* Trade-offs: zero Azure spend; cannot satisfy real Azure/SQL/AI acceptance (C17 via addendum CON-007 text).
* Rejection rationale: kept as stage zero of each tranche, not an Azure-evidence substitute.

### Alternative: new publisher VM or ACR pool

* Rejection rationale: known capacity failures and no UK South pools (C10); retries not authorised.

### Alternative: retire old environment as well as Front Door

* Trade-offs: further about 2.4 USD/day, but removes the existing API and rollback path.
* Rejection rationale: out of scope without separate owner disposition and identities preservation review (C12).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: subscription-scope accrued charges, credits and billing latency (C16, W2); owner choice of idle-burn option; owner approval of any plan.
* Important: SQL pause effect; model deployment quota (C14); private executor and tenant/roster prerequisites; held-out manifest and human gates.
* Follow-up: agreement prices (currency/accounting month) for owner-confirmed rates.
* Residual uncertainty: SQL/Front Door list prices unavailable publicly; 20 Oct partial; reserve unsized.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| USD 500 is TOTAL monthly cap incl. accrued; expiry 2026-10-25T16:02Z | confirmed | user | Owner comments | C17 | All gates use projected month end |
| Documentation-only; no cloud mutation | confirmed | user, constraint | Coordinator brief | n/a | Plan is for approval only |
| Draft artifacts are unverified pre-RPI inputs | confirmed | user | Coordinator intervention | n/a | Recovery artifacts distinct |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Subscription-scope charges and credits | Owner-run subscription cost query with timestamp | Owner | Headroom | blocking |
| Idle-burn disposition (Front Door, SQL idle) | Owner choice | Owner | Feasibility | blocking |
| Reserve size | Owner figure or evidence of latency | Owner | Thresholds | important |
| Approval of tranches | Completed approval fields | Owner | Any execution | blocking |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related |
|----------|---------------|----------------|---------|-----------|---------|
| H | Subscription-scope cost and latency | Verifies cap | Owner supplies access/data | deferred | Q1; C16 |
| M | Measure SQL pause after stopping schedule | Sizes saving | Owner approves idle option | deferred | Q2; C4, C5 |

## Planning Readiness

* Status: Ready (to plan options, gates and the documentation synthesis); Blocked for any paid execution.
* Decision state: convergence selection above.
* Evidence basis: C1-C17, W1, W2.
* Preconditions met: Research disposition executed; three waves complete; readiness recorded.
* Blockers: for execution only, as unresolved decisions.
* Smallest action to change execution readiness: owner supplies subscription-scope charges and approves an idle-burn option and approval fields.

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian (cycle 1) |
| Lane evidence or inline fallback | Inline; no RPI Researcher worker; no lane artifacts; limitation: single investigator |
| Research disposition | executed (recovery) |
| Planning Readiness | Ready for plan; Blocked for execution |
| Blockers | Subscription-scope charges, owner approvals |
| Continuation owner and state | Active RPI Agent parent; proceed to rpi-plan |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready (planning only) |
| Output mode and planning support | convergence; yes |
| Acting owner | confirmed automatic RPI Agent per coordinator direction |
| Required gates or confirmations | state write passed (see recovery state file) |
| Continuation result | automatic continuation to actual rpi-plan |
| Primary evidence file | .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md |
| Notes | Reuse verified figures; do not cite pre-RPI draft as executed phases |

* Advisory only: this skill did not invoke rpi-plan.
* Completion basis: remaining gaps are owner-only data.

## Sources

* W1 - Azure Retail Prices API - https://prices.azure.com/api/retail/prices (retrieved 2026-10-20, current)
* W2 - Understand Cost Management data - https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data (retrieved 2026-10-20, updated 2026-06-02)

## Artifact Self-Check

* [x] Questions answered or marked unanswerable.
* [x] Wider, Deeper, Contrarian in order.
* [x] Posture, provenance, limits, completion basis recorded.
* [x] C# with locations; W# with URL and date.
* [x] W# map to Sources.
* [x] Extension registry, participation, direction controls recorded.
* [x] Parent synthesis and re-entry recorded.
* [x] Convergence recommendation with rejected alternatives.
* [x] Decisions, unresolved decisions, next research, readiness recorded.
* [x] No secrets or IDs recorded; fetched content treated as data.
* Missing or limited sections: no delegated lane evidence (inline); some C rows cite private Azure state without path:line by nature.

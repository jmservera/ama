---
title: Azure total cost and protected AI budgets for the capstone pitch
ms.date: 2026-11-27
---

| Field | Value |
| --- | --- |
| Primary evidence file | .copilot-tracking/research/2026-11-27/azure-total-cost-pitch-research.md |
| Date source | User-supplied current date, 2026-11-27 |
| Research root | Repository .copilot-tracking/research/2026-11-27 |
| Posture | Focused: bounded continuation of the presentation cost story |
| Output mode | Analysis preparing presentation authoring, not runtime implementation |
| Participation | Agent-owned under active autopilot; illustrative assumptions do not approve spending |

## Executive Summary

Research is complete for a qualified presentation update. The identified
persistent-service subtotal is USD 334.838 per 30-day month. A whole-platform
planning scenario must add app and job compute, storage, logs, security,
monitoring, operations and model usage. The illustrative envelope described
below is about USD 435-1,260 per month, not an observed bill or a maximum invoice.

AI model charges can be zero when no model is called. An illustrative USD 50
monthly policy can allocate USD 20 to recommendations, USD 10 to document
judging and USD 20 to chat. Existing monetary admission mechanisms support
finite budgets, but this update does not configure or prove those allocations.

## What You May Not Know

Scale-to-zero for application replicas does not establish zero charges for
storage, databases, registry, networking or monitoring. Source configuration
and any current management-plane observation will be distinguished.

The current source supports money limits as well as call/token allowances.
Azure budget alerts are not the enforcing mechanism. Deterministic gap checks
use no model tokens; semantic interpretation is a different, potentially paid
step, and neither substitutes for professional acceptance.

## Findings

### Zero app replicas still leave a persistent platform bill

The current management reads show all three apps on Consumption with minimum
zero, but SQL is provisioned S3, not the parameter template's serverless
database. Premium registry, IoT B1, Event Hubs Standard, nine private endpoints
and fourteen private DNS zones persist. Their public-rate subtotal for a
30-day/720-hour scenario is USD 334.838 before storage, logs, alerts, security,
jobs, app compute or AI. This is an estimate, not a retrieved invoice.

Evidence state: evidence-backed finding for the scoped management observation
and list-rate arithmetic; capacity/volume assumptions remain illustrative.
C1: infra/modules/sql.bicep, sku and serverless settings.
C2: 27 November read-only management observation (SQL S3, app bounds and service counts).
W1: Azure Retail Prices API, UK South SQL S3, registry, IoT and Event Hubs; global Private Link and private DNS meters, retrieved 27 November.

### Quiet websites do not stop scheduled work

The current apps use a one-hour cooldown. Separate jobs run every five minutes,
every thirty minutes and nightly; the simulator is scheduled eight times an
hour. Empty replicas incur no app resource charge, but running jobs are billed
at the active rate. Log retention is 90 days with no daily ingestion quota.
No finite maximum Azure invoice follows from these settings.

Evidence state: evidence-backed finding for configuration, not measured
replica history or billed runtime.
C3: read-only app/job/Log Analytics configuration observation, 27 November.
W2: https://learn.microsoft.com/en-us/azure/container-apps/billing, retrieved 27 November.

### Priority allocations are a policy, not a current guarantee

The source supports capability-scoped authorities and multiple finite call,
token and money budgets. Admission reserves worst-case liability before the
provider call and accounts for completed plus outstanding reservations.
Unknown liability, expired authority and shared-budget conflicts can hold
dispatch. A chat-exhaustion isolation policy must use disjoint class allowances
inside an aggregate ceiling; it must not bypass those holds.

Evidence state: evidence-backed source finding; priority allocation and live
acceptance are proposed, not deployed by this presentation work.
C4: src/core/src/zava_forward/core/ai_consumption.py, authorize and reserve_in.
W3: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets, retrieved 27 November: budgets notify, not stop consumption.

### Theoretical model bounds depend on the deployed SKU

The observed deployments include GPT-4.1-nano GlobalStandard and GPT-4.1-mini
regional Standard. Public API prices retrieved on 27 November are USD
0.10/0.40 per million input/output tokens for nano, and USD 0.484/1.936 for
regional mini. A one-call envelope of 4,000 total provider-input tokens and
1,000 output tokens costs at most USD 0.0008 or USD 0.003872 respectively,
without a cache discount. These are bounded-call estimates, not measurements,
quality guarantees or permission to use either model.

The minimum monthly model charge is zero. With enforced daily/monthly
allocations of 1/20, 0.50/10 and 1/20 USD respectively, the theoretical aggregate
is at most USD 2.50 per day and USD 50 per 30-day month. A known exhausted chat
allocation cannot consume the other two. The absolute aggregate authority and
unknown-liability holds remain; external/bypassing model traffic is outside
this policy.

Evidence state: public-rate finding plus explicitly proposed policy.
C5: 27 November read-only deployment identity/SKU observation.
C6: src/core/src/zava_forward/core/assistants.py, deterministic evidence predicates and separate generated finding.
W4: https://prices.azure.com/api/retail/prices, service Foundry Models, UK South, exact meters below.

### Full-cost scenarios need explicit allowances and exclusions

The two planning columns assume a 30-day/720-hour month, no negotiated rates,
no currency conversion and no shared free allowances. The low-demand example
has one replica of each app for 198 hours (176 working hours plus 22 one-hour
cooldowns); the high-load example has all configured maximum replicas for
720 hours. Neither is actual replica history.

| Component | Low USD | High USD | Assumption |
| --- | ---: | ---: | --- |
| Identified persistent infrastructure | 334.838 | 334.838 | S3, Premium registry, IoT B1, Event Hubs, nine endpoints, fourteen zones |
| Active app compute | 37.422 | 517.104 | 1.25 vCPU/2.5 GiB for 198 h; 4.75 vCPU/9.5 GiB for 720 h |
| Job compute | 0.756 | 151.200 | 20/4,000 equivalent 0.25-vCPU/0.5-GiB replica-hours; illustration, not an execution cap |
| Hot LRS Blob capacity | 0.192 | 1.920 | 10/100 GB-month |
| Analytics log ingestion | 2.880 | 57.600 | 1/20 GB-month gross, without shared free allowance |
| Billable retention | 0.260 | 5.200 | 2/40 GB-month; steady-state allowance for retained data, not all 90 days charged again |
| Monitoring allowance | 6 | 20 | Alert/resource/series charges; not a measured invoice |
| Security allowance | 50 | 100 | Planning provision; protected quantity, legacy versus DWU billing and trial status require reconciliation |
| Other operations and transfer allowance | 2 | 20 | Blob/Queue/Key Vault transactions, DNS, network, Event Hubs events and registry tasks |
| AI model charges | 0 | 50 | Illustrative aggregate monetary policy, not current configured authority |
| Total | 434.348 | 1257.862 | Conditional planning totals, displayed as about USD 435-1,260 |

Five temporary S0 QA databases would add USD 90.75 if retained for all 30 days,
before their other charges. They are outside the core-service scenario.
Optional future Fabric, production redundancy, larger capacity, exceptional
transfer, unmodelled resource additions, tax and human work are not included.
Actual billing reconciliation and accepted-outcome cost remain open.

The Defender catalog includes a new SQL DWU meter, but official documentation
calls that billing model preview and says subscriptions move to it. Its
existence does not establish this subscription's migration or protected DWU
quantity. Do not silently multiply it into an actual security bill; retain a
visible planning allowance until the applicable billing is reconciled.

Evidence state: arithmetic from accepted rates plus labelled assumptions;
security/monitoring/operation figures are allowances, not accepted actual costs.
W5: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-portal/estimate-track-costs, retrieved 27 November.
W6: https://azure.microsoft.com/en-us/pricing/details/dns/, retrieved 27 November:
the first 25 hosted zones are priced per zone-month, prorated for partial
months. The selected private DNS API meter is "Zone 1", not UK South.

## Recommendation and Alternatives

Present the identified persistent subtotal beside a full low/high planning
envelope, then show isolated priority allocations. Keep the existing measured
12-proposal/2,522-token batch as usage evidence, not a billing record.

Reject a zero-total-cost claim: it ignores persistent services and jobs.
Reject a single chat-shared allowance: it can starve business tasks.
Reject treating Azure notifications as hard caps: their data and evaluation
are delayed. Defer changing SQL, schedules, security or monitoring until a
separate operational decision; savings must not disable audit or safety work.

## Scope and Questions

Audience: the capstone executive panel. Continue PR #2474 and preserve the
demo-first route, native architecture and original protected financial records.

* Q1: Which Azure services and billing meters remain when application replicas are zero?
* Q2: What bounded monthly low/high scenario can be computed from explicit capacity and workload assumptions?
* Q3: What theoretical AI minimum/maximum follows from model rates, call counts and context/output limits?
* Q4: Which spending controls exist, and which policy would prevent chat from consuming recommendation and document-check allocations?

No deployment, paid model calls, billing-account export, real resident data,
application-control implementation, grant/FX assumptions or production
acceptance is authorised by this presentation update.

## Decisions and Feedback

| Decision | State | Basis |
| --- | --- | --- |
| D1: Reuse presentation topic/PR | Confirmed | PR #2474 remains open on the coherent presentation branch |
| D2: Use public list-price planning scenarios | Selected for research | The user asks for theoretical ranges; actual invoices and negotiated rates are not supplied |
| D3: Protect recommendations and document judging from chat exhaustion | Confirmed direction | Current user request; monetary mechanisms exist in source, live isolation is unproved |
| D4: Use USD 50 monthly / USD 2.50 daily illustrative policy | Agent-selected example | Disjoint class allocations total the absolute ceilings; not spending authority |
| D5: Use explicit security/monitoring/operations allowances | Selected with qualification | Actual protected quantity, invoice and consumption volumes unavailable; avoid invented actual charges |

## Risks and Open Questions

Region, deployed SKUs, workload envelope, free-allowance sharing and ingestion/
egress assumptions are established or labelled. A finite upper scenario
is not a contractual maximum bill. Safety, unknown-liability holds and total
authority limits must still stop model dispatch where necessary.

No protected-quantity/security billing reconciliation, invoice, production
forecast, live priority-policy configuration or accepted-outcome denominator
was supplied. None is required to label and explain the planning example;
all remain required before claiming actual cost or operational acceptance.

## Planning Readiness and Next Step

Research disposition: completed for the conditional presentation scope.
Planning readiness: Ready with explicit financial/operational limitations.
No user walkthrough is required for the agent-owned illustrative choices.
The parent continues automatically with source-owned cost data, existing
unprotected cost/budget slides, integrated notes and focused generation checks.
No deployment or spend-control implementation follows from this research.

## Research Record

### Method and Boundaries

Starting internal areas: infra modules/parameters, architecture guides,
Tokenomics evidence, admission/budget code and selected cost-slide sources.
Starting external areas: official Azure pricing/billing/scale documentation
and public model pricing. Read-only management-plane SKU and scale reads are
permitted; identifiers and secrets will not enter the public deck.

Prior knowledge: the earlier demo-first review establishes the measured token
batch and unknown attributable cost, but does not supply full Azure pricing.
This task uses a separate cost research record, rather than rewriting that
historical review. Evidence IDs are local to this record.

### Extension Registry

* Repository guidance: selected for source boundaries, native generation, privacy, evidence retention and focused validation.
* hve-slides: selected for scoped source-backed presentation authoring; retain the incumbent native deck.
* rpi-research: selected for this read-only evidence phase; no peer phase during research.
* ama-author-voice: retained for later prose, not a grant of research or publication authority.
* Web-design skills: skipped; no website implementation or standalone UI review.

### Research Cycle Log

Cycle 1 wider wave: inventory covers apps, SQL, registry, storage, private
network, monitoring, IoT/Event Hubs, scheduled jobs, model deployments and
temporary QA databases. Source templates differ from the serving database.

Cycle 1 deeper wave: exact UK South/global rate meters and financial-admission
contracts read directly. The retail catalog now calls OpenAI's service
Foundry Models; obsolete service-name filters returned no records.

Cycle 1 contrarian wave completed: persistent costs, cooldown, scheduled
overnight work, unconstrained ingestion, shared unknown-liability holds and
production/optional-service costs challenge a zero-bill or unconditional
priority guarantee. New Defender DWU pricing is conditional on migration,
not proof of the existing bill. The regional mini tariff differs from the
global tariff. No helper was dispatched.

Synthesis accepts exact public-rate facts and source/configuration distinctions;
it labels workload and budget choices as illustrative and actual billing as
unresolved. No additional cycle is required to author those qualified claims.
Re-enter for billing reconciliation, changed tariffs/SKUs, production capacity
or implementation of policy isolation.

The read-only Azure CLI scheduled-query command auto-installed its missing
preview extension through the CLI's existing dynamic-install behaviour.
No Azure resource, security, budget, scale or deployment write was performed;
the shared CLI configuration was not altered.

### Accepted rate evidence

All rates below were retrieved from https://prices.azure.com/api/retail/prices
on 2026-11-27 using Consumption filters and UK South unless Global is stated.
The API's selected filtered responses had no next page. No subscription
identifier, secret or raw private resource inventory is retained.

| Meter | Unit | USD | Meter ID |
| --- | --- | ---: | --- |
| Container Apps active CPU | vCPU-second | 0.000034 | 2c27faec-4865-58a4-9bca-4c64327315d3 |
| Container Apps active memory | GiB-second | 0.000004 | edbe3fc7-4303-5495-a104-88c166efe547 |
| Container Apps requests | million | 0.40 | edca2d58-b847-565c-828a-df27aa4bae75 |
| SQL S3 | day | 6.048 | 23581df3-94d7-4621-8507-b1c7cb4b6d27 |
| SQL S0 | day | 0.605 | 30cf8266-ff5a-4f43-aa52-fa4d080ee691 |
| Premium registry | day | 1.6666 | 2f8e1105-47d0-4105-a934-b2175c766a71 |
| IoT Hub B1 | month | 10 | b639605e-822b-4c37-aced-7505f2272819 |
| Event Hubs Standard unit | hour | 0.03 | 62d94a65-9300-48a6-8c15-0e70fc41eb44 |
| Private endpoint (Global) | hour | 0.01 | e6ab7238-e433-4fe0-a2b2-2b2564df2cdb |
| Private DNS first 25 zones | zone-month | 0.50 | 0b608a26-f611-4232-8192-ce81b6b57194 |
| Hot LRS Blob storage | GB-month | 0.0192 | 758b46f1-1579-4490-a54a-9829ff267c51 |
| Analytics Logs ingestion | GB | 2.88 | d664ef7a-c553-4b1c-a2ae-1a44ea5ed8ce |
| Log retention | GB-month | 0.13 | b1ea455c-26fc-40a1-b16b-86ad898f4fc5 |
| Metric monitored | series-month | 0.10 | 6860c782-bbcc-41ed-a218-fb308dd0942e |
| System log monitored, 15 min | rule-month | 0.50 | cf20b9c8-d39b-40df-8a95-35f38bbd6ed2 |
| Key Vault operations (Global) | 10,000 | 0.03 | 0f824807-2376-435c-95c9-f992b67a07b0 |
| Nano global input | 1,000 tokens | 0.0001 | 5a96380c-2dbe-5b68-b0da-e71db0e00147 |
| Nano global output | 1,000 tokens | 0.0004 | 0af08775-3bab-5db5-ac98-5ddb9fbd3c30 |
| Mini regional input | 1,000 tokens | 0.000484 | a9c78fe9-7568-5bbc-b7bc-51f8977c79d7 |
| Mini regional output | 1,000 tokens | 0.001936 | 84d4645a-720e-5eb0-a3e9-e4e811a2a45b |

The SQL DWU meter e6c4c1d8-3188-5fca-b39a-b6f2eaa8ecb3 at USD 0.006849
per DWU-hour is candidate evidence only, not applied to this deployment.
Marketing price cells returned "$-"; numerical rates come from the API.
An obsolete Defender FAQ URL returned 404; the current official pricing and
billing-model pages supplied the material caveat.

### Artifact self-check

All four questions are answered for presentation purposes or have a named
evidence gap. Wider, deeper and contrarian waves completed in order. The
record distinguishes observed configuration, source mechanisms, public rates,
illustrative scenarios and unproved actuals/acceptance. The proposed policy
preserves professional judgement and global safety holds.

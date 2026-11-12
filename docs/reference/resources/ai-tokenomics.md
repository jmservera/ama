---
title: AI Tokenomics (Total Cost of AI and Value Realised)
description: What the mentor clue on Tokenomics points to, the public Tokenomics Foundation framing, how it maps to the capstone rubric and the Zava Forward evidence, and what remains unmeasured
ms.date: 2026-11-10
ms.topic: reference
---

## Purpose

On 2026-10-22 a mentor mentioned Tokenomics during the mentor progress review.
The owner reported this as a clue about what the capstone panel will probe. The
mentor's exact words are not in the repository, so the link between the remark
and the sources below is an owner-reported inference, not a recorded finding.
Ask the mentor to confirm what they meant before the final deck is frozen.

This page records the retrieved external framing, maps it to the
[Capstone Assessment Guide](../method/ama-capstone-assessment-guide.md) and to
what Zava Forward can already show, and names the gaps. It is a resource
pointer with retrieved findings, not regulatory evidence, a company fact or a
validated benefit.

## Access and Retrieval

| Item | Detail |
| --- | --- |
| Public source | [Tokenomics Foundation](https://www.tokeneconomics.com/), pages on the definition, Total Cost of AI and projects; retrieved 2026-10-22 |
| Source status | Draft working-group output. The definition is labelled draft v0.5.2, dated 2026-09-01. The Foundation runs alongside the FinOps Foundation. Treat every item as an emerging practice, not an accepted standard |
| Internal pointer | A Microsoft internal slide deck, "FinOps for AI & Tokenomics on Microsoft" (Ali Mazaheri and Patrick Vangoedsenhoven, modified 2026-10-22), found through WorkIQ. Internal Microsoft material: paraphrase, do not quote or show it to a customer or panel |
| Not confirmed | That this deck, or any named speaker, is the source of the mentor's remark. A WorkIQ check found no evidence that the deck itself was presented on 2026-10-22, only a same-day team meeting that discussed AI spend, model selection and prompt return on investment |
| Foundation events | The site lists a Tokenomics event on 22 to 23 October 2026; the relationship to the mentor's remark is unknown |

## What Tokenomics Says (Public Framing)

Evidence class: community and practitioner framing, draft.

| Idea | Statement | Source |
| --- | --- | --- |
| Definition | AI Tokenomics is the discipline of converting energy and capital into AI capabilities and consuming that intelligence efficiently across the organisation to realise measurable business value | Definition page, draft v0.5.2 |
| Three questions | Production (energy and capital into capability), Consumption (using it well: model selection, routing, caching, forecasting, licences) and Value (what the output is worth: pricing, labour, revenue, business processes) | Home and definition pages |
| Total Cost of AI (TCA) | Tokens are not the AI bill. TCA adds energy, capital, platform, software, licensing, labour and process change. The Foundation's host claims token and API cost is 10 to 25 percent of total AI spend and cites one enterprise audit at about 25 percent | Episode 17, 2026-09-07. An assertion from one podcast and one audit, not a benchmark |
| Unit economics | TCA divided by realised, finance-defensible value delivered above a quality floor | Episode 17 |
| Value destinations | A booked value claim needs one of five destinations: new revenue won, revenue retained, spend removed, spend avoided or capital freed | Episode 17 |
| Labour claims | Split into capacity gain, augmentation and automation, each with its own baseline | Episode 17 |
| Big-T notation | Big-O for AI consumption: T(1) cache or precompute, T(log n) filter before inference, T(n) one call per request, T(n.k) k hidden calls per request, T(n.k.a) agent depth multiplies calls, T(infinity) loops with no termination. Remedies: cache, filter, trim, bound depth, add budgets, hard termination | Projects page, release due December 2026 |
| Seven-layer stack | What AI costs is decided in the lower layers; how much is spent is decided in the upper ones | Projects page |
| Gateway and routing | A gateway holds policy, observability and failover; routing is one decision inside it | Episode 17 |

The internal Microsoft deck, paraphrased, adds three practical points. First,
choose the denominator deliberately: cost per token suits infrastructure, cost
per agent run suits workflows and cost per business outcome is the finance
metric. Second, time saved is not value until it is booked somewhere. Third,
change one lever (routing, caching, context), measure again and keep or revert,
so that cost per acceptable outcome improves, not only the average token price.
Also treat gateway token limits as operational guardrails and billing records as
the financial source of truth.

## Why It Matters for the Capstone

The rubric already asks for this, in different words.

| Criterion | Descriptor that Tokenomics answers | Current position |
| --- | --- | --- |
| A5 Operations | "cost modelled per unit of business value" for the top band; "cost or performance evidenced, but not both" below it | [ADR 0001](../../adrs/0001-azure-architecture.md) states cost per unit of business value "cannot be stated until a deployment produces measured usage" and calls this an explicit gap. This is the clearest named gap |
| A6 AI solution design | Model choice justified against alternatives "on cost, latency and quality" | Offline evaluation harness and a smallest-model rule exist (#108). Cost per accepted proposal is not reported |
| B7 Evidence | "Bring numbers. Cost per transaction, latency, evaluation scores, the value at stake. Assertions without evidence cap you at a 3" | Token counts exist for one operator exercise; no cost-per-transaction figure exists |
| C1 Business framing | Quantify the value at stake and the cost of inaction | [BRD](../../brds/agentic-retrofit-programme-brd.md) value claims remain hypotheses; AI running cost is not in the investment case |
| C3 Intellectual honesty | Surface risk unprompted; say "I don't know" credibly | Stating the gap before the panel asks is the scored behaviour |

## What Zava Forward Can Already Show

Evidence class: repository observation, not a benchmark.

This inventory is pre-extension evidence. The dated 2026-10-31 source-only
section below supersedes its code-path descriptions, not operational acceptance.

* The five-assistant path validates prompt, completion and total tokens and keeps
  them with the append-only ledger event when the provider supplies them
  ([assistants](../../../src/core/src/zava_forward/core/assistants.py)). This is
  partial coverage: the legacy `Ai.run()` and `look_at()` paths already return
  validated usage with the meter id and root through the request receipt, and
  the text-draft path joins its output and review to the ledger (2026-11-12
  source reading of [core `ai.py`](../../../src/core/src/zava_forward/core/ai.py));
  only the resident chat host's direct `_chat` call keeps no receipt. Usage can
  remain unknown for an assistant or legacy call, in which case the reservation
  is retained. This is source and synthetic-spy evidence only, not a cost.
  Complete per-call metering is what NFR-012 proposes.
* Operator-authorised exercises carry finite call and token allowances and an
  expiry per authority reference, and proactive generation is off by default
  ([ADR 0002](../../adrs/0002-pilot-readiness-architecture.md),
  [agents README](../../../src/agents/README.md)). The README states that token
  allowances are not a currency guarantee and that the operator derives limits
  from deployment pricing. Independent task and period budgets, and per-request
  call and agent-depth bounds, are proposals (NFR-012, AC-100, AC-109), not
  current controls. The assistant design does avoid open-ended agent loops.
* One renewed QA exercise ran five assistant tasks on Azure OpenAI
  `gpt-4.1-mini-2025-04-14` using 6,884 tokens in five attempts, an arithmetic
  mean of about 1,377 tokens per proposal. This is a five-sample operational
  check with no human acceptance, so it is not a throughput, quality or cost
  estimate.
* ADR 0001 names the Azure cost drivers and a monthly budget alert at 80 percent
  actual and 100 percent forecast, and records the Foundry tokens-per-minute
  throttle that degrades a task to workflow-only.
* The BRD already treats time saved as capacity and not cash unless a budget
  owner confirms spend will fall (RULE-016, RULE-019), which matches the
  Tokenomics "booked value" test.

## Rubric Scorer Model Pilot (2026-10-24)

Evidence class: one local, owner-authorised screening run per model, not an
application inference benchmark or a production-model selection decision.
The owner approved a USD 10 pilot. All three requested model identities were
confirmed by their CLI usage records; no fallback or paid retry was used.

The same baseline-hidden prompt and registered artifact snapshot came from
commit `4ed85ba06c3a820591cf86e5d75da8c8db401a8b`. The bundle contained one
capstone deck, 12 pitch files and registered supporting evidence. The source
and prompt hashes were verified after execution. Copilot CLI 1.0.103 exposed
read tools only, with no scoring-output tool, shell, writes, network tools or
delegation. This differs from the hosted scorer's pinned CLI 1.0.87 and MCP
submission transport. Model-chosen reads differed despite identical inputs.

| Requested and reported model | Wall time | Inference calls | Reported AI credits | USD equivalent | Result |
| --- | --- | --- | --- | --- | --- |
| `claude-sonnet-5` | 121.75 seconds | 15 | 24.018900 | 0.24018900 | Valid raw JSON and adapter card; calibration 61/100 |
| `claude-haiku-4.5` | 113.76 seconds | 9 | 11.417745 | 0.11417745 | Prose/fenced response; required summary omitted; adapter rejected it |
| `gpt-6-luna` | 155.89 seconds | 13 | 3.194431 | 0.03194431 | Valid raw JSON and adapter card; calibration 59/100 |

Usage records reported complete accounting. Each credit value is the CLI's
`totalNanoAiu` divided by 1,000,000,000, not its legacy
`totalPremiumRequestCost`. USD equivalents use GitHub's published
[one AI credit = USD 0.01](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing),
checked 2026-10-24. Total equivalent usage was USD 0.38631076, excluding
subscription allocation, labour and other infrastructure. These are reported
usage estimates, not a reconciled invoice or Total Cost of AI.

The unchanged local gate forced D1-D3 to zero because thought leadership was
absent; both valid cards remain Incomplete, not capstone acceptance. Luna
matched Sonnet on 16/20 final grades, including the three forced zeros, or
13/17 remaining criteria. Differences were A4 4/3, A7 4/3, B1 3/4 and C2 3/2
(Sonnet/Luna). A passing constructed baseline replay does not establish a
hosted PR pass or identical scores. Haiku was not repaired or assigned an
accepted total. A hosted required-summary rejection could permit correction;
this final-response pilot did not test that native retry behavior.

Keep Sonnet pinned: Luna was about 87 percent cheaper but 28 percent slower
in this sample and did not reproduce the grades. Haiku was about 52 percent
cheaper and 7 percent faster, but the card was incomplete. One sample cannot
estimate model variance, stable latency or equivalence; nor does Sonnet's
score establish ground truth. Next comparisons need repeated, held-out and
threshold-adjacent examples, independent evidence adjudication and the native
submission path. No score, workflow, baseline, application model or live
status was changed. This pilot does not close the application gaps below.

### Native MCP Follow-Up (2026-10-24)

The owner approved one additional invocation each for Haiku 4.5 and GPT-6
Luna within the original USD 10 total. Both used the original frozen evidence,
the same native prompt and the real, unmodified safe-output runtime pinned at
`github/gh-aw-actions@924af5fdc64061cfbf66fb584c8b07e2ac230c60`. Runtime blob
hashes, generated schema and local stdio/HTTP rejection/append regressions were
verified; seven checks passed. Model integration used local stdio MCP with CLI
1.0.103, not the full hosted workflow or its firewall/permission environment.

| Requested and reported model | Wall time | Inference calls | USD equivalent | Native result |
| --- | --- | --- | --- | --- |
| `claude-haiku-4.5` | 111.07 seconds | 10 | 0.10206125 | One tool call, one append, strict gate valid; calibration 64/100 |
| `gpt-6-luna` | 107.97 seconds | 11 | 0.01870419 | One tool call, one append, strict gate valid; calibration 56/100 |

Neither invocation needed a rejected-call correction. Each included the
required summary and complete details. The original Haiku final-response
failure remains an observed failure, not a repaired or replaced result.
Native Haiku's A5 rationale was 303 characters, violating the prompt's
under-300 instruction even though that limit is not enforced by the strict
adapter/gate. Tool acceptance therefore does not establish full instruction
conformance. Luna met the rationale-length check.

The native cards differ on nine of 20 criteria: A3, B1-B6, C1 and C2, including
a two-point B5 difference. Their three forced D zeros remain identical, and
both outcomes remain Incomplete. No new Sonnet native run was approved, so
earlier Sonnet timing and grades are not a same-prompt native control.

Follow-up reported equivalent usage was USD 0.12076544; aggregate usage across
all five invocations was USD 0.50707620, with complete accounting and requested
model identities confirmed. Only read tools and the local record tool were
used. The MCP child environment contained no GitHub credentials; only local
append files were written. No publisher jobs, live score/status updates,
production-model switch, commit or push occurred. Later owner changes to the
live deck/registry are outside this frozen comparison.

Cheaper models can submit structurally valid cards through this pinned MCP
surface, but equivalent grading and stable speed are still unproven. Keep
Sonnet pinned pending repeated native-path comparisons, an independent
criterion-level reference assessment and threshold-adjacent decision checks.
Do not select the highest-scoring model as the most accurate one.

## Source-only Metering Extension (2026-10-31, Refs #432)

Evidence class: local engineering, not a measured financial result.
The [core consumption ledger](../../../src/core/README.md#ai-consumption-ledger-432)
extends immutable assistant events with content-free call/configuration/prompt/
cached-token attribution, intersecting task/period budgets, root call/depth bounds,
owned alerts, output/review links and billing-led reporting. The
[manager JSON report](../../../src/api/README.md#ai-consumption-report-432)
keeps cost Unknown without applicable evidence and reports quality and capacity
separately. Current report components/floors are supplied, unverified observations;
engineering defaults do not approve OD-51.

The 31 October PR #602 review corrections preserve enclosing document request
call/depth bounds and validate reporting periods even without SQL. Missing
financial output links no longer prevent legacy/priority rejection; opaque
original-root associations retain visible incomplete joins. Assistant failed-
provider rejection creates an ineligible link atomically. Meter-capacity-held
withdrawal remains explicitly financially unresolved and excludes stale
accepted economics after read recovery. These are source-only controls, not
Finance reconciliation, human acceptance, or expanded issue coverage.
The subsequent three-thread correction preserves bounded returned-model
mismatch evidence through worker shaping to non-retryable quarantine and
release suspension. Valid backend-held reports retain evaluation/live/registry
with unavailable/Unknown consumption instead of HTTP 400. An admitted call's
9,999-to-10,001 event transition returns persistent manual draft/priority/chat
fallbacks with unresolved attribution, keeping subsequent dispatch held and
recovered economics incomplete. These remain synthetic source-contract results.
Later hosted review corrections retain revoked releases as terminal and persist
capacity-held assistant completion before task/event serialization, so financial
linkage cannot roll back mismatch quarantine or its safety evidence.

This corrects the older inventory above prospectively: merged #480/#593 already
provide independent resident currency reservations. They are not joined into the
new financial cohort; complete per-call and accepted-outcome coverage remains
unmet. No deployment or stored procedure change is made by this extension.

The [dated official pricing-source retrieval](./azure-ai-price-source-2026-10-31.json)
records the public URL, content hash and unavailable numerical price cells.
The official page distinguishes token deployment types and states that public
prices are estimates, not actual quotes. No applicable region/model/currency
rates or billing record are supplied, so **cost remains Unknown**.

Local constructed ledger and loopback HTTP tests establish engineering
behaviour, not paid inference, human-witnessed acceptance or Azure reconciliation.
The issue's nine criteria retain this boundary:

| Criterion | Source-only position | Remaining evidence |
| --- | --- | --- |
| Per-call attribution | Core calls retain consumption joins and cached usage | Historical/resident joins and complete real provider usage |
| Request calls/depth | Atomic root bounds and looping/fan-out stop are engineered; a constructed test shows hazard recording and its UTC awareness time continue after the stop and that hazard, workflow and task-queue code imports no model module | Live governed activation/acceptance; statutory-clock behaviour under a live stop is not observed |
| Limits/alerts | Token/money/expiry/unknown-price/liability deny with owner reference | Named owner and approved budgets |
| Dated price | Official source metadata/version stored; unavailable rates explicit | Applicable approved rate source |
| Azure billing reconciliation | Exact-period, scope, allocation and tolerance mechanism | Actual attributable Azure cost records and Finance validation |
| Accepted cost/quality/TCA | Billing-led denominator and quality regression failure mechanism | OD-51, real quality/effort and complete approved TCA inventory |
| Released time | Capacity-not-cash classification | Measured effort; Finance booked destination if cash is claimed |
| Held-out batch/spread | Recorded token min/max/mean mechanism | Finite owner-authorised held-out batch and accepted results |
| Pitch | Drafting insert below carries the engineering result and gaps | Current source-manifest placement, regenerated notes/question bank, deck/rehearsal and final challenge |

### Pitch Drafting Insert (2026-10-31)

After merged #558, the old brief is historical. Feed this proposal through the
[current source guide](../../capstone/source/README.md#ai-consumption-evidence-432),
not by editing generated question-bank or speaker-script files. The delivered
deck and generated notes are unchanged by this task. Fixture prices must not
appear as financial evidence.

| Use | Draft copy | Evidence label |
| --- | --- | --- |
| Tokenomics slide | Source-only core calls have durable call/depth and token/money admission. Unknown price or liability stops that AI dispatch and retains the manual path. Human acceptance can be withdrawn; interrupted review joins keep the ratio Unknown. | Local engineered mechanism, not live financial acceptance |
| CFO Q&A card | Billing, not a token projection, is the financial source. Cost per human-accepted proposal is assessed beside critical misses, unsupported claims, overrides and reopened cases. No attributable bill, approved floor or authorised held-out batch is supplied, so no cost or cash benefit is claimed. | Mechanism and stated gap; no invoice, measured value or owner approval |
| Price/source note | Official public source retrieved 2026-10-31; numerical rates were unavailable. No applicable rate or estimate is substituted. | Dated retrieval metadata, not quote or invoice |

The earlier 6,884 tokens/five runs remain historical observation without a
human-accepted denominator. Complete resident/historical joins, OD-51, named
owners and Finance validation remain open. Capacity is not cash. Actual slide
placement, rebuilt notes/deck and rehearsed Q&A remain owner-controlled work.

## Configured Demo Model, Limits and Evidence Gaps (2026-11-07, Refs #108)

Evidence class: configuration metadata for one existing demonstration
deployment, read-only. It is not an evaluation, an actual-serving attestation,
a quality or fairness result, a benefit, a price or a budget. It does not tick
or complete any #108 criterion.

### Observed configuration

| Field | Observed value | What it does not show |
| --- | --- | --- |
| Account | `aif-cutover-test-rzsrg`, resource group `ama`, kind `AIServices`, SKU `S0`, resource location `uksouth` | Where prompts are processed. Resource location is not a processing location for a `Global` deployment type |
| Deployment | `standard`, deployment type `GlobalStandard`, `currentCapacity` 10, `deploymentState` Running, `provisioningState` Succeeded | That any call has succeeded or that capacity is reserved |
| Configured model | `gpt-4.1-nano`, version `2025-04-14`, format `OpenAI`, `versionUpgradeOption` `NoAutoUpgrade`, RAI policy `Microsoft.DefaultV2` | The model that answered any request. Metadata is not a response |
| Rate limits | `request` 10 per 60 s, `token` 10,000 per 60 s (capacity 10; capacity 1 gave 1 request and 1,000 tokens per 60 s) | A guaranteed rate, latency, budget, cost or human benefit. `GlobalStandard` is pay-per-token best-effort, so capacity sets a ceiling, not reserved throughput |
| Subscription availability (pre-change snapshot) | `availableCapacity` 4,999 for `gpt-4.1-nano` `GlobalStandard` in `uksouth`; account and location usage lists were empty | A subscription quota total or limit. The empty usage lists are an unexplained absence, not zero use |
| Model lifecycle (account metadata) | `Legacy`; inference retirement 2027-04-14 (same as the 2026-10-28 note in [infra README](../../../infra/README.md#small-employee-model-prerequisite-2026-10-28-refs-514)) | That the version is available for any new deployment after that date |

The capacity change from 1 to 10 was a separate owner-authorised action
([issue #891 comment](https://github.com/jmservera/ama/issues/891#issuecomment-6705173727),
2026-11-07T09:40:56Z). This synthesis only records its observable result. No
Azure mutation, quota purchase, inference, participant exercise, provider,
task, activation or budget change was part of this delta.

### Semantics that limit what the metadata can prove

* `GlobalStandard` may process prompts and responses in any Azure region; data
  at rest stays in the designated geography. `uksouth` is the resource
  location only. Serving-in-region or UK data residency is therefore not
  evidenced ([Foundry deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types),
  page dated 2026-08-06, retrieved 2026-11-07).
* `NoAutoUpgrade` means the configured deployment never upgrades
  automatically and stops working at retirement
  ([working with models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/working-with-models),
  retrieved 2026-11-07). It makes the configured version stable; it is not an
  attestation of the version that served a call. The provider response
  `model` recorded by the application on a real call can inform version
  confirmation.
* A response model identifier does not by itself attest the physical
  processing region or data residency. Actual serving evidence needs
  source-qualified provider or operational attestation and the relevant named
  approvals; no such attestation is recorded here.
* Quota is assigned per subscription, region, model and deployment type in
  tokens per minute, and the assigned capacity maps to the enforced token and
  request limits; the request-to-token ratio varies by model
  ([quota](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/quota),
  page dated 2026-05-04, retrieved 2026-11-07).

### Sources, commands and results

| Item | Detail |
| --- | --- |
| Repository base | `origin/main` `0f420dc9514db22081cb48fa733267d9d33a0d24`, tree `3c23211ac77b4876d8a5928ce228760eabcdc257`. The live resource has no source commit; its state is a dated readback, and the repository's intended default (`infra/main.bicep`, capacity 1, [infra README](../../../infra/README.md#small-employee-model-prerequisite-2026-10-28-refs-514)) differs from the live capacity 10, so Bicep is not the record of live state |
| Native evidence (private, not committed) | `/mnt/ama-gates/live-891-capacity-1107`. SHA-256 prefixes: `before-deployment.json` 3065cd42, `after-deployment.json` fdf9b30b, `model-skus.json` bdeab081, `model-capacities.json` db79e11c, `account.json` 5206b732 |
| Fresh read-only readback | 2026-11-07 by the Azure CLI signed-in account, this resource only |
| Not re-read | Live app environment (`AI_MODEL_VERSION`), any provider response, SQL, keys and tokens |

```text
az cognitiveservices account deployment show -g ama -n aif-cutover-test-rzsrg --deployment-name standard --query "{sku:sku,model:properties.model.name,version:properties.model.version,upgrade:properties.versionUpgradeOption,state:properties.provisioningState,rate:properties.rateLimits[].{k:key,c:count,p:renewalPeriod},rai:properties.raiPolicyName,cap:properties.currentCapacity}" -o json
  -> sku GlobalStandard capacity 10; gpt-4.1-nano 2025-04-14; NoAutoUpgrade; Succeeded;
     request 10 / 60 s; token 10000 / 60 s; Microsoft.DefaultV2; currentCapacity 10
az cognitiveservices account show -g ama -n aif-cutover-test-rzsrg --query "{kind:kind,loc:location,sku:sku.name}" -o json
  -> AIServices; uksouth; S0
az cognitiveservices account list-models -g ama -n aif-cutover-test-rzsrg --query "[?name=='gpt-4.1-nano'].{n:name,v:version,lifecycle:lifecycleStatus,dep:deprecation}" -o json
  -> Legacy; inference 2027-04-14
```

### Regional metadata observation (2026-11-10, Refs #108)

Evidence class: one read-only Azure CLI metadata pass by the signed-in account on 2026-11-10 (UTC 17:50:46 to 17:50:59), four invocations, against the demo app and the one account in `ama` that it names. Repository base `origin/main` `4d8443d442fa8f1c47fa0749e5b8ba7c2bdd23ff`. These are dated queried-time observations, not a standing assertion about the current deployment. No inference, key, token, mutation or other resource was touched.

| Field | Observed 2026-11-10 | What it does not show |
| --- | --- | --- |
| Live demo app `ca-cutover-test-demo-api` (resource group `ama`), one container | `AI_ENDPOINT` `https://aif-cutover-test-rzsrg.openai.azure.com/` and `AI_DEPLOYMENT` `standard`, both plain values, no secret reference | Any other setting; the call path or that a call has succeeded. Fills the "live app environment not re-read" gap of the 2026-11-07 readback for these two settings only |
| Account | `aif-cutover-test-rzsrg` found in `ama` by name, kind `AIServices`, SKU `S0`, location `uksouth`. Its advertised endpoint host (`cognitiveservices.azure.com`) differs from the configured `openai.azure.com` host but carries the same account label | Exact endpoint-string equality; identity rests on the matching account name in the approved group |
| Deployment `standard` | `GlobalStandard`, capacity 10, `gpt-4.1-nano`, version `2025-04-14`, `NoAutoUpgrade`, `Succeeded` | Serving version or region, reserved throughput, latency or quality. A deployment name is an alias, not an immutable model |
| Regional quota limit and unit for `gpt-4.1-nano` `GlobalStandard` in `uksouth` | Unknown. The projected usage query for the two plausible name spellings returned an empty list, so no limit or unit was reported | Zero quota, absence of the model or a permission outcome. An empty list is an unexplained absence, as on 2026-10-18 |

Commands (resource names only; no subscription argument was needed; values below are the exact projections used):

```text
az containerapp show -g ama -n ca-cutover-test-demo-api --query "properties.template.containers[].{container:name,env:env[?name=='AI_ENDPOINT'||name=='AI_DEPLOYMENT'].{name:name,value:value,hasSecretRef:secretRef!=null}}" -o json   -> exit 0
az cognitiveservices account show -g ama -n aif-cutover-test-rzsrg --query "{kind:kind,location:location,sku:sku.name,endpoint:properties.endpoint}" -o json   -> exit 0
az cognitiveservices account deployment show -g ama -n aif-cutover-test-rzsrg --deployment-name standard --query "{sku:sku,model:properties.model.name,version:properties.model.version,upgrade:properties.versionUpgradeOption,state:properties.provisioningState,cap:properties.currentCapacity}" -o json   -> exit 0
az cognitiveservices usage list -l uksouth --query "[?starts_with(name.value,'OpenAI.GlobalStandard.gpt-4.1-nano')||starts_with(name.value,'OpenAI.GlobalStandard.gpt4.1-nano')].{n:name.value,limit:limit,unit:unit}" -o json   -> exit 0, []
```

The Azure CLI filters the usage list client-side, so the regional list was fetched in memory and only the projected rows were kept; current usage, other models and other workloads were never written or published. Raw minimal outputs are private and not committed (`evidence-108-model-metadata-1110` in the session store). Quota remains per subscription, region, model and deployment type, and a limit would not be reserved capacity, remaining budget or headroom; no token-rate conversion is asserted.

#### Quota usage-name mapping continuation (2026-11-10, Refs #108)

The Q4 filter above used guessed name prefixes, so its empty result was inconclusive, not evidence that the quota is missing. A second read-only pass (queries 5 and 6 of the original budget of eight; 6 spent in total, no retry) resolved the provider identifier from the regional model catalog and read only that exact name.

| Query | Queried (UTC) | Outcome |
| --- | --- | --- |
| 5: `az cognitiveservices model list -l uksouth`, projected to `gpt-4.1-nano` `2025-04-14` and its `GlobalStandard` SKU `usageName` | 2026-11-10T17:59:53Z | Exit 0. Both `OpenAI` and `AIServices` catalog entries list `OpenAI.GlobalStandard.gpt4.1-nano` (inference) and a separate `...-finetune` name. The inference identifier is `OpenAI.GlobalStandard.gpt4.1-nano`; the fine-tune identifier was observed in the catalog but was not used for a quota usage query |
| 6: `az cognitiveservices usage list -l uksouth`, projected to that exact name's `limit` and `unit` | 2026-11-10T18:00:08Z | Exit 0, empty list. No row for the exact provider name, so limit and unit remain **unknown** (not zero, not proof the quota is absent) |

The earlier Q4 prefix filter already covered this spelling, so the exact-name read adds mapping evidence, not a new figure. The `usage list` command has no server-side name selector and was not given an unverified `--filter`; the regional list was fetched in memory and only the projected rows kept. The unreturned row is unexplained: possible causes (no per-subscription usage row for this deployment type, or a read-surface limitation) were not tested and are not asserted. The Azure CLI metadata avenue is exhausted for this deployment; any further read surface (for example a different API) would need separate authority. Raw outputs are private and not committed.

### Historical and comparison observations


* The 2026-10-28 readback recorded the same `standard` deployment at capacity
  1; the earlier renewed QA exercise above used a different deployment
  (`gpt-4.1-mini-2025-04-14`, five attempts, 6,884 tokens) whose limits this
  delta did not read. Both are history, not the current nano state, and
  neither supports a mini-versus-nano quality or cost comparison.
* No regional model, version or quota evidence exists for any other
  comparison candidate. Do not infer one from the nano figures, the
  `uksouth` availability list or another model's capacity.

### Remaining #108 gates

* Model names, versions and quotas in the chosen region: configured values for
  this one deployment are now recorded, but actual serving version
  confirmation, serving region or data-residency attestation, a subscription
  quota total and any other candidate remain unconfirmed. The 2026-11-10
  regional pass re-read the configured values and the live app settings, but the
  regional quota limit and unit stayed unknown (empty usage result, also for the catalog-resolved exact name). Keep the criterion
  unticked until the owner decides the evidence suffices.
* Real-model evidence: no actual call is recorded here. A call needs separate
  finite call, token, budget and expiry authority and approved payload
  handling, and it can inform version confirmation only. It does not close the
  serving region or data-residency gap.
* Independent held-out evaluation, thresholds, qualified reviewers and
  calibrated benefit remain blocked and unchanged, and a deployment is not an
  evaluated model.

## Gaps

| Gap | Why it matters | Where it is tracked |
| --- | --- | --- |
| No price table, so no money figure per token | A cost per accepted proposal needs the regional price for the deployed model on a recorded date. None is stored, and none is invented here | BRD OD-51; NFR-012 |
| No denominator defined | Cost per token, per assistant run, per accepted proposal and per accepted handover answer different questions | BRD OD-51; FR-052 |
| TCA components not enumerated for Zava Forward | The investment case lists technology cost lines but not as a Total Cost of AI with a token share | BRD FR-025, RULE-016, NFR-012 |
| No quality floor in cost reporting | A cheaper model that raises critical misses is not cheaper | BRD NFR-012; backlog #108 |
| Review effort is the largest hidden cost | Human review, correction and re-review are likely larger than tokens, which the existing comparative-effort design already measures | BRD RULE-019; PRD effort comparison |
| Chat is a consumption driver | Per-user threads and memory multiply calls per request | Backlog #157 and #159 |

## Backlog

Created #432 (metering, limits and cost per accepted outcome) under epic #104.
Added Tokenomics delta sections with unticked criteria to #100, #104, #107,
#108, #126, #144, #146, #157, #159, #214, #225 and #226 on 2026-10-22. No
existing criterion was changed or ticked.

## Pitch Use

Use the current drafting insert above and
[current capstone authoring source](../../capstone/source/README.md) for new
placement. The [historical Tokenomics pitch brief](../../capstone/history/tokenomics-pitch-brief.md)
preserves earlier options, not the current deck or a rehearsed script.

## Review Triggers

* Tokenomics definition moves beyond draft v0.5.2, or the Big-T notation
  release (December 2026) changes the notation.
* The mentor clarifies what they meant.
* A deployed run produces a measured token total tied to accepted outcomes.
* A regional price for the deployed model is retrieved and dated.

---
title: AI Tokenomics (Total Cost of AI and Value Realised)
description: What the mentor clue on Tokenomics points to, the public Tokenomics Foundation framing, how it maps to the capstone rubric and the Zava Forward evidence, and what remains unmeasured
ms.date: 2026-10-31
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

* The five-assistant path validates prompt, completion and total tokens and keeps
  them with the append-only ledger event when the provider supplies them
  ([assistants](../../../src/core/src/zava_forward/core/assistants.py)). This is
  partial coverage: the legacy `Ai.run()` and `look_at()` paths use `_chat()`,
  which returns text only and discards usage
  ([core `ai.py`](../../../src/core/src/zava_forward/core/ai.py)), and usage can
  remain unknown for an assistant call, in which case the reservation is
  retained. Complete per-call metering is what NFR-012 proposes.
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
| Request calls/depth | Atomic root bounds and looping/fan-out stop are engineered | Live governed activation/acceptance |
| Limits/alerts | Token/money/expiry/unknown-price/liability deny with owner reference | Named owner and approved budgets |
| Dated price | Official source metadata/version stored; unavailable rates explicit | Applicable approved rate source |
| Azure billing reconciliation | Exact-period, scope, allocation and tolerance mechanism | Actual attributable Azure cost records and Finance validation |
| Accepted cost/quality/TCA | Billing-led denominator and quality regression failure mechanism | OD-51, real quality/effort and complete approved TCA inventory |
| Released time | Capacity-not-cash classification | Measured effort; Finance booked destination if cash is claimed |
| Held-out batch/spread | Recorded token min/max/mean mechanism | Finite owner-authorised held-out batch and accepted results |
| Pitch | Brief carries engineering result and stated gaps below | Owner slide placement, deck rebuild/rehearsal and final challenge |

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

See the [Tokenomics pitch brief](../../capstone/pitch/tokenomics-pitch-brief.md)
for the slide option, speaker notes, executive questions and the claims that
must stay out of the pitch.

## Review Triggers

* Tokenomics definition moves beyond draft v0.5.2, or the Big-T notation
  release (December 2026) changes the notation.
* The mentor clarifies what they meant.
* A deployed run produces a measured token total tied to accepted outcomes.
* A regional price for the deployed model is retrieved and dated.

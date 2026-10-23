---
title: AI Placement, Cost and Tokenomics Evidence
description: Curated source-bound findings for the executive script, including negative results and open economic gates
ms.date: 2026-10-23
ms.topic: reference
---

## Scope and Source Baseline

Prepared against main `140d8f494482c78e84d15f3d46b9223d3c487af0`,
including PR #433. This report summarises repository evidence, not new
inference, cloud inventory, billing, legal or customer research.
Paths and line numbers below refer to that baseline.

Independent research informed this synthesis. The final authoring package
does not reproduce unchecked intermediate research claims. In particular,
the early Decision 1 example and later five-assistant QA are different
observations: do not combine them into an invented total number of all calls.

## Why the Original Five-Agent Request Changed

| Finding | Evidence | Presentation implication |
| --- | --- | --- |
| Original brief names five responsibilities with L2-L4 autonomy | `docs/case_study_48_original.md:21-29` | Preserve the business responsibility map, not an assumption that each is an autonomous programme manager |
| Eight role instruments challenged end-to-end ownership; the missing foundation is shared records, states and handoffs | `docs/reference/research/company/agent-request-challenge.md:9-16,38-58` | Describe role agents as research aids, not actual employees approving the design |
| Deterministic policy and accountable human decisions remain distinct from bounded AI assistance | `docs/case_study_48_addendum.md:1136-1150,1265-1300` | Rules enforce gates; AI drafts/scores; people retain consent, professional and financial authority |
| Five assistants share the API proposal runtime; separate queues/workers are deferred | `docs/architecture/README.md:119-137`; `docs/adrs/0002-pilot-readiness-architecture.md`, five-assistant runtime | Do not draw five independently deployed active workers or a Foundry Agent Service orchestrator |

Richer data can improve a narrow task without granting authority. The
reassessment with enriched scenarios did not reverse the original
consultative challenge (`docs/case_study_48_addendum.md:1066-1091`).
This is a design rationale, not direct customer validation.

## Decision 1, Generation and Rules Are Different Tools

`docs/ideas/typesafe-system-one-agent-fit.md:28-76` records the pinned
PR #58 feasibility observation and parallel experiment boundary:

* A real Decision 1 task selected a source-bound EPC candidate with normalised
  option probabilities, model/version/usage and an unreviewed result.
  That demonstrates narrow selection feasibility, not held-out accuracy,
  abstention calibration, reviewer effort saved or superiority.
* A real GPT-4.1-mini task produced a citation-verified summary. One result
  does not establish general semantic quality.
* The provider-specific Foundry services path succeeded after a generic
  host failed. Do not call Decision 1 a hypothetical model with no real
  feasibility evidence, or assume it is an always-on deployed generative tier.
* The deployed support adapter is binary. It cannot establish
  supported/contradicted/insufficient three-class macro-F1 by collapsing labels.
* The four-arm rules/manual, Decision/templates, generative and hybrid
  experiment is a proposed protocol. Owner-reported parallel activity is
  not inspected participant execution or reviewed results.

The task design is source-bound candidate selection/support screening,
not free-form generation and not a rules engine. Clear structured extraction,
arithmetic and explicit policy should remain deterministic unless comparison
demonstrates a reason to do otherwise. Model results do not update
authoritative fields or replace professional judgement
(`docs/case_study_48_addendum.md:1283-1300`).

## A Useful Negative Latency Finding

The historical prototype synthesis records:

| Observation | Classification and limit |
| --- | --- |
| Workflow-only gates/holds/thresholds: 0.03 ms; live agent step: 12.5 s median, 17.7 s p95 | Historical PR #19 observation, not current production SLO or an equivalent-output quality comparison |
| AI added readable handoff drafting, not better blocker detection | Drafting-value hypothesis; reviewer effort saved is unknown |
| Unsupported finding detected by machine validation; recorded 5/6, then 6/6 after a prompt change without relaxing the validator | Small historical evaluation, not a general quality or safety guarantee |

Source:
`docs/reference/research/ux/prototype-learnings-and-simplicity-review.md:84-96`.
Do not calculate a headline speedup ratio or imply the workflow-only and
draft-generation steps produce identical outputs. The defensible learning
is to keep deterministic blocker detection off the generative critical path.

`src/api/README.md:2400-2404` and
`docs/adrs/0002-pilot-readiness-architecture.md:924` separately label the
offline evaluation harness as scripted: it tests behaviour, not live model
quality, latency, variation or incremental benefit.

## The Five-Run Token Observation

`infra/README.md:1503-1517` records a renewed operator QA with:

* A 10-call/126,000-token allowance, one-hour expiry and proactive generation
  off.
* Five registered tasks returning distinct citation-validated `ready`
  proposals through `standard`, `gpt-4.1-mini-2025-04-14`.
* Five attempts, 6,884 total tokens and 15 ledger events.
* Unchanged controlled-domain SQL hashes and retained assistant outputs/usage
  across an actual revision restart.
* Normal serving authority still absent and proactive off afterwards.

The word `ready` means generated and unreviewed, not human-accepted.
`docs/reference/resources/ai-tokenomics.md:85-89` explicitly says this is a
five-sample operational check with no human acceptance, not a throughput,
quality or cost estimate.

Arithmetic mean: 6,884 / 5 = 1,376.8 tokens per run. Do not call that
tokens per accepted proposal. Do not assert that these are all real calls
ever made, or assign these counts to the earlier Decision 1 feasibility task.

## Existing Token Controls Versus Merged Tokenomics Requirements

| Dimension | Current evidence | Proposed or unmeasured |
| --- | --- | --- |
| Token capture | Five-assistant path retains validated usage when supplied | Legacy `Ai.run()` and `look_at()` discard usage; complete coverage absent |
| Bounds | Finite call/token allowance and expiry per authority reference | Not a currency guarantee, independent task/period budget or universal request-depth bound |
| Money | Azure budget notifications exist | Notification is not a hard monetary stop |
| Unit economics | Historical usage observation above | No agreed accepted-outcome denominator, quality floor or reconciled task-cost result |
| Quality-aware optimisation | Smallest-model principle and comparison design | Cheaper routing/cache change must be tested against held-out quality/latency/effort |

Source:
`docs/reference/resources/ai-tokenomics.md:69-111`.

The merged requirements make the desired contract explicit:

| Requirement | Source | Status |
| --- | --- | --- |
| BRD NFR-012, AC-100/101: complete attribution, finite owner-approved task/period and request bounds, price/billing reconciliation | `docs/brds/agentic-retrofit-programme-brd.md:1496-1497` | Proposal; not established by existing finite allowance |
| BRD FR-052, AC-102/103: TCA and named accepted-outcome unit beside quality and Finance-confirmed value | Same source/range; expanded economics discussion at `:1695-1740` | Proposal, not a measured cost or saving |
| OD-51: denominator, quality floor, budgets, alert owners, TCA components and price source | Same source `:1910` | Open decision |
| PRD FR-061/NFR-017 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:892,991-998` | Product requirements, not implemented end-to-end |
| PRD AC-107 through AC-110: metering; quality floor; hard termination; billing reconciliation | Same source `:1554-1557` | All explicitly Not run |

TCA includes attributable platform/hosting, licensing, integration, staff,
human review/correction/re-review, assurance, training, support, maintenance
and exit, with energy/capital where disclosed. Avoid double counting a shared
platform line. Billing is the financial source of truth; any token-to-money
conversion needs a dated/versioned price source.

Report cost per accepted proposal above an agreed quality floor as the
proposed primary AI unit, subject to OD-51. Cost per accepted handover is a
separate end-to-end unit. If the denominator is zero or unknown, report not
measurable. Lower price per invocation that worsens critical misses or
resident/quality outcomes is a failure, not a saving.

No internal Microsoft deck content is needed or included. Public Tokenomics
community framing is draft, not an accepted standard. This package does not
use the podcast's token-share percentage as a benchmark.

## Current Budget Decision and What Still Blocks Execution

Source: `docs/case_study_48_addendum.md:321-405`, especially
the revised owner decision and post-change refresh gate.

| Item | Correct classification |
| --- | --- |
| USD 450/month, EXA-012 | Historical 2026-10-10 technology allocation; not current blanket authority |
| #58 cap removal | Scoped to that rebuild, not all future spend (`:215-218`) |
| USD 500 and old thresholds | Superseded 2026-10-20 historical planning basis |
| USD 700 | Owner-set replacement all-in October forecast ceiling on 2026-10-22; includes accrued charges, outside-group spend, approved tranches and reserve |
| Expiry | 2026-10-25T16:02Z; no extension inferred |
| USD 242.36 | Observed 11-22 October resource-group `ama` accrued cost, partial 22 October, estimates until invoiced and subject to lag |
| USD 535.33 | Pre-change scenario, not current forecast or an upper bound |
| Outside-group U | Unreadable/unknown, never zero by assumption |
| Paid tranche activation | Still blocked pending refreshed post-change forecast, bounded U and remaining prerequisites |

A separately authorised edge deletion and API scale-down occurred on
2026-10-22. The later cost read was unchanged: no post-change saving or zero
residual charge is measured. A fresh inventory/timestamp/currency and at least
one complete post-change day are required before recomputing the envelope.
Do not add overlapping accrued-cost snapshots.

The existence of the owner's budget decision does not mean this planning
document executes a tranche, clears access/capacity or accepts a release.
Conversely, do not mislabel the USD 700 owner decision as merely an
unapproved ceiling proposal. It is not a production monthly price.

## Retrofit Economics Is a Different Ledger

`docs/case_study_48_addendum.md:124-131,144-157` declares fictional fixtures:
GBP 18,000 contractor + GBP 2,000 internal = GBP 20,000 base;
GBP 2,000 contingency gives a GBP 22,000 envelope.
Eligible cost GBP 16,000 minus a fictional grant GBP 7,500 gives GBP 8,500
eligible match; adding GBP 4,000 ineligible cost gives GBP 12,500 provider
base funding. Gross cash before grant receipt is GBP 20,000.
Fully spent contingency increases provider exposure to GBP 14,500.
At GBP 12,000 eligible cost the fictional 50% ceiling caps grant at
GBP 6,000, giving GBP 14,000 provider base.

These are exercise arithmetic, not a company balance sheet, actual award,
current grant condition or technology price. The original GBP 40m and
doubling ambitions are not observed outcomes.

## Strong CXO Answer Stems

* Why change five agents? "We retained five responsibilities and separated
  deterministic controls, bounded preparation and accountable decisions."
* Is Decision 1 faster/cheaper? "Narrow feasibility exists. A paired,
  human-adjudicated cost/latency/quality advantage is not yet established."
* What is AI cost per accepted home? "Unknown. We must agree the denominator,
  quality floor, price/billing basis and complete cost components first."
* Can the bill grow unseen? "The existing bounded path has finite tokens and
  expiry, but complete metering and monetary/request-depth controls are
  proposed, not tested."
* Is the exercise worth it? "Compare workflow-only and AI-assisted tasks,
  including review and rework. Saved time is capacity until Finance confirms
  where value is realised."

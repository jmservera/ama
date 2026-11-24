---
title: Tokenomics Model-Tier Comparison, Placement and Timing for the Capstone Pitch
description: Dated comparison of a decision model, a small GPT model and a large LLM for yes/no document checks, with evidence labels, a placement recommendation for the decision-model-first point and computed (not rehearsed) timing; supports #435
author: AMA programme
ms.date: 2026-11-24
ms.topic: how-to
---

## Status

DRAFT for the owner. This page adds wording and a comparison. It is not a
rehearsal result, a measurement, a deck rebuild or a saving claim. The
owner decision of 2026-11-13 stands: slide 22 (S18) carries Tokenomics on
the main route, with B25 and B27 as question cards, and the USD 0.44 per home
figure stays a labelled planning scenario (see the
[placement draft](./tokenomics-placement-draft.md)).

## The Point to Make

Zava Forward asks a model only for work that rules cannot do. Yes-or-no
checks on documents and cases, such as whether a scan is clean, whether a
field is present or whether a gate passes, are answered by coded rules first.
A rule answer spends no tokens, gives the same result for the same input and
returns `unknown` (never a pass) when evidence is missing. This is an
architecture choice. It has not been measured as a saving.

Repository observations, read 2026-11-24:

* `src/core/src/zava_forward/core/gates.py`: pass, fail or unknown with a reason, owner and correction route; unknown never passes.
* `src/core/src/zava_forward/core/doc_controls.py`: a document is available only when its scan status is clean; the local scanner is development-only and the Defender for Storage reader has not been run against a real account.
* `src/core/src/zava_forward/core/form_validation.py`: deterministic validation; without approved rules it reports Not evaluated.
* `src/core/src/zava_forward/core/ai_decision.py`: continue, narrow, pause or retire by ordered limits; missing evidence yields pause.
* Speaker script page 17: known gates and arithmetic do not need generation; the rules-only path stays the comparator.

## Comparison (retrieved 2026-11-24)

Evidence labels: Public fact (stated by the cited source on the retrieval
date), Observation (read in this repository), Unknown (no evidence held).
Prices are published list prices in USD per 1M tokens, standard tier, short
context. They are not Zava's deployment price, not a total cost and not a
saving. No ratio between rows is computed.

| Aspect | Decision model / coded rules | Small GPT model (GPT-6 Luna) | Large LLM (GPT-6.2 Astra) |
| --- | --- | --- | --- |
| What answers a yes/no document check | Decision table or rule set; DMN 1.7 beta describes decision tables as an executable expression language (Public fact, [OMG](https://www.omg.org/spec/DMN/), beta, September 2026). Zava uses coded gates (Observation) | Model call; OpenAI recommends it for "small, repeatable tasks" such as extracting fields when the expected result is clear (Public fact, [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection)) | Model call; the same guide points to it for demanding engineering or analysis, not for simple checks (Public fact, same source) |
| Published token price | None; no per-token charge (Public fact by construction). Hosting, authoring and review cost: Unknown | Input 0.10, output 0.50 (Public fact, [OpenAI pricing](https://developers.openai.com/api/docs/pricing)) | Input 8.00, output 40.00 (Public fact, same page) |
| Same input, same answer | Yes by design for a pure rule (Observation of `gates.py`; not a measured test across the pipeline) | Not guaranteed; Unknown for Zava checks | Not guaranteed; Unknown for Zava checks |
| Missing evidence | Explicit `unknown`, never a pass (Observation) | Unknown | Unknown |
| Where it fits | Yes/no and threshold checks with a stated rule and owner | Narrow, repeatable extraction or classification with a quality floor | Open-ended drafting or analysis behind human review |
| Routing between models | Not applicable | Microsoft Foundry model router sends simple prompts to small models and hard ones to frontier models (Public fact, [Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router), ms.date 2026-11-18) | Same source |
| Accuracy on Zava checks | Unknown: no held-out comparison of rules against a model exists | Unknown | Unknown |
| Cost per accepted outcome | Unknown | Unknown | Unknown |

The Microsoft Azure OpenAI pricing page was fetched on 2026-11-24 but its
prices did not render without a browser, so no Azure price is used here. The
GPT-4.1-mini rate behind the USD 0.44 scenario is a separate, older secondary
source; do not mix it with this table.

## Placement Recommendation

Recommended: speak it as the lead-in of slide 22 (S18) inside the existing
50-second slot, anchored back to page 17, with B25 as the CFO answer and B27
for hidden calls. No new slide, no new minutes on the 24:30 route and no
deck rebuild are needed; the comparison table stays as presenter backup for
questions. Reasons: page 17 has already told the audience that gates and
arithmetic do not need generation, and S18 is where the audience first meets
model cost, so "ask a model only after rules" answers the cost question at the
moment it forms. A separate main-route slide would spend time without new
evidence (B7); spoken-only without the table leaves no cited answer (B6).

Draft lead-in (45 words, evidence label: observation and proposal; no price
or saving claimed):

"Before any model call, coded rules answer the yes-or-no checks: is the scan
clean, is the field present, does the gate pass. Those spend no tokens. A
model is asked only for work rules cannot do, such as preparing a proposal,
and a person decides."

If the owner wants the table on a slide, treat it as a B-series appendix card
and rebuild the deck through the `powerpoint` workflow; that has not been done.

## Rehearsal Timing (computed, not rehearsed)

| Text | Words | At 130 wpm | At 150 wpm | At 160 wpm |
| --- | --- | --- | --- | --- |
| Lead-in above | 45 | 20.8 s | 18.0 s | 16.9 s |
| Existing slide 22 cue (20-second version) | 54 | 24.9 s | 21.6 s | 20.2 s |
| Lead-in plus cue | 99 | 45.7 s | 39.6 s | 37.1 s |

Reading: the combined text fits the 50-second slot at all three rates, so
the route length is unchanged. This is arithmetic on the script, not an
observed time. A presenter run and the mentor's meaning of Tokenomics are
still needed; the record in the
[rehearsal notes](./tokenomics-rehearsal-notes.md) stays blank until they
happen.

## Claims to Keep Out

* Any saving, payback or percentage reduction from using rules instead of a model.
* Any statement that rules are more accurate than a model on Zava checks.
* The list prices above presented as Zava's cost.

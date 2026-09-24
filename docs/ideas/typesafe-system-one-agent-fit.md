---
title: System One Decision Models for Retrofit Agents
description: Research on using typed decision models such as Kev-4B through the TypeSafe System One contract, and where they fit the Case Study 48 agents
ms.date: 2026-09-24
ms.topic: reference
---

## Status and Evidence

This is research for [IDEA-001](./idea-register.md). It is a proposal to
evaluate, not a validated design or an approved requirement. Read it alongside
the [original Case Study 48](./case_study_48_original.md), the
[Case Study 48 Addendum](./case_study_48_addendum.md) and the
[Business Requirements Document](./brds/agentic-retrofit-programme-brd.md).

| Evidence | Classification | Retrieved | Notes |
| --- | --- | --- | --- |
| [TypeSafe documentation](https://docs.typesafe.ai/llms.txt), including the [API reference](https://docs.typesafe.ai/api), [primitives](https://docs.typesafe.ai/primitives), [confidence](https://docs.typesafe.ai/confidence), [building guide](https://docs.typesafe.ai/concepts/how-to-build-with-system-one) and cookbooks | Vendor documentation | 2026-09-24 | Describes the contract and design patterns; cookbook results are vendor demonstrations, not housing evidence |
| [Kev-4B model card](https://huggingface.co/jaredpalmer/kev-4b), version dated 2026-09-24 | Self-reported open-weight model benchmarks | 2026-09-24 | Many evaluation labels are AI-adjudicated with human spot checks; the checkpoint changes often |
| [Kev repository](https://github.com/jaredpalmer/kev) | Open-source project documentation | 2026-09-24 | Independent "Jev-like" project that serves the same API contract; not evidence of TypeSafe endorsement |
| Agent-fit assessment in this document | Internal interpretation | 2026-09-24 | Needs review by the delivery, data, safety, resident and data-protection owners |

> [!IMPORTANT]
> No accuracy figure in this document is evidence of performance on Proper
> North Homes data. Every candidate use needs a labelled test set, a threshold
> chosen for its consequences and a shadow-mode trial before any live use.

## What a System One Model Is

A System One model receives a *state* (a document, record or conversation) and
a map of typed questions. It returns one typed answer per question in a single
forward pass, with no generated text. TypeSafe's flagship model is Jev. Kev is
an independent family of open-weight models (0.8B, 4B and 9B) that serves the
same `POST /v1/systemone` contract, so the TypeSafe SDK can point at a local
or self-hosted Kev server.

The contract has three question types:

| Primitive | Returns | Use when |
| --- | --- | --- |
| Choice | The selected option, a probability per option and a confidence value | One answer from a defined set, with at most 255 options per question |
| Noul | The probability that the answer is yes, with no separate confidence value | A single condition, or one question per label when several labels may apply |
| Score | A probability-weighted position on ordered, described levels, with confidence | A degree along one dimension, such as severity or completeness |

Each question has `instructions` and `criteria`. Both accept strings or
structured JSON, and questions can reference fields in the state by backticked
path. Question IDs are for code only and are not sent to the model.
Independent questions over the same state run in parallel in one request.

### Why This Counts as Typesafe

The typed interface is the safety property. It does not guarantee that the
answer is correct.

* The answer can only be one of the options that code defined, so downstream
  functions receive values they accept. Closed sets map to `Literal` types.
* The model never writes free text that could be mistaken for an approval, a
  consent record or a legal conclusion.
* Code keeps the workflow, rules, dates, calculations and permissions. The
  model supplies a narrow semantic judgment where ordinary code cannot read
  meaning.
* Probabilities and confidence let code decide when to act, when to ask for
  confirmation and when to route to a person.

This matches the addendum's position that deterministic workflow controls
mandatory gates and bounded AI supports recommendations, reconciliation and
exception detection.

## Kev-4B Profile

Figures are from the model card for the 2026-09-24 version and are
self-reported.

| Property | Value | Implication for this project |
| --- | --- | --- |
| Architecture | LoRA adapter (r=16) and pointer head on `Qwen/Qwen3.5-4B-Base` | Small enough to self-host |
| Licence | Apache-2.0 for the adapter and head; the Qwen3.5 base is Apache-2.0 | Permits commercial self-hosting, subject to legal review of dataset licences |
| Serving | About 9 GB of GPU memory in bf16; 8,192-token serving context | Long documents such as survey packs must be split into sections |
| Out-of-domain accuracy | 0.835 on the locked test (Brier 0.233); Jev 0.857 on the development set | Useful, but lower than Jev on new kinds of content |
| Coverage at 5% error or less | 0.552 (Jev 0.70) | About half of decisions could be automated at a strict error budget in the reported suites |
| Confident errors out of domain | 2.9% of answers at p of 0.9 or more were wrong (Jev 3.7%) | High confidence still needs checks for consequential actions |
| Unknowable items answered at 0.9 or more | 0.00 (Jev 0.09) | Tends to report uncertainty when evidence is missing |
| Real-document accuracy | 0.904 after a delta fine-tune on about 5,200 US consumer-finance complaints | The gain is in distribution only and does not transfer automatically to housing records |
| Date arithmetic | 0.60 on the deadline suite; 0.85 with the `date_facts` preprocessor (older checkpoint figures) | Statutory clocks must stay in code |
| General knowledge | MMLU-Pro 0.515 (Jev 0.840) | Must not be used to answer regulatory or technical knowledge questions |

The card also reports that the shipped calibration temperature is fitted in
distribution and does not transfer to every workload. It provides a
calibration tool that refits temperature on a workload's own labelled rows.

### Hosting Options

| Option | Strengths | Constraints |
| --- | --- | --- |
| TypeSafe hosted Jev | Highest reported accuracy and coverage; no model operations | Resident and property data leave the association's environment; needs supplier, contract and data-protection review |
| Self-hosted Kev-4B | Data stays in a controlled environment; open weights; can be fine-tuned and recalibrated on local data | Lower accuracy than Jev; the association or a supplier must run GPU serving, monitoring and version control |
| Self-hosted Kev-9B | Better reported accuracy and calibration than Kev-4B | Needs more GPU memory and cost |

Any option handling vulnerability, health or safeguarding data needs a
lawful basis, purpose limitation, retention rules and a data-protection impact
assessment under BR-058 and BR-016. Self-hosting reduces transfer risk but does
not remove these duties.

## Design Rules for This Programme

Apply these rules to every candidate use:

* Ask one narrow judgment per question and give each Choice a no-match or
  unclear option.
* Keep rules, dates, deadlines, calculations, eligibility formulas and
  permissions in code.
* Put only the minimum necessary data in the state, and label each field.
* Treat a model answer as a recommendation or flag under BR-009, never as an
  approval.
* Fail closed. A missing, low-confidence or failed answer must not permit
  progression or suppress an urgent response (BR-017).
* Let a model add a hazard, safeguarding or complaint flag, but never let it
  remove, downgrade or close one.
* Set thresholds per action from labelled evaluation data, weighting missed
  hazards and missed withdrawals far more heavily than extra reviews.
* Log the model version, question definitions, state hash, answers and
  resulting route for every consequential decision (BR-006, BR-042).
* Pin model revisions and question versions, and rerun regression tests
  before changing either.

## Fit With the Requested Agents

The five agents in the original brief combine several kinds of work. A
decision model can serve some of their judgments, but none of the agents can
be replaced by a classifier alone.

| Agent (original autonomy) | Fit | Useful typed judgments | Stays in code, generative models or people |
| --- | --- | --- | --- |
| Contractor and Resident Coordination (L3) | Strong for intake and routing | Message intent, hazard mention, complaint, possible withdrawal or pause, request for adjustments, contractor delay cause | Scheduling solver, capacity commitment, drafting messages, recording consent |
| Quality Verification (L4 flags) | Strong for evidence flags | Per-item evidence presence, match between installation evidence and approved design, defect severity in inspection notes | Sensor analytics, quality acceptance, defect closure |
| Stock Prioritisation (L2) | Partial | Features from free-text surveys, repair logs and resident contacts, such as described damp severity or ventilation issues | Ranking weights, grant eligibility rules, structured energy and stock data |
| Grant and Funding (L3) | Partial | Whether cited evidence supports each claim in a draft; mapping evidence to scheme requirements | Drafting, calculations, reconciliation totals, Finance approval and submission |
| Assessment (L3) | Limited | Completeness checks of survey packs; selecting values from candidate spans; flagging conflicts with the stock record | Site observation, professional assessment and every PAS 2035 output |

### Contractor and Resident Coordination Agent

Inbound resident and contractor messages are the clearest fit, using the
intent-routing and speculative fan-out patterns.

* A Choice selects the main intent from a closed set, such as reschedule,
  question, complaint, decline or withdraw, report a problem and unclear.
* Independent Nouls check for a hazard description, a complaint, a request
  for a pause or withdrawal, a support or adjustment need and signs of
  distress. They run in the same request.
* A Choice with closed sets can fill scheduling preferences, such as preferred
  time window and contact channel, following the function-calling cookbook.
  The scheduling itself stays in code.
* For contractor updates, a Choice classifies the delay cause against a
  controlled taxonomy. This also supports the Phase 0 baseline by delay cause
  (IDEA-001a).

Controls that must hold:

* A hazard Noul above a deliberately low threshold opens a hazard handoff in
  addition to normal routing. A low score never closes or delays the
  statutory response, and the response clock starts from recorded facts in
  code.
* A possible withdrawal or pause places affected non-urgent work on hold and
  routes to a person (BR-014). The model never records agreement, and silence
  or access is never treated as consent (BR-011).
* Failed access is not classified as refusal (BR-020).
* Low intent confidence routes to a named human queue with the full handoff
  content required by BR-018.

### Quality Verification Agent

Quality flags suit Noul and Score questions because the agent only flags.

* One Noul per required evidence item asks whether the submitted pack
  contains it. Code compares the answers with the evidence template for the
  measure.
* The citation-check pattern asks whether each installation record supports,
  contradicts or does not address the approved design element.
* A Score rates defect severity described in inspection notes against
  levels written by the competent quality authority.

Sensor readings are numeric and belong in statistical code, not a language
decision model. A normal reading cannot override a resident report (BR-037).
Flags are autonomous, but acceptance and closure remain human (BR-010).

### Stock Prioritisation Agent

Most prioritisation inputs are structured and should use rules or classical
models. A decision model can turn unstructured records into reusable features
using the composite-scoring pattern.

* Scores for described damp, mould, condensation or ventilation severity in
  surveyor notes and repair logs
* Nouls for mentions of specific conditions or previous failed work
* A Choice for property archetype when only a text description exists, using
  hierarchical classification for large taxonomies

Weights stay in code and are approved by the asset and safety owners. Missing
data or a missing signal triggers investigation, not silent deprioritisation,
as the addendum trade-offs require.

### Grant and Funding Agent

Drafting a bid is a generation task. A decision model can check the draft.

* For each claim in a draft, a Choice decides whether the linked evidence
  supports, contradicts or does not address it. Quotes are matched in code
  first, so a missing quote is marked as fabricated without a model.
* A Choice maps each evidence item to the scheme requirement it is meant to
  satisfy, with an explicit "none of these" option.

All figures, match-funding calculations and claim totals stay in code. Finance
validates, approves and submits (BR-027).

### Assessment Agent

This is the weakest fit. Competent professionals own PAS 2035 outputs, and the
licensed standard is not reproduced in this repository.

* Nouls can check whether a survey pack contains the sections required by a
  template that a competent person has approved.
* The pre-parsed value-extraction pattern can find candidate values with
  regular expressions and use a Choice to select the intended one, so values
  are copied rather than invented.
* The entity-alignment pattern can flag disagreements between survey data and
  the stock record for a named data owner.

The model must not infer an observation that is not in the evidence.

### Cross-Cutting Opportunities

| Capability | Candidate judgments | Main constraint |
| --- | --- | --- |
| Damp-and-mould response loop | Hazard description Noul and severity Score on resident reports | Adds flags only; statutory timescales are computed in code from the applicable, verified regulations |
| Exception handoff routing | Choice of receiving team and exception type, with hierarchical classification for large taxonomies | Missing classification cannot permit progression (BR-017) |
| Resident communication guardrails (IDEA-001b) | Nouls for implied consent, universal bill-saving promises, use of the working programme line in hazard, complaint or consent content, and missing complaint routes | A human still approves and sends the message |
| Regulatory change monitoring (IDEA-001d) | Choice of change type and a Noul per affected requirement for each detected difference | Legal, compliance or professional owners decide; the model does not interpret law |
| Executive reporting | Citation checks of narrative claims against controlled records; a Noul for forecasts presented as facts | Executives and the Board decide |

## Poor Fits

Do not use a System One model for:

* Drafting resident letters, bids or reports, which need a generative model
  and human review
* Date arithmetic, statutory deadlines and response clocks
* Financial calculations, eligibility formulas and scheduling optimisation
* Numeric sensor analysis
* Legal interpretation, regulatory knowledge or technical PAS 2035 judgement
* Any decision to approve, submit, accept, release a hold or record consent

## Example: Typed Resident Message Triage

The example shows the shape of a fail-closed integration. Option wording,
thresholds and queues are placeholders to be set by the owners and by
evaluation.

```python
from typing import Literal

from typesafe_sdk import Choice, Noul, TypeSafeClient

Intent = Literal[
    "reschedule", "question", "complaint", "decline_or_withdraw",
    "report_problem", "unclear",
]

INTENT_CRITERIA: dict[Intent, str] = {
    "reschedule": "Wants to change or arrange an appointment time",
    "question": "Asks for information about the proposed works",
    "complaint": "Expresses dissatisfaction and wants it addressed",
    "decline_or_withdraw": "Does not want, or no longer wants, some or all works",
    "report_problem": "Reports a defect, hazard or problem in the home",
    "unclear": "None of the above clearly applies",
}

# Placeholders: set from labelled evaluation data, biased towards recall.
HAZARD_FLAG_AT = 0.2
WITHDRAWAL_FLAG_AT = 0.2
INTENT_ACT_AT = 0.8

client = TypeSafeClient(api_key="local", base_url="http://127.0.0.1:8008", model="kev-latest")


def triage(message: str) -> list[str]:
    response = client.system_one(
        state={"resident_message": message},
        questions={
            "intent": Choice(
                instructions="What is the resident mainly asking for in `resident_message`?",
                criteria=INTENT_CRITERIA,
            ),
            "hazard": Noul(
                instructions=(
                    "Does `resident_message` describe damp, mould, a leak, loss of "
                    "heating or any other possible hazard in the home?"
                ),
            ),
            "withdrawal": Noul(
                instructions=(
                    "Does `resident_message` say the resident wants to stop, pause "
                    "or not go ahead with any proposed works?"
                ),
            ),
        },
    )

    routes: list[str] = []
    if response.nouls["hazard"].noul >= HAZARD_FLAG_AT:
        routes.append("hazard_handoff")  # Added, never removed, by the model.
    if response.nouls["withdrawal"].noul >= WITHDRAWAL_FLAG_AT:
        routes.append("pause_and_consent_review")  # A person confirms with the resident.

    intent = response.choices["intent"]
    if intent.choice == "unclear" or intent.confidence < INTENT_ACT_AT:
        routes.append("human_triage")
    else:
        routes.append(f"queue:{intent.choice}")
    return routes
```

A service failure must raise an error that routes the message to human
triage. It must not return an empty route list.

## Evaluation Plan

Run this inside Phase 1 shadow mode from the addendum, with no live
consequential action.

1. Build synthetic, labelled test sets for resident messages, contractor
   updates, inspection notes and survey extracts. The Housing Data and
   Performance Lead agent can help design them. Use real data only after
   lawful-basis and privacy approval.
2. Compare rules, Jev, Kev-4B, Kev-9B and a generative model on the same
   items, with the same question definitions.
3. Report accuracy, recall on hazard, safeguarding and withdrawal cases,
   Brier score, calibration error and coverage at an agreed error budget.
4. Refit calibration on local labelled data for Kev, and set thresholds per
   action with the accountable owners.
5. Measure review effort, override rate, latency and whole-life cost,
   including GPU serving and model operations.
6. Consider fine-tuning Kev on approved local labels only if the baseline is
   close but insufficient. The model card suggests a few thousand labelled
   documents can move in-distribution accuracy, but that result comes from a
   different domain.

Success needs zero missed critical exceptions in the agreed tests, consistent
with the addendum's AI safety measure, not only a high average accuracy.

## Open Questions

* Which owners approve the question definitions and option sets for each
  judgment?
* Which hosting option is acceptable to data protection, procurement and
  information security?
* Which labelled historical records exist, and can they lawfully be used for
  evaluation or fine-tuning?
* What error budget does each action tolerate, and who signs it off?
* How are model and question versions governed alongside the regulatory
  source register?

## Change Monitoring

| Source | Change likelihood | Review cadence |
| --- | --- | --- |
| Kev model card and checkpoints | High; new versions appeared on 2026-09-21 and 2026-09-24 | Pin a revision and check before each evaluation run |
| TypeSafe API and SDK documentation | Medium | Check before writing or upgrading integration code |
| TypeSafe cookbook results | Low relevance to housing performance | Treat as design examples only |

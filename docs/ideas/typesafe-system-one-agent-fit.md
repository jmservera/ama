---
title: System One Decision Models for Retrofit Agents
description: Dated research on typed decision models, including Microsoft Decision 1 in Foundry, bounded workflow assists and reviewed form extraction/filling
ms.date: 2026-10-10
ms.topic: reference
---

## Status and Evidence

This is research for [IDEA-001](./idea-register.md). It is a proposal to
evaluate, not a validated design or an approved requirement. Read it alongside
the [original Case Study 48](../case_study_48_original.md), the
[Case Study 48 Addendum](../case_study_48_addendum.md) and the
[Business Requirements Document](../brds/agentic-retrofit-programme-brd.md).

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

## Microsoft Decision 1 Reassessment (2026-10-10)

The owner requested reassessment across the process after Foundry model
availability, then specifically requested PRD integration for form
extraction/filling, retrofit subsidy applications and other AI-assisted
decisions. The recommendation is an optional scoring capability inside the
existing bounded task service, not another autonomous agent or replacement
workflow engine. The [PRD v0.11.0](../prds/proper-warm-retrofit-programme-demonstrator.md)
records this as proposed DD-007/008 and FR-036 to FR-044, not a production
selection, deployment result or approved funding process.

### Current Product Evidence and Limits

All sources in this table were checked on 2026-10-10. They are vendor product
documentation, not regulatory authority or Proper North Homes performance
evidence. The findings below supersede incompatible automation, SDK or
ranking suggestions in the retained 2026-09-24 research sections.

| Source / source date | Verified finding | Design consequence |
| --- | --- | --- |
| [Microsoft announcement](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/), October 2026 announcement | Decision 1 is offered through Foundry for typed decisions | Availability justifies evaluation, not deployment or local benefit claims; advertised pricing/speed/calibration are not a subscription quote or housing result |
| [Model catalog](https://ai.azure.com/catalog/models/Microsoft-Decision-1), checked 2026-10-10 | Text-only, closed questions; no generated text/rationale; not intended as sole automated decision-maker for consequential housing decisions, or for individual surveillance/profiling/tracking | Separate parsing/OCR and generation; application-owned evidence explanation; no resident profiling or new model decision rights |
| [Deployment/API guide](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision), source date 2026-10-07, updated 2026-10-09 | Version 1; POST `/providers/microsoft/v1/systemone`; deployment name in `model`, text/JSON `state`, named typed `questions`, response `answers` plus model identity/usage | Provider-specific adapter; do not assume Chat Completions or the historical TypeSafe SDK's response/confidence fields; prove actual synthetic-response schema before activation |
| [Deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) and [regional availability](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability), checked 2026-10-10 | Documented Decision 1 serving uses GlobalStandard or DataZoneStandard in selected regions | A UK resource does not establish UK-only processing; confirm subscription/model availability and permitted processing before any personal-data inference |
| [Entra configuration](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/configure-entra-id), checked 2026-10-10 | Foundry supports Entra authentication subject to resource/deployment permissions | Verify the actual inference role/scope, local-auth setting, private endpoint/DNS and network route; generic Foundry support is not evidence of this deployment |

Choice selects a defined key with option probabilities. Noul scores a yes/no
question. Score is a probability-weighted position on supplied ordered
criteria, not an absolute calibrated technical or hazard severity. Exact
response fields, probability validation and local abstention thresholds
remain conformance/evaluation work. Typed output can be confidently wrong
and may be sensitive to wording, order and unfamiliar data.

### Process-Wide Candidate Map

These are task-shape hypotheses. None is a measured accuracy, savings or
company-practice finding. All nine workflow families were revisited.

| Workflow | Useful optional judgment | Boundary |
| --- | --- | --- |
| Stock, import and prioritisation | Candidate-field selection, record/document classification and conflicts | No model score or inferred feature changes authoritative ranking, queue membership or eligibility; source corrections need separate owner authority |
| Technical assessment/design | Documentary support, missing observations and version conflicts | No site observation, design suitability, PAS 2035 output or professional sign-off inferred |
| Resident service/access/choice | Independent multi-intent, complaint, possible pause/withdrawal flags; draft screening | First human urgent triage is independent; no consent/refusal inference, latent vulnerability profile or unreviewed communication |
| Procurement/capacity/work release | Delay-note categories and proposed-scope mismatch | Scheduling, commitments, instructions and contract judgments remain rules/people |
| Hazard awareness/response | Supplemental raise-only signal in already routed text | Never suppress, downgrade, defer, reset a clock, release a hold or close; service cannot depend on scorer availability |
| Quality/defects/handover | Evidence support/contradiction and draft-content checks | No image inspection, physical acceptance, defect grading/closure or inferred resident understanding |
| Budget/invoice/funding/claim/cash | Candidate fields, section-to-evidence match and unsupported financial narrative | Rules calculate; Finance interprets/reviews; application, award, invoice, claim and cash stay distinct; no submission/payment/certification |
| Cross-team case orchestration | Exception category or suggested task from permitted candidates | Deterministic state machine, permissions, ownership and accepted handoff remain authoritative |
| Portfolio investment/performance | Source-support checks and aggregate narrative classification | Statistical forecast, investment, scale and causal benefit decisions remain code/Finance/Board |

The fifteen-step lifecycle was also examined. Candidate documentary tasks
do not make a step model-owned:

| BRD lifecycle step | Candidate assist / retained authority |
| --- | --- |
| 1. Identify/match home | Flag ambiguous documentary identity; owner resolves identifiers |
| 2. Prioritisation/screens | Advisory conflict/support checks; rules alone rank and screen |
| 3. Safety/data readiness/access | Missing evidence/contact-request flag; first human triage, clocks and access remain independent |
| 4. Assessment accepted | Evidence support/omission check; competent reviewer accepts |
| 5. Options/disruption discussed | Draft-content guardrail; human conversation and explanation |
| 6. Design approved | Document/version conflict flag; competent designer signs off |
| 7. Resident decision recorded | Possible pause/withdrawal flag for review; no inferred or prefilled decision |
| 8. Funding/investment/capacity confirmed | Evidence mismatch checks; approved budgets, deterministic eligibility and named human commitment |
| 9. Work released/scheduled | Proposed scope check; gates, solver and authorized issuer |
| 10. Installation hold points | Installer-note categories; physical observation and competent acceptance |
| 11. Quality evidence accepted | Documentary support/conflict check; independent quality acceptance |
| 12. Resident handover | Draft omissions/unsupported promises; human delivery and accessibility/understanding validation |
| 13. Payment/grant reconciliation | Semantic line/evidence checks; arithmetic, Finance approval and external submission |
| 14. In-use monitoring | Aftercare text classification; numeric analytics and human response |
| 15. Close/reopen | Possible missing/recurring evidence flag; authorized human decision only |

Supporting uses include delay-note baseline discovery, access-filtered
retrieval relevance, generated-output pre-screening and categorizing verified
regulatory differences. These do not validate legal duties, approve rule
activation, replace independent assurance or create model-owned task routing.
Static capability selection comes first.

### Form Extraction and Filling Recommendation

Use a reusable, versioned form workspace, first demonstrated with constructed
retrofit funding applications and separate claims. An evidenced competitive
application, allocation request, award-delivery return and reimbursement
claim are not interchangeable. Unknown route blocks funding bid/form
preparation under BRD FR-027; non-funding forms need an approved schema but
not a funding route. No open round or actual award terms are assumed.

* Approved structured records and parsers supply candidate values. Scans need
  separately approved OCR/transcription; preserve its errors, source
  page/span/cell and document version/hash.
* Decision 1 may select among cited candidates or classify evidence as
  supported, contradicted or insufficient. Include no-match/unknown; never
  invent missing EPCs, measures, costs, co-funding or site observations.
* Rules compute amounts, dates, limits and eligibility from approved scheme
  versions and confirmed inputs. Optional generative models draft only cited
  narrative; a decision score cannot generate a truthful rationale.
* Show raw/normalized values, alternatives, lineage, uncertainty and each
  reviewer decision side by side. Selection changes a draft, not a source
  record, ranking, queue or approval. Review all required fields, not only
  flags, to counter automation bias.
* Exclude resident choices, declarations, signatures, certifications and
  controlled approvals from AI pre-fill and batch acceptance. Finance reviews
  the pack; exporting it does not submit it, secure an award, certify a claim
  or establish cash. External submission is outside the demonstrator.
* Versioned source/schema/rule/input dependencies invalidate affected field
  and pack reviews, preserving previous values and decisions. Unknown
  mandatory fields block a reviewed pack; incomplete working copies are
  visibly incomplete.

### Evaluation and Activation Gate

Compare manual/templates, parsers/rules, Decision 1 and appropriate
generative alternatives on identical, human-adjudicated held-out cases.
Separate tuning/calibration/test sets by case/building/document family;
measure exact/normalized field accuracy, provenance, unsupported critical
values, omission recall, abstention/calibration, OCR-error propagation,
export fidelity, total preparation/review/correction effort and whole-life
cost. Test ambiguity, option order, negation, mixed intents, unreadable
sources, stale schema/input, restricted sources and source-text injection.

Owner-approved thresholds and critical categories are pre-registered per
task. Zero missed critical controls in an agreed sample is required but does
not prove zero population risk. Compare unflagged outputs too. Disable or
retain manual handling when incremental value or review capacity is absent.
No automatic training, threshold/policy activation or provider substitution.

The adapter must validate the real provider response and bind source IDs
through application code, recording explicit timeout, access/throttle,
missing/invalid-answer and stale-source states rather than empty success.
Serving version, quota, inference authorization, network/processing terms,
local performance and subscription pricing remain unverified. Personal-data
use, control activation and live submission require separate named approval.

## Historical 2026-09-24 Baseline

The remaining sections preserve the earlier Jev/Kev investigation and SDK
example. They are not a Decision 1 API specification or current permission
to automate an action. The dated reassessment and current PRD authority
boundaries take precedence.

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

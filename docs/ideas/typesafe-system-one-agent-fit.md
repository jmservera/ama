---
title: System One Decision Models for Retrofit Agents
description: Dated research on typed decision models, including Microsoft Decision 1 in Foundry, bounded workflow assists and reviewed form extraction/filling
ms.date: 2026-10-11
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

## Observed Feasibility and Parallel Value Experiment (2026-10-11)

Evidence boundary: [PR #58](https://github.com/jmservera/ama/pull/58),
pinned to `5136f192d583a5bf53adeeec4b0f21369b005c9d`, inspected 2026-10-11.
Its [README, Current continuing MVP](https://github.com/jmservera/ama/blob/5136f192d583a5bf53adeeec4b0f21369b005c9d/mvp/README.md)
and [decision-model learning](https://github.com/jmservera/ama/blob/5136f192d583a5bf53adeeec4b0f21369b005c9d/docs/ideas/typesafe-system-one-agent-fit.md)
record real results. These reported observations were inspected, not rerun
by this documentation amendment. They supersede earlier access-blocked
conclusions, not historical result rows.

| Observed learning | Interpretation and remaining proof |
| --- | --- |
| Real Decision 1 selected a source-bound EPC candidate with normalized option probabilities, model/version/usage and Not reviewed status | Narrow closed-set selection is technically feasible. Held-out accuracy, abstention calibration and net benefit are not demonstrated |
| Real GPT-4.1-mini produced a citation-verified catch-up summary | Generative integration works for that example; one supported output does not establish general quality or human review savings |
| Generic cognitive-services host failed; the Foundry services host with `/providers/microsoft/v1/systemone` succeeded | Endpoint/audience/auth conformance was an integration problem, not model infeasibility. [Official API guide](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision), retrieved 2026-10-11, corroborates the provider-specific API |
| Provider optional confidence validates separately from option probabilities | Validate question/answer IDs, types, allowed keys, finite normalized probability vectors and optional fields; never substitute confidence for task probability/runner-up thresholds |
| Actual Azure SQL/Blob deployment retains 60,000 generated stock rows and 980 programme cases | Reuse the continuing application/data lineage. Local fixtures or unrelated model calls are not updated-build acceptance |
| Later work-order controls are source-tested, while recorded deployment is revision `ca-zavaforward-mvp--0000018` | Match source, immutable image, config and deployed revision to each claim. Full permissions/workflow/performance/recovery/human acceptance remains unproved |
| Deployed evidence-support adapter is binary | Binary labels cannot establish supported/contradicted/insufficient macro-F1. Use a separately frozen three-option shadow task or Not evaluated |
| Owner removed the prior inference cap for this rebuild | Preserve scope of approval, source/task/input bounds, SQL upper-liability reservations and usage telemetry; no blanket future spend authorization |

The owner's [subsequent-build direction](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11)
requires actual AI/SQL/Azure for all delivered AMA prototypes/PoCs/MVPs.
At least one in-scope real model task is required, not a winning Decision
model in every task. Clear structured fields should use deterministic
extraction unless comparison demonstrates added semantic-selection value.
Manual access/failure handling remains mandatory; unsupported AI tasks
stay disabled rather than bypassing quality gates.

The owner reports an experiment running in parallel. The available
[MVE protocol](https://github.com/jmservera/ama/blob/5136f192d583a5bf53adeeec4b0f21369b005c9d/.copilot-tracking/mve/2026-10-10/decision-model-value/mve-plan.md)
is proposed design evidence, not verified participant execution or results.
It separates R rules/manual, D Decision/templates, A generative agent and
H agent with Decision tools: A versus D tests narrow replacement; H versus
A tests complementarity; H versus R tests overhead and benefit. A closed
scorer cannot replace free-form generation or accountable reviewers.

Reconcile its 120 grouped families, 30 tuning/30 calibration/60 held-out,
720 dispositions, human adjudicators and counterbalanced full-pack effort
with [PRD experiment intake](../prds/zava-forward-retrofit-programme-demonstrator.md#parallel-decision-model-experiment-intake).
Require version/hash-bound source, split, task, model, prompt/question,
schema and frozen thresholds; exclusions/denominators and failures;
quality/critical errors, coverage/calibration, complete paired human effort,
cost/latency and uncertainty. Data reviews method, Finance cost/effort,
task/control owners placement and the exercise owner adoption. No role-agent
gold labels or simulated human timings. Insufficient labels, people or
precision means Inconclusive/Not evaluated, not demonstrated benefit.

Independent platform/control work can continue without waiting for results.
Value-based task adoption and benefit claims require reviewed evidence; no
automatic control activation or change to human/resident authority. Historical
2026-10-10/September material below retains its retrieval-time meaning.

## Microsoft Decision 1 Reassessment (2026-10-10)

The owner requested reassessment across the process after Foundry model
availability, then specifically requested PRD integration for form
extraction/filling, retrofit subsidy applications and other AI-assisted
decisions. The recommendation is an optional scoring capability inside the
existing bounded task service, not another autonomous agent or replacement
workflow engine. The historical PRD v0.11.0 amendment introduced DD-007/008
and FR-036 to FR-044; the [current PRD candidate](../prds/zava-forward-retrofit-programme-demonstrator.md)
retains conditional task placement with mandatory application-level AI, not a production
selection, deployment result or approved funding process.

### Current Product Evidence and Limits

All sources in this table were checked on 2026-10-10. They are vendor product
documentation, not regulatory authority or Zava North Homes performance
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

### Pricing and Alternatives

The [Microsoft announcement](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/)
advertised USD 0.042 per million input tokens and free output. The
2026-10-10 retrieval of the [Azure Microsoft model pricing page](https://azure.microsoft.com/en-us/pricing/details/ai-foundry-models/microsoft/)
did not establish a regional/subscription rate. Illustrative arithmetic only:
60,000 homes x 20 requests x 1,000 input tokens = 1.2 billion input tokens,
or USD 50.40 at the announcement rate. This is not a workload forecast,
subscription quote or programme budget. Whole-life cost includes
question/context tokens, retries, generation, document processing,
networking, observability, evaluation and human review.

Foundry is the first new integration candidate because it fits the existing
platform, not because it has proved superior quality or cost. Hosted Jev and
self-hosted Kev remain contingencies if approved processing location,
quality or economics favor them, subject to fresh API, licensing, model-card
and operational verification.

### Observed Feasibility, Not Proven Incremental Value (2026-10-10)

The continuing generated-data MVP has now executed real Microsoft Decision 1
inference: a validated source-bound EPC candidate proposal with probability,
version and usage evidence, displayed as Not reviewed. Real GPT-4.1-mini also
produced a citation-verified summary. See the
[Decision 1 behaviour specification](../reference/research/decision-1-behaviour-specification.md). This newer
observation supersedes the deployment/access blockers in the historical
pre-activation assessment below; it does not establish model calibration or
business benefit.

The exercise proves technical feasibility and a bounded review UX, not that
Decision 1 improves decisions or saves effort. No paired manual/rules versus
Decision 1 trial, human-adjudicated held-out accuracy study or measured grant
capture improvement has been completed. Deterministic extraction is preferable
for clear structured fields unless comparison demonstrates incremental benefit.
The defensible tribunal statement is: real inference is integrated; incremental
value remains a hypothesis to test on ambiguous source-selection tasks.

Use the identical held-out case families for manual/parser-rule and assisted
arms. Measure correctness, critical errors, abstention and calibration, total
preparation plus review/correction effort, latency and cost. Freeze task-specific
success and stop criteria before executing the comparison. Automated synthetic
oracles can establish engineering accuracy, but do not stand in for human
adjudication, usability evidence or real company outcomes.

### Evaluation and Activation Gate

The owner's priority on 2026-10-10 is now comparative value before further
MVP expansion. The proposed
[Decision Model Value MVE](https://github.com/jmservera/ama/blob/5136f192d583a5bf53adeeec4b0f21369b005c9d/.copilot-tracking/mve/2026-10-10/decision-model-value/mve-plan.md)
compares rules/manual, Decision-assisted, generative-agent and hybrid paths,
with selection/screening ablations. It retains the PRD 120-family split and
12-pack paired-effort baseline. It is an experiment design, not executed
evidence or authorization to replace agents. Real participant availability
remains required for human-effort findings.

Historical pre-activation assessment follows. Read-only implementation verification on 2026-10-10 found the AMA resource's
model eligibility metadata includes `Microsoft-Decision-1`, format `Microsoft`,
version `1`, with `GlobalStandard` advertised. The returned SKU cost is null:
this is neither a price quote nor verified budget clearance. Deployment
metadata still lists only the existing generative deployments, not Decision 1.
The eligibility response advertises a 2027-02-04 deprecation date; treat it as
an operator review trigger, not a prediction of outage or a legal deadline.
Evidence is the authenticated Azure account `list-models` and `deployment list`
read on that date, not a performed deployment or model call. No resource
creation, billable probe, processing-location approval or model quality is
implied. The [official deployment guide](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision),
source date 2026-10-07, updated 2026-10-09, rechecked 2026-10-10, continues to
distinguish global processing from selected-region data-zone serving.

The local exercise now has tested cross-process SQLite upper-liability
reservations shared by scoring and generation, alongside registry/permission/
terms/price/quota guards. Failed or timed-out calls do not refund reservations;
lowering an environment baseline cannot erase retained liabilities and no
automatic monthly rollover discards them. This conservative engineering control
does not establish actual prices, invoice reconciliation or owner authorization.
Actual deployment/response-schema verification, bounded billable permission
and human-adjudicated evaluation remain mandatory before activation.

Compare manual/templates, parsers/rules, Decision 1 and appropriate
generative alternatives on identical, human-adjudicated held-out cases.
Separate tuning/calibration/test sets by case/building/document family;
measure exact/normalized field accuracy, provenance, unsupported critical
values, omission recall, abstention/calibration, OCR-error propagation,
export fidelity, total preparation/review/correction effort and whole-life
cost. Test ambiguity, option order, negation, mixed intents, unreadable
sources, stale schema/input, restricted sources and source-text injection.

Apply adjudicated labels, separate tuning/calibration/held-out sets and
unflagged-case review to every scoring task, not only forms. Report
calibration/reliability and coverage, differential false negatives and
review delays across lawful relevant evaluation slices, retry/throttle
rates and whole-life cost per correctly handled task. No latent person
profile or aggregate score may conceal a critical miss. The initial
research shortlist is delay-note categorization, documentary
evidence-support/mismatch checks and drafted-communication guardrails;
inbound complaint/pause flags remain shadow-only behind independent first
human triage. Task owners confirm or replace this shortlist before testing.

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

Decision 1 context/token/question/option limits, version-pinning and
retirement behavior, and fine-tuning support were not established by the
accepted sources. Do not inherit Kev's 8,192-token context, TypeSafe
option/confidence limits or generic Foundry Batch/provisioned support.
Validate every expected question ID, answer type, allowed key and finite
probability vector against the actual provider contract, including any
documented normalization requirement. Verify the Entra audience and detect
unavailable or changed model versions; disable the task until regression
passes rather than silently substituting a provider.

Removing names or contact details does not anonymize health/disability
content. Before resident-data use, accountable owners must verify applicable
processing, retention and abuse-monitoring terms, contracts, transfer
position, lawful basis and DPIA. A UK resource or data-zone deployment is
not evidence of UK-only inference. These are unresolved approval checks,
not findings that the deployment or data use is compliant.

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

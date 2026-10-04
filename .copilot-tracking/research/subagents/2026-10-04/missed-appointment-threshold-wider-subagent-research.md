# Cycle 1 / Wave 1 Wider — Missed-appointment escalation thresholds

## Delegated input contract

| Field | Value |
|---|---|
| Cycle / wave | Cycle 1 / Wave 1 — Wider |
| Lane | External UK housing provider, regulator, sector data/policy, and bounded practitioner/forum material |
| Topic | Candidate evidence for repeated missed-resident-appointment escalation thresholds |
| Questions | What published UK housing policies, statistics, datasets, and practitioner commentary define or quantify resident no-access/missed appointments? Do any distinguish cancellation/refusal, contractor non-attendance, or rescheduling? Is a repeat threshold published? |
| Evidence criteria | Preserve exact definition, denominator, date, scope, source type, URL, and retrieval date. Prefer primary sources. Treat forums as anecdotal. Identify gaps and contradictions. |
| Scope | Public UK housing-sector sources and bounded practitioner/forum material only. |
| Non-goals | Do not select a threshold, validate five, infer a sector average, conflate no-access with refusal/cancellation or provider non-attendance, or edit the parent artifact or production files. |
| Research posture | Wider |
| Explicit limit | Bounded source discovery; stop on source redundancy or accessible-source saturation. |
| Wave evidence goal | Find candidate sources and definitions/hypotheses for later parent synthesis, rather than deciding policy. |
| Parent primary artifact (read-only) | `.copilot-tracking/research/2026-10-04/missed-appointment-threshold-research.md` |
| Lane-artifact preflight | Confirmed before this write: this file is under `.copilot-tracking/research/subagents/2026-10-04/` and is distinct from the parent primary artifact. |

## Status

Finalized 2026-10-04. This lane records evidence and gaps for parent synthesis only; it makes no policy decision.

## Research log

| Action | Result / next action |
|---|---|
| 2026-10-04 — created delegated artifact after path preflight | Search public primary sources first; record only source-supported distinctions and measures. |
| 2026-10-04 — reviewed RSH Tenant Satisfaction Measures (TSM) technical requirements | Located the national England regulatory measure set. It includes repair satisfaction/time-to-complete and a target-timescale measure, but no listed resident-no-access or repeated-missed-appointment TSM. |
| 2026-10-04 — reviewed Housing Ombudsman resident repairs support material | Located primary guidance requiring residents to allow access and setting expectations for reasonable notice and repair appointments. It supplies no numerical no-access denominator, observed rate, or repeat-escalation count. |
| 2026-10-04 — searched for provider policies, public performance data, and practitioner/forum material | Search endpoints returned CAPTCHA, irrelevant results, or no accessible attributable candidate. No forum assertion is recorded as evidence. This is an access/discovery limit, not evidence that sources do not exist. |

## Findings

### F1 — The England regulatory core performance set does not standardise resident no-access or repeat thresholds

* **Question answered:** Is there a regulator-published sector measure that can supply a comparable denominator, rate, or repeated missed-resident-appointment threshold?
* **Source type / scope / date:** Primary regulator technical requirements, England, published 2023-03-23 and last updated 2026-06-11; retrieved 2026-10-04.
* **Source:** [Regulator of Social Housing, *Tenant Satisfaction Measures – Technical requirements*](https://www.gov.uk/government/publications/tenant-satisfaction-measures-technical-requirements).
* **Evidence (fact):** The document describes the TSMs as the core performance measures all relevant registered providers must calculate and publish. Its published summary lists repair-related TSMs as satisfaction with repairs (TP02), satisfaction with time taken for the most recent repair (TP03), and repairs completed within target timescale (RP02). It does **not** list a resident no-access/missed appointment measure, a cancellation/refusal measure, contractor/provider non-attendance, rescheduling, or a repeat-miss threshold.
* **Definition / denominator:** This source supplies names of standard measures, not a no-access definition or no-access denominator in the material reviewed. The individual repair measures are not interchangeable with a resident no-access count.
* **Relationship:** **Weakens** any claim that a nationally standardised England sector figure or repeat threshold is available from the mandatory TSM core set. **Leaves unresolved** whether individual providers publish compatible additional measures; the source expressly permits additional provider measures.
* **Confidence:** High for the bounded claim about the listed core TSMs; low for any inference about provider-specific data.

### F2 — Ombudsman guidance distinguishes the access obligation from service delivery but supplies no threshold or observed rate

* **Question answered:** Does a primary sector oversight source define resident access and establish a repeated missed-appointment escalation threshold?
* **Source type / scope / date:** Primary Housing Ombudsman resident support guidance; UK social-housing complaint context; page date not stated in retrieved material; retrieved 2026-10-04.
* **Source:** [Housing Ombudsman Service, *Repairs and property condition support guide*](https://www.housing-ombudsman.org.uk/centre-for-learning/learning-hub/knowledge-and-information-management/).
* **Evidence (fact):** The guidance says residents “must allow landlords access” to complete repairs and that a landlord “may be able to seek an injunction” if access is not allowed. Separately, it says landlords should give reasonable notice of repair appointments and a schedule of works; it identifies actions or behaviour of a landlord’s contractors as a potential complaint subject.
* **Definition / denominator:** “Do not allow access” is the source's resident-access concept. The guide neither defines an operational no-access event nor states a denominator, period, observed frequency, cancellation/refusal rule, rescheduling rule, contractor/provider non-attendance definition, or a number of occurrences for escalation.
* **Relationship:** **Supports** preserving resident failure to allow access as distinct from landlord/contractor conduct and from appointment notice. **Leaves unresolved** all numerical threshold and measurement questions.
* **Confidence:** Medium: direct primary guidance, but it is general resident guidance rather than a performance-reporting specification.

## Cross-source distinctions and evidence relationships

| Delegated question | Evidence relationship | Provenance | Status |
|---|---|---|---|
| Is there a comparable regulator denominator/rate for resident no-access? | F1: the listed mandatory TSM core set contains repair outcomes/satisfaction, not a no-access measure. This weakens use of TSM results as a no-access sector average. | RSH TSM technical requirements URL; F1 | Supported (bounded) |
| Does primary oversight guidance set a repeat count? | F2: it requires access and discusses notice, but gives no count, rate, or escalation threshold. | Housing Ombudsman support-guide URL; F2 | Unresolved |
| Can resident no-access be combined with refusal/cancellation, provider non-attendance, or rescheduling? | Neither source supplies a common operational definition or denominator across these categories. F2 keeps resident access separate from landlord/contractor conduct; F1's repairs measures do not bridge the categories. | F1; F2 | Unresolved; do not combine |
| Is there provider-policy or forum evidence for a candidate repeat count? | No attributable accessible provider policy, dataset, or forum item met the required provenance/definition criteria during this bounded discovery pass. | Research log, 2026-10-04 | Missing evidence, not negative proof |

## Gaps and conflicts

1. No located source supplies an observed UK housing-sector rate of resident no-access, a compatible denominator, or a published repeated missed-resident-appointment threshold.
2. No located source defines a mutually exclusive taxonomy for: resident no-access; resident cancellation/refusal; contractor/provider non-attendance; and rescheduling. A follow-up would need provider-level operational policy plus performance data with event-level definitions and reporting period.
3. No conflict was identified between the two primary sources. Their different purposes (mandatory regulator measures versus resident-facing complaint guidance) mean neither can validate a provider escalation count.
4. Practitioner/forum commentary was intentionally not elevated: no attributable item with sufficient context was recovered. Any future item remains anecdotal and cannot establish a sector rate or threshold.

## Parent-synthesis pointers

* Use F1 only to establish the bounded absence of a **mandatory TSM core** no-access measure; do not extend it to a claim that no provider tracks no-access.
* Use F2 only for the access/service-delivery distinction; it does not establish an escalation mechanism or numerical trigger.
* Preserve separate data fields for the four requested event categories until a source supplies explicit inclusion/exclusion and denominator rules.

## Stop decision

**Stop reason:** accessible-source saturation and search access boundary within the explicit bounded Wider lane. Primary regulator and Ombudsman sources supplied definitional/performance-framework evidence; repeated discovery attempts did not yield attributable provider policies, comparable datasets, or credible forum material. Further searching through the blocked/irrelevant endpoints was likely redundant. This lane does not conclude that a threshold is supported or unsupported beyond the evidence relationships above.

## Final status

* **Execution status:** Partial — two primary sources captured; requested provider-policy/data/forum breadth not recovered with adequate provenance.
* **Evidence confidence:** Medium — high for F1's limited measure-set observation, medium for F2's general guidance, unavailable for a numerical threshold.
* **Synthesis readiness:** Needs more evidence — suitable to inform distinction and data-gap handling, not a numeric-threshold assessment.

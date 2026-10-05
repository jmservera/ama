<!-- markdownlint-disable-file -->

# Task Research: missed-appointment-threshold

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-10-04                                                               |
| Researcher / agent | rpi-research                                                             |
| Status             | Complete for public evidence; operational decision pending              |
| Artifact path      | .copilot-tracking/research/2026-10-04/missed-appointment-threshold-research.md |

## Research Brief

* What to research: Find UK housing-provider statistics, policies, published datasets, and credible forum or practitioner discussion about missed appointments, failed access, repeated visits, and escalation thresholds.
* Why it matters: The owner directed that the BRD make the missed-appointment trigger configurable, with a current default of five, pending stronger evidence. Research should test whether comparable evidence supports that default or suggests safer distinctions.
* Audience or intended use: Project owner, Executive Reviewer role profile, and Housing/Repairs/Resident Engagement owners validating draft RULE-006 and AC-025.
* Scope: UK social housing and closely comparable housing repairs/property-maintenance services; resident and contractor missed appointments, repeated no-access events, escalation policies and statistics.
* Non-goals: Do not decide company policy, infer Proper North Homes performance, authorize live use, or make legal determinations. Do not recommend treating failed access as refusal or delaying hazard response.
* Criteria: Prefer primary housing-provider/regulator/public-sector data and published policies; distinguish resident no-access from landlord/contractor non-attendance; identify denominators, time periods, definitions, sample limitations and source dates; use forum material only as anecdotal context.
* Requested outputs: Evidence synthesis on whether five missed appointments is supported as a default, comparable statistics or policy examples, caveats, and minimum evidence needed to retain or change the configurable default.
* Output mode: analysis

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | What comparable statistics or policies exist for repeated missed appointments/no-access in UK housing? Does evidence support a trigger at more than five missed resident appointments, and what distinctions should govern escalation? |
| Codebase scope | BRD RULE-006/AC-025; current sector baseline, company role research and pilot measurement challenge |
| External scope | Open web, prioritizing UK housing providers, regulators, Ombudsman, local authorities and sector bodies; practitioner/forum material is secondary |
| Initial internal candidate areas | `docs/brds/agentic-retrofit-programme-brd.md`; `docs/reference/research/sector/uk-social-housing-baseline-research.md`; `docs/reference/research/company/agent-request-challenge.md`; `docs/reference/research/company/pilot-measurement-challenge.md` |
| Initial external candidate areas | Housing-provider repairs/access policies and annual reports; regulator and Ombudsman publications; local authority housing repairs statistics; sector/practitioner forum discussions |
| Research posture | balanced |
| Posture provenance | default, informed by the user's bounded question and request for comparable evidence |
| Explicit limits / deadline | none |
| Posture-specific completion basis | Cover the question with credible, traceable evidence; stop when sources are redundant and remaining company-specific questions cannot be resolved publicly |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | No private systems, personal data, or unverified company records. Forums are anecdotal, not representative statistics. No source can authorize the Proper North Homes threshold. |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | `copilot-tracking.instructions.md` | `applyTo` matches `.copilot-tracking/research/**` | Tracking artifact structure and evidence ownership | Selected |
| Skill | `rpi-research` | User requested new evidence research; skill loaded | Dated primary artifact, three-wave process, evidence IDs and read-only scope | Selected |
| Skill | `requirements-author` | BRD topic | Requirement and gate context only | Selected as existing context; no BRD edits in research phase |
| Skill | housing / retrofit research skills | Topic-adjacent | Could add domain criteria | Skipped; repository role profiles and primary public sources are sufficient for this bounded question |
| Research specialist | `hve-core-all:rpi-researcher` | Stable name available; independent external evidence lane | Return evidence relationships and provenance only; no decisions | Selected for Wave 1 external source discovery |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
|---|---|---|---|
| Intake | Is the relevant trigger configurable, and what default should be used now? | Owner: make the number configurable, with a default of 5 until stronger evidence is available. | Research comparable statistics/policies; treat five as owner-directed provisional default, not a validated sector standard. |
| Threshold semantics | Should five trigger at the fifth eligible event, or only after the count exceeds five? | Owner: preserve existing behavior; escalate after more than five (the sixth event). | Record configured value 5 and comparator `>` separately; do not interpret this as evidence for the value. |
| Counted event | Which events count toward the threshold? | Owner: count only a confirmed appointment where the resident did not provide access; record provider no-shows, cancellations and reschedules separately. | Only a human-confirmed resident no-access event contributes; maintain separate event categories and do not infer refusal or non-cooperation. |
| Counting window | How should same-case events expire or reset? | Owner: count only while the case is active; reset the counter when a human closes the case. | Record the active-case window and human-closure reset; retain the event history for audit. Company ratification remains open. |
| Direction change | None required; scope and use are clear. | N/A | Proceed in balanced analysis mode. |
| Convergence | To be considered after the three research waves. | Pending | Decide whether additional targeted research could materially change the evidence state. |

## Scope and Success Criteria

* Scope: Public evidence about repeated missed appointments and no-access in housing repairs or closely comparable home services.
* Assumptions: Terms such as “missed appointment,” “no access,” “failed access,” and “no-show” may refer to different parties and events; verify each source's definition.
* Success criteria:
  * Every material claim has a source and evidence ID.
  * Resident non-access and provider/contractor non-attendance are reported separately.
  * Statistics state denominator, period and limitations.
  * The research does not promote forum anecdotes into sector rates.
  * The threshold remains a decision for the owner and accountable Housing/Repairs functions.

## Task Research Requests

* Explicit requests: Find comparable company statistics, data, and forum comments about similar situations; assess the owner-directed configurable default of five.
* Inferred research questions: Are escalation policies common? Are thresholds evidence-based? What causes or safeguards should be considered before repeated failures are attributed to residents?
* Caller constraints and non-goals: Research only; do not change the BRD or choose company policy during this phase.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|---|---|---|---|
| add | Make the missed-appointment number configurable | User answer | Research whether comparable evidence supports a default; investigate ownership/versioning only as policy evidence, not implementation design |
| change | Retain default value 5 for now pending better evidence | User answer | Treat as a provisional owner decision, not a validated benchmark or approved operational rule |
| clarify | Preserve the current strict-greater-than comparator, so five is the stored threshold and human review begins after more than five eligible events | User answer | Resolve count semantics; default remains provisional and subject to Housing/Repairs ratification |
| narrow | Count only a confirmed appointment where a resident did not provide access; record provider no-shows, cancellations and reschedules separately | User answer | Revalidate the active event categories; public sources support distinction but do not validate local classification or threshold |
| clarify | Count eligible events only while the same case is active; reset the count only when a human closes the case | User answer | Record the counting window/reset direction; retain event-level audit history and leave company ratification open |
| narrow | Focus on comparable UK housing and closely similar home-repair services | User request | Exclude unrelated appointment domains unless useful as clearly marked contrast |
| exclude | No legal or operational approval conclusions | User context and repository controls | Route company approval to Housing/Repairs and resident validation |

## Research Questions

| # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
|---:|---|---|---|---|
| Q1 | What published UK housing statistics measure missed appointments/no-access, and what do they count? | breadth | H | answered with comparability limits |
| Q2 | What comparable provider policies or escalation triggers exist, and are numeric thresholds evidence-based? | breadth | H | answered: no verified common threshold |
| Q3 | What credible practitioner/forum accounts illuminate repeated access failures or fair escalation? | breadth | M | answered with one low-confidence private-landlord anecdote and resident-panel context |
| Q4 | Does the evidence support five as a default, or only as an owner-selected provisional value pending company data? | depth | H | answered: public evidence does not validate five |

## Prior Knowledge Gate

* Existing artifacts reviewed: BRD v0.11.0 RULE-006/AC-025 and OD-08/OD-09; sector baseline research; agent-request challenge; pilot measurement challenge; role-panel record.
* Reused (verified) findings: Repository research states no defensible UK social-housing average was identified for no-access, resident refusal or missed appointments; it retains planning assumptions of 10% first-appointment no-access and 5%-10% refusal/withdrawal, explicitly to be replaced with company data. BRD requires human review and no automatic refusal classification.
* Superseded / stale: None for the question. Existing sector assumptions are context, not evidence for a repeated-appointment threshold.

## Research Cycle Log

### Cycle 1

* Active direction controls: configurable threshold; default five is provisional; resident and contractor events remain distinct.
* Active research posture and completion basis: balanced; cover credible public statistics, policies and bounded practitioner evidence; avoid redundant examples.
* Explicit limits or deadline effect: none.

#### Wave 1: Wider

* Plan and independent lanes: Search sector/provider/regulator data and published policies; a bounded researcher lane is discovering candidate sources and reporting provenance. Inline review mapped existing repository evidence.
* Worker evidence relationships or inline fallback: The `hve-core-all:rpi-researcher` lane completed partially and stopped at accessible-source saturation; its artifact is `.copilot-tracking/research/subagents/2026-10-04/missed-appointment-threshold-wider-subagent-research.md`. It found primary RSH and Housing Ombudsman evidence on missing standard measures/thresholds and distinctions between resident access and service delivery. Parent inline search additionally found a sponsored 74-organisation survey, one provider's annual no-access figures, a housing-sector executive roundtable, a resident panel report, a council no-access policy and public forum posts.
* Reflection: The lane could not recover attributable provider/forum sources within its access boundary; this is not evidence those sources do not exist. Parent sources measure different things. Survey bands are organisation-reported missed-appointment rates; provider and roundtable figures concern no-access events; policy steps count contact attempts for specified compliance checks. These cannot be pooled or converted into a repeated-resident-miss threshold.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Verify sample size and self-report limits in the sector survey; calculate the single-provider no-access rate against its stated visit denominator; inspect whether the three-attempt policy applies to missed repair visits or separately to compliance contact; verify resident-panel sampling caveats.
* Plan and independent lanes: Verify accessible source text and policy wording inline. Council policy PDF text was extracted with pypdf after web fetch returned binary data; no PDF or source file was saved in the workspace.
* Worker evidence relationships or inline fallback: Parent inline evidence; the Wider lane found that the RSH's mandatory TSM core contains repair outcomes/satisfaction but no no-access or repeated-miss measure, while Ombudsman resident guidance provides no rate or numeric trigger (lane F1-F2; see W7-W8).
* Reflection: There are comparator statistics and staged-contact examples, but none validates five consecutive resident no-access appointments. One local authority's three contact attempts apply to statutory compliance checks; its repairs section does not specify a numeric trigger. Resident-panel findings highlight barriers and accessibility concerns, supporting investigation before assigning cause.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Test whether any observed rate or policy supports five; distinguish contact attempts from missed appointments, resident no-access from provider no-show, and ordinary repairs from statutory/safety cases; look for evidence that a numeric trigger could misclassify resident barriers or delay urgent action.
* Plan and independent lanes: Compare primary-provider and public-sector evidence against sponsored survey and anecdotal forum material; examine how emergency and compliance routes differ.
* Worker evidence relationships or inline fallback: Parent inline contrarian review; the Wider lane's regulator and Ombudsman findings independently leave any repeat threshold unresolved (lane F1-F2; see W7-W8).
* Reflection: Evidence challenges use of one undifferentiated count. The policy example separates compliance and ordinary repairs and has a separate emergency route; the resident panel documents access/logistics and accessibility barriers. These sources do not establish a better universal count, but they weaken the case for interpreting every failed appointment as resident fault or using a count to gate urgent action.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|---|---|---|---|---|
| A default of five is supported by comparable sector evidence | C1-C4; W1-W8 | rejected | Available evidence measures rates, policies or experiences but does not test or validate a five-appointment trigger. | Record five as provisional owner direction only, not a sector standard or proven threshold. |
| Appointment/no-access statistics can be compared directly across providers | W1-W3 | rejected | Definitions, denominators, publication methods and populations differ; survey data is self-reported and sponsored, provider examples are single-organisation disclosures, and roundtable figures are not a representative sample. | Report source-specific context and do not pool rates. |
| Repeated failures can be escalated using one count without examining cause or risk | W3-W5 | rejected | The council procedure distinguishes statutory checks, routine repairs and emergencies; resident evidence identifies access, communication and disability barriers. | Preserve human cause investigation, resident engagement and separate urgent/safety response. |
| A public sector-wide numeric trigger should replace five | W1-W5, W7-W8 | deferred | No verified cross-provider evidence establishes a common threshold for repeated repair no-access. | Leave threshold approval to Housing/Repairs using company records and resident review. |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no, for the bounded public-evidence question.
* Trigger or stop basis: Three waves found no comparable evidence validating a repeated-miss value; more public-source examples are unlikely to resolve Proper North Homes' own appointment definitions, baseline or policy approval.
* Revised brief or revalidation required: no. Re-enter only if company appointment data, a directly comparable multi-provider dataset, or accountable Housing/Repairs direction becomes available.
* Readiness effect: Research can close with the answer that public evidence does not validate five; the operational decision remains Not ready pending local evidence and approval.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | Repository baseline explicitly says no defensible UK social-housing average was identified for no-access, refusal, or missed appointments; existing rate assumptions are planning assumptions only. | `docs/reference/research/sector/uk-social-housing-baseline-research.md:186-195` | read | high | The file labels the values as assumptions and directs replacement with company records. |
| C2 | Failed access must not be treated automatically as resident refusal; RULE-006/AC-025 now specifies configurable default five, strict `>`, verified resident no-access at confirmed appointments, separate excluded event types and active-case counting with human-close reset. | `docs/brds/agentic-retrofit-programme-brd.md:1122` | read | high | v0.12.0 records owner direction; Housing/Repairs ratification and company evidence remain open. |
| C3 | Owner direction requires actual 12-month records by reason, party, channel and adjustment need; OD-08/OD-09/OD-40 remain open. | `docs/brds/agentic-retrofit-programme-brd.md:445,469,1459-1491` | read | high | Company-specific baseline is unavailable in repository. |
| C4 | Role research warns that scheduling software does not create installers and that Proper North Homes' actual no-access/refusal rates are unknown. | `docs/reference/research/company/agent-request-challenge.md:243-244` | read | high | Sector-informed hypothesis, not company evidence. |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|---|---|---|---|---|---|---|
| W1 | An Inside Housing/Localz sponsored survey of 74 housing organisations reported 63% saying up to 10% of their repairs/maintenance appointments were missed, and nearly 20% reporting 10-20%; it does not identify repeated resident no-access counts. | Counting the cost of missed repairs appointments - Inside Housing | https://www.insidehousing.co.uk/sponsored/counting-the-cost-of-missed-repairs-appointments | 2026-10-04 | Publication date not exposed in retrieved page | medium |
| W2 | Aspire Housing reported 10,457 no-access events across 81,830 home visits for Apr 2025-Mar 2026 (about 12.8%); its page excerpt does not provide repeated-event thresholds or event-level definitions. | No access - Aspire Housing | https://www.aspirehousing.co.uk/you-and-your-home/myhome/myhome-summer-26/no-access/ | 2026-10-04 | Apr 2025-Mar 2026; indexed search excerpt (direct fetch returned 403) | medium |
| W3 | A housing-sector executive roundtable reported responsive-repair no-access rates of 1-10% and stock-condition survey rates up to 30-40%, but did not provide sample size, denominator, source data or a repeated-miss threshold. | Rethinking No Access in UK Social Housing - Neemar Search | https://www.neemarsearch.com/insights/rethinking-no-access-in-uk-social-housing/ | 2026-10-04 | Publication date not exposed in retrieved page | low |
| W4 | An England resident panel online community found access/logistics, communication, accessibility and other repair barriers; 62% of those requesting hazard repairs reported barriers and 45% said repair timing was unreasonable. The report says the activity is not statistically representative. | Repairs, maintenance and Awaab's Law: Resident Panel report - GOV.UK | https://www.gov.uk/government/publications/social-housing-resident-panel-reports-2022-to-2023/repairs-maintenance-and-awaabs-law-resident-panel-report-accessible-version | 2026-10-04 | Wave 2 online community, May 2023; report published 2023 | high for reported panel findings; not population estimates |
| W5 | Stevenage Borough Council's Aug 2024 policy specifies three contact attempts for statutory compliance checks followed by in-house support and a final council attempt; ordinary repairs have no stated numeric count, and emergencies have a separate route. The policy's approval field is blank. | No Access Policy - Stevenage Borough Council | https://www.stevenage.gov.uk/documents/housing/policies-and-strategies/no-access-policy.pdf | 2026-10-04 | Created Aug 2024, version 1; approval not recorded in document | high for wording; limited comparator authority |
| W6 | A public landlord forum thread records an individual landlord's concern about costs when residents cancel or miss appointments; it is a private-landlord anecdote, not social-housing evidence or representative statistics. | Tenants missing pre-arranged appointments with trades - MoneySavingExpert Forums | https://forums.moneysavingexpert.com/discussion/6403388/tenants-missing-pre-arranged-appointments-with-trades | 2026-10-04 | Thread post date not captured in retrieved content | low |
| W7 | England's mandatory TSM core standardizes repair satisfaction, time taken and completion within target, but does not list resident no-access or repeat-miss measures; providers may publish additional measures. | Tenant Satisfaction Measures - Technical requirements - Regulator of Social Housing | https://www.gov.uk/government/publications/tenant-satisfaction-measures-technical-requirements | 2026-10-04 | Published 2023-03-23; updated 2026-06-11 | high |
| W8 | Housing Ombudsman resident repairs guidance distinguishes resident access expectations from landlord notice/appointment duties and contractor conduct; it supplies no no-access rate, denominator or repeat threshold. | Repairs and property condition support guide - Housing Ombudsman Service | https://www.housing-ombudsman.org.uk/centre-for-learning/learning-hub/knowledge-and-information-management/ | 2026-10-04 | Page date not stated in lane evidence | medium; primary source, general guidance |

### Contradictions / Conflicts

* W1's sponsored survey reports organisation-level bands for missed appointments, while W2 is a provider's no-access count and W3 describes roundtable estimates. Definitions, samples and denominators differ; no pooled or benchmark rate is justified.
* W5's three contacts are specifically for booking statutory compliance checks, not a rule that three missed routine-repair appointments should trigger enforcement. Its ordinary repairs section says continually denied access or appointments not kept may prompt injunction consideration, without a count.
* W4 contains qualitative and panel percentages, not representative prevalence. It supplies resident-impact counterevidence to simplistic attribution, not an appointment threshold.
* W7 establishes only that no no-access/repeat-count measure appears in the mandatory TSM core; it explicitly does not establish that individual providers never collect or publish such data.
* W8 supplies service and access expectations, not a numeric threshold or an observed rate.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|---|---|---|---|---|
| Q1 | Published sources provide provider-specific or survey-band measures, but definitions and representativeness vary. | C1; W1-W3 | medium | Do not claim a UK housing-sector average or pool rates. |
| Q2 | One council example has a staged three-contact process for statutory compliance booking; it does not set a fixed repairs no-access count. | W5 | high | Do not translate a compliance-contact sequence into the BRD's repair threshold. |
| Q3 | Public forum posts evidence individual landlord concerns about appointment costs; resident-panel evidence records repair access and service barriers. | W4, W6, W8 | low for forum anecdotes; high for panel report facts | Use anecdotes only as context; retain resident impact review. |
| Q4 | No evidence reviewed validates five as a threshold for repeated resident no-access. | C1-C4; W1-W8 | high for bounded reviewed sources | Keep default five as an owner-directed provisional value only; company data and Housing/Repairs approval remain necessary. |

## Key Discoveries

* The public evidence found is not a defensible sector-wide standard. A sponsored 74-organisation survey reports broad missed-appointment bands; a housing provider reports a 12.8% no-access rate for its own visits; a consultancy roundtable offers non-representative ranges. The RSH's mandatory England TSM core and Housing Ombudsman resident guidance contain no comparable no-access denominator or repeat trigger, but providers may collect additional measures.
* The council policy's three contact attempts address statutory compliance checks, not a universal repeated-missed-repair trigger; ordinary repairs and emergencies are treated separately.
* Five remains the owner's configurable provisional default, not an evidence-backed or legally required sector value.
* Resident-panel findings and forum anecdotes support distinguishing access barriers and provider no-shows from resident conduct; they cannot estimate company rates.

## Decision State

* State: proposed comparison outcome.
* Rationale: Research can inform whether the owner-directed default is plausible but cannot establish company rates or approve a service trigger.
* Evidence refs: C1-C4.
* Next owner or trigger: Owner directed a configurable default of five; Housing/Repairs must validate against company appointment history and resident barriers before live use.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: Housing/Repairs must ratify the owner-directed provisional rule after reviewing company event data; company event records and operational approval remain unavailable.
* Important: Company appointment data by cause, party, channel, adjustment, property and time period is not supplied.
* Follow-up: Housing/Repairs and Resident Engagement should test fairness and usability with real cases/residents.
* Residual uncertainty: Public sources may use non-comparable definitions; forum discussion is anecdotal and cannot establish prevalence.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|---|---|---|---|---|---|
| Make the missed-appointment threshold configurable with default five pending stronger evidence | confirmed | user | Explicit direction; threshold is not a sector standard and does not authorize live use | C1-C4; W1-W8 | Preserve five as provisional default; require review/versioning by accountable owners before live use |
| Escalate only when verified resident no-access outcomes for confirmed appointments exceed the configured value; preserve provider no-show, cancellation and reschedule as separate outcomes | confirmed | user | Explicit direction; sources show categories are not interchangeable but do not validate this company's count | C2; W4-W5; W7-W8 | Default value 5 with strict-greater-than comparator means the sixth eligible event triggers human review; Housing/Repairs ratification and company data remain required |
| Count eligible events only while the same case is active and reset the counter only upon human case closure | confirmed | user | Explicit direction; a closed-case reset is a draft behavior, not evidence of a company standard | C2; W4-W5; W8 | Preserve historical events for audit; Housing/Repairs must ratify the case and closure rules before operational use |

## Company Role-Profile Challenge

The user requested a focused review of the updated control by company-role
profiles, especially the Executive Reviewer. These are simulated research
perspectives grounded in repository materials, not actual employee statements,
resident evidence or company approvals.

| Profile | Assessment | Remaining owner / evidence |
|---|---|---|
| Executive Reviewer | Initially returned `CHANGES_REQUESTED` because the BRD wording did not state the configurable default, strict `>` comparator, eligible event definition or excluded event outcomes. Follow-up review found the user-defined semantics resolved in v0.12.0 and requested that event history and the threshold/configuration version remain auditable after counter reset; RULE-006/AC-025 now state this. Public evidence does not validate five. | Housing/Repairs must validate company event records; OD-09/OD-40 retain service handoff and configuration/change authority. |
| Asset Executive | Supported five only as a provisional human-review trigger; requested reliable event history, named service ownership and protection against adverse treatment based on count alone. | Housing/Repairs and Resident Engagement review; company baseline and authority remain unknown. |
| Resident Engagement | Supported human investigation only. Recommended verified records, accessible notice and adjustment checks, correction and complaint routes, data minimisation, and a separate urgent-hazard path. No resident research evidence was supplied. | Resident Engagement and Housing/Repairs; DPO review where processing requires it. |
| Retrofit Programme Manager | Considered the sixth-event trigger expressible operationally with distinct outcome codes, event provenance, active-case count, human-close reset and a staffed handoff. No technical choice for the owner remains. | Housing/Repairs ratification and company records; Programme/Digital to document configuration control after approval. |

The earlier Executive Reviewer `CHANGES_REQUESTED` disposition applied to the
previous incomplete draft wording. It did not reject the owner's now-clarified
draft semantics, ratify company policy, close an open decision or authorize
live use.

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|---|---|---|---|---|
| Ratify threshold, event codes, active-case window and human-close reset for operational use | Company appointment history with cause/party distinctions, resident/adjustment review, and Housing/Repairs approval | Housing/Repairs; Resident Engagement review | Resident service and escalation policy | important |
| Define configuration ownership and governance | Named policy/configuration owner, change approval/version/audit requirements; no technical choice is delegated to the owner | Housing/Repairs with Programme/Digital | Operational control | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|---|---|---|---|---|---|
| H | Obtain company-specific appointment outcomes by event cause, responsible party, adjustment need and rescheduling status | Establish an operational baseline without conflating distinct events | Before approving or using a live threshold; owner direction requires further evidence | yes; accountable functions must supply and validate records | Q1-Q4; C1-C4; W1-W8 |

## Planning Readiness

* Status: Not ready.
* Decision state: Five is a user-directed provisional default, not an evidence-backed operational threshold.
* Evidence basis: C1-C4; W1-W8.
* Preconditions met: Scope and owner direction recorded.
* Blockers: No company baseline or approved operational definition; Housing/Repairs ratification, Resident Engagement review, named configuration authority and handoff ownership remain necessary. Owner direction now resolves the draft comparator, event categories and active-case reset, but does not approve live use.
* Smallest action to change readiness: Review actual company appointment records with the accountable owners and ratify the event definition, threshold, case lifecycle and service handoff.

## Closeout Record

| Field | Record |
|---|---|
| Research execution status | Complete for the bounded public-evidence question; delegated Wider lane completed partially |
| Completed waves | Parent Wider, Deeper and Contrarian waves completed; delegated Wider lane stopped partially at accessible-source saturation |
| Lane evidence or inline fallback | Parent inline evidence plus `hve-core-all:rpi-researcher` findings F1-F2 at `.copilot-tracking/research/subagents/2026-10-04/missed-appointment-threshold-wider-subagent-research.md`; lane limitation: no attributable provider-policy, dataset or forum item recovered |
| Research disposition | executed |
| Planning Readiness | Not ready |
| Blockers | Company-specific validation and owner/role approval remain |
| Continuation owner and state | user; research-only closeout pending |

## Advisory Next Step

| Field | Record |
|---|---|
| Research disposition | executed |
| Planning Readiness | Not ready |
| Output mode and planning support | analysis; no planning handoff until evidence and company approvals exist |
| Acting owner | user |
| Required gates or confirmations | Housing/Repairs threshold and case-lifecycle approval, company records and resident-impact review pending |
| Continuation result | explicit no-handoff reason: public evidence does not validate five; company evidence and approval belong to accountable owners |
| Primary evidence file | .copilot-tracking/research/2026-10-04/missed-appointment-threshold-research.md |
| Notes for planning or re-entry | Public evidence does not validate five. Before operational approval, obtain the company baseline and explicit Housing/Repairs decision on the owner-directed comparator, event categories, active-case reset and configuration governance. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Parent inline Wider, Deeper and Contrarian waves are synthesized; the delegated Wider lane completed partially and documented its access boundary. Company-specific validation is outside this public research scope.

## Sources

* W1 - Counting the cost of missed repairs appointments - Inside Housing - https://www.insidehousing.co.uk/sponsored/counting-the-cost-of-missed-repairs-appointments (retrieved 2026-10-04; publication date not exposed).
* W2 - No access - Aspire Housing - https://www.aspirehousing.co.uk/you-and-your-home/myhome/myhome-summer-26/no-access/ (retrieved 2026-10-04; Apr 2025-Mar 2026 figures; direct fetch returned 403).
* W3 - Rethinking No Access in UK Social Housing - Neemar Search - https://www.neemarsearch.com/insights/rethinking-no-access-in-uk-social-housing/ (retrieved 2026-10-04; publication date not exposed).
* W4 - Repairs, maintenance and Awaab's Law: Resident Panel report - GOV.UK - https://www.gov.uk/government/publications/social-housing-resident-panel-reports-2022-to-2023/repairs-maintenance-and-awaabs-law-resident-panel-report-accessible-version (retrieved 2026-10-04; Wave 2 online community, May 2023).
* W5 - No Access Policy - Stevenage Borough Council - https://www.stevenage.gov.uk/documents/housing/policies-and-strategies/no-access-policy.pdf (retrieved 2026-10-04; created Aug 2024, version 1).
* W6 - Tenants missing pre-arranged appointments with trades - MoneySavingExpert Forums - https://forums.moneysavingexpert.com/discussion/6403388/tenants-missing-pre-arranged-appointments-with-trades (retrieved 2026-10-04; thread post date not captured).
* W7 - Tenant Satisfaction Measures - Technical requirements - Regulator of Social Housing - https://www.gov.uk/government/publications/tenant-satisfaction-measures-technical-requirements (retrieved 2026-10-04; published 2023-03-23, updated 2026-06-11).
* W8 - Repairs and property condition support guide - Housing Ombudsman Service - https://www.housing-ombudsman.org.uk/centre-for-learning/learning-hub/knowledge-and-information-management/ (retrieved 2026-10-04; page date not stated).

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free.
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued, including the later active-case reset clarification.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: intake, research brief, parameters, extension registry, participation, direction controls, questions, prior-knowledge gate, all three parent-inline waves, evidence, findings, role-profile challenge, synthesis and readiness.
* Missing or limited sections: delegated Wider lane was partial because attributable provider/forum sources were not recovered within its search boundary; parent research separately recovered limited provider statistics, a council policy and one forum post. Public statistics have comparability and provenance limits; local company data and approval remain unavailable.

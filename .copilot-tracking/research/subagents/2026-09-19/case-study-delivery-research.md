<!-- markdownlint-disable-file -->

# Case Study 48 Delivery Roadmap Research

## Research status

Status: Complete for planning handoff, with material company and presentation
inputs still explicitly unknown.

Research date: 2026-09-19.

Scope: 2026-09-19 is planning day zero. A fixed 85-calendar-day delivery
roadmap runs from 2026-09-20 through 2026-12-13 inclusive, with one dedicated
working day in each of 12 execution windows, ending in a one-hour C-suite
presentation. The roadmap covers
the opening 10-minute pitch, high- and medium-level architectures, trade-offs,
synthetic data, fictional role-agent interviews, an optional demonstration,
feedback-driven resets and schedule buffer.

`docs/case_study_48.md` is not present. The source record is
`docs/case_study_48_original.md`, supplemented by
`docs/case_study_48_addendum.md` and the draft BRD.

## Executive research conclusion

The strongest C-suite proposition is not "approve five agents." It is:

> Approve a capped readiness and shadow-pilot decision to establish the binding
> retrofit-flow constraint and test whether a governed portfolio control plane,
> with deterministic controls and bounded AI assistance, improves safe,
> resident-accepted, evidence-complete handovers.

This is consistent with the addendum's explicit recommendation to approve
readiness and a pilot, not a five-agent rollout or unsecured grant assumption
(`docs/case_study_48_addendum.md:338-342`). The presentation should make the
investment decision easy to understand while showing that the team knows what
not to automate.

With only about 12 focused work sessions available, the credible output is an
evidence-backed executive proposition, architecture pack, options appraisal,
synthetic evidence scenario and optionally a tightly bounded demonstrator. It
is not a production implementation, live-data integration, PAS 2035 automation
or proof of portfolio benefits. The repository itself proposes 6-8 weeks for
readiness and 6-9 months for a controlled live pilot
(`docs/case_study_48_addendum.md:211-223`).

## Exact case-study requirements

### Facts in the original request

* The fictional association has 60,000 homes in the North of England and is
  behind plan while a small team coordinates assessment, grants, procurement,
  resident consent and quality assurance using spreadsheets
  (`docs/case_study_48_original.md:15-17`).
* The objective names five capabilities: property prioritisation, PAS 2035
  assessment drafting, grant preparation, contractor/resident coordination and
  quality verification. The original autonomy levels range from L2 recommend
  to L4 autonomous flags (`docs/case_study_48_original.md:19-31`).
* A programme supervisor, contractor scheduling APIs, a resident consent
  channel and a separate damp-and-mould response loop are requested
  (`docs/case_study_48_original.md:33-35`).
* Resident consent, vulnerability safeguards, statutory response clocks,
  grant compliance, contractor accountability and regulator reporting are hard
  governance constraints (`docs/case_study_48_original.md:33-35`).
* Stated outcomes are doubled delivery, increased grant capture, statutory
  damp-and-mould response and lower resident energy bills. The original
  business case also claims GBP 40 million grant opportunity and borrowing
  capacity risk in the hundreds of millions
  (`docs/case_study_48_original.md:37-49`).

### Later corrections and controlling proposals

* Spreadsheet use signals fragmentation but is not evidence that
  administration is the binding constraint. Capital, competent roles, supplier
  capacity, property data, resident access, technical complexity, quality and
  grant conditions may dominate (`docs/case_study_48_addendum.md:60-66`).
* The proposed business outcome is a governed retrofit delivery service and
  portfolio control plane; agentic technology is an option, not the outcome
  (`docs/case_study_48_addendum.md:97-113`).
* AI must not diagnose hazards, satisfy statutory duties, release safety holds,
  approve professional work, infer consent, commit capital, award work, submit
  claims, accept quality, or close complaints or defects
  (`docs/case_study_48_addendum.md:193-196`).
* Pilot measures distinguish safe accepted handovers from starts and propose,
  subject to validation, 20% lower assessment-to-ready cycle time and 25% less
  manual coordination effort net of review
  (`docs/case_study_48_addendum.md:225-240`).
* The BRD contains 51 proposed requirements, not approved requirements. Its
  current decision is capped readiness and a gated pilot
  (`docs/brds/agentic-retrofit-programme-brd.md:9-33`).

## Evidence base and important limitations

### Quantitative planning evidence

The sector baseline estimates 74% of social rented homes at EPC/EER C or above,
which translates only illustratively to 44,400 of 60,000 homes. The remaining
15,600-home and 3,900-per-year figures are scenarios, not Proper North Homes
facts (`support/uk-social-housing-baseline-research.md:36-63`). Damp, repairs,
complaints and satisfaction figures are likewise sector comparators, not
company performance (`support/uk-social-housing-baseline-research.md:65-91`).
The source register maps these measures to official and supporting references
and records all derived calculations
(`support/uk-social-housing-baseline-source-register.md:19-46`,
`support/uk-social-housing-baseline-source-register.md:583-602`).

The following must remain labelled as hypotheses:

* Actual homes below EPC C and current accepted throughput.
* GBP 40 million grant availability, award, eligibility, claimability and cash.
* GBP 20,000 fully loaded cost and resulting GBP 312 million scenario.
* Borrowing capacity impact.
* Resident bill savings and causal attribution.
* No-access, refusal, supplier capacity and professional-capacity rates.

The BRD requires separate appraisal of the physical retrofit programme and the
incremental technology option, including integration, review, assurance,
support and exit costs
(`docs/brds/agentic-retrofit-programme-brd.md:663-690`).

### Company evidence gaps

The company-profile evidence explicitly says public evidence is stronger for
sector regulation than internal job descriptions, authority or operating model
(`support/company-profile-research.md:235-241`). The priority unknowns include:

* Address-level stock condition, EPC and higher-risk-building baselines.
* Twelve-month lifecycle events, accepted-handover throughput and delay causes.
* Authoritative systems, identifiers, data ownership and reconciliation.
* PAS 2035 role competence and available monthly capacity.
* Supplier route, committed capacity, subcontractors and contingency.
* Resident demographics, accessibility needs, channels, access outcomes,
  decisions, complaints and feedback.
* Capital envelope, grant award, match funding, cash, covenants and approval
  thresholds.
* Safety evidence, exception routes, material-change rules and defect severity.
* Board risk appetite and the exact decision sought.

These align with the BRD open decisions OD-01 through OD-23
(`docs/brds/agentic-retrofit-programme-brd.md:778-813`).

## Regulatory and professional concerns at 2026-09-19

### Awaab's Law

* Phase 1 has been in force since 27 October 2025 for all emergency hazards and
  significant damp and mould hazards
  (`docs/reference/awaabs-law-phase-1-guidance-2025.md:13-29`).
* Current maximum controls include 24 hours to investigate and make an emergency
  hazard safe, 10 working days to investigate a potential significant hazard,
  three working days for the written summary, and five working days after the
  investigation for relevant safety work
  (`docs/reference/awaabs-law-phase-1-guidance-2025.md:63-83`).
* Phase 2 guidance applies from 30 November 2026
  (`docs/reference/awaabs-law-phase-2-hazards-guidance-2026.md:8-15`).
  The roadmap therefore crosses an imminent regulatory change and must include
  a dated rule-source register and a final pre-presentation recheck.
* Retrofit workflow must not pause, suppress or reset the independent emergency
  and hazard-response service. BR-001 through BR-004 make this explicit
  (`docs/brds/agentic-retrofit-programme-brd.md:474-490`).

### Social rented sector MEES

The addendum's statement that EPC C by 2030 remains a consultation proposal
(`docs/case_study_48_addendum.md:323-335`) has been overtaken by a government
response published on 1 April 2026 in the repository's newer reference set.
That response describes the final policy position:

* EPC C or higher against one reformed EPC metric by 1 April 2030.
* EPC C or higher against a second metric by 1 April 2039.
* A transition for properties achieving current EER C before 1 April 2030.
* Spend exemptions, with enforcement intended through the reformed Decent
  Homes Standard and Regulator of Social Housing.

Evidence: `docs/reference/social-rented-sector-mees-government-response-2026.md:62-104`
and `docs/reference/social-rented-sector-mees-government-response-2026.md:154-160`.
This is a final government policy response, but the roadmap must still verify
the implementing legal and regulatory commencement status before calling it an
in-force landlord obligation. The case-study/addendum/BRD wording needs an
explicit presentation caveat rather than silent reuse.

### PAS 2035 and quality

PAS 2035:2023 is an end-to-end, whole-house retrofit specification, but the
licensed standard is not reproduced in the repository
(`docs/reference/pas-2035-2023-bsi-overview.md:11-18`,
`docs/reference/README.md:64-75`). The 2026 MEES response recommends PAS 2035
but does not make it a general MEES requirement; it remains required for
government-funded WH:SHF measures
(`docs/reference/social-rented-sector-mees-government-response-2026.md:951-972`).
The applicable edition, contract and funding conditions require competent
professional confirmation.

### UK GDPR

The current consolidated text was converted on 19 September 2026 and should be
used rather than the adopted historical text
(`docs/reference/README.md:53-61`). Key design implications are:

* Lawfulness, fairness, transparency, purpose limitation, minimisation,
  accuracy, storage limitation, security and accountability apply
  (`docs/reference/uk-gdpr-current-text.md:815-828`).
* Health and vulnerability information may be special-category data requiring
  both an Article 6 basis and an Article 9 condition
  (`docs/reference/uk-gdpr-current-text.md:917-938`).
* Current Articles 22A-22C define solely automated significant decisions by the
  absence of meaningful human involvement, restrict some decisions involving
  special-category data and require information, representation, human
  intervention and contestability safeguards
  (`docs/reference/uk-gdpr-current-text.md:1159-1192`).
* New technology, systematic profiling or large-scale special-category
  processing can require a DPIA before processing; the assessment must cover
  necessity, proportionality, risk and safeguards
  (`docs/reference/uk-gdpr-current-text.md:1347-1374`).

Synthetic data should therefore be genuinely artificial, non-identifying and
segregated from real data. Pseudonymised company data would still be personal
data. A synthetic demo does not remove the need for a DPIA, lawful basis,
retention, processor and transfer review before any later real-data pilot.

## Fictional role-agent interview strategy

The profiles are research instruments, not employees with company knowledge.
Their shared evidence base requires distinctions among case-study facts,
sector hypotheses and unknown company details
(`support/company-profile-research.md:8-18`). Interviews should use one
focused question at a time, record evidence classification, unresolved
company evidence, authority boundary and handoff. Do not present role-agent
answers as stakeholder validation.

Recommended interview set and question:

| Fictional profile | Primary interview question | Expected planning output |
| --- | --- | --- |
| Housing Asset Executive | What evidence would justify readiness spend and what must the Board decide later? | Decision ladder and risk appetite gaps |
| Building Safety Lead | Which hazards, holds and clocks can never depend on retrofit or AI? | Safety boundary and kill conditions |
| Retrofit Programme Manager | What is the accepted-handover lifecycle and where are competent approvals? | Lifecycle, PAS roles and capacity gaps |
| Finance and Grants Lead | What evidence separates opportunity, award, claim and cash? | Economics and finance gate |
| Procurement and Contracts Lead | What capacity is committed, and how are quality and failure controlled? | Supplier gate and reserve assumptions |
| Resident Engagement Lead | How are choice, accessibility, withdrawal and redress preserved? | Resident journey and equity measures |
| Neighbourhood Housing Officer | What must frontline staff see when work stalls or mould worsens? | Exception/handoff view |
| Data and Performance Lead | What synthetic design can test competing constraints without implying company facts? | Dataset, ground truth and validation |

The role/decision map confirms that these decisions require cross-role handoffs
(`support/company-profile-research.md:120-134`). The Data and Performance Lead
requires explicit synthetic identifiers, no real names or addresses,
`is_synthetic=true`, separate ground truth and no mixing with real data
(`.github/agents/data-performance-lead.agent.md:60-79`).

SME routing should remain small and opt-in. The cohort map suggests Martin
Pockl for Data/Fabric, Graham Hosking for Copilot Studio/multi-agent boundaries,
Niels Roos for applied AI prototyping, and Dominik Zemp or Michal Furmankiewicz
for architecture/security or AI application review
(`support/cohort.md:13-22`, `support/cohort.md:44-51`). Confidence describes
evidence strength, not proficiency, and every entry requires human confirmation
(`support/cohort.md:64-79`).

## Recommended architecture package

### High-level architecture

The high-level view should fit one slide and show:

1. Residents, frontline staff, competent professionals, suppliers, finance and
   executives.
2. Existing systems of record for assets/buildings, repairs/hazards, housing
   and resident preferences, PAS workflow, contracts/scheduling, finance/grants
   and evidence/document storage.
3. A portfolio control plane between users and systems, not a system-of-record
   replacement.
4. Deterministic lifecycle, safety clocks, evidence gates, decision rights,
   queues, audit and reconciliation.
5. Bounded AI services that only recommend, draft, reconcile and flag.
6. Analytics and executive scorecards based on controlled event records.
7. Cross-cutting identity/access, privacy, security, observability, versioning,
   manual fallback and stop controls.

Trust boundaries must distinguish resident channels, Proper North Homes,
supplier systems and any cloud/model processor. Human decisions for resident
consent, safety, PAS outputs, investment, procurement, grant submission,
payment and quality acceptance sit visibly outside the AI boundary.

### Medium-level architecture

Use two slides or one detailed appendix diagram:

* Ingestion adapters accept approved read-only extracts/events and retain source
  identifiers, version and provenance.
* Identity reconciliation maps property to parent building and flags conflicts.
* An append-only lifecycle/event store preserves state, handoff, pause, return,
  reopen and evidence history.
* A policy/rules service runs dated Awaab clocks, evidence validity, safety
  holds, delegated authority and segregation of duties.
* A deterministic state machine and work queues enforce gates and assign named
  human owners.
* An evidence ledger links assessment, design, resident decision, supplier,
  quality, payment, grant claim and cash without collapsing them into one state.
* Bounded assistants prepare sourced inputs, summarise evidence and flag
  anomalies; every output is labelled and reviewable.
* Approval and exception services capture decisions, rationale, authority,
  version, expiry, override and restart.
* Analytical views calculate queue time, accepted handovers, quality,
  complaints, capacity, cash and review effort.
* Export, manual operation, replay, disable and rollback paths prevent platform
  or model lock-in.

The detailed lifecycle is already defined as 15 separate stages in
`docs/brds/agentic-retrofit-programme-brd.md:449-471`. BR-005 through BR-010
require distinct states, immutable transition history, current design approval,
material-change invalidation, output labels and segregation of duties
(`docs/brds/agentic-retrofit-programme-brd.md:492-516`).

### Justified trade-offs

| Decision | Recommendation | Reason/evidence |
| --- | --- | --- |
| Control plane vs replacement platform | Integrate existing systems first | Authoritative systems are unknown; replacement adds migration and delivery risk |
| Deterministic workflow vs agent orchestration | Deterministic controls first | Rules, calculations, authorisation and irreversible actions are easier to test; repository guidance says the same (`.github/agents/agentic-solution-orchestrator.agent.md:104-118`) |
| One combined coordination agent vs separated services | Separate resident service from supplier coordination | Their interests, authority and failure modes differ; combined optimisation can pressure consent |
| Five-agent breadth vs one coherent slice | Prototype the flow/evidence slice | Twelve focused sessions cannot validate five end-to-end agents; one slice tests the binding premise |
| Live data vs synthetic data | Synthetic only for presentation/demo | Company access and lawful basis are unknown; synthetic evidence avoids false claims and resident risk |
| Working demo vs architecture/story | Demo only after a gate | A fragile demo can consume scarce days and reduce executive trust |
| AI vs conventional BI/workflow | Compare both | BRD requires attributable incremental value, not agent novelty |
| Throughput vs quality/safety | Optimise accepted handovers | Starts and nominal installations can conceal defects, resident harm and missing evidence |

## Synthetic data and optional demo

### Recommended synthetic package

Use the existing fictional Data and Performance Lead contract. A minimum useful
package contains properties, lifecycle events, monthly capacity, finance/grant
states, a separate hidden ground-truth file, manifest and data dictionary
(`.github/agents/data-performance-lead.agent.md:81-102`).

Recommended demonstrator scenario:

* 500 synthetic candidate properties across three fictional localities and four
  archetypes over twelve months.
* Competing generated constraints: supplier capacity, unaccepted handoffs,
  resident adjustment recovery, building dependencies, evidence rejection and
  fragmented identifiers.
* Visible anomalies: missing timestamps, stale evidence, unmatched building
  IDs, duplicate events, failed inspections and reopened defects.
* No names, addresses or free-text health histories.
* A deterministic property timeline and portfolio queue view.
* One explainable bounded-AI output: a source-linked constraint summary with
  uncertainty and questions for human validation.

The demo's visible success signal should be: a C-suite member can identify why
one property is blocked, who owns the next action, which control prevents unsafe
progression and how the portfolio constraint evidence differs from a guess.

### Demo gate and fallback

Proceed with a working demo only if, by Session 8:

* The high- and medium-level architectures are accepted.
* Dataset generation and deterministic validation pass.
* The demo runs from a clean reset in under six minutes.
* There are no credentials, live systems, network dependencies or real PII.
* The demo adds decision evidence not already communicated by two slides.

Otherwise kill the live demo and use tested screenshots or a short recorded
walkthrough. The orchestrator profile explicitly requires prepared inputs,
visible success, a reset, failure narration and a static/recorded fallback, and
warns against connectivity, hidden credentials and irreversible actions
(`.github/agents/agentic-solution-orchestrator.agent.md:209-230`).

## C-suite evaluation and presentation strategy

### Decision and audience

Ask: approve a capped readiness/shadow exercise with named owners, evidence
gates and stop authority; do not ask for a portfolio rollout. Evaluate the
presentation on whether executives can state:

1. The resident/business problem and why now.
2. The proposed decision and what it does not authorise.
3. The evidence supporting the proposition and the largest unknowns.
4. The architecture's human and deterministic control boundaries.
5. The next gate, owner, cost envelope requirement and stop conditions.

The communications profile recommends putting decision, evidence, future
state and resident experience into a deliberate mixed-audience sequence
(`.github/agents/presentation-communications-strategist.agent.md:29-78`) and
requires every claim to be supported or labelled, the ask to be identifiable
and the narrative to fit the allotted time
(`.github/agents/presentation-communications-strategist.agent.md:140-149`).

### Winning first 10 minutes

* 0:00-1:30: Start with the decision. "Approve a bounded readiness and shadow
  pilot, not five agents." Name the 60,000-home context and imminent 30 November
  Phase 2 date without claiming unverified company performance.
* 1:30-3:30: Tell one fictional, explicitly illustrative resident/property
  journey: worsening mould plus a stalled retrofit handoff. Show why speed,
  safety, consent and evidence cannot be optimised separately.
* 3:30-5:30: Expose the core insight: spreadsheets may be a symptom, while
  capacity, data, approvals, access or quality may be the constraint.
* 5:30-7:30: Reveal the high-level control-plane architecture. Emphasise
  deterministic gates and the bounded verbs "recommend, draft, reconcile,
  flag."
* 7:30-9:00: Quantify only the labelled scenario: 15,600 below-C homes and
  3,900/year are planning translations, GBP 40 million is not an award.
* 9:00-10:00: State the staged ask, success measures, kill gates and the
  consequence of a "no": continue safe statutory delivery and use the evidence
  to choose a simpler workflow option.

### Full one-hour run of show

| Time | Content | Evaluation purpose |
| --- | --- | --- |
| 0-10 min | Decision-led opening above | Win attention and establish trust |
| 10-18 min | Evidence, regulatory update and unknowns | Show urgency without overclaiming |
| 18-28 min | Current journey, target operating model and high-level architecture | Make the intervention tangible |
| 28-38 min | Medium-level architecture, controls and trade-offs | Prove feasibility and accountability |
| 38-44 min | Optional six-minute demo or fallback | Show one bounded capability |
| 44-50 min | Economics, benefits attribution and downside | Separate retrofit from technology value |
| 50-54 min | Roadmap, gates, owners and requested decision | Make action and limits explicit |
| 54-60 min | Structured challenge/Q&A and decision confirmation | Capture conditions, objections and next owner |

Use appendix slides for requirement traceability, regulatory wording, synthetic
schema, options scoring, detailed economics, risk register and role interviews.
The repository already contains an 11-slide deck property-validation report
with no structural warnings, but it covers only slides 3-8 and does not prove
narrative, factual or delivery readiness
(`.copilot-tracking/ppt/2026-09-18/proper-warm-cxo/slide-deck/validation/deck-validation-report.md:1-41`).

## Twelve-session, 85-calendar-day sequence

The fixed window runs from 2026-09-20 through 2026-12-13 inclusive, with
2026-09-19 treated as planning day zero. One dedicated workday in each of 12
execution windows yields exactly 12 focused sessions. Capacity is budgeted
as nine production sessions, two feedback/recovery sessions and one final
presentation session. Sessions 6 and 11 contain protected restart capacity;
they are not spare feature capacity. Each session ends with one accepted
artifact, an explicit decision and an updated remaining-capacity check.

| Session and calendar window | One-day objective and deliverable | End-of-session gate |
| --- | --- | --- |
| 1, 20-26 Sep | Lock goal card, audience, decision ask, evidence classes, source register and 12-session capacity limit | Sponsor-level planning proxy accepts the question and non-goals |
| 2, 27 Sep-3 Oct | Build requirement/claim traceability from original, addendum, BRD and current references; record the MEES wording conflict | No unsupported claim remains in the core story |
| 3, 4-10 Oct | Run Asset, Safety, Programme and Frontline fictional interviews; synthesise current journey and top unknowns | Gate A: if the problem/decision cannot be stated in one sentence, reset scope |
| 4, 11-17 Oct | Run Finance, Procurement, Resident and Data interviews; create the handoff register; score process, platform, workflow and bounded-AI options | Interview outputs remain hypotheses and at least one non-agent comparator survives |
| 5, 18-24 Oct | Draft high-level architecture, trust boundaries, human authority matrix and primary trade-offs | Gate B: kill five-agent-first design unless evidence uniquely supports it |
| 6, 25-31 Oct | Feedback and protected restart session: obtain architecture/sector review and either accept v1 or rebuild the failed boundary/value assumption | No medium-level design starts from a rejected high-level architecture |
| 7, 1-7 Nov | Draft medium-level component, data and event architecture, including failures, manual fallback, privacy and security controls | All Must control concepts and traceable interfaces are represented |
| 8, 8-14 Nov | Specify and generate synthetic data with hidden ground truth; run deterministic validation; make the demo/no-demo decision | Gate C: build only if data, reset and six-minute demo criteria pass |
| 9, 15-21 Nov | Accept or discard the prototype specification after mentor review, then build one narrow prototype or static walkthrough and run failure scenarios | Prototype or fallback is reproducible from a clean start |
| 10, 22-28 Nov | Executive-proxy checkpoint; test the first 10 minutes, architecture comprehension, evidence trust and demo value; then build the full deck and notes | Gate D: reset the narrative if the proxy cannot repeat the ask, evidence and stop conditions |
| 11, 29 Nov-5 Dec | Protected narrative recovery and mandatory assurance: recheck regulation after the 30 November Phase 2 date, reconcile claims/economics, finalise appendix, rehearse and test demo failure fallback | Gate E: freeze the deck and kill any unreliable live demo; no discretionary new scope |
| 12, 6-13 Dec | Final timed readiness check, one-hour C-suite presentation and decision capture; record conditions, owners, next gate and unanswered questions | Outcome is a recorded decision, not applause |

If no restart is consumed by Session 11, use the protected capacity only for
regulatory/citation assurance, accessibility, timed rehearsal and Q&A. Do not
convert it into additional product scope. If a restart consumes all of Session
11, presentation readiness takes priority over the live demo and detailed
appendix polish.

## Kill, reset and restart rules

* Gate A, problem reset: Kill the current story if evidence cannot distinguish
  a company fact, sector hypothesis and unknown. Restart with an evidence and
  discovery proposition, not a solution pitch.
* Gate B, architecture reset: Kill the five-agent architecture if a simpler
  process, BI or deterministic workflow option addresses the measured problem,
  or if human authority cannot be shown. Restart from the lifecycle and
  authority matrix.
* Gate C, prototype reset: Kill implementation after two bounded failed
  build/validation attempts or if synthetic ground truth cannot be recovered.
  Restart once with a smaller deterministic slice; otherwise switch to static.
* Gate D, narrative reset: If an executive proxy cannot repeat the ask,
  evidence and stop conditions after 10 minutes, discard the sequence, not the
  evidence. Rebuild the opening before polishing slides.
* Gate E, demo kill: Remove the live demo if it needs network access, hidden
  credentials, manual data repair, more than six minutes, or fails a
  cold-start/reset rehearsal. Use the tested fallback.
* Safety/privacy stop: Any design that infers consent, suppresses a hazard
  route, uses real resident data without approval, or allows AI/contractor
  controlled approval stops immediately.
* Restart evidence: A restart requires a documented root cause, repaired
  acceptance criterion, named owner and re-run of the failed check. Time
  pressure alone is not restart evidence.

These rules mirror the BRD's requirement that breaches trigger containment and
restart only with remediation evidence and relevant owner approval
(`docs/brds/agentic-retrofit-programme-brd.md:865-872`).

## Likely final deliverables

1. Executive decision brief and one-page claim/evidence register.
2. One-hour C-suite deck with speaker notes, first-10-minute script and Q&A.
3. High-level context/control-plane architecture.
4. Medium-level component, data flow, trust-boundary and approval architecture.
5. Options appraisal and architecture decision records with trade-offs.
6. Fictional role-agent interview pack with classification and handoffs.
7. Synthetic dataset, manifest, dictionary, ground truth and validation report.
8. Optional narrow demo with runbook, reset and static/recorded fallback.
9. Benefits/evaluation scorecard separating company baseline, scenario and
   pilot target.
10. Risks, decisions, kill/restart record and next-phase roadmap.

## Remaining research gaps

* Legal/regulatory confirmation of the 2026 MEES response's implementing and
  commencement status, and any further Decent Homes Standard instruments.
* Latest official Phase 2 Awaab guidance immediately before 30 November 2026.
* Proper North Homes source-system landscape, architecture standards and cloud,
  identity, residency, processor and model constraints.
* Actual C-suite attendees, decision rights, meeting format and appetite for a
  demo.
* Whether the existing 11-slide deck and source artifacts are intended as a
  baseline to revise or merely prior work.
* Realistic weekly availability around year-end holidays and access to human
  reviewers.
* Actual readiness budget ceiling, pilot locality and internal approval route.
* Confirmation from the suggested cohort SMEs that they are willing and
  appropriate reviewers.

## Genuinely blocking question

No question blocks creation of the 85-day plan or research-backed presentation
package. One question blocks final optimisation of the presentation and
investment ask:

> Which named C-suite decision-maker will chair the final hour, and what exact
> decision are they authorised to make in that meeting: endorse further
> discovery, release a capped readiness budget, or approve a shadow pilot?

Until answered, plan to request a capped readiness and shadow-design mandate,
not live deployment or portfolio capital acceleration.

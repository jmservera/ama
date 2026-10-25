---
title: Optional resident portal and communication agent — draft BRD amendment
date: 2026-10-23
status: draft
upstream_brd_version: 0.19.0
candidate_brd_version: 0.20.0
upstream_commit: 140d8f494482c78e84d15f3d46b9223d3c487af0
---

## Status and purpose

This is a bounded authoring package, not business signoff, permission to deploy,
a passed Define/Govern gate, a PRD or an ADR. The 2026-10-23 owner request is
authoritative direction to add optional resident self-service and a communication
agent to the proposed business scope. It is not evidence of actual company
delegations, resident demand, benefit, digital uptake or operational approval.

`amendment.patch` is the complete surgical change to the existing BRD at the
pinned commit. This readable document supplies its rationale and inserted
content. Existing headings, IDs, legacy aliases, staff work and historical
approval records are preserved. No replacement BRD or governed supersession is
claimed; lineage arrays stay unchanged. Rebase and reallocate new IDs if the
parent's integration base has moved.

## Source evidence and conflicts

All line references below are to **origin/main at the pinned commit**, not the
detached checkout. Its BRD bytes have SHA-256
`25ed596cafc4d9a4d83e2411a59cf0e6d9667c816fc2f537f82a84f3d9c6cf4c`.
The complete BRD text and registry were inspected: 13 BG, 52 FR, 103 AC,
12 NFR, 7 CON, 26 RULE, 51 OD and no DD identifiers. BR is a legacy alias
namespace, not available for new rules.

| Source file:line | Evidence and amendment implication |
| --- | --- |
| `docs/reference/README.md:9-17` | Immutable sources, maintained syntheses and append-only change log are distinct. Update dependent syntheses prospectively, not the historical source. |
| `docs/reference/memory.md:8-20` | Owner working context is not evidence; do not change memory without a request. |
| `docs/case_study_48_original.md:17-35` | 60,000 homes, small spreadsheet-led team, residents control consent; resident channel already envisaged. Immutable original remains untouched. |
| `docs/case_study_48_addendum.md:61-93,115-125` | Historical exercise approval is not live approval. EXA-004 protects non-digital service and says no *required* portal; rationale defers a portal pending research. EXA-005/011 preserve access isolation and accessibility. Append a dated amendment proposal; do not rewrite the approved register. |
| `docs/case_study_48_addendum.md:1085-1092` | Named person approves every AI-drafted resident message. Replace this as a universal future assumption only through the bounded policy proposal, never silently. Historical finding remains valid for its date. |
| `docs/reference/research/sector/housing-association-primer.md:249-288,333-355` | Diverse needs and fragmented information are context, not company adoption or smartphone evidence. Preserve supported contact and human escalation. No new legal-currentness claim is made. |
| `docs/reference/research/company/company-profile-research.md:8-26,261-271,284-299,341-374` | Modelled profile and role map are hypotheses. Demographics, channels, capacity, authority and outcome baselines are unknown. |
| `docs/brds/agentic-retrofit-programme-brd.md:599-656,692-718` | Reuse BG-005/009/010/011/012 and existing control-owner roles; effort targets are proposals and OD-18 is still open. Do not invent new benefits or corporate appointments. |
| `docs/brds/agentic-retrofit-programme-brd.md:749-765,1425-1433` | Existing non-staff conversation exclusion conflicts with the requested candidate scope; consent, representative authority and capacity-backed appointments must survive. FR-045/046 remain Should overall; portal release must nevertheless satisfy their applicable controls. |
| `docs/brds/agentic-retrofit-programme-brd.md:1511-1539,1555-1560,1906-1910` | RULE-018, RULE-022/AC-079, RULE-025/AC-095 and FR-044/AC-084 require explicit reconciliation. Resident agent is distinct from staff-only FR-049/050 and regulatory FR-051, which still cannot send communications. OD-47 is extended for proposed scope, not marked operationally closed. |
| `docs/reference/research/ux/customer-journeys/residents.md:21-25,65-95` | “No required portal” is not a prohibition. The actual deferral is line 95: no portal assumed, all AI messages human-approved, self-service later exploration. Replace this future-state interpretation prospectively while retaining historical provenance. |
| `docs/reference/research/ux/customer-journeys/frontline.md:51-63` | Intake and channel recovery need ownership; actual integrations are unknown. Optional portal must not become a precondition for assisted service. |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md:216-246,709-815,1895-1918,1946-1967,2071-2141` | Staff Entra realization, staff chat, release exclusions and profile journeys need explicit resident additions. Historical exercise acceptance does not approve the new amendment. Parent commissions PRD next, ADR after it. |

The detached checkout differs from pinned main in the BRD, addendum, current PRD,
knowledge-base index/log, resident/finance/programme journeys, UX content/profile
notes and other delivery research. This package uses `git show` pinned main
throughout; local/stale text is not an authority. No fetch, checkout, repository
write, issue/worktree change, heavy gate, Azure, paid call or private data was used.

## Business rationale and evidence limits

More than 80 homes arriving each week and weeks/months in process are owner
planning premises, not measured throughput or cycle-time evidence. In a stable
flow, illustrative open cases are arrival rate multiplied by average elapsed
weeks in the same case boundary. At an illustrative 81 arrivals/week and
*assumed*, not observed, durations of 4, 8 or 12 weeks, this gives 324, 648 or
972 concurrent home cases. These sensitivity choices are not duration forecasts.
Opening backlog, variable arrivals, pauses, reopened work and household/service
subcases require separate treatment; cases are not contacts or people.

No contact frequency, contact minutes, staff capacity, phone ownership or digital
uptake has been measured. The owner subsequently authorized explicit illustrative
assumptions to quantify the pitch; the model below uses author judgement, not
statistics or approved targets. Smartphone availability is an owner belief, not
a verified sector fact or justification for withdrawing service. 60,000 **homes** does not establish
60,000 unique residents, accounts or logins: homes can have several occupants,
representatives or cases, and one person can be linked to several homes.

The hypothesis is that self-service plus a common case event record reduces
avoidable status chasing and transcription, leaving staff to handle exceptions.
An agent is not sufficient by itself: deterministic access, published records,
valid commitments and owned queues are essential. Compare portal/workflow-only
with agent assistance; count review, correction, support and resident effort.
No cost saving, cashable headcount reduction or achieved benefit is claimed.

## Proposed inserted BRD content

The following blocks are intended for the existing BRD sections, not a second BRD.

<!-- BEGIN MODEL -->
### Optional Resident Service — Illustrative Capacity Case (2026-10-23)

The owner authorizes planning assumptions for a persuasive hypothetical
exercise, not operational approval or numeric benefit targets. Every input
below is **author judgement/gut-feel**, chosen on 2026-10-23; none is a
measured company metric, externally sourced statistic or validated forecast.
Low/base/high combine several assumptions and are sensitivities, not confidence
intervals. No public statistic is claimed or needed to run this exercise.

| Assumption and denominator | Low | Base | High |
| --- | --- | --- | --- |
| New home cases/week, following owner's >80 premise (A) | 81 | 90 | 100 |
| Mean elapsed active-case duration in weeks (D) | 4 | 8 | 12 |
| Routine calls per active home case/week (C) | 0.30 | 0.50 | 0.70 |
| Staff minutes per routine call, including lookup and post-call recording (Tc) | 8 | 10 | 12 |
| Separate routine email/document transactions per active case/week (E) | 0.25 | 0.40 | 0.60 |
| Staff minutes per email/document transaction, including recording (Te) | 4 | 5 | 6 |
| Share of active cases using self-service (U) | 30% | 50% | 70% |
| Share of those adopters' routine contacts actually avoided (V) | 50% | 65% | 75% |
| Additional reviews/escalations per digital active case/week (R) | 0.10 | 0.15 | 0.20 |
| Staff minutes per additional review/escalation (Tr) | 4 | 4 | 5 |
| Additional channel reconciliation minutes per active case/week, all channels (Q) | 0.05 | 0.08 | 0.10 |
| Fixed recurring resident portal/agent support hours/week (S) | 1 | 2 | 4 |
| Staff onboarding minutes per newly enrolled primary case contact (To) | 6 | 8 | 10 |

Calls and email/document transactions are mutually exclusive handling episodes:
a call and its follow-up document are counted once unless separate staff work
is actually required. Recording is already inside Tc/Te, never saved again
as an additional transcription benefit. All volumes refer only to routine
status/process/document/scheduling coordination; consequential/safety/consent
decisions and their existing workload are excluded and are not deflected.
Non-avoided contacts, including contacts merely shifted to another channel,
remain in baseline workload and earn no saving. R is additional exception/review
effort beyond that retained workload; Q/S are incremental costs, not hidden
inside avoided minutes. The scenarios assume OD-53 eventually permits eligible
routine traffic; they do not authorize it. Human approval remains default until
then. Without that exception, rerun with the actual per-message review effort;
if review needs are higher, increase R/Tr rather than assume approval.

Formulas (hours/week unless stated):

* Concurrent WIP W = A × D, assuming stable arrivals/duration and no opening backlog.
* Routine baseline B = W × (C × Tc + E × Te) / 60.
* Gross routine handling avoided G = B × U × V.
* Additional review H = W × U × R × Tr / 60.
* Reconciliation J = W × Q / 60.
* Routine net capacity released N = G − H − J − S.
* New-intake onboarding O = A × U × To / 60.
* Net including ongoing intake onboarding F = N − O.
* Initial active-cohort enablement I = W × U × To / 60, a one-off staff-hours
  scenario, not another recurring weekly charge for the same people.

| Derived measure | Low | Base | High |
| --- | --- | --- | --- |
| Concurrent active home cases W | 324 | 720 | 1,200 |
| Routine baseline calls/week | 97.2 | 360 | 840 |
| Separate email/document transactions/week | 81 | 288 | 720 |
| Routine baseline staff hours/week B | 18.36 | 84.00 | 240.00 |
| Gross avoided handling hours/week G | 2.75 | 27.30 | 126.00 |
| Additional review/escalation hours/week H | 0.65 | 3.60 | 14.00 |
| Reconciliation hours/week J | 0.27 | 0.96 | 2.00 |
| Recurring support hours/week S | 1.00 | 2.00 | 4.00 |
| Routine net released hours/week N | 0.84 | 20.74 | 106.00 |
| New-intake onboarding hours/week O | 2.43 | 6.00 | 11.67 |
| Net released hours/week including intake F | -1.59 | 14.74 | 94.33 |
| Initial active-cohort onboarding hours I, one-off | 9.72 | 48.00 | 140.00 |

Onboarding assumes one primary case contact per digitally adopted home case
solely for staff-workload arithmetic, not one actual resident/account per home.
Representatives, shared households, repeat cases and reusable accounts may change
it. I and O must cover disjoint cohorts/time periods; do not charge an initial
cohort again as newly onboarded. I excludes development, migration, training and
security setup, which need separate estimates. S is not proof of adequate
operational support capacity. No monetary ROI or payback is stated: loaded
hourly cost, cashability, build, identity/storage/model/platform and incremental
operating costs remain unspecified and must be stated before any money claim.
No headcount reduction or booked savings is inferred from released capacity.

With base inputs held fixed, including new-intake onboarding:
F(U) = 35.4 × U − 2.96 hours/week. The hypothetical break-even uptake is
2.96 / 35.4 = **8.36%**; this is an algebraic sensitivity, not an adoption
forecast. At 25%/50%/75% uptake, F is 5.89/14.74/23.59 hours/week. At base
50% uptake, V must exceed **29.90%** to break even on staff time. If the
denominator is non-positive after review/onboarding effort, no uptake rate
breaks even. Extra human review, poor identity recovery, duplicate entry or
low eligible demand can remove the gain; the low combined scenario costs time.

Pitch: **“At an illustrative 90 new homes/week and eight weeks in process,
720 cases overlap. If half use self-service and 65% of their routine contacts
are avoided, the model releases about 15 staff-hours/week after review,
reconciliation, recurring support and new-intake onboarding—not 15 hours
observed, a staffing cut or cash savings. The low scenario loses about
two hours/week, so we will test task success, actual effort and safety.”**

FR-062 and OD-55 turn these assumptions into an explicit validation protocol.
Keep measured baselines and approved targets separate from this scenario;
do not block the hypothetical exercise while awaiting company data. Compare
workflow/portal-only and agent-assisted handling and report adverse results.
<!-- END MODEL -->

<!-- BEGIN CONTEXT -->
### Optional resident service amendment (2026-10-23, proposed)

The owner directs inclusion of a lean, mobile-responsive optional resident
portal and resident communication agent in the draft business scope. This
replaces the earlier assumption that resident self-service is only later
exploration; it does not replace EXA-004's protection against a required portal.
Phone, email, letters, visits and assisted service remain available without
detriment. The approved 2026-10-10 exercise baseline is historical, not rewritten.

The owner's planning premises are more than 80 new homes/week and cases
lasting weeks or months. Illustrative steady-flow WIP is arrivals/week times
average elapsed weeks, not a validated capacity forecast. At 81/week and
assumed 4/8/12-week durations, 324/648/972 cases overlap. These are sensitivities,
not measured durations, contact volumes, staffing needs or targets. The source
fact is 60,000 homes, not 60,000 residents or accounts. Smartphone availability
and uptake remain unvalidated; no resident loses service by not using the portal.

Proposed benefits extend BG-011 and BG-009: staff contact-minutes per open case
per week and per completed case, avoidable repeat contacts, manual transcription
minutes/events, resident task success and effort, access/recovery failures,
unowned/overdue exceptions and human-response times. Baselines, cohort, window,
denominators and improvement targets remain unknown pending OD-18 and OD-55.
The Illustrative Capacity Case below provides owner-requested quantified
author-judgement sensitivities, not measured baselines or approved targets.
Measure channel switching, abandonment, review/correction/support effort and
non-digital outcomes, not digital uptake or contact deflection alone.
Proposed release guardrails are zero unauthorized disclosures or controlled
decisions, zero inferred works consents and zero suppressed hazard referrals
in agreed tests; they are not proof of zero live risk or achieved benefits.

Programme Manager is the proposed accountable delivery owner; Resident
Engagement owns service inclusion/content and resident validation; Housing
owns assisted intake and accepted human handoffs; Digital owns access,
integration, abuse and recovery; Data and Performance owns measurement.
Repairs/Safety, Legal/DPO, contract and financial owners retain their existing
decisions. These are role assignments for review, not named company appointments
or signatures (OD-52 to OD-55). Residents, including non-digital households and
task-limited representatives, must be consulted, not represented by role agents.

Add an incremental synthetic resident slice without delaying the owner-testable
staff landing/authentication work unless a specific dependency is evidenced.
First demonstrate authorized case/timeline/document access, one requested upload,
one appointment response, one grounded question and an accepted human handoff
against the continuing 60,000-home/980-case exercise lineage. Exercise at least
one registered real AI task in a later accepted application build under CON-007;
this authoring task authorizes no cloud action or model spend. Use fictional
resident identities and records only. No live sending or real resident access.
Production onboarding, channel connectors, throughput sizing and operational
hardening require separate decisions; basic authorization, privacy and accessible
task completion are prerequisites even for the demonstrator.
<!-- END CONTEXT -->

<!-- BEGIN REQUIREMENTS -->
### Optional Resident Portal and Communication Agent (Draft Amendment)

These rows are in proposed business scope, not deferred to unspecified research.
They are additive to staff workflows and are not resident memory or an extension
of staff FR-049/050. No persistent resident preference memory is authorized beyond
the explicit case/contact records. A resident submission is a sourced event, not
an accepted fact, professional approval or works consent. Login, portal use,
document upload and appointment acceptance never confer consent to works or
representative decision authority (FR-011/013/045).

The proposed exception to per-message human approval is RULE-028 and FR-061.
Until its specific gate is recorded, every AI-drafted resident message still
requires named human approval. The exception cannot authorize consequential,
sensitive, uncertain or out-of-scope communication or alter FR-036's prohibitions.

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-053 | None | The service shall give a signed-in resident or authorized representative a self-service view of only their currently authorized home case(s), timeline, next action and approved resident documentation. | BG-005, BG-009, BG-011 | Residents, representatives, Engagement, Housing | AC-104: Given authorized and unrelated cases, when the resident opens or searches the workspace, then only authorized case summaries, next actions and timelines are returned, with recorded-as-of time and unknown or stale status explicit.<br>AC-105: Given approved and internal-only document versions, when a resident requests documentation, then only approved resident-visible versions for that case are returned and their version and source are shown. | Must |
| FR-054 | None | The service shall allow a resident to submit requested documents to an authorized case with a receipt and a visible review state. | BG-005, BG-009, BG-011 | Residents, Housing, reviewers, Digital | AC-106: Given a current document request, when a permitted file is submitted, then the resident receives a traceable receipt and the request shows received/pending review, never verified or accepted without authorized review.<br>AC-107: Given a rejected or interrupted upload, when the resident checks the request, then it remains outstanding with an accessible reason, safe retry or assisted route and no false receipt. | Must |
| FR-055 | None | The service shall let residents propose, accept or postpone appointment options while preserving confirmed-capacity, household-preference and human-authorization gates. | BG-005, BG-009, BG-011 | Residents, Housing, Programme, contractors | AC-108: Given an offered slot, when the resident accepts or proposes another time, then their response is recorded and no confirmed commitment is shown before FR-046/AC-088 and RULE-007 pass.<br>AC-109: Given a postponement or pause request, when submitted, then affected non-urgent progression is held for its human owner, the next update is visible and no no-access event or works consent is inferred. Urgent hazard response continues. | Must |
| FR-056 | None | The programme shall maintain a unified, provenance-bearing case event record across portal, phone, email, letters, visits and document exchanges, with reconciliation that reduces duplicate entry. | BG-010, BG-011 | Housing, Engagement, Programme, residents, audit | AC-110: Given an event from any supported channel, when recorded, then the case retains event/source reference, channel, occurrence and recorded times, actor/reporter, original account or protected source link, contact purpose, delivery/receipt state, review state and next-action owner; unknown values are explicit.<br>AC-111: Given the same event replayed or an ambiguous home match, when intake runs, then replay is linked without duplicate case effects and ambiguity enters an owned queue without cross-household disclosure. Manual capture remains available where a connector is absent; assisted entry and automatic capture are labelled distinctly. | Must |
| FR-057 | None | Staff shall receive exception-led queues for resident requests, failed contacts, document reviews, unresolved conflicts and unaccepted or overdue handoffs. | BG-009, BG-010, BG-011 | Housing, Engagement, Programme, Digital | AC-112: Given new, failed, overdue and unowned events, when staff inspect the queue, then each exposes the case, reason, urgency, due/next-update time and accountable human or escalation owner; message delivery alone cannot close a handoff under FR-018. | Must |
| FR-058 | None | A resident communication agent shall answer status and process questions only from the requester's authorized current case records and approved resident sources, with safe abstention and human handoff. | BG-003, BG-005, BG-009, BG-012 | Residents, Housing, Safety, Engagement, Digital | AC-113: Given a status or process question, when an answer is proposed, then each material assertion cites an authorized case fact or approved source/version and its as-of time; missing, stale or conflicting information is unknown and cannot be fabricated or retrieved across households.<br>AC-114: Given uncertainty, a sensitive or consequential request, possible hazard, distress or a request for a person, when received, then the agent abstains from the controlled decision and creates a traceable human handoff. Possible hazards are referred immediately through FR-003/RULE-003 independently of model success; emergency/help routes remain visible. | Must |
| FR-059 | None | Residents shall be able to request human help and manage safe contact, language, accessibility and channel preferences through digital or assisted routes. | BG-005, BG-009, BG-010 | Residents, representatives, Housing, Engagement | AC-115: Given a changed safe contact or human-help request, when recorded, then subsequent contact uses the verified current preference or pauses for human clarification, the request has a reference/owner/next-update time and portal non-use has no service penalty. | Must |
| FR-060 | None | The service shall manage resident and representative case entitlements independently of login and maintain audited grant, expiry, revocation and recovery workflows. | BG-005, BG-010 | Residents, representatives, Housing, DPO, Digital | AC-116: Given several occupants, an interpreter-only representative, several homes or revoked authority, when any view, download, upload, search or agent turn is requested, then current task/case/field scope is rechecked; revoked scope is denied on the next request and grant/revocation reasons, actor and time remain auditable.<br>AC-117: Given enrolment, account recovery or a household change, when identity is established or recovered, then case rights are separately verified by the authorized process and neither shared address, relationship nor successful login grants works-consent authority. Assisted recovery cannot bypass the same entitlement check. | Must |
| FR-061 | None | The service shall enforce configurable bounded communication authority at dispatch, with routine automation disabled until the specific policy gate and evaluation pass. | BG-003, BG-005, BG-010, BG-012 | Residents, Engagement, Housing, Digital, assurance | AC-118: Given a proposed automated acknowledgement, reminder or factual status reply, when dispatch is attempted, then the service requires the approved task/channel/audience/content policy version, current permitted evidence, scope and safe contact; it records the policy approver, action, sources, time and delivery outcome and denies any unmatched action.<br>AC-119: Given changed permissions, preferences, evidence, policy expiry, model failure or a guardrail breach, when dispatch is attempted, then it stops or falls back to named human review and exposes an owned exception; disabling automation leaves case access and urgent human routes available. | Must |
| FR-062 | None | The programme shall measure resident-service effort and outcomes with a frozen comparable protocol before claiming portal or agent benefit. | BG-009, BG-011, BG-012 | Data and Performance, Programme, Finance, Engagement, residents | AC-123: Given a proposed comparison, when the protocol is reviewed, then it defines case/contact/task denominators, open and completed populations, time window, non-digital cohorts, repeat-contact classification and staff/resident effort including review, transcription, support and failure recovery; missing baselines/targets remain unknown.<br>AC-124: Given results, when reported, then portal/workflow-only and agent-assisted outcomes, guardrail breaches, task success, failed access, human response and uncertainty are separated; no uptake, saved minutes or cashable benefit is claimed without measured evidence and attribution. | Must |
| NFR-013 | None | The portal shall offer a lean mobile-responsive, accessible username/password-style resident experience without requiring a staff account or withdrawing assisted access. | BG-005, BG-009 | Residents, Engagement, Digital | AC-120: Given the core resident tasks, when tested at 320/390/1280px with keyboard, screen reader, text resize and reflow, then navigation, status, errors, upload and help are operable against the existing EXA-011 WCAG 2.2 AA engineering target; failures block the affected demo task and no achieved conformance or real-user validation is inferred. Managed identity choice and proportionate extra verification/recovery controls are deferred to ADR, not homegrown password storage or emailed passwords. | Must |
| NFR-014 | None | Resident access, documents and agent processing shall preserve least privilege, safe handling, purpose-limited retention and recoverability across normal and abusive use. | BG-003, BG-005, BG-009 | Residents, representatives, DPO, Digital, assurance | AC-121: Given adversarial access and file tests, when links, identifiers, search, export, model retrieval or uploads are manipulated, then cross-case content/metadata disclosure is denied and audited, unsafe/unvalidated files are isolated from readers/models pending checks and document instructions cannot expand agent authority. Recovery, session and abuse controls are tested without logging credentials or sensitive document content.<br>AC-122: Given portal/agent outage, lost access or retention expiry, when recovery or rights handling runs, then approved retention/deletion rules apply to files, case events and minimal conversation records separately, case/audit history reconciles without duplicate effects, and safe assisted service continues. Missing retention, recovery, rate/size limits or response targets block live release under OD-54/55, never become assumed defaults. | Must |
| RULE-027 | None | Portal or agent use shall be optional and shall not be a condition of service, consent, priority, complaint access or an accessible human response. | BG-005, BG-009 | Residents, representatives, Engagement, Housing | AC-125: Given a resident without a device/account or declining self-service, when they use phone, email, letter, visits or authorized support, then the same controlled case and decision routes remain available without digital-completion requirements or automated detriment. | Must |
| RULE-028 | None | Only an explicitly approved, versioned routine communication policy may replace per-message human approval for bounded acknowledgements, reminders and sourced status/process replies; all consequential, sensitive, uncertain or unmatched communications retain named human review before sending. | BG-003, BG-005, BG-009, BG-012 | Residents, Engagement, DPO, Legal, Digital, control owners | AC-126: Given the policy gate is absent, expired or outside its approved scope, when an AI-drafted resident message would be sent, then named per-message human approval is required. The exception activates only after OD-53 records authorized owner approval, permitted content/tasks/channels, evaluated limits, monitoring, disable/recovery and release under RULE-020. No policy may authorize hazard decisions, consent inference, contract/cost commitments or other FR-036 prohibitions. | Must |
<!-- END REQUIREMENTS -->

<!-- BEGIN DECISIONS -->
| ID | Decision | Proposed roles | Effect while open |
| --- | --- | --- | --- |
| OD-52 | Appoint the resident-service accountable owner, staffed intake/exception/support owners and source owners; confirm which phone/email/visit/document routes exist and which need manual capture or a separately accepted connector. | Programme Manager accountable; Housing, Engagement and Digital responsible (proposed roles, people unconfirmed) | Blocks live resident-service release; does not block synthetic draft/demo planning or independent staff landing/auth work |
| OD-53 | Approve or reject the narrow routine-communication exception to RULE-022/AC-079, RULE-018 and RULE-025; record task/content/channel/audience boundaries, policy approver, evaluations, oversight, incident/disable/restart rules and a separate RULE-020 release. | Resident Engagement accountable for proposal; DPO/Legal review and each affected control owner approves within delegated authority | All AI-drafted resident messages remain individually human-approved until this explicit gate; no change to prohibited decisions |
| OD-54 | Confirm resident identity/enrolment/recovery and task-limited case-entitlement model, household changes, representative revocation, privacy notice/lawful basis/DPIA, document safeguards, retention/rights, session/abuse controls and supported managed identity options. | Digital service owner accountable for design; Housing, Engagement, DPO and Legal review within existing authority | Blocks real resident accounts/data; ADR selection follows PRD, no staff-Entra-only assumption or emailed passwords |
| OD-55 | Freeze baseline/proposed targets and test conditions for contact effort, repeats, transcription, resident task success, non-digital equity, response/recovery, access failures, throughput/concurrency and AI limits; validate arrivals, cycle duration, uptake and staffing assumptions. | Data and Performance responsible; Programme accountable; Engagement, Housing and Finance validate relevant outcomes | Blocks benefit and production-capacity claims, not the incremental synthetic slice; coordinate OD-18/25/51 without fabricating targets |
<!-- END DECISIONS -->

## Proposed ownership and residual approvals

For amendment planning, Programme and Digital are high-power/high-interest
stakeholders to manage closely; DPO/Legal/Safety and contract/financial owners
are high-power approval participants for their boundaries. Residents and
representatives are high-interest affected people to involve directly; low formal
power must not make them low priority. Include households with no safe device,
limited connectivity/literacy, shared phones, accessibility/language needs,
leasehold questions, several occupants and revoked representatives.

Exactly one proposed accountable role is stated per OD work item; domain
approvals are separate decisions, not a committee pretending to be one person.
EXA-001 gives the exercise owner baseline approval; no role-agent answer can
appoint real service owners, validate uptake or approve a policy exception.
No new role-agent consultation was necessary: the existing journeys answer
service safeguards, and the residuals require owner/design/governance decisions,
not another synthetic opinion. No owner questions already answered are repeated.

## Downstream boundary

Use `draft-prd-handoff.json`, not `BRD_TO_PRD_HANDOFF_V1`. It is a draft amendment
input for parent-coordinated PRD authoring, then ADR evaluation, not permission
to implement. Core controlled-decision rules, staff chat privacy and regulatory
assistant no-send authority remain. No resident long-term memory, live channel
connector, autonomous booking confirmation, operational rollout or production
identity product is selected here.

The parent must integrate dependent reconciliations in `change-manifest.md`,
obtain review and owner exercise acceptance, and retain operational blockers.
Neither historical PRD acceptance nor owner acceptance of staff ADR 0004
constitutes acceptance of this new resident communication policy.

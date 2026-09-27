---
title: Agent What-If Study
description: What-if session on the Agent Request Challenge, testing whether phone-captured evidence, geotagging, digital invoices and other new inputs move any of the five requested agents closer to a viable agentic end-to-end
ms.date: 2026-09-27
ms.topic: reference
---

## Purpose and Method

The [Agent Request Challenge](./agent-request-challenge.md) concluded that
none of the five requested Proper Warm agents should be built as an
end-to-end agent. Every "owns end-to-end" line bundled deterministic control
work, accountable human decisions and a smaller set of tasks where bounded
AI genuinely helps.

The project owner asked a follow-up question. If the programme could feed
each agent richer inputs, for example residents, assessors and retrofit
companies uploading photos and invoices from their phones with GPS metadata
so the platform could confirm the pictures were taken on site, would that
tip the verdict? The Assessment case was given as a worked example: a photo
and invoice bundle, checked for provenance, could give the assessor an
evidence assessment that speeds the decision.

This page runs that thought experiment for each requested agent. For each
one it:

* Specifies a concrete augmentation, so the analysis is not about "more AI"
  in the abstract
* Asks whether the augmentation removes any of the reasons the original
  challenge rejected end-to-end autonomy
* Puts one focused clarification question to the relevant `company-*` role
  agents and records their sector-informed answer
* States a revised verdict against the original challenge

All role-agent answers are `Sector-informed hypothesis` unless they restate
material already in the case study, the addendum or the local regulatory
snapshots. The role agents have no access to Proper North Homes' systems,
contracts, resident base or supplier arrangements, so this study does not
establish that any of the augmentations is feasible, lawful or affordable
in Proper North Homes' actual environment. It identifies which
augmentations, if validated, would justify revisiting the earlier verdicts.

The regulatory citations in this page were spot-checked against the local
snapshots on 2026-09-27. They were not checked against the official
sources online.

## Summary of Revised Verdicts

None of the augmentations tested changes the headline finding of the
original challenge: no requested agent should own an end-to-end lifecycle,
and the shared foundation (property master, lifecycle state machine, hazard
case record, evidence schedule, grant ledger, capacity register) still has
to be built first. Adding richer inputs to services that lack these records
makes unreliable decisions faster.

Within that constraint, the augmentations change how much bounded AI could
usefully do inside a workflow that a human still owns. The strongest cases
are Assessment and Quality Verification, where per-measure evidence packs
with location and time provenance would materially shorten review cycles.
The weakest is Grant and Funding, where the binding constraints are award
evidence, eligibility rules and finance-authority acts, not the format of
the inputs.

| Requested agent | Augmentation tested | Original verdict | Revised verdict after augmentation |
| --- | --- | --- | --- |
| Stock Prioritisation | Resident and inspection app with geotagged condition photos, plus a resident-declared vulnerability channel with UK GDPR Article 9 controls | Do not build as agent | Unchanged. Better inputs improve the scoring model but the ranking is still arithmetic and the cohort policy is still a Board decision |
| Assessment | Assessor, resident and installer app that uploads geotagged photos and structured invoice data against a per-measure evidence schedule | Bounded AI inside workflow, limited to pre-filling sourced facts | Unchanged in kind, wider in scope. Provenance-checked evidence could support pre-populated hazard, ventilation and higher-risk building flags, but site observation and PAS 2035 sign-off stay with the assessor and coordinator |
| Grant and Funding | Structured digital invoices with installer VAT, product and serial data, linked to the geotagged install evidence | Bounded AI inside workflow, only after the ledger exists | Unchanged. Better inputs raise claim quality but do not replace the four-state ledger, versioned eligibility rules or Finance authority |
| Contractor and Resident Coordination | Contractor scheduling and capacity feeds, resident app for consent, adjustments and appointment outcomes, geotagged proof-of-visit | Split in two; bounded AI on both sides | Unchanged. The augmentation strengthens the deterministic decision record and reduces "no-access equals refusal" errors, but consent, contract instructions and safeguarding stay human |
| Quality Verification | Per-measure geotagged photo packs from the installer, resident-uploaded post-install photos, structured commissioning data, sensor validity register | Bounded AI inside workflow. Flags can only raise concerns | Slightly stronger. The augmentation makes the flagging model more useful and enables raise-only pattern detection across installers and archetypes, but acceptance and defect closure stay with the competent quality authority |
| Programme Supervisor | Photo, invoice and appointment events all keyed to the property lifecycle state machine | Do not build as agent | Unchanged. Richer events make the workflow engine more useful. They do not remove the need for named owners, gates and clocks |
| Damp-and-Mould Loop | Resident and contractor app with geotagged hazard photos and same-visit reporting | Do not build as agent; statutory clocks in the repairs system | Unchanged. Faster awareness capture is valuable, but Awaab's Law Phase 1 awareness and triage decisions stay with the landlord, not with an AI |

## Cross-Cutting Considerations

Six issues run through every augmentation. They should be treated as
constraints on how any of the ideas below is designed, not as reasons to
refuse the ideas outright.

* Provenance is not proof. Geotag metadata (EXIF GPS) is easy to strip,
  alter or spoof. A "GPS-verified" photo needs corroborating signals such
  as device attestation, network location, time-of-day matching an
  appointment, capture inside a first-party app and, where possible,
  independent inspection sampling. Even then, provenance-checked photos
  are evidence to a human, not autonomous acceptance.
* Article 9 special category data. Photos inside a home routinely capture
  health cues, faith articles, disability aids and other people. A resident
  photo channel needs a lawful basis, a DPIA, retention rules, redaction
  routines and a clear resident right to decline. Building Safety, Data
  Protection and Resident Engagement own this together
  ([UK GDPR](../../regulatory/data-protection/uk-gdpr-current-text.md),
  and the UK Data Protection Act 2018).
* Digital exclusion and adjustments. A phone-first evidence channel cannot
  become the default route or a precondition for repairs or retrofit.
  Non-digital, third-party assisted and phone-based routes stay open
  (BRD BR-011, BR-016 legacy IDs; addendum service-design section).
* Contractor market realism. The original challenge found no evidence that
  small retrofit installers work through scheduling or capacity APIs.
  Requiring geotagged photo bundles is contractable through PAS 2035 and
  procurement, but "an installer app" is not free.
* Awaab's Law awareness. Any channel that could see damp, mould or
  emergency hazards creates awareness for the landlord from the moment the
  content lands, whether or not the app is officially "for" hazards
  ([Awaab's Law Phase 1 guidance](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
  section 3, in force from 27 October 2025). The design must respect the
  statutory clock; it must not become a way to delay or reset it.
* PAS 2035 competence. Better inputs do not make an AI a competent
  Retrofit Assessor, Designer, Coordinator or Evaluator. Sign-off, risk
  path and material change decisions stay with named professionals.

## Stock Prioritisation Agent

### What-If Augmentation

The programme offers residents a Proper Warm app to report condition
issues with geotagged photos, note vulnerabilities and adjustments, and
consent to any onward use. Housing officers and stock-condition surveyors
use the same app during visits. The platform normalises these into the
property master with source, date, capture location and confidence.

### Would It Remove the Original Blockers?

The original blockers were: ranking is arithmetic once weights are agreed;
weights, exclusions and treatment of health risk are Board policy;
eligibility is a deterministic pass/fail/unknown result; special category
data needs a lawful basis and a DPIA; solely automated significant
decisions are restricted; open damp cases follow the statutory route and
missing data must trigger investigation.

The augmentation improves inputs but does not change any of these. It
increases the amount of Article 9 data flowing in (resident-declared
vulnerabilities and photos that reveal health cues) and therefore
increases DPIA scope. It also raises the risk that resident-reported
condition issues visible to the app create landlord awareness of hazards
under Awaab's Law before any prioritisation logic runs.

### Clarification Questions to the Company Agents

`Data and Performance Lead` was asked: if a resident and inspection app
supplied geotagged condition photos and resident-declared vulnerability
flags into the property master, would the scoring model become more
defensible, or would the underlying data-completeness problem remain the
binding constraint?

* Sector-informed hypothesis: an app improves timeliness and provenance
  for the properties it reaches, but the ranking's defensibility depends
  on covering every property, not on the richness of the covered ones. In
  most housing associations, the properties least likely to appear in a
  self-service app are the ones with the greatest data gaps: households
  who never contact the landlord, residents without smartphones or English
  as a first language, and unoccupied or void homes. Without an outreach
  and assisted-capture route, a photo channel could widen, not close, the
  data-completeness gap. The field-level source register in the shared
  foundation is still the binding change.

`Executive Director of Assets` was asked: would you accept a ranking that
weights resident-declared vulnerabilities differently from
professional-observed vulnerabilities, or would that need a Board policy
change first?

* Sector-informed hypothesis: differential weighting of self-declared
  versus recorded vulnerability would need explicit cohort policy from the
  Board, with DPO and legal review. It is likely to be rejected as a
  single weight and accepted only as a documented exception route that
  routes self-declared cases to a named assessment queue.

### Revised Verdict

Do not build as agent. The augmentation belongs to the shared foundation
(property master and hazard case record), not to a Stock Prioritisation
agent. If the app exists, its outputs feed the deterministic rules model
and a bounded AI reconciliation module already scoped in the original
challenge.

### Stop Criteria for the App Concept

* Stop if the app becomes the only way to report a condition issue
* Stop if resident photo uploads are not linked to the hazard case record
  and the Awaab's Law awareness timestamp
* Stop if resident-declared vulnerabilities are used in a solely
  automated significant decision without a documented lawful basis and
  DPIA

## Assessment Agent

### What-If Augmentation

The worked example from the project owner. The Retrofit Assessor, the
resident and the installer all use a Proper Warm app to upload evidence
against a per-measure PAS 2035 evidence schedule. Each upload carries
device attestation, EXIF GPS, capture time and app-signed provenance. The
platform matches each artefact to the property, the measure and the
appointment. Invoices are structured, with installer VAT number, product,
serial and unit price parsed and linked. The AI produces an evidence
assessment for the assessor: what evidence is present, what is missing,
what is inconsistent, and where site observation is still required.

### Would It Remove the Original Blockers?

The original blockers were: the request omitted the Retrofit Assessor, so
"coordinator approves a draft" merged two PAS 2035 sign-offs; an agent
cannot make site observations; L3 was acceptable only for pre-filling
facts from named sources.

The augmentation does not let an AI make site observations. It does let it
verify that named-source facts match the site (photo at the property,
serial number on the plate, invoice against the fitted product). This
lifts the evidence-assembly and completeness-check step from manual to
mostly automated, which is what the addendum's target of at least a 20%
cut in assessment-to-ready-to-install time depends on. It does not remove
the Assessor's or Coordinator's sign-off.

It does expand two governance duties. Photos capture household context
that Article 9 covers, and provenance-checked hazard photos create Awaab's
Law awareness the moment they arrive.

### Clarification Questions to the Company Agents

`Retrofit Programme Manager` was asked: if the AI produced a provenance-
checked evidence assessment for the Retrofit Assessor, could the
Assessor's on-site time realistically fall, or would the PAS 2035 method
still require the same visit length?

* Sector-informed hypothesis: on-site time would fall for the pre- and
  post-visit work rather than for the visit itself. The Assessor still
  has to inspect construction, ventilation, condition, occupancy patterns
  and higher-risk features in person. Pre-populated evidence packs reduce
  the desk time and the rework caused by missing surveys, and they let
  the Coordinator set the risk path faster. A cautious planning
  assumption is that assessment-to-ready-to-install cycle time can fall
  by 15% to 25% from evidence handling alone, subject to Phase 1
  measurement; visit duration is largely unchanged.

`Head of Building Safety and Compliance` was asked: if resident and
installer photos routinely showed damp, mould, unsafe electrics or
fire-safety issues while an assessment was in progress, how should the
platform route them so the Awaab's Law clock is respected without
suppressing the retrofit process?

* Sector-informed hypothesis: every inbound photo channel needs a
  raise-only hazard signal scan and a hard split from the retrofit
  workflow. When any content matches the hazard signal set, a hazard case
  is opened in the repairs system with the awareness timestamp taken from
  the earliest evidence of arrival, not from the moment a human triager
  reads it. The retrofit safety hold flag is set on the property lifecycle
  record. The retrofit workflow continues its non-safety steps but cannot
  release works until the hold clears. AI decides nothing about the
  hazard; it just makes sure the case, the timestamp and the hold exist.

### Revised Verdict

Bounded AI inside workflow, at recommend level for the evidence
assessment. The augmentation widens what bounded AI can usefully check
(hazard, ventilation, higher-risk features, site-photo-versus-invoice
consistency), but the request stays a workflow with named professionals
in it, not an end-to-end agent. The autonomy level in the original case
study (L3, coordinator approves) can stand for pre-filling; it should not
be lifted for the evidence assessment itself.

### Stop Criteria for the App-Fed Evidence Assessment

* Stop if the AI records a site observation that no photo, sensor or note
  supports
* Stop if a hazard signal is generated but no case, timestamp or hold is
  created
* Stop if the pre-fill or evidence assessment removes an assessor from
  the pathway rather than reallocating their time
* Stop if the review of AI drafts takes as long as the manual pre-visit
  work it replaces

## Grant and Funding Agent

### What-If Augmentation

Installers submit structured digital invoices through the app, with
itemised measures, product identifiers, serial numbers, dates and
locations. Each line is linked to the geotagged install evidence, the
measure-specific decision record and the assessment. The four-state
grant ledger consumes these as an evidence pack. The AI drafts claim
packs and reporting from the ledger.

### Would It Remove the Original Blockers?

The original blockers were: bidding, match funding, certifying claims,
submitting and recording receipts stay with humans who hold financial
authority; agent-produced figures cannot be audited; reporting is a
data-lineage problem; and the funding route materially affects whether
"drafting" is worth much (formula allocations in Greater Manchester and
the West Midlands, competitive bids elsewhere).

The augmentation directly attacks the data-lineage problem. It does not
change the authority arrangements. It also does not turn an unsecured
opportunity into an award: the addendum's GBP 40 million line remains an
opportunity until Proper North Homes evidences an executed award.

### Clarification Questions to the Company Agents

`Head of Finance, Capital and Grants` was asked: if every installer
invoice arrived structured and reconciled to a geotagged evidence pack,
what is the highest autonomy level the ledger and drafting step could
run at before Finance loses audit control?

* Sector-informed hypothesis: draft only, with Finance signing every
  claim. Structured invoices raise claim quality and reduce Finance's
  review time, but the finance authority acts (certify, submit, accept
  receipt) are personal responsibilities under the delegated authority
  matrix and, where applicable, funder terms. The addendum's stop
  criterion for the Grant and Funding module (Finance's net review time
  must fall by at least 25%) becomes more testable with structured
  invoices, not more permissive. There is also a Construction Act payment
  notice question if the app becomes the interpreted "application for
  payment" channel; that needs Legal.

`Head of Procurement and Contract Management` was asked: could the
requirement for a structured, geotagged evidence pack be introduced
through PAS 2035 contracts and framework mini-competitions without
excluding small installers who are commonly used?

* Sector-informed hypothesis: yes as a contractual expectation, subject
  to a transition period, a supplied evidence template and an assisted
  route for installers without smartphone workflows. Enforcing it from
  day one would probably shrink the supplier pool. Procurement Act 2023
  route selection and the risk that the app or its data terms count as a
  material contract modification for existing framework calls need Legal
  review before rollout.

### Revised Verdict

Bounded AI inside workflow, only after the four-state ledger exists.
Structured invoices and linked evidence make the ledger and the Finance
review faster and more defensible; they do not turn Grant and Funding
into an end-to-end agent. The Phase 1 comparator (ledger alone) becomes
more competitive, not less, because a lot of the value the "agent" was
supposed to deliver actually comes from the invoice format.

### Stop Criteria for the App-Fed Grant Module

* Stop if invoice parsing produces any figure that cannot be traced to
  the source document
* Stop if the AI recommends a claim line without a matching accepted
  evidence pack
* Stop if the app becomes the sole permitted channel for installer
  invoices without a Legal review of the payment-notice implications

## Contractor and Resident Coordination Agent

### What-If Augmentation

Contractors publish committed capacity through an installer app or an
existing scheduling system with an integration. Residents use a Proper
Warm app to view proposed slots, record measure-specific consent,
withdraw consent, register accessibility adjustments, and see who is
coming. Installers on arrival open the appointment, capture a geotagged
proof-of-visit photo and log the outcome against fixed codes. Housing
officers see the same log.

### Would It Remove the Original Blockers?

The original blockers were: an agent cannot secure consent; a failed
visit is not a refusal; committing capacity and instructing contractors
are contract-manager acts; no evidence of a market of scheduling APIs;
putting utilisation and resident choice in one agent creates a conflict
of interest.

The augmentation genuinely helps two of these. Geotagged proof-of-visit
plus a fixed outcome-code list makes "no-access equals refusal" much
harder, because a no-access visit is now a timestamped, located event
routed to a named officer (BRD BR-020 legacy ID). A resident app that
captures measure-specific consent, if designed with an explicit "do not
consent" and "withdraw consent" path and non-digital fallbacks, gives
the deterministic decision record real teeth.

It does not remove the other blockers. The AI still cannot instruct
contractors or vary scope, and there is still a conflict of interest if
supplier utilisation and resident choice are optimised together.

### Clarification Questions to the Company Agents

`Head of Resident Engagement and Insight` was asked: if the resident
consent flow lived in a Proper Warm app, what would you require in the
design so digital consent does not become the default expectation and
excluded households do not lose their offer?

* Sector-informed hypothesis: every measure-specific consent has an
  equally weighted paper, phone and in-person route with the same
  wording, the same right to withdraw and the same audit trail; the app
  never marks a resident as harder to serve for using a non-digital
  route; adjustments recorded once flow to every future contact; and no
  contractor visit is scheduled until an explicit affirmative consent
  exists in the record, from any channel. Silence, implied consent from
  access for a survey and click-through terms of service are not
  consent (BRD BR-011, BR-013 legacy IDs).

`Neighbourhood Housing Officer` was asked: does a geotagged proof-of-
visit and fixed outcome-code list remove the risk that a missed visit
is silently reclassified as refusal, or are there frontline situations
that would still fall between the codes?

* Sector-informed hypothesis: proof-of-visit removes the "was the visit
  even attempted" question, which is the source of the worst
  misclassifications. Between-code cases still exist: household in
  crisis, safeguarding concern discovered on the doorstep, contractor
  arriving without notice, wrong address, subcontractor sent when the
  named installer expected, or resident asking to speak to the housing
  officer first. The design must let the installer log "handoff to
  officer" as an outcome code and must not let the AI reclassify a
  handoff as a refusal.

`Head of Procurement and Contract Management` was asked: which
contractors could commit capacity through the app or an API, and what
contract change would that require?

* Sector-informed hypothesis: large national and regional installers
  with existing job-management platforms can integrate through an API,
  probably at the price of a paid connector. Small local installers can
  publish committed capacity through a lightweight app with SMS or
  email fallback. Both changes are contractable through the standard
  work order and appointment outcome codes in the shared foundation and
  through a KPI-linked payment schedule. Procurement Act 2023
  modification questions on existing framework calls remain and need
  Legal.

### Revised Verdict

Split in two, as in the original challenge. The augmentation strengthens
the deterministic decision record and the no-access handling, and
narrows the useful scope of AI to drafting, translation, routing and
slot suggestion inside committed capacity. It does not create an
end-to-end agent, and it does not resolve the utilisation-versus-choice
conflict of interest.

### Stop Criteria for the App-Fed Coordination Module

* Stop if any consent is recorded from silence, an implied action or
  click-through terms
* Stop if a no-access or handoff outcome is converted into a refusal by
  any automated step
* Stop if the AI suggests slots against uncommitted capacity or an
  active safety hold
* Stop if measured outcomes diverge between digital and non-digital
  residents

## Quality Verification Agent

### What-If Augmentation

The installer uploads a per-measure evidence pack with geotagged photos
of substrate, install, commissioning, product plates and serial
numbers. The resident is asked to upload a small number of follow-up
photos after 24 hours and after 6 weeks. Structured commissioning data
(for example airflow rate, mean air temperature, pressure test result)
arrives from installer equipment. Post-retrofit sensors have a device
register with calibration and validity status. AI checks the pack
against the per-measure evidence schedule, flags mismatched serials,
dates or locations, and looks for defect patterns across installers,
products or archetypes. The addendum's typed decision-model idea
(IDEA-001) sits here.

### Would It Remove the Original Blockers?

The original blockers were: autonomous flags are acceptable only if a
flag adds work to a human queue; the real risk is a pack with no flags
being read as proof of quality; the competent quality authority keeps
acceptance and defect closure; a normal sensor reading cannot override
a resident report; sensors have their own validity problems; Awaab's
Law Phase 1 guidance says a sensor risk notification does not by itself
make the landlord aware
([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
section 3 and section 3.5).

The augmentation reduces the "no flags means quality" risk in one
specific way. If the pack is complete against the per-measure evidence
schedule, provenance-checked and reconciled with the invoice, a
"nothing to flag" outcome is stronger than it was, but it is still not
acceptance. It also gives the pattern-detection module real material
to work with, because raise-only signals across installers and
archetypes need volume and consistency to be useful.

It does not remove the other blockers. Resident reports still take
precedence over sensor readings. Acceptance still belongs to the
competent quality authority.

### Clarification Questions to the Company Agents

`Head of Building Safety and Compliance` was asked: with a
provenance-checked, per-measure evidence pack, could raise-only AI
flags safely move from L4 (autonomous flags into a queue) to a slightly
higher autonomy, for example holding payment automatically until a
human closes the flag?

* Sector-informed hypothesis: no. Holding payment is a
  contract-manager act with commercial consequences and, potentially,
  Construction Act payment-notice implications. Even where the flag
  seems safety-critical, the AI should raise the flag, the human
  should decide the hold. The gap between "raise" and "act" is what
  keeps the quality authority intact. A better use of the richer input
  is to make the flag queue triaged (safety, evidence, invoice
  mismatch) so that competent inspectors see the safety flags first.

`Head of Procurement and Contract Management` was asked: could per-
measure geotagged photo packs and structured commissioning data be
contracted for through PAS 2035 and standard work orders, and what
would that mean for payment gates?

* Sector-informed hypothesis: yes, as a contractual condition of a
  payment gate rather than as an AI-driven withhold. The evidence
  schedule already exists in the shared foundation; the contract makes
  the pack a condition of the milestone claim. Payment is released by
  the named quality authority once the pack is accepted, whether that
  acceptance is preceded by AI checks or not. The commercial change is
  in the contract, not in the AI.

`Data and Performance Lead` was asked: does structured commissioning
data plus a sensor validity register produce enough clean device-months
for the flagging model to work at recommend level?

* Sector-informed hypothesis: probably not in the first 12 months.
  Sensor coverage, calibration, heating-season alignment and consent
  variability mean the recommend-level flagging model needs a
  deliberate reference cohort with baseline readings and an independent
  inspection sample. Without that, false-flag and missed-flag rates
  cannot be reported honestly. This supports the Data Lead's earlier
  divergence (recommend, not L4) rather than resolving it.

### Revised Verdict

Bounded AI inside workflow, unchanged in kind, stronger in what it can
usefully check. Autonomy stays at raise-only flags. The augmentation
strengthens the case for the typed decision-model approach in IDEA-001
for evidence checks and defect-pattern detection, and it makes the
sampling model in the shared foundation more defensible.

### Stop Criteria for the App-Fed Quality Verification Module

* Stop if any safety-critical defect caught by humans is missed
* Stop if an evidence pack with no flags is treated as acceptance
* Stop if AI raises a payment hold, a defect notice or a claim rejection
  without a human decision
* Stop if the sensor validity register is not maintained and used to
  qualify every sensor-based flag

## Programme Supervisor and Damp-and-Mould Loop

### Programme Supervisor

The augmentation for the supervisor is that every event from the apps
above (photo upload, invoice line, appointment outcome, consent action,
capacity commitment) is keyed to the property lifecycle state machine
and to the delegated-authority matrix. The supervisor sees a live view
of who owns the next step, which clocks are running, which gates are
open, which items are held.

The augmentation makes the case for a conventional workflow engine
stronger, not weaker. Richer events help a state machine; they do not
turn one into an autonomous supervisor. AI could later summarise
exceptions from the controlled records, as in the original challenge.

`Executive Director of Assets` was asked: with richer events, could the
supervisor role move from workflow engine to an AI orchestrator, or
does the accountability model still require named owners at every
gate?

* Sector-informed hypothesis: named owners are required at every gate
  regardless of how rich the events are. The regulator, funder and
  auditor need to see who decided what, when and on what evidence. AI
  orchestration would create a supervision layer that no one signs.
  The right pattern is a workflow engine with an AI summarisation
  module for board and executive narratives.

Stop if any AI summary misstates a hold, a clock, an owner or a
consent status.

### Damp-and-Mould Loop

The augmentation is a resident and contractor app with geotagged
hazard photos, a mandatory hazard question on every contact, and
same-visit reporting clauses in contractor agreements. The Phase 1
timescales are: emergency hazards investigated and made safe within
24 hours; significant hazards investigated within 10 working days;
written summary within 3 working days; safety work within 5 working
days; supplementary works started within 12 weeks
([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
section 1.4 and section 3).

The augmentation gives the statutory clock a much earlier awareness
timestamp for any hazard that appears in a photo, note or contractor
form. That is a benefit and a risk. Benefit: fewer missed reports and
a defensible awareness date. Risk: the landlord is aware from the
moment content arrives, whether or not a human has read it, so
retention, triage and duty routing must run in near real time.

`Head of Building Safety and Compliance` was asked: does an
always-on evidence channel accelerate compliance with Phase 1, or
does it increase the volume of clocks the association is expected to
meet?

* Sector-informed hypothesis: both. Awareness moves earlier, which
  starts more clocks, which raises the risk of missed statutory
  deadlines if triage and inspection capacity does not scale. The
  evidence in the same channel makes it easier to prove the clock
  was met when it was. The net effect depends on Proper North Homes'
  current damp and mould volumes and inspection capacity, which are
  Unknown company details.

`Neighbourhood Housing Officer` was asked: how should a hazard photo
from a retrofit app become one timed case, given that residents may
also report the same hazard through the repairs line or a housing
officer visit?

* Sector-informed hypothesis: one damp intake route with strict
  deduplication, keyed to the property and to the earliest awareness
  timestamp of any channel. The retrofit app never opens a second
  case; it links to the existing one. The retrofit safety hold is
  set from the case, so the retrofit workflow always sees the hold
  even if the case moves through the repairs service. Housing
  officers keep the frontline decision on whether a report needs
  urgent visit.

### Revised Verdict for Both

Do not build as agent. The augmentation strengthens the case for a
workflow engine and a statutory clock in the repairs service, both of
which are in the shared foundation.

Stop if any AI output delays, suppresses or closes a clock; if
awareness timestamps are set from human review rather than from
arrival; or if the retrofit app opens a duplicate hazard case.

## Cross-Cutting Findings

Two threads run through every revised verdict.

* The augmentations do not create new agents. They enrich the same
  shared foundation the original challenge identified: property
  master, hazard case record, measure-specific decision record,
  committed-capacity register, per-measure evidence schedule and
  four-state grant ledger. Where richer inputs help most, they help
  the foundation, not the agent layer.
* The augmentations expand governance duties before they expand
  autonomy. Photos, structured invoices, capacity feeds and consent
  events all bring in Article 9 data, Awaab's Law awareness,
  Construction Act payment questions and Procurement Act 2023
  modification questions. Every added input needs Data Protection,
  Legal, Building Safety and Procurement review before the module
  runs live.

### Recurring Bounded AI Candidates, Refined

The five recurring bounded AI candidates from the original challenge
survive intact. The augmentations sharpen three of them:

1. Reconciling records and flagging missing data across legacy
   sources, now including provenance-checked evidence from apps
2. Reading unstructured evidence against fixed checklists, now
   extended to geotagged photo packs, structured invoices and
   commissioning data
3. Drafting accessible content from controlled records, unchanged
4. Routing inbound messages to staffed queues, now including inbound
   photo channels and their hazard signal
5. Raise-only signal scanning for missed hazard reports, missed
   handoffs and defect patterns, now with volume and consistency to
   support recommend-level flagging in Quality Verification once a
   reference cohort exists

### Value Test and Stop Criteria

The value tests and stop criteria for the augmentations are the same
as the ones in the original challenge, plus these additions:

* Every augmented module must publish a false-provenance and false-flag
  rate against a seeded test set before live use
* Every augmented module must run a digital-exclusion equity check by
  age, disability, language and channel and stop if outcomes diverge
* Every augmented module must record the Awaab's Law awareness
  timestamp from arrival, not from human review
* Every augmented module must pass a Data Protection Impact Assessment
  including retention, redaction and resident right-to-decline

## Questions for Proper North Homes

Each augmentation depends on an unknown company detail. The most
important questions to Proper North Homes, in priority order, are:

| Priority | Question | Why it matters |
| --- | --- | --- |
| 1 | Does the association have an approved lawful basis, DPIA and retention model for a resident app that captures photos and vulnerabilities? | Every augmentation above depends on it |
| 2 | What share of contractor capacity today is with installers who could integrate an app or API, and what does the transition look like for the rest? | Sets the feasible pace of the coordination and quality modules |
| 3 | Which system will own the property lifecycle state machine and the hazard case record, and who is accountable for its data quality? | The augmentations all key to it |
| 4 | Does the association hold an evidenced WH:SHF Wave 3 award, and under which route? | Determines whether the grant module is worth the augmentation cost |
| 5 | What is the current damp and mould volume and inspection capacity, and how would it scale if awareness moved earlier through app channels? | Determines whether the Awaab's Law augmentation reduces or increases the risk of missed clocks |

## Limitations

* The role agents have no access to Proper North Homes' systems,
  contracts, resident base or supplier arrangements, so this study does
  not establish feasibility, lawfulness or affordability.
* The regulatory citations are from the local snapshots and were not
  checked against the official sources online on 2026-09-27. Legal,
  Procurement and Data Protection review is needed before any of these
  augmentations goes live.
* The augmentations were tested one at a time. Interactions between
  them (for example, a resident app used for both consent and hazard
  reporting) need a separate cross-module Data Protection and safety
  review.
* IDEA-001 (typed decision models) is referenced as a candidate
  implementation for the flag- and route-heavy modules. It remains an
  unvalidated proposal in the
  [Idea Register](../../../ideas/idea-register.md).

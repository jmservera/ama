---
title: Agent What-If Study
description: What-if session on the Agent Request Challenge, running multiple augmentation scenarios per requested agent to test whether any moves them closer to a viable agentic end-to-end
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

That worked example is only one of many plausible augmentations. This page
therefore runs several distinct what-if scenarios for each requested agent,
not one. Each scenario:

* Specifies a concrete augmentation, so the analysis is not about "more AI"
  in the abstract
* Asks whether the augmentation removes any of the reasons the original
  challenge rejected end-to-end autonomy
* Puts one focused clarification question to the relevant `company-*` role
  agents and records their sector-informed answer
* States a scenario-level verdict against the original challenge

After the individual scenarios each section closes with an aggregate
verdict for the agent as a whole.

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

| Requested agent | What-if scenario | Original verdict | Revised verdict after augmentation |
| --- | --- | --- | --- |
| Stock Prioritisation | 1. Resident and inspection app with geotagged condition photos, plus a resident-declared vulnerability channel with UK GDPR Article 9 controls | Do not build as agent | Unchanged. Better inputs improve the scoring model but the ranking is still arithmetic and the cohort policy is still a Board decision |
| Stock Prioritisation | 2. Smart-meter half-hourly reads (with consent), EPC recommendations register and fuel-poverty proxies fused into the priority score | Do not build as agent | Unchanged. Fusion helps the arithmetic; ranking, weights and lawful basis stay with the Board and the DPO |
| Stock Prioritisation | 3. Per-archetype digital twin with parametric energy modelling that returns a confidence-scored EPC-C pathway per property | Do not build as agent | Unchanged. A twin is a design and appraisal tool; it does not replace surveys, cohort policy or eligibility rules |
| Assessment | 1. Assessor, resident and installer app that uploads geotagged photos and structured invoice data against a per-measure evidence schedule | Bounded AI inside workflow, limited to pre-filling sourced facts | Unchanged in kind, wider in scope. Provenance-checked evidence could support pre-populated hazard, ventilation and higher-risk building flags, but site observation and PAS 2035 sign-off stay with the assessor and coordinator |
| Assessment | 2. On-site structured scanning (LiDAR room capture, thermal imagery, moisture pins) that pre-populates fabric geometry and condition into PAS 2035 templates | Bounded AI inside workflow | Unchanged in kind. Measured geometry reduces manual capture time; the assessor still interprets condition, ventilation and higher-risk features |
| Assessment | 3. Pre-visit AI triage from asset, repairs, EPC and open-source data, producing a proposed PAS 2035 risk path for coordinator review | Bounded AI inside workflow | Unchanged in kind. Triage speeds coordinator preparation; the coordinator still sets the risk path |
| Grant and Funding | 1. Structured digital invoices with installer VAT, product and serial data, linked to the geotagged install evidence | Bounded AI inside workflow, only after the ledger exists | Unchanged. Better inputs raise claim quality but do not replace the four-state ledger, versioned eligibility rules or Finance authority |
| Grant and Funding | 2. Direct funder-portal, TrustMark and MCS integrations turning the ledger into a submit-ready pack the moment evidence is accepted | Bounded AI inside workflow | Unchanged. Faster submission still needs Finance certification and, where applicable, funder terms; opportunity is not an award |
| Grant and Funding | 3. Continuous eligibility monitoring that reflects scheme rule changes in real time, with plain-language explanations for each home | Bounded AI inside workflow | Unchanged. Live eligibility helps Finance and Programme; it does not decide eligibility |
| Contractor and Resident Coordination | 1. Contractor scheduling and capacity feeds, resident app for consent, adjustments and appointment outcomes, geotagged proof-of-visit | Split in two; bounded AI on both sides | Unchanged. Strengthens deterministic decision record and reduces "no-access equals refusal" errors, but consent, contract instructions and safeguarding stay human |
| Contractor and Resident Coordination | 2. Multi-supplier capacity mesh with automated re-routing across a preferred-supplier list under a KPI-linked framework | Split in two | Unchanged. Re-routing is a contract-manager act; the mesh recommends, the contract manager instructs |
| Contractor and Resident Coordination | 3. Multi-channel resident concierge (voice, WhatsApp, SMS, letter, in-person) writing to one contact log and one measure-specific decision record | Split in two | Unchanged. Reduces channel gaps and digital exclusion risks; consent, safeguarding and complaint handling stay human |
| Quality Verification | 1. Per-measure geotagged photo packs from the installer, resident-uploaded post-install photos, structured commissioning data, sensor validity register | Bounded AI inside workflow. Flags can only raise concerns | Slightly stronger. Makes flagging model more useful, enables raise-only pattern detection, but acceptance and defect closure stay human |
| Quality Verification | 2. Independent robotic and drone inspection (thermal drone flyover, cavity borescope), producing a machine-readable inspection record | Bounded AI inside workflow | Slightly stronger for defect detection; results are evidence for the competent quality authority, not acceptance |
| Quality Verification | 3. Cross-installer benchmarking against an anonymised sector defect feed (for example TrustMark and MCS defect data) | Bounded AI inside workflow | Slightly stronger for earlier detection of systemic patterns; still raise-only |
| Programme Supervisor | 1. Photo, invoice and appointment events all keyed to the property lifecycle state machine | Do not build as agent | Unchanged. Richer events make the workflow engine more useful; they do not remove the need for named owners, gates and clocks |
| Programme Supervisor | 2. Always-on AI exception dashboard and board-narrative generator drafting daily executive summaries from controlled records | Do not build as agent | Unchanged. Summaries are drafts under human sign-off; they do not replace named accountability |
| Damp-and-Mould Loop | 1. Resident and contractor app with geotagged hazard photos and same-visit reporting | Do not build as agent; statutory clocks in the repairs system | Unchanged. Faster awareness capture is valuable, but Awaab's Law Phase 1 awareness and triage decisions stay with the landlord, not with an AI |
| Damp-and-Mould Loop | 2. Consented ambient sensors (temperature, humidity, VOC) as a raise-only early-warning across a defined cohort | Do not build as agent | Unchanged. A sensor risk notification does not by itself make the landlord aware; deployment needs a separate lawful basis and a DPIA |
| Damp-and-Mould Loop | 3. Contractor and repairs call-recording transcription with automatic hazard-signal extraction to catch reports made verbally | Do not build as agent | Unchanged. Extraction is a raise-only signal into human triage; it must never delay, reset or close a statutory clock |

## Value vs Complexity Quadrant

The quadrant plots every what-if scenario on business value (vertical
axis) against implementation complexity (horizontal axis). The top-left
(high value, low complexity) is the target quadrant. Scenarios there
should be considered first; scenarios in the bottom-right (low value,
high complexity) should be deferred or dropped.

Each scenario is labelled by agent initial and scenario number:

* SP1, SP2, SP3: Stock Prioritisation what-ifs 1, 2, 3
* AS1, AS2, AS3: Assessment what-ifs 1, 2, 3
* GF1, GF2, GF3: Grant and Funding what-ifs 1, 2, 3
* CO1, CO2, CO3: Contractor and Resident Coordination what-ifs 1, 2, 3
* QV1, QV2, QV3: Quality Verification what-ifs 1, 2, 3
* PS1, PS2: Programme Supervisor what-ifs 1, 2
* DM1, DM2, DM3: Damp-and-Mould Loop what-ifs 1, 2, 3

Value and complexity are scored `H`, `M`, `L` from the augmentation
analysis in each scenario section, the addendum's stop criteria and
the regulatory citations. Scoring is deliberately coarse; the aim is
to sequence scenarios, not to price them. The target quadrant contains
scenarios that are at least `M` value and at most `M` complexity, with
at least one axis at its favourable extreme (`H` value or `L`
complexity); this is why AS1, QV1 and DM1 (all `H/M`) sit there
alongside PS1 (`H/L`) and GF1 (`M/L`).

### ASCII Quadrant

The chart is a 3-by-3 grid on value (rows) and complexity (columns).
The top-left cell is the target; the bottom-right cell is defer.

```text
                             Implementation complexity
                       LOW              MEDIUM             HIGH
                  +----------------+----------------+----------------+
             HIGH |  PS1           |  AS1           |  SP2           |
                  |                |  QV1           |  QV2           |
                  |                |  DM1           |  DM2           |
                  |                |                |  DM3           |
                  +----------------+----------------+----------------+
  Business   MED  |  GF1           |  SP1           |  GF2           |
  value           |  CO1           |  GF3           |                |
                  |                |  CO3           |                |
                  |                |  PS2           |                |
                  +----------------+----------------+----------------+
              LOW |                |  QV3           |  SP3           |
                  |                |                |  CO2           |
                  |                |                |  AS2           |
                  |                |                |  AS3           |
                  +----------------+----------------+----------------+
                    TARGET zone      Housekeeping       Big-bet /
                    (top-left)       or selective       Defer
                                     bets (middle)      (right)
```

Read the grid by cell:

* Target zone (top row and left column): do first. PS1 (H/L), AS1
  (H/M), QV1 (H/M), DM1 (H/M), GF1 (M/L), CO1 (M/L).
* Big-bet zone (top-right cell, H/H): only after the shared
  foundation and the target zone are stable. SP2, QV2, DM2, DM3.
* Housekeeping or selective bets (middle band, M value): do
  opportunistically. SP1, GF3, CO3, PS2 sit at M/M; GF2 at M/H is a
  selective bet.
* Defer zone (bottom row and right column with L value): do not
  start without a specific triggering condition. QV3 (L/M), SP3
  (L/H), CO2 (L/H), AS2 (L/H), AS3 (L/H).

### Scoring Table

| ID | Scenario | Value | Complexity | Rationale |
| --- | --- | --- | --- | --- |
| SP1 | Resident and inspection app with geotagged photos and vulnerability channel | M | M | Better prioritisation inputs, but ranking is arithmetic; Article 9 handling and equity checks add real design work |
| SP2 | Smart-meter, EPC and fuel-poverty data fusion | H | H | Meaningfully improves cohort selection; DCC access, consent, Article 22 controls and fairness monitoring are heavy |
| SP3 | Per-archetype digital twin with parametric energy modelling | L | H | Useful for design and appraisal but does not remove the survey, cohort or eligibility blockers; modelling and calibration cost is high |
| AS1 | App-fed provenance-checked evidence into PAS 2035 templates | H | M | Directly shortens assessor review cycles; app and provenance stack are well-understood; DPIA and equity checks are the main lift |
| AS2 | On-site structured scanning (LiDAR, thermal, moisture, blower door) | L | H | Real time saving in fabric capture, but small addressable population, kit and training cost is high, and it does not remove sign-off |
| AS3 | Pre-visit AI triage across asset, repairs, EPC and open-source data | L | H | Speeds coordinator preparation; model risk on HRB and damp signals is significant; requires audited accuracy record before adoption |
| GF1 | Structured digital invoices with product and serial data | M | L | Clean lineage into the ledger; low technical cost; value ceiling set by the ledger itself |
| GF2 | Direct funder-portal, TrustMark and MCS integrations | M | H | Removes re-keying and speeds submission drafts; each integration is a separate governance and data-sharing exercise |
| GF3 | Continuous eligibility monitoring with plain-language explanations | M | M | Real value in catching mid-programme rule changes; rule pack versioning and immutable snapshots are non-trivial |
| CO1 | Contractor capacity feeds and resident app for consent and outcomes | M | L | High operational uplift once the shared foundation is in place; app tech is mature; consent-parity and non-digital fallbacks are the design work |
| CO2 | Multi-supplier capacity mesh with automated re-routing | L | H | Attacks single-supplier fragility, but Procurement Act 2023 route selection, resident re-consent and conflict-of-interest controls are heavy |
| CO3 | Multi-channel resident concierge with unified contact log | M | M | Real accessibility uplift; requires fairness-gap monitoring and clear human-send rules for sensitive categories |
| QV1 | Per-measure geotagged evidence packs plus structured commissioning data | H | M | Directly strengthens raise-only flagging and defect-pattern detection; contract change and evidence schedule already exist in the shared foundation |
| QV2 | Independent drone and robotic inspection sampling | H | H | Genuine independent evidence source and stronger defect-pattern signal; airspace, insurance, consent and separate procurement are heavy |
| QV3 | Cross-installer benchmarking against sector defect feeds | L | M | Useful additional signal, but sector feeds may be biased; supplier right-of-challenge and data-sharing agreements limit the value ceiling |
| PS1 | Photo, invoice and appointment events keyed to the lifecycle state machine | H | L | The single highest-leverage change in the study; a conventional workflow engine consumes richer events with almost no new AI risk |
| PS2 | Always-on AI exception dashboard and board-narrative generator | M | M | Real reporting uplift; needs prompt or model versioning, independent audit reconciliation and executive sign-off |
| DM1 | Resident and contractor hazard app with geotagged photos | H | M | Materially earlier awareness for Awaab's Law; requires real-time triage capacity and strict one-case-per-property deduplication |
| DM2 | Consented ambient sensors as raise-only early warning | H | H | High potential value in silent-hazard detection; consent, DPIA, fairness and threshold governance are all substantial |
| DM3 | Call-recording transcription with hazard-signal extraction | H | H | Catches hazards mentioned verbally on other calls; Article 9 data, notification and retention model are heavy |

### Sequencing Implied by the Grid

Combining the grid with the aggregate verdicts, a defensible sequence
is:

1. Shared foundation first (property master, lifecycle state
   machine, hazard case record, evidence schedule, grant ledger,
   capacity register). Nothing in the grid delivers its full value
   until this exists.
2. Target zone: PS1, then AS1, QV1, DM1, then GF1 and CO1. PS1 is
   the load-bearing enabler; the others depend on the workflow
   engine (PS1) to carry their events safely.
3. Middle band, opportunistically: SP1, GF3, CO3, PS2 (all M/M),
   guided by digital exclusion and consent constraints; GF2 (M/H)
   only alongside a clearly-scoped funder integration.
4. Big-bet zone (H/H), only with explicit business-case sign-off
   and a completed DPIA: DM3 and DM2 for hazard detection uplift,
   then SP2 for cohort prioritisation, then QV2 for independent
   quality evidence.
5. Defer zone: QV3, SP3, CO2, AS2, AS3. Only revisit if a specific
   triggering condition (for example evidenced supplier fragility
   for CO2, or evidenced coordinator preparation bottleneck for
   AS3) emerges.

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

### What-If 1: Resident and Inspection App

#### Augmentation

The programme offers residents a Proper Warm app to report condition
issues with geotagged photos, note vulnerabilities and adjustments, and
consent to any onward use. Housing officers and stock-condition surveyors
use the same app during visits. The platform normalises these into the
property master with source, date, capture location and confidence.

#### Would It Remove the Original Blockers?

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

#### Clarification Questions to the Company Agents

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

#### Scenario Verdict

Do not build as agent. The augmentation belongs to the shared foundation
(property master and hazard case record), not to a Stock Prioritisation
agent. If the app exists, its outputs feed the deterministic rules model
and a bounded AI reconciliation module already scoped in the original
challenge.

### What-If 2: External Data Fusion

#### Augmentation

Proper North Homes negotiates data-sharing agreements to pull consented
smart-meter half-hourly reads (via the Data Communications Company or a
consented DNO route), the national EPC recommendations register,
DWP-derived fuel poverty proxies at postcode or LSOA level, and any
scheme-specific data pack from WH:SHF or its combined authority. The
priority score fuses these with the property master and hazard case
record. AI reconciles conflicts and drafts a plain-language explanation
for each home.

#### Would It Remove the Original Blockers?

Data fusion improves the arithmetic. It does not change the four earlier
blockers: weights are Board policy; eligibility is deterministic;
Article 9 data still needs a lawful basis; and hazards still take the
statutory route. Smart-meter consent is on the resident, not the
landlord, so coverage will be partial and skewed.

#### Clarification Questions to the Company Agents

`Head of Finance, Capital and Grants` was asked: would fused smart-meter,
EPC-register and fuel-poverty data raise or lower the strength of a
grant-eligibility narrative for a given cohort?

* Sector-informed hypothesis: raise it, but only for the homes in the
  cohort with consented smart-meter data and a live EPC. For the rest,
  the narrative is no stronger than today. The grant case has to be
  built on the shared cohort, not on the best-instrumented subset. This
  also creates a fairness question if consented properties are more
  likely to attract funded work than unconsented ones.

`Head of Building Safety and Compliance` was asked: does fusing DWP-
derived fuel poverty proxies with vulnerability data create a solely
automated significant decision under UK GDPR Article 22?

* Sector-informed hypothesis: it can. A ranking that materially decides
  whether a household is offered retrofit is a significant decision. If
  a proxy plus a vulnerability weight decides that ranking without a
  human review path, Article 22 is engaged and needs a lawful basis and
  meaningful human involvement. This is a DPO decision, not a technical
  one.

#### Scenario Verdict

Do not build as agent. Fusion strengthens the deterministic model and
the reconciliation module; it does not create a new agent and it
increases Article 22 and fairness risk that must be resolved before use.

### What-If 3: Per-Archetype Digital Twin

#### Augmentation

The programme builds a parametric energy and moisture model per
archetype (for example, 1930s solid-wall terrace, post-war
non-traditional, 1960s system-built high-rise), calibrated against
sampled surveys, and returns a confidence-scored EPC-C pathway per
property with expected cost, comfort and moisture outcomes. Prioritisation
uses the twin's confidence score alongside the deterministic rules
model.

#### Would It Remove the Original Blockers?

A twin is a design and appraisal tool. It could reduce reliance on
survey-derived assumptions for planning, and it could sharpen bundle
selection at archetype level, but it does not replace physical surveys
for individual homes and it does not resolve cohort policy or
eligibility rules. It introduces model risk: if the archetype average
is used to deprioritise a specific home, that is a solely automated
significant decision.

#### Clarification Questions to the Company Agents

`Retrofit Programme Manager` was asked: could a confidence-scored twin
pathway safely inform work-package bundling at archetype level, or
would that still need a per-property survey?

* Sector-informed hypothesis: yes for early scoping and design-package
  choice at archetype level, subject to sampled physical validation and
  a documented rule that no home enters delivery without a PAS 2035
  assessment. The twin can help decide which archetypes to prioritise
  procurement for, but a home's actual works order comes from the
  assessor and coordinator, not the twin.

`Executive Director of Assets` was asked: is a twin-derived pathway
acceptable evidence for a Board cohort-approval paper, or does the
Board need physical survey evidence?

* Sector-informed hypothesis: acceptable for the cohort framing paper,
  with named sensitivity and model-risk sections and a clear statement
  that individual home decisions require survey evidence. Not
  acceptable as sole evidence for individual capital commitments.

#### Scenario Verdict

Do not build as agent. The twin is a design tool for the shared
foundation. It can inform cohort framing under sensitivity and
professional review; it cannot decide priority or eligibility for
individual homes.

### Aggregate Verdict for Stock Prioritisation

Do not build as an end-to-end agent under any of the three scenarios.
Each of them enriches the deterministic scoring model and the shared
foundation; none of them removes the Board policy, eligibility rules,
Article 22 or Awaab's Law blockers.

### Stop Criteria Across All Stock Prioritisation Scenarios

* Stop if the app becomes the only way to report a condition issue
* Stop if resident photo uploads are not linked to the hazard case record
  and the Awaab's Law awareness timestamp
* Stop if resident-declared vulnerabilities are used in a solely
  automated significant decision without a documented lawful basis and
  DPIA
* Stop if fused external data materially affects priority or eligibility
  without a documented Article 22 human-review path
* Stop if a twin-derived pathway is used as sole evidence for an
  individual home's investment decision

## Assessment Agent

### What-If 1: App-Fed Provenance-Checked Evidence

#### Augmentation

The worked example from the project owner. The Retrofit Assessor, the
resident and the installer all use a Proper Warm app to upload evidence
against a per-measure PAS 2035 evidence schedule. Each upload carries
device attestation, EXIF GPS, capture time and app-signed provenance. The
platform matches each artefact to the property, the measure and the
appointment. Invoices are structured, with installer VAT number, product,
serial and unit price parsed and linked. The AI produces an evidence
assessment for the assessor: what evidence is present, what is missing,
what is inconsistent, and where site observation is still required.

#### Would It Remove the Original Blockers?

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

#### Clarification Questions to the Company Agents

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

#### Scenario Verdict

Bounded AI inside workflow, at recommend level for the evidence
assessment. The augmentation widens what bounded AI can usefully check
(hazard, ventilation, higher-risk features, site-photo-versus-invoice
consistency), but the request stays a workflow with named professionals
in it, not an end-to-end agent. The autonomy level in the original case
study (L3, coordinator approves) can stand for pre-filling; it should not
be lifted for the evidence assessment itself.

### What-If 2: On-Site Structured Scanning

#### Augmentation

The Retrofit Assessor carries a scanning kit: a LiDAR-capable phone or
tablet, a thermal camera, moisture pins, a blower-door adaptor, an
airflow meter and a borescope. On the visit the assessor captures room
geometry, U-values estimated from thermal transects, moisture readings,
airtightness where feasible and photographs of concealed elements. The
platform pre-populates PAS 2035 templates with measured geometry and
condition observations. AI reconciles the scan with existing asset
records and flags conflicts.

#### Would It Remove the Original Blockers?

Structured capture reduces the manual data-entry portion of the visit
and removes several classes of transcription error, but the interpretive
step (construction type, ventilation adequacy, higher-risk building
implications, likely design measures) still belongs to the assessor.
Measured U-values remain estimates unless properly instrumented and are
weak evidence for high-consequence decisions. Blower-door tests need
occupancy cooperation and produce results only when the fabric is in a
suitable state.

#### Clarification Questions to the Company Agents

`Retrofit Programme Manager` was asked: does measured geometry and
thermal imagery let the assessor sign off risk-path decisions in the
office rather than on site?

* Sector-informed hypothesis: no. The risk-path decision (Path A or B
  under PAS 2035, higher-risk building classification, presence of
  significant heritage or safety features) is a judgement based on the
  built form and its context. Scans support the judgement, but the
  assessor must still be able to inspect ambiguous items, discuss
  occupancy with the resident and observe features that scans miss.
  The office-based portion of the assessment gets shorter and better;
  the on-site portion stays.

`Head of Procurement and Contract Management` was asked: does mandating
scanning kit and workflows for the assessor pool constrain the
supplier market?

* Sector-informed hypothesis: yes for smaller assessor firms without
  the equipment, which is a real risk given PAS 2035 assessor capacity
  is already tight. A framework specification with a transition
  window, a supplied-kit option or a shared-kit pool by geography
  reduces the risk. Any imposed data format should follow an open
  standard, not a single vendor's file type.

#### Scenario Verdict

Bounded AI inside workflow. Better inputs make pre-population and
completeness-checking more useful; they do not lift the sign-off level
or move the visit indoors.

### What-If 3: Pre-Visit AI Triage

#### Augmentation

Before the assessor visits, AI reads the asset record, repairs history,
planned-maintenance plan, EPC and its recommendations, prior complaints,
open damp or safety cases, aerial imagery, planning history and any
consented smart-meter data. It produces a proposed PAS 2035 risk path,
a draft archetype match, a list of measures likely to be in scope, a
list of higher-risk building or heritage flags, and a set of questions
for the assessor to ask on site. The coordinator reviews and either
adopts, adjusts or rejects the proposal before dispatch.

#### Would It Remove the Original Blockers?

Triage tightens the pre-visit workflow and gives the coordinator a
concrete draft to work from. It does not remove the coordinator's
professional decision on the risk path, and it must not become the
default the coordinator waves through. The triage step is where
selection bias can enter the pipeline (properties with rich records get
richer triage) and where undocumented AI opinions can quietly become
decisions.

#### Clarification Questions to the Company Agents

`Retrofit Programme Manager` was asked: what evidence would you require
before an AI-proposed risk path could be adopted by the coordinator
without rework?

* Sector-informed hypothesis: an audited historical accuracy record
  against past coordinator decisions, published false-path rates, the
  coordinator's written confirmation for each adopted proposal, and a
  policy that a proposal cannot be adopted for higher-risk buildings
  or for properties with open safety cases without explicit
  coordinator review. The comparator is a coordinator working from the
  same records with no proposal; if the proposal does not measurably
  reduce coordinator time without lowering decision quality, it is
  not worth the risk.

`Head of Building Safety and Compliance` was asked: if the AI triage
missed a higher-risk building indicator or an open damp case, where
should accountability sit?

* Sector-informed hypothesis: with the coordinator, whose job includes
  independent verification of higher-risk building status and open
  safety cases before dispatch. AI triage is a draft, and drafts do
  not shift accountability. The safeguard is to require the
  coordinator to positively acknowledge the higher-risk building and
  open-hazard check at dispatch, whether or not AI made a proposal.

#### Scenario Verdict

Bounded AI inside workflow. Triage runs at recommend level, and the
coordinator's positive acknowledgement of higher-risk building and
hazard checks is required whether the triage flagged them or not.

### Aggregate Verdict for Assessment

Bounded AI inside workflow across all three scenarios, at recommend or
pre-fill level. Combined, the scenarios could plausibly meet the
addendum's 15% to 25% assessment-to-ready-to-install cycle-time target,
but none of them lifts the PAS 2035 sign-off model, and each of them
must be delivered without deepening supplier-market or Article 9
exposure.

### Stop Criteria Across All Assessment Scenarios

* Stop if the AI records a site observation that no photo, sensor or note
  supports
* Stop if a hazard signal is generated but no case, timestamp or hold is
  created
* Stop if the pre-fill or evidence assessment removes an assessor from
  the pathway rather than reallocating their time
* Stop if the review of AI drafts takes as long as the manual pre-visit
  work it replaces
* Stop if a structured scan is treated as a substitute for the on-site
  assessor visit rather than as evidence carried into it
* Stop if a proprietary scan format prevents the Retrofit Coordinator,
  the Retrofit Evaluator or a funder auditor from reading the raw
  evidence
* Stop if scanning kit is mandated in a way that excludes small PAS 2035
  installers without a supported transition path
* Stop if pre-visit AI triage output is adopted as the assessment path
  without the coordinator positively acknowledging HRB, damp-and-mould
  and vulnerability signals
* Stop if triage adoption rises without an audited record of triage
  accuracy against subsequent on-site findings, per archetype and per
  tenure

## Grant and Funding Agent

### What-If 1: Structured Digital Invoices

#### Augmentation

Installers submit structured digital invoices through the app, with
itemised measures, product identifiers, serial numbers, dates and
locations. Each line is linked to the geotagged install evidence, the
measure-specific decision record and the assessment. The four-state
grant ledger consumes these as an evidence pack. The AI drafts claim
packs and reporting from the ledger.

#### Would It Remove the Original Blockers?

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

#### Clarification Questions to the Company Agents

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

#### Scenario Verdict

Bounded AI inside workflow, only after the four-state ledger exists.
Structured invoices tighten data lineage without changing who certifies
or submits. The Phase 1 comparator (ledger alone) becomes more
competitive, not less.

### What-If 2: Funder-Portal, TrustMark and MCS Integrations

#### Augmentation

The four-state ledger is directly integrated with funder claim portals
(for example WH:SHF Wave 3 reporting), TrustMark lodgement and MCS
certification lookups. The Grant module fetches lodgement identifiers,
certificate statuses and funder-side receipt statuses automatically,
reconciles them line by line against the internal ledger and highlights
mismatches. Draft claims are pre-populated in the funder's own
schema.

#### Would It Remove the Original Blockers?

Not fully. It removes the manual re-keying and evidence-hunt work that
sits between the internal ledger and each funder's format, and it
narrows the window in which a lodgement or certificate can silently be
missing before Finance discovers it at claim time. It does not remove
the requirement for Finance to certify and submit under delegated
authority, and it does not remove the fact that some funder routes
(for example ECO or LADS successor schemes) apply different eligibility
tests to the same measure and are not internally consistent, so a
single automated pack cannot be reused verbatim across funders.

#### Clarification Questions to the Company Agents

`Head of Finance, Capital and Grants` was asked: which funder portal
would you accept the module writing to directly on your credentials,
and where must a human always paste and press "submit"?

* Sector-informed hypothesis: writes should be limited to draft or
  save-as-draft calls even when APIs allow submission. The named finance
  officer retains the physical act of submission, both to preserve the
  audit trail and to match funder terms of use that name a responsible
  officer. Read integrations (lodgement identifiers, certificate
  statuses, receipt statuses) are lower risk and give most of the
  reconciliation benefit.

`Chief Data and Digital Officer` was asked: if TrustMark and MCS
identifiers become the reconciliation key, what data-quality and change
management is required inside Proper North Homes before that key is
trusted?

* Sector-informed hypothesis: a controlled property and measure master
  where TrustMark lodgement identifiers and MCS certificate numbers are
  treated as authoritative external keys, plus a documented process for
  handling upstream corrections (revoked certificates, re-lodged jobs).
  Without that, mismatches from the funder side will be misread as
  installer error and generate spurious holds.

`Head of Procurement and Contract Management` was asked: does requiring
installers to keep TrustMark and MCS records synchronised on a defined
cadence constitute a change to existing PAS 2035 contracts?

* Sector-informed hypothesis: potentially a material change if enforced
  with new deductions or holdbacks, so it should be introduced through
  new contracts and mini-competitions rather than retro-fitted. Legal
  review under the Procurement Act 2023 is needed.

#### Scenario Verdict

Bounded integration and reconciliation, human submission. Adds material
lineage value and reduces the risk of late-discovered lodgement gaps,
but does not change autonomy on the certifying act.

### What-If 3: Continuous Eligibility Monitoring

#### Augmentation

The Grant module continuously re-evaluates every in-flight scheme
against a rules pack maintained by Legal and Finance. When guidance,
scheme rules, funder Q&A or interpretive updates change, the module
recomputes which live measures, addresses or claim lines are still
in-scope, and flags at-risk lines to Finance and the Coordinator with
the specific rule change cited.

#### Would It Remove the Original Blockers?

It attacks a different blocker: the risk that a scheme's interpretation
shifts under a live programme (a live risk on Wave 3 spend by 31 March
2028 and on any successor scheme). Without this, breaches are usually
detected at claim time. It does not remove authority blockers; it
raises the odds of catching a fatal-eligibility change in time to
adjust delivery.

#### Clarification Questions to the Company Agents

`Executive Director of Finance and Governance` was asked: are you
willing to accept an agent-generated "at risk" flag as the trigger for
pausing a live install, or must every pause be a human call?

* Sector-informed hypothesis: the flag is an input to a human pause
  decision, not a pause. Automatic pauses would create Construction Act
  and contractor-cost exposure. However, an audited "flag raised, human
  decision required within N working days" service level is
  appropriate.

`Head of Building Safety and Compliance` was asked: what regulatory
change categories must trigger a mandatory human review regardless of
model confidence (for example HRB scope, Awaab's Law scope, Decent
Homes Standard changes)?

* Sector-informed hypothesis: any change touching Building Safety Act
  in-scope buildings, Awaab's Law hazard scope or duties, Decent Homes
  Standard revisions, or PAS 2035 versioning should always route to a
  named human reviewer. Model confidence must not gate these; they are
  legal-review categories.

`Chief Data and Digital Officer` was asked: how do you version the rule
pack so that a claim submitted last month is judged against the rules
in force last month, not today's?

* Sector-informed hypothesis: rules must be immutable snapshots with
  effective dates, and every claim, hold and pause records the rule
  version applied. Without this, retrospective changes will corrupt the
  audit trail and Finance will lose confidence in the module.

#### Scenario Verdict

Bounded monitoring and alerting. Genuinely useful because it addresses
a risk humans currently manage by hope. Autonomy stays at proposal.

### Aggregate Verdict for Grant and Funding

None of the three scenarios makes an end-to-end Grant and Funding
agent responsible. Together they harden the four-state ledger with
better inputs (structured invoices), better integration (funder
portals, TrustMark, MCS) and better foresight (continuous eligibility
monitoring). The Phase 1 comparator is unchanged but its value ceiling
rises.

### Stop Criteria Across All Grant and Funding Scenarios

* Stop if invoice parsing produces any figure that cannot be traced to
  the source document
* Stop if the AI recommends a claim line without a matching accepted
  evidence pack
* Stop if the app becomes the sole permitted channel for installer
  invoices without a Legal review of the payment-notice implications
* Stop if the module submits (rather than drafts) to a funder portal
  under any credentials
* Stop if TrustMark or MCS identifiers become the reconciliation key
  without a documented process for upstream corrections
* Stop if continuous monitoring pauses works automatically rather than
  raising a flag for a human decision
* Stop if rule-pack versions are not immutable snapshots with effective
  dates recorded against each claim, hold and pause

## Contractor and Resident Coordination Agent

### What-If 1: Capacity Feeds and Resident App

#### Augmentation

Contractors publish committed capacity through an installer app or an
existing scheduling system with an integration. Residents use a Proper
Warm app to view proposed slots, record measure-specific consent,
withdraw consent, register accessibility adjustments, and see who is
coming. Installers on arrival open the appointment, capture a geotagged
proof-of-visit photo and log the outcome against fixed codes. Housing
officers see the same log.

#### Would It Remove the Original Blockers?

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

#### Clarification Questions to the Company Agents

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

#### Scenario Verdict

The augmentation strengthens the deterministic decision record and the
no-access handling. It narrows the useful scope of AI to drafting,
translation, routing and slot suggestion inside committed capacity. It
does not create an end-to-end agent.

### What-If 2: Multi-Supplier Capacity Mesh

#### Augmentation

Instead of one installer per work package per property, several
approved installers publish capacity into a shared committed-capacity
register keyed to archetype, measure and postcode area. The Coordinator
module proposes a matching against a defined objective (for example
minimise Awaab's Law breach risk, minimise cost within cap, respect
resident-chosen supplier). Assignment remains a human contract
manager's decision. The mesh gives resilience when one installer's
capacity collapses.

#### Would It Remove the Original Blockers?

Partially. It attacks single-installer bottlenecks and the "programme
stalls when a supplier folds" risk. It does not remove the requirement
that the contract-manager instructs works. It also introduces two new
risks: the utilisation-versus-choice conflict of interest gets sharper
(the mesh is very good at hiding resident preference behind aggregate
optimisation), and the mesh makes it easier to swap in an installer the
resident did not choose without explicit re-consent.

#### Clarification Questions to the Company Agents

`Head of Procurement and Contract Management` was asked: what
contractual model supports several installers publishing capacity to a
shared register without triggering Procurement Act 2023 modification
issues?

* Sector-informed hypothesis: a dynamic purchasing system or a
  framework with a defined mini-competition rule set (for example
  measure and archetype call-offs), designed from the outset with the
  capacity-mesh model in mind. Retrofitting this to existing framework
  calls is high risk. Terms of use and data terms for the register must
  be part of the agreement, not an afterthought.

`Head of Resident Engagement and Insight` was asked: when the mesh
proposes reassigning a household from installer A to installer B, what
must the resident be told and consulted on?

* Sector-informed hypothesis: any change of named installer requires
  positive re-consent from the resident, with a clear explanation of
  why the change is proposed and their right to keep the original slot
  even if that means waiting longer. Silent reassignment for
  utilisation reasons is not acceptable and would likely breach both
  the consumer standards and the deterministic decision record's
  spirit.

`Executive Director of Finance and Governance` was asked: what
conflict-of-interest controls are required so mesh optimisation does
not implicitly favour installers that maximise short-term utilisation
over installers with better quality or complaints records?

* Sector-informed hypothesis: the objective function must be published,
  reviewed by Audit and Risk, and must weight quality and complaint
  history explicitly; a periodic independent review of the mesh's
  proposed matchings against actual assignments is required; and
  finance cannot hold both the utilisation KPI and the objective
  function.

#### Scenario Verdict

Bounded matching-proposer inside a governed procurement model. Only
useful once What-If 1 is stable. Autonomy stays at proposal to the
contract manager, with explicit resident re-consent on any change of
named installer.

### What-If 3: Multi-Channel Resident Concierge

#### Augmentation

A concierge module handles resident communication across WhatsApp, SMS,
voice call, email, letter and doorstep visits, translating in and out
of the resident's preferred language, summarising into the deterministic
record, and offering the same consent options with identical wording on
every channel. AI drafts responses; humans send them for sensitive
categories.

#### Would It Remove the Original Blockers?

It attacks a real blocker (digital exclusion and language accessibility)
without moving decision authority. It does not remove the fundamental
constraint that consent, withdrawal and complaint handling remain
human-signed. Poorly designed, it can create a fairness gap: residents
whose interactions are AI-drafted may get faster or better-worded
responses than residents whose interactions rely on frontline officers.

#### Clarification Questions to the Company Agents

`Head of Resident Engagement and Insight` was asked: what categories of
resident contact must always route to a human before response, even if
the concierge could draft accurately?

* Sector-informed hypothesis: complaints, safeguarding, hazard reports,
  Awaab's Law-in-scope reports, requests to withdraw consent, requests
  for adjustments under the Equality Act 2010, tenancy-affecting
  matters, and anything mentioning suicide, self-harm, domestic abuse
  or a child at risk. AI may prepare a summary and a suggested reply
  but must not send.

`Chief Data and Digital Officer` was asked: how do you monitor and
correct for a fairness gap between AI-assisted channels and human-only
channels?

* Sector-informed hypothesis: measured outcomes (response time, first-
  time-fix rate, complaint escalation rate, satisfaction) split by
  channel and by protected characteristic, published to a governance
  forum. If a gap emerges, service level on the human channels is
  raised, not the AI channels throttled, so no resident is worse off
  for choosing a non-digital route.

`Neighbourhood Housing Officer` was asked: does the concierge risk
displacing the doorstep visit as a form of contact, and what would you
protect?

* Sector-informed hypothesis: yes if left unmanaged. Doorstep contact
  is the only route that finds hidden hazards, hoarding, safeguarding
  concerns and unreported disrepair. The concierge must not be a metric
  against which "avoided visits" is scored positively; a proportion of
  visits must remain scheduled as a matter of policy.

#### Scenario Verdict

Bounded AI translation, drafting and summarisation with human send on
sensitive categories. Real accessibility value if fairness monitoring
is in place. Autonomy stays low.

### Aggregate Verdict for Contractor and Resident Coordination

Split in two, as in the original challenge, remains right. The three
scenarios individually strengthen consent capture, capacity resilience
and accessibility. Together they do not create an end-to-end
Coordination agent, and they explicitly cannot resolve the
utilisation-versus-choice conflict of interest.

### Stop Criteria Across All Coordination Scenarios

* Stop if any consent is recorded from silence, an implied action or
  click-through terms
* Stop if a no-access or handoff outcome is converted into a refusal by
  any automated step
* Stop if the AI suggests slots against uncommitted capacity or an
  active safety hold
* Stop if measured outcomes diverge between digital and non-digital
  residents
* Stop if the capacity mesh reassigns a resident's named installer
  without explicit resident re-consent
* Stop if the mesh's objective function is not published, reviewed by
  Audit and Risk or weighted for quality and complaint history
* Stop if the concierge sends (rather than drafts) in any category on
  the always-route-to-human list
* Stop if "avoided visits" becomes a positive concierge metric

## Quality Verification Agent

### What-If 1: Per-Measure Geotagged Evidence Packs

#### Augmentation

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

#### Would It Remove the Original Blockers?

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

#### Clarification Questions to the Company Agents

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

#### Scenario Verdict

Bounded AI inside workflow, unchanged in kind, stronger in what it can
usefully check. Autonomy stays at raise-only flags. Strengthens the
case for the IDEA-001 typed decision model and the sampling model in
the shared foundation.

### What-If 2: Independent Drone and Robotic Inspection

#### Augmentation

Where property access and safety allow, a third party (not the
installer) uses drone photography, thermal imaging or roof-mounted
robotics on a sample of completed jobs. Structured outputs (thermal
delta by fabric zone, moisture trace, roof-line integrity check) feed
the raise-only flag queue independently of the installer's own pack.
The sample is stratified by archetype, installer and measure to
strengthen defect-pattern detection.

#### Would It Remove the Original Blockers?

It attacks the "installer marks their own homework" problem inside
What-If 1, and it shortens the loop between an emerging defect pattern
and a signal that survives challenge. It does not remove any of the
acceptance-authority or Awaab's Law blockers, and it introduces new
constraints: airspace, resident consent, insurance, safeguarding when
imaging can inadvertently capture people or interiors.

#### Clarification Questions to the Company Agents

`Head of Building Safety and Compliance` was asked: what conditions
must be met for independent drone or robotic imagery to be admissible
as evidence for a defect notice or refusal to accept?

* Sector-informed hypothesis: a documented scope, a competent
  inspector reviewing the imagery, a chain of custody for the raw
  files, and a resident-facing statement of what was captured and why.
  Imagery is evidence for a human decision, not itself an acceptance
  or rejection.

`Head of Resident Engagement and Insight` was asked: what consent and
notification model is required before drone or robotic inspection over
tenanted homes?

* Sector-informed hypothesis: measure-specific written notice with the
  purpose, scope, retention period and right to object; equally
  weighted non-digital consent routes; and a clear commitment that
  refusal does not affect a resident's retrofit offer or their
  Awaab's Law protections. Blocks of flats need block-level and
  household-level consultation.

`Head of Procurement and Contract Management` was asked: does an
independent inspection tier need to be a separately procured supplier
from the installers, and how is that structured?

* Sector-informed hypothesis: yes, separately procured under an
  independent scope with an explicit conflict-of-interest control that
  the inspector does not carry installer work in the same programme.
  Procurement Act 2023 route selection needs Legal review. The
  budget line is small relative to remediation cost avoided but
  must be visible in the business case.

#### Scenario Verdict

Bounded independent evidence source. Increases the credibility of the
raise-only flag queue and of pattern detection. Autonomy stays at
raise-only. Only proceed where consent and airspace conditions are
cleanly satisfiable.

### What-If 3: Cross-Installer Benchmarking Against Sector Defect Feeds

#### Augmentation

The Quality module compares Proper North Homes' per-measure defect
patterns to sector defect feeds (for example TrustMark defect data,
MCS certificate-holder patterns, published sector research on
common retrofit defects). Where an installer's defect signature
diverges from sector baselines in a specific measure/archetype
combination, the module raises a flag ranked by severity for human
review.

#### Would It Remove the Original Blockers?

It attacks the "small sample" problem inside a single housing
association's data. It does not remove acceptance authority. It
introduces model-risk and governance issues: sector feeds may
themselves be biased by which installers report and which do not,
and using them as a benchmark risks unfairly penalising installers
whose customers are more likely to report.

#### Clarification Questions to the Company Agents

`Head of Procurement and Contract Management` was asked: can
sector-defect-feed comparisons be used in supplier reviews, and if
so under what governance?

* Sector-informed hypothesis: yes, as one input into supplier
  performance reviews, never as a sole basis for exclusion or
  deduction. The methodology must be published to suppliers, they
  must have a right to challenge, and the review record must show
  where the internal Proper North Homes data was decisive versus where
  the sector comparison was decisive.

`Chief Data and Digital Officer` was asked: what data-governance
obligations attach to importing sector defect feeds?

* Sector-informed hypothesis: written data-sharing agreements with the
  source, a documented lawful basis, retention limits, and a
  documented process for handling corrections or withdrawn defect
  reports. Sector feeds are third-party data; treating them as a
  source of truth without governance would create both fairness and
  data-protection exposure.

`Executive Director of Assets` was asked: is there a risk that
benchmarking to a sector baseline drives the programme towards
"average" quality rather than better?

* Sector-informed hypothesis: yes if the benchmark is used to signal
  "acceptable when not worse than sector". The correct use is to
  identify divergence for investigation, not to define an acceptable
  ceiling. Proper North Homes' own quality target sits above the
  sector baseline by design.

#### Scenario Verdict

Bounded benchmarking as an additional signal, governed by published
methodology and supplier right-of-challenge. Autonomy stays at
raise-only. Do not use as an acceptance floor.

### Aggregate Verdict for Quality Verification

The three scenarios strengthen inputs (per-measure packs), add an
independent evidence source (drone/robotic inspection) and add
external context (sector benchmarking). None makes Quality
Verification an end-to-end agent. Together they harden the raise-only
flag queue and the sampling model, and they strengthen the case for
IDEA-001.

### Stop Criteria Across All Quality Verification Scenarios

* Stop if any safety-critical defect caught by humans is missed
* Stop if an evidence pack with no flags is treated as acceptance
* Stop if AI raises a payment hold, a defect notice or a claim rejection
  without a human decision
* Stop if the sensor validity register is not maintained and used to
  qualify every sensor-based flag
* Stop if independent inspection imagery is used to justify acceptance
  or rejection without a competent inspector's decision and chain of
  custody
* Stop if drone or robotic inspection proceeds without measure-specific
  written notice and an accessible objection route
* Stop if sector defect feeds are used as a sole basis for supplier
  exclusion or deduction
* Stop if the sector baseline is treated as an acceptance floor

## Programme Supervisor and Damp-and-Mould Loop

### Programme Supervisor

#### What-If 1: Events Keyed to Lifecycle State Machine

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

Scenario verdict: workflow engine, unchanged in kind, stronger in
inputs. Autonomy stays with named owners at every gate.

#### What-If 2: Always-On AI Exception Dashboard and Board Narrative Generator

An always-on AI module reads the workflow-engine events, watches for
exceptions (stalled clocks, missed handoffs, unresolved holds,
diverging supplier performance, forecast breach of statutory
deadlines) and generates board-narrative and executive-narrative
drafts from the controlled records on a defined cadence. Sensitive
categories (safeguarding, HRB, complaints) are excluded from the
generator and routed to named humans.

Would it remove the original blockers? It attacks the "board sees the
programme via retrospective PDFs" blocker without changing decision
authority. It does not remove any statutory duty, and it introduces two
new risks: the board comes to trust the AI narrative as authoritative
even though the source is still the workflow engine, and a
hallucinated narrative could mislead governance if unnoticed.

`Company Secretary and Head of Governance` was asked: what controls
must sit around AI-drafted board narratives so the board does not
mistake the narrative for the record?

* Sector-informed hypothesis: every narrative carries the workflow-
  engine snapshot identifier and a link back to the underlying
  records; the executive owner signs the narrative before it goes to
  the board pack; and any narrative sentence that cannot be traced to
  a specific record is removed before sign-off. The board minutes
  reference records, not the narrative.

`Head of Internal Audit and Assurance` was asked: how do we evidence
that exception detection did not miss a stalled clock or a breached
gate?

* Sector-informed hypothesis: a periodic independent reconciliation
  between the AI exception log and an audit sample from the raw
  workflow-engine events, with any missed exception documented and
  the detection rule adjusted. Detection cannot be judged solely by
  the AI's own record.

`Chief Data and Digital Officer` was asked: what stops narrative drift
between successive board packs?

* Sector-informed hypothesis: prompts, models and record-selection
  rules are versioned, changes are logged, and any material prompt or
  model change requires an executive sign-off before publication.
  Otherwise the "same" narrative silently changes tone or emphasis.

Scenario verdict: bounded AI summarisation and exception detection.
Genuinely useful, autonomy stays at draft. Only proceed with
independent audit reconciliation.

#### Aggregate Verdict for Programme Supervisor

The supervisor is a workflow engine plus a bounded AI summarisation
module. Neither what-if creates an autonomous supervisor.

#### Stop Criteria Across All Supervisor Scenarios

* Stop if any AI summary misstates a hold, a clock, an owner or a
  consent status
* Stop if a board narrative sentence cannot be traced back to a
  specific workflow-engine record
* Stop if independent audit reconciliation of the exception log is
  not maintained on a defined cadence
* Stop if prompt, model or selection-rule changes are not versioned
  and executive-signed

### Damp-and-Mould Loop

#### What-If 1: Resident and Contractor Hazard App

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

Scenario verdict: workflow engine plus hazard app. Autonomy stays at
awareness capture and routing; investigation and decision remain with
named humans.

#### What-If 2: Consented Ambient Sensors (T/RH/VOC) as Raise-Only Early Warning

A subset of properties, with explicit, measure-specific written
resident consent, is fitted with ambient sensors (temperature,
relative humidity, volatile organic compounds) that push
anonymised trend readings to a raise-only module. When trends
cross validated thresholds tuned per archetype and heating season,
the module raises a hazard-suspected flag into the same intake
route that residents and contractors use. Awaab's Law Phase 1
guidance is explicit that a sensor risk notification does not by
itself make the landlord aware
([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
section 3.5), so the module never sets an awareness timestamp on
its own.

Would it remove the original blockers? It attacks the "silent
hazard" blocker for consented households, and it feeds
defect-pattern detection with much more consistent longitudinal
data. It does not, and cannot, replace the awareness rules. It
introduces new risks: fairness (only consented households benefit,
which may correlate with vulnerability); model risk (thresholds
tuned wrong will either over-flag or miss); and the reverse
Awaab's Law trap where a sensor reading was normal and a resident
report is de-prioritised because "the sensors are quiet".

`Head of Building Safety and Compliance` was asked: what governance
attaches to threshold-based hazard flags in an Awaab's Law-in-scope
setting?

* Sector-informed hypothesis: thresholds are published, versioned
  and reviewed by a competent inspector, with false-positive and
  false-negative rates reported. A sensor flag is never sufficient
  to close a resident-reported case; a resident report is always
  investigated as such, regardless of sensor readings, per section
  3.5 of the Phase 1 guidance
  ([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md)).

`Head of Resident Engagement and Insight` was asked: what does a
lawful, non-coercive consent flow look like for ambient sensors?

* Sector-informed hypothesis: measure-specific written consent with
  a plain-English purpose, retention period, right to withdraw
  without effect on the tenancy or the retrofit offer, and a
  documented data-minimisation stance (aggregated trends, not
  continuous fine-grained data). Consent must be re-affirmable on
  any change of purpose. Bundling with retrofit consent is not
  acceptable.

`Chief Data and Digital Officer` was asked: what lawful basis and
DPIA controls are required?

* Sector-informed hypothesis: consent as lawful basis under UK GDPR
  ([local snapshot](../../regulatory/data-protection/uk-gdpr-current-text.md)),
  with a full DPIA covering necessity, proportionality, security,
  and safeguards against inference of special category data
  (household composition, illness, occupancy patterns). The DPIA
  must be reviewed before any threshold change goes live.

Scenario verdict: bounded raise-only early warning under consent
and independent threshold governance. Autonomy stays at flag-only,
and the awareness rules are unchanged.

#### What-If 3: Call Recording Transcription with Hazard-Signal Extraction

Repairs-line calls and housing-officer calls, where the caller has
been notified and had a right to object, are transcribed. An AI
module scans transcripts for hazard signals (damp, mould, cold,
condensation, breathing difficulty, roof leak, mention of a child
or vulnerable person) and raises a suspected-hazard flag into the
same intake route.

Would it remove the original blockers? It attacks the well-known
gap where a hazard is mentioned in a call about something else and
never becomes a case. It introduces significant new duties: call
recording, special category data, transcription accuracy across
accents and languages, and the same reverse Awaab's Law trap as
sensors if human triage stops trusting the transcript flag.

`Head of Resident Engagement and Insight` was asked: what
notification and consent model attaches to call recording for
hazard extraction?

* Sector-informed hypothesis: a plain-English notification at the
  start of every call, an accessible objection route that does not
  degrade service, and separate lawful bases for recording (contract
  or legitimate interest) and for AI hazard extraction (a documented
  legitimate-interest assessment with an explicit balancing test
  covering vulnerable residents). Bundling into a click-through
  consent is not acceptable.

`Chief Data and Digital Officer` was asked: what are the special
category data implications, given calls may reveal health, ethnicity
or religious observance?

* Sector-informed hypothesis: UK GDPR Article 9 applies as soon as
  the transcript captures such content, whether or not the module
  uses it. An Article 9 condition is required (typically substantial
  public interest with a formal appropriate-policy document); DPIA
  is mandatory; and retention must be short and purpose-limited.
  Transcripts should be discarded after signal extraction, keeping
  only the extracted case link
  ([local snapshot](../../regulatory/data-protection/uk-gdpr-current-text.md)).

`Head of Building Safety and Compliance` was asked: does a
transcript-derived flag itself start an Awaab's Law clock?

* Sector-informed hypothesis: the awareness timestamp is set at the
  moment the resident said it on the call, not at the moment the
  AI extracted it. The extraction speeds up detection but does not
  change the awareness rule. Statutory clocks must therefore be
  back-dated to the call time.

Scenario verdict: bounded transcription-and-extract as raise-only,
under a documented Article 9 condition and a short retention
policy. Only proceed after Data Protection and Legal review.

#### Aggregate Verdict for Damp-and-Mould Loop

Do not build as an agent. The three scenarios enrich the intake
route with resident-generated evidence, consented ambient sensors,
and call-derived signals. Together they materially increase the
chance of earlier awareness, while explicitly not moving awareness
authority or investigation authority. All three depend on the same
one-case-per-property, deduplicated hazard-case record.

#### Stop Criteria Across All Damp-and-Mould Scenarios

* Stop if any AI output delays, suppresses or closes a clock
* Stop if awareness timestamps are set from human review rather than
  from arrival
* Stop if the retrofit app opens a duplicate hazard case
* Stop if ambient-sensor thresholds are unpublished, unversioned or
  not reviewed by a competent inspector
* Stop if a sensor "quiet" reading is used to de-prioritise a
  resident report
* Stop if ambient-sensor deployment lacks measure-specific written
  consent, a full DPIA and a costless withdrawal route
* Stop if call recording proceeds without a plain-English
  notification and accessible objection route
* Stop if the transcript is retained beyond signal extraction, or if
  Article 9 conditions and DPIA are not in place
* Stop if a transcript-derived flag sets the awareness timestamp
  later than the moment the resident said it on the call

### Revised Verdict for Both

Do not build as agent. The augmentations strengthen the case for a
workflow engine and a statutory clock in the repairs service, both of
which are in the shared foundation.

## Cross-Cutting Findings

Three threads run through every revised verdict.

* The augmentations do not create new agents. They enrich the same
  shared foundation the original challenge identified: property
  master, hazard case record, measure-specific decision record,
  committed-capacity register, per-measure evidence schedule and
  four-state grant ledger. Where richer inputs help most, they help
  the foundation, not the agent layer.
* The augmentations expand governance duties before they expand
  autonomy. Photos, structured invoices, capacity feeds, sensor
  readings, call transcripts, drone imagery, sector defect feeds and
  digital twin outputs all bring in Article 9 data, Awaab's Law
  awareness, Construction Act payment questions, Procurement Act 2023
  modification questions and, in several cases, UK GDPR Article 22
  concerns about solely automated significant decisions
  ([local snapshot](../../regulatory/data-protection/uk-gdpr-current-text.md)).
  Every added input needs Data Protection, Legal, Building Safety and
  Procurement review before the module runs live.
* Several scenarios (external data fusion, digital twin, ambient
  sensors, call transcription, sector benchmarking) risk fairness or
  coverage skew if benefits accrue only to consented or digitally
  active households. The default response is to raise service for
  the non-participating cohort, not to throttle the participating
  one.

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
| 6 | Is there an approved lawful basis, DPIA and consent flow for consented ambient sensors and for call-recording transcription used for hazard extraction? | Both scenarios depend on it and both engage UK GDPR Article 9 |
| 7 | Are there existing or planned data-sharing agreements with TrustMark, MCS and any funder portal that would support automated reconciliation? | Determines the feasibility of the Grant and Funding integration scenario |
| 8 | Does the association have or intend to procure independent inspection capacity (drone, thermal, robotic) separately from the installer base? | Determines the feasibility of the Quality Verification independent-evidence scenario |
| 9 | What is the association's stance on external data fusion (smart-meter DCC, EPC, fuel-poverty proxies) as inputs to prioritisation, and its associated Article 22 human-review model? | Determines the feasibility of the Stock Prioritisation external-data scenario |

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
* Several scenarios (per-archetype digital twin, sector defect
  benchmarking, ambient sensors, call transcription) depend on
  external data sources or third-party feeds. The study assumes those
  sources can be governed and audited; that assumption itself needs
  testing before commitment.
* Each agent's what-ifs were reasoned in isolation from the others.
  Real deployments would combine them (for example a resident app
  used for consent, hazard reporting and evidence upload at the same
  time), which raises additional Data Protection, safety and fairness
  questions that this study does not resolve.

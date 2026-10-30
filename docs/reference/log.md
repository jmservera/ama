---
title: Knowledge Base Log
description: Append-only record of ingests, restructures, filed answers and lint passes for the project knowledge base
ms.date: 2026-10-29
ms.topic: reference
---

## Conventions

Append new entries at the end. Do not edit or delete earlier entries; record a
correction as a new entry. Start each entry with a heading in this form so the
log can be searched with simple tools:

```text
## [YYYY-MM-DD] type | Short title
```

Use one of these types: `ingest`, `query`, `restructure`, `memory`, `lint`.
List the files touched and any contradiction or open question raised.

Entries dated before 2026-09-25 are reconstructed from Git history and file
metadata when the knowledge base was created.

## [2026-09-11] ingest | Sector baseline and company profile research

* Added company profile research and UK social housing baseline research with
  its source register, then located in `support/`.

## [2026-09-19] ingest | Regulatory source snapshots

* Downloaded and converted 16 official legislation, regulator, policy,
  guidance, standards and funding documents, with the regulatory register.
* Retrieval date for the snapshots: 2026-09-19. Register updated 2026-09-20.

## [2026-09-25] ingest | Housing association primer

* Source: newhomesforsale.co.uk, Understanding Housing Associations in the UK,
  last updated June 2026, retrieved 2026-09-25.
* Created `research/sector/housing-association-primer.md`.
* Contradiction flagged: the source frames 300,000 affordable homes over five
  years, while GOV.UK describes the Social and Affordable Homes Programme as a
  ten-year programme from April 2026 to March 2036.
* Inconsistency flagged: the source ranks L&Q above Peabody while reporting a
  higher home count for Peabody.

## [2026-09-25] restructure | Create the project knowledge base

* Turned `docs/reference/` into the knowledge base with an index, this log
  and a project memory file.
* Moved the regulatory snapshots and register into `regulatory/` topic
  folders.
* Moved research syntheses from `support/` into `research/sector/` and
  `research/company/`.
* Moved `support/loop_example.md` to `method/loop-goal-designer-prompt.md`.
* Moved `support/notes.md` to `memory.md` and restructured it without
  changing its meaning.
* Kept `support/cohort.md` and `support/resources.md` in `support/` as private
  owner material.
* Updated links in the addendum, BRD, discovery brief, idea documents, agents,
  root README and repository instructions. Fixed pre-existing broken links in
  the addendum, idea documents and discovery brief.

## [2026-09-25] ingest | Microsoft Industry Hub

* Source: Microsoft Industry Hub home page and Nonprofit Industry Page on
  Seismic, supplied by the project owner, with related SharePoint items.
* Retrieved search snippets with WorkIQ on 2026-09-25. Documents were not
  read end to end.
* Created `resources/microsoft-industry-hub.md` with entry points, nonprofit
  hero use cases, patterns mapped to each Proper Warm agent, customer
  evidence and lessons. Added a `resources/` layer to the index.
* Excluded internal-only deal data, such as opportunity identifiers,
  contract values and battlecard content, and staff names.
* Open question: no UK housing association customer story was found. Search
  again or ask the nonprofit or public sector industry team.
* The owner removed `support/resources.md`, whose Industry Hub link now lives
  in the resources page, and moved its meeting note into `memory.md`. Updated
  the memory standing preference to match.

## [2026-09-25] query | File back the sector archetype research

* Filed the answers to the primer's four open questions and the sector
  archetype research into the knowledge base.
* Files touched: `research/sector/housing-association-primer.md` (sector
  scale, archetypes, tenure, lease responsibility for retrofit, residents and
  vulnerability data, board capital patterns, sources, open questions and
  limitations), `research/company/company-profile-research.md` (Modelled
  Customer Profile, comparators, gaps, sources, limitations and the SRS MEES
  line), `../case_study_48_addendum.md` (cross-reference to the modelled
  profile), the index (`README.md`) and this log.
* Web sources were retrieved on 2026-09-25. Modelled Proper North Homes
  values are estimates from sector medians and national rates, not company
  facts.
* Correction: a housing association fuel poverty figure of 10.0% is the
  superseded LIHC measure. The primer uses 11.6% (LILEE, 2024, DESNZ via UK
  Housing Review 2026 Table 39a).
* Contradiction flagged: the primer cites 91% sector EBITDA-MRI interest
  cover from the RSH Sector Risk Profile 2025, while the baseline research
  cites 87% as the weighted 2025 Global Accounts average. The bases probably
  differ. The baseline research was left unchanged and the difference is not
  yet reconciled.
* Correction: the company profile Regulatory Baseline no longer describes EPC
  C as a policy objective or proposal. It now states the 2026 SRS MEES final
  policy position from the local snapshot, which is not by itself a commenced
  duty.
* Open question: the preserved right to buy provisions (Housing Act 1985,
  sections 171A to 171H) for transferred stock have not been checked.
* Open question: the Warm Homes: Social Housing Fund Wave 3 30% non-social
  rule was verified only in the GMCA copy. Check the national DESNZ guidance.
* Open question: actual retrofit responsibility in shared ownership and
  leasehold homes needs a lease-by-lease sample review under legal approval.

## [2026-09-26] query | Challenge the requested agents with the role agents

* Sent each requested agent's "owns end-to-end" line to the eight `company-*`
  role agents in parallel. Each role was asked for the real problem, the
  challenge, non-agent alternatives, where an agent fits, what to build
  behind it, a value test with stop criteria, and the unknowns.
* Files touched: `research/company/agent-request-challenge.md` (new),
  `../case_study_48_addendum.md` (new subsection, Challenge of the Requested
  Agents, and `ms.date`), the index (`README.md`) and this log.
* Finding: no role supported building any of the five as an end-to-end
  agent. Each request bundles deterministic controls, accountable human
  decisions and a smaller set of tasks suited to bounded AI. All of them
  depend on the same shared records.
* BRD IDs and regulatory provisions cited in the page were spot-checked
  against local files on 2026-09-26. They were not checked against the
  official sources online.
* Open contradictions: Quality Verification AI at L4 or at recommend level;
  L3 booking for residents who have opted into digital contact. Legal
  questions on procurement modification, payment notices and contractor
  awareness remain open.

## [2026-09-26] query | Review the BRD against the new research and challenge

* Reviewed the Agentic Retrofit Programme BRD against the Modelled Customer
  Profile and Housing Association Primer (2026-09-25), the Agent Request
  Challenge (2026-09-26) and IDEA-001.
* Sent one focused gap question each to five `company-*` role agents in
  parallel: Building Safety, Resident Engagement, Procurement, Finance and
  the Retrofit Programme Manager. Their proposed wording, labelled as
  sector-informed, informs the new requirements.
* Files touched: `../brds/agentic-retrofit-programme-brd.md` (BR-059 to
  BR-068, OD-26 to OD-33, disposition table with a damp-and-mould loop row,
  bounded AI capability value tests, stakeholders, scope, data domains,
  risks, sponsor questions, traceability, sources and `ms.date`),
  `../case_study_48_addendum.md` (cross-reference to the new BRD IDs), the
  index (`README.md`) and this log.
* Awaab's Law Phase 1 guidance sections 3 and 7.5 and the WH:SHF technical
  annex Pages 3 and 5 were checked against the local snapshots only. Section
  7.5 advises reviewing contractor agreements; the same-visit reporting duty
  in BR-062 is a proposal, not a guidance requirement.
* Still open: the QV autonomy divergence (OD-31, with a proposed three-arm
  shadow test) and L3 digital booking (OD-32). The Legal questions are
  consolidated in OD-27, OD-29 and OD-30. The 30% non-social rule is still
  verified only in the GMCA copy (OD-26).
* No BRD quality reviewer subagent was available, so no
  `BRD_QUALITY_REPORT_V1` was produced. The BRD remains a draft for business
  validation.

## [2026-09-26] query | Apply confirmed not-for-profit status to role agents

* Recorded the project owner's confirmation that Proper North Homes is a
  not-for-profit organisation. Its exact legal form, registration, group
  structure and charitable status remain unknown.
* Updated `research/company/company-profile-research.md`,
  `../case_study_48_addendum.md`, all eight `company-*` role agents, the index
  (`README.md`) and this log.
* Applied the fact by role: mission-led asset stewardship, retained-surplus
  affordability, whole-life procurement value, resident accountability,
  frontline service outcomes, unchanged safety duties, quality-adjusted
  retrofit outcomes, and mission-aware performance measurement.
* Guardrail: not-for-profit status does not imply unlimited funding, reduced
  legal duties, charitable status, resident endorsement or freedom from
  financial discipline.

## [2026-09-26] update | Relabel the BRD to the canonical requirement taxonomy

* A BRD quality review (BRD Quality Reviewer, Define phase) failed the draft
  because its legacy BR-### and OBJ-## identifiers gave 0.0% canonical
  FR-to-AC and FR-to-BG coverage. The owner chose to relabel with legacy
  aliases and to use RULE-### for business rules, so no ID means two things.
* Updated `../brds/agentic-retrofit-programme-brd.md`: frontmatter overlay
  (`brd_id` BRD-2026-AMA48-001, version 0.2.0, prefixes), 12 BG, 41 FR,
  73 AC, 9 NFR, 6 CON and 23 RULE identifiers, a Requirement Identifier
  Scheme, Imposed Constraints, NFR categories by ISO/IEC 25010, regenerated
  traceability and a Legacy Identifier Map. BR-046, BR-048, BR-062 and BR-066
  were split; no requirement changed meaning.
* Goal alignment is now generated from each row's business goals. Where the
  earlier OBJ-to-BR table disagreed with the rows, the rows govern.
* Updated `../case_study_48_addendum.md` (legacy alias note), the index
  (`README.md`) and this log. BR-### and OBJ-## citations in earlier entries
  and other documents remain valid through the map.
* Constraint citations were checked against local snapshots only. CON-004
  cites legislation outside the local corpus through the housing association
  primer; Legal must validate it before live use.
* Rerun result: FAIL, Define exit blocked. FR-to-AC and FR-to-BG coverage are
  100.0%. Remaining risks are seven business goals lacking a numeric target,
  a timeframe or both, and NFR-009 thresholds, which need company data or
  board decisions (OD-01, OD-08, OD-09, OD-11, OD-12, OD-13, OD-15, OD-18,
  OD-25). Targets were not invented.

## [2026-09-26] query | Challenge the pilot measurement and benefits dashboard proposal

* The owner proposed a benefits dashboard, comparison with historical
  records or a short prospective history, and comparison of the pilot with
  non-pilot retrofit work. The eight `company-*` role agents challenged it in
  parallel.
* Added `research/company/pilot-measurement-challenge.md`: challenge table,
  the operating-model versus agent decision, a two-layer comparison design,
  freeze list, analysis rules, effort measurement, operational dashboard
  versus benefits scorecard, consolidated scorecard, guardrails with stop
  triggers, vanity metrics and plausible history sources.
* Flagged contradictions: the BRD Current-State Summary treats the
  twelve-month reconstruction as the counterfactual, while the panel treats
  it as context only; the BG-011 targets may be below the pilot's minimum
  detectable effect. Both go to OD-18. The BRD and addendum were not changed.
* BRD identifiers were spot-checked against the local BRD, and the Awaab's
  Law timer claim against the local Phase 1 guidance snapshot. Nothing was
  checked against official sources online. All role answers are hypotheses,
  not company facts.
* Updated the index (`README.md`) and this log.

## [2026-09-26] update | Integrate the pilot measurement design into the BRD and addendum

* At the owner's request, the BRD Builder integrated
  `research/company/pilot-measurement-challenge.md` into
  `../brds/agentic-retrofit-programme-brd.md`, now version 0.3.0. RULE-019
  requires a frozen two-layer protocol. AC-062 covers the freeze and Finance
  attribution, and AC-074 to AC-077 cover Layer A, Layer B, statistical
  reporting and effort measurement. New RULE-024 (AC-078) pauses affected
  work on a guardrail breach. Other changes: a BG-011 caveat on the minimum
  detectable effect, FR-025 measurement costs, an operational dashboard
  versus benefits scorecard, a misleading-measures list, OD-34 to OD-38, and
  updated traceability and approval criteria.
* The Current-State Summary now treats the twelve-month reconstruction as
  context. The proposed counterfactual is the instrumented pre-period plus a
  concurrent matched comparison, pending OD-18. This resolves the
  contradiction flagged in the previous entry, but only as a proposal.
* Added a measurement-design note and a challenge row to
  `../case_study_48_addendum.md`.
* BRD Quality Reviewer, Define: the first 0.3.0 pass raised four CAUTION
  findings (compound AC-062, unnumbered prose obligations, untraced
  guardrails, inconsistent timing gate). The BRD Builder corrected all four,
  and the rerun found no new findings. The overall result is still FAIL, with
  Define exit blocked, only because of the accepted company-data gaps
  (req-qual-001 to 008). Run 3 was recorded in
  `.copilot-tracking/brd-sessions/agentic-retrofit-programme.quality-report.yml`.
* Updated the challenge page, the index (`README.md`) and this log.

## [2026-09-26] update | Reframe as agent-led modernisation and place agents only where they add value

* At the owner's request, the programme is now framed as an agent-led
  modernisation of the existing retrofit model. The BRD Builder updated
  `../brds/agentic-retrofit-programme-brd.md` to version 0.4.0 and
  `../case_study_48_addendum.md`. The pilot uses existing teams and
  suppliers. The dedicated delivery cell and ring-fenced capacity were
  removed, and "control plane" became "digital foundation".
* Measurement: Comparison 1 tests a locality with agents against a matched
  locality without them. Comparison 2 gives per-capability task-level
  evidence. Both replace Layer A and B, and AC-074, AC-075 and RULE-019 were
  edited in place. OD-34 is a proposed resolution: the pilot decides which
  agent capabilities scale. Sponsor, Assets and Finance must confirm it. An
  Owner Decision section was added to
  `research/company/pilot-measurement-challenge.md`.
* Agent placement: the capability tables in the BRD and the addendum now show
  a deterministic core beside the place where an agent helps. Decisions that
  need clear, transparent and repeatable rules stay deterministic. Agents turn
  free text into sourced values, propose missing values for owners to
  confirm, reconcile records, draft and raise signals. Ranking weights and
  executive reporting are no longer agent capabilities, and programme
  supervision and reporting have no agent in the initial pilot. A raise-only
  hazard-signal row was added. The addendum links each capability to a
  proposed business value measure.
* Removed wording saying the documents do not judge current teams.
* BRD Quality Reviewer, Define: Runs 4 and 5 found no new findings. The result
  is still FAIL, with Define exit blocked, only because of the accepted
  company-data gaps (req-qual-001 to 008).
* Updated the index (`README.md`) and this log.

## [2026-09-26] review | Check the BRD against explainability and transparency

* Reviewed the Agentic Retrofit Programme BRD against NIST AI RMF MS-2.8,
  MS-2.9 and GV-1.6, UK GDPR Articles 12 to 15 and 22A to 22C, and Safety and
  Quality Standard 2.3.2 and 2.3.3. Proper North Homes is a regulated
  not-for-profit, so explanations are designed for residents, the Regulator,
  funders and the Board.
* Contradiction fixed: CON-003 cited UK GDPR Article 22. The local
  consolidated text (converted 2026-09-19) omits Article 22 and uses Articles
  22A to 22D. CON-003, RULE-022 and AC-072 now cite Articles 12 to 15 and 22A
  to 22C and map human review to the four Article 22C(2) safeguards.
* BRD version 0.5.0 adds the AC-079 transparency gate, audience-specific
  explanation records with a resident comprehension test (FR-034, AC-080,
  AC-081), a published prioritisation policy with per-home reason codes
  (FR-042), an AI capability register and Board assurance report (FR-043),
  per-output provenance (FR-044), source-based confidence categories,
  unsupported-claim, explanation-fidelity and automation-bias measures
  (AC-085), AI supplier documentation terms and OD-39.
* Evidence gap (OD-39): the Transparency, Influence and Accountability
  Standard, the Housing Ombudsman Complaint Handling Code, the Governance and
  Financial Viability Standard and ICO guidance on explaining AI decisions are
  not held locally.
* BRD Quality Reviewer, Define: Run 6 found no new findings. The result is
  still FAIL, with Define exit blocked, only because of the accepted
  company-data gaps (req-qual-001 to 008).
* Updated the index (`README.md`) and this log.

## [2026-09-27] update | Refresh and publish the AMA mentor progress review deck

* Reviewed the mentor deck against the four later 2026-09-26 entries: pilot
  measurement challenge, BRD 0.3.0 integration, the agent-led modernisation
  reframe (BRD 0.4.0) and the transparency review (BRD 0.5.0). Working files
  are in `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/`.
* Slide 8 now shows the digital foundation, bounded agents and accountable
  people, with the one-locality ask using existing teams and suppliers. A new
  slide 9 covers Comparison 1 and 2, the dashboard versus benefits scorecard,
  RULE-024, the CON-003 citation fix, AC-079, FR-042 to FR-044, OD-39 and the
  OD-34 proposal. BRD counts were updated to 12 BG, 44 FR, 85 AC, 9 NFR,
  6 CON and 24 RULE, and to six quality runs.
* The AMA Presentation Communications Strategist reviewed the changes. It found
  one error: the local UK GDPR text omits Article 22 and holds Articles 22A to
  22D, while CON-003 cites 22A to 22C. The error and its other recommendations
  were applied. At the owner's request, the knowledge-organisation slide moved
  to an appendix and the speaker notes were cut to about 2,000 words.
* Found why `../presentations/` was empty. The PowerPoint pipeline writes only
  to its tracking folder. The owner had deliberately removed
  `proper-warm-cxo-initial-proposal.pptx`, and that deletion was committed
  with the first mentor deck (df1de38), so the index links were broken.
  Published `../presentations/ama-mentor-progress-review.pptx`, replaced the
  broken index links with it, and added a delivery-copy rule to
  `.github/copilot-instructions.md`.
* Updated the index (`README.md`) and this log.

## [2026-09-27] query | What-if session on the Agent Request Challenge

* Owner asked whether richer inputs (phone-captured photos with EXIF GPS,
  structured digital invoices, app-based consent, adjustment and outcome
  capture, contractor capacity feeds, sensor validity metadata) would
  change any of the five 2026-09-26 verdicts. Assessment was given as a
  worked example: a provenance-checked evidence bundle enabling an
  evidence assessment for the Retrofit Assessor.
* Files touched: `research/company/agent-what-if-study.md` (new),
  `../case_study_48_addendum.md` (cross-reference from the Challenge of
  the Requested Agents subsection and `ms.date`), the index (`README.md`
  and `ms.date`) and this log.
* Focused clarification questions were put to the relevant `company-*`
  role agents per augmentation: Data Lead and Asset Executive for Stock
  Prioritisation; Retrofit Programme Manager and Building Safety for
  Assessment; Finance and Procurement for Grant and Funding; Resident
  Engagement, Neighbourhood Officer and Procurement for Coordination;
  Building Safety, Procurement and Data Lead for Quality Verification;
  Asset Executive, Building Safety and Neighbourhood Officer for the
  Supervisor and Damp-and-Mould loop. Answers are labelled
  `Sector-informed hypothesis`.
* Finding: no augmentation changes the headline verdict. The strongest
  cases (Assessment and Quality Verification) widen what bounded AI can
  usefully check without moving autonomy above recommend or raise-only.
  The augmentations mostly enrich the shared foundation and expand
  governance duties (Article 9, Awaab's Law awareness, Construction Act
  payment notices, Procurement Act 2023 modification) before they expand
  autonomy.
* Open items and risks: false-provenance rates for EXIF GPS need a
  seeded test set; digital exclusion needs equity checks; Awaab's Law
  awareness timestamp must come from arrival, not human review; a
  cross-module DPIA is needed if one resident app carries consent,
  adjustments, condition photos and hazard photos.
* Regulatory citations in the study were spot-checked against local
  snapshots on 2026-09-27. They were not checked against the official
  sources online.

## [2026-09-27] query | What-if study extended to multiple scenarios per agent

* Owner feedback on the initial study noted that the photo/GPS worked
  example was one scenario, and asked for multiple distinct what-if
  scenarios per requested agent.
* Files touched: `research/company/agent-what-if-study.md`.
* Extension: each of the five requested agents plus the supervisor and
  damp-and-mould loop was re-examined with two or three distinct
  scenarios (for example Stock Prioritisation now covers a resident app,
  external data fusion and a per-archetype digital twin; Assessment
  covers app-fed evidence, on-site structured scanning and pre-visit AI
  triage; Grant and Funding covers structured invoices, funder-portal
  integrations and continuous eligibility monitoring; Coordination
  covers capacity feeds, a multi-supplier capacity mesh and a
  multi-channel resident concierge; Quality Verification covers
  per-measure packs, independent drone or robotic inspection and
  sector-defect-feed benchmarking; the Supervisor gains an exception
  dashboard and board-narrative generator; the damp loop gains ambient
  sensors and call-recording transcription).
* For every new scenario, the same role agents were asked clarification
  questions and answered as `Sector-informed hypothesis`. The summary
  table, per-agent aggregate verdicts and per-agent stop criteria were
  extended accordingly.
* Finding: none of the additional scenarios changes the headline
  verdict; several sharpen it by exposing new Article 9, Article 22,
  Procurement Act 2023 and fairness questions.

## [2026-09-27] review | What-if study validated after the branch merge

* Trigger: owner `/rpi-review` request to check the Agent What-If Study
  was still valid after merging `Review-progress-challenge` (BRD v0.3.0 to
  v0.5.0, the agent-led modernisation reframe, the pilot measurement
  design and the transparency review) and to fix anything outdated.
* Review record:
  `.copilot-tracking/reviews/logs/2026-09-27/agent-what-if-study-post-merge-review.md`
  (outcome: defects found; six findings, RV-001 to RV-006).
* Files touched: `research/company/agent-what-if-study.md`,
  `../case_study_48_addendum.md` (what-if paragraph), `README.md`
  (catalog row).
* Finding: the headline verdict still holds. The reframe adds bounded
  agent capabilities, not end-to-end agents.
* Correction: the study's "Article 22" citations did not resolve, because
  the local consolidated UK GDPR text omits Article 22. They now cite
  Articles 22A to 22C, with the Article 22B special-category restriction
  where it applies. This is the same correction made to BRD CON-003 on
  2026-09-26.
* Contradiction flagged and resolved: the extension entry above says the
  same role agents answered every new scenario, but eleven answers were
  attributed to four perspectives with no role agent (Chief Data and
  Digital Officer, Executive Director of Finance and Governance, Company
  Secretary and Head of Governance, Head of Internal Audit and Assurance).
  At the owner's direction, nine were re-run with the Data and
  Performance Lead and the Head of Finance, Capital and Grants and
  replaced. Material differences changed the capacity-mesh stop criterion
  (quality and complaint thresholds become hard limits), the sensor
  description (pseudonymised, not anonymised readings) and the
  transcription answer (keep the call timestamp and a minimal excerpt as
  awareness evidence). The governance and internal audit answers are
  relabelled as author hypotheses with no role-agent anchor. The earlier
  entry is left unchanged as history.
* Added a Reconciliation With the Current Proposal section. It maps
  "shared foundation" to the digital foundation and reads "Do not build
  as agent" as "no end-to-end agent", which is consistent with the Agentic
  Architecture Brief. It positions the grid as a candidate order for
  Phase 0 and Comparison 2 testing under the proposed OD-34 resolution,
  not a scaling decision. The Value Test now cross-references FR-042,
  FR-043, FR-044, RULE-019, RULE-024, OD-36 and OD-39. Legacy BR-011,
  BR-013, BR-016 and BR-020 are replaced by FR-011, FR-013, NFR-001 and
  RULE-006.
* Residual: the other role answers were given against the pre-reframe
  addendum and have not been re-run.

## [2026-09-27] presentation | Mentor deck iteration 4 and the ama-mentor-deck skill

* Trigger: the owner asked for another review of the mentor deck against
  the log and memory, and for the deck process to be captured so it does
  not need re-explaining.
* Files touched: `../presentations/ama-mentor-progress-review.pptx`
  (replaced), `README.md` (deck row), `../../.github/skills/ama-mentor-deck/`
  (new skill with `deck_yaml.py` and `Export-SlideImages.ps1`),
  `../../.github/copilot-instructions.md` (pointer to the skill).
* Deck: a new slide 10 covers the what-if stress test. It shows a grid of
  all 20 scenarios as a Comparison 2 test order under proposed OD-34, and
  the post-merge corrections. Slides 1, 3, 6 and 15 now use the verified
  counts: 39 non-merge commits from 10 to 27 Sep and 13 BRD commits. The
  slide 12 notes add the lesson to search every derived document when
  fixing an error. The deck has 14 main slides plus an appendix.
* Review: the AMA Presentation Communications Strategist made eleven findings,
  and all were accepted after checking. Main notes went from 2,158 to 1,921
  words. The review found a contradiction in the iteration-3 deck: the
  slide 3 card said twelve BRD revisions while the notes and slide 6 said
  thirteen. It is now corrected to thirteen, which `git log` confirms.
* Validation: both validators report 0 issues across 15 slides. The
  published copy matches the build by SHA-256.
* Working records: `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/changes/build-validate-iteration-4.md`
  and `research/subagents/storytelling-review-iteration-4.md`.

## [2026-09-27] research | Re-run all what-if role answers against the current proposal

* Trigger: the owner asked to re-run the remaining what-if role answers
  after the agent-led modernisation reframe, closing the residual in the
  review entry above.
* Method: the 39 answers not re-run earlier went to the eight
  `company-*` role agents in parallel. Each agent read the current
  addendum and BRD v0.5.0 and classified its answer as unchanged (1),
  refined (32) or materially changed (6). Every cited BRD identifier
  resolves in the BRD. The answers remain sector-informed hypotheses.
* Files touched: `research/company/agent-what-if-study.md`,
  `../case_study_48_addendum.md` (what-if paragraph), `README.md`
  (catalog row).
* Material changes, each checked against the BRD before applying:
  * Photo scans raise flags for human triage and do not open cases
    (FR-003, FR-004). Assessment awareness wording now defers to OD-29.
  * Pre-Visit AI Triage keeps risk-path proposals in blind shadow mode
    until a RULE-020 release decision (AC-014, FR-010).
  * Suppliers offer capacity through any channel, and a contract manager
    accepts it (FR-022, RULE-007). A new stop criterion bars making an
    app or API a condition of work.
  * A named person approves every AI-drafted resident message before
    sending (AC-079), and always-human categories go to staffed queues.
  * Programme supervision has no AI summarisation in the initial pilot;
    Board narratives stay written by executives.
  * A transcript flag never back-dates a clock. Earlier-awareness hits go
    to Legal and Safety (FR-004 AC-007), and the stop criterion changed.
* Other corrections:
  * The Assessment aggregate verdict cited a "15% to 25%" addendum
    target. The addendum says at least 20%.
  * The sensor-awareness citation said Phase 1 guidance section 3.5
    (information about the tenant). The rule is in section 3.
  * The sensor stop criteria now require a separate sensor agreement, a
    DPO-approved basis and Building Safety threshold approval (OD-05).
  * The earlier asset answer's claim that the company targets quality
    above the sector baseline was unevidenced and is withdrawn.
  * A missing blank line before the presentation entry above was fixed.
* Residual: the two author hypotheses (board-narrative controls and
  exception-detection audit) still have no role-agent anchor.

## [2026-09-27] presentation | Mentor deck iteration 5 after the role-answer re-run

* Trigger: the owner asked to update the mentor deck again after the
  what-if role answers were re-run.
* Files touched: `../presentations/ama-mentor-progress-review.pptx`
  (replaced).
* Deck: the slide 10 findings panel now says all 48 role answers were
  re-run on the reframe, with six tightened controls and every verdict
  held. The notes describe both re-run passes, give two tightened
  controls as examples and qualify Awaab's Law awareness: a hazard photo
  can establish it no later than its arrival. Slides 3 and 15 now say 41
  non-merge commits from 10 to 27 Sep, and slide 15 says three merged PRs.
* Review: the AMA Presentation Communications Strategist made five findings.
  All were accepted, one with changed wording. The review caught the
  draft notes saying all eleven no-agent answers were re-run, which undid
  an iteration 4 fix, and "no verdict changed", which overstated the
  study because scenario verdict text changed. Main notes are 1,967 words.
* Open for the owner: commit 7bdd952, which carries the role-answer
  re-run, has a generic message that does not describe the change.
* Validation: both validators report 0 issues across 15 slides. The
  published copy matches the build by SHA-256.
* Working records: `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/changes/build-validate-iteration-5.md`
  and `research/subagents/storytelling-review-iteration-5.md`.

## [2026-09-30] query | Validate mentor deck iteration 6

* Trigger: the owner supplied the completed iteration 6 storytelling review
  and asked for its three findings to be executed without changing the
  15-slide structure or the 10 to 27 September title period.
* Slides 3 and 15 now show 42 non-merge commits through 27 September. Slide 15
  distinguishes that period from five pull requests merged by 28 September.
* Source footers on slides 3 to 13 now use concise citations, explicit
  left alignment and one- or two-line layouts with safe edge margins. Slides
  3 to 13 were inspected from the final PowerPoint exports.
* Both validators report zero issues across 15 slides. Main notes remain
  1,967 words. The validated working build has SHA-256
  `8F3CD9DDFAF47CB1E5738AFB7BE790E2D8A61CA70C87203D98066677D46A5F5D`.
* Publication is blocked because PowerPoint holds
  `../presentations/ama-mentor-progress-review.pptx` open. The file was not
  replaced or forced. Its SHA-256 remains
  `D950070D0E8C1EC50951E33E5B412B6F12E02C5AF24D1272DFD45CE83F645343`.
* Working records:
  `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/changes/build-validate-iteration-6.md`
  and `research/subagents/storytelling-review-iteration-6.md`.

## [2026-09-30] memory | Add cohort presentation guidance

* Trigger: the owner asked to preserve presentation advice shared by AMA
  cohort 1.
* Added five customer-first storytelling principles to `memory.md`: lead with
  the customer and why, make the business problem and value explicit, tell one
  end-to-end story, show the changed customer outcome and use the demo as the
  proof point.
* Classified the material as peer advice rather than validated evidence and
  updated the knowledge-base index summary for Project Memory.

## [2026-09-30] ingest | Add AMA capstone assessment rubric

* Trigger: the owner supplied the FY27 participant rubric and asked that the
  final presentation, architecture and pitch be checked and challenged against
  it.
* Converted the supplied document to
  `method/ama-capstone-assessment-guide.md` without changing its wording.
* Added the rubric to task routing and the method catalog.
* Added an explicit rubric review gate to `memory.md` and
  `../case_study_48_addendum.md`.

## [2026-09-30] query | Review BRD against capstone rubric

* Reviewed the Agentic Retrofit Programme BRD against all 20 FY27 AMA
  capstone criteria and applied the section and individual-criterion floors.
* Recorded a provisional evidence score of 61/100 if assessed today. Section B
  is below its floor, and A4, B3, B5 and D3 score 1 because working
  implementation, demo delivery and dissemination evidence do not yet exist.
* Added
  `research/company/capstone-brd-rubric-review.md` with criterion evidence,
  gaps and a four-gate remediation plan covering build, operation, executive
  delivery and publication.
* Updated `../brds/agentic-retrofit-programme-brd.md` to version 0.6.0 with a
  Board decision narrative and a clearer separation between the complete
  non-production demonstrator and separately authorised operational
  validation.
* Open questions: the demonstrator architecture, technology choices, threat
  model, model evaluation harness, operating targets, cost per journey, timed
  demo and thought-leadership publication route remain to be completed.

## [2026-09-30] research | Add synthetic retrofit evidence pack

* Trigger: the case required a realistic operating evidence model for a small
  retrofit delivery team and the repo lacked the missing spreadsheet-heavy
  artefacts needed to support a realistic design loop.
* Added the synthetic evidence pack at
  `research/retrofit-synthetic-data/` with a README, property register,
  candidate lifecycle, resident journey, contractor capacity, grant and finance,
  quality evidence, edge-case returns, handover examples, a missing-information
  plan and a structured evidence-gap register.
* Framed the artefacts explicitly as synthetic design material rather than live
  operational fact, aligned to the repo's evidence hierarchy and discovery brief.
* Updated the knowledge-base index to include the synthetic pack and recorded
  the file set as a durable research artifact for the next RPI loop.

## [2026-09-30] restructure | Regenerate synthetic evidence pack as year-one operating history

* Trigger: the owner asked for a larger synthetic dataset with human error,
  representing a professional team about a year into delivery that sees
  bottlenecks but cannot locate them, grounded in the explicit and implicit
  problems of the case study.
* Replaced the ten-home snapshot in `research/retrofit-synthetic-data/` with
  version 2.0.0: 980 candidate homes from July 2025 to the 2026-09-30 extract,
  generated by a seeded discrete-event simulation with capacity-limited
  survey, coordinator review, supplier, QA and evidence queues.
* Added `lifecycle-events.csv`, `resident-contacts.csv`, `appointments.csv`,
  `safety-holds.csv`, `programme-board-snapshots.csv`,
  `delay-code-dictionary.csv`, `data-dictionary.md` and `manifest.json`.
  Regenerated the property register, tracker, resident journey, capacity,
  finance, quality and issues tables. Rewrote the README, handover examples,
  missing-information plan and evidence gap register.
* Record-keeping imperfections include overwritten statuses, a mid-year
  delay-code revision, mixed date formats, merger duplicates, legacy and
  mistyped references, missing and duplicate events, and supplier outcome
  codes as recorded.
* The generator, parameters and answer key are held in the owner's private
  `support/synthetic-data/retrofit-flow/proper-warm-year-one/` area, outside
  the knowledge base, so analysis can stay blind. Seed 1341953496.
* All content is synthetic and is not a Proper North Homes finding. Open
  question: run a blind constraint analysis against the discovery brief
  before consulting the answer key.

## [2026-09-30] restructure | Separate synthetic generator from its answer key

* Correction to the previous entry: the generator and answer key were in one
  flat folder under `support/synthetic-data/retrofit-flow/proper-warm-year-one/`.
* Split it into `generator/`, which holds the code and is committed, and
  `answer-key/`, which holds `answer-key.md` and the `ground-truth-*` files.
  `answer-key/` is git-ignored so the ground truth stays on the owner's machine.
* The generator now defaults to the knowledge-base pack folder and
  `../answer-key`. Regenerating with seed 1341953496 reproduces identical
  files.

## [2026-10-02] query | Design the program-manager document workspace

* Trigger: the owner requested a shared project canvas so program managers can
  navigate and edit repository documentation without using Git or a coding
  editor.
* Added `research/ux/program-manager-document-workspace-journey.md` with a
  stakeholder-informed JTBD analysis, journey map, accessibility requirements,
  design handoff and validation plan.
* Added the project-scoped Program Workbench extension under
  `../../.github/extensions/program-workbench/`. It indexes Markdown,
  presentations and visual artifacts; searches Markdown content; renders and
  edits Markdown; exposes outgoing links and backlinks; and protects the
  original case study, regulatory snapshots and owner-controlled memory.
* Presentations and visual artifacts are discoverable but read-only in version
  one. Rich presentation preview, relationship visualisation and MCP
  connectivity remain version-two opportunities.
* Research limitation: no program-manager interviews, contextual inquiry,
  analytics or usability studies have been completed. Behavioural findings are
  reported or assumed and must be validated before they become requirements.

## [2026-10-03] query | Record BRD implementation options

* Trigger: the owner requested an Azure versus M365 and business-platform
  assessment and then asked to preserve the discussion.
* Integrated the comparison into the case-study addendum's Solution Proposal,
  covering Azure custom development, a Dataverse and Copilot Studio-led
  implementation, and an Azure-led hybrid.
* Recorded the conditional Azure-led preference, relevant BRD controls,
  candidate service boundaries, whole-life cost and equivalent-journey
  evaluation needs, and official product documentation checked on 3 October.
* Separated the owner's Azure preference for AMA from a validated customer
  platform decision. No architecture, procurement, production release or
  expanded agent authority is approved by this assessment.
* Updated the knowledge-base index. The original case study, BRD requirements
  and owner-controlled memory remain unchanged.

## [2026-10-03] create | Draft platform assessment PRD

* Trigger: the owner asked to present full Azure, business-app and mixed
  approaches to the `company-*` role profiles, then draft a PRD.
* Consulted the eight role profiles for bounded perspectives on asset,
  programme delivery, finance, procurement, residents, data, safety and
  frontline workflow. Their views are labelled as sector-informed hypotheses,
  not company facts, resident evidence or approvals.
* Added `docs/project-planning/proper-warm-retrofit-programme-demonstrator.md`
  and its `.copilot-tracking/prd-sessions/` state file from the canonical PRD
  template. The draft keeps platform selection open and scopes an options gate
  plus a synthetic-data, non-production demonstrator.
* No signed `BRD_TO_PRD_HANDOFF_V1` was available. The PRD records the upstream
  BRD's draft status and the need to reconcile its latest quality evidence
  before PRD validation.
* Updated this index. The PRD is not approved for implementation.

## [2026-10-03] update | Set hybrid demonstrator baseline

* Trigger: the owner selected the hybrid approach as the PRD direction and
  confirmed that current coordination uses Excel files, with no Dataverse or
  Dynamics 365 estate.
* Updated the addendum to classify the Excel-only and absent-platform details
  as owner-confirmed company context; M365 tenant, SharePoint availability and
  licensing remain unknown.
* Revised the PRD to version 0.2.0: Azure owns the proposed programme control
  plane; M365 document collaboration is conditional on verification, with
  controlled Azure Blob Storage as a demonstrator fallback. Excel import is
  tested on synthetic representatives; source workbooks remain unchanged.
* Kept the greenfield business-apps option as a whole-life-cost comparator.
  The hybrid is a proposed demonstrator baseline, not production architecture,
  procurement approval or permission to process resident data.
* Updated the index. Owner-controlled memory and the original case study
  remain unchanged.

## [2026-10-03] restructure | Move PRD to rubric registry path

* Moved the hybrid retrofit PRD from `docs/project-planning/` to
  `docs/prds/`, matching the path anticipated by the rubric artifact registry.
* Updated the PRD session-state path and the knowledge-base catalog link.
* The PRD registry entry is still marked `planned`; this move alone does not
  activate rubric scoring.

## [2026-10-03] query | Role-profile Open Questions register added to the PRD (v0.3.0)

* Ran a second-pass review of the proposed hybrid baseline through all eight
  `company-*` role profiles (Asset Executive, Retrofit Programme Manager,
  Finance and Grants, Procurement and Contracts, Data and Performance,
  Building Safety, Neighbourhood Housing Officer, Resident Engagement) and
  synthesized one open question per role into a new Open Questions section
  in `docs/prds/proper-warm-retrofit-programme-demonstrator.md`
  (OQ-001 to OQ-008), each with an accountable function, evidence to obtain
  and the decision/gate it blocks.
* Labelled the register as role-profile discovery prompts/hypotheses, not
  company facts, resident research or approvals; no row infers a company
  answer, and every row stays Open pending accountable-function evidence.
* Corrected four overstated "Excel-only" passages (Product Context, DD-001,
  CON-007, AC-012) to "Excel-based current coordination; other systems and
  authority unknown," matching OQ-005.
* Preserved MVP scope: synthetic data only, no live resident contact.
* Updated the PRD session-state file
  (`.copilot-tracking/prd-sessions/proper-warm-retrofit-programme-demonstrator.state.json`)
  with the new role-profile review, question history, next actions and the
  evidence boundary, and updated the knowledge-base catalog entry above.

## [2026-10-03] query | Owner direction on BRD Sponsor Discovery Questions recorded (v0.7.0)

* The owner answered all 12 Sponsor Discovery Questions in
  `docs/brds/agentic-retrofit-programme-brd.md`. Added a new subsection,
  "Owner-Provided Direction on Sponsor Discovery Questions (2026-10-03)",
  immediately after the existing question table, recording each answer with
  an explicit evidence-status label.
* Recorded as genuine owner direction, not inferred company fact: acceptance
  of a mixed/unseparated delay cause for elapsed time; a new candidate
  escalation control for more than 5 missed appointments (pending Housing and
  repairs leads' ratification); confirmation that a grant award exists
  covering roughly half the eligible homes; a description of current hazard
  reporting practice (technician write-up or resident phone call, then a
  technician audit); and a direction that the pilot would use all current
  contracts and frameworks.
* Declined to fabricate statistics for four requests with no grounding
  evidence in the repository: survey/install/quality capacity, pilot
  building dependencies, tenure/lease verification share, and local-authority
  stock distribution. These stay fully open.
* For two requests, substituted the existing, already-sourced sector
  benchmarks (rolling stock-survey cadence; first-appointment no-access and
  refusal/withdrawal rates) as explicitly-labelled illustrative reference
  points only, not company evidence.
* For the PAS 2035 role question, the owner asked the company-role agents to
  decide. Dispatched the Housing Retrofit Programme Manager role-profile
  agent and added its six-role hypothesis (Retrofit Coordinator, Assessor,
  Adviser/Designer, Evaluator, PAS 2030 installer/site-supervisor quality
  role, named programme assurance) as a labelled role-profile hypothesis, not
  confirmed staffing.
* No Open Decision (OD-01 to OD-39) was marked resolved; each referenced OD
  stays open pending named accountable-function evidence. Bumped the BRD to
  version 0.7.0 and updated its session-state file
  (`.copilot-tracking/brd-sessions/agentic-retrofit-programme.state.json`)
  and the knowledge-base catalog entry above.

## [2026-10-03] update | PRD strengthened against BRD v0.7.0 and the capstone rubric (v0.4.0)

* Trigger: review `docs/prds/proper-warm-retrofit-programme-demonstrator.md`
  against the updated BRD and the capstone rubric/assessment guide, and
  improve it without inventing company facts or fabricated results.
* Added design-rigor content targeting only the rubric's non-live,
  repo-evidence-scored criteria: a Component Contracts and Failure Domains
  table (architecture decoupling and failure domains), an illustrative
  Threat Model explicitly marked as not yet validated (security), a
  log-schema/correlation-ID/named-SLO-measurement-method observability
  design under NFR-009 (targets left TBD), an AI Model Selection and
  Evaluation Harness section stating no model is selected and no evaluation
  has run, an Agent Orchestration Pattern section (state-graph handoff,
  reflection step, tool-scoped authorization, workflow-only fallback), and
  an Options Gate Scoring Framework with criteria-only, weights-TBD scoring
  (new DD-005, DD-006).
* Added candidate FR-014 and AC-016 for a missed-appointment escalation
  route, traced to the BRD's owner-directed "more than 5" threshold and
  explicitly marked unconfirmed/unratified pending Retrofit and Building
  Safety sign-off. Updated the FR-to-AC, FR-to-GOAL and
  requirement-to-source traceability tables to 14/14 coverage.
* Added an "Owner-direction cross-references (2026-10-03)" subsection in
  Open Questions: BRD v0.7.0 owner direction narrows but does not close
  OQ-002 (PAS 2035 roles, escalation), OQ-003 (grant award is partial),
  OQ-004 (all contracts/frameworks direction) and OQ-006 (hazard-reporting
  description); the four BRD-declined items (survey/install capacity,
  pilot building dependencies, tenure/lease share, LA stock distribution)
  remain fully open and are not modelled from role-profile hypotheses.

* Added a Risk Register row warning that owner-provided planning direction
  must not be mistaken for named-function verified evidence or a ratified
  operational rule, and requiring the accountable function to supply and
  ratify real evidence before FR-014 or any related control is built.
* Did not and could not address the rubric's live criteria (B1-B5, C2,
  scored only in an actual panel session) or A4/D3 (no working demonstrator
  evidence yet; no publication path yet) through PRD document edits; these
  remain outstanding and require separate, non-documentation work.
* Updated the PRD's session-state file, this log and the knowledge-base
  catalog entry above. PRD bumped to version 0.4.0.

## [2026-10-04] query | Restore BRD objective and refresh Define review

* Traced OBJ-11/BG-011 through Git history. Taxonomy migration commit
  `c3e423a` removed the existing objective row while leaving BG-012/OBJ-12
  present and inserting explanatory prose inside the objective table. No
  intentional removal rationale was recorded.
* Restored BG-011/OBJ-11 from the pre-migration row with its assessment-to-
  ready-to-install cycle-time and net coordination-effort measures. Kept the
  20% and 25% targets explicitly unvalidated pending OD-18 and omitted the
  obsolete RULE-023 label. Repaired the table and incorporated the owner-
  directed missed-appointment escalation and all-current-contract pilot
  scope, with Housing/repairs ratification and OD-30 evidence still pending.
* Updated `../brds/agentic-retrofit-programme-brd.md` to v0.8.0 and recorded
  the undocumented owner-reported grant award without changing its controlled
  funding status.
* Refreshed the Define quality review in
  `.copilot-tracking/brd-sessions/agentic-retrofit-programme.quality-review-0.8.0.yml`.
  FR-to-AC and FR-to-BG coverage are both 100%; all 12 goals fail the SMART
  check on missing owner-approved evidence, so Define remains blocked.
  OD-01 to OD-39 remain open and no approval or waiver is recorded.
* Updated the BRD session state and this catalog. The BRD remains a draft;
  Govern and BRD-to-PRD handoff were not entered.

## [2026-10-04] review | Record delegated BG-011 target decision

* Updated `.github/agents/company-executive-reviewer.agent.md` with the owner's
  bounded delegation to either ratify a proposed target for draft planning or
  request changes. The profile explicitly excludes actual company approval,
  waiver, measurement authorization and operational authority.
* The reviewer assessed BG-011/OBJ-11 and returned `CHANGES_REQUESTED`: the
  20% cycle-time and 25% net coordination-effort values remain owner-confirmed
  proposals, but no direct comparator or supporting forecast was found and
  the measurement proposal lacks frozen population, event, baseline, case
  handling, effort-shift and MDE definitions.
* Recorded the decision, exact protocol evidence still required, and open
  approval boundaries in the BRD v0.9.0 and its session state. OD-18 and OD-36
  remain open; no actual company approval, waiver or measurement authority is
  inferred. The BRD remains draft and its Define gate remains blocked.

## [2026-10-04] review | Record BRD role-panel challenge and owner directions

* Consulted the Proper North Homes Executive Reviewer and Asset, Retrofit
  Programme, Finance and Grants, Resident Engagement, Building Safety,
  Procurement, Data and Performance, and Neighbourhood Housing role profiles
  on BRD v0.9.0. Recorded their evidence gaps and accountable follow-ups in
  the BRD. These are research-role perspectives, not actual employee
  statements, company records or approvals.
* Recorded the owner's direction to use Azure-led hybrid only as a provisional
  non-production demonstrator baseline, leaving customer/production
  architecture for the Phase 0 appraisal. Recorded the owner's choice of
  assessment-to-ready-to-install as BG-011's primary cycle-time endpoint,
  with accepted handover reported separately.
* The Executive Reviewer retained `CHANGES_REQUESTED` for BG-011 target
  ratification. Updated the BRD to v0.10.0, its session state, the addendum and
  this catalog. OD-16, OD-17, OD-18, OD-20 and applicable evidence, privacy,
  legal, safety, resident, finance and procurement approvals remain open;
  the BRD remains draft and the latest quality report still covers v0.8.0.

## [2026-10-04] update | Clarify required pilot contract participation

* The owner clarified that every current contract/framework is required to
  participate in live pilot delivery. Recorded this as an owner-directed scope
  condition in BRD v0.11.0, not as evidence of supplier capacity or contractual
  permission.
* Added the explicit gate that Procurement and Legal must verify each
  agreement, authority, data/measurement terms and readiness before supplier
  activity. A failed contract gate blocks live-pilot approval; the owner
  direction waives no legal, safety, privacy or contract control. OD-17/OD-30
  remain open for evidence and approval.
* Updated the session state and knowledge-base catalog. The BRD remains draft;
  the latest persisted quality report remains the v0.8.0 assessment.

## [2026-10-04] update | Clarify missed-appointment threshold direction

* Completed a bounded public-evidence review of missed appointments and
  repeated no-access. The sources use different definitions and denominators;
  none validates five as a sector-wide repeated-event threshold. The
  researcher lane remains marked partial because it did not recover
  attributable provider-policy or forum sources within its access boundary.
* Recorded the owner's directions in BRD v0.12.0: configurable provisional
  default five; strict `>` comparator (sixth eligible event triggers human
  review); only a confirmed appointment with verified resident no-access
  counts; provider/contractor no-shows, cancellations and reschedules are
  separate; count only while the case is active and reset only on human
  closure, retaining the event history.
* Consulted the Executive Reviewer, Asset Executive, Resident Engagement and
  Retrofit Programme Manager role profiles. The Executive Reviewer
  `CHANGES_REQUESTED` outcome applied to the earlier incomplete wording.
  Profiles identified company appointment history, Housing/Repairs
  ratification, resident-impact review, named handoff ownership and
  configuration/change governance as remaining requirements. These are
  simulated perspectives, not actual company approvals or resident evidence.
* Integrated the caveat and owner direction into the case-study addendum,
  updated the project index and session state, and added OD-40 for company
  ratification and rule governance. OD-08/OD-09 and OD-40 remain open; no
  live-use approval is implied.

## [2026-10-04] review | Record threshold follow-up and quality-review blocker

* The Executive Reviewer follow-up found the owner's comparator, event
  categories and case-reset semantics resolved in RULE-006/AC-025, and asked
  that audit history and configuration version remain explicit. Added those
  controls to the requirement; no actual company approval was inferred.
* Invoked the BRD Quality Reviewer for v0.12.0. It confirmed the threshold
  control is covered but could not access the authoritative payload contracts
  in its execution environment and did not emit either required quality
  payload. The persisted v0.8.0 report remains the latest valid quality
  assessment, not a current v0.12.0 review; Define remains unverified and
  blocked pending a valid paired assessment.

## [2026-10-04] update | Align PRD with BRD v0.12.0 missed-appointment rule

* Reviewed `docs/prds/proper-warm-retrofit-programme-demonstrator.md` against
  BRD v0.12.0 RULE-006/AC-025. Updated candidate FR-014 and AC-016 to reflect
  the configurable provisional default of five, strict greater-than trigger,
  eligible resident no-access event, active-case counting, human-closure
  reset, audit retention, no adverse inference and urgent-hazard bypass.
* Limited the acceptance behavior to synthetic, non-production scenarios.
  Added OQ-009 for company appointment evidence, Housing/Repairs ratification,
  Resident Engagement review and configuration/change ownership. Five remains
  an owner-directed provisional value, not a validated sector norm or company
  policy; operational use remains blocked under BRD OD-40.
* The owner confirmed that FR-014 should be exercised in synthetic acceptance
  tests only; no operational approval was inferred.
* Bumped the PRD to v0.5.0 and updated its session state and this catalog.
  The PRD remains draft: no signed BRD handoff or current v0.12.0 quality
  report is available, and OQ-001 to OQ-009 remain open.

## [2026-10-05] query | Define the home-centred retrofit workbench flow

* Reviewed the case study, addendum, BRD, discovery brief, PRD, synthetic data
  dictionary and the restored `feat/proper-warm-prototype` branch at
  `5e52ceb`.
* Expanded the BRD's future-state process with linked building and home
  records, separated safety/eligibility/capital prioritisation, role-oriented
  queues and accepted handoffs, resident complaint/service/defect intake,
  provider work orders and invoice matching, distinct grant claims, budget and
  work approval gates, and source-linked agent next-step suggestions.
* Added a connected workflow portfolio covering stock and prioritisation,
  assessment/design readiness, resident access and choice, procurement and
  capacity, hazard response, quality and defects, invoice/payment and grant
  reconciliation, case orchestration, and portfolio investment. Each maps the
  underlying problem hypothesis to owners, bounded AI opportunities and
  proposed business-value evidence, with end-to-end and task-level comparison
  kept distinct.
* The product direction is a proposed home-centred case workbench, not an
  approved company process. The resident intake scope is limited to service,
  complaint and defect/repair reports, not compensation or reimbursement.
* Updated the BRD to v0.14.0, its catalog entry and this log. Company systems,
  named service owners, resident channels, response targets, delegated limits,
  contract/payment terms and resident research remain open. No fixed payment
  timing or compensation process was inferred.
* No legal or regulatory source was newly verified; the local evidence remains
  subject to the existing register and live-use checks.

## [2026-10-05] query | Rewrite PRD for the full retrofit workbench

* Replaced the narrow demonstrator PRD framing with one role-based Proper Warm
  Retrofit Programme Workbench PRD, using the BRD v0.14.0 home-centred model
  and nine-workflow portfolio.
* Represented every workflow with a workbench module/screen and synthetic
  scenario coverage. Added profile workspaces over shared case data, queue
  signals for new/priority/stale/blocked/attention work, individual and
  guarded bulk edits, auditable handoffs and return/reopen behavior, and
  coordinator heatmap, funnel, timeline, stakeholder progress and
  uncertainty-aware forecast views.
* Kept one PRD because workflows share case identity, permissions, evidence,
  authority controls, handoffs and reporting; staged implementation through
  four increments. Retained bounded, source-linked agent suggestions and
  workflow-only paths.
* Updated the PRD to v0.6.0 with 30 functional requirements, 32 acceptance
  criteria, 13 non-functional requirements, 8 constraints and 14 open
  questions. The PRD remains draft and synthetic-only. No signed BRD handoff,
  current valid BRD quality report, confirmed company process, forecast
  calibration or operational approval is claimed.
* Updated the PRD session state and catalog entry. No legal or regulatory
  source was newly verified.

## [2026-10-06] review | Restore PRD architecture and evaluation evidence

* Read the Capstone Rubric Scorer job log and PR #20 feedback. The reviewer
  identified that the full-workbench rewrite had removed design evidence for
  component contracts/failure domains (A1), a named threat model (A3),
  observability and SLO measurement (A5), AI selection/evaluation (A6), and
  bounded-agent orchestration (A7).
* Restored those areas in PRD v0.6.1, adapting them to the shared role-based
  workbench, bulk edits, returns/reopens, portfolio views and synthetic-only
  boundary. Reintroduced a proposed options gate and the synthetic-only
  missed-appointment scenario. The platform/services, threat model and
  methods remain proposed; no implementation, test result, model selection,
  target, company approval or production authority is claimed.
* Aligned telemetry vocabulary to the shared OpenTelemetry foundations:
  semantic conventions, resource/log fields, trace correlation, bounded
  metric cardinality and PII redaction. Updated PRD state and catalog counts.

## [2026-10-06] query | Clarify capstone case framing and exercise-data provenance

* At the owner's direction, present Proper North Homes as the real customer
  case and attendees as its stakeholders in their actual roles. Clarified
  that the constructed exercise records are not evidence of company
  performance, resident outcomes, systems or operating decisions.
* Updated the BRD to v0.14.1 and the workbench PRD to v0.6.2; aligned the
  index and PRD session state. The underlying operating-data exercise pack
  was not renamed or changed.
* Files touched: `../brds/agentic-retrofit-programme-brd.md`,
  `../prds/proper-warm-retrofit-programme-demonstrator.md`, `README.md`,
  `.copilot-tracking/prd-sessions/proper-warm-retrofit-programme-demonstrator.state.json`
  and this log.
* No regulatory claims, process authority, company baselines or operating
  outcomes were added or validated.

## [2026-10-06] query | Review prototype with all company profiles and UX

* Launched all nine `company-*` role agents in parallel against the current
  constructed-data prototype, including the Executive Reviewer. Collected
  their own-role critiques, then obtained an eleven-profile UX synthesis
  and four relayed discussions with Procurement, Resident Engagement,
  Building Safety and Data/Performance.
* Added `research/ux/proper-warm-prototype-profile-review.md`, updated
  `README.md` and reconciled the working research record at
  `../../.copilot-tracking/research/2026-10-06/proper-warm-profile-journey-critique-research.md`.
* Corrected previous working-record claims that dispatch was unavailable
  and workflow cards only displayed descriptions. They also filter cases.
  Recorded actual ownership/rationale inconsistencies, filter recovery,
  independent snapshot populations and missing portfolio example.
* UX recommends correctness and evidence scope first, then a synthetic
  exception-to-accountable-owner slice before a broader home lifecycle.
  The resident-update model was amended to include purpose, safe-route
  reference and sent evidence, independently of operational acceptance.
* Role agents are research instruments, not employee interviews or company
  authority. Adjacent provider, quality and operator lenses do not validate
  those actual users. No prototype, PRD, original case, regulatory snapshot
  or owner memory was changed; no production control or real-user
  accessibility conformance was established.

## [2026-10-06] update | Integrate prototype review and challenge PRD v0.7.0

* Integrated the nine-company-role review, eleven-profile UX synthesis and
  four relayed discussions into the existing workbench PRD, now draft v0.7.0.
  Added explicit profile journeys, ownership/rationale/source consistency,
  visible filter/reset semantics, independent metric populations and
  resident-update continuity; retained the full MVP architecture and controls.
* Defined read-only prototype slices A/B/C with a versioned fixture manifest,
  complete per-profile defaults, independently reportable acceptance checks,
  evidence comparisons and safe endpoints. This prepares a later prototype;
  no HTML was changed or regenerated.
* Obtained an independent PRD Quality Reviewer challenge and addressed slice
  applicability, hidden conflict inputs, reset oracles, exact traceability,
  receipt/acceptance examples, composite checks and constraint classification.
  Follow-up exposed incomplete defaults and reflow criteria; both were
  corrected and confirmed in a bounded final follow-up.
* Preserved challenge disposition and paired reviewer payloads in
  `../../.copilot-tracking/reviews/2026-10-06/proper-warm-prd-v0-7-0/`.
  PASS covers only the two final amendments, not full PRD quality or approval.
  Validate remains BLOCKED; Finalize is NOT_EVALUATED. Unknown company
  processes, baselines, owners and human approvals remain open.
* Updated the PRD session state and this catalog. The revision has 35 FRs,
  43 ACs, 13 NFRs, 8 constraints and 14 open questions. Reviewed reciprocal
  requirement/criterion links, exact matrix agreement and fixture defaults;
  Markdown lint excludes MD013 to retain existing long-table style.
  No original case, memory, regulatory snapshot or production rule changed.

## [2026-10-07] update | Require committed evidence for rubric criteria

* Reviewed how the rubric gate scored against the capstone assessment guide.
  Section D and the live criteria (B1 to B5, B7, C2, C3) were scored from BRDs
  and PRDs although the guide scores them on a separate artifact and the live
  session, neither of which is committed.
* Added `requires_any`, `cap_without`, `submission_required` and
  `rubric_version` to the rubric, so the gate forces 0 where required evidence
  is absent, caps B6 without a deck and reports an incomplete outcome without
  a thought leadership artifact. Removed D1, D2, C3 and B7 from the BRD mapping
  and activated the deck, pitch and thought leadership registry entries.
* Added `docs/capstone/README.md` as the storage map for every capstone asset
  and updated the catalog. Existing scores are rebaselined on the next run.

## [2026-10-07] update | Add rubric score badge

* The rubric gate now renders `.github/rubric/scores/badge.svg` beside
  `latest.json`, the workflow commits both, and the root `README.md` embeds
  the badge. The lock file was edited by hand to match the workflow source;
  recompile it with `gh aw compile rubric-score` to refresh its hashes.

## [2026-10-07] query | Capture owner prototype usability learnings

* Source: owner feedback on the later application at `localhost:3410`, relayed
  for documentation-only capture; prototype PR #24 is provenance, not a
  dependency or merge prerequisite.
* Updated `research/ux/proper-warm-prototype-profile-review.md` in place with
  the verbatim notes, separate evidence classification, proposed design
  direction and eight unexecuted next-prototype acceptance checks.
* Preserve style, logo, typography, general palette and clarity; correct
  error-like reddish emphasis, role/workflow scope, readiness, accountable
  handoff acceptance and agent input/output/human-decision explanations.
* Record the requested full-screen case, recoverable queue context and
  necessary synthetic address/phone/contact/adjustment/evidence/task context,
  with explicit unknowns and production role/case/field privacy boundaries.
* Difference flagged: the 2026-10-06 source review found workflow filtering
  in its HTML artifact; the owner reports no visible context/filter change in
  the later application. Neither is generalized across artifacts or silently
  treated as superseding the other.
* Updated `README.md` routing/catalog. No original case, addendum, PRD, memory,
  prototype code, generated resident data or tracking artifacts changed.
  No runtime inspection, operational approval or user-tested success claimed.

## [2026-10-08] update | Propose Azure architecture and Bicep

* Added `docs/adrs/0001-azure-architecture.md` and Bicep under `infra/`
  proposing Container Apps hosting, bounded agent placement, Azure SQL with
  ledger, Blob evidence, a two-tier Foundry model deployment, private
  endpoints, managed identities, monitoring and audit controls, derived from
  the PRD component contracts, threat model and NFRs.
* Status is proposed and unverified: Bicep builds and lints, but nothing was
  deployed, and model versions, quotas and region availability are unchecked.
* Updated the `README.md` catalog.

## [2026-10-08] update | Revise Azure architecture after PR 28 review

* Responded to the rubric score on PR 28 (A1 to A5 held below Excellent for
  lack of failure domains, measured operations and deployment evidence). ADR
  0001 gained failure domains and scaling, threat model mapping, operational
  targets and a cost model, and an M365 section covering Entra ID, optional
  SharePoint (`Sites.Selected`) and Teams.
* Bicep gained API 5xx and restart alerts, a budget, a Teams webhook receiver
  and evidence store parameters. PRD v0.8.0 records the proposed Azure and M365
  realisation under the platform boundary.
* Validation: build, lint, ARM validate and what-if only. The deployment was
  not applied because the only writable resource group belongs to another
  project and the template would modify its private DNS zones.

## [2026-10-08] query | Review hybrid M365 Excel transition and deploy test stack

* Researched the hybrid Azure and M365 design (Graph Excel API, `Sites.Selected`,
  Graph without Private Link, Teams Workflows replacing connectors, E3 versus E5
  compliance) and challenged it with the Neighbourhood Housing Officer, Data and
  Performance Lead and Executive Director Assets agents. Added a staged Excel
  transition, measures and open options to ADR 0001 and a summary to the PRD.
  Role views are hypotheses, not company facts.
* Deployed the Bicep to resource group `ama` in `uksouth` after fixing the
  Foundry ordering; `swedencentral` lacked Container Apps capacity. Placeholder
  images only, nothing measured.

* Added the `prototype/` constructed-data code slice (workflow authority,
  bounded agent proposals, hash-chained audit, offline contract evaluation), a
  provisional weighted options appraisal and observed `warm-test` deployment
  timings to ADR 0001. Weights and scores are architect proposals pending
  sponsor approval; the prototype image is not deployed.

* Added the development-only `allowPublicNetworkAccess` Bicep parameter
  (default false) to `infra/`, documented in `infra/README.md`. It opens public
  endpoints alongside the private endpoints for a throwaway dev stack only.

* Added an architecture challenge section to ADR 0001 (Azure SQL kept, ledger
  digest gap, cross-region SQL trade-offs, deferred AI Search, later Document
  Intelligence, Design Thinking experiments) and recorded the North Europe dev
  deployment findings. Agent views are judgement, not company facts.

* Recorded the region selection (uksouth recommended, EU data-zone fallbacks untested) in ADR 0001.

* Recorded the staff data trust and control consultation (architect, product
  advisor, Housing Officer, Data and Performance, Building Safety and Resident
  Engagement role views) in ADR 0001 and proposed trust requirements TR-001 to
  TR-007 in the PRD. Role views are hypotheses, not company facts.

* Added a proposed data handling and retention baseline to the addendum,
  derived from the UK GDPR and Data Protection Act 2018 local copies, the
  Safety and Quality Standard and Awaab's Law guidance. The corpus has no
  numeric retention periods, so every period is a proposed default for the DPO
  and Legal to confirm; limitation and building-life figures are flagged as
  outside the local corpus.

* Regenerated BRD (v0.15.0), PRD (v0.9.0, requirements DH-001 to DH-007) and
  ADR 0001 from the data handling and retention baseline: updated CON-003 and
  OD-14, added an ADR retention alignment table and the Key Vault name
  collision fix. All retention periods remain proposals pending DPO and Legal.

* Added the `keyVaultPurgeProtection` development parameter to the Bicep and documented it in `infra/README.md`.

* Added the Prototype Learnings and Simplicity Review (research/ux) from open
  PRs 19, 24 and 27, critiqued by the UX designer, Design Thinking coach and
  six company-role agents, and proposed PRD requirements SA-001 to SA-010. The
  PRs stay unmerged as evidence. Role views are hypotheses; no staff
  usability study exists.

## [2026-10-08] build | Proper Warm MVP and name generator

* Added `mvp/`, a working case-management application following SA-001 to
  SA-010: sign-in to "My cases today", full-screen case card, plain status
  line, call log, resident decision recorded separately, server-side
  ready-to-book gate, hash-chained audit, Excel export and a forgiving
  spreadsheet check. Drafts are templates; nothing is sent.
* Extended the synthetic data generator with `pw_names.py` (seeded names,
  Ofcom drama-range phone numbers, example email domains, named contractors and
  staff) and `build_mvp_dataset.py`, which places homes on addresses from the
  private stock-geography register. The built data is git-ignored and local
  only because it pairs real map addresses with invented residents.
* Product screens do not label the data as constructed; the README and this
  log do. Sign-in is a shared local password, not Entra ID.

## [2026-10-08] update | Bicep deployment profile

* Added `deploymentProfile` (`production` default, `development`) to
  `infra/main.bicep`. Development enables external network access, disables
  registry image quarantine and drops Key Vault purge protection; production
  keeps every isolation control. Documented in `infra/README.md`. Observed
  during the MVP deployment: a quarantined ACR image could not be pulled by
  Container Apps until released.

## 2026-10-08 MVP improvement loop

* Extended `mvp/` after owner feedback: list filters and sorting, an Overview
  screen with a map, charts and workload, a Visits screen, handover
  suggestions with stated reasons, document upload with an evidence
  checklist, and a funding application workflow with human approval gates.
* Added bounded AI assistance (`ai.py`): briefing, drafted messages, case
  summary, funding wording and document reading. Output is validated, every
  run is audited, templates are the fallback, and nothing is sent or
  submitted by the system. Labelled "AI-drafted, human-approved".
* Dataset builder now adds seeded document records and funding routes.
* Limits: files live on ephemeral disk in the demo, sign-in is a shared
  password, funding routes and statuses are illustrative.

## 2026-10-08 MVP usability pass

* MVP: filters moved to a left panel that loads from the API without page
  reloads, so the AI briefing is fetched once and cached server-side until
  case data changes. Overview now has a zoomable OpenStreetMap (bundled
  Leaflet, BSD-2) with resident-name tooltips, and the KPI tiles filter the
  map. Tiles are the only external request and are allowed in the CSP.

## 2026-10-08 MVP map tile policy fix

* OpenStreetMap blocked the demo's tile requests: the app sent
  `Referrer-Policy: no-referrer`, but the tile usage policy requires a
  Referer (https://osm.wiki/Blocked). The header is now
  `strict-origin-when-cross-origin` (only the origin leaves the site), the
  Leaflet layer sets `referrerPolicy`, and attribution links to the OSM
  copyright page. Production should use a licensed tile provider.

## 2026-10-08 MVP: all cases for everyone, role-tailored My cases

* All cases is now open to every signed-in user with the Owner filter and
  shows other people's cases. My cases lists only the user's own cases and
  each card shows facts for their role (for example contractor and works for a
  Retrofit Coordinator, funding and missing evidence for a Grants and Evidence
  Officer).

## 2026-10-08 Gap analysis and next build

* Added [Gap Analysis and Next Build](research/gap-analysis-next-build.md):
  BRD, PRD, ADR, addendum, research, rubric score and the MVP reviewed
  together. Key findings: capstone deck, pitch and thought leadership assets
  are missing, the rubric registry does not include `mvp/`, durable storage and
  Entra sign-in are not built, and several PRD lifecycle workflows are open.

## 2026-10-08 Owner decisions on build direction

* The MVP replaces the prototype as scored solution code
  (`.github/rubric/artifacts.json`, rubric and capstone READMEs). The next build
  targets pilot readiness. Thought leadership options and the pending OD-14,
  OD-17, OD-19 and OD-36 questions are recorded in
  [Gap Analysis and Next Build](research/gap-analysis-next-build.md).

## 2026-10-08 Owner direction on OD-14, OD-17, OD-19 and OD-36

* Lawful basis: contract for service delivery, consent for works. Vulnerability
  reasons hidden from contractors. Retention defaults accepted as the design
  baseline. Audit entries kept in full for the legal period (the addendum now
  says so, DPO to confirm). Individual staff time capture allowed with staff
  knowledge and a DPIA. Whole stock of about 60,000 homes to be loaded with
  staff choosing priorities, which differs from the BRD pilot size. AI limited
  to recommend, draft, reconcile and flag. Recorded in
  [Gap Analysis and Next Build](research/gap-analysis-next-build.md); none is
  approved by the DPO, Legal or Board.

## 2026-10-08 Ranking rule clarified

* Owner direction: home ranking must be deterministic and policy-versioned; AI
  prioritisation is a recommendation only and never changes the ranking.
  Replaces the earlier note that the product must not rank homes. See
  [Gap Analysis and Next Build](research/gap-analysis-next-build.md).

## 2026-10-08 PRD v0.10.0

* PRD records owner direction as PR-001 to PR-008 (lawful basis, contractor
  visibility, retention, staff time capture, 60,000-home scale, deterministic
  ranking, AI recommendation only) and changes DH-007 to keep audit entries in
  full. Pilot-readiness scope replaces read-only slices as the next step.

## 2026-10-08 ADR 0002 pilot-readiness architecture

* Added [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) (proposed):
  durable Azure SQL store behind the `Store` interface with keyset paging,
  Blob documents and immutable ledger digests, Entra ID with field projections,
  deterministic ranking with an AI recommendation evaluation harness, server
  side map clustering and licensed tiles, deployment and CI, and DPIA-gated
  staff time capture. Owner direction (PR-001 to PR-008, DH-007) is cited;
  nothing is recorded as approved.
* Added a Supersedes/amends note to ADR 0001 and an index row in the README.

## 2026-10-08 Rubric scores the Proper Warm MVP

* `.github/rubric/artifacts.json` solution-code now reads `mvp/` (code, tests,
  Dockerfile, README, generator scripts) and no longer reads `prototype/`.
  Private data and vendored libraries are excluded. Storage map updated in
  `docs/capstone/README.md`.

## 2026-10-08 MVP build slice 1: deterministic ranking and scale

* `mvp/` now ranks cases with a versioned policy (`ranking.py`, v1.0.0, owner
  to be named) with reason codes and a fixed tie-break, per PRD PR-006. AI
  prioritisation is a separate, audited recommendation that can be accepted,
  edited or rejected and never changes the ranking (PR-007). Case lists page
  server-side and the map clusters, tested on 60,000 constructed cases (PR-005).
  Deviations from ADR 0002: offset paging, in-memory ranking cache, policy as
  code. Not deployed; front end checked by syntax only.

## 2026-10-08 MVP build slice 2: pilot-readiness backlog built in-repo

* `mvp/` gained a sqlite-backed SQL store behind the `Store` interface (row
  versions, append-only full-content ledger, hash-chain verify command and
  endpoint, local digests), server-side role projection with a role-matrix test,
  return/reopen, handoff and safety referral workflows, an offline AI
  evaluation harness, an off-by-default time capture gated on `DPIA_APPROVED`,
  an auth provider abstraction (Entra trusted-proxy headers and dev password),
  an accessible map list and configurable tile provider, a hardened Dockerfile
  and `.github/workflows/mvp-ci.yml`.
* Status per item is in the Implementation status section of
  [ADR 0002](../adrs/0002-pilot-readiness-architecture.md). Nothing was run in
  Azure; Entra, Azure SQL and Blob are designed and documented, not verified.

## 2026-10-08 MVP build slice 3: remaining gaps from slice 2

* `mvp/` gained screens for return, reopen (manager "Closed cases" page),
  handoff and safety referral, and contractor screens that show only "needs
  notice" and a named contact (server-side projection; rank also removed from
  the contractor list).
* Added a `DocumentStore` interface with local and Azure Blob (urllib, SAS or
  managed identity) implementations, limits, role checks and audit entries;
  time capture now also needs a consultation reference and a staff notice
  acknowledgement; sqlite list reads, search, sorts and counts run in SQL with
  keyset paging and a 60,000-case timing test; tests for the map list and
  `PW_TILE_URL`; and a manual Playwright check (`mvp/tests/browser_check.py`).
* Unverified: nothing ran in Azure, the Blob store ran only against a fake
  transport, there is no time capture screen, case detail, map and stats still
  read the in-memory copy, and no screen reader run was done. Status per item is
  in [ADR 0002](../adrs/0002-pilot-readiness-architecture.md).

## 2026-10-09 review | MVP and PRD and ADR pending-work review

* Reviewed `main` after PRs #35 and #36 against PRD v0.10.0, ADR 0001 and ADR 0002.
  Added a ranked pending-work section to
  [Gap Analysis and Next Build](./research/gap-analysis-next-build.md).
* Twelve pending items found; the largest are Azure verification, CI scan and
  SBOM, ranking snapshots, AI evaluation measures and citations, and the
  quality, finance and insight workflows. People-dependent approvals are listed
  separately. Internal judgement; nothing was run in Azure.

## 2026-10-09 MVP build: finance, grants, technical sign-offs and resident decisions

* Built in `mvp/` the PRD v0.10.0 requirements FR-018, FR-019, FR-013 and
  FR-014 (ACs 016, 017, 021, 022, 037, 042) as mixins over the case record,
  shared by the JSON and sqlite stores: record-only finance with line-level
  match exceptions and holds, separate grant stages, role-separated technical
  sign-offs with design versions, and per-measure resident decisions with a
  complaint route. Approvals need a different person and refuse bulk requests.
* Unverified: constructed data only, role mapping is a proposal, screens were
  syntax-checked but not run in a browser. Status in
  [ADR 0002](../adrs/0002-pilot-readiness-architecture.md).

## 2026-10-09 MVP build: quality acceptance and procurement (FR-016, FR-017)

* `mvp/` gained quality acceptance per measure (versioned checklist evidence,
  independent acceptance, defects with owners, reinspection, resident handover,
  aftercare) and procurement and capacity (packages, offered versus evidenced
  committed capacity, versioned work orders, appointment outcomes, completion
  and correction). Contractors see only their own work orders, never the
  vulnerability reason. Tests cover state machines, independence, the role
  matrix and parity across the JSON and sqlite stores.
* Covers PRD AC-019, AC-020, AC-039 and AC-042 in the MVP only. Checklists are
  examples, there is no contractor evidence login, and the screens were not run
  in a browser. Status row added to
  [ADR 0002](../adrs/0002-pilot-readiness-architecture.md).

## 2026-10-09 MVP build: AI evaluation measures and citations

* Extended the offline AI evaluation harness (`mvp/properwarm_mvp/ai_eval.py`,
  `mvp/evals/ai_priority_golden.json`) with top-k overlap, Spearman rank
  correlation, critical misses (harness fails on any), citation validity,
  run-to-run variation, latency, model and prompt version, reviewer
  accept/edit/reject counts with reasons and added value against the
  deterministic and workflow-only orders. Negative controls cover the new
  measures.
* Every AI output now carries citations validated server-side
  (`ai_tasks.py`): unresolved citations mark it Unverified, uncited items are
  dropped, and it stays Not reviewed until a person answers. Added a
  workflow-only mode (`mode` flag or `PW_AI=off`) and a comparison record per
  AI task in both stores, a review endpoint and a manager-only
  `GET /api/ai/report`. Updated the ADR 0002 status row for the AI evaluation
  harness and the mvp README.
* Unverified: scripted model only, so latency and variation are not live
  figures; no live-model run, no browser run of the new UI parts.

## 2026-10-09 MVP ranking policy files and snapshots

* `mvp/policies/ranking-v1.json` replaces the Python policy constant: policy
  id, version, owner ("to be named"), status (unsigned draft), effective date,
  rule order and a SHA-256 content hash over canonical JSON, verified at load
  with refusal on mismatch. A registry loads every file so old versions re-run.
* Ranking takes an explicit `as_of` and reads no clock. Managers can read a
  ranking snapshot (policy version and hash, as-of, rank, reason codes,
  deciding rule) at `GET /api/ranking/snapshot`; list headers carry policy
  hash and as-of. Both the JSON and sqlite stores support it.
* Tests: golden snapshot, byte-identical re-run, tampered file refused, old
  version re-run, snapshot unchanged after an AI priority call. Updates
  [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) decision 4 status
  and the `mvp/README.md` ranking paragraph and limits. Unverified: not run in
  Azure; no named owner or sign-off.

## 2026-10-09 MVP on Azure SQL, Blob and two replicas (dev subscription)

* `mvp/properwarm_mvp/mssqlstore.py` adds `PW_STORE=mssql`: the SQL store logic
  over Azure SQL with Entra managed-identity sign-in, a write lock shared across
  replicas, binary collation and an append-only ledger table (or trigger). The
  `mssql-python` driver is pinned with hashes in `mvp/requirements.txt` and the
  image adds the two runtime libraries it needs.
* Verified: 26 store and list-read parity tests on SQL Server 2022
  (`mvp/tests/test_mssqlstore.py`); the dev app `ca-properwarm-mvp` ran on the
  dev Azure SQL `retrofit` database (980 constructed cases), documents in Blob
  through a user-assigned managed identity, two replicas, shared sign-in cookie
  key, a write read back from every replica and after a revision restart, and
  the ledger check intact. The engine refused update and delete on the audit table.
* Found: `retrofit` is a ledger-enabled database, so every table keeps row history
  (note for erasure and retention in the DPIA); replicas need a shared
  `PW_SESSION_KEY` or sign-in fails on alternate requests.
* Not done: Entra built-in authentication (no permission to create an app
  registration, owner action), Bicep for the MVP app, an Azure load test, direct
  Blob listing (no data-plane role), and the SQL Server CI job.

## 2026-10-09

* `mvp-ci.yml` image job extended (ADR 0002 decision 6): Trivy scan failing on
  fixable HIGH or CRITICAL findings, SPDX SBOM artifact, and a read-only root
  file system with all capabilities dropped `/healthz` check. Documented in
  `mvp/README.md`. Verified locally with Docker and Trivy 0.65.0; the GitHub
  workflow result is the proof.

## [2026-10-10] query | System One and reviewed funding forms in the PRD

* Integrated the completed Decision 1 reassessment into
  [IDEA-001 research](../ideas/typesafe-system-one-agent-fit.md), preserving
  the dated Jev/Kev baseline and making current catalog/API limits explicit.
  All nine workflow families and fifteen lifecycle steps were revisited;
  availability is evidence for evaluation, not deployment or housing benefit.
* Updated the [Proper Warm PRD](../prds/proper-warm-retrofit-programme-demonstrator.md)
  to draft v0.11.0: nine new requirements and eleven acceptance criteria for
  registered optional scoring, application-owned evidence explanations,
  versioned forms, candidate extraction/selection, field review, deterministic
  validation, Finance-reviewed packs, dependency invalidation and optional
  assistance without authority-bearing pre-fill.
* Funding application/export, award, reimbursement claim and cash remain
  separate. Unknown route blocks preparation; no actual current funding
  round, template, award terms or eligibility is assumed. Declarations,
  signatures, resident choices, approval and submission remain human-owned;
  live funder submission is outside the demonstrator.
* Updated the idea follow-up, knowledge-base index and PRD session state;
  reconciled stale PRD banner/metadata, upstream version labels, goal-table
  references and index counts. Final counts are
  44 FRs, 54 ACs, 13 NFRs, 8 constraints and 16 open questions.
* Open evidence: approved scheme/schema and critical-field criteria (OQ-015);
  response conformance, task thresholds, serving/privacy/network gates and
  incremental value (OQ-016); existing upstream handoff, named owners and
  human approval gates. No application implementation, model inference,
  deployment or production sign-off is claimed.
* An independent draft challenge identified three amendment gaps: funding
  route requirements on non-funding forms, application/claim event ambiguity
  and extraction/invalidation test oracles. All three received author
  corrections, recorded with original paired reports in the
  [challenge disposition](../../.copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-11-0/challenge-disposition.md).
  The original full-document FAIL and formal approval blockers are preserved;
  no independent final regrade or product approval is claimed.

## [2026-10-10] query | Reconcile System One research and PRD branches

* Compared PR #54's research with PR #55's draft design amendment.
  The nine-workflow/fifteen-step recommendation and form-control boundaries
  were already integrated; no new high-confidence amendment defect was found.
* Preserved the original research Markdown byte-for-byte from commit
  `c9bada6417c05ae961b561078ef1a2b1faa9a17e` in
  `.copilot-tracking/research/2026-10-10/system-one-decision-models-research.md`.
  Did not import the obsolete Research-phase RPI session state.
* Integrated omitted pricing-source assumptions and illustrative arithmetic,
  hosting alternatives, serving-contract unknowns, privacy approval checks
  and task-wide evaluation detail into the existing
  [IDEA-001 synthesis](../ideas/typesafe-system-one-agent-fit.md).
  Updated this index and PRD reference provenance. No new requirement,
  deployment, model result or human approval is claimed.
* PR #55 remains a draft requirements amendment with its existing full-PRD
  quality and approval blockers. Repository merge does not approve
  production use. PR #54 can be closed as superseded once the consolidated
  amendment is safely delivered.

## [2026-10-10] query | Owner-approved exercise assumptions and PRD completion

* The owner clarified that fictional company discovery must not repeatedly
  block exercise design. Programme, Finance, Resident Engagement and Data/
  Performance role agents proposed grounded assumptions; the owner approved
  the reconciled sixteen EXA/OQ dispositions and test targets before edits.
* Added the assumption register to the
  [addendum](../case_study_48_addendum.md#owner-approved-exercise-baseline-2026-10-10),
  with sources, rationale, alternatives, sensitivity/reversal tests and a
  four-week plan from baseline acceptance. USD 450/month is a technology cap,
  not a quote; no purchase, deployment or implementation is authorised.
* Updated the [PRD](../prds/proper-warm-retrofit-programme-demonstrator.md)
  to v0.12.0 in review for exercise-only acceptance. Defines measurable goals,
  workload/recovery, real-inference quality/value, forecast/financial oracles
  and UX engineering checks. Zero unanswered exercise-design questions;
  sixteen real-world validation questions remain.
* Real Decision 1 and generative Foundry inference are essential evidence;
  actual subscription/API/access/processing/cost verification cannot be
  assumed or replaced by scripted replay. No broad new research phase.
* Preserved original case study, owner memory, historical failed quality
  reports and unsigned upstream BRD. No company signatures, legal readiness,
  direct user validation, measured benefits or passing implementation tests
  are claimed. Current-version independent review and final owner acceptance
  follow; historical state/actions are retained as history.
* Updated the knowledge-base index and PRD session state.

## [2026-10-10] query | Reviewed exercise PRD accepted by owner

* Independent v0.12.0 review identified four actionable source concerns.
  Corrected canonical resident-choice/withdrawal decomposition, supplementary
  source aliases, forecast resource/sensitivity semantics and result labels.
  Targeted closure accepted the substantive corrections; two final editorial
  residues were applied and locally verified.
* Current counts: 46 FR, 56 AC, 13 NFR, eight constraints and four SMART
  exercise goals; reciprocal coverage 100%, all ten NFR categories present.
  Original formal FAIL/Validate BLOCKED/Finalize NOT_EVALUATED is retained
  for genuinely absent governed upstream evidence, not fictional discovery.
* The owner accepted the reviewed v0.12.0 exercise baseline for implementation
  planning on 2026-10-10, with no changes. Recorded separate exercise
  acceptance, without company signatures, governed approval or runtime claims.
* [Review and corrections](../../.copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/targeted-closure.md)
  and [local documentation validation](../../.copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/local-validation.md)
  are preserved. Implementation, actual inference and direct human validation
  remain later evidence tasks; this change authorises no application work.

## [2026-10-11] update | Mandatory real-platform exercise builds and PR58 learning

* Updated [BRD v0.16.0](../brds/agentic-retrofit-programme-brd.md),
  [PRD v0.13.0](../prds/proper-warm-retrofit-programme-demonstrator.md)
  and [addendum](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11)
  for the owner's real AI, real SQL and actual Azure requirement in every
  subsequent delivered AMA prototype/PoC/MVP. Original generated 60,000-home
  stock and retained programme lineage continue; small fixtures remain tests.
  New versions are candidates, not inherited v0.12.0 acceptance.
* Added BRD CON-007/AC-086 and PRD CON-009/AC-057 with actual Azure
  workflow, identity, SQL write/read/restart and enabled real AI evidence.
  Missing budget/authority/evidence blocks acceptance, not mock substitution.
  Clarified FR-044/SA-004 optional per-record/manual access without optional
  whole-application AI. Counts: BRD 44 FR/86 AC/9 NFR/7 CON/24 RULE;
  PRD 46 FR/57 AC/13 NFR/9 CON.
* Integrated [pinned #58](https://github.com/jmservera/ama/pull/58)
  `5136f192d583a5bf53adeeec4b0f21369b005c9d` observations into
  [model learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11),
  [simplicity review](./research/ux/prototype-learnings-and-simplicity-review.md)
  and [next-build synthesis](./research/gap-analysis-next-build.md).
  Actual selection/generation and Azure SQL are recorded feasibility;
  calibration, screening, benefit and full acceptance remain unproved.
  Earlier provider-host failures and historical result rows stay historical;
  later source tests are not automatically deployed.
* Recorded the parallel four-arm experiment boundary and versioned result
  intake, independent human labels/full effort, uncertainty and task adoption.
  Proposed protocol is not execution/result evidence. Binary support cannot
  establish three-class macro-F1. Negative/inconclusive tasks do not waive
  required AI/SQL/Azure, or block independent platform/control work.
* Scoped prior USD450/360/405 budget history and #58 rebuild cap override,
  retaining per-build authorization, reservations and usage controls.
  Added dated applicability notes to both ADRs and updated the index.
* Documentation-only implementation: no runtime/deployment/model calls,
  regulatory snapshot, private data or owner-memory changes. Fresh full-BRD/
  PRD quality and owner acceptance remain separate from RPI outcome review.

## [2026-10-11] update | Publish the validated Proper Warm council deck

* Rebuilt the 18-slide Proper Warm executive solution draft for the council
  from the latest 2026-10-11 research. The workbench offer, bounded AI,
  proposed architecture, Excel transition, resident/contractor boundaries,
  controls, evidence gates and unscored platform options are explicit.
* Closed the iteration-2 storytelling findings F01-F11. The independent
  iteration-3 review found no material communications blocker to publication
  as a clearly labelled draft. The main notes contain 1,668 spoken words
  (about 11.9 minutes at 140 wpm); the 517-word appendix is for reference.
  Oral timed rehearsal remains pending.
* PPTX-property and geometry validation each reported zero issues across 18
  slides. Published
  `../presentations/proper-warm-executive-draft.pptx` and confirmed the
  delivery copy matches the validated build by SHA-256
  (`2764263A97F1A8086E6F3DE31A0BDC4376B8BC06F5E0B235A5989341AC664193`).
  At 98,072 bytes, it is below the scorer's 2,000,000-byte file limit.
* Updated `README.md` and `../capstone/README.md`; the existing
  `.github/rubric/artifacts.json` entry already includes the delivery path.
  Working files and review evidence remain under
  `.copilot-tracking/ppt/2026-10-11/proper-warm-executive-draft/`.
* Benefits, product whole-life cost, direct user acceptance, legal currentness,
  full security assurance and production readiness remain unproved. No
  contradiction or new company fact was introduced.

## [2026-10-11] correction | Put the deck in the scorer's base-branch path

* Review of `.github/rubric/scripts/prepare.py` and the `origin/main`
  registry confirmed that pull-request scoring loads `.github/rubric/artifacts.json`
  from the base branch and matches only `docs/capstone/deck/*.pptx`.
  The earlier change that added the delivery path under `docs/presentations/`
  therefore did not make this PR's deck discoverable by the current scorer.
* Added `docs/capstone/deck/proper-warm-executive-draft.pptx` as the scorer
  input and retained the validated delivery copy in `docs/presentations/`.
  The two files have identical SHA-256 hashes. Restored the registry glob to
  the canonical scorer path and clarified the storage map and deck catalog.
* The deck extractor reads slide and speaker-note text. The deck informs B1,
  B2, B6 and B7 when present; B3, B4, B5 and C2 still require pitch artifacts
  where specified by `rubric.json`. Scoring still requires the deck to be
  committed and changed relative to the base.


## [2026-10-11] update | Add architecture diagrams and a working-day view to the council deck

* Rebuilt the Proper Warm executive deck from 18 to 21 slides in response to scorer feedback and owner direction: a system landscape (slide 5), a layered architecture (slide 7) and a same-case working-day comparison (slide 8). All architecture is labelled proposed, not deployed.
* Speed and experience gains are stated as mechanisms and hypotheses to test; no time, error or benefit measurement is claimed. Main spoken script is about 15 minutes.
* Both validators report 0 issues. The delivery and scorer copies are identical (SHA-256 ABD74B0F2EC8F82EE042E077CF3608FA6A8AC91663B672860E6701B980C3317E). A scorer note: the bot's reviewer rated the deck B1, B2, B6 and B7 at 4 but ignored the change because its evidence cited no changed file by path.

## [2026-10-11] correction | Diagnose discarded capstone slide citations

* Inspected the actual scorecard and trusted context from PR #61 workflow run
  `38174177112`. The capstone deck was found and assessed, not missing. Its
  submitted citations used `path.pptx:slide1` and other slide numbers; the
  deterministic gate stripped text line anchors only and treated these as
  different filenames. It therefore retained missing-deck baseline rationales.
* Added strictly scoped positive slide-number anchor support for PPTX
  references and clarified original-file citations in the scorer prompt.
  Recompiled the workflow with the installed v0.89.21 compiler. Nineteen
  targeted tests passed, including unchanged-file rejection and missing
  pitch/thought-leadership controls.
* Replayed that saved scorecard: the previous parser retains 35/100; the
  repaired parser records 47/100, with B1=4, B2=3, B6=4 and B7=4. This is a
  reproduction of the old assessment, not a new grade for the revised deck.
  Ordinary PR scoring uses the gate from `main`, so owner-approved merge and
  a subsequent run are required to activate the repair.
* At the owner's request, removed the saved executive draft from
  `docs/presentations/` and redirected the catalog and capstone storage map to
  the sole executive publication in `docs/capstone/deck/`. The separate mentor
  deck is unchanged. No previous log entry or score baseline was rewritten.

## [2026-10-11] update | Reframe the capstone as accountable agent-led change

* Rebuilt the 21-slide council deck around the 60,000-home mission, original
  five-agent request, eight role-agent research instruments and three
  request/discovery/build chains. The bold proposal is justified as a shared
  foundation for the requested capabilities, not replacement of the whole
  company, its teams, suppliers or source systems.
* Made the new way of working tangible through one constructed home,
  ownership, lifecycle states, timestamps, blockers, accepted handoffs and
  evidence. Explainable decisions retain source/version, rule/reason,
  reviewer, event and authorized override; people retain approval and consent.
  Architecture diagrams, supported Excel transition, resident/contractor
  service and separate programme/AI comparisons support that argument.
* Independent narrative and full-slide visual review found no blockers.
  Applied its three editorial findings and rebuilt with zero issues in both
  validators. Final main narration is 1,919 words, approximately 13.71
  minutes at 140 words/minute; timed rehearsal and measured benefits remain
  open. Review and execution records remain in the deck tracking workspace.
* Published only `docs/capstone/deck/proper-warm-executive-draft.pptx`.
  SHA-256: `bb857cb474ad03c38a29c26af052556a4933ef6cdf762cd6bf0eaa53862d2e03`.
  Verified its scorer-extracted slide/notes text and equality with the
  validated working build. No new production, spending, legal or operational
  acceptance is claimed.

## [2026-10-11] validation | Fresh calibration measures the revised capstone

* Report-only workflow run
  [38177388117](https://github.com/jmservera/ama/actions/runs/38177388117)
  completed successfully on `6a8b60a`. The revised deck received B1=4, B2=4,
  B6=4 and B7=4. Narrative, executive/technical register, written structure
  and evidence-labelled financial storytelling were explicitly cited using
  the capstone PPTX path and slide numbers.
* The full-portfolio calibration is 43/100: A=23, B=16, C=4, D=0. Missing
  pitch and thought-leadership artifacts were still forced to zero; outcome
  remains Incomplete. This is a fresh assessment with baseline withheld,
  not an incremental comparison or overwrite of `latest.json`. Normal PR
  scoring still needs the repair on `main`; no merge was performed.
* The wider rubric test run produced 100 passes, one skip and 19 failures.
  An unchanged pre-repair snapshot reproduced the same 19 failures due to
  historical seed/prototype expectations. The snapshot's initially omitted
  workflow fixture added one extra failure; restoring it made that test pass.
  All 19 targeted slide-citation and required-artifact tests passed. No
  unrelated historical fixture or actual score baseline was modified.
## [2026-10-11] update | Decision 1 rebuild specification and PR 58 learnings split

* Added the [Decision 1 behaviour specification](./research/decision-1-behaviour-specification.md),
  derived from the unmerged [PR 58](https://github.com/jmservera/ama/pull/58)
  source and tests, so the capability can be rebuilt from scratch.
* Carried only the PR 58 documentation learnings in
  [System One Decision Models](../ideas/typesafe-system-one-agent-fit.md) and
  the synthetic-data README. The BRD, PRD, addendum, ADR and code changes stay
  in the draft PR until the code is validated on the current infrastructure.
* Documentation only: nothing re-run and no deployment or model call.

## [2026-10-11] update | Decision 1 integrated into the application design

* Updated the addendum's
  [agentic architecture](../case_study_48_addendum.md#decision-1-in-the-application-design-2026-10-11)
  to place Decision 1 inside Proper Warm's workbench/domain API/AI service
  boundary, not as a separate PoC or approval authority.
* Linked the [rebuild specification](./research/decision-1-behaviour-specification.md)
  to the overall design, separating scoring, generation, review and controlled
  application. Complete human review/application is a rebuild requirement,
  not an assertion that draft #58 delivered every action.
* Preserved manual handling, deterministic controls, task-level comparative
  evaluation and the distinction between design, feasibility and benefit.
  No runtime changes, deployments, inference or production approval.

## [2026-10-11] update | Zava Forward migration tooling

* Owner selected Zava Forward as the programme name alongside Zava North Homes.
  Added a [temporary migration script and guide](../../tools/rename-zava.md),
  with dry-run inventory, explicit apply, text/path and PPTX/slide-source
  changes, local logo embedding and per-file partial-failure reporting.
* Preserved historical records, regulatory snapshots, owner memory, original
  case study and external evidence URLs. Working-copy migration does not
  rewrite Git history or alter user-local untracked configuration/secrets.
* Azure reset/redeployment and visual deck acceptance remain explicit later
  actions, not side effects of the local rename command. Disposable synthetic
  exercise state is not a production data-loss policy.

## [2026-10-11] update | Zava Forward local branding migration

* Applied the owner-selected company/programme names to active documentation,
  package/import names, runtime environment and CSRF contracts, infrastructure
  defaults, website and four PPTX files. Retained the original case study,
  regulatory snapshots, owner memory, earlier log entries and pinned URLs.
* Historical links into the renamed PRD and UX synthesis retain exact original
  snapshots, declared in
  `.copilot-tracking/renames/zava-forward-history.json`. Active index links use
  the renamed documents; no new broken Markdown targets remain against the
  pre-migration baseline. Ten pre-existing placeholder/relative-link defects
  remain outside this rename's scope.
* Twenty migration regressions pass; the renamed MVP runs 270 tests with 26
  existing skips, and the prototype runs 15 tests. Bicep compiles. All 40 slide
  sources pass pipeline dry-run; four decks render with zero logo/text
  bounding-box intersections, and published mentor bytes match the working copy.
* The retained synthetic fixture still has 980 cases, of which 443 are open.
  Local browser checks show populated lists, 443 map points, loaded map tiles
  and the supplied logo. This uses localhost development authentication, not
  evidence of live Entra acceptance, SQL restoration or actual model inference.
* Azure recreation remains blocked on API app-registration permissions:
  both the current Azure identity and M365 session receive `Insufficient
  privileges`. The owner approved resource deletion inside `ama` and downtime,
  but no resources have been deleted and live Entra login is not claimed.
  The [rebuild guide](../../tools/rename-zava.md#azure-reset-and-acceptance)
  records the remaining dependency and acceptance boundary.

## [2026-10-11] update | Rename reconciled with the new executive capstone deck

* Preserved the owner's concurrent merge of #61 into the rename branch using
  a normal history-preserving merge. The only conflict was the rubric score
  snapshot; its remote workflow record was retained unchanged, rather than
  mixing evidence from two scores or rewriting historical assertions.
* Migrated the newly published executive deck, its 21 slide sources and Python
  authoring scripts. Final coverage is five PPTX files and 61 slide sources;
  the additional deck renders with no logo/text intersections and its sources
  pass the shared pipeline dry-run. Research/review records remain historical.
* Historical rubric snapshots are explicit migration exceptions. A new
  regression reuses identical PPTX inputs' output bytes so working/published
  copies do not drift only because separate saves carry different ZIP times.
  There are now 21 migration regressions; earlier validation entries remain
  snapshots of their own passes. The Azure app-management blocker is unchanged.
* Seven targeted rubric deck-citation tests pass. The scorer includes the
  renamed MVP/generator paths and still excludes private dataset/vendor files;
  no score was manually increased or recalibrated as part of this rename.

## [2026-10-12] update | Renamed Azure stack rebuilt from an empty group

* Removed active resources in the owner-authorised `ama` scope, including
  recreatable workload identities and the budget omitted by generic inventory.
  Confirmed empty resource and budget indexes; retained the group, external
  operator and tenant/M365 resources. Foundry project/account and AMPLS/App
  Insights deletion dependencies required explicit ordering corrections.
* Both staged Zava deployments succeeded. Built the real versioned image,
  privately transferred the retained auth credential, recreated SQL grants
  and restored the continuing 980-case fixture with 443 open cases.
* Workload-identity checks confirmed SQL reads/writes, actual inference from
  both model deployments and persisted audit entries after an actual API
  revision restart. Public health is 200, API without credentials is 401 and
  browser entry redirects to Entra. No authentication bypass was introduced.
* Updated [infrastructure rebuild instructions](../../infra/README.md#from-empty-rebuild-observed-on-2026-10-12)
  and the [migration guide](../../tools/rename-zava.md#recorded-azure-rebuild-on-2026-10-12).
  Added explicit API model invocation, user-assigned model token selection,
  foundation-only bootstrap and transitional tenant-role mapping. The MVP has
  272 tests run with 26 existing skips.
* Interactive sign-in, scoped browser lists/map and the tenant name/role
  transition remain gated on an authorised registration owner adding the new
  callback. Existing role values are a declared external identity exception.
  Worker placeholders and planned Decision 1 scoring remain separate limitations.

## [2026-10-12] update | Remaining Entra gate checked through the M365 session

* Continued the owner's requested acceptance work after the completed reset
  review. The delegated M365 client's current Graph scopes lack application
  management; its existing login does not authorise app-registration updates.
  Official Graph update guidance requires delegated `Application.ReadWrite.All`
  and suitable user authority, not just `Application.Read.All`.
* Tried the supported delegated-token route for the rebuilt API without
  disclosing a token. It returned `AADSTS65001` (consent required), so it cannot
  replace the missing authenticated browser session.
* Updated [provisioning access guidance](../../infra/README.md#api-registration-management-with-the-existing-m365-session).
  Runtime authentication and claims remain unchanged. The child acceptance
  task is blocked on authorised owner action; the reset task's single Review
  is not repeated and full migration acceptance is not claimed.

## [2026-10-12] update | Repeatable callbacks and missing-logo permission repair

* The owner reports the callback repaired and requests repeatable initialization.
  Added [callback-only initialization](../../infra/README.md#post-deployment-api-authentication-initialization)
  after deployment: discover the existing client/FQDN, explicitly authenticate
  through an isolated tenant profile, preserve redirects/settings and verify
  the minimal update. Thirteen mocked-CLI tests pass; this is not live Graph or
  interactive browser acceptance.
* Diagnosed the owner's missing logo from the deployed server's PermissionError.
  Migration-created assets inherited mode 0600 from temporary files; Docker
  retained root ownership, preventing runtime UID 10001 from reading the PNG.
  New public assets now use 0644 and image packaging normalizes web readability.
* Added a logo HTTP regression and a restricted-source-permission image check.
  The MVP suite runs 273 tests with 26 existing skips; 22 migration regressions
  pass. Ingress authentication and separate tenant/browser acceptance gates
  remain unchanged.
* Rebuilt and deployed the repaired image from the restricted-mode source.
  The actual UID 10001 API now returns the exact 14325-byte PNG with image/png
  and mode 0644. Health remains 200, unauthenticated ingress remains 401 and
  browser entry remains an Entra redirect. Full signed-in browser acceptance
  is still a separate gate.

## [2026-10-12] update | Public welcome, own-account photos and renewable token storage

* The owner confirmed working workbench sign-in and completed an isolated
  provisioning login. The initializer then verified the retained callback;
  opt-in `--account-photo` merged delegated own-user Graph `User.Read` and a
  read-only rerun verified it. Existing roles, credentials and redirects were
  retained. This is not a grant of administrator consent or wider runtime
  directory authority.
* Added a public branded root with explicit sign-in and protected `/app`.
  Exact platform exemptions cover only the welcome, its logo/stylesheet,
  sign-in and probes. Live anonymous root/logo/styles return 200, while APIs
  and non-browser workbench requests still return 401.
* Added an accessible account panel and fixed server-only own-photo proxy:
  real Entra name/email, role, photo or initials with explicit status, safe
  logout/switch and one bounded provider refresh. Synthetic browser checks
  cover mobile containment, keyboard closure, expired-photo handling and
  production role failure without a password form. They are not real-user
  photo/consent acceptance.
* ACR db3 built the real image. Bootstrap and activation deployments succeeded.
  The real maintenance job succeeded and wrote a SAS expiring five days later.
  Verified shared keys/public Blobs disabled, token-only classification and
  container-/single-secret-scoped grants. Activated supported token store,
  delegated scopes and versionless rotation without reading token values.
* Updated [setup and rotation instructions](../../infra/README.md#public-welcome-and-microsoft-account-photos),
  [MVP account behavior](../../mvp/README.md#entra-id-on-container-apps), and the
  knowledge-base routing. MVP 284 tests (26 existing skips), initializer 15
  tests and migration 22 tests pass; Bicep build/lint and JavaScript syntax pass.
  Fresh real-user sign-in, consent/photo and account-switch acceptance remain
  explicitly separate from provisioning and synthetic checks.

## [2026-10-12] update | Successful photo rendering requires image-only Blob CSP

* The post-implementation Review reproduced a real success-path failure:
  the account-photo client creates a Blob object URL, but the response CSP
  did not allow `blob:` images. A live Chromium check used only the public
  logo as binary input, without a personal photo or fabricated live session.
* The necessary scoped repair permits `blob:` only in `img-src`; default,
  script and frame permissions are unchanged. Two regressions cover the
  image-only source and authenticated binary MIME/no-store/no token output;
  both pre-existing exact tile-host assertions are retained and updated.
* The full suite passes 286 tests with 26 existing skips. Real ACR db4 and
  image-only deployment succeeded; latest-ready revision 0000004 renders
  the binary Blob image successfully. Existing auth/token store stays enabled.
* Updated [account behavior and CSP](../../mvp/README.md#entra-id-on-container-apps)
  and routing. Prior Review findings remain historical, not rewritten as
  closure. Fresh legitimate photo/consent/account-switch acceptance is still
  separate and unavailable while the owner is away.

## [2026-10-12] update | Tenant people require app roles and internal staff bindings

* Live Coordinator denial was `no staff record with this oid`, after successful
  tenant/role validation. An enterprise-app assignment is not a staff binding;
  SQL staff is loaded once and requires replica restart after initialization.
* Owner explicitly requested tenant people rather than generated staff names,
  preserving the main admin and existing Coordinator. Existing ten positions
  plus one supplier-scoped Contractor require eleven distinct people to
  demonstrate all eight role kinds without changing workload codes.
* Added a repeatable [private-roster initializer](../../infra/README.md#tenant-staff-and-application-role-initialization),
  read-only check, app-only add-missing grants, atomic current roster/owner-label
  update and restart recovery. Directory roles/groups, stock and historical
  actors are not rewritten. Directory identities remain outside Git.
* Twelve new synthetic methods cover effective roles, fail-closed validation,
  transaction preservation/rollback and no-op restart recovery; existing
  authentication assertions are retained.

## [2026-10-13] update | Explicit account selection and canonical deployment learning

* Owner confirms tenant access but reports Use another account only signs out.
  Separate switching from logout: fixed switch route requests select_account
  directly. Ordinary sign-in/sign-out and fail-closed role/oid/CSRF checks remain.
  Five constant app-flow markers now feed the existing diagnostics; actual
  table is ContainerAppConsoleLogs. No generic token/query/identity logging.
* Local 289-test suite (26 existing skips), non-root read-only image and live
  tenant/callback/prompt/anonymous boundaries pass. Image-only rollout compares
  private app/auth configuration and all ready replicas; current image
  account-switch-20261013-01, revision 0000009. A fresh anonymous browser is
  not an observed authenticated account replacement.
* Owner requests learning in its proper project documents. Integrated dated
  rebuild/asset/initialization, identity versus app access, preserved workload/
  history, own-photo Blob CSP/token store, account choice, diagnostics and CI
  evidence into [ADR 0002](../adrs/0002-pilot-readiness-architecture.md#observed-exercise-identity-and-session-learning-2026-10-13),
  [PRD v0.13.1 learning](../prds/zava-forward-retrofit-programme-demonstrator.md#review-learning-disposition)
  and [addendum](../case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213).
  PRD counts/approval unchanged; no new business fact warrants a BRD change.
* Specified rubric job failed with Copilot provider HTTP403; owner's attempt 3
  succeeded. Other prior-head checks lacked runner admission, not failing
  application tests. Scores, runner execution and real-user/product acceptance
  remain distinct. No secrets, directory roster, original case, memory or
  regulatory snapshots changed.

## [2026-10-13] validation | Account-switch source publication and runner recovery

* Published source and canonical learning as baf6a5c on continuing PR #65.
  MVP CI run 38368944188 passed test, mssql and image; MVP validation
  38368944195 and Prototype validation 38368944263 also passed.
* Read-only recheck confirms prior-head MVP CI and both validation workflows
  passed on owner-started attempt 2. Earlier runner admission failures remain
  history, not current application defects. Scorer execution and rubric/score
  remain separate; these results do not close personal browser acceptance.

## [2026-10-13] audit | PR #65 documentation and handover reconciliation

* Reviewed owner feedback, checkpoint/PR review provenance, current source
  contracts, operator guides and canonical PRD/ADR/addendum learning. Preserved
  pending real-session, own-photo, full-role/workflow, M365, accessibility,
  calibrated AI benefit, pilot and production gates; no requirement or approval
  was added. The BRD changes only missed wrapped branding, not its business
  contract; original case, owner memory and regulatory snapshots are unchanged.
* Corrected contradictory local-only/unrun claims in the
  [MVP guide](../../mvp/README.md#honest-limits), added the
  [current operator handover](../../infra/README.md#current-exercise-handover-2026-10-13)
  and [ADR delivery delta](../adrs/0002-pilot-readiness-architecture.md#current-exercise-delivery-delta-2026-10-13),
  and distinguished optional M365 provisioning from active Blob/own-user-photo
  permissions. Contributor guidance now acknowledges executable tests.
* Restored real historical warm-* deployment IDs and ca-properwarm-mvp
  app/revision evidence rather than silently rename observations. Corrected
  wrapped company/programme names in active syntheses; preserved exact
  historical snapshots and log entries. Migration regressions cover whitespace,
  retained identifiers and CSP-compatible document-workbench logo styling.
  The document-workbench also now explicitly serves the binary PNG route;
  25 migration and five Node tests passed. Browser rendering confirmed the
  loaded logo at 114x40 CSS pixels after preventing flex compression.
* The mentor delivery is a 15-slide PPTX, byte-equal to the working copy
  (SHA256 c40c4295c2bcf45bcdba98c8c65ab39579a6694e80cc4337ef9495aac2307f3e).
  Updated the index to supersede the earlier publish-blocked note. This audit
  checks metadata/equality and existing recorded migration validation, not a
  new narrative/visual redesign or a fabricated post-iteration build.
* Current source-head checks and the scorer are distinct from capstone/product
  acceptance. Final publication checks are recorded separately; this audit
  does not merge #65 or start the previously stopped RPI follow-ups.

## [2026-10-13] update | Use standard workflow tokens and exclude tracking-only CI

* Merged #65 at the owner's explicit request, then started the independent
  `fix/rubric-github-token` branch from the merged main. The original checkout's
  private/untracked configuration is untouched.
* The [rubric operator guide](../../.github/rubric/README.md#owner-setup) now
  documents automatic Actions-token authentication: `copilot-requests: write`
  for inference and explicit built-in token selection for checkout/fetch,
  GitHub reads and safe outputs. Trusted prepare/record jobs retain their
  scoped status/review/content/issue permissions; the agent cannot write
  repository content. No repository secret was created or deleted.
* Checked the [official authentication reference](https://github.github.com/gh-aw/reference/auth/)
  on 2026-10-13. Token-based inference still depends on Copilot authorization
  and billing eligibility; user-owned repository compilation does not prove
  organization-style inference access. No PAT fallback or entitlement
  change is implied.
* Tracking-only push/PR changes no longer start rubric or prototype workflows;
  MVP workflows already restrict paths to source/infrastructure. Mixed
  source changes still trigger applicable validation and manual dispatch
  remains available. Required-check and cumulative-PR-diff caveats are explicit.
* Regenerated the lock using gh-aw v0.89.21; repeat compilation is byte-identical.
  Authentication, job-permission, all-four-workflow path-filter and existing
  generated-schema checks passed: 13 tests. Seven real-MCP-runtime tests were
  skipped because the pinned external runtime was unavailable; no runtime or
  live model result is represented as Passed. Updated index routing.

## [2026-10-13] audit | Draft experiment PM and UX closure learning

* Reviewed all four open drafts at their exact heads against main `71aaf9d`,
  using pinned source, captured PR metadata and the requested UX Designer
  review. No new app execution, browser/user study, deployment, tenant change
  or resource teardown was performed. Existing tests, owner reports and old
  revisions remain dated evidence, not newly reproduced acceptance.
* Added the [closure inventory and #58 disposition queue](./research/gap-analysis-next-build.md#draft-experiment-closure-review-2026-10-13).
  Recommend retiring #19/#24/#27 as learning only after capture merges and
  owner authorization; #58 remains draft pending explicit carry/replace/defer
  decisions and current-infrastructure verification. None of the four pinned
  heads is an ancestor of inspected main; retirement does not imply all code
  is merged, requirements accepted or resources deleted.
* Integrated genuinely missing [UX recovery/capability learning](./research/ux/prototype-learnings-and-simplicity-review.md#draft-ux-closure-review-2026-10-13),
  preserving owner feedback alongside later #24 source behavior and replacing
  untested first-task failure assertions with hypotheses. Existing human,
  role, accessibility and value checks remain unexecuted. Current welcome/
  account progress does not replace absent #58 connected journeys.
* Added [ADR regression and resource boundaries](../adrs/0002-pilot-readiness-architecture.md#retained-draft-architecture-learning-2026-10-13):
  atomic state/event/replay, exact intent, independent handover reacceptance,
  current work-order/scope binding and preserved historical/resident records.
  Old local runbooks/topology do not become current operator contracts.
* PRD v0.13.2 is evidence-only: corrected actual historical #19 branch
  provenance and linked recovery, invalidation and carry-forward learning.
  IDs/counts/approval are unchanged. Updated addendum and index; BRD v0.16.0,
  original case, owner memory and regulatory snapshots remain unchanged.

## 2026-10-13 Combined assistant source and blocked-reset publication

* Preserved concurrent intended-proposal identity correction `687e4aa` with
  a normal merge, without rewriting PR ancestry or losing generator/ledger
  corrections. Combined source `ec7721b` passes 389-test discovery (316 passed,
  73 conditional SQL skips) and all 73 actual disposable SQL tests.
* Built exact-source image04 locally:
  `sha256:d5eba379f5fd2ce5d9a38965357c193be88eb1882f8e62f75b06faa5aa52fe22`.
  Updated the [ADR receipt](../adrs/0002-pilot-readiness-architecture.md#fresh-ledger-and-synthetic-coverage-learning-2026-10-13),
  PRD, operator guide and index. Rendered nine changed canonical pages and
  checked links, fragments, frontmatter and protected evidence.
* Database reset remains cancelled, image02/revision11 remains the disabled
  serving version, and no model call or image04 cloud deployment is claimed.
  Prepared synthetic counts and all private tenant bindings remain separate
  from live acceptance; historical Reviews are preserved.

## 2026-10-13 Populated visits renderer and exact-image local validation

* Generated-data browser QA found 38 booked visits in the actual API but zero
  rendered rows: the shared page renderer discarded arrays of day-group
  elements. Source `a76d281` flattens before filtering nodes and adds a two-day
  appointment/case-link regression.
* Latest local image05/source `cd14b3b` passes 21 browser regressions and 21
  exact-image generated-data UI/API/restart checks. All 38 visits, 12 Finance
  rows and 601 source work orders render; funding/quality remain pending,
  and all five assistant requests remain disabled/manual. Independent SQLite
  checks preserve domain/proposals through restart with zero provider attempts.
* Updated PRD, [ADR receipt](../adrs/0002-pilot-readiness-architecture.md#fresh-ledger-and-synthetic-coverage-learning-2026-10-13),
  MVP/operator guide and index. This is safe local evidence only: the Azure
  database remains intact, the reset cancellation is not bypassed, and expired
  QA authority is not renewed by a general autonomous-continuation instruction.

## 2026-10-14 Authorized exercise SQL recreation and five real assistant paths

* Owner explicitly reauthorized deletion/recreation and all offered remaining
  delivery. Recreated only `retrofit` with ledger/serverless/backup settings
  and diagnostics restored; restored original contained SQL users/grants and
  all 11 private tenant staff bindings without tenant changes. The generated
  baseline now serves 980 cases, 38 visits, 12 Finance/quality/grant/request
  records, one package/601 source orders and four offered handoffs.
* Published exact image05/source `cd14b3b`, manifest
  `sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`,
  in existing API revision `--0000012`. Five registered deployed operator
  paths returned distinct citation-validated ready proposals through real
  Azure OpenAI `standard`/`gpt-4.1-mini-2025-04-14`: five attempts/6884 tokens,
  15 append-only ledger events and one finite allowance.
* Independent controlled-domain hashes and full assistant-table content
  hashes/outputs/usage survived actual revision restart. Bounded authority
  activated 06:41:03Z, expiry 07:41:03Z, limited to 10 calls/126000 tokens;
  only five calls used. Normal serving authority remains absent/proactive off.
  No human approval, staff-browser acceptance, semantic/value or production
  acceptance is claimed; previous recommendations/audit were deliberately reset.
* Updated PRD, ADR, addendum, operator/MVP guides, synthetic recipe/dictionary
  and index. Transport timeouts were reconciled against zero durable attempts
  before first model dispatch; transient stale-replica exec errors caused no
  inference retry or allowance replenishment. Historical sources and Reviews
  remain unchanged.
  The available four-arm MVE evidence is proposed, not verified benefit results.

## [2026-10-13] ingest | Agent process map and PowerPoint handoff

* Created the [agent process map](../capstone/deck/agents-in-retrofit-process.svg)
  and matching high-resolution PNG, grounded in the addendum, PRD and agent
  request challenge. Five stage-specific assists distinguish staff-requested
  help, proposed event/scheduled review and the separate human decision owner.
  Rules own progression; agents do not gain approval, resident consent,
  instruction, submission, quality acceptance or payment authority.
* Handed supplied content to the installed PowerPoint Builder, which inserted
  one slide after the AI boundary. Published the verified 22-slide
  [capstone deck](../capstone/deck/zava-forward-executive-draft.pptx), with the
  new map at slide 13 and all 21 original slides, notes, images, masters and
  layouts retained. Only moved page counters and necessary notes backlinks
  changed. The parent inset the new artwork/footer/logo to resolve nine
  edge-margin warnings, then rebuilt only slide 13 and re-exported. The shared
  builder ignores `alt_text`; a small partial-build helper embeds the YAML
  description, which was verified in the actual published PPTX.
* Added an accessible [text equivalent and value tests](../capstone/README.md#agents-in-the-retrofit-process-2026-10-13),
  new-slide notes/alt description and sources, and an addendum explanation.
  Updated the index. Working YAML, diagram source/contract, handoff and
  validation evidence remain under `.copilot-tracking/ppt/2026-10-13/`;
  the sole delivery is in `docs/capstone/deck/`, not `docs/presentations/`.
* Validated all-slide notes/count, new-slide geometry (zero issues), original
  shape XML apart from allowed counter digits, exact notes/image content and
  unchanged original master/layout/theme parts. Inspected fresh LibreOffice
  renders of slides 12-14. SDK vision validation and real PowerPoint/Aptos
  rendering are unavailable/deferred, not passed; the source deck's existing
  font substitution remains distinct from this addition.
* Improvements are unmeasured hypotheses, to be tested against paired rules/
  manual work including preparation, review, correction and shifted burden.
  Proactive watchers are proposed, not claimed deployed. No new requirement,
  regulatory currentness claim, resource change, draft closure, merge,
  user acceptance, timed rehearsal or capstone score is implied. BRD, PRD,
  original case, owner memory and regulatory snapshots are unchanged by this
  diagram/deck continuation.

## [2026-10-13] update | Five bounded reactive/proactive assistant contracts

* Updated the [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md#five-reactive-and-proactive-assistants-2026-10-13)
  to v0.14.0 with the five stable capabilities, distinct permitted sources,
  proactive predicates, reactive/reviewer audiences and separate human
  decisions. Added FR-047/AC-058 to AC-061 and traceability: 47 FRs, 61 ACs,
  unchanged 13 NFRs/9 constraints. Historical v0.12.0 approval is preserved,
  not inherited; fresh requirements/owner acceptance remains open.
* Amended [ADR 0002](../adrs/0002-pilot-readiness-architecture.md#five-assistant-exercise-runtime-2026-10-13)
  for shared API/SQL proposal execution rather than five apps: durable
  deduplication, fenced leases, bounded shared reservations, recipient-safe
  sources and atomic source/version-bound human review. Provider calls hold no
  domain lock; unknown usage is not zero or an exactly-once billing guarantee.
* Reconciled [ADR 0001](../adrs/0001-azure-architecture.md) and this index:
  separate agent/queue/orchestrator resources remain proposed. These contracts
  do not establish deployed parity, semantic quality, measured value, control
  approval or production readiness. Build evidence is recorded separately.

## [2026-10-13] implementation | Five-assistant workbench version and build boundary

* Implemented the five v1.0.0 capabilities in the existing MVP with separate
  request/proactive provenance, durable SQL claims/allowances and independently
  source-verified proposal review. Existing controlled case state is not the
  assistant write target. [MVP configuration/API](../../mvp/README.md#five-retrofit-assistants-2026-10-13-implementation)
  keeps authority, expiry and finite shared limits explicit; proactive defaults
  off. Fixed safe worker/scan warnings and bounded backoff avoid silent failure.
* Recorded [exact source/local image and CI evidence](../adrs/0002-pilot-readiness-architecture.md#implementation-and-build-evidence):
  333 parent-discovered tests (26 integration skips), 44 targeted tests,
  15 reported Chromium checks and passing source CI including real SQL Server
  general parity and hardened-image scanning. The disposable local SQL login
  could not be established; new-assistant real-SQL/model acceptance is not
  supplied by the general parity job.
* Updated PRD/ADR/index with the honest boundary: no new ACR image/serving
  revision, paid inference or actual changed-build SQL before/after/restart.
  Specific shared-runtime/spend confirmation was unavailable. Preserve the
  existing deployment/data, historical budget exceptions and separate human,
  calibration and comparative-value gates; no merge or production approval.

## [2026-10-13] validation | Corrected assistant lifecycle and actual SQL coverage

* Fixed the initial Review's shutdown-admission and manual-rendering defects:
  a short dispatch/stop gate prevents delayed claims starting new inference;
  ordinary case controls render before auxiliary reads, with a 10-second abort
  deadline, visible manual fallback and stale-panel protection.
* Recorded corrected runtime `bf383c4`, exact local image `assistants-20261013-02`
  and hardening/source-CI evidence in
  [ADR 0002](../adrs/0002-pilot-readiness-architecture.md#implementation-and-build-evidence).
  The earlier SQL bootstrap failure is historical: actual disposable SQL Server
  now passes 69 tests, including 43 assistant contract/review/durability/API
  tests and concurrent additive startup. Those suites are in the existing CI
  SQL job, not emulation or generic parity alone.
* Updated PRD, operator handover, MVP guide and index in place. Current local
  regression is 379 discovered/310 passed/69 SQL skips; 47 nonbillable assistant
  tests and 19 Chromium checks cover the source candidate. Provider/human
  fixtures are not actual model or human acceptance. Initial Review retained.
* Specific retained-data rollout/up-to-USD-5 incremental QA approval was again
  unavailable. Azure image/revision/data/configuration remain unchanged; no
  ACR publication or paid calls occurred. CON-009/AC-057, actual workload
  permission/restart proof, semantic calibration and human/business acceptance
  remain distinct open gates, not inherited from the corrected source checks.

## [2026-10-13] validation | Corrected candidate final CI receipt

* Source `560c30c` preserves the shipped runtime/UI/dependencies of exact local
  image source `bf383c4`. Final
  [CI 38461679776](https://github.com/jmservera/ama/actions/runs/38461679776)
  passes test/image/mssql: 379 discovered tests with 69 conditional skips,
  all 69 actual SQL tests, and hardened-image scan/SBOM checks.
* This closes source/build validation, not the unapproved live rollout,
  registered actual model invocation or independent changed-Azure SQL restart
  gate. Earlier evidence and the initial Review are preserved.

## [2026-10-13] implementation | Ledger discovery and prepared operational coverage

* Owner authorized image02 rollout and bounded QA; exact `d3e652ce` manifest
  reached revision `--0000010`. Private auth/config/identity comparisons and
  independent managed-identity SQL fingerprints preserved 980 cases, 11 staff,
  three metadata entries, 15 recommendations and audit head/count 40.
  Live ledger-trigger incompatibility prevented model execution; no paid call
  or human acceptance is claimed.
* Source `99aeaac` creates append-only ledger assistant events instead of an
  unsupported system-versioned-table trigger, refusing incompatible retained
  evidence without deletion. Actual disposable SQL passes 72 tests, including
  fresh-ledger five-path/immutability/restart and invalid-table refusal.
  Full discovery passes 387 tests with 72 conditional SQL skips.
* Requested eval-dataset-creator supplied a read-only schema/coverage audit;
  parent implemented/tested the existing generator and SQL seed persistence.
  [Dated recipe](./research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
  preserves seed 20260901, 60000 stock and 980-case slice, with 38 visible booked
  visits (11 current-week), six designated forward visits, one package/601
  source orders, 12 each invoices/unverified quality/pending grants/requests
  and four offered handoffs. No new approval, consent, payment or benefit.
* Owner stopped migration and requested a reset. QA authority removed in
  healthy revision `--0000011`, still image02. Database deletion was cancelled;
  no wipe/reseed occurred. Private enriched seed and 11 tenant staff bindings
  are prepared. Image03 is local-only, not a serving digest. Updated PRD/ADR,
  addendum, operator guide, synthetic dictionary and index; earlier receipts,
  original case, owner memory and regulatory snapshots remain unchanged.

  ## [2026-10-14] query | Capstone narrative refresh and native PowerPoint process map

  * Owner requested the AMA Presentation Communications Strategist and PowerPoint
    Builder. Rebuilt all 22 executive slides with current bounded technical
    evidence, customer-first decisions, source-linked notes and planned timing.
    Five real operator-service paths/SQL-content/restart proof remain distinct
    from open staff/human/accessibility/semantic/value acceptance.
  * [Native slide 13](../capstone/deck/zava-forward-executive-draft.pptx)
    replaces its embedded process-map image with editable textboxes, backgrounds
    and connectors. Peer titles use fixed TOP-anchored regions and common body
    starts across the deck, including two/three-line title contrasts.
  * Updated [capstone handover](../capstone/README.md#native-powerpoint-rebuild-2026-10-14),
    [knowledge-base index](./README.md) and
    [preview](../capstone/deck/agents-in-retrofit-process-native.png).
    Original standalone SVG/PNG remain reference illustrations; dated working
    YAML/style/generated assets and specialist handover are preserved.
  * Fresh full-deck exports, saved shape/notes/source checks and parent image
    inspection support the published copy. Compact-spacing/edge-band warnings
    are explicitly classified, not presented as a clean generic-geometry pass.
    Native PowerPoint/font fidelity, SDK vision, real rehearsal/pitch, full
    rubric floors and product/production approval are not claimed.
  * No new legal claim, private identity, cloud/auth/model action or spending
    authority. Original case, owner memory and regulatory snapshots unchanged.

## [2026-10-14] create | Executive and technical Excalidraw architecture views

* Owner requested both audiences' architecture views from #68, with Azure
  icons. Added [editable scenes and handover](../architecture/README.md),
  vector/high-resolution previews and unmodified official icon selections
  with provenance and permitted-use terms.
* Executive view explains one accountable staff workflow, durable evidence,
  bounded AI and human approval. Technical view maps ingress/auth, the
  single-API five-assistant service, SQL/Blob/model interfaces, own-photo/
  token renewal, registry, networking, diagnostics and alerts, with
  separate deferred worker and conditional M365 relationships.
* Preserved distinctions: static source versus live inventory, development
  public access versus private production design, source-defined telemetry
  versus measured tracing, declared archive policy versus unimplemented
  immutable digest anchoring, and five operator paths versus real-user/
  semantic/value acceptance. Ordinary five-assistant authority and proactive
  scans remain off. No new architecture decision or operational approval.
* Linked the views from ADR 0002, infrastructure and capstone handovers and
  this index. Retained complete-guide coverage and open capstone floors.
  The presentation, original case, owner memory, regulatory snapshots and
  runtime code remain unchanged; no cloud, tenant or model operation.

## [2026-10-14] update | Architecture and UX capstone presentation refresh

* Owner requested the new architecture materials in the presentation and
  the UX Designer/PowerPoint skills and agents to improve it. Published the
  [24-slide capstone deck and handover](../capstone/README.md#architecture-and-ux-refresh-2026-10-14),
  retaining the 18-slide main route and adding two optional appendices.
* Native presentation architecture covers the executive view on slide 10,
  current runtime on 19, operations/identity/network context on 23 and
  deferred/conditional topology on 24. Official Azure service icons remain
  individual assets; diagrams are editable boxes, text and connectors.
  The Excalidraw sources retain their separate baseline and authority.
* UX expert review made alternatives explicit, separated recorded proof
  from outstanding acceptance, clarified the planning-only decision and
  proposed owners/deliverables, and added technical-detail/return links.
  It is artifact review, not human comprehension, resident engagement or
  observed usability evidence.
* The native five-capability map, human decision boundaries and common
  title/body starts remain. The current working handover records fresh
  rendering, notes/geometry/source checks, icon provenance, warning
  dispositions and the full-guide contribution/gap assessment.
* Planned 795-second main route plus 105 seconds questions/contingency is
  not rehearsal. Authority and proactive scans remain off; real-user,
  semantic, value, native-viewer and production acceptance remain separate.
  No new legal, funding or business-outcome claim, cloud/tenant/model
  operation or spending authority. Original case, owner memory, regulatory
  snapshots, runtime and infrastructure code remain unchanged.

## [2026-10-14] query | All-user journeys and bounded agent opportunities

* Owner requested original/addendum review and contributions from all
  nine `company-*` research agents. Published the
  [customer journey atlas](./research/ux/customer-journeys/customer-journey-atlas.md)
  and its linked Assets, Programme, Safety, Finance, Procurement/Suppliers,
  Resident Engagement, Frontline, Data/Performance and Executive Reviewer
  contributions under `research/ux/customer-journeys/`.
* Filed 28 stage-based maps and nomination/source-change subjourneys,
  including motivations, pains, desired gains, channels, handoffs,
  exceptions, practical and imaginative requests, approval boundaries,
  manual fallback, non-AI comparators and 24 opportunity hypotheses.
  Five connected learning bundles count review, correction, resident
  burden and whole-life cost rather than agent actions.
* Executive reconciliation added leasehold-service workflow and corrected
  controller accountability, all-contract participation, owner-reported
  award/hazard touchpoints and later-only portfolio AI. No corporate
  delegation, user observation, target ratification or achieved gain
  follows from a role-agent contribution.
* Preserved research snapshot 7b5807c and reconciled publication against
  main snapshot d931066: current Zava names/source paths, five-assistant
  operator evidence, Decision 1 contracts and draft carry-forward limits.
  Normal assistant authority/proactive scans remain off; deterministic
  supervision and independent resident/safety/professional/Finance
  decisions remain. Publication does not imply human or benefit acceptance.
* Updated this index and the addendum's service-design section. Original
  case, owner memory, regulatory snapshots, runtime and infrastructure
  are unchanged. No cloud/model action, real data publication, new legal
  currentness check, spending or operational approval.

## [2026-10-14] query | Design humidity and temperature sensor data flow

* Reviewed the Business Challenge and Modernised Retrofit Delivery Objective.
  The current sensor inventory, device mapping, calibration and ownership are
  unknown; three humidity/temperature readings per simulated day are an AMA
  demonstration assumption only.
* Added a simulator-only capture and analysis proposal to ADR 0002. It reuses
  the existing API and Azure SQL, retains append-only readings and provenance,
  derives versioned deterministic review signals, and extends the existing
  map/review queue. No IoT Hub/Event Hubs integration, production threshold or
  device integration is selected.
* Sensor signals can create a `SENSOR_REVIEW_DUE` human condition-review task,
  but cannot diagnose a hazard, alter statutory clocks, override a resident
  report, release a hold or directly change investment ranking. Missing or
  invalid data remains insufficient and cannot deprioritise a home.
* Updated `../case_study_48_addendum.md`, `../adrs/0002-pilot-readiness-architecture.md`,
  `../architecture/README.md`, this index and this log. No simulator code,
  cloud resources, live data or operational approval was created.
* Open items remain the actual sensor inventory/protocol, mapping and
  calibration ownership, lawful basis and resident choice, retention, data
  quality rules, analysis window, thresholds and operational triage owner.


## [2026-10-14] assessment | Responsible AI review and proposed release gates

* Read the preserved original case study, current addendum, Zava Forward PRD
  and both proposed ADRs. The older Proper Warm PRD and owner memory remain
  unchanged; the current requirements candidate advances to v0.15.0.
* Delegated an audit of baseline commit `1cb398c7b90bec05a5700008a97d0cfac494144a`
  / PRD v0.14.0. Six framework assessments returned 29 preliminary checks:
  7 PASS, 11 PARTIAL and 11 NOT_ASSESSED. Measure and AI STRIDE verification
  terminated with `INVALID_PAYLOAD` / `Retryable=false` because full finding
  records could not be consumed through temporary-file references. No retry,
  consolidated verified counts, severity breakdown or RAI report is claimed.
* Preserved that limitation and preliminary review priorities in the
  [addendum assessment status](../case_study_48_addendum.md#assessment-attempt-and-evidence-limits),
  with human acceptance PENDING. UK operational scope and conditional EU AI
  Act screening do not establish a legal classification or currentness check.
* Proposed [PRD RAI controls](../prds/zava-forward-retrofit-programme-demonstrator.md#responsible-ai-release-and-oversight-contract-2026-10-14):
  FR-048 to FR-051, AC-062 to AC-066 and NFR-014 cover release/impact records,
  meaningful oversight, challenge/correction, cohort fairness and incident
  suspension/restart. Strengthened semantic truth/unsafe-advice evaluation and
  source-permission parity across every retained model path. All new criteria
  remain Not run; three new RAI approval/evidence questions remain open.
* Amended [ADR 0001](../adrs/0001-azure-architecture.md#responsible-ai-architecture-boundary-2026-10-14)
  and [ADR 0002](../adrs/0002-pilot-readiness-architecture.md#responsible-ai-control-plane-2026-10-14)
  with proposed version-bound release, privacy, incident and review boundaries
  in the future worker estate and current shared API/SQL design respectively.
  Updated this index. No runtime, deployment, model call, regulatory snapshot,
  processor approval or operational authority was changed.
* Local documentation checks verify relative links/anchors, table structure,
  frontmatter presence, 51 FRs/66 ACs/14 NFRs, exact FR-to-AC traceability and
  new reciprocal references. Git patch hygiene and historical-file preservation
  are checked separately; formal RAI verification, PRD approval, hosted CI,
  direct human review and real-data activation remain unproved.


## [2026-10-14] validation | Authorized RAI verifier-handoff recovery

* Preserved the original terminal `INVALID_PAYLOAD` attempt and executed a
  separately owner-authorized bounded recovery using full original findings
  and codebase profile inline for AI STRIDE and NIST Measure. Reused complete
  compatible Govern/Map/Manage verdicts; no finding was reconstructed from a
  count summary, omitted or changed into plan-mode pass-through.
* Generated the [RAI_REPORT_V1 baseline report](../../.copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md)
  for commit `1cb398c7b90bec05a5700008a97d0cfac494144a` / PRD v0.14.0.
  All six frameworks yield 29 checks: 7 PASS, 0 FAIL, 11 PARTIAL and
  11 NOT_ASSESSED. Residual severity: 0 CRITICAL, 0 HIGH, 8 MEDIUM, 3 LOW.
  Verification: 2 CONFIRMED, 0 DISPROVED, 9 DOWNGRADED, 18 UNCHANGED.
* Deterministically checked full input fields and inline payloads, every
  original/response/collection ID, all 11 verification records and total
  verdict mappings, unchanged-record fidelity, all 29 principal report rows,
  summary/severity/verification counts, exact path/hash/caution, failed-attempt
  history and PENDING human acceptance. Session-only structured handoff is
  validation evidence, not an additional public report or professional sign-off.
* Updated the addendum, PRD, both ADRs and index with verified review
  dispositions and baseline limitations. v0.15.0 safeguards remain proposed/
  Not run, not verified fixes. Explicitly flagged actual staff/tenant identity
  privacy scope despite synthetic resident content, and distinguished restart
  persistence from witnessed backup recovery/erasure reconciliation.
* No application, installed plugin, cloud resource, model call, real-data scope,
  legal rule, deployment or operational approval changed. Human acceptance
  remains PENDING and live use BLOCKED; legal currentness, representative
  fairness/oversight, held-out model quality and net benefit remain unassessed.
## [2026-10-14] update | BRD v0.17.0, PRD v0.15.0 and ADR 0003 from the journey atlas

* Reviewed the customer journey atlas, the updated addendum and the Zava
  documentation. Amended the BRD to v0.17.0 (FR-045 to FR-047, AC-087 to
  AC-089, OD-41 and OD-42; refined AC-011, AC-023 and AC-065) after an
  independent review whose traceability, ordering and consistency findings
  were applied. The BRD business-goal SMART gate remains blocked on open
  decisions.
* Handed the BRD to the PRD (v0.15.0): FR-048/049, AC-062 to AC-065,
  FR-045 extended, a BRD-to-PRD ID table and journey learning-test bundles.
  An independent critique found stale BRD versions, a cross-document ID
  collision and under-specified acceptance criteria; all were applied except
  the deferred BRD FR-037 challenge requirement and OD-41/OD-42.
* Added [ADR 0003](../adrs/0003-journey-derived-capabilities-runtime-fit.md)
  (Proposed) and indexed it here. The addendum's "BRD unchanged" statement
  refers to the operator evidence; the later atlas drove this change. The
  atlas stays desk research, not validation. No owner acceptance, runtime
  change, real data or approval follows.

## [2026-10-14] update | BRD sensor and in-use monitoring capture

* Added BRD FR-048/AC-090 (retained in-use monitoring observations kept
  separate from derived analysis and human decisions) and OD-43 (actual
  inventory, mapping, calibration, lawful basis, retention, thresholds and
  owner), linked to RULE-014 and the ADR 0002 simulator-only sensor design.
  The BRD stays solution-agnostic and names no IoT platform. A PRD
  requirement is still needed before build. No data, device, threshold or
  approval is created.
* Resolved merge conflicts with main in this index and log, keeping both
  the sensor-flow and journey entries.

## [2026-10-14] update | IoT Hub decision, PRD sensor requirement and analytics research plan

* Owner direction: Azure IoT Hub is the product for IoT. ADR 0003 decision 6
  adopts it as the device-to-cloud ingestion boundary, with an API consumer
  that validates and appends to Azure SQL; ADR 0002's earlier "no IoT Hub for
  the demo" advice carries a dated amendment. Tier, cost, provisioning,
  network exposure and Entra roles remain open.
* PRD v0.15.0 adds FR-050 and AC-066 to AC-068 (counts 50 FR, 68 AC) and
  traces BRD FR-048/AC-090/OD-43.
* Added the [analytics research plan](./research/iot-sensor-analytics-research-plan.md)
  with phases R1 to R5 for dew point and trend analysis. Its leads come from an
  uncited web synthesis and are unverified; no method, threshold or standard
  claim is validated, and the PAS 2035 monitoring claim is flagged unverified.
* No IoT Hub provisioned, no cloud action, real data or approval.

## [2026-10-14] review | Source verification of IoT analytics leads

* Checked the unverified leads in the
  [analytics research plan](./research/iot-sensor-analytics-research-plan.md)
  against public sources and recorded status, source and caveat for each.
* Magnus dew point constants, the BS 5250:2011 80 percent surface humidity and
  fRsi 0.75 figures, persistence rules, the Housing Ombudsman no-blame
  principle and Azure IoT Hub tier features were confirmed, in places only
  through secondary or mirrored sources. The official BSI, BRE and AMS texts
  were not read, so R1 stays open.
* Corrected two claims: PAS 2035 requires risk-based monitoring and
  evaluation, not a blanket sensor mandate, and IoT Hub devices use X.509 or
  symmetric keys, not Entra ID. ADR 0003 decision 6 was amended accordingly.
* No threshold, standard or legal duty is validated by this check.

## [2026-10-14] review | arXiv search for IoT analytics sources

* Searched arXiv for dew point, mould, condensation, fRsi, retrofit
  monitoring and Magnus formula sources. No building-physics paper was found,
  so no lead was validated by arXiv. Four generic sensor calibration, drift,
  sampling and anomaly-detection papers (abstracts only) were recorded as
  method leads in the research plan. R1 stays open; official standards and
  building-science journals are the next sources.

## [2026-10-14] review | Owner-supplied BS 5250:2021 public documents

* Read the BMI Group BS 5250:2021 roofing guide (August 2021). It supports the
  dew point definition of condensation and names BS EN ISO 13788, but states no
  80 percent, 70 percent or fRsi figure. It shows a 2021 edition exists, so
  the 2011-based thresholds must be re-confirmed against the 2021 edition.
* The Scribd copy could not be read (access challenge) and its provenance and
  right to use are unconfirmed, so it is not used. R1 stays open.

## [2026-10-15] update | Reconcile journey/sensor and Responsible AI requirements

* Merged main's BRD v0.17.0, journey learning tests, ADR 0003 and IoT research
  into the RAI topic. Preserved both index/log contributions and the original
  audit report, case study and owner memory.
* Reconciled the two draft v0.15.0 ID allocations in PRD v0.16.0: main keeps
  FR-048 to FR-050 / AC-062 to AC-068; unmerged RAI additions move to FR-051
  to FR-054 / AC-069 to AC-073. Updated current addendum/ADR references and
  recorded the explicit draft-to-current mapping in the PRD.
* Restored the incoming PRD's omitted NFR and existing acceptance sections;
  separated its combined offer requirement/criterion and supplied FR-049
  from BRD FR-047/AC-089. Counts are 54 FRs, 73 ACs, 14 NFRs, nine constraints.
  Fresh requirements review, human approval and implementation remain open.

## [2026-10-15] approval | Owner acceptance of the bounded RAI baseline report

* Recorded the owner's explicit instruction to accept the recovered RAI report.
  Acceptance covers its bounded findings, limitations and remediation-planning
  basis, not legal/privacy sign-off, remediation closure, PRD acceptance or live use.
* Added dated acceptance metadata and the pre-annotation report commit/hash;
  retained all 29 findings and counts, the eleven PARTIAL and eleven NOT_ASSESSED
  checks, the unchecked qualified-review gates and live-use BLOCKED disposition.
* Updated current addendum, PRD, ADR and index references. Historical generation
  and log entries remain unchanged. Merge fixes are local; no push was performed.

## [2026-10-15] plan | Responsible AI remediation and independent critique

* Added the [RAI remediation plan](../../.copilot-tracking/plans/2026-10-15/rai-remediation-plan.md)
  with six phases/thirteen tasks, mapping all eleven verified residuals and eleven
  unassessed checks to engineering and separately authorized evidence/approval work.
* The independent [standard critique](../../.copilot-tracking/reviews/plans/2026-10-15/rai-remediation-plan-critique.md)
  completed with Pass and no actionable findings. Canonical helper projection and
  hash bind the assessed content; unchanged candidate identity is checked at delivery.
* Offline engineering is planning-ready; actual staff-data, serving-model attestation,
  lawful cohorts/thresholds, participant/budget, restore/erasure and qualified release
  gates remain. No application code, tests, paid inference or deployment was run.
* Owner then authorized merging PR #72 into main after completion/checks and a
  subsequent read-only Functional Planner review of GitHub issue coverage. Issue
  creation is a separate reviewed execution pass.

## [2026-10-15] update | Per-user agent chat and memory proposal (BRD v0.18.0, PRD v0.17.0, ADR 0004)

* Added a proposal, not an adopted requirement set, for per-user agent chat and
  memory (GitHub backlog epic #157, children #158 to #164). It appeared in no
  earlier BRD, PRD or ADR, and the owner has not decided to adopt it.
* BRD v0.18.0 adds BG-013, FR-049, FR-050, RULE-025, RULE-026, NFR-010, NFR-011,
  AC-091 to AC-098 and OD-44 to OD-49. PRD v0.17.0 adds FR-055 to FR-059,
  NFR-015, NFR-016, AC-091 to AC-103, OQ-020 to OQ-025 and a journey, agent and
  UI mapping. ADR 0004 is Proposed.
* Evidence: the backlog issues, the customer journey atlas (desk research),
  ADR 0001 to ADR 0003 and the current assistant code. Microsoft Learn
  documentation on Foundry Agent Service memory (a preview, retrieved
  2026-10-14) was compared and not chosen.
* Merged with main after the RAI controls took FR-051 to FR-054, NFR-014,
  AC-069 to AC-073 and OQ-017 to OQ-019; the proposal PRD IDs were renumbered
  to avoid collisions. Main had already restored the PRD NFR, Constraints and
  Acceptance Criteria sections that PR #71 dropped, so the earlier flagged
  defect no longer applies to main.

## [2026-10-15] update | Regulatory literacy synthesis and ADR 0005 regulatory compliance assistant

* Added the regulatory literacy synthesis and ADR 0005 (numbered after main took
  ADR 0004 for per-user chat). Added BRD FR-051, AC-099 and OD-50, PRD FR-060,
  AC-104 to AC-106 and OQ-026, and an addendum section. Proposal only; no owner
  approval, legal interpretation or fresh quality review.

## [2026-10-15] review | Post-merge RAI issue coverage

* PR #72 merged into main as `7a8b1fe65475752fcf242ed52acab8e7e43b58d3`
  after prototype validation and the rubric gate passed at 47/100 against 47/100.
* The Functional Planner reviewed 144 hydrated GitHub issue bodies and read-only
  field/hierarchy evidence against the merged PRD and remediation plan. Its
  [coverage analysis](../../.copilot-tracking/github-issues/prds/rai-remediation/artifact-analysis.md)
  maps all thirteen tasks, eleven residuals and eleven unassessed checks.
* Twelve existing open issues provide suitable homes, but each is Similar rather
  than a complete Match: their acceptance criteria need the RAI delta. The
  [issue plan](../../.copilot-tracking/github-issues/prds/rai-remediation/issues-plan.md)
  proposes twelve body-only updates, zero creates and zero links, preserving
  current state, types, labels, milestones and assignees.
* The [handoff](../../.copilot-tracking/github-issues/prds/rai-remediation/handoff.md)
  requires human review and a separate authorized execution pass. No issue was
  created, edited, commented on, linked or transitioned. Existing native hierarchy
  pairs and qualified authority remain needs_review where not proven.
* Focused artifact validation confirms four planning artifacts, 23 relative links,
  exact task/check coverage and unchecked human gates. No remediation implementation,
  model calls, recovery drills or live-use approval is implied.

## [2026-10-15] review | Owner RAI issue decisions and chat coverage

* The owner approved the eight review decisions in conversation and requested
  adding existing chat evaluation issue 164. The [updated issue plan](../../.copilot-tracking/github-issues/prds/rai-remediation/issues-plan.md)
  now proposes thirteen body-only updates, zero creates and zero links.
* Chat-specific held-out, memory/injection, permission-change, human review and
  finite-authority criteria reuse shared evaluation methods without authorizing
  chat implementation or enablement. Original thirteen-task/22-check coverage
  remains unchanged; this is an owner extension, not a new baseline finding.
* Dated decisions are recorded in the [handoff](../../.copilot-tracking/github-issues/prds/rai-remediation/handoff.md).
  Human-review checkboxes remain untouched and require the owner's saved edits
  before execution. No GitHub issues have been changed by this review update.

## [2026-10-15] execute | Approved RAI issue updates applied

* After explicit one-by-one owner approval and eight owner-completed saved human
  review boxes, applied thirteen body-only updates in jmservera/ama: 105, 121,
  116, 106, 107, 146, 122, 130, 128, 108, 145, 126 and 164.
* The [live operation log](../../.copilot-tracking/github-issues/prds/rai-remediation/handoff-logs.md)
  records each successful mutation and saved-body SHA-256 before the next update.
  All bodies were re-read immediately before update and after saving; titles,
  state, type, labels, milestone, assignees and relationship metadata were verified
  unchanged. No issues were created, linked, closed or commented on; no failures.
* Preserved existing criteria and history, applied the three approved factual
  corrections and left new acceptance criteria unchecked. Issue 164 adds future
  chat assurance, not chat implementation or enablement authority.
* This executes the approved backlog update only. The thirteen remediation tasks,
  22 outstanding checks and qualified legal/privacy, human, model, recovery and
  operational evidence gates remain work to be completed and accepted.

## [2026-10-15] merge | RAI execution record and chat proposal reconciled

* Resolved PR #205 against main's chat/memory proposal from PR #204, retaining
  current BRD v0.18.0, PRD v0.17.0 and ADR 0004 index entries alongside the
  completed RAI issue-update record. All prior log entries from both branches
  remain intact.
* The RAI review and executed payloads retain their dated PRD v0.16.0/source
  baseline; merging the newer proposal does not retroactively change accepted
  payloads, enable chat or satisfy qualified operational evidence gates.
* No application behavior or GitHub issue body was changed by this conflict
  resolution. The thirteen previously verified issue updates remain completed.

## [2026-10-15] merge | Concurrent regulatory proposal retained

* While PR #205 checks ran, PR #207 added the regulatory-literacy synthesis and
  proposed regulatory assistant. Retained its addendum, BRD, PRD, ADR 0005 and
  index changes without modifying their scope or approval status.
* Preserved both append-only log additions. Kept main's generated 47/100 rubric
  record as the current merged baseline rather than hand-combining generated
  provenance or inventing a score. The RAI branch's successful hosted score
  remains available in its original workflow run.
* The thirteen issue updates and their original review/source binding remain
  unchanged; the newer assistant proposal is not silently added to that completed
  execution or activated by this merge.

## [2026-10-15] add | Backlog delivery coordinator agent

* Added `.github/agents/ama-backlog-delivery-coordinator.agent.md`. It reviews
  issues with the backlog manager, builds dependency waves, runs one RPI loop per
  issue in its own worktree and branch, reviews each PR, and merges and rebases
  in dependency order under owner approval.
* Updated the `ama-*` agent row in the index. No research or regulatory content
  changed.

## [2026-10-15] update | Coordinator agent loop and gated automerge

* Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md`: the
  qualified `hve-core-all:rpi-agent` name, a loop that continues until every
  issue is merged or blocked, an owner delegation for gated squash merge and
  run-owned rebases, and a human-blocker ledger that stops only dependent work.
* Repository auto-merge is disabled and branch protection is unavailable on
  this plan, so the agent merges after verifying checks itself. No repository
  settings were changed.

## [2026-10-15] add | Document and form fixtures

* Added a section on the 120-family document, form-schema and seeded-defect fixtures
  to the retrofit synthetic data README, with open items for the real funding schema
  (OQ-015) and human adjudication of gold labels. No index entry changes needed.

## [2026-10-15] update | Evaluation dataset registry and scale fixture (#174)

* Added `mvp/evals/registry.json` (version, owner, purpose per dataset) and the
  seeded `mvp/zavaforward_mvp/scale_fixture.py` for a fictional 60,000-home /
  600,000-event fixture, output Git-ignored. Documented in `mvp/README.md`.
* Open: named dataset owners; migrating in-test 60,000-case builders. No
  research or regulatory content changed.

## [2026-10-15] update | Synthetic data provenance register

* Added `research/retrofit-synthetic-data/provenance-register.json` covering
  every dataset (public pack, private stock register, MVP seed, AI scenarios,
  assistant runtime tables, sensor gap), external source licence, retrieval
  date and attribution, and public/private visibility.
* Extended `data-dictionary.md` with dataset coverage, the private stock
  register, chat and assistant data, sensor data and the real-person guarantee.
* Added `mvp/tests/test_synthetic_provenance.py` (PII patterns, unlabelled
  records, public/private separation). Open items: retrieval dates and licence
  wording for Census 2021, IMD 2025 and ONS boundaries; sensor data scope.

## [2026-10-15] update | Synthetic data determinism, manifests and refresh policy

* Added a determinism, manifest and proposed refresh-policy section to the
  retrofit synthetic data README, and linked it from the index (issue #176).
* Recorded owner decisions still open: policy approval, the missing stock
  register generator and the absent sensor generator.

## [2026-10-15] update | Synthetic data needs inventory and phase gate

* Added `research/retrofit-synthetic-data/needs-inventory.json` and a gate
  section in the retrofit synthetic data README (issue #166, parent #165).
  Checked by `mvp/tests/test_needs_inventory.py`.
* Open: owner approval, volumes for sensor, chat and survey needs, link from
  the scenario manifest (#103), reconciliation with the 2026-10-14 handoff.

## [2026-10-15] update | Design system foundations

* Added `research/ux/design-system.md` and linked it from the index (issue
  #150): tokens now defined in `mvp/web/style.css`, component and state
  inventory, blocked-step and AI suggestion patterns, extend-versus-adopt
  decision.
* Open items: owner confirmation of the extend decision, Zava brand colours,
  non-colour map marker shapes and contrast verification.

## [2026-10-15] update | Content standard and copy audit

* Added `research/ux/content-standard.md` and linked it from the index (issue
  #153): content standard, glossary, blocked-message pattern, AI suggestion
  wording and the core-flow copy audit. UI copy and server labels changed to
  "AI suggestion, not approved"; checked by
  `mvp/tests/test_content_standard.py`.
* Open items: named human reviewer for resident-facing wording, stored
  finance value "Keep on hold", reading-age targets and user testing.

## [2026-10-15] update | Generator gap closure mapping

* Extended `research/retrofit-synthetic-data/needs-inventory.json` to version
  1.1.0 (issue #167): every need maps to a child story or delivered issue, and
  generator conventions (seed, identifiers, `is_synthetic`) are recorded. New
  README section and tests in `mvp/tests/test_needs_inventory.py`.
* Open items: owner confirmation of the mapping and of the SN-01 regeneration
  scope; no deferrals recorded.

## [2026-10-15] update | WCAG 2.2 conformance baseline

* Added `research/ux/wcag-conformance-baseline.md` and linked it from the index
  (issue #151): proposed WCAG 2.2 AA target and scope, first audit, computed
  contrast, manual check record and accessibility statement draft. Design
  system focus token row updated (`--focus-ink`). Fixes in `mvp/web`: two-tone
  focus indicator, field border contrast, chart table equivalent.
* Open items: owner confirmation of target, rendered-page scanner for CI,
  manual screen-reader, keyboard, zoom and target-size results per role,
  contact route for the statement, re-retrieval of WCAG 2.2.

## [2026-10-15] decision | Synthetic regulatory demo assumptions permitted

* Owner permits synthetic development without waiting for real Legal,
  Compliance or DPO delegates and missing company source documents. Recorded
  the scope in [ADR 0005](../adrs/0005-regulatory-compliance-assistant.md#owner-decision-synthetic-demo-development-2026-10-15).
* Fictional role accounts, simulated review/approval records and original demo
  contract/grant fixtures must be labelled synthetic-demo and remain distinct
  from official evidence. The decision does not authorize fabricating law,
  licensed standards, official dates, company facts or real human sign-off.
* Real-source applicability, personal delegation, actual data processing,
  paid/provider calls and operational acceptance retain their existing gates.
  No application implementation or operational approval is recorded here.

## [2026-10-15] update | Stock-to-case link and fabric attributes

* Added a synthetic stock-link report (980 of 980 cases linked, 825 distinct
  homes) and seeded fabric attributes for the 60,000-home register to the
  [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md#stock-to-case-link-and-fabric-attributes-2026-10-15).
  Distributions are stated as assumptions, not company facts (#168).

## [2026-10-15] implementation | Versioned law store seeded from local snapshots

* Added the Phase 1 law store of [ADR 0005](../adrs/0005-regulatory-compliance-assistant.md)
  in `mvp/` (issue #210): source, version, provision and gap records, immutable
  content-hashed snapshots, a rebuildable keyword index and a read-only viewer.
  Source metadata is in `mvp/law/law-source-register.json`; see the
  [Regulatory Source Register](./regulatory/README.md).
* Snapshots were not edited. Effective dates are recorded only where the local
  snapshots state them; review dates and owners are unknown and left empty or
  "to be named". Official-source change checks have not been performed.
* Open: named Legal, Compliance and DPO owners (#209), licensed PAS 2035 and
  official sources for leasehold, complaints handling and TrustMark.

## [2026-10-15] update | Coordinator updates project board status

* Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` so the
  coordinator sets the Status field on the owner's project 7 when an issue
  starts, opens a PR, blocks, closes or reopens. Ids are discovered at run
  time and the `project` token scope is a precondition. No index change.

## [2026-10-15] update | Household and tenancy fields at stock scale

* Extended `mvp/zavaforward_mvp/scale_fixture.py` (version 1.1.0) with a
  `households.jsonl` of 60,000 synthetic households (tenancy, channel,
  adjustment, representative and works-consent states) and documented the
  fields in the [data dictionary](./research/retrofit-synthetic-data/data-dictionary.md#stock-scale-household-and-tenancy-fixture-2026-10-15).
* Distributions are invented; consent and representative rules are demonstrator
  rules, not legal advice. No index change.

## [2026-10-15] update | Synthetic stock EPC, survey and conflict fixtures

* Extended `research/retrofit-synthetic-data/README.md` and its index entry for
  issue #170: EPC and survey records for the 60,000-home stock derived from the
  fabric attributes, plus a committed manifest of seeded EPC conflicts.
* Labelled synthetic fixtures under ADR 0005 (2026-10-15); not lodged EPCs.
* Open: conflict mix and rates are unconfirmed generator assumptions.

## [2026-10-15] update | Coordinator requires RPI loop evidence

* Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md`: briefs
  must require the full research, plan, implement and review loop, the
  `.copilot-tracking/` artifacts are committed and pushed in each PR, and the
  coordinator verifies them before review. Prompted by wave 1 to 5 sessions
  that implemented directly and pushed no RPI artifacts. No index change.

## [2026-10-15] update | RPI loop made a merge-gate condition

* Updated the coordinator agent so the RPI loop is mandatory for every issue
  and the merge gate checks for research, plan, changes and review artifacts
  in the PR. No index change.

## [2026-10-15] update | Coordinator runs RPI loops in tmux sessions

* Updated the coordinator agent so each issue's RPI loop runs in its own named
  tmux session with the agent and brief passed as Copilot CLI parameters, and
  is the only allowed execution route. No index change.

## [2026-10-15] update | Contractor, finance, grant, safety and consent lifecycle coverage

* Added a lifecycle coverage section to `research/retrofit-synthetic-data/README.md`
  for issue #173: seeded states plus a recorded deferral for every state that
  would be an invented approval, acceptance, payment, award or consent outcome.
* Generator receipt gains a `lifecycle` block; two more cases carry a Raised
  commitment and a Valuation. Labelled synthetic fixtures under ADR 0005.
* Open: owner decision on demo-only outcome fixtures. No index change.

## 2026-10-15 Law store Azure SQL and Blob backends (#210)

* Noted in `mvp/README.md` (law store section) the Azure SQL ledger backend and
  Azure Blob snapshot interface; SQLite and local files are test doubles only.
* No regulatory snapshot changed. Open: Blob immutability policy and Azure SQL
  deployment are unverified infrastructure items.

## 2026-10-15 AI evaluation harness evidence gate (#108)

* Noted in `mvp/README.md` the harness `evidence` block: golden hash, scripted
  provider, not-evaluated and calibration-not-applicable statements, no benefit
  claim, and open items. No regulatory snapshot changed.
* Open: Foundry model, version and quota confirmation in the chosen region,
  authorised live calls, held-out split and thresholds, human participant
  protocol and Finance validation need owner decisions or retrieval. No index change.

## [2026-10-15] update | Stock fabric and EPC generator determinism (#176)

* `retrofit-synthetic-data/README.md`: fabric and EPC generators now record
  `generator_revision` in their summaries and have a byte-identical test.
* Open for the owner: the stock register generator is not in the repository,
  and the sensor generator does not exist (depends on #177 to #183), so those
  two criteria remain unmet; refresh-policy approval is still pending.

## [2026-10-15] update | Coordinator uses /every to monitor tmux sessions

* Changed `.github/agents/ama-backlog-delivery-coordinator.agent.md` so the coordinator registers a recurring `/every` check for its tmux RPI sessions instead of a long blocking loop, and stops the schedule when all issues are merged or blocked.

## 2026-10-15 Frozen protocol, benefits register and release gates (#126)

* Added a governance section to `mvp/README.md`: versioned frozen protocol,
  BG-011 definitions and MDE register (no pass or fail when the MDE exceeds a
  target), per-phase and tranche release decisions, and breach pauses with
  authorised restart. Index row for the MVP updated.
* Synthetic demonstration values only. Open: OD-18 definitions and MDE, OD-36
  DPIA and lawful basis, OD-35 authority, real approvers, and the RAI closure
  registers and fresh assessment, which need qualified owners and evidence.

## 2026-10-15 Governance gates wired into case workflows (#126)

* `mvp/README.md` governance section updated: capture and pause guard on case
  event paths, breach role check, Shadow and Live release need Phase 0 released.
* No regulatory snapshot changed. Open: pilot cohort enrolment and work package
  and workstream pause scopes.

## 2026-10-15 Immutable Blob ledger digests (#115)

* `mvp/README.md` section added and ADR 0002 implementation status row for the
  ledger updated: Blob digest publisher, scheduled verifier and alert built,
  not deployed or locked.
* Follow-up: missing-success alert added, `--publish` trust-on-first-use gap and
  owner-chosen retention before locking documented.
* No regulatory snapshot changed. Open: legal retention period, policy lock,
  deployed run and unconfirmed Log Analytics table names.

## 2026-10-15 Staff time capture gated on DPIA, notice and audited enabling (#120)

* `mvp/README.md` and ADR 0002 status row updated: capture also needs a notice
  approval reference and an audited manager enabling action; `#/time` screens
  added. No regulatory snapshot changed.
* Follow-up (#120, PR 267 review): the enabling record, entries and notice
  acknowledgements moved from a local SQLite file into the shared SQL store
  (portable DDL, tested on SQL Server); enabling now needs a request by one
  manager role and enabling by a different role. No regulatory snapshot changed.
* Open (owner decisions, not invented): the real OD-36 DPIA, consultation and
  notice approval references, the minimum group size and the notice wording.

## 2026-10-15 Key Vault secret lifecycle (#142)

* `infra/README.md` gains a Key Vault secret lifecycle section: inventory,
  expiry and denied-access alerts on Log Analytics, zero-downtime Entra client
  secret rotation order and quarterly access review.
* No regulatory snapshot changed. Open: named secret owners, a live rotation
  exercise, deployed alert verification and review scheduling.

## 2026-10-15 Document scanning, retention and legal hold (#117)

* mvp/README.md, ADR 0002 implementation status and open items, and the retrofit synthetic data README updated. New synthetic control fixtures for 120 homes from the 60,000-home stock register.
* No regulatory snapshot changed. Open: real malware scanner and Defender enablement, DPO and Legal retention periods (PR-003), the real legal-hold delegate, and retention job scheduling.

## 2026-10-15 Export completeness and ledger head check (#122)

* `mvp/README.md` continuity section documents that the evidence export flags
  truncation and incompleteness, records the ledger head for tail-truncation
  detection, and that assistant proposals are unsupported on the JSON store.
* No regulatory snapshot changed. Open: externally held head in an immutable
  Azure container and Azure SQL drill evidence.

## 2026-10-15 Role endpoint inventory and free-text note handling (#116)

* `mvp/README.md` role projection section updated: free-text notes are held
  (not pattern-redacted) for roles without a recorded need, with a route
  inventory test across every role.
* No regulatory snapshot changed. Open: DPO and Legal confirmation of the roles
  allowed to see a vulnerability reason (OD-14, OD-19), Entra B2B guest
  contractor identity model, and browser acceptance for every role.
## 2026-10-15 Azure Policy, Defender plans, locks and tagging as code (#147)

* infra/README.md gains a Governance controls section; ADR 0001 open item updated. New `infra/governance.bicep`, `main.pilot.example.bicepparam`, `policy-exceptions.json` and tests.
* Review fixes: pilot parameter file renamed `main.pilot.example.bicepparam` and labelled non-deployable (test rejects a deployable `main.pilot.example.bicepparam`); EX-001 expiry set to 2026-12-31; docs state policy is audit-only and Defender stays Free until a cost is accepted.
* No regulatory snapshot changed. Open: Defender cost estimate and enablement, audit versus Deny stance.

## 2026-10-15 Deterministic sensor backfill generator (#183)

* `mvp/README.md` documents the sensor backfill generator, its volume and size estimate (about 1.05 billion hourly rows, about 118 GiB CSV for 60,000 homes over two years), manifest and idempotent load.
* No regulatory snapshot changed. Open: Met Office and Environment Agency data retrieval, reconciliation with #110 validation, and a full-stock storage and cost decision.
## 2026-10-15 IoT Hub Bicep module (#140)

* `infra/README.md` records the proposed IoT Hub tier, region, retention, identity, network and credential-owner decisions; ADR 0003 open items point to them. No regulatory snapshot changed.
* Open: owner approval of ADR 0003, verified pricing, live what-if, BRD OD-43.

## 2026-10-15 ADR 0004 accepted (#158)

* ADR 0004 status set to Accepted as written by the owner (OD-44); BRD and PRD status text and the index updated. Authority limits, FR-036 registry change, Azure SQL storage and Azure-only uksouth deployment recorded.
* No regulatory snapshot changed. Open: OD-45 to OD-49 (lawful basis, DPIA, retention, access, thresholds) carried forward; no live personal data until recorded.

## 2026-10-15 ADR 0004 review fixes (#158)

* Removed an unsourced deployment sentence, restored the original fallback and A-or-B wording, and updated stale proposal wording in the ADR, BRD and PRD. OD-45 to OD-49 stay open. No regulatory snapshot changed.
## 2026-10-15 Identity and RBAC as code (#141)

* `infra/role-assignments.json`, `infra/entra/app-registration.json`, `infra/tests/test_identity_rbac.py` and an `infra/README.md` section added; index row added. No regulatory snapshot changed.
* Open: owner sign-off of the review, contractor B2B decision (#116), live role-assignment comparison, chat store roles when ADR 0004 resources exist.

## 2026-10-15 Identity and RBAC review fixes (#141)

* Matrix test now compares parsed (identity, role, scope) tuples; Entra owner wording corrected; criterion 4 stated as manual steps plus owner. Open: db_ddladmin drop, contractor B2B decision (#116).

## 2026-10-15 Chat and memory test fixtures (#172)

* `mvp/zavaforward_mvp/chat_fixture.py` and `mvp/tests/test_chat_fixture.py` added; provenance register entry `DS-CHAT-MEMORY-FIXTURE`, data dictionary section, eval registry entry and `mvp/README.md` updated. No regulatory snapshot changed.
* Open: approved retention policy and legal retention lock (OD-45/OD-46), persona-to-app-role mapping confirmation by the owner, dataset owner, and runtime enforcement evidence from #160 to #164.

## 2026-10-15 Chat and memory DPIA record (#163)

* Added `research/chat-memory-dpia.md` (data map, decision record, rights, logging, provider position, redaction) and `mvp/zavaforward_mvp/chat_privacy.py` with tests. Index row added.
* No regulatory snapshot changed. Open: DPO and Legal lawful basis, notice, DPIA decision and retention (OD-45, OD-46); Azure OpenAI terms retrieval.

## 2026-10-15 Chat and memory DPIA record rework (#163, PR #281)

* `chat_privacy.py` now runs locate, export and erase through the #160 chat repository and its `owner` column; only `chat_memory` is added, with DDL in the store dialect hooks. The separate `chat.sqlite` and bare `sqlite3` use were removed; portability tests added.
* Wording corrected: provider data handling is not recorded and the free-text warning is not wired into any UI. Lawful basis, notice and DPIA decision remain unrecorded for the DPO.

## 2026-10-15 Per-user memory lifecycle (#161)

* `chat_privacy.py` gains opt-in, item class and source, edit, delete, clear, global and per-task switches and a non-evidence prompt view; `chat_memory` gains `item_class`, `source`, `updated_at` and `chat_memory_control` is added in the same dialect hooks. `research/chat-memory-dpia.md` updated; no new knowledge base page, so the index is unchanged. No regulatory snapshot changed.
* Open: DPO retention per class, memory administrator app role (placeholder in code), UI and endpoint wiring.

## 2026-10-15 Memory lifecycle review fixes (#161, PR 285)

* `chat_privacy.py`: `add_memory` requires a known task (fails closed); expired items are hidden by `list_memory`, `edit_memory` and the prompt view; the administrator role is read from the staff register record; memory ids sort by creation time (fixes a CI ordering flake).
* `chatthreads.py`, `sqlstore.py`, `mssqlstore.py`: idempotent ALTER adds `item_class`, `source`, `updated_at` to an existing `chat_memory` table.
* Open: administrator Entra app role (owner decision), DPO retention, scoping and wiring to users.

## 2026-10-15 Chat and memory isolation (#162)

* Added `mvp/zavaforward_mvp/chat_isolation.py`, chat and memory endpoints, `mvp/tests/test_chat_isolation.py` and a `mvp/README.md` section. No knowledge base page or regulatory snapshot changed, so the index is unchanged.
* Open: break-glass and administrator content-access policy (BRD OD-46, owner), contractor use of chat, live-model injection evaluation (OD-49).

## [2026-10-15] restructure | ADR 0006 source layout and cut-over policy (#196)

* Added `docs/adrs/0006-src-layout-and-cutover.md` (Proposed, owner approval pending) and indexed it in `docs/reference/README.md`. It records the owner decisions of 2026-10-14 and 2026-10-15 (standard `src` layout, `zava_forward` namespace, one isolated package per ADR 0001 workload plus a shared core), the module mapping, move-not-copy and new-feature rules, phases, cut-over gate, rubric counting and `mvp/data/` relocation.
* No code moved and no regulatory snapshot changed. Open: owner approval, soak period, whether the temporary `api` to `agents` import is acceptable until #144.

## [2026-10-15] restructure | ADR 0006 accepted (#196)

* ADR 0006 status set to Accepted by the owner. Recorded answers: no soak period before deleting `mvp/`; the `agents` image carries no `core[sql]` or blob code and the temporary `api` to `agents` import is accepted until #144; old workflow and check names stay until after cut-over; a GitHub release accompanies the archive tag. Index row updated.

## [2026-10-15] restructure | Rubric registry excludes for src (#198)

* Added `src/**/web/vendor/**`, `src/**/data/**`, `**/*.egg-info/**` and `**/build/**` to the `solution-code` excludes in `.github/rubric/artifacts.json`, fixture tests in `test_prepare.py` and a note in `.github/rubric/README.md`. `mvp/` globs kept until the cut-over registry PR (#201, #202); `rubric_version` not bumped.
* Baseline 47 of 100; file sets before and after are identical on the current tree. The change takes effect only after merge. Open: 19 pre-existing test failures, post-merge workflow score.

## 2026-10-15 MVP to src parity matrix (#197)

* Added `docs/architecture/mvp-to-src-parity-matrix.md` (outcome for all 125 tracked `mvp/` and `prototype/` files, review of PRs 235 to 287, issues to reopen, migration order for #199) and two index rows. Baseline recorded: 703 tests, 92 skipped.
* Based on the owner layout decisions of 2026-10-15; ADR 0006 is in draft on another branch, so targets are a working assumption. Open: confirm the `devtools` package, job placement, the handling of PR 287 and each retire row.

## 2026-10-15 MVP to src parity matrix aligned to ADR 0006 (#197)

* Updated `docs/architecture/mvp-to-src-parity-matrix.md` after ADR 0006 was accepted and PR 287 merged: targets follow the ADR module mapping (no `devtools` package), deviations are stated as proposed amendments A1 to A5, three PR 287 files added, the 450 `mvp/.assistant-test-*` sandbox files mapped as retire, the hold action removed, and the owner answers of 2026-10-15 recorded (check names renamed after cut-over, GitHub release with the archive tag, agents image without the `sql` extra, no soak period). Baseline re-recorded: 719 tests, 92 skipped. The index row is updated.
* Open: owner decision on A1 to A5 (core importing `ai_registry` and `assistants`, `assistant_release` placement, agents and orchestrator test dependencies).

## [2026-10-15] restructure | src project skeletons (#290)

* Added `src/{core,api,agents,orchestrator,importer}` (ADR 0006 phase 1): per-project `pyproject.toml`, version module, `python -m` entry point, tests with a dependency-rule import test, `requirements.in` and hashed `requirements.txt`, Dockerfiles for the four workloads, `src/.dockerignore`, `/src/**/data/` in `.gitignore`, `src/README.md` and the new workflow `.github/workflows/src-ci.yml` (checks `src-<project>`, `src-namespace`, `src-no-working-data`). `mvp/`, `mvp-ci.yml` and existing check names are unchanged; no module moved.
* ADR 0006 clarified: Docker build context is `src/`, not the project folder, so images can include the core. Indexed in `docs/reference/README.md`. No regulatory snapshot changed.
* Open: image checks and the Trivy scan are verified locally and still need a CI run; the per-project core extras are provisional until modules move (#199).

## 2026-10-15 Retire prototype/ (#202 step 1)

* Removed all ten tracked `prototype/` files, `.github/workflows/prototype-validation.yml` and the dead `prototype/deploy/**/*.bicep` glob from the `infrastructure` entry in `.github/rubric/artifacts.json`. All ten files were already mapped as archive or retire in the parity matrix (P1). Updated live references in the rubric README, rubric test fixtures, capstone README, ADR 0006 status, the parity matrix, the backlog coordinator agent and the index. Dated historical records and `tools/rename-zava*` identifiers are unchanged.
* The registry edit takes effect only after merge; any score dip is accepted by the owner (2026-10-14). Open: whether `Prototype validation / validate` is a required check (branch protection could not be read with the available token); the service-role denial test remains an open item for `src/api/tests/`.

## [2026-10-15] restructure | M1 isolated leaves moved to src (#199)

* Moved `profile`, `rulecards` and `ai` from `mvp/zavaforward_mvp` to `src/core/src/zava_forward/core`, `test_profile` and `test_rulecards` to `src/core/tests`, and `test_ai_identity` to `src/agents/tests` with `git mv` (pure renames apart from import lines). `mvp/` imports them from the installed `zava_forward.core`; no shim is left. `mvp-ci`, `mvp-validation` install `src/core`, and the `mvp` image now builds from the repository root with a core wheel. `mvp/requirements.*` are unchanged (core adds no third-party dependency; a fresh `pip-compile` drifts only in transitive `pycparser`, so the lock was not regenerated).
* Parity matrix M1 rows marked moved. Test count 719 equals the baseline (702 `mvp` + 17 moved), 92 skipped. Rubric: temporary dip accepted, no `rubric_version` bump. Open: docker is not permitted locally, so the image checks rely on CI; traceability strings in `rulecards.TRACE` still name the old test paths.

## [2026-10-15] restructure | M2 core hub moved to src (#199)

* Moved 25 core hub modules (`store`, `sqlstore`, `mssqlstore`, `factory`, `ledger`, `continuity`, `chatthreads`, `doc_controls`, `documents`, `controls`, `finance`, `grants`, `governance`, `signoffs`, `resident_decisions`, `workflows`, `quality`, `procurement`, `insights`, `projection`, `ranking`, `ai_tasks`, `assistant_release`, `ai_registry`, `assistants`) and `policies/ranking-v1.json` from `mvp/` to `src/core` with `git mv`, plus eight test modules and `release_support` to `src/core/tests` and `test_content_standard` to `src/api/tests`. The shared fixtures from `test_mvp` now live in `src/core/tests/dataset.py`. `mvp/` imports `zava_forward.core`; no shim or copy remains.
* Divergence recorded in the parity matrix: `ai_registry` and `assistants` are in `core`, not `agents` (A1, dependency rule). Four M2-marked tests stay in `mvp/tests` (they use `test_mvp` or the server) and move with M5. Updated `mvp/README.md`, `infra/README.md`, `src/README.md`, CI PYTHONPATH settings and the image (policy now ships as core package data).
* Tests: `mvp` 702 on `main` before; after, `mvp` 551 plus `src` 191 (742 total, equal to the 742 baseline). Open: docker and SQL Server are not available locally, so the image and `mssql` jobs rely on CI; the `core` ruff and mypy exemptions end in M6.

## [2026-10-15] restructure | M3 synthetic tools and data governance moved to src (#199)

* Moved `scale_fixture`, `sensor_backfill` and `loadcheck` to `src/core/src/zava_forward/core/synthetic`, `chat_fixture` to `src/agents/tests`, `document_control_fixtures.json` to `src/core/evals`, `document_form_fixtures.json` to `src/importer/evals`, and `registry.json` to `src/agents/evals`, with seven tests (`test_chat_fixture`, `test_eval_registry` to `agents`, `test_document_form_fixtures` to `importer`, `test_needs_inventory`, `test_sensor_backfill`, `test_sensor_plausibility`, `test_synthetic_provenance` to `core`), all with `git mv`. No shim or copy is left in `mvp/`; `test_recovery`, `test_chat_isolation` and `test_document_controls` import or read the moved files.
* Data governance (ADR 0006): the generators default to the per-user `ZF_DATA` folder (`~/.zava-forward/data/`) through `zava_forward.core.synthetic.output_dir`, never under `src/`. Updated the provenance register, data dictionary, needs inventory, exercise-pack README, eval registry and generator usage strings for the new paths. The owner copy of the real `mvp/data/` to `ZF_DATA` is an owner action before the cut-over gate; `build_mvp_dataset.py` is repointed in #200. The provenance and registry tests now also require `/src/**/data/` in `.gitignore`.
* Divergences in the parity matrix: `chat_fixture` keeps a local role-name map until `auth` moves in M5 (a `mvp` test keeps it equal to `auth.DEFAULT_ROLE_MAP`); `mvp` test commands and CI add `src/agents/tests` to `PYTHONPATH`; `src-ci` also triggers on the synthetic-data docs and generator paths its tests read; temporary ruff and mypy exemptions cover the moved files until M6. No dependency change, so the hashed requirements are untouched.
* Tests: baseline on `main` 742 (`mvp` 551, `src` 191); after, 747 (`mvp` 505, `src` 242: core 196, agents 25, importer 9, api 8, orchestrator 4), 92 skipped. Open: docker and SQL Server are not available locally, so the image and `mssql` jobs rely on CI.

## [2026-10-15] restructure | M4 core features moved to src (#199)

* Moved `chat_privacy`, `chat_isolation` and `recovery` to `src/core/src/zava_forward/core`, `ai_eval` to `src/agents/src/zava_forward/agents`, `ai_priority_golden.json` to `src/agents/evals`, and `test_chat_privacy`, `test_chat_memory`, `test_recovery` and `test_ai_eval` with them, all with `git mv`; no shim or copy remains in `mvp/`. `mvp` imports `zava_forward.core` and `zava_forward.agents`. One pull request (about 1,000 lines, no cycle), so no M4a/M4b split.
* Divergences in the parity matrix: `test_chat_isolation` stays in `mvp/tests` until M5 (it extends the role matrix and server harness); `ai_eval` reads the golden file from `src/agents/evals/` or `ZF_AI_GOLDEN`, which the `mvp` image sets after installing the `agents` wheel; `mvp-ci` and `mvp-validation` install `src/agents` and trigger on `src/agents/**`. Repointed the eval registry, provenance register, data dictionary, needs inventory, chat memory DPIA, `mvp/README.md`, `infra/README.md` and `src/README.md`.
* Tests: baseline on `main` 747 (`mvp` 505, `src` 242); after, 747 (`mvp` 443, `src` 304: core 252, agents 31, importer 9, api 8, orchestrator 4), 92 skipped. No dependency change, so no pip-compile run. Open: docker and SQL Server are not available locally, so the image and `mssql` jobs rely on CI; the `core` and `agents` ruff and mypy exemptions end in M6.

## [2026-10-15] restructure | M5 api, orchestrator and image moved to src (#199)

* Moved `server`, `auth` and `timecapture` to `src/api/src/zava_forward/api`, `web/` to `zava_forward/api/web` (package data), `lawstore` and the law source register to `src/core/src/zava_forward/core`, `digest_blob` and `token_store` to `src/orchestrator/src/zava_forward/orchestrator`, the browser checks to `src/api/checks`, 21 tests to `src/api/tests` and 2 to `src/orchestrator/tests`, all with `git mv`; no shim or copy remains in `mvp/` (only `mvp/README.md`, for M6). `src/api/Dockerfile` replaces `mvp/Dockerfile`; the hashed `src/api/requirements.txt` was regenerated with `pip-compile --generate-hashes` and direct pins are unchanged.
* Divergences in the parity matrix: all remaining tests live in `api/tests` because they build on the server harness; the api image also carries the orchestrator wheel so the Bicep jobs keep running (`python -m zava_forward.orchestrator.token_store` and `.digest_blob`); `mvp-ci`, `mvp-validation` and `src-ci` keep their check names and set `PYTHONPATH` for the shared fixtures. Repointed `infra/README.md`, `mvp/README.md`, `src/README.md`, `.github/copilot-instructions.md`, the UX research notes, the rule card trace and the eval registry.
* Tests: baseline on `main` 747 (`mvp` 443, `core` 252, `agents` 31, `importer` 9, `api` 8, `orchestrator` 4); after, 747 (`mvp` 0, `core` 252, `agents` 31, `importer` 9, `api` 438, `orchestrator` 17). Open: docker and SQL Server are not available locally, so the image and `mssql` jobs rely on CI.

## [2026-10-15] restructure | R1 assistants dispatch rebuilt in src/agents (#107, #199)

* Added `src/agents/src/zava_forward/agents/dispatch.py`: a database-free agents worker with task and result messages, a provider port, bounded call slots and timeout, queue and result-sink ports with in-memory implementations, and `run_once` (acknowledge only after the result post succeeds). `core/assistants.py` gained `build_request`, `shape_result` (extracted unchanged from `execute`) and an injectable `provider` port; the API composes the agents worker. SQL leases, fences, allowance, release admission, quarantine and human review stay in the API.
* Matrix updated (`assistants.py` row and R1 row). #107 stays open: queue transport and result post-back (#144), release approvers unset, retention, break-glass, serving attestation, Azure SQL race evidence and delivered-build acceptance (CON-009/AC-057) need owner decisions or a deployed environment.
* Tests: `agents` 45 (14 new), `api` 440 (94 skipped; 2 new composition tests), `core` and `orchestrator` unchanged; ruff and mypy clean. Docker and SQL Server are not available locally.

## [2026-10-15] restructure | M6 mvp README split and docs repointed (#199)

* Split `mvp/README.md` into `src/api`, `src/core`, `src/agents`, `src/orchestrator` and `src/importer` READMEs, keeping the dated evidence sections and validation record unchanged, and left a short pointer README in `mvp/`. Repointed `README.md`, `infra/README.md`, the architecture index, ADR 0002, the case study addendum, the UX content standard, `src/README.md`, `.github/copilot-instructions.md` and the rubric README; removed the dead `mvp` `sys.path` lines from two infra tests and the `mvp/README.md` rubric glob.
* Removed the `importer` ruff and mypy exemptions. `core`, `api`, `orchestrator` and `agents` keep theirs (about 2,300 findings without them), recorded as a follow-up in `src/README.md` and the parity matrix.
* Tests: baseline on `main` 747 (core 252, agents 31, orchestrator 17, importer 9, api 438; 92 skipped); after, 747. Open: docker and SQL Server are not available locally, so the image and `mssql` jobs rely on CI.

## [2026-10-15] restructure | CI, generator and docs repoint verified against main (#200)

* Verified each #200 criterion against main (see `.copilot-tracking/changes/2026-10-15/issue-200-src-repoint-changes.md`). Most work landed in M1 to M6. Gaps fixed: `build_mvp_dataset.py` no longer puts `mvp` on `sys.path` and defaults its output to `ZF_DATA` (`~/.zava-forward/data/zavaforward.json`); the `mvp-validation.yml` committed-data check now also covers `src/**/data/**`; `src/api/README.md` notes the output location.
* Left open and unticked: new-tag deploy and verification on Container Apps (needs the Azure subscription and a CI-built image; Docker is not available locally), the branch-protection rename (owner decision 2026-10-15: keep names until after cut-over, #201).

## [2026-10-15] build | Excel transition library in src/importer (#80)

* Added `xlsx`, `mapping`, `quarantine` and `export` modules to `src/importer` (standard library only, synthetic data): declared workbook structure with column mapping, conflicts and a row-level preview with lineage; scan through `core` `doc_controls`; quarantine store with a named-human approval gate (approver differs from stager, automation refused) and supersession history portable to SQL Server; CSV and one-way read-only Excel export with a History sheet independent of any AI provider; read-only comparison. 17 new tests (importer 26).
* Open on #80, left unticked: owner staged-transition thresholds (ADR 0001), the export control on every list and the import screen (the api may not import `importer` until #144), AI-assisted column suggestion with approval, importer image and limited SQL role. Docker is permission denied locally and SQL Server is unavailable, so image and `mssql` evidence rely on CI.

## [2026-10-15] build | Environment parameter sets and guard (#137)

* Added `infra/main.test.bicepparam`; dev file now sets the development relaxations explicitly; all three files set `location` and `sqlLocation` to `uksouth` and mark placeholders. `environmentName` allows `pilot`, and a new guard rejects a pilot with relaxations.
* `infra/README.md` gains an Environments section: one differences table, promotion rules, recorded region and quota checks (zone and pilot quota checks left open) and the naming and tagging convention. Tests extended.

## [2026-10-15] implementation | Case conversation panel in src (#159)

* Added the optional case chat panel: `src/core/.../chat_panel.py` (cited, labelled, abstaining answers and workflow-only fallback over the merged chat isolation and thread code), `src/agents/.../chat.py` (provider adapter), `POST /api/chat/threads/{id}/ask` and `/proposals` in `src/api` (proposals use the existing assistants invoke and independent review) and `web/chat.js`.
* Documented in the `src/api` README ("Conversation panel") and the reference index task routing. No `mvp/` change.
* Tests: `core` 256, `agents` 47, `api` 457 (92 skipped), `orchestrator` 17, `importer` 9; ruff and mypy clean. Docker is permission denied and SQL Server is absent locally, so the image and `mssql` jobs rely on CI.
* Open on #159: screen-reader test, live model run, and real chat data (OD-45 to OD-49) need owner action, so those criteria stay unticked and the PR uses `Refs #159`.


## [2026-10-15] implementation | Chat grounding, evaluation and refusal boundaries (#164)

* Added `src/agents/.../chat_eval.py` and `evals/chat_golden.json` (registered in the eval registry, reusing the #108 harness): 21 synthetic multi-turn scenarios across grounding, permission, out-of-scope, prompt injection and memory poisoning, a comparison with the non-AI path, version bindings and failure recording. Three known gaps are recorded as failures, not hidden. The harness never enables chat.
* `src/core` `chat_panel` now refuses approve, decide, consent, contact and diagnose requests before any model call, with a workflow route. Its initial stale-history filtering was partial: it checked citation identifiers and role permissions, not changed source values. `web/chat.js` shows the refusal. No `mvp/` change.
* Tests: `core` 258, `agents` 62, `api` 458 (92 skipped); ruff and mypy clean. Docker is permission denied locally; image and `mssql` evidence rely on CI.
* Open on #164, left unticked: thresholds, accountable reviewer and enablement, independently labelled held-out set, live model run, human exercises and review-effort comparison. The PR uses `Refs #164`.

## [2026-10-15] correction | PR 307 chat refusal and critical evaluation gaps (#164)

* Normalized lexical refusal input with NFKC, format-character removal, common
  Greek/Cyrillic confusable folding and whitespace collapse. Added synthetic
  scenarios for need/want requests, marking a case/person as consented, named
  contact targets, Cyrillic/Greek substitutions and zero-width variants.
* Refusal is lexical and still paraphrase-bypassable. Output approval/consent
  action-claim checks are also lexical; the model's own refusal behaviour is
  unmeasured. No semantic safety or actual-model effectiveness is established.
* Replaced partial assistant-history filtering with exclusion of all assistant
  turns from model input. Stored conversation remains available; current
  projected sources and untrusted user questions still supply context. User
  history may itself contain stale claims or injections, so this is not complete
  stale-content or injection protection.
* The stale-assistant-history and lexical plain-prose approval/consent scenarios
  now pass their real checks. Unsupported claims with valid citations remain an
  open critical gap. Category totals no longer count known gaps as passes;
  critical gap details block report success, CLI exit and enablement.
* Corrected the historical stale-history statement above; the earlier aggregate
  success/insufficient result was not acceptance evidence. Thresholds, reviewer,
  held-out data, live model and human exercises remain open. Synthetic data
  only, ADR 0006 dependencies unchanged, nothing enabled.
* Local validation: core 261, agents 70, api 459 (92 skipped), orchestrator 17,
  importer 39; all suites, dependency-rule tests, ruff and mypy passed. The
  24-scenario/61-turn golden CLI correctly exits 1 with one critical known gap
  (two failed assertions), `passed: false` and enablement `fail`, disabled.

## [2026-10-15] implementation | Building shared systems model and views (#75)

* Added the source-backed building model in `src/core`, with separate systems,
  dependencies, holds, shared works and GBP costs. Exact home/package references
  determine applicability; unknown scope is not approval. Home evidence,
  consent, funding, technical, quality, closure and allocations stay home.
* Reused JSON and checked-document SQL persistence, including the inherited
  MSSQL path, without new SQL or workload dependencies. Existing stores are
  not silently reseeded; linked missing building context is explicitly unknown.
* Added staff-only API and home/building navigation in `src/api`, Finance-only
  shared costs and home allocations, scoped progression/instruction checks and
  wholly fictional regression fixtures. Hazard intake/referral stays independent;
  existing AI remains proposal-only with human gates and no new prompt data.
* Indexed the component guides rather than creating another synthesis page.
  No real register/owner authority, live SQL Server, inference, Azure deployment
  or direct human UX/accessibility acceptance is claimed. The BRD FR-002
  cross-reference in issue #75 differs from the PRD building requirement; this
  implementation follows the explicit issue criteria and PRD FR-002.

## [2026-10-15] update | Needs inventory iteration gate and scenario linkage (#166)

* Reviewed all thirteen SN rows against public migrated source evidence and
  bumped `research/retrofit-synthetic-data/needs-inventory.json` to v1.2.0.
  Corrected stock/EPC, household, chat, scale and sensor fixture notes without
  claiming private output validation, full-volume runs or owner approval.
* Added the versioned `scenario-manifest.json` inventory integration seed:
  reciprocal path, exact inventory version/date and complete reviewed row set.
  All eleven profile and nine workflow execution checks remain deferred to
  #103; no full FR-035, application acceptance or resident consent is claimed.
* Reconciled public provenance metadata, documented the iteration review and
  pre-build issue/PR citation rule, updated the knowledge index/core README and
  extended existing `src/core/tests/test_needs_inventory.py` with positive and
  mutation regressions. No new runtime code or dependencies.
* Owner ratification, row owners, scope/volume decisions, gap mapping and the
  unavailable 2026-10-14 handoff matrix remain open. Tooling checks cannot
  substitute for approval or prove that a GitHub citation preceded a build.

## [2026-10-15] implementation | Src synthetic determinism and protected refresh (#176)

* Extended the migrated core scale and sensor generators, not `mvp/` or a
  replacement private register. Manifests record seed, as-of, version,
  dependency-aware source revision and per-payload hashes. Sensor estimates
  and output share an explicit UTC date window; omitted dates preserve
  historical payloads. Nonempty destinations are refused without overwrite.
* Added whole-directory/multi-shard byte comparisons, pre-change payload
  digests, date/seed sensitivity, dependency-source mutation tests and
  fail-before-write/refresh preservation checks in core/tests.
* Corrected the stale sensor-generator absence claim and linked current src
  recipes in the knowledge-base index. Private OSM-register reproduction,
  full-stock sensor evidence and owner approval of refresh defaults remain
  open; no real data, model evidence, consent or live reset authority is
  invented. No deployment or live records changed.

## [2026-10-15] query | Return, reopen and role-owned handoff controls (#83)

* Extended the migrated core workflow and API/web panels in `src/`, following
  accepted ADR 0006 and the parity matrix; no new `mvp/` code or SQL schema.
* New returns/reopens require reason, human-recorded source and next action;
  versioned history records authenticated authority and the existing receiving
  owner without transferring accountability.
* Kept Offered/Declined storage compatibility and added canonical Sent/Rejected
  status, Received, Escalated and Completed, immutable transition snapshots and
  explicit current/proposed/confirmed/chase responsibility. Legacy handover is
  now an offer, not an acceptance bypass.
* Sender, receiver and manager pending views use existing need-role projection.
  Human-selected due dates, urgency and resident-update commitments remain
  distinct; reassignment/rejection never silently replaces a pending update.
* Updated the [API guide](../../src/api/README.md#return-and-handoff-api-83),
  [core guide](../../src/core/README.md#return-reopen-and-handoff-accountability-83)
  and index. New synthetic JSON/SQLite and HTTP contracts, plus CI-only SQL
  Server replay, cover the bounded controls.
* BG-010/OD-09 approved operational escalation timings remain unresolved.
  Manual escalation and exercise hours are not operational acceptance.
  Existing AI proposal/human-review gates, resident consent and safety controls
  remain; no live inference, Azure deployment or human acceptance is claimed.

## [2026-10-15] query | Generator gap-routing baseline (#167)

* Added a read-only coverage report in `src/core` against the unchanged merged
  needs inventory v1.2.0: all 13 needs routed, two covered and eleven partial.
  Semantic and CLI tests reject malformed/duplicate IDs, issue references,
  blank rationale, unexplained deferrals and unsupported delivered claims.
* Reused the existing generator and determinism suites; no private register,
  new generator, generated output or owner scope/deferral was introduced.
* Updated the pack gap-closure section, core README and this index. Declaration
  presence is not output conformity: scale homes/events use manifest-level
  synthetic labels rather than universal per-record `is_synthetic=true`.
* Owner mapping/row-owner ratification, private stock regeneration, scope and
  volume decisions, full profile/SQL-scale and actual AI/Azure/human acceptance
  remain open. Human approvals, resident consent and AI release gates are unchanged.

## [2026-10-15] query | Generator coverage review repairs (#167, PR #312)

* Require covered/delivered consistency in both directions. Missing needs and
  deferred closures are reported as open gaps with CLI exit 1; partial child
  routes retain exit 0 without claiming delivery or acceptance.
* Replace the overbroad `routing_validated` field with
  `routing_shape_validated` and `issue_existence=not-assessed`. Issue references
  are shape-checked only; neither public consuming epics nor dataset provenance
  provides a complete issue registry.
* Add mutation/CLI tests for unknown routes, issue-less partial deferrals,
  covered child closures and missing needs without closure changes. Use normal
  temporary directories rather than tests/__pycache__.
* Update the core/pack explanations and knowledge index. Inventory values and
  scenario bindings remain unchanged; no private data, generator output, SQL,
  owner approval or real-platform acceptance is introduced.

## [2026-10-15] query | Fluent 2 foundations and non-colour workbench signals (#150)

* Reconciled the [design-system decision](./research/ux/design-system.md) with
  the owner's 2026-10-15 Fluent UI (Fluent 2) choice, superseding the earlier
  extend-current-UI proposal. The [index](./README.md) now reflects that decision.
* Added a source-pinned Fluent token mapping and documented project brand,
  body-size and focus deviations. This native-foundation slice does not complete
  Fluent component-library adoption; the integration/evidence gate remains open.
* Reused migrated `src/api` assets: circle/O, square/W and triangle/! markers,
  matching keys/status names, explicit cluster home/safety counts including zero,
  and visible selected-filter wording. DOM construction avoids record HTML.
* Documented keyboard map activation and named scrollable Overview data tables.
  Updated the AI inventory to describe actual draft-review actions without
  implying approval, resident consent or safety authority.
* Added synthetic local browser coverage of the real API's point/cluster modes,
  rendered tokens, keyboard behavior, narrow widths, forced colours and reduced
  motion, with development-only Playwright and source-CI wiring. No private data
  or external basemap calls are needed.
* Human accessibility acceptance, full Fluent integration, live inference,
  SQL Server and Azure results remain separate unmet evidence. Docker access is
  permission denied locally; image checks remain with CI. No deployment changed.

## [2026-10-15] query | Hazard referral evidence and home retrofit holds (#85)

* Extended the merged `src/core` workflow and `src/api` safety panel/API with
  authenticated report source/awareness, separate sent/received/accepted
  evidence and sender follow-up until safety-service acceptance.
* Recorded the linked-home hold scope/accountable role, externally sourced
  response/resident-update times and independent evidence-backed hold release.
  No hazard categorisation, statutory clock or closure command was added;
  hold release is not hazard resolution or resident consent.
* Preserved legacy history with prospective evidence binding, closed-record
  safety intake, need-role narrative projection and independent building gates.
  Controlled retrofit sign-off, instruction, booking/completion and quality
  handover now enforce an active home hazard hold consistently.
* Updated the [API guide](../../src/api/README.md#hazard-referral-and-retrofit-hold-api-85),
  [core guide](../../src/core/README.md#hazard-referral-and-home-retrofit-holds-85)
  and knowledge-base index. JSON/SQLite and loopback synthetic HTTP tests cover
  the engineering contract; no new code was placed in `mvp/`.
* The issue currently has no comments returned by GitHub. Its BRD FR-015 pointer
  now refers to tenure; current hazard-service authority is RULE-003/FR-003.
  No requirement identifiers were silently changed.
* Approved operational timing/escalation policy, verified service transport,
  real permitted model inference, SQL Server/Azure workflow and human acceptance
  remain open. Existing AI release/human gates stay unchanged; local synthetic
  checks do not establish accepted application-exercise or full issue delivery.
* Updated the content-standard glossary to distinguish stopped retrofit work
  and its restart decision from external hazard-service closure.

## [2026-10-15] query | Task-bound RAI release evidence (#219)

* Extended the merged registry/release gate in `src/core`, following ADR 0006
  and the parity matrix rather than adding a parallel service or `mvp` code.
* Records now require versioned use, prohibited uses, stakeholders, accountable
  owner, impact, residual-risk acceptance, evaluation references and material
  change triggers. Activations retain the exact release ID/version/digest;
  supersession invalidates old work and cannot revive historical routing approval.
* Canonical retained prompts share their hashes with binding/output metadata.
  Cached briefings, ordinary/document and priority review paths recheck release
  validity. JSON configured inference denies without SQL-owned evidence.
* Updated the [core contract](../../src/core/README.md#task-bound-rai-release-records-219),
  [API guide](../../src/api/README.md#rai-task-release-api-219),
  [agents guide](../../src/agents/README.md) and index. Synthetic local HTTP
  checks demonstrate deny/record/propose/revoke without changing case state.
* OQ-017 live holders/delegations, approved real evaluation, independent model
  attestation, direct human oversight and Azure execution remain open. The
  project contact is not a release/risk/suspension/restart authorization.

## [2026-10-15] query | Stock comparisons and human technical decisions (#84)

* Added owned, append-only competing stock assertions in `src/core` with both
  values, source IDs/dates/versions and recorded validation states. Source
  authority, resolution and eligibility remain Unknown; no automatic merge
  or silent cohort exclusion was added.
* Reused four separate human sign-offs, affected-only design reassessment,
  building blockers and hazard holds. Strengthened registered-actor history
  and pre-mutation validation without treating an agent as a professional.
* Centralised observed support versus missing coverage for ranking, staff
  views, filters, counts and AI facts. Existing SQL-derived support/rank keys
  receive an idempotent encoding refresh; no new SQL dialect was introduced.
* Added staff API/read-only evidence panel and JSON/SQLite plus loopback
  HTTP/rendered-browser synthetic checks. Updated the
  [core contract](../../src/core/README.md#stock-comparisons-and-human-technical-sign-offs-84),
  [API guide](../../src/api/README.md#stock-reconciliation-api-84) and index.
* Nomination/challenge and tenure routing stay with #130/#131. Source-authority
  policy, eligibility decisions, operational competence/delegation, real model,
  SQL Server/Azure and direct human acceptance remain unmet. Local engineering
  evidence is not permission for operational use or issue closure.

## [2026-10-15] implementation | Stock fabric and exact case references (#168)

* Moved PR 246's fabric generator into installed `src/core` synthetic tooling,
  preserving v1 seeded attribute draws and adding per-record `is_synthetic`.
  Retained builder/EPC consumers import core; legacy manifests fingerprint
  the moved dependency. No second stock generator or code in `mvp/`.
* Added explicit per-case linked/unlinked reasons, duplicate-ID diagnostics,
  shared-anchor/non-unit scope and a fresh-snapshot CLI through `ZF_DATA`.
  Unknown or ambiguous references are never guessed; home fields, histories,
  resident decisions and human approvals remain independent.
* Updated the synthesis, data dictionary, core guide and index. SN-01 remains
  partial; the private stock generator is unavailable and the owner has not
  approved its regeneration/deferral, inventory mapping or field/unit
  reconciliation. Historical PR 246 private counts were not revalidated.
* Local engineering evidence connects a wholly fictional 60,000-row register
  and seeded fabric to the retained 980-case builder, then compares case
  evidence after closed SQLite restart. It does not establish private-corpus,
  actual-model, SQL Server/Azure or human application acceptance. Existing AI,
  consent and release gates are unchanged.

## [2026-10-15] query | Register-backed historical sensor backfill (#177)

* Added a src/core register adapter to the existing sensor writer, reusing
  merged stock-fabric-v1 with sorted declared subsets, synthetic monitoring
  choices and no copied resident/address fields. Unknown/declined fixtures
  produce no readings; coverage, sanitized fabric and hashes remain explicit.
* Added stock-mode SQL column bounds without migrating legacy stores or
  changing historical fixture payloads. Core guide, synthetic-data synthesis
  and reference index distinguish bounded 730-day fictional tests from a
  full-stock, historical-climate or real-device result.
* Children #178-#183 remain open, not owner-deferred. Climate provenance and
  licence, dated measures, full behaviour/fault truth, #110 integration,
  full-stock storage approval and real AI/SQL Server/Azure/human evidence
  remain unavailable. No new model authority, deployment or resident consent.

## [2026-10-15] query | Shared role workbench IA and recovery (#152)

* Reused the merged Fluent-derived design foundations and migrated API web
  under accepted ADR 0006. No code was added to `mvp/`.
* Added server-described navigation using existing access rules, labelled
  own/programme scope, current destination, keyboard skip and persistent result
  announcements. No client role simulator or new authorization policy.
* Reset restores own cases, all filter defaults and safety-first order with
  logical focus. Case return retains mine/all filters but deliberately reloads
  page one; full previous selection/position/focus restoration remains open.
* Kept safety details expanded before routine forms and retained contractor
  minimum projection. Cancelled obsolete route loads, exposed retry/session
  failures and preserved wide-table keyboard scrolling during narrow reflow.
* Added a versioned bounded eleven-perspective/nine-workflow manifest and
  real loopback synthetic checks for eight existing login roles, five CSS
  widths and 200% root text. Updated the [API guide](../../src/api/README.md#shared-workbench-information-architecture-152),
  [UX synthesis](./research/ux/zava-forward-prototype-profile-review.md#shared-workbench-ia-engineering-slice-2026-10-15)
  and this index. Existing CI browser entry point runs both check suites.
* Owner-supported devices/browsers, full AC-034/043 journey acceptance,
  browser zoom, human/screen-reader and actual model/SQL Server/Azure evidence
  remain unmet. Local Docker access was permission denied; no deployment or
  AI release/approval/consent authority changed.

## [2026-10-15] fix | Stock query lifecycle and case responsibility (#84)

* Corrected PR #318's permanent stock-query hold: separate append-only
  withdrawal or human reconciliation events derive current status without
  editing the original comparison or prior events. Audit retains named
  recorder, event/query references, reason and human evidence.
* Opening requires case ownership or a programme/manager role. Withdrawal
  requires the original raiser or manager; reconciliation is a registered
  named human programme-role attestation, never an agent or sign-off.
* JSON/SQL and authenticated HTTP regressions were observed failing before
  the fix. The lifecycle preserves independent approvals, safety/building
  holds and sibling case isolation; SQL uses existing rowversion/audit
  transactions, with commit-time stock checks and no new SQL dialect.
* Updated [core](../../src/core/README.md#stock-comparisons-and-human-technical-sign-offs-84)
  and [API](../../src/api/README.md#stock-reconciliation-api-84) contracts and
  index. Source authority, resolution rules and eligibility remain
  Unknown/owner-approval-needed. Local evidence is not professional,
  operational, real-model or SQL Server/Azure acceptance; Refs #84 remains.

## [2026-10-15] query | Resident decisions, representative authority and scoped withdrawal (#86)

* Extended existing `src/core` and `src/api` contracts, not `mvp/`, to record
  supplied resident answers against exact measure/scope/design revisions.
  Historical case-wide answers and contact/access/AI output cannot create
  scoped consent. Source, actor and answer history remain separate.
* Added versioned representative tasks, evidence/review dates, resident wishes
  and safe-contact binding. Current authority is rechecked for disclosure,
  consent reliance and dependent release; interpreter/scheduling permission is
  not works-decision authority. Nothing is sent by these local controls.
* Pause/withdrawal flags only its measure for human review. Explicit work-order
  and QA bindings preserve independent sibling release; restart needs new
  supplied acceptance and review evidence. SQL transaction guards recheck the
  dependency using existing case bodies, without new SQL syntax or dependencies.
* Added independent review bound to a recorded decision and distinct reviewer,
  keeping complaint/review, urgent safety and retrofit state independent.
  Detached field projections protect authority/wishes without changing stored
  histories; existing AI proposal and human-review boundaries are preserved.
* Updated the [core guide](../../src/core/README.md#resident-decisions-and-representatives-86),
  [API guide](../../src/api/README.md#resident-decisions-and-representative-api-86)
  and this index. Local JSON/SQLite, synthetic adapter and loopback HTTP evidence
  do not establish real model, SQL Server/Azure or resident acceptance.
* Formal complaints-service integration, real accessible independent review
  without detriment, operational field/retention policy and authorized live
  platform evidence remain open. Docker daemon access is permission denied;
  image checks remain for CI. Issue #86 returns no comments from GitHub.

## [2026-10-16] fix | Resident decisions current-main integration (#86)

* Continued PR #319's interrupted merge of origin/main without aborting,
  rebasing or rewriting history. Preserved both append-only log histories,
  component guide sections and every mypy override module from both parents.
* Combined resident SQL dependencies with main's stock and hazard checks,
  retaining technical sign-off/design-version, handoff, RAI release,
  role-workbench and synthetic behavior. Scoped withdrawal cannot clear
  independent technical or safety gates; sibling release remains isolated.
* Extended endpoint inventory and authenticated role-matrix coverage and
  retained regressions for commit-time dependency checks and cleanup. Local
  core 392, API 516 run/99 skipped and agents 70 suites passed; mypy, Ruff and
  format checks passed in all three projects. Full commands and honest
  environment/skipped-test limits are in the existing
  [changes record](../../.copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md#resumed-integration-results-2026-10-16).
* Refs #86 remains open: formal complaints/human acceptance, operational
  authority/retention and actual model/SQL Server/Azure evidence are not
  established. Local checks do not claim hosted CI, deployment or approval.

## [2026-10-16] query | Role task queues and shared case context (#76)

* Audited all seven #76 criteria against existing `src` after #116/#317/#318;
  preserved delivered identity, role navigation, case card and domain controls.
  Recorded the before/after boundary in the
  [parity matrix](../architecture/mvp-to-src-parity-matrix.md#role-task-queue-offline-slice-2026-10-16).
* Added six visible versioned engineering queue definitions, projected shared
  case/current-history/suggestion/source context, structured blockers, recorded
  hazard-clock observations and server-described single reset. Dynamic
  membership is evaluated before count/page/export using existing JSON/SQL
  read behavior, with no schema or SQL-dialect additions.
* New human-text aliases use the existing need-to-know rules; a sentinel test
  exposed and corrected a coupled derived-status leak. Contractors receive
  neither staff context nor staff-queue rights. No operational rights or
  approvals were granted.
* Local core 401, API 519 (101 skipped), agents 70, orchestrator 17 and
  importer 39 tests passed, with each project's Ruff and mypy checks.
  The real loopback Chromium suites covered role navigation/projection,
  queue membership, consistent current context, responsive case/queue,
  cancellation and versioned reset. API tests exercised SQLite and 120
  interleaved records across page boundaries; browser fixtures used JSON.
* Updated [API](../../src/api/README.md#role-task-queues-and-shared-case-context-76),
  [core](../../src/core/README.md#derived-role-task-queues-76) and reference
  routing. Snapshot age is not a live statutory clock, and document-record
  age is not proof of source freshness or certificate expiry.
* Queue/ranking-policy owner approval, OQ-005 and OD-14/OD-19 role/redaction/
  delegation decisions, direct human acceptance and real AI/SQL Server/Azure
  evidence remain open. Approved priority is visibly unavailable while the
  existing policy remains draft. Refs #76, not issue closure or deployment.
## [2026-10-16] ingest | Rule-card identity and source-review engineering slice

* Extended the existing `src/core` rule-card/law stores and `src/api`
  authentication/routes for #211; no new feature code in `mvp/`.
* Updated the [core lifecycle contract](../../src/core/README.md#rule-cards-adr-0005-phase-2),
  [API authority boundary](../../src/api/README.md#rule-card-approval-api-211)
  and knowledge-base index. Retained versions and approval dates, atomic
  supersession/source reviews, separate trusted rule capabilities, email-fallback
  denial and owner hold now have local synthetic regression coverage.
* Both seed cards remain labelled unassigned exercise drafts. Recorded
  approvals are simulated, not legal or operational approvals; #209 owner
  nomination approves no card. No tenant assignments, real legal approval,
  SQL Server/Azure run, rule-card UI or rule engine is claimed.
* Local core 398 and API 532 tests passed (103 API environment-dependent
  skips); final core 17/API 40 targeted checks and project mypy/ruff checks
  passed. The six-test running loopback app exercise passed. Single RPI
  Review was conformant for the labelled local slice, with four explicitly
  routed deployment/human/product residuals; Refs #211 remains open.
## [2026-10-16] restructure | Complete live src path cut-over (#200)

* Reused the merged source packages, generator imports and private-data guards.
  Aligned the API module entry point, CI version probes/shared build filters,
  Bicep job image selection and branding web/policy targets. Runtime and
  generators now share the external `ZF_DATA` default; no private data was read.
* Updated the [source project index](../../src/README.md#ci),
  [API local recipe](../../src/api/README.md#run-it-locally),
  [orchestrator guide](../../src/orchestrator/README.md),
  [infra source-image recipe](../../infra/README.md#source-image-cut-over-200-2026-10-16),
  [branding guide](../../tools/rename-zava.md), root README, repository instructions
  and knowledge-base routing. Historical deployment identifiers remain exact.
* Kept workflow/check names for branch-protection continuity. The issue #200
  owner comment of 2026-10-15 confirms retention until cut-over; the later naming
  question remains a deliberate single-PR owner decision.
* Local synthetic runtime and four-image non-root/no-data/read-only checks
  passed, as did compiled Bicep build/lint and infra/branding regressions.
  No new tag was deployed to Azure. Private copy/encrypted backup, healthy
  Azure revisions/job executions and #201/#202 owner sign-off remain unmet;
  `mvp/README.md` remains, with no deletion or invented approval.

## [2026-10-16] ingest | Bounded deterministic checks and scoped alerts (Refs #212)

* Extended new exercise card versions with optional immutable executable
  contracts, visible before existing distinct named-owner approval. Seed cards
  remain unapproved drafts; no legal interpretation, awareness date or
  statutory duration was invented.
* Added SQL-fact checks and atomic append-only checkpoints/alerts, explicit
  source/status gating, per-home deadline/harm ordering, attention publication
  limits, owner acknowledgement/outcome and false-positive classifications.
  The engine has no model, resident-message or hold-release path.
* Updated the [core contract and schedule](../../src/core/README.md#deterministic-checks-and-alerts-212),
  [role-scoped alert API](../../src/api/README.md#deterministic-step-alert-api-212)
  and knowledge-base routing. Failed checks remain visibly unknown while
  independently committed hazard work remains available.
* Local constructed SQL/HTTP evidence is distinct from actual legal approval.
  Step UI, hosted scheduling, tenant assignments, real staff precision and
  comprehension, retention policy, continuing-stock acceptance and live SQL
  Server/Azure verification remain unmet. Refs #212, not issue closure.
## [2026-10-16] query | Resident first-contact retention and confirmed field matrix (#86)

* Applied [owner retention/matrix decisions](https://github.com/jmservera/ama/issues/86#issuecomment-6209881675)
  and the [first-interaction clarification](https://github.com/jmservera/ama/issues/86#issuecomment-6209904857):
  five calendar years from first recorded resident contact, including withdrawn
  decisions and expired authority. This supersedes the earlier one-month and
  decision-date proposals; it is exercise policy, not legal advice.
* Updated the [core contract](../../src/core/README.md#resident-decisions-and-representatives-86),
  [API contract](../../src/api/README.md#resident-decisions-and-representative-api-86)
  and index. Liaison/coordination staff record/view, managers view resident
  fields, contractors see only per-measure Proceed/Hold resident flags, and
  agent inputs exclude private resident evidence. Separate complaint/redress
  rights remain unchanged. Missing contact history is Unknown.
* Core 401 run/1 opt-in skip, API 517 run/99 opt-in skips and agents 70 passed.
  Core/API Ruff, format and mypy passed; loopback application and exact
  permission/retention regressions passed. New tests fail without the fix.
* Real Azure SQL in ama/uksouth: isolated Basic database
  resident86test20261016b, constructed DATA only. MssqlStore/SqlStore decisions,
  withdrawal, permissions, anniversary expiry, reopened-state persistence,
  current-payload purge and intact audit verified. Database ledger mode false.
  No existing private database or properwarm input was read.
* Current-payload deletion is manager-reviewed and legal-hold-aware, not a
  configured automatic erasure job. Existing audit text, backups and SQL history
  require separate retention design. Universal cross-case resident identity,
  missing historical contact evidence, named human acceptance and formal
  complaints integration remain open. Refs #86, never closes it.
* Published draft PR #326. Main integration preserved both append-only log
  histories; final integrated core 409/API 534 tests and Ruff/format/mypy passed.
* Authorized ama teardown removed the observed SQL/apps/storage/AI/monitoring
  resources. Final group/environment absence is not independently confirmed:
  the deletion poll and subsequent group reads became Forbidden after
  group-scoped access disappeared; a filtered group list is empty. An operator
  with subscription-scoped read access must confirm completion. No zero-cost
  or complete erasure claim is made; this remains the delivery blocker.
* A later main refresh incorporated accepted PR #325 while retaining both
  shared-queue privacy and the stricter resident contractor projection.
  Final combined core 418/API 537 tests and Ruff/format/mypy passed. Resident
  retention/write persistence and SQL driver remained unchanged; new queue
  reads were validated locally, not claimed as another Azure run.

## [2026-10-16] review-fix | Resident retention expiry limit pinned

* PR #326 review found that after retention expiry and an approved deletion the
  first-contact marker is kept, so the case refuses new resident decisions.
  Documented this as a known limit in `src/core/README.md`, pinned it with a
  core test, and asked the owner on #86 whether renewed contact restarts the
  period. No restart rule was invented.

## [2026-10-16] ingest | Offline source monitoring and regulatory reviews (Refs #213)

* Extended delivered #127 on the merged #210/#211/#212 stores and evaluator,
  entirely in `src/`. Added append-only per-source configuration, local
  observations, unverified candidate differences, exact affected card
  histories and explicit requirements/journeys/tests/communications.
  Candidates remain outside the current law versions and search index;
  detection never changes approved cards.
* Recorded the exercise Legal, Compliance and DPO owner as Juan Manuel
  Servera. Simulated provenance/completeness assessment binds exact targets,
  fixture regression plans and effective dates; latest failures and stale
  source/configuration/card evidence prevent activation. Named owner
  rollback preserves prior events and cannot override intervening decisions.
  No real approval, new legal interpretation or operational acceptance is
  asserted.
* Updated the [core contract and six-criterion audit](../../src/core/README.md#source-change-monitoring-and-review-213),
  [offline job recipe](../../src/orchestrator/README.md#offline-source-change-job-213),
  source index and knowledge routing. The job has no network, approval,
  activation or communication path; no endpoint or role inventory changed.
* Live official retrieval, hosted scheduling/missing-run alerts, exhaustive
  impact mapping, verified new-source publication, actual human legal
  approval, operational regression/notification delivery and live Azure/SQL
  verification remain unmet. Refs #213, never issue closure.
* Published PR #331. Final local core suite: 463 run, one opt-in skip;
  orchestrator: 21 passed. Core/orchestrator Ruff, format and mypy passed.
  Existing API law-store tests: 34 run/16 SQL Server skips; API rule tests:
  five passed. No live legal-source currentness or Azure acceptance is implied.
## [2026-10-16] update | Coordinator guards against accidental issue closing

* PRs #321 and #326 auto-closed #200 and #86 because their bodies contained
  close keywords followed by an issue number, one of them negated. Both issues
  were reopened with a comment. The coordinator merge gate now checks
  `closingIssuesReferences` before merging and reopens issues closed with unmet
  acceptance.

## [2026-10-16] update | Offline Bicep quality gates (Refs #139)

* Strengthened the existing [infra gates](../../infra/README.md#quality-gates):
  per-service compiled endpoint/connection/DNS and public-access assertions,
  local-auth controls, Entra-only SQL, purge/soft-delete/RBAC, exact audit
  container targets and positive retention. Same-assertion mutations demonstrate
  control removal or bypass is rejected; production/public/purge and named
  unsupported-combination checks remain offline.
* Reused the existing error-level linter and parameter guards. Source CI now
  triggers for infra changes and runs all-template build/lint, infra tests and
  scoped ruff within the existing namespace job. Existing workflow/job/check
  names and the legacy validation gate are preserved per #321.
* All-template build exposed subscription-prefixed built-in policy IDs in
  governance; corrected to tenantResourceId without changing audit mode or
  enabling Defender. Added the missing positive audit-retention bound, matching
  the existing digest bound. No control was weakened.
* Policies remain unlocked; legal retention/locking approval, live ARM guard
  messages and private-network/Front Door acceptance are unverified. No
  deployment, Azure resource access, private-data operation or #138 pipeline
  work was performed.
* Published PR #333. Local Bicep 0.48.1 build/lint passed for all entry points
  and modules; 86 infra tests passed with no skips, including 131 compiled
  mutation cases; scoped Ruff check/format passed. One RPI critique and one
  Review completed; no in-scope defect, with live and owner-approval residuals
  routed separately. CI names are unchanged; hosted checks remain separate
  from these local results. No merge or issue disposition is implied.

## [2026-10-16] update | Indexed task queue membership (Refs #327)

* Replaced repeated full work-context scans with a snapshot-scoped inverted
  case-ID index in [core](../../src/core/README.md#derived-role-task-queues-76).
  JSON and SQL queue reads share it; existing visibility, filtering, ordering,
  paging, CSV and per-request narrative projection remain unchanged.
* Recorded [generated 60,000-case timings](../../src/core/README.md#generated-60000-case-queue-timing-327-2026-10-16):
  median repeated nonempty pages improved from 2102.7-2567.9 ms to
  129.6-611.3 ms. The first cold page remained 3090.6 ms versus 3217.4 ms before;
  cold rebuilds still run after writes, snapshot/policy changes or the current
  resident-authority/retention day changes. CSV retains output-size costs.
* Added five core regression methods covering all queues, uncached parity,
  policy/snapshot/day changes, shared/local/cross-process changes and 60k
  evaluator counts. Original-scan mutation fails in both JSON and SQLite;
  the new 60k regression also failed for all six queues before implementation.
* Used only generated fictional data and local pip-venv checks. No private
  datasets, environment files, Docker, Azure, schema migration, changed
  approval/assignment or operational acceptance is involved.
* Local suites totalled 1,140 tests with 104 existing conditional skips; all
  executed tests passed. All five projects passed ruff, formatting and mypy.
  Hosted checks and any live-platform performance remain separate evidence.
* Published PR #336 with Refs #327, no automatic issue-disposition reference.
  One plan critique passed and one implementation Review was Conformant.
  Hosted checks started; merge remains the owner's decision.
## [2026-10-16] update | Rule-engine gating regression coverage (Refs #329)

* Tightened the [core deterministic-check contract](../../src/core/README.md#deterministic-checks-and-alerts-212)
  tests to distinguish exact `not applicable` consultation/historical/future
  source results from `unknown` incomplete/unreviewed/stale/missing evidence.
  Assertions retain source metadata and verify no evaluator call or persisted
  alert for gated sources.
* Added same-home, distinct-case and changed-due-time episode attempts.
  Checks/checkpoints remain persisted while attention publication is limited
  until exactly 24 elapsed hours. Independent home/card/step/item keys and
  immediate cross-case breach escalation are positive controls.
* All 20 rule-engine tests and the full 466-test core suite passed locally
  (one explicit isolated-Azure-SQL opt-in test skipped). Core Ruff check,
  format check and mypy passed in a pip venv. Nine in-memory source-gate,
  shared-throttle, boundary and key-dimension mutations failed the intended
  assertions without changing package files.
* No production defect was revealed; runtime code is unchanged. Evidence uses
  constructed temporary SQL facts and simulated approvals only. No private
  data, cloud service, deployment, actual legal approval or operational
  acceptance is involved. Updated the knowledge-base routing entry.
* Published PR #334 with references-only linkage. One RPI critique and one
  Review completed; Review Conformant with no findings. Hosted checks and the
  owner's merge decision remain separate from local regression evidence.
## [2026-10-16] update | Source monitor retrieval retry cadence (Refs #332)

* Corrected the [core monitor](../../src/core/README.md#source-change-monitoring-and-review-213)
  to measure per-source cadence from the last successful retrieval, retaining
  failed attempts without postponing an already-due source. Latest-attempt
  clock protection remains in force, including failures.
* Updated the [offline job contract](../../src/orchestrator/README.md#offline-source-change-job-213)
  and synthetic core/job regressions for next-day retry, repeated failures,
  successful recovery and exact cadence boundaries. Retrieval success remains
  unverified discovery, not legal approval or rule activation.
* Scope is local source scheduling only; no live retrieval, hosted timer,
  private data, Azure operation or human approval is implied.
* Local pip-venv validation: core 466 tests run with one opt-in skip,
  orchestrator 22 passed; both component Ruff check/format and mypy passed.
  In-memory mutation of the original cadence method made all four selected
  regression methods fail (five assertions including long-cadence subtests),
  while the fixed method passed all four. One RPI Review found no in-scope
  defect; hosted PR checks and the owner merge decision remain separate.
* Published PR #335 with Refs #332 only and no issue-closing references.

## [2026-10-16] update | Source cut-over evidence pack (Refs #200, Refs #201)

* Added the [owner evidence pack](../architecture/cutover-evidence-pack.md),
  [row reconciliation](../architecture/cutover-parity-audit.tsv),
  [scoped legacy-reference inventory](../architecture/cutover-reference-inventory.tsv)
  and [sanitized Azure record](../architecture/cutover-azure-evidence.json).
  All 578 historical tracked path names map to 130 matrix rows/patterns;
  actual-target exceptions and partial worker rebuild remain explicit.
* Ran five local source suites, Ruff/format/mypy, 86 infrastructure tests,
  all Bicep build/lint, 25 rename regressions, JS/namespace/data checks and
  the synthetic Chromium harness. SQL skips, initial dependency/discovery
  failures and the lack of measured coverage equivalence are disclosed.
* Reproduced remote-build failures and added a source-context ACR BuildKit
  task plus a golden-only context exception. Run db8 built four images and
  passed bounded UID/read-only/capabilities/no-working-data-path checks;
  agents client isolation passed. Regression and old-context mutation checks
  fail without the corrections.
* The authorized ama bootstrap failed: Microsoft.Devices is NotRegistered;
  SQL rejected firewall changes with its public interface disabled. No
  subscription registration, policy workaround, tenant change or app exposure
  was attempted. No deployed health/smoke pass is claimed.
* Retained the partial stack and unique image tags for inspection, recording
  resource IDs and ongoing-charge risk; no current post-evidence teardown
  instruction was established. Preserved ama and its pre-existing budget.
  Private-data copy/open/encrypted-backup attestation and sign-off remain
  owner-only, with every checklist box unchecked. No legacy folder deletion
  or workflow rename occurs in this work.
* Published PR #341 with Refs-only linkage. One RPI critique and one Review
  executed; Review outcome Residual work, not accepted cut-over. Hosted checks
  and the owner decision remain separate from this evidence preparation.

## [2026-10-16] update | Resident retention restarts after approved deletion (Refs #86)

* Implemented the [latest owner retention decision](https://github.com/jmservera/ama/issues/86)
  in the [core resident contract](../../src/core/README.md#resident-decisions-and-representatives-86):
  after manager-approved deletion, five calendar years starts from the first
  newly recorded contact, not the deletion or decision date. No contact means
  an Unknown origin/due date; subsequent contact does not extend the period.
* Cleared the cached origin and retained a content-free count tombstone so
  separately purposed old contact records cannot pin the new clock. Same-day
  renewed contacts remain eligible. Older date-only deletions conservatively
  exclude general contacts on/before deletion; fresh safe-contact evidence or
  later-day general contact can establish their new period.
* Replaced the obsolete pinning regression with inherited JSON/SQLite coverage
  for returning residents through each contact route, repeated expiry/deletion/
  renewal, legacy recovery, persistence, fresh scoped acceptance and exact
  personal-data-free tombstone metadata. Old consent is never revived.
* Removed the superseded README known limit and updated reference routing.
  This is an owner-approved exercise rule, not legal advice, historical erasure,
  live-platform evidence or resident acceptance. Existing issue #86 operational
  and human acceptance work remains open. No private data, Docker or Azure
  operation was involved.
* Local pip-venv evidence: full core suite 482 tests with one explicit Azure
  opt-in skip; all executed tests and three resident API tests passed. Core
  Ruff check/format and mypy passed. All ten new inherited JSON/SQLite cases
  failed semantic assertions against the complete original module in memory,
  then passed against the installed changed code without package-file mutation.
* Published PR #338 with Refs #86 only; no issue-disposition reference was
  attached and #86 remained open. One RPI Review completed with a Conformant
  outcome and no in-scope findings. Hosted checks and the owner's merge decision
  remain separate from the local evidence.
## [2026-10-16] update | Image-preserving infrastructure redeploy (Refs #322)

* Applied the owner's 2026-10-16 decision: empty `orchestratorImage` in
  `main.bicep` means the bootstrap placeholder; explicit tags/digests pass
  unchanged to the orchestrator, auth-renewal and ledger-verify jobs.
* Added the [canonical deploy wrapper](../../infra/README.md#orchestrator-image-selection-322),
  because no deployment script existed under infra/ or tools/. It prints and
  preserves a unique existing real job image, otherwise chooses the newest
  updated registry tag, otherwise warns before using the placeholder.
  Conflicting job images and discovery failures stop deployment. Explicit
  image selection is required for intentional roll-forward or reconciliation.
* Discovery distinguishes confirmed absence using group-scoped job/registry
  lists and a registry repository list; no permission/network error is
  interpreted as a bootstrap state. Default operation is what-if; `--apply`
  performs deployment. Workload/environment options bind lookup and deployment
  identity. No resource-group creation/deletion is performed by the helper.
* Local pip-venv evidence: all 103 infra tests passed, including 15 fake-az
  resolver tests and compiled Bicep parameter/consumer assertions. Four
  resolver mutations and three compiled-template mutations fail the intended
  assertions; the actual pre-change HEAD Bicep also fails the new contract.
  Changed Python Ruff check/format and resolver/test mypy passed; main Bicep
  build/lint and Git diff whitespace checks passed. Existing CI discovery and
  check names remain unchanged; its lint selector now includes the new files.
* Updated infrastructure deployment guidance and the knowledge-base routing
  index. No Azure deployment, Docker execution, private data access, pipeline
  #138 integration or live maintenance-job acceptance is claimed.
* One final-candidate RPI critique passed and one implementation Review was
  Conformant with no findings. Publication and hosted checks follow; merge
  remains the owner's decision.
* Published PR #337 with Refs #322 only via a normal topic-branch push.
  Hosted checks were queued at handoff; the owner retains the merge decision.

## [2026-10-16] update | Indexed SQL queue membership on every write (Refs #327)

* Implemented the owner's follow-up to merged #336: six indexed integer flags
  maintained transactionally by SqlStore seed/save, inherited by MssqlStore,
  with the existing case-ID hot cache retained. Permissions and viewer context
  remain request-time, after candidate lookup.
* Existing rows are backfilled before publication. Fingerprint/generation
  checks cover definition, snapshot, complete policy and resident-control day;
  refresh-only changes invalidate other processes. Shared building/procurement
  or linked-home writes conservatively refresh the whole membership generation
  from authoritative SQL state. No approval or queue semantics change.
* Updated the [core contract and measurement recipe](../../src/core/README.md#generated-60000-case-queue-timing-327-2026-10-16),
  API README and knowledge-base routing. On the same generated 60,000-home/case
  fixture (58,224 open), three-round median cold-after-write pages changed from
  2.85-3.49 s to 1.06-1.24 s. Repeats were 0.2-191.8 ms before and 0.2-145.0 ms
  after; the empty priority queue is included. New-page context evaluations fall
  from 58,274 to 50 (58,224 to zero for priority).
* Both runs used the same lightweight evaluator counter and identical fixture,
  with baseline Store/SqlStore loaded from aedd616. Seed/backfill initialisation
  measured 14.213/15.029 s; ordinary writes had 2.5-16.6/3.6-5.1 ms medians,
  with noisy baseline outliers. Global ranking still rebuilds after writes;
  full shared/clock/policy refreshes remain expensive and are not represented
  by ordinary-write timings. These are local SQLite observations, not Azure,
  private-stock, operational or constant-time performance claims.
* Extended uncached parity to positive priority and every queue/sort/view.
  Added physical flag, seed/backfill/reopen, index, rollback, authoritative
  cross-process and portable SQL Server DDL/statement tests, with behavior
  wired into the opt-in real-engine harness. All six benchmark assertions fail
  on the original merged sources; three additional lookup/write/shared-write
  mutations fail the intended assertions without editing package files.
* Local pip-venv suites: core 487 tests (one skip), API 549 (110 skips),
  agents 70, orchestrator 22, importer 39. All executed tests and all five
  projects' Ruff check/format and mypy passed. SQL Server/Azure opt-ins were
  not configured; those skips are not live compatibility evidence.
* Published PR #340 with Refs #327 only and no issue-disposition reference.
  Concurrent main updates #337/#338 were intentionally integrated into the
  topic without rewriting history; only this append-only log conflicted, and
  main's entire log remains an unchanged prefix. The integrated core suite
  passed 495 tests (one skip), nine affected API/portable-SQL tests passed, and
  core Ruff check/format and mypy passed again. Its additional full-suite
  timings were 1.33-2.00 s cold and 0.3-222.6 ms repeated, with unchanged
  bounded context counts; README records this variability. One RPI Review
  was Conformant; hosted checks and the owner merge decision remain separate.
## [2026-10-16] update | Cut-over evidence refreshed after main integration (Refs #200, Refs #201)

* Refreshed the [evidence pack](../architecture/cutover-evidence-pack.md) after
  integrating #337/#338 into PR #341 without rewriting history; preserved all
  append-only log entries. Latest core run: 491 tests, one skip; infra: 103.
  Five latest project suites total 1,164 tests and 104 skips, not measured
  line/branch coverage equivalence.
* ACR db9 rebuilt all four source images and passed bounded remote contracts.
  Recorded current source hashes, immutable image digests and retained IDs.
* Ran the newly merged canonical deploy wrapper: scoped what-if passed,
  apply Failed again on Microsoft.Devices registration and SQL public-interface
  restrictions. No app or deployed smoke pass; 65 generic resources and the
  run-created budget remain billable alongside the preserved original budget.
* Disclosed the additional strict typing probe's 23 upstream test annotation
  errors separately from passing project/CI checks. No unrelated code changes,
  legacy deletion, workflow rename, owner sign-off or second RPI Review.

## 2026-10-16 Backlog board reconciliation

* Added [tools/backlog-sync.py](../../tools/backlog-sync.py), a read-only audit
  (default) and `--apply` repair of the project board against issues and PRs:
  closed issues become Done with criteria ticked, open issues never Done,
  In Progress only with an open PR or live worktree, missing items added.
* Applied it: moved merged-but-partial issues from In Progress to Todo, reopened
  #117 and #122 on the board (criteria unmet), ticked criteria on 17 closed
  issues and set or added board status for 14 issues. About 70 open issues have
  merged PR references but unticked criteria and are listed for evidence-based
  ticking by the coordinator at merge time.
* Updated the coordinator agent with the status and criteria upkeep rules.
## [2026-10-16] query | Private deployed-from-src proof (Refs #200, Refs #201)

* Updated the [cut-over pack](../architecture/cutover-evidence-pack.md),
  [sanitized Azure evidence](../architecture/cutover-azure-evidence.json),
  index and [infra recipe](../../infra/README.md#private-cut-over-proof-2026-10-16).
  Preserved historical failures and every unchecked owner gate.
* Owner confirmed provider registration and acceptable ama costs. Repository
  bootstrap and corrected full source-image rollout succeeded privately;
  SQL public access remained Disabled, without policy/tag/firewall bypass,
  peering, resource deletion or changes outside ama. All three budgets retained.
* Remote ACR runs dba/dbb built four src images and the proof instrument.
  In-VNet jobs initialized schema/two contained users and one fictional case,
  with zero staff. API-MI seedless reload and restart persistence passed;
  private health returned 200 and anonymous, malformed-token and forged-header
  requests returned 401 before/after replacing both serving replicas.
* Corrected explicit-false development networking, added environment-only
  staging and opt-in bearer-only ingress. Corrected ledger alerts to the actual
  Azure Monitor table schema. An instrument allowlist omission failed closed
  after API assistant-table creation; deployed tracked runner source as a
  hashed job command and verified persistence without reseeding or reopening ACR.
* Aggregate smoke is Partially passed: authorized HTTP token acquisition
  returned 400; actual tenant staff initialization requires an owner-supplied
  private roster/approved registration and Graph permissions unavailable to
  this principal. No fabricated human binding, private dataset read, inference,
  worker acceptance, owner sign-off, legacy deletion or workflow rename.

## [2026-10-16] query | Public src browser restoration and deployed parity audit

* Refs #344. Refs #143. Refs #200. Selected additive Front Door Premium,
  WAF Prevention and Private Link to the existing internal environment instead
  of a new external environment. Preserved private SQL and all existing data,
  workloads, budgets and group; no pre-existing deletion, policy bypass, public SQL or
  tenant mutation. Recorded exact new edge resources and image-only audit job.
* Added existing-stack guard/auth-preservation Bicep and explicit health/all-path
  route settings; extended callback initialization for a validated edge HTTPS
  origin with explicit Custom X-Forwarded-Host/Proto forwarding, retaining
  existing callbacks/roles/secrets. Public health/welcome 200, native API 401
  and Entra browser redirect proved. Forwarded-host spoof correction verified;
  only the empty unused rule set created by a rejected header-delete trial
  was removed. Browser API User-Agent 302 remains a filed #350 gap.
* Updated infra/API READMEs, evidence pack/JSON, full feature/16-asset parity
  audit and this index. Image-only execution verified all 17 serving web assets
  match src; anonymous public observations remain distinct from functional
  rendering, positive authorization and real-user acceptance.
* Detected the earlier proof's invalid `systemAssignedIdentity` client literal.
  Matching-tenant read-only discovery found no retained workbench registration.
  Filed tenant browser prerequisites as #349 and all remaining deployed
  feature/data/model/map/photo/law/positive-role acceptance gaps as #350.
  Browser sign-in remains Blocked, not a redirect-shaped success.
* ADR 0005 is accepted for synthetic development only. Real sources/owners,
  legal interpretation/rule activation, consent, safety, financial commitments
  and operational reliance remain named human gates; Juan Manuel Servera is
  the exercise Legal/Compliance/DPO owner. No other approval was invented.
* Published the implementation and honest acceptance boundaries as #352.
  One postimplementation Review ran: Complete execution, Not accepted for full
  #344 acceptance; tenant, browser API and positive-feature findings route to
  #349/#350. No merge or issue-body tick was performed.
## [2026-10-16] query | Hardened source deployment and honest criterion audit

* Refs #118. Updated the reference index, source/infra READMEs and cut-over
  evidence pack with all five original criteria and explicit unmet gates.
* Four local Docker image contracts passed with fail-closed startup, real API
  health/static delivery and five rejected unsafe launches per image.
  Existing CI now runs the same harness and retains unsuppressed scan JSON.
* All four Trivy 0.76.0 scans failed: 61 HIGH and two CRITICAL package findings
  each, 16 unique CVEs, all without a reported fixed version. No ignore lists,
  baselines or unfixed-finding exemption was introduced.
* Compiled Bicep proves six image consumers and the gated Premium/WAF/private
  origin. Disabled Defender opt-in no longer submits Free pricing resources
  that could downgrade existing shared-subscription protection.
* Hosted read-only-root/capability enforcement remains unmet with the current
  Container Apps schema; new image rollout is blocked, not silently relaxed.
  No Azure/public deployment, policy bypass, SQL access change, private data
  read or human approval was performed or inferred. ADR 0005 remains only a
  synthetic-development acceptance with real owners/sources still a gap.

## [2026-10-16] query | Bounded home-specific cited chat (Refs #214)

* Added the synthetic-only cited lookup, source/fact envelope persistence,
  current-role retrieval and selected-turn doubt inbox in src/core,
  src/agents and src/api. Updated their READMEs with the contracts, eight-row
  acceptance audit, privacy/copy semantics and explicit unmet boundaries.
* Reused the merged law store, simulated card lifecycle, shared source gates
  and isolated chat repositories. No legacy code, source snapshots, memory,
  operational approvals or rule-engine state were changed.
* Recorded exact cited-answer/refusal development evaluation and a same-source
  deterministic-card-with-links comparator under src/agents/evals. Context-join
  value is structural offline evidence, not measured staff time, AI benefit,
  semantic conflict detection, human review or legal compliance.
* Owner's 2026-10-16 direction accepts ADR 0005 for synthetic development only;
  Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
  Real sources/delegates/approvals, actual inference, continuing-stock,
  Azure SQL and operational privacy/retention remain unmet. No issue acceptance
  checkbox was updated; the coordinator retains merge-time ownership.

## [2026-10-16] query | Environment strategy and parameter checks (Refs #137, Refs #139)

* Updated [infra environments](../../infra/README.md#environments), parameter
  examples, deployment wrapper and compiled infrastructure tests. Preserved
  file paths and naming lineage; consolidated environment differences into
  one table and documented required tag propagation/component exceptions.
* Current owner direction supersedes the 2026-10-15 pilot region/subscription
  ownership assertion in the issue comment and README. Both stay open;
  pilot locations and dated region/quota check references remain placeholders.
  Historical deployment observations are not current subscription checks.
* Production remains the default. Development alone disables no controls;
  only dev explicitly relaxes purge protection and quarantine. Test/pilot
  keep production protection, all examples keep public networking off, and
  SQL has no public access switch or firewall in any profile.
* Added named missing-check/location guards and ama-only wrapper scope.
  Extended existing issue 139 offline semantic/mutation gates, without new
  workflow/check names, live Azure operations or invented human approvals.
  Juan Manuel Servera remains the synthetic exercise Legal/Compliance/DPO
  owner; ADR 0005 acceptance is development-only, not operational reliance.
## [2026-10-16] decision | ADR 0005 accepted for synthetic development only (Refs #209)

* Updated [ADR 0005](../adrs/0005-regulatory-compliance-assistant.md) to
  record Juan Manuel Servera's 2026-10-16 acceptance for synthetic development,
  not operational approval. Preserved the 2026-10-15 fixture safeguards and
  added decision routing to the [knowledge-base index](./README.md).
* Compared no assistant, rule cards/law store without chat, and the full
  assistant with chat. Accepted measured value over deterministic cards with
  provision links as the chat ship test; no measured pass is claimed.
* Made retrieve, compare, cite, flag and route the explicit authority boundary,
  with prohibited actions and human/resident decision rights retained.
  Recorded Juan Manuel Servera as exercise Legal, Compliance and DPO owner
  for simulated reviews only, without waiving author/approver separation.
* Real company owners/delegations and binding grant awards, contracts and
  leases remain unverified before operational reliance. Search and monitoring
  costs are explicitly unknown; paid deployment, actual processing, real
  legal approval and benefit evidence are not authorized or proved here.

## [2026-10-16] implementation | Synthetic regulatory evaluation gates (Refs #216)

* Added [per-check development evaluation and acceptance audit](../../src/agents/README.md#regulatory-evaluation-gates-216):
  24 frozen source/adversarial questions, independent expected fragments and
  template, negative controls and explicit provisional thresholds pending Juan
  Manuel Servera's exercise-owner agreement. No overall pass or legal approval.
* Recorded a generated 60,000-home seeded stateless baseline: 120,000 exact
  rule-state matches, 78,000 required flags and zero misses among 42,000 required
  hazard flags. Every omitted/mismatched seeded hazard flag is critical.
  Recall threshold remains unset pending baseline review. A separate ten-state
  SQLite engine slice is not continuing-stock or Azure acceptance.
* Added [read-only source-cadence labels](../../src/core/README.md#read-only-source-cadence-labels-216)
  to card collection/version HTTP reads and chat. Missing evidence is unknown;
  failed observations cannot refresh cadence. No activation, hold release,
  alert suppression or new source authority follows.
* Same-role/source-version card links and structural chat facts are recorded,
  but no staff task/comprehension/time/review/cost comparison ran. The report
  recommends cards-only shipment; explicit synthetic-development chat access
  is unchanged. Owner agreement, independent grading, actual staff precision/
  acknowledgement/comprehension and continuing-stock acceptance remain unmet.
  Updated the knowledge-base index; did not modify memory or legal snapshots.
## [2026-10-16] implementation | Regulatory alert and home chat UX (Refs #215)

* Added the [API UX guide and criterion audit](../../src/api/README.md#regulatory-alert-and-home-chat-ux-215)
  and index route for seven audience patterns, plain-language presentation,
  scoped home alerts, structured cited lookup and explicit doubt/missing-source
  states. Reused merged deterministic checks, source monitoring and home chat;
  no new rights, clocks, legal interpretation, approvals or sending.
* Added a synthetic local SQL-backed browser exercise with automated WCAG 2.2
  A/AA-tagged axe checks and keyboard/reflow assertions. This is bounded
  engineering evidence, not complete conformance or staff acceptance.
* Documented a repairs/housing/grants comprehension protocol and left actual
  testing Not run/unmet. ADR 0005 acceptance remains synthetic-development-only;
  real owners/sources, operational approval and measured chat value remain gaps.

## [2026-10-16] query | One-command Entra setup and public-edge discovery (Refs #351, Refs #344)

* Added `infra/scripts/setup-entra.py` and routed the old auth initializer CLI
  to it. The tool discovers the ama API/linked edge, preserves existing
  redirects and roles, provisions missing registration/enterprise app,
  reconciles explicit private user/group role mappings and wires auth.
* Updated the [infra guide](../../infra/README.md#api-registration-management-with-the-existing-m365-session)
  and [knowledge index](./README.md) with isolated device login, fictional
  roster schema, human consent/authority, optional private secret storage and
  interrupted-credential recovery. Added minimal API/edge discovery tags and
  a browser secret-name parameter for later declarative redeployments.
* Read the unpublished #344 branch and pending additive infra changes without
  modifying them. Origin-linked edge discovery and preservation of auth
  exclusions, token storage and bearer/browser action support both designs.
* Evidence is offline mocked-az testing, not a tenant write, private roster
  read, successful browser sign-in or operational approval. Private-network
  SQL staff binding/restart, actual admin consent and human acceptance remain
  separate gates. No private dataset or live Entra identifier was recorded.
## [2026-10-16] implementation | Regulatory security, privacy and audit (Refs #217)

* Added separate trusted RegulatoryChat capability and matching local Entra
  manifest/script declarations alongside RuleAuthor and RuleOwner. Direct and
  generic regulatory-thread access deny without the capability; current token
  roles cannot regain wider hazard access from the staff register.
* Added metadata-only own-role retention review using existing chat settings,
  explicit unknown source/card/check/alert/audit periods and no deletion or DPO
  approval. SQL turn/referral audit now commits with messages/receipts; JSON
  retains its separate-file atomicity limitation. Significant-decision checks
  require recorded reasons, not just an evidence ID.
* Extended the [draft DPIA for DPO review](./research/chat-memory-dpia.md)
  with regulatory data flows, risks, rights/hold questions and unchecked human
  gates. Juan Manuel Servera remains the exercise Legal, Compliance and DPO
  owner; DPIA completion and real retention periods remain unmet.
* Updated [API acceptance evidence](../../src/api/README.md#regulatory-security-privacy-and-audit-217),
  [core controls](../../src/core/README.md#regulatory-privacy-and-audit-217),
  [infra role declaration](../../infra/README.md#regulatory-assistant-capability-roles-217)
  and index. Synthetic local tests, lint/type checks and loopback HTTP only;
  no actual staff/resident data, Azure/tenant changes, model call or operational
  legal approval. Issue checkboxes remain for merge-time coordination.
## [2026-10-16] query | PR 347 deployment hardening review corrections

* Refs #118. Merged origin/main into the existing topic branch and preserved
  both append-only log histories. Updated the reference index, source/infra
  READMEs and [criterion audit](../architecture/cutover-evidence-pack.md#deployment-hardening-audit-118-2026-10-16).
* Removed the shipped fail-closed ENTRYPOINT guard and its two maintenance job
  command additions so images can start on Container Apps. UID/GID 10001 stays.
  Docker runtime controls are enforced and probed in local/CI launch contracts;
  hardened and plain non-root application startup pass. Hosted enforcement
  remains Partial, not silently treated as fulfilled.
* Latest same-tag Python base digest is unchanged. Four no-cache builds reran
  apt upgrade with zero available upgrades. Fresh before/after scans each show
  61 HIGH/two CRITICAL unfixed package findings per image, zero reduction.
  Owner-directed scanner ignore-unfixed true gates only fixable findings;
  separate full/unfixed-inclusive JSON reports remain uploaded and visible.
  No ignore lists, baselines or vulnerability-specific suppressions.
* All five local project suites, Ruff and mypy pass; 130 infra tests, every
  Bicep build/lint, four Docker/application contracts and workflow syntax pass.
  Corrected step-time absolute CI fixture paths after matrix-time workspace
  expansion caused API/orchestrator import failures.
* No public edge changes, Azure execution, policy bypass, SQL public access
  change, private-data read or invented approvals. ADR 0005 remains synthetic
  development only; real owners/sources are still a gap. Issue checkboxes stay
  unchanged; the same PR stays draft until green CI is verified.

## [2026-10-16] query | Integrated PR 347 validation and publication evidence

* Refs #118. Concurrent main advanced while CI ran. Merged it again without
  rewriting history and retained both log histories verbatim. Preserved new
  agents/core test fixtures in the step-time absolute CI configuration.
* Repeated full local validation: 517 core, 553 API, 77 agents, 22 orchestrator
  and 39 importer tests pass, 111 opt-in skips total; all Ruff/format/mypy and
  130 infra tests pass. Four integrated Docker builds and hardened/plain
  startup contracts pass, including real API health/PNG.
* Same-DB integrated image scans still have 61 HIGH/two CRITICAL unfixed
  findings per image, zero fixable findings. Earlier uploaded CI artifacts
  were downloaded and checked, not merely assumed to exist.
* All 11 checks pass at integrated source candidate 8142553 (source CI
  38936437239, API/SQL CI 38936437236, validation 38936437380).
  An earlier browser navigation timeout passed the full local harness unchanged
  and its CI rerun; no test bypass or speculative application change.
* Final documentation/RPI closeout retains identical source/infra/workflows.
  Existing PR ready status requires all latest-head checks green. Hosted
  hardening and other unmet criteria remain Partial; owner review and all
  operational/legal/consent/safety/financial approvals remain separate.

## [2026-10-16] implementation | PR 355 integrated regression corrections

* Refs #216. Merged origin/main into the existing topic branch without rewriting
  history; preserved both append-only log histories.
* Strengthened the retained-card lifecycle regression to compare the entire
  decorated HTTP history across reopen and every underlying stored field.
  Added loaded-empty-store coverage for unknown cadence/checks without alerts,
  and unavailable-store check/alert 503/unknown plus saved human safety intake.
  The logged unavailable-store ValueError was caught handling, not the CI
  failure; the full-suite failure was the additive HTTP-shape assertion.
* Main's stricter automated-decision safeguard requires recorded human reasons.
  Updated the declared synthetic fixture, not the runtime rule, and regenerated
  the report fingerprint without changing its measured positive counts.
* Updated component READMEs and the index with whole-suite commands and exact
  run/pass/skip counts. Owner-agreed thresholds, independent grading, staff
  comparative value and continuing-stock/Azure acceptance remain unmet.
  No issue checkbox, legal approval, live activation, private dataset, Azure
  resource or legacy application tree was changed.
## [2026-10-16] query | Offline CI/CD deployment pipeline

* Refs #138. Added trusted default-branch PR what-if and main-only manual
  source-image release/deployment workflows, pinned actions, job-local OIDC
  permissions, protected environment configuration checks and isolated private
  runner requirements. No retired-layout or legacy CI workflow edits.
* Reused the environment parameter sets, source Docker contexts, hardened/plain
  startup contract and fixable/full Trivy policy. Four run-versioned images
  are handed off as exact digests; no mutable cache reuse or mixed-source release.
* Added ama-only incremental what-if/apply guards, sanitized artifacts,
  quarantine-aware pull-only admission, private SQL checks and strict local
  HTTP health/authentication-denial regressions. Source CI retains existing
  check names and adds dependency-aware image path filtering.
* Updated source/infra guides and reference routing. All live issue criteria
  remain unchecked: no Azure pipeline execution, real federation, reviewer
  approval, release, SQL/model identity proof or operational/legal acceptance
  is claimed. Existing hosted-kernel hardening and pilot setup gaps remain.
* Local evidence: 154 infra tests including the real installed API on an empty
  constructed fixture, Ruff/format, strict helper mypy and actionlint pass.
  All three actual Bicep parameter examples compiled through the new helper
  offline with constructed override fixtures.
  Docker daemon is unavailable locally; no image/Trivy rerun is claimed.

## [2026-10-16] query | Infra CI test-only dependency correction

* Refs #138. Reproduced PR 357 validate's missing `yaml` import in a clean
  Python 3.12 venv with only editable core, agents and API installed:
  infra discovery ran 131 tests with one import error.
* Merged origin/main without rewriting history and retained both log histories.
  The validate infra-test step now installs `PyYAML==6.0.3`, matching source
  CI. No production package dependency was added. Updated the full infra
  quality-gate recipe and reference routing.
* Added assertions for both CI discovery consumers and six mutations covering
  missing, unpinned and late installation. Existing removed-control workflow
  mutations remain intact; no ImportError skip or weakened YAML parser.
* Same-venv discovery passes all 156 tests after the explicit pinned test
  prerequisite. The Bicep-required run with absolute source fixture paths also
  passes; local real API health/authentication-denial probes, Ruff/format and
  strict pipeline helper mypy pass.
* All six live acceptance criteria remain unmet and unchecked. No Azure
  deployment/OIDC execution, new human approval, private-data read or
  operational/legal acceptance is claimed. ADR 0005 remains synthetic-only;
  real owners and sources remain gaps.
## [2026-10-16] implementation | Regulatory UX review regression gates

* Refs #215. Merged origin/main into the existing PR branch and retained both
  append-only log histories. Updated the [API engineering evidence](../../src/api/README.md#local-engineering-checks),
  source README and index without changing issue checkboxes or human authority.
* Wired the regulatory browser harness into src-api CI beside the design-system
  browser check, with hash-verified axe 4.10.3 and uploaded JSON evidence.
  Download failure warns and runs every non-axe assertion; wrong-hash content
  fails. The exact new CI shell block passed locally with successful and
  deliberately failed downloads; hosted CI remains pending, not claimed passed.
* Measured 142 interactive targets across 17 browser states, minimum 24px in
  both axes. Raised citation links from 18px inline boxes to 24px targets.
  Removing the regulatory summary rule failed the real check at 1198 x 24px
  against the retained 44px disclosure design floor; restoring it passed.
  A 24px unstyled summary is not itself an AA violation.
* Existing 86 API and 33 core regressions, three new harness tests, the existing
  design-system browser check, API ruff/format/mypy passed. Axe still reports
  eight contrast-incomplete states; full WCAG, real staff comprehension,
  measured chat value and real owners/sources remain unmet. No operational
  approval, rule activation, consent, safety or financial commitment is added.

## [2026-10-16] implementation | Browser-free regulatory UX unit imports

* Refs #215. Merged origin/main into the existing PR branch first, preserving
  every line from both append-only log histories in order. Combined main's
  privacy/retention warning and textarea association with the existing
  accessible live-log/list and unavailable-chat fallback.
* Reproduced the reported import failure in `/tmp/v215c` with editable core,
  agents and API runtime distributions only. Deferred browser runtime imports
  and retained Page typing under TYPE_CHECKING, without adding runtime
  dependencies, skipping pure tests or weakening mypy. Added a subprocess
  regression that explicitly rejects eager Playwright imports.
* Full API discovery passes without Playwright and again with Playwright
  1.64.0: 561 tests, 110 opt-in skips in each environment. All four harness
  unit tests, 56 core regulatory regressions, API Ruff/format and strict mypy
  pass. Existing source CI still executes both browser harnesses.
* Both real synthetic loopback browser checks pass. The regulatory check with
  hash-verified axe retains 17 states and 142 targets, zero detected violations
  and eight contrast-incomplete states. Updated [API commands and evidence](../../src/api/README.md#local-engineering-checks),
  source README and index. Full WCAG and staff comprehension remain unmet;
  no issue checkboxes, actual legal/consent/safety/financial approvals, Azure
  resources or real owner/source gaps are changed.
## [2026-10-16] implementation | Entra setup review findings and infra CI repair (Refs #351)

* Merged current main into the existing setup topic without rewriting history;
  retained both sides of the append-only log conflict. Read pending public-edge
  changes without editing that branch; setup preserves its Custom forwarded
  headers and supports the legacy CLI's delegated `--public-url`.
* Moved planned effective user/group role-conflict rejection before any
  registration/enterprise-app writes. Added selected-vault metadata-only
  preflight before one-time credentials and final provisioning checks even
  for converged runtime values. No secret values are read by the vault probe.
* Reproduced the failing infra suite in an isolated pip venv with editable
  source distributions; repaired the parameterized secret-inventory assertion
  and the compiled-policy test's CI formatting. All 177 infra tests, all
  template build/lint checks, workflow static checks, setup mypy and both
  local CLI help launches pass. Each review safeguard's behavioral test fails
  when its fix is removed in memory.
* Updated the [infra guide](../../infra/README.md#post-deployment-api-authentication-initialization)
  and [index](./README.md). Mock evidence proves sequencing/idempotence, not
  tenant writes, live vault permissions, human consent, private SQL bindings/
  restart or browser sign-in. No private roster/dataset was read and no Azure
  policy, resource or network setting was changed. Exercise legal ownership
  and the development-only ADR 0005 boundary remain unchanged.

## [2026-10-16] implementation | Public edge review continuation (Refs #344)

* Merged main into PR #352 without rewriting history. Retained both sides of
  evidence/log/compiled-test conflicts and the #351 CLI delegation to
  `setup-entra.py`; its existing linked-edge callback tests remain authoritative.
* Added a fail-closed UUID-syntax prerequisite before the existing-stack
  auth/edge writes, rejecting `systemAssignedIdentity` with setup guidance.
  Compiled behavioral tests reject non-empty-only/bypassed/disabled/unordered
  guard mutations. A separate regression pins the legacy CLI's delegation.
* Documented full-resource auth PUT preservation as limited to read-visible
  references: `union` cannot reconstruct omitted, write-only or redacted fields.
  No secret value or live auth configuration was read/written.
* Fresh public probes retain health 200, native API 401, browser app 302 and
  browser API 302 even with JSON Accept; User-Agent-sensitive handling is not
  API-wide 401 acceptance. Refs #350. Read-only SQL/environment checks retain
  public access Disabled and an internal environment; no Azure writes.
* Updated the infra guide, cut-over evidence/JSON and reference index.
  Full acceptance remains Blocked on authorized real registration/credential/
  staff setup and human sign-in (#349), browser API coexistence and positive
  feature evidence (#350). No issue tick, merge or operational approval.

## [2026-10-16] implementation | Offline direct demo ingress (Refs #360)

* Added explicit demo-only external Container Apps configuration, distinct
  replacement workload names/subnet/HTTPS NSG and inactive background staging.
  Default/production isolation, private backing services and reused identities
  remain; no broad public-data access or Azure operations are authorized.
* Added direct Entra discovery from an explicit flag or demo app tag without
  Front Door discovery/cdn requirements, mode-aware browser auth reconciliation
  and strict public probes. Fake CLI/HTTP tests are offline engineering
  evidence, not tenant authority, directory writes or successful human sign-in.
* Updated [infra migration/runbook](../../infra/README.md#direct-demo-ingress-migration-proposal-2026-10-16-360),
  [ADR 0001](../adrs/0001-azure-architecture.md#direct-synthetic-demo-entry-decision-2026-10-16),
  architecture notes, [cut-over audit](../architecture/cutover-evidence-pack.md#direct-demo-ingress-offline-scope-2026-10-16)
  and index. Historical Front Door observations and MVP git-only direct callback
  prior art remain distinct from the proposed replacement; obsolete broad
  development exposure is not copied.
* The proposed sequence includes image/config/DNS/identity parity, all queue and
  scheduled consumer staging/drain, rollback, separately authorized selective
  retirement and cost sensitivity, not a quote or financial approval.
  Criterion c owner approval and d/e live verification/retirement remain unmet.
  No issue checkbox, Azure resource, private dataset or tenant object changed;
  `ama` and all private endpoints remain untouched. Browser JSON API 302 remains
  an explicit failure/gap, not a denial pass.
* Offline validation: 234 infra tests with required local Bicep compiler,
  all root/module template builds/lints, CI-aligned Bicep-test Ruff/format,
  probe Ruff and setup mypy passed. API suite passed 563 tests with 110
  conditional skips after correcting the discovery working directory.
  Broader setup Ruff/probe mypy retain baseline diagnostics, none introduced.
* Juan Manuel Servera remains the exercise Legal, Compliance and DPO owner;
  ADR 0005 is accepted for synthetic development only. No actual legal,
  consent, safety, rule activation, spending or operational approval is inferred.

## [2026-10-16] implementation | Routed direct-ingress review corrections (Refs #360)

* The single Review returned Not accepted for overlong demo job names and an
  invalid role-denial endpoint. Subsequent bounded implementation shortens only
  demo job suffixes and aligns ledger alerts; compiled tests cover supported
  workload/environment bounds and preserve existing names.
* Role-denial probes now establish authenticated Contractor `/api/me` 200,
  then require staff-only `/api/stats` 403. The actual local provider/router
  regression distinguishes valid Contractor authorization from anonymous/
  unknown-session authentication failure. Credentials and response bodies
  remain private and unlogged.
* Updated the infra runbook and evidence receipt without rewriting the
  completed Review or claiming another review/conformance. Owner approval and
  all replacement live/retirement gates remain unmet; no Azure operation.
* Corrected full infra suite passed 237 tests without skips, including 46
  compiled-policy and 20 proof/probe tests. Corrected Bicep builds/lints,
  scoped Ruff and CI-format checks passed.
* Integrated current main's device-code/missing-tool diagnostics changes
  without rewriting history; final infra suite passed 238 tests without skips
  and setup production mypy passed. Opened PR #362 for human review; no issue
  ticks, live acceptance, deletion or merge.

## [2026-10-16] ingest | Single-command Entra onboarding continuation

* Refs #360. Continued the existing topic/PR and RPI plan, without repeating
  completed research, critique or the historical Review.
* Updated `infra/scripts/setup-entra.py`, the directly coupled SQL/deployment
  helpers, Bicep guards and offline tests: automatic credential discovery and
  direct-demo app-local fallback, private roster template/validation/helpers,
  post-reconcile Entra verification, SQL check/confirmation/apply/restart or
  exact authorized-host handoff, and advisory deployment coordination.
* Updated `infra/README.md`, the cut-over evidence pack and this index. Store
  tags plus guarded CLI/CI and Bicep parameters prevent supported full
  application deployments from overwriting app-local credentials; dependency
  updates must explicitly retain that store and omit application deployment.
* No Azure, directory, private-dataset or network changes were performed.
  Advisory tags do not prove a simultaneous-start distributed mutex. Real
  browser, vault/MI, SQL/restart and original migration/retirement acceptance
  remain unproved; no issue checkboxes or approval records were changed.
* Final offline validation: 260 infra tests with compiled Bicep guards and no
  skips, four-script scoped mypy, focused Ruff with no introduced baseline
  findings, 32 responsive loopback API auth tests and Markdown/diff checks.

## [2026-10-16] ingest | Automatic private demo roster follow-up

* Refs #360. Implemented missing/exact-template roster generation using existing
  private SQL codes/roles/supplier scopes and enabled member Graph users with
  individual-mailbox purpose evidence; no invented staff codes or people.
* Reserved the first stable ProgrammeManager code for the selected admin,
  seeded remaining distinct assignments, privately persisted version/seed/staff,
  and preserved existing Entra verification then SQL check/confirmation/restart.
  Production/unknown/conflicting profiles and existing immutable SQL bindings
  refuse regeneration. Shortages report exact counts and stop, never reuse.
* Updated `infra/README.md`, registration guidance, the cut-over evidence pack
  and reference index. Both private roster readers retain legacy arrays. No
  private names, UPNs or directory IDs enter generated summaries or handoff.
* Official Graph mailbox-settings API/purpose documentation retrieved
  2026-10-16 identifies the classification and MailboxSettings.Read prerequisite.
  Missing mailbox access fails closed; no permissions are granted automatically.
* Offline infra suite: 282 tests passed without skips, including compiled Bicep
  profile-tag protection and mocked SQL/Graph cases. Scoped production mypy
  and 32 responsive loopback API auth tests passed; actual tenant people,
  browser sign-in, SQL binding/restart and migration/retirement approvals remain
  Not run or unmet. No Azure writes, live setup, issue ticks or approval claims.

## [2026-10-16] ingest | Synthetic generator replay inputs and acceptance audit

* Refs #176. Updated the existing synthetic-data README and reference index
  with a per-criterion audit and exact fabric replay inputs; updated
  `src/core/README.md` with the CLI recipe and provenance contract.
* Fabric CLI now captures exact register/optional case bytes once, hashes
  those inputs without source paths/content, and records a strict optional
  as-of label (unknown when omitted). Algorithm draws and payload histories
  are preserved; snapshot labels do not imply evidence freshness.
* Local 45-test generator regression covers exact byte replay, both sensor
  modes, source/seed/date changes, consumed-byte compatibility, manifests,
  refused refreshes and fixture-backed SQL restart. No private source data,
  Azure, live resets or setup-entra changes.
* AC1 remains unmet for the missing original stock-register generator and
  pinned OSM inputs; current manifests pass but historical stock/public
  receipts are not regenerated. Refresh cadence/approval/live-protection
  policy is documented, not owner-approved. No resident, legal, safety,
  financial or operational approval is inferred; issue ticks stay unchanged.
## [2026-10-16] query | Offline historical climate source audit

* Refs #178. Updated the existing sensor analytics research plan with the
  2026-10-15 owner direction: Met Office (UKCP18) and Environment Agency
  OGL data where available, otherwise clearly labelled synthetic data.
* Recorded every issue candidate and both owner-directed leads across
  coverage, resolution and licence/reuse evidence gaps. No external climate
  metadata, licence page or observation records were retrieved under the
  offline-only instruction; no product facts, retrieval dates or climate
  figures are presented as verified.
* Retained the existing synthetic generator and exercise plausibility
  expectations unchanged. Documented the required local provenance/terms
  packet, reproducible observed-extrema procedure and explicit unmet audit
  for all three issue criteria; source direction is not reuse confirmation.
* Updated the reference index and core README. Juan Manuel Servera remains
  the exercise Legal, Compliance and DPO owner; dataset-specific reuse,
  competent method review and operational authority are not inferred.
  No issue checkboxes, executable files, private data or Azure state changed.
## [2026-10-16] update | Demo external environment created (#360)

* Owner approved (via ask_user form): full migration at once, Key Vault
  credential store, retire the old environment without a rollback window, and
  retire the demo Front Door without a second confirmation. Group `ama` is
  never deleted.
* Applied the environment-only deployment `demo-env-360` (`demoDirectIngress`,
  `deployApplications=false`, `deployBackgroundWorkloads=false`, registry
  quarantine pinned to the live false value). Created `cae-cutover-test-demo`
  (external, own subnet and NSG) and its diagnostics. The old environment, apps,
  jobs and Front Door were not changed. SQL, Key Vault, storage and registry
  still report public network access Disabled.
* Blocked: the demo apps cannot be deployed yet. The Key Vault credential
  `entra-client-secret` and the real registration client ID need the owner's
  Entra login and private vault access (this VM's service principal cannot read
  the tenant or the vault). Old resources are retained because no replacement
  serves traffic; real browser sign-in, roles, SQL and AI remain unverified.
* Next: owner runs `python3 infra/scripts/setup-entra.py --direct-ingress`
  from an authorised host, then the coordinator deploys the apps and jobs,
  verifies, and retires the old stack and Front Door.

## [2026-10-16] ingest | Explicit orchestrator image whitespace

* Refs #339. Trim explicit `--orchestrator-image` before image selection so
  empty or whitespace-only values use existing discovery and warned placeholder
  fallback instead of forwarding a blank image to Bicep.
* Expanded `infra/tests/test_deploy.py` subprocess coverage for empty/spaces/
  tabs-newlines, existing-job and placeholder outcomes, what-if/apply and
  padded explicit tags/digests/placeholder. Updated `infra/README.md`.
* Validation is offline with isolated fake Azure CLI responses. No live Azure,
  setup-entra changes, private datasets, operational approvals or issue ticks.
* Expanded regressions failed in 11 subcases before normalization; all 19 deploy
  tests pass after the fix, with scoped Ruff/format/mypy and local CLI help.

## [2026-10-16] ingest | Offline synthetic dictionary and provenance audit

* Refs #175. Updated the existing dictionary/register for generated sensor
  readings/registers/manifests, stock-scale homes/households/events, derived
  fabric/link reports, scripted chat/evals and potentially personal runtime
  messages/memory. Visibility is separate from full-stock materialization.
* Added the core offline pattern/label checker with public-only and explicit
  snapshot modes, sanitized diagnostics and independently failing source audit.
  Replaced private-stock-reading regressions with public inventory, ignored-path
  and fresh generated-fixture checks; generated chat tests cover all nine
  payloads. Generator payload bytes and approval/consent boundaries are unchanged.
* The acceptance audit marks three local engineering criteria met for their
  stated scope and external-source completeness unmet. Historic retrieval
  dates and verified licence/attribution terms for Census TS054, IMD 2025 and ONS
  boundaries remain unavailable; no dates or legal approvals were invented.
  Exercise Legal, Compliance and DPO owner Juan Manuel Servera owns review;
  operational owners/sources remain a gap. No Azure, actual model, private data
  attestation or universal PII-free certification is claimed.
* Updated the knowledge-base index and relevant core/agents/pack READMEs.

## [2026-10-16] ingest | In-VNet staff job continuation

* Refs #360. Added `--run-in-azure` and automatic fallback for blocked local
  candidate/check SQL work. Directory grants and seeded roster generation stay
  under the operator login; uncertain local applies never switch execution hosts.
* Extended the source-based proof image with the SQL-only staff worker, shared
  protected-roster preparation and manifest. Existing SQL-admin MI performs
  SQL binding, post-commit verification and API restart through an optional
  API-only custom role, separately inventoried in the role matrix.
* Roster/request and fresh encryption key use a temporary job secret, never
  command-line values. Authenticated encrypted results are captured privately
  from explicit job execution/replica logs; normal output is codes-free on
  the Azure path. Owned-job deletion removes the transfer secret; timeout,
  uncertain creation, interruption and failed cleanup remain explicit.
* Updated the infra runbook, cut-over acceptance audit and reference index.
  The runbook records required image build, scoped role deployment, actual
  log-endpoint access, private-host fallback and leftover-job recovery.
* Offline validation: 304 infra tests passed without skips, 32 responsive
  loopback API auth tests passed, all ten CI-gated infra Python files passed
  Ruff/format, worker/transport mypy and standalone Bicep build/lint passed.
  Tests use synthetic fixtures, not private datasets or live Azure.
* No Azure commands against live resources, image builds, network changes,
  tenant writes, issue ticks or approvals. Image/role activation, actual log
  access, private SQL binding/restart, real browser sign-in and human cut-over
  acceptance remain Not run or unmet.

## [2026-10-17] ingest | Online official climate-source evidence

* Refs #178, continuing merged #367's explicitly offline audit. Retrieved
  official metadata/terms for HadUK-Grid, MIDAS Open, historic stations, ERA5,
  CIBSE, UKCP18 and the EA flood-monitoring lead. Integrated comparison and
  dataset-specific source register into the existing sensor research synthesis.
* Recommended exact regional HadUK-Grid v1.3.2.ceda for monthly historical
  context only, with OGL v3 and catalogue citation. Actual RH file request
  returned CEDA login HTML, not data; no registration/login/terms acceptance.
  Met Office website automation restriction recorded; no further retrieval
  after discovering it. Owner licence/reuse approval remains UNMET.
* Retrieved public Durham monthly file, hash-pinned the local input and used
  the focused offline standard-library helper to derive 1991-2020 statistics:
  360 calendar months, 351 accepted pairs, nine estimated exclusions per field.
  Retained derived JSON with extrema/months/lines/counts, not a raw data bundle.
  No humidity, instantaneous or regional replay bounds inferred.
* Added tiny wholly synthetic helper regressions and updated the index and
  core README's directly coupled climate status. Earlier
  offline findings remain dated history; original/snapshots/memory untouched.
  No private datasets, stock generation, live database, Azure or spending.
  Issue remains open for exact remaining terms/access/paired-record evidence
  and human approval; generator parameters and operational controls unchanged.

## [2026-10-17] implementation | Opt-in sensor fault packets and separate truth

* Refs #182, continuing merged #320/#177 in src/core, not another stock or
  audit-only delivery. Added explicit seeded configurable exclusive two-reading
  packet rates for outlier, stuck, drift, gap, duplicate, out-of-order,
  unmapped, wrong-unit, clock-skewed and uncalibrated, plus valid remainder.
* Retained nominal clean packets, labels and emitted shard positions in
  evaluator-only truth/; analysis/ contains no injected labels, fault profiles,
  rate config or truth links. Synthetic stock/fabric identities and monitoring
  exclusions are reused. New schema is refused by the legacy database loader.
* Preserved default historical CSV hashes. Focused semantic tests detect 15
  broken variants; the tiny fictional five-home CLI selection has three granted,
  one declined and one unknown, 292 delivered rows and 144 truth packets covering
  all 11 classes, byte-identical across reruns.
* Updated the core README, existing synthetic synthesis and this index.
  All rates/magnitudes are exercise values, not scientific bounds or operational
  rules. No private data, private 60,000-home output, live IoT/SQL/AI/Azure,
  spending, infra/authentication, ranking, approval or resident-choice changes.
  #183/#110 consumer integration and AC-066 live-platform acceptance remain
  separate; no analytics-method or real-monitoring approval is inferred.

## [2026-10-17] update | Credential expiry and secret-reference preservation

* Refs #358. Updated the existing cutover evidence pack and setup runbook with
  generated/legacy stored-expiry coverage, KV URL/identity reconciliation across
  full/sparse/omitted responses, exact app-value/reference retention and safe
  inventory refusal. Added a reference-only pending-handoff guard so failed
  readback cannot silently activate auth on rerun.
* Recorded 15 real failing-before assertions, seven killed behavioral safeguard
  mutations and 313 passing offline infra tests, including 101 setup tests.
  Existing legacy delegation and merged #370 job/CI behavior are preserved.
* Actual existing-resource non-production preservation remains UNMET / Not run;
  public schema and mocks are not live evidence. No Azure/Graph/SQL operations,
  secret/private-data reads, role/network changes, image builds or new spending.
  Broader setup/job readiness and live coordination remain #360. Index updated;
  prior log entries and owner memory untouched.

## [2026-10-17] implementation | Queue signal definitions and versioned reset

* Refs #77, parent #76 hierarchy only, no ordering dependencies. Completed the
  existing src API queue's Show only definitions, explicit perspective/workflow
  stage/search/own-all scope and server-versioned reset scope. Empty proposed
  reviewer is explicitly Unknown; case selection reuses own-record context.
* Updated the existing UX profile-review synthesis, API guide and reference
  routing. Native disclosure/controls, Fluent tokens, reduced motion, ranking,
  permission intersections and human/resident approval boundaries are retained.
* Evidence uses three tiny constructed cases and the actual local application;
  no private stock, credentials, paid model, live SQL Server/Azure or new service.
  Human accessibility/comprehension, complete workflow representation, operational
  owner ratification and live-platform exercise acceptance remain separate.

## [2026-10-17] implementation | Laptop-safe setup and restricted migration (Refs #360)

* Completed Research (3e24e7c), Plan (96871b3, one critique with direct
  dispositions) and Implement. Dated phase evidence and state are committed
  under .copilot-tracking; one post-implementation Review remains next.
* Replaced private-console result dependence with bounded authenticated
  ciphertext in existing initializer ARM tags, owned-run cleanup and verified
  same-VNet parent discovery. Key Vault handoff uses a minimal secureString
  ARM deployment, exact single-secret Create what-if and metadata verification.
  No app fallback, plaintext roster/key in tags, or private endpoint opening.
  Actual vault what-if passed; intercepted PUT, no secret created.
* Approved deployment demo-stage-360-20261017 created only the replacement
  API/auth in the already existing external environment after reviewed what-if.
  Retained source fingerprint, immutable image, runtime settings, identity and
  auth verified; new replica Healthy/Running. Deny-all keeps four direct routes
  403 pending genuine tenant/runtime setup; this is not welcome/health/login
  acceptance. Old API/environment/Front Door and all six Disabled backing
  public-access settings remain preserved.
* Full infra 319 tests/no skips, API auth 32 tests, all 22 Bicep build/lint,
  existing relevant eleven-file Ruff/format, strict/scoped mypy and pip check
  passed. No expiry/reuse or app-secret preservation edits owned by #358.
* [Current a-f audit](../architecture/cutover-evidence-pack.md#laptop-setup-and-restricted-migration-readiness-2026-10-17),
  [runbook](../../infra/README.md#in-vnet-sql-staff-step-refs-360) and
  [ADR status](../adrs/0001-azure-architecture.md#direct-synthetic-demo-entry-decision-2026-10-16)
  distinguish source delivery/staging from **UNMET d/e**.
  Private image publisher, explicit source-job tags/demo-API restart role
  activation and human tenant/mailbox/roster/browser/SQL/AI gates remain.
  No live role, Graph, SQL or credential write, build, exposure or retirement;
  no issue closure or human sign-off inferred.

## [2026-10-17] review | Demo readiness full RPI phase completion (Refs #360)

* Completed the one post-implementation Review of 6f43559; execution Complete,
  outcome Residual work, not conformant live readiness. Research, Plan,
  Implement and Review all have dated persistent artifacts/completion records.
* No material source defect identified in the supplied boundary. RV-001/002/
  003/004 route existing private-publisher, explicit IAM, human tenant/runtime
  acceptance and gated retirement work to their distinct owners. No second
  Review, source correction loop or further Azure action.
* Refs #360 publication follows; issue d/e and human approval remain unmet.
  No coordinator-owned issue closure, merge or child task is performed.

## [2026-10-17] delivery | Demo readiness PR published and session stopped (Refs #360)

* Published [PR #375](https://github.com/jmservera/ama/pull/375), base main,
  branch fix/demo-setup-readiness-360, Refs #360 only. Observed initial remote
  head 4b50561cff0a0f1b6598bad3451e962f66e4f890; final receipt-only completion
  commit records this publication and stopped state, without source/live changes.
* All four RPI phases complete with dated committed evidence. One critique,
  one Review (Complete / Residual work); current source candidate 6f43559.
  Exact final PR head is read back after the receipt commit push, not embedded
  circularly in its own committed content.
* Automatic session stopped under the caller's explicit publication boundary.
  No issue closed, merge, force-push or child task. d/e remain UNMET; exact
  owner actions and actual resource/validation evidence are in the PR/current
  audit. No human approval or operational readiness is inferred.

## [2026-10-17] integration | Same-session PR #375 upstream and blocker continuation

* Owner explicitly resumed #360/PR #375, authorized latest-main rebase and
  topic-only force-with-lease. Integrated main 51db4fa8 (#373 sensor faults,
  #374 credential preservation), retaining exact #358 helper source, expiry/
  selection/readback/handoff behavior, upstream tests and legacy CLI delegate.
  Both index/evidence sections and entire upstream append-only log prefix
  retained; no sensor or upstream evidence changes.
* Four additive combined ARM/KV inventory, digest/recovery, failure and generated/
  legacy expiry tests; focused37, unchanged setup/legacy/mutation101 and
  full infra329/no skips passed. Existing eleven-file Ruff/format, strict/scoped
  mypy, all22 Bicep build/lint and pip check passed. Broader retained workflow
  results are recorded in the same changes artifact, not a new delivery loop.
* [Concrete publisher/IAM evidence](../../infra/README.md#private-publication-blocker-evidence-2026-10-17-pr-375-continuation):
  actual Docker socket permission denial, anonymous registry403 and GitHub
  packages403 (missing read:packages, inventory unknown). Registry task/pool
  lists and self-hosted runner list empty; permitted ama inventory has no
  builder VM/ACI. Current CI retains reports, not images; historical default
  quick-run success does not provide a private-connected publisher now.
* Official ACR guidance requires a dedicated pool/public task-IP rules for
  private builds, or trusted-service bypass for restricted import. No pool,
  new spend/network change prohibited: neither build nor import attempted or
  claimed as an actual denied write. IAM activation also not attempted:
  explicit approval still required, not an observed AuthorizationFailed.
  Smallest actions: identify existing private-connected builder/operator with
  existing push rights, and separately authorize exact demo-API/source-job
  role deployment. No credentials, role/network/resource/data changes or
  live sign-in; #360 d/e remain UNMET and issue open.
* Original one-pass Review remains historical. Reviewer4536f9cc unavailable
  through agent messaging; new exact candidate SHA and retained finding boundary
  are supplied in PR #375, not falsely described as already reviewed.

* Completed broader retained workflow checks: API563 tests/OK with110 explicit
  skips (109 disposable SQL Server, one opt-in rendered browser); core546/OK
  with one isolated Azure SQL skip; orchestrator22/OK; branding migration25/OK
  after restoring its missing pinned dependencies. API initial wrong-cwd import
  errors resolved by using existing src/api workflow cwd, not source workarounds.
  JS syntax and pip check passed. These are local synthetic checks, not live
  staff/SQL/browser acceptance.

## [2026-10-17] delivery | PR #375 continuation rebased, tested and pushed

* Same #360 session, main51db4fa8 integrated; exact owner-authorized topic lease
  from662c11b to63aea6445bb89fe5a12064aa932a9df84fea85e9 verified by remote
  ref. Upstream helpers/tests/legacy delegate, #373/#374 artifacts and both
  knowledge histories retained. Final completion-only commit records stopped
  state; its exact head is supplied in PR #375, not claimed pre-reviewed.
* P04-T01/T02/T03/T04 complete. No extra critique/Review or delivery loop,
  no main rewrite/merge/issue closure and no live resource/credential/role/
  network/data writes. #360 d/e remain UNMET and open. Concrete blocker actions
  remain existing private-connected builder/operator and explicit exact IAM
  authorization, not generic image denial or a fabricated permission failure.

## [2026-10-17] delivery | PR #375 independent reuse-guard correction

* Independent Revise accepted: eligible untagged/unreferenced app-backed
  credential bypassed the requested Key Vault mode. Two new regression
  methods failed in11 subcases before source changes, including directory
  callback reconciliation before rejection. Original internal PC-001/no-defect
  assessment missed it; historical evidence retained with explicit correction.
* Actual selected generated/legacy candidate now checked before recording
  its store. Read-only pre-reconciliation uses the same expiry/selection
  implementation, before locks/directory writes; no incompatible reuse,
  rotation, migration or unrelated-secret loss. #374 helpers/tests/legacy
  and #373 source remain intact; pending digest verification stays read-only.
* Focused41, unchanged setup101 and full infra333/no skips passed. Existing
  lint/format/type, setup static/compile, pip and whitespace gates passed.
  Same-loop correction only; exact pushed head supplied in PR #375.
  Independent reviewer must verify before merge; Revise not self-overridden.
* IAM actions ["*"]/no exclusions is not demonstrated inability; activation
  unattempted pending explicit narrow-grant authorization. Docker socket
  denial actual, ACR Tasks/import not attempted or proven IAM-denied.
  No live writes or ready/login claim; restricted403 only, #360 d/e remain open.

* P05-T01/T02/T03 completion persisted after ordinary topic push of
  23db069a32618678a04bd8a0fa58d3d9ed723e99 and exact remote-ref readback.
  Final completion-only head reported in PR #375; stopped pending independent
  verification, no self-acceptance, extra loop, merge or issue closure.

## [2026-10-17] delivery | PR #375 integration after queue PR #376

* Owner-authorized topic rebase onto0bdcb2f0, no new phase or RPI/review loop.
  Both append-only KB histories retained byte-for-byte, both index routes
  retained; credential scripts/tests/runbook exact190391a and every other
  #376 file exact main. Correction1 evidence/hashes remain historical.
* Fresh focused41/setup101/full infra333/no skips and existing lint/format/
  static/compile/type/pip gates passed on integrationc187909. Exact final
  artifact-only head verified at topic/PR publication and posted in PR375.
  Authorized force-with-lease only on topic, expected prior190391a.
* Original finding remains open pending independent Pass on final head;
  reviewer4536f9cc's review of190391a is not presumed final-head acceptance.
  No cloud writes or merge; draft and human private-image, explicit narrow
  IAM authorization, tenant/live d/e prerequisites remain unchanged.

## [2026-10-17] ingest | Form schema and candidate staging foundation

* Refs #97. Added migrated core/API registry and candidate-only collection
  using existing JSON/SQL stores, checked shared documents, case row versions,
  document hashes/scans and audit. Updated component guides and index routing.
* Schema versions retain field type/unit/options, required/conditional,
  source-precedence/evidence policy and versioned template/rule references.
  Every version remains Unapproved; no actual form authority was supplied.
* Candidates retain raw spans/cells, source hash/version/date/locator and
  supplied parser/model/OCR lineage, with separate deterministic location
  verification. OCR route/pixel claims remain unverified; unreadable input
  has owned manual recovery. No AI/OCR invocation, acceptance or submission.
* #105's AI registry already exists; no parent hierarchy ordering gate or
  duplicate AI registry was introduced. PRD v0.12.0 exercise-planning acceptance
  is separate from actual form approval. Full AC-046/047/053, approved template
  binding, live SQL Server/Azure and #98 review/pack/staleness remain unmet.
  No private data, source snapshots, memory, original specification or
  concurrent infrastructure/credential/sensor sources were changed.

## [2026-10-17] query | Controlled administrative bulk preview (#78)

* Added the existing-workstream engineering continuation in
  `research/ux/zava-forward-prototype-profile-review.md` and its index route.
  Component API/core guides define the closed case-reason and existing
  handoff due/next-action contract, exact preview/outcome shapes and denials.
* Named owner/manager and existing note visibility remain mandatory. Fresh
  SQL staff/OID, target rowversion and guardrail checks occur under the writer
  lock; durable issuance/consumption and immutable provenance audit accompany
  local synthetic stale/replay/rollback/reopen tests. No controlled approval,
  ownership acceptance, resident commitment or hazard clock is changed.
* PRD FR-005/006/007 and same-number BRD entries have different meanings.
  Broader preexisting evidence-upload/handoff provenance is not certified by
  this bounded delivery. No new UI, human usability/WCAG, live Azure SQL,
  private-data, real-model or operational acceptance claim. Memory and the
  original case study remain unchanged.

## [2026-10-17] update | Bulk-preview correction ONE and exact provenance residual (#78)

* Updated the existing UX synthesis, index and component guides for PR #378
  correction ONE. RV-001 now refuses cached/persisted status-reset blocked
  issuance using immutable outcomes/failures and exact records/snapshot
  coverage; every issued target, including no-ops, is rechecked at SQL commit.
* Captured four real failing-before subtests; 71 focused synthetic bulk,
  loopback HTTP, handoff and document tests pass after correction. Core
  lint/format/type checks pass. Original RPI Review remains Not accepted,
  not rewritten as a Pass; independent correction assessment is separate.
* RV-002 is source-confirmed partial FR-005: upload and handoff offer/accept
  callers lack explicit source/version/reason contracts and complete
  per-change evidence/ownership provenance. Completing that input/history
  work affects existing UI/API behavior; no fake metadata or widened bulk
  authority is substituted. #78 is not fully accepted or closed.
* No UI source change, human/WCAG/browser acceptance, live SQL Server/cloud,
  private stock or real model. Original case and memory remain unchanged.

## [2026-10-17] update | Same-PR #78 integration after merged forms #97

* Owner-authorized rebase onto main92d4f89 retains both core/API guides,
  Store/projection/handler/inventory behavior, checked SQL documents and
  validators. Both complete KB histories and all index rows remain intact.
  Separate form/bulk modules and tests retain their respective upstream/
  old-publication content, including pending/missing-rescan durability fix.
* 110 joint focused forms/bulk core/API, role inventory, handoff/document
  tests pass; core ruff/format53/mypy106 and API ruff/format19/mypy49 pass.
  Synthetic rollback/reopen is not live SQL Server or human approval.
* RV-001 correction retained unchanged; RV-002 remains unfulfilled/blocking
  full criterion 1 / #78 acceptance. Actual schema authority is an unrelated
  human blocker. Original Not accepted Review preserved; active independent
  review requires exact final SHA/delta, no new review loop or Pass inferred.
  No merge, cloud/private/model use, memory or original-case change.

## [2026-10-17] update | Implement existing upload and handoff provenance (#78 correction TWO)

* Owner explicitly requires RV-002 implementation after independent Revise,
  superseding residual-only treatment. Required user-supplied source,
  source-version and reason now flow through existing upload/offer/accept
  UI/API/store contracts; missing old payload metadata refuses actionably.
  Handoff history version rejects stale actions; recipient-only acceptance
  and the bulk closed allowlist remain unchanged.
* Document/handoff histories and identical immutable audit events bind exact
  old/new document references/ownership, registered actor, UTC time and
  server change version. SQL commits together and rechecks current actor;
  failures restore staged state. No filenames/hashes/defaults invent source
  versions or reasons; old historical records stay unknown, not backfilled.
* Updated existing synthesis/index and component guides. Local synthetic
  tests and Chromium cover exact retention/reopen/audit, permissions, stale/
  conflict/rollback, required-field focus and keyboard paths. Original
  reviews remain historical; coordinator final-head independent reassessment
  required. No full issue/PRD or human/WCAG/live acceptance inferred.
* Forms pending/missing-rescan and bulk RV-001 remain independent and covered.
  Actual approved schema authority is a separate human prerequisite, not
  a provenance implementation blocker. No cloud/private/model calls,
  unrelated workflow change, original-case or memory edit.

## [2026-10-17] delivery | #360 scoped initializer API-only IAM activation

* Started clean requested topic/worktree at latest main e065ecd2 after merged
  #375. Activated ordered RPI Research, Plan and Implement; one independent
  plan critique Pass and separate independent predeployment source review Pass.
  Final full-task Review is recorded separately with publication evidence.
* Exact owner boolean approval covers reviewed API read/restart and temporary
  staff-job lifecycle in ama, not tags/read + tags/write on the existing
  initializer job. Added includeResultRelay boolean default true, conditioning
  both relay resources; explicit false safely omits that unapproved grant.
  No new permission action, role design or operator lifecycle role created.
* Exact API-only preview: two Creates/94 same-group Ignore; deployment
  staff-iam-360-api-20261017 Succeeded. Existing init principal
  3830883a-f4af-44f8-bff8-8859b78fc2f8 receives only four reviewed API actions
  at ca-cutover-test-demo-api. Role/assignment/actions/scope read back; AcrPull
  preserved; existing-job tag role/assignment absent, no old-API assignment.
* Azure canonicalized the role definition URI to subscription-level while
  retaining ama-only assignableScopes and exact API assignment. Initial
  verification assertions were corrected for that URI and expected identity
  Read, without redeployment, broad fallback or fabricated permission denial.
* Existing identity11 and compiled guard48 tests passed, plus Bicep build/lint
  and scoped Ruff/format. Restored declared dependencies only after missing
  import/tool failures. Updated runbook/evidence/index; historical #375 and
  prior log entries retained.
* No Graph/SQL/vault secret read, restart/job execution/browser acceptance,
  image build, network change/new infrastructure/spend/deletion. Demo deny-all
  and both APIs' observed metadata unchanged; ama/old stack preserved.
  Private publisher and exact relay approval remain blocked; #360 d/e UNMET.

* Subsequent independent full-task RPI Review completed once: no implementation
  defects; bounded verdict Conformant with justified divergence, three Medium
  wider-delivery residuals for relay approval, publisher and human acceptance.
  Parent retains overall Residual work/d/e UNMET; publication follows without
  another Review, runtime execution, child delivery loop or merge.

* Published main [PR #379](https://github.com/jmservera/ama/pull/379) on
  chore/activate-scoped-initializer-360; implementation/phase evidence
  4bf12775ca4025a15cd2c196547fc047375fd6e1 matched local/origin/PR head.
  Privacy-safe author/committer and required trailer verified. Session stops
  at exact documented outcome per owner; evidence-only completion follows.
  No merge/forcepush/issue closure or remote CI acceptance claim.

## [2026-10-17] delivery | #360 explicitly approved existing-job relay delta

* Prior publication verified complete: clean local/origin/OPEN main PR #379
  at38e6abf. New owner boolean true permits only initializer MI encrypted-result
  tags/read and tags/write on existing job-cutover-test-init. No plaintext,
  job-config/new-workload/broader-scope approval. Updated scoped plan/details
  as P04; original full RPI/Review remain historical, no new full loop.
* Reviewed source unchanged; actual toggle includeResultRelay=true (caller
  named includeResultTagRelay, not an existing parameter). Fresh preview
  Succeeded with two exact relay Creates and95 same-group Ignore/NoChange.
  Raw API assignment Modify retained: exact principal reference/canonical
  role URI only, principalType NoEffect. Whole before/after normalization and
  independent actual prior-role/assignment match prove API unchanged, not
  an arbitrary Modify allowance or falsely clean raw two-row preview.
* staff-iam-360-relay-20261017 Succeeded, correlation
  53c578e1-bea0-4655-a9ff-ce574b995d6b. Separate ARM readback verified role
  64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c, assignment
  8e9a497e-3b90-50e2-a783-93e58755165b, principal
  3830883a-f4af-44f8-bff8-8859b78fc2f8, two tag actions only, ama-only
  assignableScopes and exact existing-job assignment scope. Only new MI
  assignment is relay; existing API role/assignment and AcrPull exact.
* ARM labels idempotent API/empty-guard PUT operations Create; no new effective
  API grant or workload resource. Existing job identity/environment and both
  APIs' observed environment/revision/ingress metadata unchanged; deny-all retained.
  Prior RV-001 resolved for permission configuration only; RBAC is not an
  encrypted-content filter. No tag payload read/write/test or runtime proof.
* No secret/Graph/SQL reads/writes, temporary job/config/run, restart, image
  build, network/new infrastructure/spend/deletion or browser acceptance.
  Private publisher and genuine tenant/runtime acceptance remain unproven;
  #360 d/e UNMET. Targeted final-state review completed inline with no defects,
  explicitly labelled after the original independent full Review. One normal
  final topic commit/push is the terminal publication action, verified
  externally without an extra receipt commit; no merge or unrelated work.

## [2026-10-17] delivery | #360 authorized integration after merged #97/#78

* Rebased existing PR #379 topic onto latest main
  bf98977ed6b30176b1f2d0a0a1e91a80d273a742 by explicit owner direction.
  Both complete append-only KB histories and every upstream/topic index row
  retained. Core/API trees exactly main; scoped Bicep option, guard,
  runbook/evidence pack and actual approved API/relay receipts exacta51fef2.
* Owner reports independent Pass on bounded a51fef2, not the new final head.
  Rebased candidate00cafd0 passed59 scoped identity/compiled-Bicep tests,
  scoped template/guard build+lint and preservation/link/diff checks.
  No unrelated suite or live Azure operation/new grant; no acceptance inferred.
* One integration-receipt commit and authorized exact-lease topic-only push;
  final head/run reported externally, no follow-up receipt commits. Ordinary
  existing Source projects CI may be dispatched on topic if automatic checks
  are absent. Missing CI is not Pass; paid rubric not dispatched.
* Final exact-head independent review still required. Private publisher and
  genuine tenant/browser/runtime evidence remain unproven, #360 d/e UNMET;
  owner live approvals, ama/old-stack retention unchanged. No merge/autoclose.

## [2026-10-17] query | Constructed iteration manifest and criterion audit (#103)

* Audited exact #103 criteria, current PRD v0.17.0 FR-035/AC-043,
  BRD v0.18.0 CON-007, prior scenario/IA manifests and closed #174 registry
  at main bf98977. Dependencies none; #100 is hierarchy, not a dependency.
* Versioned existing scenario metadata to v0.2.0: all eleven profiles/nine
  workflows accounted for, with explicit required paths, safe endpoints or
  owned unknowns. Full journeys are unavailable in this offline iteration;
  removed unsupported blanket deferral claims without claiming APIs absent.
* Retained existing tiny three-case recipe and partial IA check provenance,
  with source hashes and exact ordered role/profile defaults. Shared core
  validation and destructive mutations enforce identity, status, binding,
  defaults and source restrictions through existing core CI discovery.
* Reviewed all thirteen public metadata inventory rows, bumped inventory to
  v1.3.0/date and clarified SN-11; owner review stays pending and coverage
  partial. Updated existing synthesis, provenance display label, core guide
  and index. Reused #174 evaluation registry unchanged; Git is iteration history.
* One Programme Manager research scope refinement is not owner ratification.
  No new people/home dataset, private/support/stock read, regeneration,
  runtime/UI behavior, billable AI, SQL/cloud service, operational approval
  or human/browser acceptance is claimed.

## [2026-10-17] query | #103 correction ONE retains proposed journey authority

* Independent reviewer fa457455 returned Revise against 7c3c6a7, relayed by
  the caller: manifest v0.2.0 incorrectly called PRD-proposed journeys
  approved. PRD Users and Personas describes provisional roles; the Profile
  Journey Contract describes proposed constructed walkthroughs, not confirmed
  company staffing, delegated authority or customer/owner approval.
* Corrected owned active attribution in manifest v0.2.1, validator messages,
  research and phase details; updated existing synthesis/index/core guide and
  manifest display references. Retained original critique/Review verdicts as
  history with explicit correction notices and a pending finding disposition.
* Added structured inventory-authority metadata separate from coverage.
  One mutation test first failed for five unsupported authority promotions;
  the guard now rejects promotions, missing metadata and substituted sources.
  Nineteen focused scenario/inventory tests and scoped lint/format/types pass.
* Exactly eleven profile/nine workflow entries remain; all twenty full journeys
  unavailable, no approved deferrals invented. No new data, private read,
  cloud/model use, merge or scope expansion. Implementation correction does not
  establish independent Pass; final exact-head independent review is required.

## [2026-10-17] delivery | #360 normal-Docker private publication follow-up

* Normal Docker Server29.9.0 and docker group membership verified without
  elevation; historical socket blocker resolved after owner update. Existing
  private ACR publicDisabled/bypassNone/adminFalse unchanged. Host DNS resolves
  login publicly to51.143.208.3/HTTPS403; this is not an AcrPush denial.
* Existing private endpoint NIC and private DNS zone agree on login10.40.4.21
  and UK South data10.40.4.20. Exact-IP HTTPS probes with normal TLS/no proxy/no
  credentials each time out at10seconds; no TLS connection or permitted private
  route demonstrated. No authenticated login/base pull/build/push/pin attempted
  over public routing, no Tasks/import/pool/VM/role/network workaround.
* Native local network-disabled scratch/COPY-only context audit exposed two
  directory-wide ignore exceptions including unrelated scripts/generated pyc.
  Removed only !scripts/ and !entra/, retained explicit file exceptions and
  Dockerfile/base/nonroot contract. Existing context test extended with unwanted
  script/.env/pyc/private-profile/data exclusions. Final native audit lists
  exactly seven intended files. Audit containers never started; both exact
  audit container/image objects and task-owned test scratch cleaned.
* Final focused source suite83passed/0skips; five network-forbidden source
  imports and two isolated source-help checks pass. Missing distributions
  restored only in task-owned venv after actual missing-package failure.
  These are not real-image smoke or no-secrets/runtime certification.
* Two read-visible job settings fingerprints match; old proof digest,
  Manual initialize args, identity, registry/env/config/template preserved.
  Existing demo deny-all retained. No SQL/private data/secret/Graph access,
  initialization/jobstart/restart, IAM/resource/network changes, new spend,
  retirement or image-pin idempotency claim. No new published tag/digest.
* [Runbook](../../infra/README.md#normal-docker-private-publication-follow-up-2026-10-17-360),
  [evidence](../architecture/cutover-evidence-pack.md#normal-docker-private-publication-follow-up-2026-10-17)
  and index distinguish actual current route blocker from historical Docker/IAM
  boundaries. Full ordered RPI artifacts/phase evidence retained; publication
  remains Blocked pending an existing authorized private-connected publisher.
  Genuine browser/roles/SQL/AI and #360 d/e remain UNMET; no inferred approval.

## [2026-10-17] delivery | #360 authorized PR #381 main integration

* Owner authorized rebase from a606258 onto main
  adedf1f232e567d3a22a623d9c871513fa6b7cdc after #380. Rebased candidate
  e31a1ae5705287f92729b031fedbc280324afce7 retains both complete KB index row
  sets and append histories. All fifteen other upstream files, including
  constructed manifests/source/tests, exactly main. Docker ignore/test/recipe
  exactly prior a606258; only additive index/log conflicts resolved.
* Minimal existing context test passed through stdlib-only class extraction;
  native network-none scratch/COPY Docker audit confirms exact seven context
  files, no container start/base pull/registry request. Initial audit assertion
  counted generated runtime files outside /context; corrected harness scope and
  reran successfully, no source fix. Exact owned audit objects cleaned.
  Diff/preservation checks passed; no full suite, dependency install or venv
  restoration. Prior venv was already removed, not deleted during this review.
* Independent reviewer463ad179 assesses olda606258, not this final integration
  head. Final exact-head follow-up required and notified externally on PR #381;
  no fabricated Pass/new full review. One privacy-safe integration-record commit,
  topic-only exact-lease push and external head/CI verification; ordinary Source
  CI only if checks absent, no paid rubric dispatch or receipt-only commit.
* No repeated private ACR probe, public-access workaround, cloud/network/IAM
  writes or workload/private-data access. Existing10.40.4.20/.21 timeouts remain
  concrete evidence; image publication/pin and #360 d/e UNMET. Stop final push,
  no merge or automatic child work.

## [2026-10-17] query | #84 current-authority and failed-decision engineering continuation

* Verified exact four issue criteria against PRD FR-012/013 and BRD FR-037/
  AC-065/RULE-017, current modules and constructed baseline tests. Comparisons,
  independent versioned sign-offs, affected-only reassessment and Unknown
  support with other ranking factors were already delivered; none replaced.
* Reproduced revoked SQL actor approval and failed-write success-audit gaps.
  Added a bounded stock/technical decision scope using existing current-staff
  validation, writer transaction and discard mechanisms. No policy weights,
  role grants, new source authority, procurement/capacity or infrastructure/
  package changes.
* Eight selected canonical cases passed on a task-owned local SQL Server 2022
  container: all decision successes, stale/removed/changed-OID actors,
  independent pre-save authority change, case/audit rollback, reopen and no
  later success-audit flush. Component guides, existing synthesis and index
  updated. JSON's separate-file durability boundary remains explicit.
* No private/cohort/real-map reads, real cloud, paid model, inferred health,
  actual professional delegation, source-policy/legal approval or new human
  accessibility acceptance. Broader nomination/self-referral belongs to #130;
  this evidence does not close #84 or establish full BRD AC-065 acceptance.

## [2026-10-17] query | #84 Review blocks failed-recovery acceptance

* The one independent post-implementation Review completed with outcome
  Not accepted. RV-001 High is an in-scope blocker: early `_discard` read failure
  can leave a failed success audit for outer cleanup, while persistent failure
  can mask the original save error. The existing recovery-fault test performs
  successful discard before raising and does not cover those cases.
* Four original issue mechanisms and current-authority checks remain separately
  evidenced; passing normal-recovery suites do not resolve the blocker.
  Updated current component/synthesis/index status to prevent a successful
  acceptance claim. No source correction, second Review, issue closure or
  operational approval; any visibility PR is explicitly incomplete.

## [2026-10-17] query | #84 correction ONE contains failed recovery before reload

* Coordinator explicitly authorized RV-001 correction on existing PR #382.
  Original Review and Not accepted outcome retained; no repeated full RPI.
  New actual recovery SELECT fault test failed all six one-shot/persistent
  technical/comparison/terminal subcases before source edits. A second
  transactional GateError/ConflictError fault test failed both cases before
  the additional scoped refusal-path change.
* Canonical SQL discard clears pending audit/writes/validation first, restores
  known case/recommendation/shared-document snapshots and invalidates sync
  watermark before fallible reads. Stock/technical refusal cleanup remains
  with its existing decision scope, preserving original exception/logged
  uncertainty even if reload fails; next operation retries, never succeeds
  on dirty cached state.
* Ten actual local SQL Server tests, 102 focused core/gate tests, 69 direct
  shared-cleanup-consumer tests and 72 targeted API tests (one opt-in browser
  skip) pass; core/API lint/format/types pass. Owned loopback SQL container
  removed; no other task container touched, new dependency, private/cloud/model
  use, authority/policy change or broad lock/architecture rewrite.
* Bounded independent correction verification closes RV-001 for the exact
  fingerprinted source/test content: 91 focused tests and two constructed
  persistent-recovery snapshot probes pass. Original adverse Review retained,
  no repeated full RPI. No merge, issue closure or human/operational approval.

## [2026-10-17] engineering | #94 exact record-only finance controls

* Audited exact issue, PRD FR-018 and current BRD references against finance
  helpers, API/screens and SQL transaction prior art. BRD FR-018/RULE-003 now
  describe handoff/hazard controls; stale finance numbering is explicitly
  preserved as a conflict, not silently corrected in source requirements.
* Finance emits actual line indices for all match exceptions, refuses ambiguous
  commitments, rechecks current matching at acceptance and uses current named
  staff with email/code/OID independence. Caught JSON failure recovery and SQL
  staged-audit rollback preserve prior state; no payment adapter or authority
  model added. Status notes leave budget/commitment/grant cash unchanged.
* Updated the existing [Finance journey synthesis](./research/ux/customer-journeys/finance.md#exact-finance-control-audit-2026-10-17-94),
  core/API guides and index. Focused fixture/API and isolated local SQL Server
  checks cover unknowns, holds, independent people, reopen, rollback, fresh rights
  and concurrent writers. Initial MSSQL cleanup failed on pooled connections;
  corrected exact owned-database cleanup, then 14 cases passed.
* #93 is parent hierarchy only; no explicit dependencies. One actual shared
  SqlStore.save validation hook may overlap #90; no shared Store/server or #84
  signoff change. No private data, real provider/financial commitment, payment,
  paid AI or Azure activity. No browser/WCAG, real delegation, full PRD or
  operational acceptance claim. Original and memory unchanged.

## [2026-10-17] correction | #94 persistent JSON recovery audit

* The one independent Review found a blocking persistent os.replace case:
  recovery save could fail before success-audit rollback. Coordinator correction
  ONE added failing-first primitive-level proof, then decoupled ledger rollback
  from the second state write. A failed restoration now explicitly reports an
  uncertain durable outcome and requires persisted readback, never success.
* Fifty-five focused JSON/SQLite/existing-finance/authenticated-HTTP cases and
  scoped Ruff/format/mypy passed afterward. Prior fourteen local SQL Server
  cases retain their original boundary; SQL is unchanged by the JSON correction.
  Updated the existing Finance synthesis and core guide. Original Review remains
  Complete / Not accepted for the assessed pre-correction candidate, with
  separate objective resolving evidence; no repeated full Review or invented
  independent pass. One of two authorized coordinator corrections used.

## [2026-10-17] correction | #94 SQL recovery audit, coordinator cycle TWO

* External exact-852b342 coordinator verdict Revise identified false success
  audit after SQL audit INSERT failure plus first discard SELECT failure.
  Three SQLite regressions reproduced original-error masking before the fix.
  Canonical cleanup now quarantines failed audit/touched/validation state before
  fallible I/O, restores snapshots and invalidates sync state for healthy reload.
  Finance retains its prior legitimate audit prefix. Save-refusal/lock-exit
  recovery preserves original exceptions with explicit notes and error logs.
* Passed 158 combined finance/HTTP/shared-SQL/role/provenance/bulk regressions
  plus one added internal-save-refusal test. Actual isolated local SQL Server
  passed 18 finance cases plus that added case. New checks prove early/persistent
  recovery failure, rollback/reopen, no false approval, prior audit retention,
  lock release and healthy subsequent approval/chain. Scoped Ruff/format/mypy
  and documentation checks recorded in the dated execution artifacts.
* Updated existing Finance synthesis, index and component guides. Actual
  `_discard` overlap with #84 / PR #382 requires coordinator integration
  sequencing; no foreign dirty-worktree read, cherry-pick, rebase or merge.
  Both authorized corrections are used. Original single RPI Review and JSON
  correction ONE retained; no repeated full Review or independent Pass claimed.
  External coordinator closure remains pending. Fictional local fixtures only,
  no private data/cloud/payment activity; original and memory unchanged.

## [2026-10-17] integration | #94 on merged assessment main bbbc924

* Explicit coordinator authorization rebased only the clean run-owned finance
  topic from published 54ed445 onto main bbbc924, which contains merged #84 /
  PR #382. Reconciled canonical discard/save conflicts, retaining cleanup before
  reads, committed case/recommendation/document snapshots, watermark reset,
  stock-scoped actor/refusal ownership and finance pending-prefix/original-error
  logging. Provenance/bulk/stock/finance/safety transaction checks all remain;
  no duplicate helper, test removal or procurement/workflow source change.
* Upstream log is exact byte prefix followed by finance's entries; both task
  routes, guides and upstream synthesis retained. Original/memory and original
  adverse Review unchanged. One combined test invocation needed src/api on the
  path for upstream tests.test_mvp; corrected remaining invocation passed.
  Total 232 local passes and one existing opt-in browser skip. Actual isolated
  local SQL Server passed 19 finance and 18 stock/procurement/workflow cases;
  exact owned container/database cleanup only. Scoped lint/format/types pass
  after restoring the missing declared API dev Playwright package, no browser
  download or browser acceptance claim.
* Existing RPI evidence records base/head, conflict choices and commands. Both
  original corrections retained; no new full RPI Review or independent Pass.
  Topic publication uses explicit expected-remote lease only; no main write,
  merge, issue closure, private data/cloud/payment or automatic child work.
  External coordinator independent closure remains next.

## [2026-10-17] implementation | #90 evidenced capacity and controlled orders

* Audited actual migrated procurement/controller/JSON/SQL paths against the
  exact four criteria, PRD FR-016 and BRD RULE-007/008. Parent #89 is hierarchy,
  not an explicit dependency. A procurement-manager research instrument
  reviewed scope without pretending to supply live company authority.
* Reproduced eight failing JSON/SQLite cases before fixes. Bound positive
  commitments to original bytes/hash/version, review/delivery dates, covered
  homes, home-order units and explicit trusted named delegation; unknown and
  offered capacity cannot authorize work or alternate case advancement.
* Retained existing SQL locks/CAS and added commit-time dependency checks.
  Versioned every successful order mutation, preserved immutable issuer
  snapshots, explicit non-instruction drafts and own-only contractor reads.
  No self-granting endpoint or production delegation seed was introduced.
* Updated existing component guides, synthesis and index. Local fictional
  JSON/SQLite/SQL Server and browser checks are engineering evidence only;
  actual delegations, supplier commitments, Azure, human/screen-reader/WCAG
  acceptance remain unestablished. No private data, cloud/paid AI, live order,
  award, payment, merge or real financial commitment occurred.

## [2026-10-17] correction | #90 coordinator Revise and hosted regressions

* Coordinator Review of integrated PR #384 head 527a537 returned Revise.
  Required contract/call-off version before package creation, with omitted,
  empty and whitespace-only domain/API denials before mutation; the existing
  UI retains inputs, announces the inline error and focuses the version.
  No new editor, delegation grant, redesign or production authority.
* Refreshed only dataset.py's exact SHA-256 in the existing #103 scenario
  manifest after intentional fictional fixture-helper changes. Eleven
  profiles/nine workflows remain unavailable, product roles provisional,
  journeys proposed and actual approval not established. Validator unchanged.
* Corrected JSON/SQLite safety-flow positives with explicitly fictional source,
  trusted delegation and booked work order after independent safety release.
  Original raiser/receiver/release independence and blocked-advance assertions
  remain, with no skip or weakened production capacity guard.
* Original independent Review remains historical Conformant evidence, separate
  from coordinator Revise and this correction; external exact-head closure
  remains required. No real data, live instruction, Azure/paid AI, financial
  commitment, professional approval, issue closure or merge is claimed.
* Correction validation: core full CI discovery 651 run/one existing skip;
  API full CI/MVP discovery 613 run/142 existing opt-in skips; separate actual
  local SQL Server procurement domain/API 31 pass and local browser validation
  pass. Counts overlap. Configured lint/format/types, strict browser harness,
  JS/compilation/diff checks pass. No test/validator weakened or skip added.

## [2026-10-17] delivery | #360 renewed actual az acr initializer publication

* Corrected the prior private-publisher-only inference with an actual hosted
  CLI experiment on retained source bab4bf3 (#381). Read-only run dbb proves
  historical ordinary cpu2 success on 2026-10-16, not current publication.
* Normal Docker retained-base build failed on manifest HEAD firewall403.
  The actual corrected hosted command uploaded 20.157 KiB, queued ordinary
  cpu2 QuickRun dbc and downloaded source; agent registry login then failed
  `/v2/`403. Failed run, no output image/build/push/digest/pin. Initial
  Dockerfile-path error was local, corrected and preserved separately.
* Exact native CLI archive contains seven unique intended regular paths, all
  hashes equal committed source, plus identical duplicate Dockerfile member.
  Retained base, upstream pinned/security-upgrade source and #375/#379/#381
  implementation unchanged. Full read-visible job projection matches before/
  after; registry public Disabled/bypass None preserved.
* Actual current-source localhost fixture smoke: welcome/health200, anonymous
  protected endpoints401, one fictional case/zero staff, AI off/no SQL. This
  is NOT actual image, tenant sign-in or deployed-runtime proof. Focused
  infra suite83passed/0skips after worktree-local pip dependency recovery.
* Updated [current runbook](../../infra/README.md#renewed-initializer-acr-cli-attempt-2026-10-17-360),
  [evidence pack](../architecture/cutover-evidence-pack.md#renewed-initializer-acr-cli-attempt-2026-10-17)
  and index without rewriting earlier observations/logs. Dated ordered RPI
  research/plan/details/critique/changes/receipt/review records accompany PR.
  Only authorized source upload/failed QuickRun, no workload/network/IAM/
  infrastructure/secret/private-data/Graph/SQL/restart/jobstart/retirement.
  Exact hosted-digest image validation remains blocked; #360 d/e UNMET.

## [2026-10-17] delivery | #360 PR385 integration and read-only registry403 diagnosis

* Coordinator explicitly authorized clean topic60134c5 integration onto fresh
  origin/main bbbc9243505b606550327c64bf5429243f457f2e. Only append-log
  conflict, resolved with exact upstream prefix then complete own append;
  both #84 upstream routing/history and #360 routing retained. No source
  mutation. Intermediate integration6311b51 is not tested source; actual
  dbc receipt/sourcebab4bf3/payload/base hashes and original single Review
  Complete/Residual work preserved byte-identically. External final-head gate
  forthcoming, not a new Pass or repeated full RPI.
* Bounded read-only comparison found both runs QuickRun Linux/amd64/cpu2,
  no named task/pool. Original deployment record says images captured before
  registry isolation; ARM metadata shows registry write13:56:53 after dbb's
  13:53:24 October16 success. Strongly supported likely isolation explanation,
  not proof of exact changed property or daemon identity/RBAC denial.
* Current publicDisabled/bypassNone/LegacyRegistryPermissions retained;
  task-specific bypass property absent in preview GET, not literal false.
  Microsoft documents default SAMI bypass denial, separate from generic trusted
  services; applicability to exact QuickRun token not proven. Current tasks/
  pools/ama VMs empty, externally owned private runners unknown. Pool billing/
  region limits, including UK South absent from preview list, remain explicit.
* [Runbook diagnosis/options](../../infra/README.md#initializer-registry403-read-only-diagnosis-2026-10-17-360),
  [integration evidence](../architecture/cutover-evidence-pack.md#read-only-registry403-root-diagnosis-and-pr385-integration),
  existing research/changes and current index updated. Preferred later owner
  choice identifies an existing private publisher; new costed pool or task-bypass
  exception requires separate specific approval, not blanket IAM/public access.
* No new Azure writes/builds, log payload/SAS/secret/actor/identity-detail
  retrieval, initializer update/start, SQL/Graph/private data, restart or
  teardown. Actual exact-image smoke/digest/pin and #360 d/e remain UNMET.

## [2026-10-17] query | Safe setup API selection during retained migration (Refs #360)

* New ordered setup-api-selection-360 RPI on PR #385 found the actual demo API
  has legacy `workload=api` plus explicit `zava-forward-ingress=direct`, but no
  modern role tag. Old API retains workload-only metadata. Read-only selected
  ARM fields, not names or list order, establish the existing selector.
* [Setup runbook](../../infra/README.md#post-deployment-api-authentication-initialization)
  and script now accept the compatible legacy direct tag combination. Exact
  old-API override remains supported; mixed modern/legacy direct candidates
  refuse ambiguity. Single legacy/Front Door path remains unchanged.
* Corrected active transport guidance: `--check`, `--dry-run` and `--list-staff`
  now refuse temporary Azure job/secret writes before request payload creation,
  including automatic fallback. Local read-only verification remains; failed
  private connectivity reports blocked/incomplete, not verified SQL. Mutation-mode
  Azure preflight/roster/apply transport remains separately scoped.
* Existing runbook and index updated; new phase evidence records red-first and
  offline regressions. No live setup, private SQL/Graph writes, image smoke/pin,
  restart, public access/bypass/IAM/new infrastructure or retirement. Prior ACR
  historical receipts and Review remain unchanged; actual #360 d/e unmet.

## [2026-10-17] delivery | #360 setup selection offline Review and publication

* New setup RPI has one independent critique, three resolved findings, 164
  passing setup/staff/legacy regressions and scoped lint/format/types/compile.
  Its one independent Review is Complete / Residual work: bounded source
  conformant, no defects, no correction used. No runtime acceptance implied.
* PR #385 now includes the narrow selector/no-cloud-write guard and dated
  evidence, integrated onto finance main d400eb8 with exact upstream log prefix,
  all owned append entries and #84/#94/#360 routes retained. Eight prior ACR
  artifacts/receipt/Review remain byte-identical; historical bab4bf3 build
  source is not relabeled as new reviewed setup source f48cc9b.
* No Azure write during this continuation. Private-publisher authority decision,
  exact-image smoke/pin, real operator sign-in/roles/SQL/AI and later retirement
  remain open. External final-head gate/owner merge decision pending; no closure.
## [2026-10-17] query | Grant lifecycle and scoped human exercise authority (#95)

* Fresh issue/source audit verified existing grant states and second approver,
  but tiny JSON/SQLite probes accepted unregistered role dictionaries and a
  same-code alias. Current BRD grant rules are FR-023/024 and RULE-009/010;
  the issue's BRD FR-019 reference now concerns capacity.
* Updated the Finance journey synthesis, KB index and core/API guides. Reused
  #94's operation recovery/SQL hook and independent email/code/OID helpers for
  grant and application writes. Explicit trusted human exercise designation
  matches exact target/action/case/scheme or route and fresh UTC validity;
  role alone, request metadata and production exercise use cannot authorize.
* Kept application, award, claimable, submission and cash evidence separate
  from provider finance; per-event amounts do not inherit the GBP 40 million
  opportunity. GBP-only refusal, retained actor/designation/source history and
  legacy unknown-currency withdrawal/re-proposal avoid fabricated provenance.
  Application confirmation wording now explicitly means neither award nor cash.
* Focused local grant/finance/API/browser run passed 89 tests without skips.
  Actual isolated loopback SQL Server passed 15 grant and 19 preserved finance
  cases; both task-owned containers and their UUID databases were removed.
  Full API discovery passed 588 tests with 121 explicit skips; core discovery
  exposed two stale manifest hash checks, fixed with the actual test-source
  SHA-256 and all eight manifest checks passing. DATA AST and journey coverage
  remain unchanged; final broad rerun and independent gate are recorded in task
  evidence, not inferred here. Existing Ruff/format/core/API types pass.
* No private stock/roster, continuing dataset alteration, real authority,
  financial execution, paid inference or Azure writes. Original case and owner
  memory unchanged. Synthetic engineering and focused browser evidence are not
  full PRD pack/export, WCAG, human or deployed-application acceptance.

## [2026-10-17] correction | Grant legacy transaction identity (#95)

* The single independent Review executed Complete / Not accepted. RV-001 found
  a regression freezing legacy preparer identity before transaction validation.
  Original verdict is retained; this is not a human permission blocker.
* Authorized correction ONE restores original unresolved-versus-captured
  identity provenance in #94's validation context. Legacy grants and finance
  budgets reread current persisted preparer identity inside the SQL transaction;
  captured historical identity and current actor/designation gates stay intact.
  Four grant/finance x code/OID subtests failed before correction and now refuse
  with unchanged case/audit, cleared validation context and valid audit chain.
* Updated existing Finance synthesis, index and core contract. Current combined
  grant/finance/API/actual Chromium/manifest checks pass 98 tests without skips;
  actual isolated loopback SQL Server passes 16 grant and 19 preserved finance
  tests. Owned container zf-grant95-74996418b02e and UUID databases removed.
  Core/API Ruff, format and types pass. Earlier full discovery remains dated
  pre-correction evidence; local closure is not an independent Pass.
* Coordinator final independent gate remains pending. No second Review, real
  delegation, payments, private data, cloud actions or continuing-data changes.

## [2026-10-17] integration | Grant controls on latest main (#95)

* After completed ordered RPI, correction ONE and PR #386 publication, explicit
  coordinator authorization rebased only this topic onto fetched main
  1fc7325b93ea845b9cb2e827efbea624f7d20d30 (#385 and #384).
* Preserved upstream exact log prefix, all index routes and both shared-source
  intents. Only manual conflicts were this append-only log and the manifest's
  fixture digest, regenerated from combined public source. Entire own 12-file
  src added/removed byte patch parity proved across bases; no authority,
  coverage or approval metadata promotion. Original case/addendum unchanged.
* Fresh 156 grant/finance/procurement/API/actual Chromium/manifest tests pass;
  core/API Ruff/format/types pass. SQL 35/35 and prior full discovery remain
  historical correction evidence, not new integration runs. Original adverse
  Review retained; coordinator independent closure pending. No new full Review,
  private data, financial/cloud action, main write, merge or issue closure.

## [2026-10-17] correction | #85 current hazard evidence and persistence

* Audited existing source/awareness, separate sent/receipt/acceptance, sender
  follow-up, home hold/restart evidence and visible external response/update
  times. Preserved authoritative hazard-service categorisation, clocks,
  resident updates and closure; no communications or automatic release added.
* Reproduced and corrected unregistered/stale actor recording, case-only
  self-release and failed-save success audit. Current caller/destination checks
  repeat inside existing SQL writer transaction; retained email/code/OID
  identities enforce independent retrofit-only decisions. Failed staged SQL
  state/audit is quarantined before recovery, preserving prior audit and errors.
* Canonical JSON/SQLite tests and actual task-owned loopback SQL Server exercise
  cover authority changes, release/audit rollback and recovery-read faults.
  JSON separate-file post-save audit failure explicitly reports uncertainty,
  not fictional rollback. No quality/finance source, shared fixture recipe,
  scenario manifest, regulatory snapshot or UI edits were needed.
* Updated existing component guides, hazard synthesis and index. BRD hazard
  anchors are FR-003/RULE-003; older FR-015 issue pointer now refers to tenure.
  Actual operational delegation, release/timing/escalation policy, verified
  service receipt, Azure/model/human/WCAG acceptance remain unestablished.
  No private stock/rosters, live instruction, legal activation, paid AI,
  external resident communication or cloud change occurred.

## [2026-10-17] correction ONE | #85 retained adverse Review and post-commit audit

* One independent Review returned Complete / Not accepted for RV-001 High:
  post-commit synchronization failure replayed an already-committed prior audit.
  Both one-shot and persistent failures reproduced before correction.
* Authorized correction ONE records acknowledged SQL COMMIT in the hazard
  scope. Later synchronization failure reloads without replay, retains the
  original error and explicitly warns that evidence committed. Existing
  uncommitted rollback/quarantine and all shared validators remain.
* Canonical SQLite and actual task-owned loopback SQL Server assertions cover
  a second writer, committed release, exactly-once prior/release audit and
  explicit warnings. Parent correction evidence is not independent closure;
  original adverse Review and final-head acceptance limitation are retained.
  No new UI, service authority, regulatory change or operational approval.

## [2026-10-17] integration | Hazard controls on latest main (#85)

* After correction ONE and draft PR #388 publication, coordinator authorization
  rebased the owned topic from base b5d4c840 onto fetched main
  2b24456863c0a8f39d47a73e22daeff3875cc825, including merged PR #385/#386.
* Only manual conflict was this append-only log. Upstream exact byte prefix and
  all other index routes retained. Entire production/test binary patch remains
  byte-identical across bases; component documentation auto-merges preserve
  both intents. No duplicate grant fix or shared recovery redesign.
* Upstream grant/finance/store, neutral UI, fixture and exact manifest remain
  byte-unchanged, with no authority promotion. Fresh 25 SQLite/manifest tests
  pass; six added documentation links/anchors and retained Review hash verified.
  Original actual MSSQL/full/static evidence remains historical, not newly run
  integration parity. Independent final-head closure remains coordinator work.

## [2026-10-17] delivery | Per-measure quality and handover controls #91

* Executed all ordered RPI phases' preparation: fresh issue/requirements and
  current actor/transaction audit, real fail-before probes, plan and one
  independent critique. Existing stepwise flow was verified rather than
  replaced. Critique's original Revise is retained; compatible legacy
  multi-record retirement and exact regression ownership findings were applied.
* Current registered staff now authorize quality writes under the existing SQL
  decision scope. Retained contributor identities prevent original/earlier-fixer
  or name/email/code/OID alias self-acceptance. Explicit remediation evidence
  and independent reinspection are required. No new competence or risk policy.
* Same-measure replacement invalidates every prior active acceptance/handover
  and retains history/aftercare as superseded evidence. Independent new acceptance
  and resident handover remain separate. Contractor writes stay denied and no
  quality action changes finance/grants or executes payment.
* Updated existing core/API guides, programme journey synthesis and index
  without changing upstream routes/log prefix. No finance.py, dataset fixture,
  app.js, server.py, shared manifest or SQL persistence helper edit was needed;
  #84 stock, #94 finance and #90 capacity/scheduling checks remain.
* Actual tiny-fictional local JSON/SQLite/HTTP, isolated local SQL Server and
  real Chromium evidence are recorded separately from competent-human, Azure
  SQL, screen-reader, resident and WCAG acceptance, which are not claimed.
  No private data, cloud/paid AI, live order, financial commitment or merge.

## [2026-10-17] delivery | #91 independent Review and authorized correction ONE

* The one independent Review executed Complete, original outcome Not accepted.
  RV-001 reproduced known earlier legacy FIXED recorder resolution failure;
  RV-002 reproduced committed refresh failure replaying a legitimate audit prefix.
  The original verdict is retained, not overwritten by a claimed second Pass.
* Canonical fail-before tests reproduced both. Historical recorders now enter
  conservative staff lookup; earlier aliases remain excluded. Confirmed own
  committed snapshots are identified before shared recovery, preserving exactly
  one committed decision/prefix and surfacing explicit committed/reload guidance.
* The #95 shared overlap is only the sequenced two-line server.py quality-outcome
  handler returning HTTP 503 with outcome=committed. No grants/finance dispatch,
  finance.py, app.js, dataset, manifest or SQL persistence helper changes.
* Latest local selection: 361 run, 312 passed, 49 existing opt-in skips.
  Actual isolated SQL Server: 38 passed; exact owned container removed.
  Actual Chromium exercised committed-refresh failure/reload as well as the
  full quality/replacement journey; configured engineering gates passed.
  Human, Azure, resident, screen-reader and full WCAG acceptance remain unclaimed.

## [2026-10-17] integration | #91 onto merged grant controls and initializer base

* Coordinator authorized latest-main topic rebase after correction publication.
  Exact base 2b24456863c0a8f39d47a73e22daeff3875cc825 includes PR386/#95
  and PR385. Prior head d322235641487ff2c4dea1e4339c99f973b7f75d rebased
  to tested candidate c0f67838383007c3f4a95ba0aa957378e2db0ba5.
* Four documentation insertion conflicts retain all upstream routes and exact
  complete log prefix, with #91 entries appended; both component sections kept.
  Whole own production/test patch byte parity proven. No new grant/finance
  correction, shared recovery redesign, fixture/manifest or authority change.
* Preserved merged #95 current legacy-preparer transaction revalidation on grant
  AND finance, scoped synthetic designation, shared finance operation, funding
  history and neutral UI. Original #91 single Review and correction evidence
  retained verbatim. Original case unchanged.
* Fresh combined local tests: 206 run, 205 pass, one existing grant-browser skip.
  Actual unique loopback SQL Server replay: 83 pass, zero skip; exact owned
  container removed. Configured checks and document links passed. Earlier
  broader/browser receipts are historical; no new independent Pass, Azure,
  human-authority, screen-reader or WCAG claim, main write, merge or issue closure.

## [2026-10-17] integration | #91 preserves merged hazard commit-boundary controls

* Coordinator authorized own-topic rebase onto verified latest main
  1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c (PR388/#85), from reviewed
  topic 210b89df0d287675cb8ac5148dd9d198d37dd9c1. Exact upstream log byte
  prefix and all routes/quality histories retained; only log insertion conflicted.
* Hazard writer validation and per-operation marker immediately after COMMIT
  remain alongside stock/finance/procurement validation. Quality retains its own
  committed snapshot/outcome and no-prefix-replay behavior. No production change,
  shared recovery redesign, duplicate hazard/grant correction or authority change.
* Combined run exposed a copied test record with unknown Synthetic recorder;
  quality correctly refused before the intended hazard race. The test-only
  precondition now names existing fictional Sam with independent Pam, preserving
  all hazard-at-commit refusal/no-false-audit assertions. Quality regression also
  asserts next healthy save leaves audit/state unchanged after committed failure.
  Dataset/manifest/original case unchanged; no identity guard weakened.
* Tested candidate 48b90f42fe8170f3f17956e3a194a0c93b33eee2: fresh local
  243 run/241 pass/two existing skips; actual task-owned local MSSQL 99 run/
  98 pass/one existing JSON-only skip. Both one-shot/persistent post-COMMIT
  prior-prefix paths exercised; configured gates and integrity checks passed.
  Exact owned container removed; source fingerprints recorded for coordinator
  external review 42ce6748. Original adverse Reviews unchanged; no independent
  Pass, Azure, human/WCAG acceptance, merge or issue closure claimed.

## [2026-10-17] correction | #91 current-version quality assistant evidence

* Coordinator exact-210b89df external Review returned Revise / Medium for
  downstream assistant counting/exposing Superseded evidence as current.
  Authorized correction TWO followed completed post388 publication; original
  single RPI Review/correction ONE and external adverse disposition retained.
* Two fail-before canonical assistant tests reproduced false discrepancy and
  stale historical-source reliance. Shared quality selector now excludes only
  explicit Superseded, never hiding duplicate active candidates. Capture,
  discrepancy and proposal contributor review use current evidence only;
  scalar evidence_version participates in source signatures. Same-content
  replacement stales prior proposals, historical-only changes do not.
* Pending/defective/unknown/missing evidence and malformed active duplicates
  remain gaps. No proposal review writes quality acceptance or grants new AI
  authority. No shared persistence/hazard/finance/grant/stock/provider hook,
  dataset/manifest or original case change.
* Exact full core CI discovery: 788 run, 751 pass, 37 existing skips. Focused
  assistant/dispatch/quality/hazard/HTTP: 206 run, 156 pass, 50 opt-in or
  JSON-only skips; five exact targets including prior hosted hazard failure
  passed. Configured Ruff/format/mypy pass. No new MSSQL/browser replay for
  consumer-only change; prior actual SQL/browser evidence remains historical.
  External final-head/artifact gate remains pending, no self-regraded Pass.

## [2026-10-17] engineering | Historical progress controls (#102)

* Added a read-only progress mode to existing stats and CSV paths, reusing
  authorized current-record cohort filters and preserving default responses.
  Exact structured return/reopen/handoff events supply only observed clocks;
  missing, legacy, malformed and contradictory history remains unresolved.
  No narrative/snapshot reconstruction or audit/event rewriting.
* Declared EXA-009 scenarios show independent pools, assumptions, sensitivity
  uncertainty and data limits. Forecast is not a target, approved plan,
  professional decision, promise, accepted outcome or validated resource plan.
  No new AI/provider or inference of AI absence; approvals/consent unchanged.
* Shared report/export contract retains UTC as-of/period, definitions, sources,
  current cohort/filter impact, denominators and exceptions without raw private
  actor/source/note/commercial fields. Updated component guides, programme
  synthesis and index; all upstream routing and log entries retained.
* Local fictional JSON/SQLite and actual uniquely named loopback Docker MSSQL
  checks plus non-root API image behavior provide bounded engineering evidence.
  Complete forward-event capture, ledger anchoring, verified operational
  capacity, human/WCAG/Azure/AI acceptance and coordinator closure remain open.
  PRD/BRD FR-022/023/024 numbering contradiction is disclosed, not silently
  resolved. No #91/#92 domain edits or other-worktree/private-data reads.

## [2026-10-17] correction ONE | Historical progress malformed inputs (#102)

* Retained the original Complete / Defects found Review unchanged. Failing-first
  tests reproduced blank query fallback and UTC conversion overflow. One
  bounded correction now rejects empty/repeated report fields without changing
  default stats/CSV and surfaces unrepresentable event times as unknown.
* Final focused 88 and actual task-owned loopback MSSQL eight tests passed;
  core/API lint/format/mypy passed. Corrected non-root image checked exact
  installed source hashes, hardening, authenticated report/export parity,
  clocks/scenario and both defects' HTTP 400 paths.
* No second full Review, Correction TWO, independent coordinator Pass, merge
  or full historical/operational approval. Own local containers stopped and
  retained without deletion; complete event capture/resources remain open.

## [2026-10-17] correction TWO | Mixed-precision handoff history (#102)

* Coordinator's independent exact-28227fa8 Revise / Medium identified a reachable
  precise offer/accept surrounding minute-truncated receipt. Failing-first
  actual writer/SQLite and pure probes reproduced version reordering and false
  chain/date contradictions. Original full RPI Review and correction ONE remain
  intact; no second full Review or independent self-Pass.
* Preserve append/version lifecycle sequence and exact source locators. Known
  legacy minute spelling or corroborated second-zero expansion supplies time
  bounds, never reconstructed seconds. Affected durations and ambiguous
  as-of/start membership remain explicitly unresolved. Precise backward dates,
  invalid versions, identities and lifecycle errors remain contradictions.
  Only prospective handoff timestamps use precise UTC via the existing helper;
  other clocks and all persisted history/audit remain unchanged.
* Authorized own-topic integration onto main 3f544fb9 retains quality #387
  active-record selection, current evidence-version staleness, post-COMMIT
  guards and all finance/grant/stock/procurement hooks. All upstream routes and
  the entire upstream log byte prefix are retained. No other worktree read.
* Final focused 76 pass; combined 547 run / 494 pass / 53 explicit existing
  opt-in or backend-specific skips; ten current actual loopback MSSQL cases
  pass. Core/API configured lint/format/types and final rebuilt hardened
  non-root API/source hashes/legacy-prospective HTTP/export checks pass.
  These are targeted engineering results, not coordinator acceptance.
* First/final forward-stage clocks and accepted-handover actual events remain
  incomplete, so the first historical criterion is not fully proved.
  Prospective complete capture is buildable separate engineering follow-up,
  not a human blocker; forecasts still lack verified operational inputs.
  No browser/WCAG, human, Azure, real AI or outcome acceptance is claimed.

## [2026-10-17] query | Resource-bound setup profile contracts (Refs #360)

* Corrected the automatic setup runbook and existing index route: a bound
  profile-neutral app patch cannot imply production merely because the
  deployment parameters omit profile fields. The actual exported ARM template
  contract controls literal defaults; full main's production default still
  vetoes development, even alongside development module tags.
* Official ARM deployment metadata, template export and parameter-default
  documentation checked 2026-10-17 and linked in infra/README.md. Unknown,
  malformed/null, contradictory, failed or unreadable bound evidence remains
  fail-closed; development plus dev/test/demo evidence is still mandatory.
* Reproduced coordinator-reported three-deployment shape before the source fix
  and passed it afterward, including a fake read-only roster preview. Fresh
  baseline was 104 setup plus 43 staff_azure tests; expanded setup suite passes
  117 tests, preserving admin selection, seeded distinct users, Key Vault and
  private/read-only restrictions. No live setup, Graph write, SQL, temporary
  cloud job, tag spoofing, public-service change or Azure deployment occurred.
* Live credential and initializer-publication 403 gates and #360 d/e remain
  unmet. Source parsing acceptance is not tenant/browser/SQL/AI acceptance or
  permission to retire Front Door or delete resource group ama.

## [2026-10-17] query | Authorized profile-evidence integration (#360)

* Coordinator authorized own PR391 topic rebase from cea89c43 onto freshly
  fetched main 3f544fb9 (#387), with exact expected-old-remote lease only.
  Only log insertion conflicted; complete upstream byte prefix plus original
  own entry retained, all upstream routes preserved.
* Infra source/test added-and-removed binary patch is byte-identical across
  bases. Original critique and single Review unchanged; all merged src,
  including quality assistant and recovery, exactly equal the new main base.
  No source correction, new full Review or self-declared coordinator Pass.
* Fresh installed-distribution complete setup/staff/auth/secret suite: 200
  passed. Configured lint/format, changed-line lint, syntax and diff checks
  pass. Ordinary CI publication/status recorded separately; absent checks
  are not green and no paid rubric scoring is dispatched.
* No main/other-worktree write, cloud mutation, Graph, SQL or live setup.
  ACR403/private publisher and actual tenant/browser/SQL/AI remain unmet;
  no merge, issue closure, service exposure change or full-setup-ready claim.

## [2026-10-17] query | Coordinator profile correction ONE (#360)

* Independent coordinator exact-9561938a assessment returned Revise for two
  Medium defects: mixed-case /Providers/ rejected valid bound ARM identity,
  and malformed schema/resource envelopes could be classified neutral.
* Both independent reproductions failed on unchanged source (four invalid
  envelope acceptances and one valid-ID rejection). Correction structurally
  validates exact subscription/ama/provider/type/name paths case-insensitively
  and validates the supported resource-group ARM envelope before classification.
* Supported resource arrays and languageVersion 2.0 symbolic resources require
  typed resource entries. Unknown schemas/languages, malformed entries and
  unsupported nested deployment parameter/default contracts explicitly refuse;
  schema validity does not prove development. Official syntax/schema sources
  checked 2026-10-17 and linked in the setup runbook.
* Expanded installed-distribution setup/staff/auth/secret suites: 206 pass,
  including six added correction methods with table cases. Original critique
  and Review unchanged; separate correction disposition retains Revise and
  does not claim coordinator Pass. Fresh main advanced to 22670277; no new
  rebase authorized or attempted.
* No live setup, private inputs, Graph, SQL, Azure/IAM/network/tag changes,
  paid rubric dispatch, merge or issue closure. Private publisher ACR403 and
  actual tenant/browser/SQL/AI acceptance remain unmet.

## [2026-10-17] query | Sensor privacy boundary actual-source audit (#112)

* Exact upstream prefix: `74617981b71bc3f10bd21d0b78691bc3cf36c473`.
  Read actual #112 criteria before treating stale Not started or historical
  references as delivery. Parent #109 is hierarchy only, no issue dependency.
* Existing runtime has an offline generator/loader, not implemented IoT
  ingestion, sensor_analysis or a registered sensor AI purpose. The existing
  sensor research synthesis now distinguishes that fact from ADR proposals.
* Loader verifies exact current-generator manifest/payload replay before SQL,
  then loads private replay-owned bytes. Stock mode requires original explicit
  Selection; labels, pseudonymization, filenames, rehashing and unverified
  approval-looking metadata do not establish synthetic origin. Computational
  budget bounds replay; supported tiny fixtures and idempotency are retained.
* Closed chat-home context prevents recursive diagnostics export; malformed
  selected legacy AI/citation/map fields refuse without value echo. Existing
  manual detail, static tiles/license/manual alternative and domain approvals
  are unchanged. No service hold, health threshold or real-use grant added.
* Failing-first sentinel regressions reproduced actual assembled chat leakage,
  malformed map/AI exposure and unverified loader admission. Focused corrected
  tests and actual task-owned loopback SQL establish construction/refusal
  boundaries, not legal/privacy conformance or operational acceptance.
* #175 unresolved external origins remain unverified. OD-43 inventory,
  lawful basis/DPIA, retention, resident choice, thresholds and competent
  approval remain open. No private dataset, Azure/IoT/Graph/IAM, paid inference,
  real contact, deployment, merge or issue closure was performed.

## [2026-10-17] query | Sensor privacy correction ONE (#112)

* The one original Review completed with Not accepted and two High findings:
  RV-001 raw reason/hazard owner stringification before chat/briefing export;
  RV-002 document metadata validation after outbound AI dispatch. The original
  Review and critique remain unchanged, not replaced by a second Pass.
* Correction ONE validates raw status contributors at the external boundary,
  and document metadata/citation inputs before AI dispatch and read-route
  scan/audit interpolation. Manual case status/detail, domain state, lawful
  approval boundaries and document-content paths remain unchanged.
* Two new test methods reproduced six failures before correction. Corrected
  focused core selection: 145 run, 144 pass, one opt-in SQL skip; agents:
  94 pass; focused API AI/chat: 86 pass. Configured Ruff/format/mypy pass
  for all three components. No weakened assertion or removed test; sixteen
  new methods remain within the planned eighteen-method limit.
* Earlier actual task-owned loopback MSSQL admission pass and cleanup remain
  evidence for unchanged persistence/admission; SQL was not restarted for
  prompt-only correction. Full core's earlier exit137 remains incomplete.
  No paid inference, web change, new deployment or operational/legal approval.
  Final-head independent acceptance remains coordinator-owned.

## [2026-10-17] implementation | #88 resident commitments and separate remedy clocks

* Reused resident_update, service_requests and existing resident endpoint/panel.
  Full commitments have purpose, current named owner, timezone-aware due date
  and supplied basis; handoffs preserve them rather than creating partial pairs.
  Commitments are not messages or evidence of receipt/understanding.
* Response and remedy have independent owner/date/version/history. Closing a
  response, completing a work order, handover, financial note or case reopen/
  return never closes another open remedy, defect or charge query. Legacy absent
  provenance stays Unknown until explicit present-responsibility confirmation;
  no historical owner/date or completion is fabricated.
* Existing SQL transaction rechecks current registry, ownership, inputs/version
  and record state. Actual owned loopback SQL negative-writer/audit/recovery
  probes, JSON/SQLite, authenticated HTTP and real local browser support this
  bounded criterion audit; committed acknowledgements never claim rollback.
* Preserved all prior KB routes and exact upstream log prefix from main
  1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c. Updated existing resident synthesis
  and component guides, not memory, regulatory snapshots or original case.
  Shared sqlstore/store/API overlap is declared for coordinator integration.
  #92 held source and other worktrees were not read or imported.
* No real resident/service/legal authority, communication, payment, paid model
  call, new IAM/Azure/public access or private dataset use. Full PRD lease/
  scope/age-band governance, direct human/WCAG acceptance and independent
  final-head coordinator closure remain unestablished.

## [2026-10-17] integration | #88 onto merged quality PR387

* Coordinator authorized own-topic rebase from exact remote
  a9a5f554151336f6e617fbcee35033234813c6e5 onto fetched main
  3f544fb9cda2c51b219db2cc8368c7525bbe0c86. Sole textual conflict
  was this log's append insertion: complete upstream byte prefix and all own
  entries retained; all index routes and both component contracts survive.
* Exact issue88 added/removed src patch lines across fourteen files are
  unchanged. Auto-merged server preserves separate resident committed 409 and
  quality committed 503 handling; resident tests retain upstream replacement
  refusal. Quality/assistant current-active selector and evidence-version
  staleness, hazard/stock and finance/grant hooks remain intact.
* All seven original RPI artifacts, including original Review/critique/state,
  are byte-identical. No new full Review or source correction. Original Review
  Complete / Residual work remains; RV-001 wider governance routing belongs
  to planning parent/repository owner at next #81 backlog triage, not an
  unproven remedy criterion or fabricated Legal/Housing/Complaints approval.
* Fresh combined installed-src tests: 499 run, 445 pass, 54 existing opt-in/
  JSON-only skips. Actual isolated loopback MSSQL: 38 run, 37 pass, one
  SQLite-only trace skip; original assertions retained. Actual integrated
  resident browser journey and configured core/API Ruff/format/mypy pass.
  First SQL transport-harness errors and their correction are recorded honestly
  in separate integration evidence, not hidden as application source fixes.
* No other worktree/private data, Azure writes, paid AI, resident messages,
  independent coordinator Pass, merge, issue closure or full PRD/WCAG acceptance.

## [2026-10-17] integration | #88 onto partial progress PR390

* Coordinator authorized own-topic rebase from clean verified remote
  a91f1737d036141169b5ba5381429cf3e49054cf onto freshly fetched
  main226702779e57e490cb10dc06ab014760c7d8a761. Documentation-only
  insertion conflicts retain complete upstream byte prefix plus all own log
  entries, both component contracts and all index routes.
* Exact own added/removed production/test/guide lines across fourteen src paths
  are unchanged. Progress implementation/tests/API configuration are exact main;
  resident/safety/quality/financial persistence guards and web bytes unchanged.
  Auto-merged Store/server/workflows preserve report/export role/source checks,
  precise UTC handoff writer timestamps and authoritative event sequence,
  alongside separate resident commitments/remedies and truthful commit outcomes.
* Fresh focused combined report/resident/handoff/quality/hazard/finance/grant
  checks:140run,138pass,two existing skips (JSON rollback inapplicable
  in SQLite, opt-in browser). Actual MSSQL classes were not selected.
  Full configured core/API Ruff/format/mypy pass. No new SQL/Docker/browser
  replay for documentation-only conflict plus exact source parity; previous
  receipts remain historical, not promoted to fresh validation.
* Original Review/critique and prior issue88 RPI/integration artifacts unchanged.
  No new full Review, application correction, complete event capture, private
  data, other worktree, Azure/paid AI, authority, independent Pass, merge,
  issue closure or WCAG acceptance. Full capture stays with issue102events;
  wider governance retains its separate named routing owner/next action.

## [2026-10-17] integration | #88 onto setup391 main

* Coordinator authorized own-topic rebase from clean exact remote
  cfeb18598ba8ae84cb8b80c0c7623e375ae886fe onto fetched main
  74617981b71bc3f10bd21d0b78691bc3cf36c473. Only KB log append
  conflict; exact upstream prefix plus all own entries and all routes retained.
* Entire src tree byte-identical to prior tested topic; exact fourteen-file
  own added/removed patch parity. Setup391 classifier, negative tests and guide
  byte-identical to upstream. Original Review/critique and previous issue88
  RPI/integration evidence unchanged, no new full Review or source correction.
* Fresh focused resident core/API:65run,63pass,two existing skips (JSON-only
  rollback in SQLite, opt-in browser). No full SQL/Docker/browser or infra
  replay for doc-only base conflict plus source fingerprints; prior evidence
  remains historical. No independent Pass, cloud/private writes, authority,
  full event capture, merge, issue closure or WCAG acceptance.

### 2026-10-17: Issue88 authorized response-owner recovery correction ONE

* Coordinator's Medium finding exposed departed response owners stranding update,
  close and reopen. Existing resident records/API/panel now support explicit
  manager-only versioned service/redress reassignment with current named assignee,
  reason and old/new identity/actor/time history. Remedy responsibility and all
  independent clocks remain separate; legacy absent provenance stays unknown.
* Updated existing core/API guides, resident criterion audit and retained index
  route. Fresh resident/browser/handoff/report selectors: 145 run, 134 pass,
  11 existing skips; targeted actual owned loopback MSSQL: eight pass, no skips.
  Configured core/API Ruff/format/mypy and JavaScript syntax passed.
* Interrupted broader replay has no completed result and is not reported green.
  Original Review/critique retained unchanged; no second full Review, operational
  authority, messaging, cloud/private writes or WCAG acceptance. Coordinator owns
  independent final-head acceptance; broader governance remains separately routed.

### 2026-10-17: Issue88 final authorized responsibility-clock correction TWO

* Coordinator f786737f identified email-collision status ownership after departed-
  owner recovery. Status clock now follows responsibility: redress for Closed/
  Independent review, otherwise service. Reassigning the non-owning responsibility
  preserves status owner/date even when one person holds both roles; missing legacy
  provenance is not fabricated. Remedy and captured history remain independent.
* Existing core/API guides and resident synthesis/index updated. Actual failing-
  first matrix produced eight failed subcases on JSON/SQLite; corrected matrix
  covers 24 route/state/responsibility/legacy subcases on each backend including
  actual MSSQL. Fresh resident core/API:74run,72pass,two existing skips; targeted
  actual loopback MSSQL:nine pass/no skips; configured core/API Ruff/format/mypy pass.
* No web bytes changed or fresh browser/JS execution claimed. Original Review/
  critique and correction ONE evidence retained unchanged; final independent
  disposition remains with coordinator. No new full Review, third correction,
  authority, communications, private/cloud writes, merge or issue closure.

### 2026-10-17: Issue88 authorized sensor-main integration

* Own PR392 rebased onto committed main943febc2 (sensor PR393) with explicit
  expected-topic-head authorization. Sole textual conflict was KB log append;
  complete sensor prefix followed by all resident entries retained, with boundary
  newline repaired after strict suffix proof. All index routes retained.
* Exact resident production/test added/removed patch parity across fourteen src
  paths; shared Store/core guide also retain exact sensor delta. Every nonoverlap
  sensor src file and all prior resident RPI Review/critique/correction artifacts
  unchanged. No third defect correction, new full Review or unmerged #394 source.
* Fresh combined resident/sensor/status/document/chat/map selectors:240run237pass/
  three existing skips; agents94pass; explicit API boundary selectors100pass.
  Counts overlap, not unique totals. Core/agents/API Ruff/format/mypy pass.
* No persistence/web semantics conflict, so no repeated SQL/browser/image run;
  prior nine actual resident MSSQL and sensor SQL receipts remain historical.
  No cloud/private/paid-model/contact/authority writes, merge, issue closure,
  independent self-Pass or WCAG acceptance. Coordinator owns final disposition.

## 2026-10-17 Engineering - #102 prospective controlled event capture

* Distinct follow-up to merged #390 at main2267027 for the remaining timestamped
  history criterion. Preserve the entire upstream index/log byte prefix and
  original Review; forecasts and export-provenance criteria stay unchanged.
* Extend existing stage/return/reopen, handoff and quality history dictionaries
  at their actual controlled writers. Registered actor, owner, source/version,
  precise UTC and authoritative append versions supply prospective evidence;
  no past record or prior audit is reconstructed or edited.
* Update [core](../../src/core/README.md#historical-progress-evidence-and-declared-forecasts-102),
  [API](../../src/api/README.md#historical-progress-report-and-export-102),
  [programme journey](./research/ux/customer-journeys/programme.md#prospective-progress-capture-continuation-2026-10-17-102)
  and the appended current routing section. Quality acceptance/handover pairs
  stay per evidence version and historical as-of; whole-home actuals remain
  unknown. Independent controls, legacy minute bounds and forecast limits stay.
* Actual-domain fictional JSON/SQLite/task-owned loopback SQL Server checks
  cover successful capture, rollback/retry, failed recovery with preserved prior
  audit, second-connection/restart and committed-refresh exact-once semantics.
  JSON case/event replacement is atomic, not its separate audit across crashes.
* quality.py history/acceptance/handover paths overlap parallel #88 and require
  coordinator integration. No server/web/finance/infra or other-worktree edits,
  operational approval, real authority, private data, Azure or paid AI.
  One original Review and independent final-head acceptance remain separate.
* Resumed the interrupted single Review after the VM upgrade; retained its two
  Medium findings and adverse outcome. Concrete correction ONE makes earlier
  waits unknown when a contradictory later handoff state is observed and
  verifies exact event/audit counts for committed refresh failure/retry/restart,
  including actual return/pause exit/reopen. Fresh targeted457 run/394 pass/
  63 explicit skips; actual own MSSQL25 pass; corrected non-root image48 run/
  47 pass/one skip plus source hashes/startup/negative probes; configured static
  checks pass. These are engineering receipts, not coordinator acceptance.
* Owner-authorized one-time own-branch integration onto main74617981 retained
  the exact complete source/test patch and full upstream index/log byte
  prefixes. Post-integration26 JSON/SQLite checks passed. Published main
  PR #394, Refs #102; independent final-head acceptance, merge and the remaining
  issue checkbox stay coordinator/owner-owned. No other branch was rewritten.
* At22:28 owner authorized own-topic integration onto merged sensor #393,
  main943febc2, with exact old-remote92c3bae3 lease. Union Store imports retain
  sensor pre-dispatch validations and progress event/recovery writers; both
  core README sections, full upstream index/log prefixes and own entries stay.
  Nonshared files/shared deltas verified, combined301 run/274 pass/27 explicit
  skips and core/API/agents statics pass. No persistence change or SQL restart;
  prior SQL25 evidence historical. Original adverse Review/correction ONE
  unchanged; PR #394 independent final gate and issue #102 remain open.
* Independent final-head review of PR #394 at7fda223a verified its original
  findings closed but found one Medium operational failure-audit regression.
  Correction TWO (last authorized cycle) restores sanitized failure/rejection
  after rollback, retains original errors and prior audit, and never replays
  success or rejects committed outcomes. Original Review/critique/correction
  ONE unchanged. Before new resident-main integration: complete core876 run/
  820 pass/56 skips, actual own MSSQL29 pass, focused213 run/200 pass/13 skips;
  static and hardened installed-image94 run/92 pass/two skips checks pass.
  No private payload in failure evidence, paid AI or approval implied.
* During correction validation main advanced to merged resident #392 atbcb4871b.
  Authorized own rebase retained resident and change-provenance SQL recovery
  guards and exact twelve-file own delta, complete upstream KB prefixes and
  both resident/sensor intents. FINAL full core942 run/847 pass/95 skips,
  combined349 run/294 pass/55 skips, actual integrated MSSQL35 pass, final
  hardened image94 run/92 pass/two skips and core/API statics pass.
  Owned SQL stopped. Original Review/critique/correction ONE unchanged.
  PR #394 remains independent-final-gate work, not a third defect cycle,
  self-Pass, approval, merge or issue closure.

## 2026-10-17 Engineering - #101 coordinator heatmap and lifecycle funnel

* Research actual checked-out list/map/filter/role/event contracts at base
  ebc8dab8, which includes merged event102/PR394, resident88/PR392 and sensor112/
  PR393. Parent100 is hierarchy only; the earlier indexed search missed existing
  web surfaces and did not justify a new dashboard framework.
* Add the scoped read-only [coordinator workbench/API](../../src/api/README.md#coordinator-heatmap-and-lifecycle-funnel-101)
  and [shared current population contract](../../src/core/README.md#read-only-coordinator-populations-101).
  Existing filters/own-all scope, current stop rules, policy draft status,
  validated timestamped partial events and map cluster/field controls are reused.
  Source stage and observed metric-stage selectors remain independent.
* Update the [existing programme synthesis](./research/ux/customer-journeys/programme.md#coordinator-population-and-observed-funnel-boundary-2026-10-17-101)
  and index. Missing groups/geocodes/history remain visible; list/map population
  totals include unmapped records, while mapped viewport counts stay separate.
  No fictional initial entry/final exit, lifecycle exclusion, conversion,
  accepted handover, ranking authority or independent acceptance.
* Preserve all Store/document/provenance writers and issue117's orchestrator/
  doc_controls paths. KB index/log are declared overlap; retain both topics'
  append-only entries on any later separately authorized integration.
  No memory edit, other-worktree read, private stock, tile-provider/licence
  change, Azure, paid AI, live communication or approval operation.

## 2026-10-17 Review - #101 original adverse outcome and publication gate

* Exactly one original Review completed with Defects found, retained in
  [the dated Review](../../.copilot-tracking/reviews/logs/2026-10-17/coordinator-lifecycle-funnel-101-review.md).
  RV-001 Medium: mixed-case registered staff email authenticates and reads cases,
  but the new coordinator registry lookup falsely denies it on JSON/SQLite.
  Passing synthetic browser/SQL/image receipts do not close this counterexample.
* Publication/completed delivery is blocked under the accepted correctness gate.
  Route the minimal identity lookup/regression correction to later selected
  implementation, preserve the original verdict and do not repeat Review.
  No issue closure, independent coordinator acceptance, push or PR is claimed.

## 2026-10-17 Correction ONE - #101 registered staff lookup

* Coordinator authorized the bounded RV-001 correction in the same original
  session/worktree/topic. Normalize only the coordinator lookup key using the
  existing lowercase staff index; retain exact current email/code/role checks.
  No Store/document/provenance writer,117 runtime, web or ranking changes.
* Four failing-first JSON/SQLite direct and actual HTTP tests reproduced the
  denial, then passed. Coordinator modules49 run/41 pass/eight skips; final
  core plus identity30 pass, real mixed-case Chromium1 pass, configured static
  gates and rebuilt hardened installed-source image checks pass.
  Actual MSSQL remains historical for this pure lookup change; no fresh SQL
  claim or backend query/refresh/authorization contract change.
* Preserve original Review Complete/Defects found and critique Revise byte-exact.
  Separate focused correction receipts resolve the engineering counterexample,
  not independent coordinator/WCAG acceptance or issue closure. No second Review.
  All denominator/hold/priority/coverage and same-filter map/list/funnel definitions
  remain unchanged; unsupported lifecycle exclusions stay explicitly Unknown.

## 2026-10-17 - Bounded pending-document rescan invocation (Refs #117)

* Research current src and merged PR270 evidence on the authorized merged102
  base. Add a bounded SQL orchestrator invocation using the existing scanner,
  factory and optimistic writer; no daemon, Azure timer or scanner activation.
* Record stable pages and non-deleting unavailable bad verdicts, explicit
  synthetic-local opt-in, safe incomplete/failure/committed outcomes and
  actual owned loopback SQL race/retry/prior-audit/commit-boundary evidence in
  the [existing synthesis](./research/retrofit-synthetic-data/README.md#pending-document-rescan-engineering-boundary-2026-10-17-refs-117),
  [core contract](../../src/core/README.md#bounded-pending-document-rescans-117)
  and [orchestrator guide](../../src/orchestrator/README.md#bounded-document-rescan-job-117).
* All 17 actual SQL rescan tests passed; real SQLite/MSSQL and hardened
  UID10001/read-only/drop-all/NoNewPrivs/no-network image commands persisted
  bounded 1/2/0 clean pages and exactly three success events with intact ledger,
  bytes and legal hold. Owned SQL stopped and removed. Existing document,
  progress, resident and sensor regression selections passed with opt-in
  skips reported separately.
* Preserve the original one-critique Revise verdict and directly applied
  findings. One original Review and external coordinator acceptance are
  separate from these implementation receipts. Real Defender/Blob enablement,
  recurring hosted schedule/cadence, approved retention triggers/periods,
  deletion/hold delegations and human approvals remain unmet. No private
  dataset, memory edit, web, paid service, real communication or live Azure.

## 2026-10-17 - Original rescan Review outcome and separate routing (Refs #117)

* The one original Review executed Complete / outcome Not accepted. Two
  Medium findings reproduce raw nested SQL recovery diagnostics and malformed
  scanner result report escape. Pending state remains unavailable in both
  repros; prior successful SQL/image receipts are not overwritten or promoted
  into overall acceptance.
* Reconcile the [existing synthesis](./research/retrofit-synthetic-data/README.md#pending-document-rescan-engineering-boundary-2026-10-17-refs-117),
  index and [job status](../../src/orchestrator/README.md#bounded-document-rescan-job-117).
  Route corrections separately; no production/test patch, repeat Review or
  independent coordinator Pass. Original critique Revise and original Review
  are retained. Real-service, schedule and human-authority gates remain open.

## 2026-10-17 - Draft rescan publication receipt (Refs #117)

* Publish [PR #395](https://github.com/jmservera/ama/pull/395) to main from the
  authorized branch, preserving the original Not accepted Review and both
  Medium correction routes. No source/test correction, second Review,
  independent coordinator Pass, merge or issue action.
* Fresh main stays `ebc8dab87ae9bd6a33380b85e86f38be5ed9f213`; source commit
  `4763c0e6337d06846d9a9c46f7d9e0cf7470079f` matches the published head.
  Owned SQL remains stopped/removed. Hosted checks are running, not presumed
  successful; Defender/scheduling and human approval gates remain unmet.

## 2026-10-18 - Authorized rescan correction ONE evidence (Refs #117)

* Coordinator authorizes both original Medium findings in one coherent cycle
  on the same branch/draft [PR #395](https://github.com/jmservera/ama/pull/395).
  Preserve original Review Complete / Not accepted and critique byte-exact;
  no second Review, self-Pass, merge or issue closure.
* Failing-first JSON/SQLite/actual CLI cases reproduce nested recovery private
  diagnostics, malformed-result escape and invalid container acceptance.
  Worker-owned SQL recovery now runs before automatic traceback emission;
  shared closed scanner-result shape/verdict/detail validation occurs before
  unpack/mutation. Explicit TypeError boundaries return safe truthful failures,
  preserving original conflict, winner, pending prefix and own-COMMIT distinction.
* All 19 actual SQL worker cases (including the prior17) plus 11 shared progress/
  resident recovery cases pass. Actual MSSQL CLI failure streams and rebuilt
  nonroot/read-only/drop-all/NoNewPrivs/no-network installed-image job prove
  unavailable failed records, retained bytes/hold, truthful counters, no private
  sentinel/traceback and exactly-once success. Exact owned SQL stopped/removed.
* Reconcile the [existing synthesis](./research/retrofit-synthetic-data/README.md#pending-document-rescan-engineering-boundary-2026-10-17-refs-117),
  index, [core contract](../../src/core/README.md#bounded-pending-document-rescans-117)
  and [job guide](../../src/orchestrator/README.md#bounded-document-rescan-job-117).
  Local regression/static evidence is targeted, not independent acceptance.
  Defender/Blob, hosted cadence and real retention/approval authority remain
  unmet; no private data, live Azure, paid activation, web or memory changes.

## 2026-10-18 - Final rescan correction TWO and authorized integration (Refs #117)

* Coordinator supplies independent558e33f1 Revise: original RV-001/RV-002
  independently closed, all seven artifact reconciliation passes; one new Medium
  unconditional optional MSSQL-driver import breaks dependency-minimal SQLite
  CI/help. Authorize this LAST source cycle and own-topic rebase onto merged
  PR #396 main f9d80724, with exact old-remote lease6a9fd3a4.
* Real no-site discovery fails first with22 passes/one import error. Load the
  driver error type only after explicit MSSQL selection inside the fixed error
  boundary. Final real driverless32 run/31 pass/one driver skip, module help
  and normal/failing SQLite CLI pass; no workflow or dependency install change.
* Actual owned SQL20/20 passes, including all19 worker guards and driver-error
  regression. A native invalid-table query before store return is sanitized.
  Rebuilt hardened installed-image help/six failure runs/real module success
  pages pass; exact SQL stopped/removed. Correction ONE30-SQL receipt remains
  historical. Combined coordinator/progress/resident/sensor/worker regressions
  and configured core/orchestrator checks pass with skips explicit.
* Preserve upstream source/browser routes byte-exact, issue runtime/test patch
  parity except two authorized CLI/test files, upstream log exact byte-prefix
  followed by both issue append histories, original Review/critique and
  correction ONE evidence unchanged. Reconcile [existing synthesis](./research/retrofit-synthetic-data/README.md#pending-document-rescan-engineering-boundary-2026-10-17-refs-117),
  index and [job guide](../../src/orchestrator/README.md#optional-driver-compatibility-correction-two-2026-10-18).
  No new full Review/self-Pass/merge/closure; draft PR #395 awaits coordinator.
  Defender, hosted schedule and real retention/approval authority remain unmet.

### 2026-10-18: Appointment commitment controls (#87), partial engineering boundary

* Extend the [existing resident journey](./research/ux/customer-journeys/residents.md#appointment-control-engineering-boundary-2026-10-18-87)
  with separate resident/staff/current-capacity appointment agreement, explicitly
  bounded representative authority, household options/pause/owner and minimal
  provider instructions. Preserve independent works consent and urgent safety.
* Record provisional strict-greater-than default 5, idempotent verified visits,
  human investigation checks and independent preference-breach/abortive cause/
  owner facts. Reporting thresholds remain Unknown; no automatic consequence.
* Source tracing found no authorized human underlying-home-case closure writer.
  Reset remains unavailable/fail-closed; no task completion is treated as case
  closure. Human closure/reset acceptance is not claimed. Update the index and
  [core](../../src/core/README.md#appointment-agreements-and-visit-evidence-87)/
  [API](../../src/api/README.md#appointment-control-api-and-manual-workbench-87)
  guides. Synthetic engineering is not ratified live policy, legal approval,
  resident validation or WCAG certification.

### 2026-10-18: Appointment human closure writer clarification (#87)

* Correct the preceding partial implementation boundary: PRD DD-006/AC-033,
  BRD RULE-006/AC-025 and addendum EXA-014 explicitly authorize recording a supplied
  human same-home-case closure/reset. Absence of a writer was an engineering seam,
  not absence of source permission. Preserve that earlier entry as history.
* Update the [resident journey](./research/ux/customer-journeys/residents.md#appointment-control-engineering-boundary-2026-10-18-87),
  index and [core](../../src/core/README.md#appointment-agreements-and-visit-evidence-87)/
  [API](../../src/api/README.md#appointment-control-api-and-manual-workbench-87)
  guides for the separate confirmed manual operation, current actor/authority,
  optimistic case version and explicit human source/version/reason. Closure
  atomically resets only the active count, retaining event/configuration and
  investigation history, consumed references, resident updates and remedies.
* No task/order/remedy completion or reopen implies reset. No general closure
  policy, technical handover, legal/financial approval, live service activation,
  resident validation or accessibility conformance is inferred.

### 2026-10-18: Appointment correction ONE (#87)

* Update the [resident appointment boundary](./research/ux/customer-journeys/residents.md#appointment-control-engineering-boundary-2026-10-18-87),
  index and component guides for seven original-Review corrections: truthful
  pre-header committed-response encoding, existing resident/reason-role privacy,
  atomic configuration evaluation of existing eligible active counts, bounded
  textual exact-scope competence, withdrawn Ended state, selected localized visit
  details and protected manual drafts with retained dependency references.
* Preserve explicit tri-party agreement, separate works consent, current capacity,
  same-case human-only closure/reset, consumed histories and outstanding updates.
  Configuration changes create no duplicate/reset task or automatic consequence.
  Original Review remains Not accepted; correction implementation and synthetic
  validation are not independent acceptance, live policy or WCAG certification.

## 2026-10-18: Issue #87 coupled public fixture digest correction

* Refresh only the `src/core/tests/dataset.py` source SHA-256 in the existing
  [scenario manifest](./research/retrofit-synthetic-data/scenario-manifest.json)
  after the supplied appointment fixture changed, and update the knowledge index.
* Retain version 0.2.1, the offline iteration, all twenty unavailable full
  journeys, partial IA provenance, exact fixture defaults and pending owner
  approval. Existing hash validation and negative mutation assertions are not
  weakened; the digest correction grants no new coverage or approval.

## [2026-10-18] query | Resource-specific chat isolation fixture coverage (#172)

* Update the [chat fixture dictionary](./research/retrofit-synthetic-data/data-dictionary.md#resource-specific-isolation-coverage-2026-10-18-172),
  [agents guide](../../src/agents/README.md#resource-specific-isolation-fixtures-172-2026-10-18)
  and index with current public-only evidence: 22 personas across eleven
  perspectives, but current assistant eligibility permits 14 thread owners
  across seven perspectives. The prior test included memory and was not failing.
* Add explicit denial expectations for both contractors as read/list/search
  actors against a legitimate active eligible staff-owned thread; no contractor
  eligibility or ownership is added. Removal and malformed-target regressions
  protect the coverage; existing synthetic-label/pattern canaries, lifecycle
  null content, opt-in/withdrawal and metadata-only ledger remain separate.
* Fresh generated manifests hash current bytes through existing tooling; no
  private input, frozen snapshot or unrelated source fingerprint is rewritten.
  Declarative expectations are not runtime enforcement. SN-08 remains partial,
  actual scope/volume approval unverified; ADR 0004 was accepted as written
  October 15 (#158/PR #279), while OD-45 to OD-49 remain open. No new policy,
  human approval, regulatory-currentness claim or whole-issue closure is implied.

## 2026-10-18: Finite design traceability and recorded review gate (#156)

* Extend the [existing prototype profile synthesis](./research/ux/zava-forward-prototype-profile-review.md#design-traceability-and-review-gate-2026-10-18-156)
  with eleven PRD profile rows and four declared shared core flows, linked to
  exact journey/task-flow sections, immutable historical prototype and shared
  IA versions, requirements/checks, status and missing-evidence owners/actions.
  Existing task flows and decisions correct a universal reading of the issue's
  historical absence claim; complete screen-backlog coverage remains unknown.
* Consolidate the actual 2026-10-15 owner Fluent 2 choice, reported recovery
  needs and source-qualified sequencing/IA interpretations. Record live #150
  CLOSED separately from the pinned partial-foundation scope and stale
  "stays open" sentence; no full Fluent or human acceptance is inferred.
* Add accessibility/content definition-of-done links and an actual dated
  automated evidence review, not an invented human design review. Current
  screen designs, named review, resident-wording approval and direct user
  research remain Not supplied; the overall design gate is Blocked. No UI,
  runtime, configuration, agent, prompt, workflow or prototype change.

## 2026-10-18: Bounded screen-backlog coverage continuation (#156)

* Extend the [existing prototype profile synthesis](./research/ux/zava-forward-prototype-profile-review.md#screen-backlog-coverage-snapshot-2026-10-18-156)
  and index with the complete public issue snapshot retrieved before
  04:13:45 UTC: 184 issues, 139 open/45 closed. The coordinator's below-cap
  all-state export and paginated REST issue IDs/states agree exactly.
  Record source/base 2ca6d1c48bb95b65e6c349fe508e99c00a74efbe,
  snapshot hashes, exclusion rules and state-qualified membership.
* Classify 74 screen-bearing issues individually with exact existing journey,
  flow and historical design evidence or explicit NOT SUPPLIED gaps; classify
  86 no-screen issues by inspected scope, route 16 aggregate epics and enumerate
  eight reviewed surface ambiguities with precise owner decisions. Retain
  closed screen features and non-obvious ingestion/storage/performance effects;
  no keyword-only or fifteen-profile proxy for whole-backlog coverage.
* Preserve T01-T11/C01-C04, D01-D04 and the original G156 record. Only G01's
  unenumerated inventory residual has a dated continuation. All 74 current
  screen designs, named detailed flow gaps and actual human/accessibility/
  content/user evidence remain missing; literal AC1 is not fully satisfied
  and the overall design gate stays Blocked. No UI, runtime, agent, instruction,
  workflow, private-data or platform change; no issue checkbox/board/merge action.

## [2026-10-18] query | Chat and alert-panel copy audit extension (#153)

* Extend the [existing content standard and audit](./research/ux/content-standard.md#chat-and-alert-panel-audit-extension-2026-10-18-153)
  and index without replacing earlier evidence. Include chat.js in the named
  lexical guard, align snapshot/envelope vocabulary and change only
  application-owned safety/time wording in chat and the coupled case summary.
* Retain authorised human restart decisions, independent hazard routes,
  unknown/unverified warnings, exact AI suggestion labels and proposal-only
  operation. No safety policy, role, backend, consent or resident contact change.
* Distinguish application labels from exact source quotations, user/model text,
  recorded facts, identifiers and raw technical detail. Add a synthetic
  browser source-quotation canary before/after history restore, not source
  sanitization or a claim that every visible term is forbidden.
* Universal core-flow/error coverage, actual user comprehension and named
  resident-facing wording review remain unmet. This partial slice does not
  close the issue, approve resident use or establish WCAG/legal conformance.
## [2026-10-17] query | Consultation record and unknown confirmation hold (#92)

* Audited the existing migrated procurement package and #90/#384 source;
  the issue's old mvp note is stale. Added a supplied-human consultation record
  with source/version/hash, reason, contract/scope, registered recorder, UTC time
  and version conflict controls. No Legal authority or approval was invented.
* Updated core/API READMEs, the existing prototype/profile synthesis and this
  index's task route. Immutable regulatory sources, memory, original/addendum
  and generated fixture/hash manifests remain unchanged.
* No verified contract-consultation Legal capability or genuine let/renew seam
  exists. All supplied statuses remain unverified, effective unknown holds
  binding order confirmations, and both exact issue criteria remain partial.
  Legacy domain regressions explicitly isolate that hold; unmocked consultation
  semantics, individual seam mutations and actual loopback SQL Server recording/
  conflict/reload checks supply separate engineering evidence.
* No real contract/order/spend, resident communication, operational legal
  activation, private data, Azure, paid AI, UI/WCAG acceptance or issue closure.

## [2026-10-17] integration | Consultation controls on hazard main (#92)

* Coordinator authorized own-topic rebase from PR #389 head
  5411f0d41fc4425a5ab3cc9592f175a2f293bd82 onto freshly fetched main
  1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c, including merged hazard #388.
  Only manual conflict was this log: upstream exact prefix retained, followed
  by all own entries. Both consultation/hazard KB routes and syntheses remain.
* Entire own src added/removed bytes match across bases; original Review and
  critique unchanged. Upstream hazard/workflows/shared SQL/Store/finance/grants/
  signoffs, fixture/hash manifest and MSSQL harness are byte-unchanged. No
  current-actor, scoped hold, recovery or pending/committed audit redesign.
* Fresh combined JSON/SQLite/API/manifest validation: 348 executions, 300 passes,
  48 explicit skips. Full component lint/format/types pass (114 core/54 API
  typed files); six added relative links/anchors verified. Original 70 actual
  SQL Server passes remain historical; no new MSSQL run for docs-only conflict.
* Both exact criteria remain partial: no actual verified authorized Legal
  decision and, separately, no genuine let/renew software seam. Isolated
  fail-closed decision recording already exists. Proposed bounded genuine
  workflow integration is coordinator follow-up, not secretly expanded scope.
* Original independent verdict retained, no repeat full Review. Coordinator
  final-head review/check gate remains pending, issue open. No main/other
  worktree/PR #387 write, operational legal activation, real contracts/spend,
  portal, Azure/paid AI, merge or issue closure.

## [2026-10-18] query | Owner-directed scoped consultation hold (#92)

* Owner direction: "Limit the hold to consultation-dependent actions; preserve
  unrelated service work". This approves scope behavior, not Legal clearance,
  contractual power, real spend or deployment. Separate new full RPI task;
  original consultation research, critique, Review and all prior task artifacts
  remain byte-exact with their historical verdicts.
* Removed five blanket consultation checks from ordinary service operations.
  Supplied consultation history, source/version/hash, recorder and effective
  unknown remain intact. Existing explicit building dependency/hold scope and
  case-wide final advancement remain; no label inference or client applicability
  flag, role, Legal authority, true let/renew or purchase API was added.
* Removed affected guard-bypass mocks. Fresh local combined checks: 519 run,
  424 passes/95 skips; core discovery 1117 run, 984 passes/133 skips; API discovery
  794 run, 542 passes/252 skips; actual owned loopback SQL Server 136 run,
  135 passes/one intentional skip. Configured core/API lint/format/mypy and
  25 migration tests pass. Five reintroduced blanket-guard mutants are killed.
  Results overlap in coverage and are not a unique-test total or live acceptance.
* Authorized integration was from topic 9fb84836 onto main 9c648b20; source
  controls and both existing consultation log entries retained after the exact
  upstream log prefix. Remote main subsequently moved to a86282c4; publication
  and any further rebase are paused for coordinator direction.
* Updated component guides, existing profile synthesis and index. No shared
  SQL-store/queue/server/export implementation edit or active-task overlap.
  Genuine let/renew, verified Legal authority, human/live acceptance and
  coordinator exact-head review remain unmet. Issue stays open/partial; no PR,
  issue/board, deployment, spending, model call or merge action at this checkpoint.

## [2026-10-18] integration | Scoped consultation publication on queue main (#92)

* Coordinator authorized only the owned topic rebase from local 7e4aa6ec onto
  exact main a86282c4, including PR407 queue correction; prior base 9c648b20.
  Rebase completed without conflicts. Both README additions, upstream queue
  production/tests and recorder controls remain; no source correction or policy
  change. All earlier entries and the upstream log byte prefix are retained.
* Exact normalized owned and upstream patches match; full tracked inventories
  and ten original artifact hashes are recorded in the separate integration
  receipt. Both old/new original Review and critique remain byte-identical.
  No second original Review or critique was executed.
* Fresh focused consultation/provider/workflow/API: 212 run, 199 passes,
  13 explicit skips. Queue-related combined smoke: 553 run, 458 passes,
  95 explicit skips. Configured core/API lint/format/mypy pass (125/56 typed
  source files). Coverage overlaps; counts are not unique-test totals.
* No production conflict or integration-authored persistence change required a
  SQL/image rerun. Actual 135 SQL passes and upstream hardened-image evidence
  remain historical, not fresh integration results. Legal authority, genuine
  let/renew, human/live acceptance and final independent review remain unmet.
* Same PR389 publication is authorized with the exact old-head lease, normal
  pushes only afterward. No private inputs, real contracts/spend, Azure, paid
  model calls, operational activation, issue/board change or merge.

## [2026-10-18] integration | Scoped consultation publication waits again (#92)

* Exact pre-push guard detected main ab0613f3336109ff9b96560a16758ee842232715,
  no longer authorized a86282c4. It stopped before push; no lease was consumed.
  Topic remote remains 9fb84836, PR389 remains unchanged/open with empty closing
  issue references. No further rebase or PR/issue/board/merge action performed.
* Authorized a86282c4 integration and fresh checks are committed locally at
  ae2bc36b; a later metadata-only stop receipt records the new wait boundary.
  Publication remains blocked pending coordinator direction. All original
  assessment hashes, source parity and historical/fresh evidence distinctions
  remain intact; no source correction or repeated assessment.

## [2026-10-18] integration | Scoped consultation exact DPIA-base continuation (#92)

* Coordinator authorized same-task integration/publication from local c6732027
  onto exact ab0613f3 (merged PR408), previous base a86282c4. Nine owned commits
  replayed without conflicts. No source correction or policy change; complete
  owned patch, upstream DPIA/queue/recorder bytes and README additions retained.
* Both prior integration receipt and old/new original assessments remain
  byte-identical; fifteen immutable artifacts verified. Old-local log remains an
  exact prefix. New separate receipt records full tree inventories, parity
  manifests and preserved execution-log hashes.
* Fresh minimal consultation/provider/workflow/API/timecapture: 235 executions,
  222 passes, 13 explicit skips; configured core/API Ruff/format/mypy pass
  (125/56 typed source files). No failed validation check in this continuation.
  Recent broad/queue smoke, actual 135 SQL passes and image evidence remain
  inherited/historical, not rerun. No packaging or persistence conflict arose.
* Publish only the owned topic using expected 9fb84836 lease; later pushes
  normal only. Later main movement is reported for coordinator gate, without
  changing this exact authorized base. PR389 update retains Refs #92 only.
  Legal authority, genuine let/renew, human/live acceptance and independent
  exact-head review remain unmet. No private inputs, Azure/spend, issue/board
  write, review checkbox completion, ready-state change or merge.

## [2026-10-18] integration | Scoped consultation exact-base publication (#92)

* Initial exact expected-head lease succeeded, publishing 5fdc9d46 on authorized
  ab0613f3. PR389 updated with scoped owner direction, full old/new RPI,
  immutable assessments, exact head/base and unmet acceptance gates; closing
  references verified empty. Remote main still ab0613f3 at publication.
* Final receipt-only closeout is normal-pushed and PR head refreshed; no source
  correction or second original assessment. Complete changed-path inventory
  and original/fresh execution logs are retained. Hosted checks and full
  coordinator independent exact-head review remain pending, not accepted.
* Integration/publication task complete, automatic session stopped as directed.
  Legal authority, genuine let/renew and human/live acceptance remain unmet.
  No issue/board/merge/ready-state operation or review checkbox completion.

## [2026-10-18] engineering | Issue 126 constructed RAI finding-evidence register

* Added append-only constructed claims and deterministic detached reads in the
  existing governance API/store for exactly eleven residual and eleven unassessed
  baseline checks, not the separate eleven AI tasks. No new service/table/role,
  acceptance/closure action, automatic signature or AI admission change.
* Preserved the 2026-10-14 report, original v0.14.0/full source baseline and
  2026-10-15 planning-only acceptance. DOWNGRADED remains open; supplied owner and
  independent-acceptance references are unverified, not assignment or approval.
  Exact assessment comparison is caller-declared, not deployed-source attestation.
* Updated existing core/API guides, addendum, current PRD implementation-status
  note, ADR 0002 and knowledge index. Memory and historical versions are unchanged.
* Local focused suite: 107 tests, 16 explicit MSSQL opt-in skips; separate actual
  disposable loopback SQL Server run: all 16 register cases passed, owned
  container removed. Hardened existing API image ran the same focused suite as
  UID10001/read-only root with dropped capabilities. Ten actual HTTP cases cover
  constructed JSON/SQLite login, authorization, append/replay and failure outcomes.
  Coupled preservation suite: 288 tests, 46 opt-in/other explicit skips, no failures.
* Local engineering is not a fresh qualified RAI assessment, witnessed recovery,
  privacy/legal review, actual-model/Azure delivery, current PRD owner acceptance
  or operational approval. All 22 checks remain Open; whole-issue acceptance and
  version-linked real AI/SQL/Azure application acceptance remain unmet.

## [2026-10-18] query | Issue 110 constructed offline sensor consumer boundary

* Added narrow existing core/API guides and accurate ADR 0003/addendum/index
  status for the owner-authorized finite offline processing slice. The exact
  replay-only synthetic loader remains unchanged and still refuses fault inputs.
* Independently supplied exercise mapping, consent, calibration, window, ranges
  and manual-review ownership are not observations or operational authority.
  SQL stable identity, current-transaction checks, restricted DQ and bounded
  receipts do not alter case/task/priority/safety/financial/consent records.
* Actual local SQLite/SQL Server evidence is distinct from live Hub identities,
  transport, Azure SQL/real AI acceptance and human/privacy approval. Whole
  issue 110/AC-066 remains open; ADR remains Proposed. Infrastructure 140
  depends on the consumer, not the reverse; analysis 111 is not a prerequisite.
  Memory, original case and immutable regulatory evidence remain unchanged.

## [2026-10-18] query | Issue 110 retained reading consistency correction

* Corrected the bounded offline consumer's retained SQL replay and ordering
  validation: malformed timestamps/numbers and inconsistent historical witness
  content now fail with metadata-only refusal instead of success or raw parsing
  failure. The API retains earlier committed-prefix metadata on a later failure.
* Historical exact replay still reconciles after current exercise consent,
  calibration and processing window change. No new admission, duplicate write,
  shared-store mutation, live transport or operational authority is inferred.
* Original adverse critique and Review remain unchanged; this separately
  authorized implementation is correction ONE, not independent acceptance.
  Whole issue/live/Proposed ADR gates and baseline API browser tooling remain.

## [2026-10-18] query | Issue 110 final correction and dated ADR reconciliation

* Reconciled current ADR 0003 status, core/API guides, addendum and index against
  the [owner's 2026-10-15 decision](https://github.com/jmservera/ama/issues/129#issuecomment-6194409951),
  retrieved 2026-10-18. Owner accepted ADR with amendment: Basic IoT Hub enough
  for the exercise; no cloud-to-device messages, device twins or device
  management for now. The ADR preserves its original Proposed status as history.
  Earlier append-only entries and adverse assessment artifacts are unchanged.
* This is not live transport, sizing/cost, network/provisioning/credential
  authority, privacy review, real AI or Azure application acceptance. Whole
  issue 110 and its live/human gates remain open.
* Final authorized correction TWO validates the complete target-sensor retained
  ordering boundary, rather than trusting MAX before validation; low-sorting
  corrupt timestamps and duplicate maxima cannot be skipped. Validated seed
  integers compare semantically across SQLite/BIGINT while retaining exact
  input/digest replay identity. No new store, service or operational policy.

## [2026-10-18] query | Issue 186 shared observation contract and measured volume

* Extended the existing [sensor synthesis](./research/iot-sensor-analytics-research-plan.md#shared-observation-contract-and-volume-2026-10-18-refs-186)
  with the unchanged consumer's authoritative imported 13-field string schema,
  exact identity/time/unit constraints, envelope distinction, stable-key
  replay/conflict and bounded receipts/DQ. No independent schema or runtime API.
* Preserved three paired temperature/RH observations/home/day: declared N=1 and
  fictional N=60,000 give 3 and 180,000 records/day, mean 1/28800 and 25/12 per
  second. Reproduced one public current-contract sorted ASCII JSON sample at
  366 bytes, yielding illustrative 1,098/65,880,000 payload bytes/day, not upper
  bounds, wire-message counts, Hub billing, peaks or measured live traffic.
* Explicitly recorded the stock adapter's 73-character lowercase-hex sensor-ID
  incompatibility with uppercase, 20-character consumer admission. No remap, truncation,
  validation weakening or source change; fixture validity is not stock/live
  interoperability. Downstream #187/#188 need a separate reviewed decision.
* Linked component READMEs, addendum and index. Preserved accepted ADR 0003/
  Basic exercise amendment and its historical Proposed text; whole #110,
  transport/identity/cost/network/privacy/real AI/Azure/human gates remain open.
  No private stock, original-case or memory changes, new data approvals,
  operational rules, tasks, priorities or resident communications.

## [2026-10-18] query | Issue 137 read-only pilot capability and quota evidence

* Added [dated infrastructure evidence](../../infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137)
  for exact unchanged template configurations, management GET command shapes,
  scope/units, support facts and explicit empty/denied/failed quota surfaces.
* Verified the actual 2026-10-15 owner comment selecting pilot `uksouth` and
  subscription owner @jmservera. Withdrew the unsupported current README claim
  of a superseding undecided direction. Added an
  [ADR dated delta](../adrs/0002-pilot-readiness-architecture.md#pilot-region-and-capability-evidence-delta-2026-10-18-refs-137)
  without changing its 2026-10-08/09 historical table; updated index routing.
* No template/example, runtime, dependencies, private data, original case or
  memory changes. The unchanged example's stale comment is explained, not
  treated as owner authority. SQL-region selection, quota/zone gaps, approved
  account binding, cost/deployment/access authority and named human review
  remain unresolved. No resource changes, data-plane calls, reservations,
  quota approval or issue closure; region/quota criterion remains unticked.

## [2026-10-19] query | Issue 137 preserved-task reproduction and authority reconciliation

* Reproduced all seventeen original read-only management GETs with identical
  command shapes and bounded timeouts; selected fields and adverse categories
  matched the retained 2026-10-18 receipts. Corrected the premature same-day
  reproduction wording in the uncommitted evidence; no historical query was
  redated. Confirmed all eight referenced configuration files byte-identical
  at original base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd and approved
  main fa659cfd021100f7c64f8ec73bbff76c03adf234.
* Reverified the actual 2026-10-15 owner comment. Explicitly retained the
  contradictory 2026-10-16 historical delivery comment as a contradiction,
  not a replacement owner decision. Updated the existing
  [infrastructure evidence](../../infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137),
  [ADR delta](../adrs/0002-pilot-readiness-architecture.md#pilot-region-and-capability-evidence-delta-2026-10-18-refs-137)
  and index. Scope/unknowns/approval boundaries remain unchanged.
* Continued the preserved RPI task without repeating critique. The owner
  superseded documentation-only validation and publication permission:
  full canonical local gate is mandatory, and independent coordinator
  source/RPI/primary-evidence review plus a final matrix receipt precede any
  later push/PR decision. No cloud writes, private dataset access, original
  case or memory changes, issue mutation or publication.

## [2026-10-19] query | Issue360 bounded RG publication capacity evidence

* Read complete live #360/#349/#358 and fresh secret-free management state.
  New owner RG-resource authority supersedes missing publication-route
  permission only; no tenant, data, public-backing or human approval inference.
* Actual exact provider preflights for B2als_v2 and D2as_v5 both failed UK South
  capacity despite unrestricted SKU GETs and available quota. No resource,
  grant, source upload, image build/push/pin or cloud deletion occurred.
  The tested isolated VM allocation candidate is undeployed, not allocatable
  proof. Preserve this contradiction and all earlier adverse/historical evidence.
* Updated [infra runbook](../../infra/README.md#bounded-private-publisher-capacity-attempt-2026-10-19-refs-360),
  [ADR0002 delta](../adrs/0002-pilot-readiness-architecture.md#private-publisher-capacity-delta-2026-10-19-refs-360),
  [evidence pack](../architecture/cutover-evidence-pack.md#bounded-rg-publication-continuation-2026-10-19)
  and KB index. Fresh HTTPS four-route403 and Graph discovery failure are
  restrictions/blockers, not actual health/browser/role/SQL/AI acceptance.
  #360d/e stay unmet, Front Door/old stack/ama retained, #358 follows separately.
  No original case, owner memory or private dataset change.

## [2026-10-19] change | Issue360 cycle2 explicit publisher outbound boundary

* Rejected the unused publisher template's unrestricted default outbound policy.
  Added exact private-ACR HTTPS and Azure platform DNS/agent/IMDS exceptions,
  explicit remaining platform-service denials and deny-all outbound before
  default VNet/Internet rules. Existing inbound, private backing, exact-RG and
  connected-resource guards remain unchanged.
* Updated the [runbook policy](../../infra/README.md#explicit-outbound-restriction-2026-10-19-cycle2),
  [evidence disposition](../architecture/cutover-evidence-pack.md#later-outbound-source-restriction-2026-10-19-cycle2),
  ADR0002 and index. Stock-image package bootstrap is intentionally blocked;
  NSGs cannot filter package FQDNs or DNS/registry content. Platform exceptions
  and unsupported live/security claims remain explicit.
* Eight focused and367 complete infra tests pass without skips. External
  compiled before/after evidence reproduces acceptance of the unsafe original
  and rejection by the new policy checks; all18 outbound mutants reject.
  These are local engineering results, not live NSG or release acceptance.
  No Azure write/deploy/what-if/capacity attempt, allocation, image publication,
  tenant/data operation or human approval occurred. Both original SKU failures
  and original Research/critique/Not accepted Review remain unchanged.

## [2026-10-19] change | Issue360 PR416 rubric publication lifecycle recovery

* Inspected actual current-main source/compiled workflow and run 39237980947
  record-job logs: gate 48/100 vs 48 PASS, successful score-only append and correct
  NEW_SHA, but immediate publication API head mismatch produced a failed status.
  The original returned SHA was not logged; reproduced old-source visibility
  is an explanation, not invented telemetry or proven concurrent movement.
* Added bounded post-successful-push visibility reads while the API returns only
  the original source SHA; exact bot HEAD remains required. True movement,
  failed score push, invalid/error responses, closure and retry exhaustion do
  not become passes. Trusted baseline/scoring/provenance, guarded non-force
  writes and retained checks/protection remain unchanged.
* Updated the [rubric guide](../../.github/rubric/README.md#post-push-visibility-and-exact-head-completion)
  and index with one-score-append/final-head local gate/independent assessment/
  retained hosted-check sequence. No hosted scoring, push/PR update, cloud,
  model or tenant write was used for diagnosis. Original issue360 live acceptance
  remains unmet; original research/critique/adverse Review remain immutable.
* Focused source/compiled lifecycle plus pinned real MCP/schema checks pass 219
  cases; baseline reproduction fails 24 visibility cases before repair. The
  full rubric suite retains the same 21 pre-existing failure IDs as bot HEAD,
  with 331 passing and no skips after restoring the pinned missing runtime.
  Compiler-generated lock and native actionlint/ShellCheck pass. Full 17-group
  frozen-candidate gate and coordinator assessment are separate required steps.

## [2026-10-19] ingest | Issue358 actual existing-resource preservation preflight

* Read complete live issue/comments and merged374, then traced the unchanged
  production helper/payload. Isolated preservation reconciliation/ARM PATCH
  does not intrinsically need image publication or Graph; full credential/setup
  mutation remains broader and was not invoked.
* Actual production Azure.rest GET at2025-07-01 confirms explicit null secrets,
  zero KV pairs and env/init/scale/registry secret bindings on all three
  existing ama apps. Both APIs have no auth secret ref/token store binding;
  agents auth read failed, not silently treated as a successful empty result.
  App-scoped permission metadata includes write/listSecrets, not provider proof.
* Demo labels are nonproduction intent, not guarded profile proof: unchanged
  require_demo refuses unknown/malformed deployment evidence. The primary
  live blocker is no populated existing target. Empty PATCH, clone and new
  sentinel state cannot replace literal preservation acceptance.
* Updated [existing runbook](../../infra/README.md#existing-resource-preservation-preflight-2026-10-19),
  [dated evidence](../architecture/cutover-evidence-pack.md#existing-resource-preservation-preflight-2026-10-19)
  and index. Final readback retains null/count/revision/lock state. Zero cloud
  writes/listSecrets/secret-value reads; no source/test defect/change or new
  offline substitute. No rollback/deletion needed; owned bytecode removed,
  only sanitized external0700/0600 summaries retained. Original evidence,
  log entries and owner memory remain unchanged; #358 and whole demo acceptance
  are not claimed. No review-ready publication candidate/full-gate receipt is
  created for this explicitly no-heavy-gate blocked disposition.

## [2026-10-19] update | Issue358 isolated real synthetic preservation evidence

* Later explicit owner direction selected a separately reviewed temporary
  synthetic baseline, not modification of existing running apps. Supplemental
  research and amended lifecycle plan/details/changes preceded all allocations;
  one independent new-material safety assessment directly read primary metadata.
  Original critique and original Partial / Residual Review remain byte-identical.
* Native secureString ARM deployment created exactly one synthetic vault secret
  after a new private synthetic-only cleanup job proved its exact absent-name
  metadata route. Dedicated MI grants were secret-scoped Secrets Officer and
  registry-scoped AcrPull only; no existing identity/workload/job was changed.
* Real baseline Succeeded before unchanged production preserve_app_secrets and
  Azure.rest configuration-only PATCH. Actual InProgress/Succeeded readback and
  private comparisons preserve KV URL/identity, known resolved synthetic KV
  value, unrelated value, unused binding, configuration/template/MI/tags/revision.
  All eight exact comparisons pass; no source defect/fix or offline substitute.
* App, active/soft-deleted secret, deployment history, job/executions, MI and
  final role pair were removed by15:09:10Z. All ten role IDs across earlier
  cleaned operator-correction incarnations were re-read absent; all11 old
  workload snapshots, RG membership and existing backing hashes match.
  One temporary app replica was observed despite min0; no zero-runtime/settled
  zero-cost claim. Four private job executions were bounded to120seconds/retries0.
* Updated [evidence/cleanup table](../architecture/cutover-evidence-pack.md#real-temporary-synthetic-preservation-roundtrip-2026-10-19),
  [existing runbook](../../infra/README.md#real-temporary-synthetic-preservation-2026-10-19)
  and index. Sanitized primary observations are included in candidate execution
  evidence for in-worktree access; exact IDs/comparison hashes remain external0600.
  This is real temporary synthetic component proof, not originally populated
  deployed-app/full credential setup, profile/browser/SQL/AI/human acceptance.
  #358 remains open for coordinator judgement; no push/PR/merge/status/settings
  action. Frozen full local gate/receipt and coordinator assessment remain
  separate publication requirements.

## [2026-10-19] query | Version-bound affected-person challenge boundary (#220)

* Updated the existing [resident journey synthesis](./research/ux/customer-journeys/residents.md#affected-person-challenge-engineering-boundary-2026-10-19-220),
  index and core/API component guides with the retained-priority engineering
  slice. Reused current resident independent-review/remedy and server recorder
  controls; no owner memory or immutable regulatory snapshot was changed.
* Supplied Digital/Phone/Letter/In person evidence binds the original proposal,
  captured case citation snapshot or recorded ranking-policy version and human
  disposition. A terminal supplied correction invalidates only exact dependency
  matches; historical decisions and independent safety/manual paths remain.
* Source hashes describe audience-filtered citation labels, not universal
  documents. Legacy absent hashes stay Unknown. Other assistant/form paths,
  whole-system AC-071, issue-specific native SQL and qualified/resident
  acceptance remain open. Local constructed tests make no new legal,
  accessibility-conformance, live-model or operational-approval claim.

## [2026-10-19] query | Restore historical challenge actions (#220)

* Updated the existing resident journey, KB index and API guide after reproducing
  the last-50 cutoff on actual public synthetic SQLite/HTTP/browser data.
  Bounded Older/Newer controls and exact reference entry make older retained
  targets, open resolution actions and resolved explanations reachable.
* URL-bound pages reload, opening drafts retain bindings while browsing, and
  unsaved resolution drafts require confirmation before page disposal.
  No core authority, selective dependency, resident choice or safety route
  changes. Original Partial / Not accepted Review and Revise critique remain
  unchanged; a separate bounded finding disposition and corrected exact-head
  local gate are required, not whole-issue acceptance.

## [2026-10-19] query | Bounded challenge PR finding corrections (#220)

* Updated the existing [resident journey boundary](./research/ux/customer-journeys/residents.md#affected-person-challenge-engineering-boundary-2026-10-19-220),
  index and core/API guides for five actual PR #418 findings: stale-route refresh,
  synthetic ownership persistence, repeated correction scans, priority-reference
  disclosure without current dual entitlement and lost release-denial audit.
* Generated 60,000-home/52-proposal read checks, correction-only SQLite query
  checks, JSON/SQLite/HTTP regressions and actual Chromium journeys support the
  bounded fixes. Seven task-owned loopback SQL Server regressions verify current
  correction races, cross-case policy matching, entitlement and rollback.
* Original research, Revise critique, Partial / Not accepted Review and historical
  failures remain unchanged. No replacement Review, whole-issue acceptance,
  native-scale/load acceptance, human approval or publication is inferred.

## [2026-10-19] query | Current challenge detail authority and indexed writer evidence (#220)

* Updated the existing resident journey, index and core guide for actual cached
  reader downgrade/removal denial across case challenge narratives and targets,
  preserving ordinary case detail and trusted internal reads.
* Reused derived case-column/filtered-index prior art for a transactionally
  maintained correction-presence flag with atomic migration and rollback.
  Actual owned native generated60,000-case plans show one flagged row/JSON
  evaluation rather than a full scan; bounded latency and competing unrelated
  writer measurements are sparse warm-cache query evidence, not an SLA or
  production/native whole-workflow acceptance.
* Actual latest review adds an off-page draft duplicate-form finding outside
  the selected backend scope. It remains unresolved; platform advisory/resolved
  labels do not establish technical closure. Original research, critique,
  Review and prior finding dispositions remain immutable. Whole issue stays open.

## [2026-10-20] query | Task-bound operator suspension and constructed restart (#221)

* Indexed the existing core/API guides for persisted incident/version capture,
  task-aware dispatch/reliance fences, separately provisioned trusted restart
  permission and immutable constructed corrective-candidate claims.
* Actual OD-35/RULE-020 restart remains unavailable, including after a
  constructed drill, provider switch, reopen or replacement release.
  Missing evidence remains explicit and fail-closed; manual/hazard response
  is not routed through the AI hold.
* This is a bounded engineering boundary, not approved monitoring thresholds,
  actual corrective-test acceptance, named human appointment, human-witnessed
  drill, live application acceptance or whole-issue closure. Original #219
  adverse and later correction evidence is retained.

## [2026-10-22] ingest | AI Tokenomics and the capstone pitch

* Owner reported that a mentor raised Tokenomics at the progress review. The
  mentor's words are not in the repository, so the link is owner-reported and
  unconfirmed. Retrieved the public Tokenomics Foundation pages (definition
  draft v0.5.2, Total Cost of AI episode, projects) and recorded a pointer to an
  internal Microsoft deck found through WorkIQ, marked do-not-quote.
* Added [AI Tokenomics](./resources/ai-tokenomics.md): framing, mapping to
  rubric A5, A6, B7, C1 and C3, existing Zava Forward evidence (per-call usage
  envelope, finite limits, 6,884 tokens over five operator runs) and gaps.
* Added BRD v0.19.0 (NFR-012, FR-052, AC-100 to AC-103, OD-51, BG-012 measure,
  AI Consumption Economics section) and PRD v0.18.0 (FR-061, NFR-017, AC-107 to
  AC-110, OQ-027), an addendum section, the
  [Tokenomics pitch brief](../capstone/pitch/tokenomics-pitch-brief.md) and a
  capstone README pointer. Index rows updated. On GitHub, created #432 and added
  Tokenomics delta sections to #100, #104, #107, #108, #126, #144, #146, #157,
  #159, #214, #225 and #226.
* Contradiction flagged: [ADR 0001](../adrs/0001-azure-architecture.md) says
  cost per unit of business value cannot be stated until measured usage exists;
  the capstone rubric A5 rewards stating it. The new rows keep the gap explicit
  and set no price, budget or target. PRD "59/59 FRs" link-coverage text was
  already stale and is corrected to 61/61.
* Not done: the 24-slide deck is unchanged (placement is an owner decision), no
  rehearsal, no price retrieved, no spend authorised, no score claimed.

## [2026-10-22] query | Backlog review after the Tokenomics amendment

* Backlog Manager review of the open GitHub backlog (about 141 issues) with the
  parent applying the executor operations, because the delegated agents had no
  write tools. Not every issue body was read; targeted queries and named issues
  only.
* Created #435 (capstone pitch preparation, under #104). Linked #432 and #435
  under #104 and #344 under #195. Added Tokenomics delta sections to #164, #216
  and #217 (unticked criteria). Added missing Dependencies sections to #349,
  #350 and #358. Removed the contradictory `status:not-started` label from #75,
  #92, #97, #110, #126, #172 and #178 (each also carries
  `status:partially-delivered`); the stale "not started" sentences in some
  bodies were left for the owner. Added `status:not-started` to #432.
* Board: `tools/backlog-sync.py --apply` moved nine open issues between Todo and
  In Progress from PR and worktree evidence. It did not tick any criterion. #432,
  #434 and #435 still report as missing from its item list although #432 and
  #435 were added to project 7.
* Left for the owner: automated rubric-failure issues #10, #33, #46 to #49 look
  expired and closable as not planned (not done), #38 needs a check of the latest
  scorer run, #6 and #434 are auto-managed and stay open, #430 stays open, and
  #349, #350, #358, #360 still lack type, area and status labels and parents.
## [2026-10-20] update | Finite costed execution plan options for an unfinished Azure demo (#126)

* Added a subsection to the existing Case Study 48 addendum and one index
  row. It gives dated, USD, resource-group-scope October accrued cost (189.94
  for 1-20 Oct, estimated and partial), current burn, existing liabilities and
  a no-change projection of 535.41 against the owner's USD 500 total.
* Offers owner-decision options (Front Door retirement, SQL idle) and bounded
  tranches T0 to T4 with approval fields, finite call and token bounds,
  thresholds, expiry gate, cleanup and recreation. Subscription-scope spend,
  prices for several meters, quota, private bootstrap and human gates stay
  unresolved and block execution.
* Proposals for separate owner approval only. No Azure change, approval of a
  manifest, issue acceptance or operational release follows.

## [2026-10-20] update | Corrected unknown-spend term in costed plan options (#126)

* Corrected the gating rule in the existing addendum subsection: the other-scope term U is a bounded month-end forecast of non-resource-group-`ama` charges and liabilities, not accrued-only. Unbounded U blocks every paid tranche; no zero is assumed and the cap is not raised. Earlier entry retained.

## [2026-10-22] update | Revised USD 700 ceiling and private-Blob demo options in costed plan (#126)

* Revised the existing addendum subsection and index row for the owner decision of 2026-10-22: USD 700 is the replacement all-in October forecast ceiling (not additional), expiry 2026-10-25T16:02Z unchanged. The USD 500 wording, its thresholds and 535.41 projection are kept as dated 2026-10-20 history.
* Recorded fresh read-only evidence for resource group `ama` (USD, retrieved 2026-10-22): 242.36 observed, 535.33 forecast with no change, reconciled against the 2026-10-20 read. Subscription-scope cost remains unreadable, so the outside-group term is unknown and every paid tranche stays blocked.
* Added finite private-Blob options (B1 ceiling 5) with envelope cap 655, review 560, pause 630 and stop 665. Retirement options are not offered because none is authorized. Screen-reader acceptance and signed source/image attestation are recorded as unverified production follow-ups.
* Proposal only: no Azure change, approval, issue acceptance or release follows; #126 stays open. Earlier entries retained.

## [2026-10-22] update | Corrected pre-change forecast labelling in costed plan (#126)

* Corrected the existing addendum subsection and index row. The earlier entry and index wording that called the 535.33 forecast "with no change" and S0 the current baseline are superseded: that figure is a pre-change scenario read about 14:00Z, before an owner-authorized deletion of the cutover-test Front Door Premium profile and its policy and a scale-down of the cutover-test demo API app to zero replicas (verified by read-only inventory, 91 resources at about 14:53Z).
* No saving or zero residual charge is stated; cost data had not caught up (observed 242.36 unchanged). A refreshed post-change forecast with a fresh inventory and complete post-change days is required before any tranche. Outside-group spend stays unknown; paid execution stays blocked; the 700 ceiling and expiry are unchanged. Earlier entries retained.

## [2026-10-23] add | Executive-first capstone Cowork authoring package

* Added `docs/capstone/pitch/cowork-main-presentation/`: 18 main-slide
  content contracts with full notes, 27 CXO question-led backups, a separate
  ten-minute demo with live/evidence/recovery routes, audience guidance and
  a complete Cowork brief. The requested 30-minute presentation allocates
  24 minutes to narration and six to interruptions, not an observed rehearsal.
* Added seven editable 1600x900 Excalidraw views with embedded official Azure
  icons, SVG/PNG previews, text alternatives and a standard-library generator.
  Views progress from the business idea to AI placement, runtime, controlled
  proposals, operations, target sensors and Tokenomics. Current contracts,
  historical observations, configured paths and deferred work remain distinct.
* Incorporated merged Tokenomics PR #433, partial metering, historical
  6,884-token/five-run evidence, proposed economics/control requirements and
  unknown accepted-outcome cost. Preserved the owner-set October USD 700
  ceiling, unchanged expiry and blocked post-change execution gates; no
  production price, model benefit or cash saving is invented.
* Checked memory/log, historical issue-generation evidence and private AMA
  Plan project 7 after owner authentication. The historical approximate
  180 means issues, including epics and stories, not agents or stories alone.
  The dated current board has 189 items; its bundled image is labelled
  API-derived, not a GitHub website screenshot or accepted delivery.
* Updated capstone and reference routing. Existing executive/mentor decks,
  original case study and owner memory remain unchanged. Final PowerPoint
  authoring, native-viewer checks, human acceptance, actual rehearsal and
  fresh live-demo preflight remain outstanding.

## [2026-10-23] ingest | Index retrofit, damp and mould statistics report

* Added the supplied [Retrofit, Damp and Mould Statistics Report](./research/sector/uk-social-housing-retrofit-damp-stats-report.md)
  to the [reference index](./README.md), in benchmark task routing and the
  research syntheses catalog.
* Retained the report's national-versus-company distinction, differing
  statistical bases, separate Scottish case counts and unconfirmed pricing
  caveats in the index summary and routing.
* Left the supplied report unchanged. Indexing does not independently verify
  its figures, citations or regulatory currentness.

## [2026-10-23] ingest | Cowork outputs and owner-selected v2 scoring candidate

* Imported nine generated outputs under
  [Cowork presentation outputs](../capstone/deck/cowork-generated/README.md):
  both handoffs, the protected source PPTX, v1/v2 PDFs, contact sheets and
  preview archives. Compared every imported file with its source; the existing
  statistics report is identical and remains canonical rather than duplicated.
  Added frontmatter and normalized v2 handoff Markdown formatting only.
* The owner selected v2 for capstone scoring and explicitly confirmed public
  repository clearance despite the Microsoft Confidential marking. Historical
  v1 exports and the old executive deck remain separate from current selection.
* The source PPTX is an encrypted CDFV2 container and cannot be read by the
  scorer. The owner chose to supply an approved unencrypted v2 export rather
  than substitute PDF text. Cowork's save-retry report, saved-v2 parity and
  speaker-note verification remain unresolved; no deck extraction is claimed.
* Changed the proposed registry to select only the future readable v2 path
  and added a 20,000,000-byte deck-only allowance with boundary and selection
  regressions. Other artifacts retain 2,000,000 bytes. Trusted base tooling
  must receive these changes before hosted scoring can use them; no workflow
  dispatch, score update, commit, push or acceptance is inferred.
* Updated the capstone/reference indexes and rubric guide. Reported Cowork
  checks remain source claims; desktop, accessibility, rehearsal, full rubric,
  independent review and publication gates are not promoted to passed.

## [2026-10-23] ingest | Public Cowork v2 scoring deck and extraction verification

* The owner supplied a public, unencrypted PPTX after the protected-source
  blocker. Imported it as the sole registry-selected
  [v2 scoring deck](../capstone/deck/zava-forward-cowork-v2-draft.pptx),
  preserving the original encrypted source and historical v1 exports.
* The actual scorer extractor reads 54 slides and 54 speaker-note blocks;
  OOXML archive integrity passes and slide 39 contains the final-save wording
  recorded in Cowork's handoff. The file is 2,632,502 bytes; its SHA-256 is
  `ebccfee35890332ca7aebd4f14f80141996747a4086c9ea03fda2dda5b53d860`.
* Updated current capstone/reference routing and the rubric guide. Original
  import blockers and Cowork's failed-save report remain as dated history,
  not current claims that the public export is unreadable.
* Local extraction does not establish complete source/PDF/notes parity,
  native rendering, accessibility, rehearsal, accepted forecasts or a rubric
  score. Trusted-base activation, independent review and publication gates
  remain separate; no commit, push or paid workflow dispatch is inferred.

## [2026-10-23] lint | Cowork import integrity and focused scorer checks

* Verified the v1/v2 PDFs parse as 46/54 pages and the preview ZIPs contain
  46/54 images with member integrity passing. The v2 PDF also contains the
  final slide-39 save marker. The parser ignores one invalid object pointer
  per PDF; strict PDF structure, visual review and semantic parity are not
  claimed. All binary imports remain unchanged.
* The complete prepare suite reports 54 passes and one deleted-file scoring
  fixture failure (`KeyError: 'total'`). The failure reproduces with the
  original HEAD prepare implementation. All six new deck-selection and
  size-boundary cases pass; no unrelated fixture repair is included.
* New output-index and imported-handoff Markdown checks pass. Existing
  rubric/index/log diagnostics remain outside this import's scope. The full
  publication gate, independent assessment and hosted scoring were not run.

## [2026-10-23] query | Main-route IoT and optional resident portal presentation refinement

* Owner requested IoT in the main presentation and optional portal benefit
  assessment rather than categorical exclusion. Read issue #441 and comment
  6374724922: Option B reuses case/API authority, portal/workflow first and
  resident-answer task separately gated. The issue is open with a Research
  integration blocker and no published PR at retrieval; owner-reported local
  work is not inspected implementation, approved requirements or delivery.
* Revised v2 slides 9, 13, 19, 33 and 46 and their notes without changing the
  54-slide inventory or navigation. The main architecture adds a consistently
  amber, not-live sensor/simulator -> IoT Hub Basic -> API/SQL -> human-review
  lane. Retained the independent hazard route and no-diagnosis boundary.
* Portal copy now assesses fewer avoidable calls and staff interruptions,
  including total review/handling and resident effort, access and comprehension.
  Assisted channels remain available without detriment; per-message human
  review stays normative and routine automation off. No numerical saving,
  cash/headcount result or resident acceptance is asserted.
* Updated the authoring brief, original slide contract, source ID E441,
  generated speaker/backup notes and demo commentary. Original Cowork exports
  and handoffs remain historical. Added a refinement record, native previews
  and current PDF; retained the owner-expanded registry without modifying it.
* Packer structural validation passed. Native PowerPoint opened 54 slides,
  rendered all five changed slides and saved the PDF. Independent visual QA
  found a clipped IoT sentence and ambiguous target status styling; local
  corrections were repacked, re-rendered and inspected. Replaced a touched
  resident banner that implied completed comprehension testing with a future
  human-validation gate. This is scoped artifact evidence, not accessibility,
  rehearsal, full capstone/human/live acceptance or publication clearance.
* Installed-deck checks verify 54 slides and 54 notes with the original
  slide-39 marker retained. Canonical XML comparison proves only the five
  intended slides and their notes changed; package membership, all other
  parts/media, sections and navigation relationships are unchanged. The
  native PDF has 54 pages and the new IoT/portal wording. Registry untouched.
* Final link review found inherited references to unretained source
  deliverables (v1 exports, v2 preview ZIP and protected source PPTX). Replaced
  those broken output-index links with explicit source-only status; did not
  restore or delete archival binaries. Retained original v2 PDF/contact sheet
  and handoff contents remain unchanged.

## 2026-10-24 - Report-Only Rubric Model Pilot

* Recorded the owner-approved USD 10, one-run-per-model Sonnet 5, Haiku 4.5
  and GPT-6 Luna pilot in the existing AI Tokenomics reference and index.
* Retained the frozen commit, runtime/transport differences, complete-accounting
  usage fields, USD 0.38631076 equivalent total and individual wall times.
* Sonnet and Luna returned valid cards but differed on four criteria; Haiku
  omitted summary and failed strict validation. Missing thought leadership
  forces D1-D3 to zero, not acceptance. No billable retry, model substitution,
  workflow/score/baseline change or live status publication was performed.
* Kept Sonnet pinned. Single-run cost reductions do not establish equivalent
  grading, stable speed, application value or a reconciled financial saving.

## 2026-10-24 - Pinned-Runtime Native Rubric Submission Follow-Up

* Added the owner-approved Haiku 4.5 and GPT-6 Luna native-MCP extension to
  the existing AI Tokenomics reference and index; preserved original results.
* Verified pinned runtime hashes and seven actual stdio/HTTP runtime tests.
  Each model made one tool call and one locally appended, strict-gate-valid
  card without a rejected-call correction. Haiku scored 64, Luna 56; nine
  criterion differences and missing thought leadership remain explicit.
* Recorded Haiku's 303-character A5 rationale as an instruction violation,
  separate from schema/gate acceptance. CLI/stdio integration is not full
  hosted workflow equivalence; no native Sonnet control was run.
* Follow-up usage was USD 0.12076544 equivalent, USD 0.50707620 aggregate
  across five approved invocations. No production-model switch, live score
  publication, commit or push; concurrent owner deck/registry edits excluded.

## [2026-10-24] lint | PR 438 review corrections

* Addressed five unresolved review threads and two additional summary findings:
  exact v2 scoring path with the existing 20 MB allowance, opt-in destructive
  diagram reset, caller-sensitive backup returns, qualified deployment labels,
  unavailable/moved assets and unsupported inference pricing.
* Added six temporary-package rebuild/navigation regressions; the normal
  real rebuild leaves native Excalidraw and SVG/PNG previews unchanged.
  Combined with six existing registry/size checks, all 12 focused tests pass.
* Preserved imported handoffs and existing uncommitted Tokenomics work.
  Retargeted retained historical deck/process/architecture assets to draft;
  unavailable original exports remain explicitly source-only.
* Corrected current v2 slides/notes and native appendix actions, preserving
  54 slides/notes, existing media and main-route text outside review scope.
  All 27 native caller actions and navigation-note reminders were verified;
  separate topic links serve index entry. The native PDF has 54 pages.
* Removed unvalidated inference-price and cheapest-cost claims in accordance
  with issue #435; retained historical usage and unknown accepted-outcome cost.
  Slides 18/19 qualify implemented functionality with current sign-in/Graph
  acceptance outstanding against the cutover evidence pack. The dated
  [correction record](../capstone/deck/cowork-generated/review-corrections-2026-10-24.md)
  supersedes those handoff claims for current use without rewriting history.
* Native rendering and independent visual inspection exposed topic-button
  clearance and oversized word callouts; both were corrected and re-rendered.
  These are scoped artifact checks, not full accessibility, rehearsal,
  live-system acceptance, a fresh rubric score or publication clearance.

## 2026-10-24 - Owner-Requested Council Cost Calculation Recovery

* Recovered the earlier v2 planning arithmetic in the
  [cost evidence](../capstone/pitch/cowork-main-presentation/evidence/ai-cost-evidence.md#recovered-council-comparison-2026-10-24):
  6,884/5 tokens x tenfold size x 20 tasks x USD 1.60/million gives
  USD 0.440576/planned home and USD 6,872.9856 for 15,600 homes.
  The price remains a dated third-party assumption, not verified deployment
  pricing, a bill or measured accepted-outcome cost.
* Restored GBP 6,082/home x 15,600 = GBP 94,879,200 works and the conditional
  50% illustration of GBP 3,041/home, GBP 47,439,600 cohort grant. Preserved
  separate fictional package costs, unknown full project TCO, currency
  boundaries and Finance/funder verification before external use.
* Updated source S09/S11, B05/B09/B25, evidence IDs, generated script and
  appendix, package guidance and this index. Clarified how reviewed evidence
  supports eligible applications/claims without guaranteeing eligibility,
  funding or additional grant income. Preserved earlier review findings and
  issue #435's unresolved measured-economics gates; no remote issue changed.
* Exact decimal arithmetic and all six existing rebuild/navigation tests pass;
  the rebuild checks 18 main slides, 27 backups and unchanged narration time.
  Native PPTX/PDF are unchanged: rendering tools and an active PowerPoint
  editing session were unavailable. The handoff maps the six required native
  slide revisions. No rehearsal, fresh scoring, full publication gate,
  commit or push was performed.

## 2026-10-24 - Native Council Cost Recovery Build and Export

* Completed the later execution request: updated pages 6, 11, 21, 32, 36 and
  52 and their notes in the existing owner-selected 54-slide deck. Replaced
  the current PPTX/PDF only after scoped checks and native rendering passed;
  saved the original pair in the dated working directory.
* Restored the labelled USD 0.440576/planned-home and USD 6,872.9856 cohort
  inference calculation, GBP 6,082/home benchmark and conditional GBP
  3,041/home grant. Retained separate fictional package arithmetic, unpriced
  project P, dated secondary pricing and proposed money-control boundaries.
* Selective OOXML generation changed exactly six slide and six note parts;
  every other ZIP member remains byte-identical. Verified 54 slides, 54
  nonempty note parts, a 54-page native PowerPoint PDF and all 27 Last Slide
  Viewed caller actions through native COM readback. The PowerPoint builder
  property validator reported zero issues across 54 slides; exact arithmetic
  and restored PDF text checks passed.
* Exported 18 changed/adjacent previews and three contact sheets. Corrected
  chart-label wrapping, grant-tile fit and a formula/ledger collision before
  delivery. The [build record](../../.copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/changes/build-deck.md)
  contains paths, methods, hashes and limitations. Updated the source handoff,
  output index and dated correction record without erasing adverse history.
* No issue #435 acceptance, primary-price/current funding verification,
  independent storytelling review, timed rehearsal, accessibility conformance,
  fresh hosted score or publication clearance is claimed. Existing staged and
  unstaged work was preserved; no commit, push, live inference or deployment.

## [2026-10-24] query | Preserve cost calculations on future slide builds

* The owner requested that later builds retain or recalculate the recovered
  AI, per-home retrofit and conditional-grant comparison. Added explicit dated
  E21 inputs to the source `cost_model` and decimal recalculation to the
  [existing builder](../capstone/pitch/cowork-main-presentation/build_assets.py).
* Source builds fail before writing notes when required costs, exact workings
  or caveats are missing or stale. The native-PPTX check covers all six cost
  pages. Input changes require corresponding evidence, copy, notes and slide
  updates; old secondary pricing does not become verified current pricing.
* Documented the mandatory candidate check and regression command in the
  [authoring brief](../capstone/pitch/cowork-main-presentation/COWORK-BRIEF.md#required-cost-preservation-on-every-rebuild),
  package README and this index. Retained separate currencies, conditional
  grant assumptions, unknown full-project TCO and accepted-outcome cost.
* All 23 focused tests pass, including removed source sections, stale inputs,
  missing caveats, altered native slides and rejected XML entity declarations.
  The delivered PowerPoint passes the guard. No deck/PDF bytes, owner memory,
  earlier log entries, price evidence or approval status were changed.

## 2026-10-24 - Durable Recovery Sources and Verified Tracking Retention

* Promoted the native recovery builder/manifest and pinned original PPTX into
  durable tools/authoring locations. Preserved the
  [original build narrative](../capstone/deck/cowork-generated/native-recovery-build-2026-10-24.md)
  and exactly 12 assurance/PRD report files byte-for-byte, with siblings,
  original findings and tracking originals retained. Updated active links,
  not historical log references or report bodies.
* Added the [retention policy](./method/tracking-retention-policy.md) and
  [native recovery guide](../capstone/pitch/cowork-main-presentation/native-recovery/README.md).
  New heavy outputs default to external scratch; active work and original
  critique/Review evidence remain. Complete local publication, independent
  review, hosted and human gates are unchanged.
* Verified the full external archive: 2,420 files / 600 directories /
  83,975,587 logical file bytes. Restored all 115 selected files /
  26,219,104 bytes before pruning. The
  [manifest](./resources/tracking-retention-manifest.json) contains the exact
  member/hash restore map; the [promotion receipt](./resources/tracking-retention-promotion.json)
  records actual removals and accounting. The archive is owner-local, not a
  public artifact or an indefinite availability guarantee.
* Pruned only the 113 approved older preview images and two older duplicate
  PPTX outputs. Actual-removal journal matches all 115 paths. Full archive
  readback and protected-snapshot comparison pass before and after pruning;
  all 89 current native-build files, original PDF, mentor YAML, current
  duplicate deliveries and unknown-active RPI evidence remain byte-identical.
  Historical selected preview links are archive-backed, not live-local.
* All 37 archive tests, 24 source tests and six registry cases pass. Two
  independent promoted Builds and Verify runs preserve exactly the six
  slide/six note changes, 54 nonempty notes, timing, one shape 70001 and
  27 caller returns. Both candidates and canonical PPTX have identical ZIP
  member names/bytes. Missing/wrong baselines fail before output creation;
  both canonical/candidate cost guards pass. Canonical PPTX/PDF hashes remain
  unchanged.
* Actual Windows PowerPoint COM rendered the promoted candidate externally:
  PDF readback confirms 54 pages and recovered arithmetic, with 18 nonblank
  1600 x 900 previews. Native readback confirms 27 Last Slide Viewed actions.
  Offline cached PDF/image libraries supplied readback; system PDF CLI tools
  were unavailable. One pre-existing missing SVG link in the addendum remains
  outside scope; no new broken active link or fragment is introduced.
* Checkout reduction is separate from external archive storage and does not
  shrink Git history. No independent presentation review, accessibility
  acceptance, current primary-price verification, Finance approval, complete
  publication gate, PR-thread change, commit, push or cloud operation was
  performed. Parent-owned tracking plan/details/changes remain unchanged.

## [2026-10-24] query | PR 438 Handoff Corrections and Independent Retention Review

* Clarified original-route offline authoring versus current-v2 editing.
  The latter requires the native PPTX/PDF, refinement folder and dated
  corrections; the 18-slide source inventory cannot reconstruct 54 slides.
  Added the handoff regression and retained the cost-preservation contract.
* Reconciled all four build-receipt backlinks to the durable narrative,
  validation receipt and explicit local-only preview custody. The latest
  missing-receipt review comment is addressed locally, not yet published.
* Verified and resolved three older published-fix PR threads: exact deck
  path/size, qualified native labels and matching registry-test semantics.
  Other handoff/reset/navigation threads were already resolved externally.
  Left the latest receipt thread open pending publication; no commit or push.
* Independent implementation review completed with outcome Conformant and no
  new material findings. Rechecked 67 tests, exact archive/restore/prune
  evidence, protected source bytes, native packages and 859 links. Nine
  inherited link defects remain; none was newly introduced. The original
  adverse plan critique remains unchanged, with its corrections recorded.
* Current-task plan/details/changes were intentionally reconciled after the
  successful post-prune snapshot comparison. No older protected evidence or
  canonical deck bytes changed. Complete publication, current-price,
  Finance/funder, accessibility and presentation acceptance gates remain
  separate. Archive portability requires transferring and verifying its
  actual bytes, not only retaining the repository manifest.

## [2026-10-24] update | Entra-authoritative staff access, owner decision (#360)

* Recorded the owner's 2026-10-24 decision that verified Entra tenant, object id and explicit application roles determine staff login, with no SQL staff row or database read on the authentication path. Added a dated subsection to ADR 0002 (the ADR stays Proposed overall) with a reciprocal ADR 0001 lineage note, BRD v0.20.0 (CON-008, FR-053, FR-054, AC-104 to AC-109, NFR-003/AC-050 clarified), PRD v0.19.0 (DD-009, FR-062, FR-063, AC-111 to AC-117) and aligned the architecture and infra READMEs and the task-routing index.
* ApplicationAdmin alone is view-only (shows the manager option set; the server refuses state-changing requests). The 2026-10-13 SQL-binding observations are retained as history and superseded prospectively for sign-in only.
* Design and source only: not deployed, no role assignment readback and no real-user login observed. Earlier entries retained.

## [2026-10-23] update | Optional resident requirements and unregistered architecture proposal (#441)

* Integrated verified unsigned BRD v0.20.0 and PRD v0.19.0 source amendments
  after genuine Research, Plan/details and independent plan critique. Source
  hashes, reconstructed candidates, original FAIL/BLOCKED quality reports and
  namespace trace remain in portable issue-specific evidence.
* Prospectively reconciled FR-044/AC-084 and coupled rules for the owner-selected
  bounded routine communication proposal, separately gated and OFF. Named
  review remains default and always applies to consequential, sensitive,
  uncertain, safety, consent, contractual and financial content. No controlled
  authority is delegated. Proposed role ownership/shared timeline, managed
  external identity/scoped grants and assisted channels without detriment
  replace no settled legal/privacy/service gate.
* Added six synthetic resident scripts and coupled content/design/WCAG/profile,
  architecture/capstone and addendum routing without changing EXA-004 or
  historical staff/map denominators. Targets/scenarios remain proposals and
  author judgement, not measured benefits, production SLA or cash/headcount.
* Published architecture as an explicitly UNREGISTERED issue-specific working
  proposal with id null, selected Option B, original matching Excalidraw/SVG/
  same-model Chrome PNG and accessible text. Owner deferred registration after
  actual allocator/bootstrap failure: full registration acceptance remains
  UNMET, no new registry/config/lineage/Govern claim.
* Original case study, owner memory, numbered ADRs and earlier log entries
  remain unchanged. OD-52-55, formal/lifecycle and live approval remain open.
  This documentation-only proposal does not deliver a portal, live sending,
  real accounts/data, Azure change or paid inference. Independent final-byte
  Review and publication gate evidence are recorded separately, not implied
  by this authoring entry. Shared-path overlap with draft #424/#426/#439
  requires later reconciliation preserving all append entries; no sibling
  proposal is imported and no false issue dependency is created.

## [2026-10-23] update | Completed unsigned resident PRD and architecture refinement (#441)

* Integrated completed PRD v0.19.1 and the one reconciled architecture working
  candidate after a new genuine Research, Plan/details and independent critique.
  Exact immutable input hashes, source-to-integrated editorial/link mappings and
  prior working bytes are retained as selected portable issue evidence.
* All existing requirement definitions/IDs and 30 resident Not-run criteria
  remain unchanged. Twenty local stories, R0-R5 planning, six-journey verification
  and qualified full FR trace elaborate the proposal, not execute or approve it.
* Current independent PRD quality remains FAIL / Validate BLOCKED / Finalize
  NOT_EVALUATED, singular1<2, seven CAUTION/34 COVERED/zero RISK. All seven
  findings remain current, including bundles, unsigned BRD, feasibility/GOAL-005,
  OPEN generic/resident latency/file-size precedence, table shape and FR-059
  trace. Author-complete does not mean Validate/Finalize/Govern or live approval.
* The existing architecture location evolves as id:null/unregistered/proposed;
  prior draft/source bytes remain history, not competing decisions or accepted
  ADR supersession. Registration stays deferred/UNMET. Unchanged 47-element
  Excalidraw and same-model SVG/Chrome PNG retain text equivalent and truthful
  non-native-render provenance.
* Owner-selected Option B, default human review/routine OFF, assisted channels
  without detriment, scoped grants, OD-52-55/OQ-028-031 and live gates remain.
  Correction1 validation/navigation and bot/history are retained; A5/B6 generated
  score citations stay OPEN without manual score edits or paid scoring.
* Only directly coupled addendum/index/journey notices change; BRD, original
  case, owner memory, numbered ADRs and earlier log entries remain unchanged.
  Draft #439 cost/index/log overlap needs later reconciliation preserving both
  lanes. No application, sending, real account/data, Azure or paid inference
  is delivered. Native Review/technical gate evidence is separate; this entry
  does not attest a completed gate or authorize push/PR changes.

## [2026-10-24] restructure | Merge resident and staff-access requirements (#441)

* Merged the unsigned resident-service increment with the owner-directed
  Entra-authoritative staff-access requirements. Preserved the earlier resident
  identifiers and assigned staff access the following BRD IDs (FR-063/064,
  AC-127 to AC-132) and PRD IDs (DD-010, FR-072/073, AC-141 to AC-147).
* Updated the canonical BRD, PRD and task-routing index. The prior Entra entry
  above is retained as a record of the pre-merge identifiers; the PRD's 0.19.2
  history row likewise records those historical IDs and their reassignment.
  The resolved rubric score metadata is historical and does not assess this
  merged candidate. No new approval, acceptance or deployment is claimed.

## 2026-10-25 - AI Software Factory Related-Work Review

* Reviewed Pavlenko et al.'s
  [Towards an AI Software Factory for Data Systems, v1](https://arxiv.org/html/2609.36323v1),
  submitted 28 September 2026 and retrieved 25 October 2026, against the
  thought-leadership manuscript. Added matching versioned references to its
  embedded bibliography and reusable BibTeX, now 97 references.
* Integrated bounded objective-guided steering, behavioural feedback and
  evidence-scoped World Model context. Qualified the threefold application-work
  productivity estimate, its excluded 57% infrastructure/onboarding time,
  human review queue and the selected top-20 scope of the 13.8% OSS performance
  average. These are source-reported findings, not independent replication.
* Narrowed the novelty claim to scheduled consolidation between feature
  additions and subsequent changeability. Preserved hypotheses, thresholds,
  budgets, earlier study evidence and tagged materials. The separate private
  study kit was not accessed or changed; no study was run.
* Filed the assessment and source's inconsistent token-efficiency comparators
  in the [paper package](../capstone/thought-leadership/everything-but-the-software/README.md#related-work-review-of-25-october)
  and updated the task-routing index. The disputed multiplier is not imported
  into the manuscript. Existing owner memory and earlier log entries remain
  unchanged; publication and independent acceptance gates remain separate.

## 2026-10-25 demo basemap configuration (issue 119 demo slice)

* Recorded a scoped, time-limited owner approval (to 2026-10-25T16:02Z) to use the public OpenStreetMap tile service for the synthetic live demo, applied as a configuration-only change of `ZF_TILE_URL` and `ZF_TILE_ATTRIBUTION` on the existing demo app. The runbook entry is in the
  [infra README](../../infra/README.md) and the dated RPI artifacts are under `.copilot-tracking/*/2026-10-25/demo-basemap-119-*`.
* The tile usage policy and privacy policy were retrieved by the coordinator; the local regulatory snapshots were not changed. This is not a production provider approval and does not meet #119 licence, cost, coverage, processor or screen-reader acceptance. Earlier log entries are unchanged.

## [2026-10-24] update | Synthetic resident feedback preview indexed (#444)

* Added an index row for the loopback-only, read-only synthetic resident preview: separate `zava_forward.api.resident_preview` server, `zava_forward.core.resident_preview` boundary and a disposable invented fixture builder. See the src/api and src/core READMEs.
* Reuses the existing case and domain store behind a resident-owned positive-allowlist view and a default-deny server-side grant. PR 442 was read as unsigned input only. No staff server, auth, projection or store file changed.
* Not resident enrolment, not a live service, no real data. Live Azure/SQL/real-AI acceptance stays a separate later gate; #444 criteria stay open until proven on the final head.

## [2026-10-25] update | Synthetic resident showcase local slice documented (#462)

* Documented the local, unpublished implementation of the fake-email synthetic resident showcase: pure domain and read-only SQL adapter in [core](../../src/core/README.md#synthetic-resident-showcase-boundary-462), server, image and checks in the [API README](../../src/api/README.md#synthetic-resident-showcase-462) and the SQL view and read-only principal in the [infra README](../../infra/README.md#synthetic-resident-showcase-sql-boundary-issue-462).
* Separate from the #444 loopback preview, whose guard is unchanged. No real password, secret, Azure or live SQL access was used. Cloud deployment, budget headroom, live email equality, the private SQL job and Key Vault retrieval stay blocked. Not resident identity, not enrolment.

## [2026-10-25] update | Synthetic resident showcase review corrections (#462)

* Added the corrections for the #462 local slice review findings: a limiter source option for direct Container Apps ingress (`ZF_DEMO_CLIENT_ADDRESS`, last `X-Forwarded-For` entry only, peer fallback), login and per-request email binding to the start-up map, and an owner-run offline hidden-input verifier tool. See the [API README](../../src/api/README.md#synthetic-resident-showcase-462) and the dated RPI artifacts `.copilot-tracking/*/2026-10-25/resident-azure-showcase-462-corrections-*`.
* Local only: no push, no real password generated or entered, no Azure or live SQL access. Budget, live equality, SQL view and principal, and vault write path stay open. Earlier log entries are unchanged.


## [2026-10-25] update | Issue 462 release preflight cost and path evidence

* Added read-only release preflight evidence for #462 (refreshed Cost Management ledger, baseline versus changed resources, priced minimal deployment, principal and vault path metadata) under `.copilot-tracking/*/2026-10-25/resident-azure-showcase-462-release-preflight-*`. Raw non-secret metadata is kept privately outside the repository with a hash manifest.
* Not budget clearance and no Azure change; the cumulative USD 50 cap is not reset. Earlier log entries are unchanged.

## [2026-10-25] update | Issue 462 gate-failure correction cycle 1

* Fixed the optional SQL driver import that broke core test collection in the failed local gate, made the demo sign-out report success only on a confirmed response, and added targeted browser (sign-out failure) and `Dockerfile.resident-demo` image checks. See the dated RPI artifacts `.copilot-tracking/*/2026-10-25/resident-azure-showcase-462-gate-correction1-*`.
* The failed gate receipt is retained and stale; the generic runner still does not cover these checks. Local only: no push, no Azure, no real password. Earlier log entries are unchanged.

## 2026-10-26 issue 462 correction cycle 2

Added a module-scoped mypy ignore_missing_imports override for the optional mssql_python driver in src/core/pyproject.toml after gate-2 failed mypy. Plan, changes and review are under .copilot-tracking/*/2026-10-26/. Gate-2 receipt remains failed and retained.

## 2026-10-26 issue 462 owner-local secret delivery helper

Added infra/scripts/resident_demo_secrets.py and a fixed-name store_resident_demo path in credential_arm.py for the two resident demo secrets (dry run default, typed-phrase apply, expiry cap, fake-fixture tests). Plan, changes and one independent Conformant review are under .copilot-tracking. Tool authoring only: no Azure write, no real password, verifier or session key, no gate. The gate 4 receipt is stale for the new head; budget, provenance, SQL principal and private-vault write path remain open.

## 2026-10-26 issue 462 secret helper correction 1

FIFO-safe verifier file open, stronger malformed-value assertion and README dry-run wording. The reported namespace-env import failure traced to stale editable paths in a retained gate env; the runner reinstalls the projects, so no runner change. Local only: no gate, push or Azure.

## 2026-10-26 issue 462 execution-readiness local stage

Moved the resident demo authority end to the exclusive 2026-11-01T00:00Z cutoff across core, SQL, secret helper, docs and tests. Added the resident-only infra/resident-demo.bicep and infra/scripts/resident_demo_deploy.py (what-if deny guard, min 0 / max 1, no main stack or schedules). Local only; no cloud action. See the 2026-10-26 execution-readiness plan, changes and review under .copilot-tracking.
## 2026-10-25 query | Presentation Paper and Journey Story Review

* Updated the owner-selected 54-slide Cowork v2 PPTX and native PDF with
  the 25 October *Everything But the Software* draft, stage-linked journey
  hypotheses, a three-lane service blueprint and three representative graphical
  maps. Role instruments and map counts are not customer interviews or accepted
  features. The paper remains an exploratory author case and paused,
  registration-pending protocol with no study results.
* The PowerPoint Subagent built and natively rendered the revision. Independent
  communications review identified seven content/visual findings; the final
  read-only check found all corrected. Preserved the original findings and
  qualitative coverage of all 20 capstone criteria in the
  [dated review and reproduction handoff](../capstone/deck/cowork-generated/presentation-review-2026-10-25.md).
* Corrected historical-versus-current sign-in/Graph claims, unsupported
  completed legal review, activity-as-value narration and consent ownership.
  Restored the concrete backlog trace and distinguished the paper's PR/log
  date windows. Existing cost calculations, all 54 notes, timing, order and
  27 caller actions remain; the repository cost-preservation guard passes.
* Updated the current-output README and this index. Native property checks
  found zero issues and zero new native text overflows; inherited warnings
  remain recorded. This is scoped artifact/story review, not rehearsal,
  accessibility conformance, legal/control acceptance, experiment results,
  rubric scoring or publication clearance. No commit, push, deployment or
  paid inference occurred; concurrent owner paper work was not changed.

## 2026-10-25 - Thought-Leadership Editorial Critique Revision

* Revised the [paper source](../capstone/thought-leadership/everything-but-the-software/main.tex)
  and [revision account](../capstone/thought-leadership/everything-but-the-software/README.md#critique-revision-25-october)
  around observed completion/usability divergence, five candidate mechanisms
  and a prospective package-level consolidation test. Added construct and
  provenance boundaries, an observation--interpretation--proposition audit,
  bounded negative cases and a fuller rival-explanation matrix. No new
  empirical case dataset or independently checked qualitative coding is claimed.
* Moved extended practitioner accounts, informal observations and the detailed
  operating practices/checklist to appendices. The recommendations are
  implications for evaluation, not a separately validated model or permission
  to bypass required repository, safety or human approval gates.
* Added six verified scholarly references, with 103 matching bibliography
  entries. Corrected the critique's RefactorBench count to 100 tasks/nine
  repositories and distinguished Building to the Test's unchanged-oracle
  delivery-contract gap from test tampering. Recent preprints, abstract-only
  verification and unavailable HITS access remain explicit.
* At the owner's direction, preserved the tagged experiment, arms, hypothesis
  priorities/thresholds, budgets, sample and prior-run labels. Added a protocol
  summary and explicit resource, control, precision, multiplicity, annotation,
  CR1 exposure and unverified-access limits rather than silently redesigning
  the study. Private study files and earlier ancillary proposals are unchanged.
* The structural check passes; two external, shell-escape-disabled pdfLaTeX
  passes produce 42 pages with no warnings or unresolved references. Fresh AI
  editorial testing is not independent human peer review. Visual PDF review
  was unavailable; the existing PDF and arXiv bundle are preserved. No study
  run, commit, push, publication gate or external submission occurred.

## 2026-10-25 - Paper PDF Regeneration Clarification

* The preceding revision entry's PDF-preservation statement is superseded:
  a separate workspace compiler regenerated the PDF during editing even though
  the assistant's compilation commands targeted an external directory. The
  workspace compiler log records 42 pages; the observed PDF hash changed.
* The owner explicitly selected leaving the current regenerated PDF untouched.
  No Git-version restore or external-build copy was performed, and pre-edit
  byte preservation is not claimed. The arXiv bundle was not refreshed by this
  workflow. Source validation and publication/approval limits remain unchanged.

## 2026-10-25 ingest | Scientific Paper Writing and Review

* Added [Scientific Paper Writing and Review](./method/scientific-paper-writing-and-review.md)
  with original paraphrases of Drake and Han, Bosworth, Bushman and Pope,
  verified source identities, retrieval date and pinpoint guidance. Preserved
  the MDPI follow-up 403, Bushman's unverified publication date and text-only
  figure coverage rather than claiming fresh access or visual verification.
* Added [AMA Scientific Paper Writer and Reviewer](../../.github/agents/ama-scientific-paper-writer-reviewer.agent.md)
  with scoped write, revise and read-only review modes, claim-source evidence
  states, scientific-integrity boundaries and human ownership. Actual venue,
  confidentiality and AI rules take priority over optional writing heuristics;
  capstone guidance applies only when relevant.
* Updated the [reference index](./README.md) only for scientific-writing task,
  method and agent routing, and appended this ingest entry without changing
  earlier log entries. Manuscript, bibliography, PDF and owner memory are outside
  this authoring task.
* Independent static review, behavior scenarios and final validation remain
  pending. Authoring does not establish scientific acceptance, venue compliance,
  independent human peer review or publication approval.

## [2026-10-25] query | Paper layout and developmental revision

* Applied the owner-approved developmental improvements to the
  [paper source](../capstone/thought-leadership/everything-but-the-software/main.tex)
  and [package record](../capstone/thought-leadership/everything-but-the-software/README.md#reader-layout-and-developmental-revision-25-october).
  The subtitle now describes delivery-signal/usability divergence rather than
  implying measured feature-caused decay. Float options, selective barriers
  and the relocated mechanisms summary keep every numbered table on the
  same page or the next page after its first reference.
* The author selected an exploratory four-run-per-arm first pass. The private
  tagged kit, arms, thresholds, budgets, sample and prior-run labels remain
  unchanged. Later confirmatory use requires separately reconciled H4/H7,
  intervals/precision, multiplicity and failure rules; no numerical accuracy
  margin or replacement hypothesis rule is invented.
* Distinguished the operational sign-in obstacle from the consolidation
  hypothesis and period-level coexistence from a verified same-release
  score/journey contradiction. Missing dated source captures, deployment
  bindings and failed-journey traces remain unverified, not newly recovered
  evidence. Narrowed universal/causal claims and shortened repeated caveats.
* Added and disclosed Scientific Agent Skills with matching citations, after
  checking current arXiv metadata. The structural checker passes with 104
  references and results disabled. The external 43-page PDF has no final
  warnings or unresolved references; rendered-page inspection and table
  proximity checks were performed, not accessibility certification.
* The owner selected preserving the modified repository PDF and unrelated
  untracked research record on PR #460. External validation output and a
  session-local revised PDF remain separate. A workspace compiler regenerated
  the repository PDF during editing; the saved owner-selected bytes are
  restored after the final source change. No private study edit, experiment,
  commit, push, complete publication gate or independent exact-head
  assessment is claimed. The existing dirty/untracked work prevents the
  required clean-candidate publication gate.

## 2026-10-25 - Paper Source Reconciliation and Fresh Layout Inspection

* Reconciled the [paper source](../capstone/thought-leadership/everything-but-the-software/main.tex)
  with the existing draft v5 revision account after finding the source still
  used draft v4's title, restrictive table floats and confirmatory first-pass
  wording. The owner selected the current branch and preservation of existing
  changes, with an exploratory first pass and explicit pending H4/H7 decisions.
* Retained all legacy hypothesis thresholds without inventing accuracy margins,
  H7 endpoints or interval methods. Added the missing operational-failure
  bridge, same-release verification requirements, bounded literature wording
  and Scientific Agent Skills disclosure/reference. No missing empirical
  evidence, experiment result or private-kit reconciliation is fabricated.
* The [current build record](../capstone/thought-leadership/everything-but-the-software/README.md#current-source-reconciliation-25-october)
  supersedes earlier build figures for this source: the external PDF has
  42 pages and all twelve tables are on the same page or the next page after
  their first reference. Structural checks pass with 104 matching references;
  final compiler logs have no warnings or underfull/overfull boxes. Rendered
  layout inspection prompted removal of an almost-empty audit-section page.
* Preserved the pre-edit repository PDF separately and restored its saved
  bytes after source-triggered workspace regeneration. Current revised PDF
  and previews remain in session storage. Existing unrelated/untracked files,
  earlier log entries and the arXiv package are unchanged. Complete publication
  gates and independent exact-head assessment remain unperformed; no commit,
  push, study run or publication approval is claimed.

## [2026-10-25] query | Owner-authorised paper table flow and exploratory framing

* Applied the supplied developmental recommendations to the
  [manuscript](../capstone/thought-leadership/everything-but-the-software/main.tex),
  preserving its title and subtitle. The owner selected the existing PR #460
  branch, preservation of other changes and replacement of the revised PDF.
  This supersedes earlier PDF-preservation instructions for this revision.
* Used flexible table placement and selective barriers; moved the mechanisms
  summary beside its introduction and kept proposed practices in the appendix.
  All twelve tables are now on the same or next page after first substantive
  discussion. The [build record](../capstone/thought-leadership/everything-but-the-software/README.md#table-flow-build-record)
  records exact pages, a 42-page rebuild, rendered layout inspection, matching
  references and the existing tooling checks.
* The owner selected exploratory first-pass framing rather than seven
  confirmatory verdicts. Existing arms, thresholds, budgets and sample sizes
  remain; H4 accuracy non-inferiority, H7 endpoint/gap treatment, interval and
  fallback methods, and later confirmatory controls need prospective decisions.
  No private tag was changed or verified and no study was executed.
* Distinguished sign-in configuration recovery from the changeability
  hypothesis, bounded attention/scrutiny language, and made missing score,
  deployment and journey linkage explicit. No same-release verification,
  API/scorer capture or other missing evidence was invented.
* Added the Scientific Agent Skills method disclosure and matching embedded/
  reusable reference using the latest arXiv metadata retrieved on 25 October.
  Updated the index and package README; preserved earlier log entries and
  unrelated staged/unstaged/untracked work. Complete clean-candidate publication
  gates and independent exact-head assessment remain unperformed. No commit,
  push, publication approval or arXiv bundle refresh is claimed.

## [2026-10-25] research | Contextual repositories and the paper's steering hypothesis

* Extended the [paper](../capstone/thought-leadership/everything-but-the-software/main.tex)
  at the owner's request with prior Aithena experience and selected public
  observations from Aithena, corrected Squad and especially PhotoCraft.
  AMA remains the single principal case. The title, subtitle, role/affiliation
  and H1-H7 protocol are unchanged.
* The [source review](../capstone/thought-leadership/everything-but-the-software/README.md#repository-context-and-hypothesis-revision-25-october)
  distinguishes PhotoCraft's live-menu metric from behavioural parity,
  historical self-estimates from new measurements, bug reports from reproduced
  failures, and open queues from defect rates. It retains tests, fixes,
  consolidation proposals, alpha-stage scope and Aithena's dependency-heavy
  PR queue as counter-evidence and rivals.
* Added a [minimised dated observation record](../capstone/thought-leadership/everything-but-the-software/anc/repository-observations-2026-10-25.json)
  with source SHAs, queries, tracker counts, declared sampling, locators and
  exploratory candidate predictions. No external applications were executed,
  private standards accessed or reporter identities/attachments retained in
  the source package. Static Aithena traces do not establish runtime data loss
  or a measured complexity effect.
* Added matching repository references and disclosed Hypothesis Generation
  assistance under Scientific Agent Skills. A matched-resource future
  steering/oracle comparison is explicitly separate from the existing study;
  no framework superiority, human necessity or causal effect is established.
  Existing unrelated work and earlier log entries are preserved. Publication
  gates and independent exact-head assessment remain unperformed; no commit,
  push, study execution or arXiv bundle refresh is claimed.
* The [repository-context build record](../capstone/thought-leadership/everything-but-the-software/README.md#repository-context-build-record)
  records the inspected 44-page PDF, 107 matching references and final
  same/next-page placement for all twelve tables. Replaced `main.pdf` under
  the existing owner permission; the requested affiliation/no-email author
  block remains. Earlier build records are historical, not current evidence.
  Concurrent shared-branch activity included the source changes in commits;
  this editing session did not commit, merge or push. The final build record
  and inspected PDF remain local, without a completed publication gate.

## [2026-10-27] research | Industry-led paper framing and inherited state

* A read-only critique and source-research agents preceded changes to the
  [paper](../capstone/thought-leadership/everything-but-the-software/main.tex).
  The [revision record](../capstone/thought-leadership/everything-but-the-software/README.md#industry-led-revision-27-october)
  preserves source versions, locators, access limits and the final scoped
  critique. Knight Capital, WyCash and PhotoCraft now introduce the wider
  maintenance problem before AMA's triggering experience.
* Distinguished conversational self-conditioning from repository-carried
  faults and instruction maintenance. Added six matching references covering
  the SEC account, instruction-file histories, context-file evaluation,
  GitHub practitioner guidance and Anthropic context engineering. Context
  debt is attributed to prior work; entropy remains an engineering analogy.
* Added [published chart data](../capstone/thought-leadership/everything-but-the-software/anc/published-evidence.json)
  and two reproducible figures: paired-history event-resolution differences
  with published intervals, and overlapping instruction-edit labels. Retained
  clean-history and useful-context counterevidence; no net-token growth,
  reproduced external defect or new study result is inferred from them.
* The protocol is unchanged after line-ending normalisation. Structural
  checks pass with 114 matching references; chart-data, denominator and image
  checks pass. Tectonic produces an external 49-page PDF with resolved
  references, four minor overflows below six points, one underfull line and
  a fontconfig warning. The existing package PDF and case figures are
  unchanged. Python plotting dependencies were installed with pip at the
  owner's direction; the cancelled PDF-renderer install was not retried.
* Updated the reference index and package record without rewriting earlier
  log entries or the owner's memory. No private study edit, experiment,
  commit, push, complete publication gate or submission occurred.
## [2026-10-27] design | Resident advisory assistant prototype (Refs #469)

* Added the [owner-decision design](../architecture/resident-assistant-prototype.md)
  and index pointer: local fixed-topic rules, fresh own-case authorization,
  explicit unknown document requests and no submission/consent authority.
* Compared candidate small Azure models without claiming verified availability
  or tariffs. Documented the USD 5 additional ceiling through 2026-10-31,
  preferred managed identity and disabled adapter requiring future reviewed
  tariff and durable shared reservation controls. No model calls, Azure changes,
  real-provider activation or live resident acceptance is established.

## [2026-10-23] query | Current scoped cost and minimum development demo refresh (#126)

* Updated the existing Case Study 48 addendum cost proposal and index row with
  sanitized read-only evidence retrieved about 10:55-10:56Z: USD 261.82 reported
  RG `ama` actual and USD 457.34 conditional RG service-derived month-end total.
  Subscription actual/forecast reads failed; no retry or all-in completeness
  inference from the 91 visible resources, all currently in `ama`.
* All-in actual/forecast and comparable USD 700 headroom remain Unknown. Exact
  ingestion lag and complete post-change-day evidence remain unverified; no
  Front Door/WAF accrued charge was subtracted, and historical evidence stays.
* Proposed one shared two-hour existing-resource development window, public
  welcome distinct from signed-in feedback, minimal SQL/private Blob/bootstrap
  and one bounded real AI coordination draft. Exact incremental prices,
  cost-complete owner export, operator/technical readiness and separate finite
  approval block activation; expiry remains 2026-10-25T16:02Z.
* No Azure mutation, paid/data-plane call, private data/roster/secret read,
  site-usability claim, legal/DPO/pilot/production approval or #126 acceptance.
  OD-51 remains open without an invented denominator, quality floor or
  production economics. Earlier log entries are unchanged.

## [2026-10-21] query | Cut-over soak evidence preparation (Refs #201)

* Added to the [cut-over evidence pack](../architecture/cutover-evidence-pack.md#soak-and-cut-over-evidence-preparation-2026-10-21)
  a dated map of all 11 #201 acceptance criteria (all remain UNMET), dated
  corrections, a proposed soak evidence specification and pending owner
  decisions D1 to D16, plus one unchecked checklist item.
* Files touched: `docs/architecture/cutover-evidence-pack.md`,
  `docs/adrs/0006-src-layout-and-cutover.md` (dated note only), `docs/reference/README.md`
  (one row) and this log.
* Contradictions raised: the 2026-10-15 owner decision of no minimum soak
  versus the open soak item in the #201 body and the 2026-10-20 proposal
  request (not resolved, decision D1); the pack statement of no available rubric
  comparison versus later snapshots 47 then 48 (no candidate-commit score).
* Preparation only, per the owner direction of 2026-10-20. No soak, duration,
  sign-off, tag, deletion, Azure or budget action; minimum duration stays open.

## [2026-10-27] query | Resident managed-identity assistant implementation (Refs #469, #466)

* Updated the existing assistant design and index for the owner's USD20
  model ceiling, resident USD30 within renewed USD700 funding, managed
  identity, bounded own-case inference and permanent atomic SQL accounting.
* Recorded real regional Standard mini provisioning and tariff, explicit
  deterministic fallback, per-resident admission and no specialist/decision
  authority. Historical USD5 prototype evidence remains unchanged below the
  current design section. Funding renewal does not extend resident access.
* Resource provisioning and reachable old-revision health are not SQL/runtime,
  authenticated managed-identity inference, privacy or production acceptance.

## [2026-10-25] update | Resident PRD target applicability and draft backlog (#441)

* Recorded the owner's 2026-10-24 PRD decisions in PRD v0.21.0: resident-route
  ordinary API p95 <=2s (five synthetic sessions, 30 minutes) and 10 MiB
  resident uploads, with audience-based applicability that leaves NFR-002
  staff/core targets unchanged; provider-neutral synthetic identity fixtures
  with no provider selected; the first milestone composition (R0 plus
  PR442-S01 to S06). No new identifier, BRD change or approval was made.
* Aligned the unregistered proposal (id null, still unregistered), the dated
  addendum and the resident journeys note, and added an index row for the draft
  backlog under .copilot-tracking/changes/2026-10-25/. The backlog awaits owner
  acceptance; no implementation issue is created and no delivery date is
  estimable before engineering sizing.
* Finding pr442-qual-041 has corrected authored text awaiting fresh independent
  review; the other six findings, OD-52 to OD-55 and registration UNMET remain.
  Earlier log entries are unchanged.

## [2026-10-25] update | Resident target applicability correction cycle 1 (#441)

* Corrected PRD v0.21.0 target-applicability text: staff rules apply to every
  staff-audience request, including one sharing implementation with a resident
  route, and never to resident-audience requests; shared implementation does
  not decide applicability. Added promotion-to-staff-evidence, unlisted
  resident class, unit and open sample-definition notes. A scoped independent
  quality review found no residual contradiction; it is not a full-PRD pass.
  The PRD stays unsigned and the prior entry above is unchanged.

## [2026-10-25] update | Resident backlog paired-protocol freeze correction (#441)

* Moved the paired effort and adverse-outcome protocol freeze into draft backlog item RB-01 (R0) and made all comparison runs depend on it; RB-21 now only collects and reviews results in R5. Documentation and draft backlog only; the PRD stays unsigned, the proposal unregistered and owner acceptance pending. Earlier entries are unchanged.

## [2026-10-25] update | Resident R4 gating split and promotion wording (#441)

* Owner-authorised bounded follow-up: the draft backlog and unregistered proposal now separate the R4 task-release gate (RB-17/18) from the OD-53 routine-dispatch gate (RB-19/20), and the proposal's staff-promotion wording matches the PRD guardrail. Documentation only; PRD unsigned, proposal unregistered, owner acceptance still pending. Earlier entries are unchanged.

## [2026-10-27] query | Historical backfill stack and explicit blockers (Refs #177)

* Updated the existing IoT research plan and index with five unmerged child
  PRs, bounded exercise projection/retrofit/household components, pending
  source reuse and consumer identity decisions, and conditional three-daily
  capacity accounting. No private register or household records were read.
* Reproduced actual consumer `IDENTITY` refusal for a public synthetic
  stock observation while its valid control passed. This confirms the
  previously documented compatibility gap, not a new admission contract.
* Files: `docs/reference/research/iot-sensor-analytics-research-plan.md`,
  `docs/reference/README.md` and this append-only log. Parent is draft
  coordination only; no child integration, acceptance tick, owner deferral,
  merge, climate reuse approval, Azure action or real monitoring authority.

## [2026-10-27] query | Approved historical backfill integration continuation (Refs #177)

* Recorded owner-approvals-2026-10-27-b prospectively: candidate climate
  synthetic-demo reuse, canonical stock IDs and authorized child integration.
  Original blocked stack findings and Residual work Review remain unchanged.
* Added hash-pinned genuine 2023-2024 paired ERA5 reanalysis and separate NASA
  2023 sensitivity evidence; source attribution and unverified production/legal
  terms remain explicit, not converted into unrestricted reuse approval.
* Updated the existing IoT synthesis and index for canonical IDs, independent
  consumer controls, opt-in composed models and the actual aggregate evidence
  boundary. Generated public stock does not prove unread private-register equality.
* Files: existing IoT research plan, index, climate evidence directory and this
  append-only log. No memory/regulatory snapshot edit, private data, real device
  activation, physical calibration, main merge or operational acceptance.
* Aggregate run reconciled every ID and all 43,800,000 daily readings for the
  public 60,000-home fixture over 730 days; 703,111,263 compressed reading bytes.
  Full core 1,427 tests (186 expected skips), static/types and actual owned SQL
  sensor/API 45 tests passed. Original Review and one scoped parent publication
  gate remain separate, not implied by this runtime evidence.
* Original approved-integration Review executed Complete / Not accepted at
  263e1dbf: one Medium composed-loader budget defect RV-001, routed to later
  implementation without rewriting or repeating Review. Preserve successful
  aggregate evidence but keep parent draft. Single scoped gate is pending at
  this committed source checkpoint; receipt and publication facts remain external.
* The sole scoped parent gate attempt at1b3f623f against fresh main2e031c89
  exited1 before checks: candidate does not descend from reviewed main base.
  No receipt, retry, push or ready transition. Preserve external failure log;
  coordinator must authorize normal main integration and a new scoped gate
  after RV-001 correction. Archive/restore-verified finite cleanup succeeded.

## [2026-10-27] query | Later authorized backfill replay-budget implementation (Refs #177)

* Standing owner authorization selects RV-001 correction, current-main
  integration and one fresh scoped foreground publication gate. Normal merge
  retains every child ancestry; original critique, Not accepted Review and
  failed ancestry gate remain unchanged, with no repeated Review.
* Composed replay now compares manifest home count with actual granted stock
  and budgets actual nominal rows and stock metadata before scratch/output.
  Bounded regressions cover forged counts, accurate oversized requests,
  zero-granted metadata limits, valid zero-row and exact-budget replay.
* Updated core loading documentation, existing IoT synthesis and KB index.
  Gate/hosted publication evidence remains external and distinct from this
  source checkpoint. No private data, physical/production acceptance, human
  approval, issue closure or main merge is asserted.

## [2026-10-27] query | Source-only IoT infrastructure definition (Refs #140)

* Recorded the owner's 2026-10-27 ADR 0003 authoring authorization: Free/B1
  envelope, `ama`/`uksouth`, overall USD700 cap, never delete `ama`, no deployment.
* Corrected the existing keyless-consumer claim using official Microsoft
  guidance retrieved 2026-10-27: the built-in IoT endpoint still requires a
  shared service key; managed-identity consumption uses a dedicated custom
  Standard Event Hub. Recorded the separate system-sender/API-receiver scopes,
  private endpoints and trusted-service routing exception.
* Corrected diagnostic minimisation: connection and identity-operation logs
  also contain device IDs. The source now exports metrics only and explicitly
  disables resource logs; this is not historical log erasure.
* Filed the public B1/TU/ingress price inputs and explicit unverified
  endpoint/variable allowances in a USD60/month transport scenario, inside
  rather than additional to USD700. Actual currency, commitments and remaining
  aggregate headroom remain unverified and block provisioning.
* Updated `infra/README.md`, ADR 0003 and the knowledge-base index. Explicit
  bootstrap omits endpoint registration; later activation requires separate
  approval and actual sender-role propagation. Individual device credential
  work remains #185; SDK transport #110 and BRD OD-43 human gates remain open.
* No Azure what-if, deployment, secret read, device creation, operational
  approval, issue closure or full RPI gate is claimed.

## [2026-10-27] restructure | Owner-authorized source cut-over (Refs #199-#203)

* Owner explicitly SIGNED OFF cut-over #201 on 2026-10-27 in the retirement
  task direction. Added the dated record to the
  [existing evidence pack](../architecture/cutover-evidence-pack.md#owner-authorized-directory-retirement-2026-10-27)
  and ADR 0006, preserving original failures and unchecked historical gates.
* Verified fetched main `65a514ed20e97816dbf47e9fb981ab4cfe40597d`:
  executable code/tests/images/CI/Bicep/scripts already use `src/`;
  only the pointer remained, and the earlier prototype was already absent.
  Removed the pointer; no private data or backups were inspected.
* Created locally absent annotated archive `v0.21.0`, matching current BRD
  version `0.21.0`, at that last pre-deletion commit. The owner, not the
  agent, publishes it with
  `git push origin refs/tags/v0.21.0:refs/tags/v0.21.0`.
  No tag push or GitHub release is claimed.
* Updated repository/source/architecture guidance, capstone registry table,
  active PRD location clarification, rubric summary, parity navigation,
  regulatory UX source path, coordinator source-layout note and KB index.
  Workflow/check names, memory,
  original case study, historical reports/audits and earlier log bytes remain
  unchanged. Historical/defensive old-path strings are classified in the
  evidence pack, not globally rewritten.
* Additive repair map for earlier log links into the removed guide:
  the two Entra/CSP entries now resolve through
  [current account behavior](../../src/api/README.md#entra-id-on-container-apps);
  the honest-limits entry through
  [current limits](../../src/api/README.md#honest-limits);
  the five-assistant configuration entry through the
  [migrated assistant guide](../../src/agents/README.md#five-retrofit-assistants-2026-10-13-implementation).
  Earlier link text and targets are intentionally untouched.
* Scoped existing tests and reference/link checks support this maintenance
  change, not full-suite parity, hosted CI/deployed health, private backup
  verification, post-merge rubric comparison or whole-issue closure.
  All five issues remain Refs; owner merge and remaining acceptance are separate.
## [2026-10-27] deployment | Merged resident features from PR #474

* Updated the [resident guide](../../src/api/README.md#synthetic-resident-showcase-462),
  [assistant design](../architecture/resident-assistant-prototype.md) and index
  with the supplied 08:59Z USD30 authorization, including USD20 AI subcap,
  MI-only boundary and expiry 2026-10-31T23:59Z.
* Deployed merged source 885ee05f and its required resident projection view.
  Retained the original failed startup caused by missing sensor columns;
  transactional exact-merged view deployment changed no table/row/grant.
  Twenty-seven actual unauthenticated HTTPS/Playwright checks passed.
* Registered-login, authenticated own-case account/gauges/history/assistant/
  sign-out and natural session expiry remain unproved because the owner-held
  password was not read. No model was provisioned: runtime MI/ledger wiring
  is absent, so deterministic rules remain. No production/human acceptance.
* Restored exact ACR policy. Final resident ingress disabled, tested revision
  inactive/zero replicas; all four app minima 0, eight Manual jobs and SQL
  Standard/10 DTU preserved. Publication gates and independent Review are
  recorded separately; this entry is not hosted or human approval.

## [2026-10-27] query | Indoor outdoor-record-derived exercise bounds (#179)

* Updated the existing IoT research synthesis with a dated three-criterion
  #179 audit and indexed it in the knowledge-base README; core README records
  the v2 equations, assumptions, envelopes and changed seeded-value boundary.
* Both indoor paths now derive bounds from each supplied outdoor pair and
  dwelling/household model with explicitly exercise-valued capped noise,
  replacing the fixed 8 C floor and 15..98% clips. Physical RH saturation
  remains distinct from an exercise threshold.
* Added independent equation/envelope, RNG order/state, forced-tail,
  saturation, domain/sensitivity and pinned public hourly-history tests.
  No new climate retrieval, private data, calibration or live approval.
* Preserved original historical stack, aggregate hashes, adverse Review and
  legal/operational blockers. Model-consistent synthetic bounds do not close
  parent #177 or establish PRD AC-066--068, OD-43 or real-dwelling physics.

## [2026-10-27] query | Indoor snapshot versioning correction (#179, PR #502)

* Filed the deliberate projection-v2 row-change decision in the existing
  synthetic-data determinism/versioning synthesis, core README and index.
  New default/stock/composed/fault snapshot versions distinguish new bytes
  without changing fault algorithms, reading schemas or published datasets.
* Preserved the original sensor golden hash as historical evidence; current
  golden binds literal snapshot/model versions. Scale/register goldens remain
  unchanged. Current loaders reject stale snapshot versions, while privacy
  auditing still recognizes historical and current stock snapshot layouts.
* Original targeted validation and adverse hosted failure remain in dated RPI
  evidence. The correction requires exact full core CI tests, lint and mypy;
  no cloud, private dataset, heavy gate or real-use approval is introduced.
## [2026-10-23] update | First bounded local stabilization checkpoint (#440)

* Added the executed current-main checkpoint to the existing cutover evidence
  pack and indexed it, pinning source140d8f49, preliminary candidate d8a65061,
  BRD0.19.0/PRD0.18.0 and ADR blobs/statuses. Runtime inputs were byte-identical
  to merged main; policy candidate evidence is separate.
* Recorded174 focused passes and five final standalone suites2392 discovered/
  468 skipped, with original archive-harness failures and corrections retained.
  Actual native Chromium/axe, disposable SQL Server244 tests (one JSON-only
  skip), four Docker/non-root/scanner/SPDX groups and logo0600 check ran.
* Preserved the failed full receipt: core SQL filtered read17383ms exceeded
  the unchanged1500ms bound. Three focused retests passed106-108ms but do not
  repair it or establish cause. Native host discovery remains Deferred despite
  static and independently graded simulation passes.
* No confirmed stable code defect/refactor, new bug issue, source feature,
  private/cloud/paid inference operation, acceptance tick, final release pass
  or publication is claimed. #349/#350/#360/#432 and human gates remain;
  independent lanes continue while affected validation/publication is blocked.
  Earlier log entries, original case study and memory are unchanged.

## 2026-10-25 stabilization checkpoint main reconciliation (#440)

* Merged main `ea5577b2` into the #440 branch without rewriting history and appended a dated reconciliation note to the [cutover evidence pack](../architecture/cutover-evidence-pack.md#reconciliation-with-later-main-2026-10-25-440).
* The first checkpoint is kept as historical evidence for main `140d8f49`; native discovery is recorded as attested only, the failed 17383 ms receipt remains a repository record with unknown root cause and an unwaived threshold, and no acceptance, Conformant outcome, publication or cloud approval is claimed.
* Earlier log entries, the original case study and memory are unchanged.
## 2026-10-25: obsolete synthetic proof case removed from the live demo database

* Removed the single obsolete synthetic proof case from the deployed `retrofit` database at the owner's request (issue 360): 981 to 980 cases, 444 to 443 open, one appended audit entry, no seed case or earlier audit row changed. The API cache needs a revision restart after an external delete.
* Recorded the route, guards and limits in the [infrastructure runbook](../../infra/README.md) and the dated `remove-synthetic-example-360` RPI artifacts. No source, image, deploy or configuration change.

## 2026-10-25: correction to the synthetic proof case removal entry

* Corrects the entry above: the earlier 17 audit rows were not compared per row. Preservation is inferred from a verified chain (count 17 to 18, head equal to the audit head) and the append-only ledger, not proven by row or hash comparison. The superseded draft phase details are marked as not a runbook. Documentation only; see the [review correction](../../.copilot-tracking/reviews/2026-10-25/remove-synthetic-example-360-review.md).

## 2026-10-28: ledger-history correction to synthetic proof case removal (#360, PR #459)

* The earlier removal entries describe removal of the current row and active-case projections, not data erasure. The live `cases` table is an updatable ledger table; its old body remains in system-managed ledger history. The non-history reference scan does not prove erasure, and the audit trigger is an alternative for non-ledger databases, not additional live-ledger protection.
* Corrected the [runbook](../../infra/README.md#historical-deployment-recipe), added a [dated research correction](../../.copilot-tracking/research/2026-10-25/remove-synthetic-example-360-research.md#schema-correction-2026-10-28-pr-459-review) without changing the original text, and qualified the related plan and changes evidence. Updated the index and [existing review artifact](../../.copilot-tracking/reviews/2026-10-25/remove-synthetic-example-360-review.md#ledger-history-correction-cycle-2026-10-28-pr-459); no new full RPI loop or live verification.

## 2026-10-28: briefing browser harness source binding (Refs #517, #516)

* Refreshed only the public recipe SHA-256 in the [scenario manifest](./research/retrofit-synthetic-data/scenario-manifest.json) after correcting the [shared-IA browser check](../../src/api/checks/workbench_browser_check.py) to match #516's programme-neutral loading copy and scope/count response fields. The stale text wait reproduced PR #517's 30-second failure locally, including correct loading with external requests blocked; no CDN flake was identified.
* Fixture IDs/defaults, inventory and manifest versions, unavailable full-journey status, pending owner review and all authority boundaries are unchanged. This source-binding maintenance is not a new scenario iteration, private-data read, full journey acceptance or operational approval.
## [2026-10-21] query | Meaningful human-review protocol preparation (#223)

* Added a proposed, Not run protocol section to the existing agents README
  evaluation area and indexed it: seeded wrong/stale/unsupported/incomplete/
  valid-citation-error case classes, baseline and automation-bias controls,
  retention fields, OQ-017 authority evidence, denominators and full-effort
  comparators.
* Prepared under the owner's 2026-10-20 preparation direction. All thresholds,
  samples, roles and approvals are PROPOSED or UNFILLED; no participants,
  model calls or execution. #108 remains open and the #222 manifest is an
  unapproved external prerequisite. No #223 criterion is met.

## [2026-10-21] update | Human-review protocol Pass preconditions (#223)

* Corrected the proposed, Not run protocol after an independent publication
  assessment: documented per-class and per-task reviewer competence and
  authority, resolved OQ-017 decisions and the required approvals are now
  explicit preconditions for execution and for any Pass. Missing evidence means
  Insufficient or NOT RUN, never Pass.
* No exercise, evaluator, outcome or approval was added. OQ-017 stays open and
  all five #223 criteria stay unmet. The earlier entry is unchanged.
## [2026-10-20] query | Map tile provider licence, cost and privacy options (#119)

* Added the [options review](./research/ux/map-tile-provider-options.md) and a
  dated ADR 0002 decision 5 delta, and extended the WCAG baseline manual check
  record with a map list screen-reader protocol.
* Sources are public vendor and policy pages read 2026-10-20 with no private
  coordinates. Azure Maps paid rate, Microsoft and OS processor terms, OS plan
  prices and MapTiler commercial terms could not be verified and are listed.
* No provider was selected, bought, configured or approved. No screen reader was
  available on the host, so no screen-reader run is claimed and the human or
  assistive-technology gate remains unmet. No UI file changed.

## [2026-10-20] correction | Map options provenance clarification (#119)

* The map tile options review and screen-reader protocol logged above were first
  drafted before the RPI skills ran, then re-checked through recovery research,
  plan, critique, implement and review. The re-read evidence (OSM tile policy,
  Azure Maps pricing page, code and tool availability) was confirmed, and an
  inconsistent secondary Ordnance Survey rate was labelled unverified.
* Conclusions are unchanged: no provider selected or bought, no screen-reader
  run, human gate unmet.

## [2026-10-20] correction | Map options budget wording (#119)

* Corrected the cost wording in the [options review](./research/ux/map-tile-provider-options.md):
  the owner budget is USD500 in total for the October 2026 calendar month,
  including accrued and forecast costs across resource group `ama` and other
  scopes. A separate finite costed execution plan must be approved before any
  paid execution, not only before account creation. The proposal authorises no
  spend, and unknown headroom blocks paid execution.
* Prompted by an independent assessment that returned Defects on the earlier
  head. No provider selection, purchase, legal or DPO approval, UI change or
  screen-reader run is claimed; the screen-reader gate and vendor rates, terms
  and DPA positions stay unverified.

## [2026-10-23] correction | Map options evidence labels and budget currency (#119)

* An independent review of the options proposal found two defects. First, the
  cost paragraph in the [options review](./research/ux/map-tile-provider-options.md)
  still presented USD500 as the owner ceiling and USD 535.41 as governing
  evidence. It now states them as dated superseded history, records the
  replacement USD 700 all-in ceiling, the unchanged 2026-10-25T16:02Z expiry and
  Unknown all-in headroom, and links the
  [addendum budget decision](../case_study_48_addendum.md#revised-owner-budget-decision-2026-10-22).
  This supersedes the budget and verification wording of the two 2026-10-20
  entries above; they are retained unchanged.
* Second, vendor statements that the recovery research recorded as not re-read
  were written as established. The options review and the ADR 0002 map delta now
  label them draft, unverified, or secondary, unverified, and only the OSM tile
  policy and the Azure Maps pricing page free allowance are marked re-read. The
  earlier recovery completion claim that these labels were applied was not
  borne out; this is an honest correction, not a new verification.
* Documentation only. No provider is selected or bought, no terms, DPA, rate,
  licence or processor decision is made, no web retrieval was done, the screen
  reader remains not run, and both original issue criteria remain unmet.
## [2026-10-21] query | Paired historical climate access check (#178)

* Tested anonymous retrieval of official paired North-East temperature and
  humidity records. MIDAS Open files require a CEDA login and EA Hydrology
  has no humidity or dew point, so no records were retrieved and no bounds
  were derived.
* Added the access-blocker record, a synthesis section and index row. The
  owner action is an authorised human supplying MIDAS files from their own
  account with reuse approval, or approval of another source.
* Source selection and licence/reuse remain UNMET, synthetic data is not
  substituted for observations, and the issue criteria stay unticked.

## [2026-10-22] query | Modelled paired historical climate source (#178)

* Following the owner decision of 2026-10-22, retrieved a fixed anonymous
  hourly Durham 2023 sample from Open-Meteo (ERA5) with a NASA POWER
  cross-check, hash-pinned under the climate sample folder, and derived
  temperature and humidity sample bounds with a validating adapter that
  rejects gaps, misalignment and inconsistent humidity.
* The source is labelled modelled, not observed. The two modelled sources
  differ (about 1 degC and 8 humidity points mean absolute), so accuracy is
  demonstrator level only. Production precision, licence and commercial-use
  confirmation, underlying C3S terms and regional representativeness remain
  pending and no approval is asserted.
* The 2026-10-21 MIDAS blocker and the Durham temperature-only report are
  unchanged. Issue criteria stay unticked.

## 2026-10-22 climate paired source: monthly timestamp correction (Refs #178)

* Corrected the modelled paired climate report after independent review: monthly
  minimum and maximum now carry every tied UTC timestamp and the paired value,
  regenerated from the same retained Open-Meteo records with tests for ties,
  provenance and reconciliation with the annual extremes.
* Earlier entries and the first gate receipt are preserved as historical. The
  source stays modelled, not observed; licence and reuse confirmation, production
  precision and representativeness remain pending, and issue criteria stay
  unmet. No legal approval is inferred.

## 2026-10-22 climate paired source: precise NASA attribution (Refs #178)

* Corrected generated NASA attribution to carry `POWER Hourly API` version
  `v2.10.3` from the hash-pinned retained response and its retrieval date
  2026-10-22, rather than static wildcard text. Missing or imprecise optional
  API metadata yields explicit `UNVERIFIED` attribution without changing
  climate-input rejection behavior.
* Report statistics, raw fixtures and source selection are unchanged. Licence,
  reuse, human owner/legal decisions, production precision and regional coverage
  remain unresolved; no issue acceptance criterion is ticked.
## [2026-10-20] query | Fictional form template and Finance decision review pack (#97)

* Added a registered fictional versioned form/template pack and reviewer guide
  over the existing form schema contract, with field type, unit, requirement,
  authority, evidence, freshness and lineage, proposed preparer/reviewer
  separation and stale propagation, and fourteen unresolved Finance
  authority/binding decision fields. Indexed it, the dictionary subsection and
  the core guide pointer. No runtime, API or schema engine changed.
* The pack is not an approved template, with no submission, payment, grant term
  or Finance signature. Issue #97 criterion 1 (actual authority and binding)
  stays unmet pending a named human authority; criterion 2 was delivered earlier.
* Process note: an earlier uncommitted draft was hand-authored before the RPI
  skills were activated. It is preserved with a dated disclosure and was
  re-verified through the executed research, plan, implement and review skills.

## [2026-10-23] lint | Corrected form review pack registration claims (#97)

* Files touched: the fictional form review guide, the core guide paragraph on the review pack, and this log (`ms.date`).
* Contradiction found by independent full-diff review (FIN-001): both documents said the public fictional schema registers unchanged, but `register_schema` refuses its placeholder reviewer, and the focused test expects that refusal before registering a derived copy with a registered reviewer substituted.
* Corrected both statements: the public file is refused as published; only a copy differing in `reviewer`, set to an existing registered person, registers, as `Unapproved`, recording no approval. No runtime, test, fixture, index, dictionary or provenance change; Finance FD-01..FD-14, template authority and OQ-015 stay unresolved and criterion 1 unmet. Earlier entries retained.
## [2026-10-20] query | Cohort and missing-data evaluation manifest preparation (#222)

* Added a DRAFT, UNAPPROVED, NOT EXECUTED wholly synthetic paired-scenario
  manifest to the existing eval registry and an owner [review pack](./research/evaluation/cohort-evaluation-review-pack.md)
  with proposed held-out custody, independent reviewer, small-sample,
  critical-error, review-burden and uncertainty handling and an AC1 to AC6
  traceability table. Owner decision 2026-10-20 authorised preparation only.
* Retained adverse evidence: ranking policy 1.0.0 is an unsigned draft, and
  support Unknown currently sorts with No (candidate defect, owner decision
  pending). The manifest is a development draft, not a held-out set; expected
  outcomes are agent-authored proposals and numeric values are illustrative.
* No evaluator, model run, participant, live data, threshold approval or
  fairness evidence. All six #222 criteria and the #108 actual-model and human
  results remain unmet.

## [2026-10-20] query | Cohort manifest correction v0.2.0 returned for owner approval (#222)

* Owner-authorised correction of the draft [review pack](./research/evaluation/cohort-evaluation-review-pack.md)
  and manifest (v0.2.0): split the multi-factor pairs, bound deterministic
  expectations to the unchanged `rank()` through the structural test, replaced the
  arbitrary 30 and 10 percent with sample-size, error-rule and uncertainty options,
  kept zero critical misses as a proposal, made Unknown-support review priority a
  policy proposal only, defined review burden over eligible cases, required fresh
  held-out scenarios with new IDs and limited the test support exemption to
  `support_state` pairs.
* Reviewer, adjudicator and custodian roles remain unfilled. No ranking change,
  evaluator, run, participant, data, approval or fairness evidence. All six #222
  criteria remain unmet; the manifest is returned for owner approval before any
  evaluator work.

## [2026-10-21] query | Cohort manifest correction after independent assessment (#222)

* Corrected the draft [review pack](./research/evaluation/cohort-evaluation-review-pack.md)
  and manifest wording: inside an open safety case the ranking order is support,
  then waiting days, then stage, then case id, not "behind only older open
  safety cases". The structural test now carries the sensor, source and
  appointment fields to the ranker input and proves a missing-data exclusion or
  appointment penalty fails the binding check. The contact_need pair stays
  representation pending because ranking has no contact input.
* Ranking, runtime and the unapproved status are unchanged. All six #222
  criteria remain unmet.

## [2026-10-28] query | Whole-project Responsible AI review

* Evidence: added [project RAI synthesis](./research/rai/project-rai-review.md)
  and dated six-phase artifacts under
  `.copilot-tracking/rai-plans/2026-10-28-zava-forward-project/`; updated the
  knowledge-base index. Repository-only review covers both sites, five
  bounded assistants, resident/employee chat, briefing, IoT, data and
  infrastructure at `9bfed51863b05a25e9939d82504c576524688e14`.
* Evidence: retained prior findings and exposed hazard-language limits,
  divergent chat routes/no-AI scope, consent/retention distinctions,
  Unknown-support ordering, synthetic/provenance limits, sensor-document
  drift and unlocked-retention wording. Open PRs remain candidates, not fixes.
* Hypothesis: twelve proposed backlog items reuse existing issue references;
  no GitHub issues, source edits, private dataset/secrets reads or Azure
  actions. Unknown: qualified approval, legal currentness, representative
  outcomes and human/accessibility acceptance.
* Evidence: mandatory complete publication gate includes `az bicep` commands
  forbidden by the task; no passing complete receipt or publication waiver is
  claimed. The dated assessment records validation/publication limitations.
## [2026-10-28] ingest | Employee case journey workspace specification (#526)

* Filed the owner-supplied [employee case workspace design](./research/ux/employee-case-workspace-redesign.md)
  and registered it in the knowledge-base index. Preserve slide order, with
  Funding and Resident agreement done only when the recorded evidence supports it.
* Implemented native journey/summary/tab composition in the current `src/api`
  web assets without changing the Fluent foundation or server decision rights.
  Journey and missing confidence stay client presentation, not invented API fields.
* Flagged the chat API limitation: informational turns have no recorded-review
  identifier; existing separately requested proposals retain source verification
  and human review. Live verification, screen-reader and real-staff acceptance
  remain pending the owner. Automated results are engineering evidence only.
* Final heavy-validation admission exhausted 40 one-minute nonblocking retries.
  Targeted tests and static checks passed, but complete API/browser/axe/zoom
  validation, independent Review and publication remain blocked/pending.
  No push, pull request or complete RPI success is claimed.

## [2026-10-28] validate | Employee case journey continuation (#526)

* Preserve the earlier blocked run and original RPI evidence. The owner
  authorized another bounded lock window, independent review and topic PR.
* Actual local API discovery passed 1156 tests (314 opt-in skips). Constructed
  journey checks pass 37 pinned axe states, retained drafts, keyboard reviews,
  blocked final-check refusal and real 200% browser zoom. Existing workbench,
  employee recovery, assistant, provenance, regulatory and challenge checks pass.
* Corrected mobile summary spacing without shrinking text or hiding values;
  measured bottom 1581.96875 at 320x800 is below the unchanged 1600 bound.
  Keyboard-focused tabs now scroll fully into view, including at 200%.
  Local gate parity includes the hosted journey check and bound result evidence.
* Updated the [design boundary](./research/ux/employee-case-workspace-redesign.md)
  and index. These are engineering observations, not screen-reader, staff,
  legal or deployed acceptance. Independent Review and final publication gates
  remain separately recorded steps; no cloud action is authorized or performed.

## [2026-10-28] refine | Independent journey review and routed repairs (#526)

* Preserve the original Complete / Defects found Review. Its four findings
  route to a later implementation: local harness import parity, same-card
  draft clearing, async proposal review edits and document review counts.
* Repaired these boundaries with explicit submitted controls, ID/revision-safe
  restoration and copy recovery, and known-local counts alongside unknown
  assistant totals. New journey 37-state axe/keyboard/actual-zoom checks and
  27 assistant scenarios pass. Full committed publication gate is still a
  separate pending requirement. Human and deployed acceptance remain unchanged.

## [2026-10-28] maintain | Journey gate public recipe binding (#526)

* The first complete gate correctly rejected a stale workbench recipe SHA-256
  and two over-100-column regulatory harness expressions. Preserve its failure.
* Refresh only the [scenario manifest](./research/retrofit-synthetic-data/scenario-manifest.json)
  source hash for retained-tab selectors and wrap the two expressions.
  Public fixture payloads, versions, inventory review and unavailable full
  journeys do not change; no private record or owner approval is inferred.

## [2026-10-28] refine | Loading feedback and HAX briefing (#531)

* Update the [design-system inventory](./research/ux/design-system.md) and
  [API guide](../../src/api/README.md#loading-feedback-and-todays-briefing-531)
  for shell loading/slow/retry, shared immediate async text and 200ms spinner,
  native pending controls, explicit AI/rules labels, declared statement
  references and conditional outcome-led draft reviews.
* Preserve draft-only immutable review, human approval and manual paths.
  HAX/Fluent sources are pattern references, not employee user research,
  accessibility conformance, full Fluent adoption or live-site acceptance.

## [2026-10-29] query | Employee chat skills design (#530)

* Filed the one-agent/five-skill versus router comparison in the
  [API guide](../../src/api/README.md#employee-chat-with-bounded-skills-530)
  and linked it from the index. Explicit selection avoids another model hop;
  no measured cost or latency improvement is claimed.
* Preserve role projection, privacy admission, minimal metadata audit,
  workflow-only fallback and human authority. Local checks do not establish
  actual SQL/live-site/model acceptance, screen-reader/voice-control acceptance
  or a complete publication gate.

## [2026-10-29] refine | Whitepaper judgment and skills sources

* Add the two owner-selected sources, retrieved 2026-10-29, to both
  bibliographies and the existing argument. The
  [source ledger and methodological dispositions](../capstone/thought-leadership/everything-but-the-software/README.md#judgment-and-skills-source-revision-29-october)
  distinguish Anthropic's analyst influence study from Zava evidence and
  Jiang et al.'s procedural skill/history comparisons from repository decay.
* Clarify agent/skill definitions, selected-episode versus matched-trajectory
  inference, missing access/use traces and approval versus independent
  judgment. Preserve observations, pilot design and historical critique.
  Update the index; no empirical audit, experiment or approval is invented.
* Paper structural checks and all seven existing tooling tests pass.
  No local TeX compiler is available, so PDF/build/layout checks remain
  unperformed and generated assets unchanged. The full publication gate
  remains blocked by its az invocation under the owner's no-az instruction;
  no push or external submission is made.

## [2026-10-27] ingest | Bounded sensor validation scenarios and two-stage dictionary

* Added a separate installed synthetic scenario pack and external tests for
  #190/#192/#193/#194: seven damp/data-quality cases, four paired retrofit
  cases, evaluator-only truth, deterministic per-check reports, case-level
  confusion, explicit insufficiency and fixed-truth threshold sensitivity.
* Updated the existing IoT research synthesis, sensor data dictionary, core
  simulator guide and this index. Corrected the dictionary's stale claim that
  composed climate/dated measures were unavailable; preserved historical
  source/approval limits and the original #191 exercise bounds.
* Recorded the actual retained ERA5 provenance, CC BY attribution, historical
  terms and synthetic-only owner approval without claiming a fresh terms
  check, underlying C3S Legal approval or real measurements. New scenario
  weather is explicitly constructed, not ERA5.
* Actual #111/#133 integration and a runnable #184 publisher remain unmet.
  R2 competent review, agreed R3 error limits, real consent, operational use
  and parent closure are not inferred from standalone synthetic tests.

## 2026-10-27: Dependent-policy RAI release binding (#218)

* The [core contract](../../src/core/README.md#dependent-policy-rai-release-binding-218-219)
  documents ranking-content binding for stock/retained priority, ordered
  checklist-policy binding for quality, and explicit current-policy capture.
  Rules, permissions, workflow/check names and actual release records are unchanged.
* Five failing-first assertions exposed the dependency/default-policy gaps.
  Local synthetic lifecycle and scripted review regressions distinguish
  release denial, source staleness and retained proposal-only decisions.
* The automation-bias negative control demonstrates the limit of citation
  syntax and false attestation, not effective human oversight. Actual paired
  human preparation/review effort is unmeasured.
* #222's corrected manifest in open PR #421 remains unapproved; no evaluator
  or participant study is implemented. OQ-017 holders, actual restart/drill
  acceptance, wider assistant/form challenge coverage, #224 legal screening
  and #440 stabilization remain open. No acceptance criterion is ticked and
  no operational, fairness, Azure or whole-epic approval is inferred.

## [2026-10-29] query | Presentation paper and journey evidence refresh

* Added a dated claim table to the
  [regulatory review update](./regulatory/reviewed-updates/2026-10-29-presentation-paper-claim-review.md)
  and linked it from the regulatory register, deck index and knowledge-base
  index. Official-page retrieval failed; currentness is `unknown` except for
  discrepancies established by retained source records.
* Updated the paper only to date its sixteen-snapshot regulatory corpus
  (downloaded 2026-09-19) and note the failed 2026-10-29 retrievals; it makes
  no EPC policy change. The review and Cowork v2 handoff record the later
  two-metric EPC policy, the 15,600/15,900 band-count discrepancy and the
  38%/39% survey-vintage mismatch; presentation binaries remain unchanged.
* No snapshot was rewritten. No legal duty is declared satisfied or approved.
  @jmservera is asked to appoint a qualified Legal/Compliance reviewer;
  Finance/funder confirmation remains necessary for grant terms.
## [2026-10-27] engineering | Bounded IoT streaming (Refs #110, #184)

* Extended the [existing IoT synthesis](./research/iot-sensor-analytics-research-plan.md#bounded-streaming-engineering-2026-10-27-refs-110-184)
  with SDK origin/identity, SQL retained-history replay, seeded seasonal
  continuity, finite-run and B1 cost/quota boundaries.
* Added API/core component usage and explicit #185-#189 criterion dispositions;
  #186 remains previously delivered. No issue status or criterion was ticked.
* Recorded the inherited individual-identity/credential owner and selected
  allowed X.509 path without credential issuance, access, rotation or teardown.
  No Azure deployment, real device discovery, private data, inference or
  operational OD-43/Legal/DPO approval was performed or inferred.
* Updated the knowledge-base index. Local constructed engineering evidence is
  separate from actual Hub/Azure SQL, hosted checks, publication and owner merge.

## [2026-10-27] query | IoT correction cycle 1 (Refs #110, #184)

* Updated the [bounded IoT synthesis](./research/iot-sensor-analytics-research-plan.md#bounded-streaming-engineering-2026-10-27-refs-110-184)
  and index with actual global send-attempt admission after setup/truth,
  receiver partial-construction cleanup and selected-input descriptor/frame
  provenance. Component guides explain the split pacing/admission contract
  and `synthetic-stream-v2` evidence format; observation bytes/IDs are unchanged.
* Focused synthetic regressions use fake SDK calls and constructed temporary
  SQLite, not actual Hub or Azure SQL. No deployment, private dataset, device
  credential, real resident consent or owner/Legal/DPO approval is inferred.
* Original adverse Review is retained. The owner-selected correction has its
  own critique and Review addendum; issue criteria and existing live/deferred
  gates remain unchanged, with Refs rather than Closes.

## [2026-10-29] engineering | Current-main IoT integration (Refs #110, #184)

* Preserved the scenario-pack and IoT engineering entries and index links
  when integrating current main into the existing IoT branch.
* Reconciled the [scenario-pack status](./research/iot-sensor-analytics-research-plan.md#bounded-r3-exercise-scenario-pack-2026-10-27-refs-190)
  and [two-stage guide](../../src/core/README.md#two-stage-simulator-operation-and-limits-194):
  the separate opt-in SDK publisher and pacing library exist, while verified
  live operation, credential lifecycle and actual scenario consumer use
  remain unproven. No historical log entry or live approval was changed.
## [2026-10-27] implement | Synthetic regulatory conflict routing and consumption (Refs #208, #214, #216, #215, #217)

* Extended existing cited-home chat with automatic supported-conflict referrals
  to the named exercise owner's isolated inbox and a durable sender receipt.
  SQL turn/referral/audit is transactional; JSON's post-save audit limitation
  is explicit. No legal interpretation or activation authority is added.
* Added closed zero-model usage metadata and bounded own-role/day audit-only
  summaries. Cost remains Unknown and paid authority absent; deterministic
  alerts, safety intake and cards-only shipment boundaries are unchanged.
* Updated the existing regulatory-literacy synthesis and draft DPIA data map,
  project guides and this index. DPO necessity/notice/recipient/rights/periods
  review must include automatic referrals and metadata; no human checkbox,
  legal snapshot, owner memory or original case-study text was changed.
* Local synthetic unit/evaluation/browser evidence and original failures are
  retained in the dated RPI artifacts. Staff comprehension, owner-agreed
  thresholds, continuing-stock validation, actual identity/deployed SQL and
  #440 remain unmet. Publication is separately blocked by the mandatory
  full-gate requirement versus the caller's explicit no-full-gate limit.
  No cloud deployment, model call, private dataset access or approval occurred.
## [2026-10-27] query | Bounded staff chat and draft privacy evidence

* Updated [DPIA draft](./research/chat-memory-dpia.md) and its index entry:
  general staff warning is now server-sourced and described at the question,
  both HTTP turn routes share cited/refusal/admission handling, and neither
  prompts retained memory before its human decision.
* Added bounded context and content-free per-turn usage evidence to the
  [API contract](../../src/api/README.md#staff-chat-hardening-2026-10-27-157)
  and [shared evaluator](../../src/agents/README.md#chat-consumption-evidence-2026-10-27-164).
  Reconciled ADR 0004's stale no-implementation statement without changing its
  accepted direction or granting activation.
* Local scripted poisoning/injection coverage and Chromium DOM/keyboard checks
  are engineering evidence, not independent human, serving-model or legal
  acceptance. The known unsupported-claim/valid-citation failure stays visible.
* No retention number, lawful basis, staff-notice/DPIA approval, provider
  transfer position, break-glass policy, threshold or role budget is invented.
  #157/#162/#159/#164/#163 remain Refs; #440 stabilization and human decisions
  prevent whole-parent acceptance.

## [2026-10-27] query | Resident content audit and assisted task designs (#153/#154)

* Extended [content standard](./research/ux/content-standard.md) with a dated
  core/supporting-surface inventory, dynamic-message and visible stored-value
  residuals, accountable follow-up roles and an honest acceptance matrix.
* Corrected stale reviewer-appointment wording using the #153 owner comment:
  Juan Manuel Servera is appointed; actual exact-text review is not evidenced.
* Extended [resident journeys](./research/ux/customer-journeys/residents.md)
  with six task flows/text wireframes, individual non-digital alternatives,
  language/literacy/adjustment and safe-contact rules, scoped representative
  briefing/actions, expiry/revocation exceptions and Not run #155 scripts.
* Indexed the evidence and made bounded existing-web draft/proposal,
  representative-date and time-capture copy clarifications with regressions.
  Fluent 2, native semantics, non-colour signals and reduced motion remain.
  No live contact, portal implementation, operational Legal/DPO decision,
  human usability/AT acceptance or whole-issue closure is claimed.
## [2026-10-27] ingest | Source-only monitoring candidates (Refs #146)

* Added [operator runbooks and the complete issue evidence/gap matrix](../../infra/monitoring-runbooks.md),
  source-only job/IoT metric alert candidates and an aggregate operations
  workbook; updated infra navigation and this knowledge-base index.
* Corrected the ledger missing-success rule's outer query range to 26 hours.
  Existing alert names, thresholds and budget notification conditions are
  preserved; budget notification is not a hard cap.
* New candidates default disabled; proposed roles are not named appointments.
  Actual owners/live thresholds, privacy exclusion, poison-queue and AI/harm
  signal integration, same-period billing/price reconciliation and accepted
  notification/suspension drills remain unresolved.
* Workbook missing data is Insufficient/Blocked and actual cost/AI metering
  remains Unknown/unreconciled. Source definitions and local checks are not a
  deployment, live approval, SLO claim or issue acceptance.

## [2026-10-29] query | Bounded existing IoT hub exercise and live blockers

* Updated infrastructure cost/environment evidence, ADR0003 dated authorization,
  API activation guide, streaming synthesis and index for Refs #140 #184 #137.
* Reused existing UK South B1/one-unit hub. Owner approved USD10/month after
  cost check, within USD5 additional through October31. Child-only deployment
  disables all device-bearing resource logs and retains metrics, private
  attachment, service auth, four app min0 and eight Manual jobs.
* No new paid hub, Event Hub, endpoint, role, device, key or public SQL change.
  Existing operator lacks registry data permission; keyless custom adapter/
  cloud revision and resident projection acceptance remain separately gated.
* Constructed actual local SQL Server passed45 sensor ingestion tests; do not
  describe this as live Hub-to-SQL or resident-gauge acceptance. Original
  source-only history, critique and open credential/OD43 criteria remain.

## [2026-10-27] query | Working Finance reviews and held human decisions

* Indexed the [core working-review boundary](../../src/core/README.md#unapproved-working-field-review-96-98-99)
  and [authenticated form-review endpoint](../../src/api/README.md#working-form-review-and-held-finance-decisions-96-98-99)
  for #96, #98 and #99.
* Isolated accept/correct/reject notes, retained source/reviewer history,
  field-specific draft diagnostics and linked diagnostic manifests do not
  approve a template, source policy, eligibility rule or application/claim.
  Draft-only read/action-time freshness is not full downstream invalidation.
* Missing template/rule authority and Finance/Board OD-12/15 are durably Held
  with null approved inputs. Diagnostic pause is not a programme-wide release
  gate or containment of live activity. Actual approved envelope, liquidity,
  covenant, downside thresholds and restart authority remain human decisions.
* No company figures, financial approvals, Azure changes, private datasets or
  new AI authority are introduced. All three issues remain Refs; engineering
  evidence is not whole-issue or operational acceptance.

## [2026-10-27] query | Rubric src counting and migration score reconciliation

* Refs #198. Added the
  [dated rubric reconciliation](../architecture/cutover-evidence-pack.md#rubric-src-counting-reconciliation-2026-10-27)
  and updated the index and rubric guide. Preserved original sign-off outcomes
  and every earlier log entry.
* Verified src package/tests/manifest/Dockerfile coverage and excluded
  vendor/private/build paths. #295/#300/#302 already removed legacy includes;
  no production registry, rubric_version, score or workflow/check name changed.
* Recorded 47/100 original baseline and carried migration snapshots separately
  from #499's actual 77/100 vs 77/100 retirement comparison. No attributable
  migration gain, fresh per-migration assessment or retroactive ordering is
  claimed. Re-evidence routes identify seven criteria and their source PRs.
* Re-assessed historical 19 failures: current baseline 18 failed/355 passed/
  seven skipped; after migration-related test repairs, one unrelated
  deck-selection failure/374 passed/seven missing-runtime skips remain.
  Thirty-one migration-targeted checks pass. No full gate, cloud, private data
  or scorer dispatch. Missing historic comparisons and prescribed sequence
  remain explicit acceptance gaps; this delivery references rather than closes.

## [2026-10-29] update | PR #507 main integration, Refs #198

* Rebased onto main `5653547507f3056f09a726a18516237728da5e5b`,
  retaining both sides of the cut-over evidence pack, KB index and this
  append-only log. Earlier entries and original RPI outcomes remain unchanged.
* Kept main's complete rubric tree and scenario manifest at the owner's
  direction. Qualified the reconciliation and index so original rubric
  repairs and test counts are not presented as the rebased candidate's delta.
* Corrected the index's duplicate date metadata while retaining its current
  date. No application source, workflow, score, Azure resource or private
  dataset changed; no push, issue acceptance or hosted-CI result is claimed.

## [2026-10-29] update | PR #507 conflict rebase, Refs #198

* Rebased onto main `356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7`.
  Preserved main's entire log prefix, both original #198 append entries,
  independent index updates and all fourteen prior RPI artifacts unchanged.
* Updated the existing
  [integration qualification](../architecture/cutover-evidence-pack.md#main-integration-qualification-2026-10-29)
  with the later base and fresh local outcomes. Main's entire rubric tree and
  scenario manifest are retained byte-for-byte; no application, workflow,
  Azure resource or private-data change was made.
* Core/API lint, format, typing and twelve focused tests passed, including
  scenario source-pin validation. The inherited rubric suite still has
  18 failures and seven missing-runtime skips; this is not CI-green evidence.
  No full API suite, full publication gate, push or hosted run was performed.

## [2026-10-30] update | PR #507 current-main synchronization, Refs #198

* Rebased onto main `91e890e07af036263316c153cbc7ceff780cdaa2`, then onto
  concurrently updated `ffd8f35e63b24905b9aeb937dbf2a7fe9968747f`, retaining
  main's complete log prefix, every original topic entry and independent index
  additions, including monitoring, finance and existing-hub reconciliation.
* Added the [current synchronization qualification](../architecture/cutover-evidence-pack.md#current-main-synchronization-2026-10-30)
  and indexed it without rewriting earlier dated results or acceptance gaps.
  Main's rubric and scenario manifest remain authoritative and unchanged.
* No application, workflow, infrastructure or legacy code changed. No Azure
  resource operation, push, fresh hosted result or issue acceptance is claimed.
  Dated RPI artifacts retain the local commands, results and independent Review;
  publication and hosted checks remain coordinator-owned.
* Fresh core/API lint, format, typing and twelve focused tests pass, as do
  twenty-five migration tests. Unchanged main rubric inputs still yield
  18 failures, 355 passes and seven runtime skips. Prepare reports no scored
  artifact change; no full API suite or publication gate was run.

## [2026-10-30] update | PR #507 review evidence correction, Refs #198

* Corrected the existing
  [rubric reconciliation](../architecture/cutover-evidence-pack.md#pr-507-review-correction-2026-10-30)
  and indexed the distinction between the original candidate and integrated
  documentation-only delta, including their different historical frozen diffs.
* Qualified discarded fixture/guide claims and acceptance rows in place.
  Original 374/1/7 and 31 fixture passes remain historical; integrated results
  are 355 passed, 18 failed and seven runtime skips, not a green suite.
* Replaced the unregistered rubric-guide B6 route with scored `src/README.md`
  in proposed later PR `docs(src): strengthen B6 navigation and evidence`,
  only when that PR actually changes the artifact. No score gain, new scored
  evidence, historical acceptance or remote metadata update is claimed.
* Prepared the replacement PR description separately for owner application.
  No rubric, test, source, workflow or score edits; local-only commit, no push.

## [2026-10-30] query | Sensor validation and current two-stage dictionary, Refs #190

* Filed current child dispositions and annual offline legacy-backfill/replay
  validation boundaries in the existing IoT research synthesis and KB index.
  Existing eleven-case scenario results remain separate from general history.
* Corrected stale sensor snapshot versions and unavailable-runner wording in
  the data dictionary; distinguished finite replay/SDK adapters, evaluator
  metadata, shared wire rows and SQL storage. Linked the existing core/API
  run guides and the credential-free per-check validation recipe.
* Retained dated climate attribution/terms, exercise-only thresholds and all
  original RPI evidence. Open children, downstream #111/#133 test use, live
  #184 execution and owner acceptance remain explicit; no remote mutation,
  live operation, new legal currentness check or whole-parent acceptance.
## [2026-10-28] implementation | January resident demo authority source renewal (#521)

* Updated the [knowledge index](./README.md) and
  [resident operations guide](../../infra/README.md#january-authority-source-renewal-2026-10-28-refs-521):
  shared source cap 2027-02-01T00:00:00Z, exclusive serving end after
  January 31 UTC; SQL rendering/migration keeps row approvals and rights.
* Documented proposed credential/version and SQL access renewal, the
  new-secret helper's unchanged Modify refusal, conditional USD15.50 January
  estimate plus USD10 reserve and unchanged USD700 all-in ceiling.
  Actual headroom and January funding are Unknown.
* No Azure, secrets or .env access. Live apply remains Pending separate
  exact owner confirmation and verification. No inference tariff extension,
  new resource, role, network path or replica minimum change is authorized.

## [2026-10-30] validation | January resident authority local evidence (Refs #521)

* Updated the [knowledge index](./README.md) and
  [resident operations guide](../../infra/README.md#january-authority-source-renewal-2026-10-28-refs-521)
  with fresh domain/HTTP/helper and disposable local SQL results. The 27
  real-SQL tests passed without skips, including legacy constraint migration,
  trusted reapply, rollback and narrow-rights preservation.
* API discovery passed 1380 tests with 320 opt-in integration skips; API/core
  Ruff, formatting and mypy passed. Targeted infra static findings reproduce
  on the reviewed main baseline and remain separate residual work.
* No Azure resource operation, deployment, actual credential access, paid
  action, inference extension or live verification occurred. Owner operational
  approval, January funding/headroom and exact-head publication gates remain
  separate; the USD700 cap and source guards are unchanged.

## [2026-10-29] query | Project-wide Microsoft Fabric fit assessment

* Added the [component review and Fabric assessment](./research/microsoft-fabric-fit-assessment.md)
  and its knowledge-base index entries. Source baseline is
  `9b74ac8daaec2a880172e43161b37ac7f2c3f801`; current official product/pricing
  sources were retrieved on 2026-10-29, with three independent component
  investigations and a separate contrarian challenge.
* Proposed retaining API/core/Azure SQL operational authority and deferring
  mandatory dedicated Fabric, while preserving a selective read-only analytics
  option for explicit portfolio/history requirements. Compared SQL/read models
  and Power BI; recorded decision-changing capacity, workload, governance and
  comparative-measurement evidence rather than asserting no analytics need.
* Distinguished ledger history from current tables, JSON text and BIGINT from
  native SQL type exclusions, private/keyless options, data-agent feature status,
  OneLake/SQL security, route-specific gateway consumption, F2/F64 licensing,
  illustrative non-regional pricing and expired earlier spending authority.
  Preserved later canonical sensor-key integration and distinct synthetic
  43.8M-row history versus declared three/day scale arithmetic.
* Research/documents only: no application/infrastructure change, private data,
  tenant/cloud operation, deployment, paid inference, benchmark, approval,
  commit, push or PR. Existing adverse reviews and operational/human gates
  remain unchanged; artifact/arithmetic/diff checks are not a complete local
  publication gate or product acceptance.

## [2026-10-30] query | Fabric assessment branch reconciliation (Refs #558)

* Reconciled the [Fabric assessment](./research/microsoft-fabric-fit-assessment.md)
  branch with main, preserving both sets of knowledge-base navigation and all
  append-only log entries. Retained the original dated assessment and research
  unchanged; this is not a new product or regulatory-currentness assessment.
* Retained main's rubric records and scenario manifest. No application,
  infrastructure, Azure resource, operational approval or issue closure is
  introduced. Local reconciliation does not establish hosted CI or authorize
  publication; the coordinator owns the subsequent push and checks.

## [2026-10-30] query | Fabric review evidence corrections (Refs #558)

* Corrected the maintained [Fabric assessment](./research/microsoft-fabric-fit-assessment.md)
  and index to distinguish the 27 October renewed overall USD700 funding through
  2026-12-31 from unknown remaining headroom, resident/inference sublimits and
  unestablished Fabric-specific purchase permission. The earlier October25
  exercise expiry is not the latest overall funding authority.
* Added the configured serverless SQL 60-minute auto-pause/0.5-vCore baseline,
  potential loss of idle compute savings, conservative no-auto-pause comparison
  and post-trial cleanup/settings/actual-pause verification. Current W2/W8 do
  not establish an automatic setting change; fresh SQL serverless sources
  support the billing/idle conditions without conflating geo-replication.
* Original research receives dated qualifications rather than rewritten
  findings, including the 480-minute, three/day 131.025M dropout estimate,
  not hourly sizing. The retained recommendation is conditional advice,
  not a renewed purchase, deployment, benchmark or operational approval.

## [2026-10-29] restructure | Capstone working set and technology rationale

* Replaced the long capstone entry point with the
  [current working set](../capstone/README.md): one 54-slide PPTX/native PDF,
  [native/JSON authoring source](../capstone/source/README.md), 36 retained
  media inputs with usage/hashes, synchronized pitch notes/Q&A and a separate
  demo runbook. The older 18-slide brief, editable diagrams, icon/evidence
  sources and dated reviews remain under history, not current scoring inputs.
* The owner selected the existing Fabric research branch and approved exactly
  15 obsolete generated exports for archive-backed removal. Full readback of
  4,411 capstone/tracking entries and selected-file restore/hash checks preceded
  removal; protected bytes were checked after the initial moves. The
  [restore map and finite receipt](../capstone/history/README.md) record local
  custody and portability limits. No original RPI evidence or thought-leadership
  file was pruned; no broader cleanup authority is inferred.
* Five existing technology pages explain rules/Decision 1/generation, shared
  API/Entra/SQL/Blob, deferred workers and the private Event Hub route. Fabric
  is a conditional read-only history/reporting option compared with SQL/read
  models plus Power BI, not a mandatory dependency, purchase or SQL-ledger
  replacement. Existing dated research, unknown benefits/current cost headroom
  and expired authority remain explicit; no fresh provider/legal check occurred.
* Independent image review raised seven original issues; corrections and
  rerenders are retained in the [dated review](../capstone/source/review-2026-10-29.md).
  Reader review exposed inherited legal/forecast claims, obsolete dynamic-return
  instructions and a recording/fallback contradiction. Legal-status page 3 and
  opening/scenario/demo notes were reconciled; current notes describe actual
  fixed jumps. All six protected cost-slide bytes and calculations remain;
  cost-note exceptions 32/36/52 change navigation sentences only.
* Actual native rendering covers all 54 slides with zero revised-text overflow;
  264 inherited bound warnings are not accessibility acceptance. The actual
  scorer's isolated indexed fixture extracts 54 slides/54 notes, finds the
  current deck and pitch/demo, and excludes source/history. Registry now pins
  the exact deck and includes the demo folder; trusted-base integration remains
  necessary for hosted scope. No score file was changed.
* Existing rubric/authoring suites report 149 passed, 23 failed and one skip.
  Seven score-fixture failures reproduce on unchanged HEAD; sixteen need
  missing `jq`. Native/source/link/editor checks do not replace rehearsal,
  fresh legal review, direct accessibility/human acceptance, current live-demo
  authority, the complete RPI publication gate, hosted scoring or owner merge.
  No commit, push, deployment, paid inference or new operational approval.

## [2026-10-30] refine | Promote roadmap recommendations into the main story

* Reviewed the retained proposals and added the
  [roadmap register and explicit crosswalk](../capstone/source/roadmap-recommendations.md):
  25 families through 22 grouped dispositions, with value hypotheses, reasons
  to wait, simpler comparators and evidence-led adoption conditions. Existing
  source work and required readiness are not presented as optional new features.
* Promoted selective Fabric/Power BI into main page 14, source connectors,
  Document Intelligence and M365 into page 15, and four improvement lanes into
  page 23. Page 24 now asks for bounded scope/owners and a costed plan before
  separately authorized execution, with results reviewed before expansion.
  Opening, demo, close and appendix labels follow the same bounded argument.
* Retrieved official Fabric and Power BI icons from the Microsoft Learn-linked
  archive. Retained unchanged SVGs, native PNG derivatives, hashes, member/URL
  provenance and permitted-use guidance. Two declared PNG package members
  augment the 293-member captured baseline; all original media remain intact.
  The rebuild verifies source/derived hashes, exact usage, aspect and native
  action preservation. No dependency or paid platform was introduced.
* Independent visual/story reviews and corrections are preserved in the
  [dated review](../capstone/source/review-2026-10-30.md). Fixed wrapping,
  presumed-benefit wording, mismatched visible calls to action, approval-order
  ambiguity and an overlong paper detour. The architecture/IoT notes now
  distinguish historical/source work, the actual bounded 29 October hub
  reconciliation, and unmet live-to-SQL/full-route acceptance. The paper
  remains unchanged and is not new causal or product evidence.
* Native render preserves 54 slides/notes, all 108 existing navigation actions,
  original timing and cost graphics/calculations. Final revised overflow is
  zero; 234 inherited bound warnings are not accessibility acceptance.
  Focused existing scorer regressions pass 22 tests. Actual isolated-index
  extraction discovers the exact current deck/pitch/demo, excludes history/
  baselines, reads all 54 note blocks and verifies main-route roadmap content
  and both embedded official PNGs. Three negative preservation checks pass.
* Updated the current deck/PDF, generated notes/Q&A, working guides and index;
  previous delivery and heavy outputs remain in external working evidence.
  The 29 October broad-suite failures retain their original scope; no new
  full-suite pass, rehearsal, current legal/provider-cost review, live-service,
  resident, human/accessibility or production acceptance is inferred. No score
  file, application, infrastructure or original RPI evidence was changed.
  No hosted score, complete publication gate, commit, push, cloud/tenant action,
  paid inference or spending approval was performed by this task.

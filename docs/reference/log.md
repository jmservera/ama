---
title: Knowledge Base Log
description: Append-only record of ingests, restructures, filed answers and lint passes for the project knowledge base
ms.date: 2026-10-07
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
* The Presentation Communications Strategist reviewed the changes. It found
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
* Review: the Presentation Communications Strategist made eleven findings,
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
* Review: the Presentation Communications Strategist made five findings.
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

## [2026-10-07] query | Build Proper Warm architecture and transactional PoC

* Added a runnable local synthetic application, architecture, runbook and
  resource ledger under `../../apps/proper-warm/` and `../architecture/`.
  Nine represented workflows share a versioned case, API-enforced gates,
  persistent history, owned exceptions and safe retry boundaries.
* The architecture distinguishes the implemented single-instance local
  container from the provisional undeployed Azure-led hybrid target.
  Demo role selection is not authentication; the evidence assistant is an
  offline simulator, not a selected model or demonstrated agentic autonomy.
* Added the PoC to this index and the root README. Preserved the original,
  addendum, owner memory, regulatory snapshots and prior read-only prototype.
* Resource creation and measured validation are recorded in
  [Proper Warm Resource and Validation Ledger](../architecture/proper-warm-resources.md).
  Azure/M365 resources are not needed and none is created.
* Full PRD MVP coverage, company benefits and capstone floor readiness are
  not claimed. The complete-rubric challenge records unknown live/stakeholder
  criteria and open human release gates.

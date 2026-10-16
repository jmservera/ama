---
title: Knowledge Base Log
description: Append-only record of ingests, restructures, filed answers and lint passes for the project knowledge base
ms.date: 2026-10-11
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

  * Owner requested the Presentation Communications Strategist and PowerPoint
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

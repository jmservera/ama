---
title: Knowledge Base Log
description: Append-only record of ingests, restructures, filed answers and lint passes for the project knowledge base
ms.date: 2026-09-26
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
  100.0%. Remaining risks are seven business goals without numeric targets
  and NFR-009 thresholds, which need company data or board decisions (OD-01,
  OD-08, OD-09, OD-11, OD-12, OD-13, OD-15, OD-18, OD-25). Targets were not
  invented.

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

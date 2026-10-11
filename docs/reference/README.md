---
title: Project Knowledge Base
description: Entry point and index for the AMA Case Study 48 second brain, routing agents and people to the right evidence for each task
ms.date: 2026-10-11
ms.topic: overview
---

## Purpose

This folder is the project's knowledge base, a persistent second brain for the
Proper Warm research. It gathers the evidence, syntheses, working method and
project memory that agents and people need, and this index tells them where to
look first.

The design follows the LLM Wiki pattern described by Andrej Karpathy: keep
immutable sources separate from maintained syntheses, read a content index
before searching, record changes in an append-only log, and file useful
answers back into the knowledge base so they are not lost in chat history.
Topic hubs work like the Maps of Content used in personal knowledge
management: short pages that point to clusters of related material.

## How to Use This Knowledge Base

1. Read this index first and pick the rows in
   [Task Routing](#task-routing) that match the task.
2. Read the [Project Memory](./memory.md) for owner context and preferences.
3. Open only the files the task needs. Large regulatory snapshots should be
   searched for the relevant provision, not read end to end.
4. Cite the file, section and date for every material claim, and follow the
   evidence rules in the [Regulatory Source Register](./regulatory/README.md).
5. When the work produces a durable finding, integrate it into the right
   document, update this index and add an entry to the
   [Knowledge Base Log](./log.md).

## Layers

| Layer | Location | Owner and change rule |
| --- | --- | --- |
| Schema | [copilot-instructions.md](../../.github/copilot-instructions.md) | Repository conventions for agents. Change only when the working method changes |
| Index | This file | Updated whenever a knowledge base file is added, moved, retired or materially changed |
| Sources | [regulatory/](./regulatory/) | Dated official snapshots. Immutable; a newer retrieval is recorded as a reviewed update |
| Syntheses | [research/](./research/) | Agent-maintained research with citations. Integrate new findings in place |
| Method | [method/](./method/) | AMA training material and reusable working prompts |
| Resources | [resources/](./resources/) | Curated pointers to internal and external resources, with retrieved findings and access notes |
| Memory | [memory.md](./memory.md) | Owner-curated notes. Agents update it only when the owner asks |
| Log | [log.md](./log.md) | Append-only record of ingests, restructures and lint passes |
| Project documents | [docs/](../) outside this folder | Problem specification and deliverables, governed by the repository instructions |

## Task Routing

| Task | Start with | Then consult |
| --- | --- | --- |
| Understand the customer and the sector | [Housing Association Primer](./research/sector/housing-association-primer.md) | [Company Profile Research](./research/company/company-profile-research.md) |
| Start or resume any project work | [Original Case Study 48](../case_study_48_original.md) and [Case Study 48 Addendum](../case_study_48_addendum.md) | [Project Memory](./memory.md) |
| Answer as a Proper North Homes role | [Company Profile Research](./research/company/company-profile-research.md) | The matching `company-*` agent in [.github/agents/](../../.github/agents/) |
| Estimate Proper North Homes' tenure, leasehold, resident or financial scale | [Modelled Customer Profile](./research/company/company-profile-research.md#modelled-customer-profile) in Company Profile Research | [Housing Association Primer](./research/sector/housing-association-primer.md) |
| Quote a benchmark, cost or sector statistic | [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) | [UK Social Housing Baseline Source Register](./research/sector/uk-social-housing-baseline-source-register.md) |
| Make a regulatory, legal or funding claim | [Regulatory Source Register](./regulatory/README.md) | The snapshot for the topic under [regulatory/](./regulatory/) |
| Design Awaab's Law, damp and mould or safety controls | [social-housing-regulation/](./regulatory/social-housing-regulation/) | [Company Profile Research](./research/company/company-profile-research.md) |
| Design EPC C, energy standard or grant logic | [energy-efficiency/](./regulatory/energy-efficiency/) and [retrofit-standards-and-funding/](./regulatory/retrofit-standards-and-funding/) | [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) |
| Handle resident data, consent or automated decisions | [data-protection/](./regulatory/data-protection/) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Write or review requirements | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Build or review a subsequent AMA prototype/PoC/MVP | [Subsequent Application Exercise Builds](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11) | BRD CON-007/AC-086 and PRD CON-009/AC-057 require actual AI/SQL/Azure on continuing generated data; [current model learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11) separates feasibility from parallel-experiment benefit |
| Refine prototype usability from owner feedback | [Owner Usability Feedback (2026-10-07)](./research/ux/proper-warm-prototype-profile-review.md#owner-usability-feedback-2026-10-07) | [Proper Warm Workbench PRD](../prds/proper-warm-retrofit-programme-demonstrator.md); reported impressions and proposed checks are not verified implementation or acceptance |
| Compare Azure development with M365 and business-platform implementation | [Implementation Options and Provisional Platform Recommendation](../case_study_48_addendum.md#implementation-options-and-provisional-platform-recommendation) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) and [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) |
| Evaluate a new idea | [Idea Register](../ideas/idea-register.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Design System One scoring or assisted funding forms | [Decision 1 reassessment](../ideas/typesafe-system-one-agent-fit.md#microsoft-decision-1-reassessment-2026-10-10) | [PRD AI/form contract](../prds/proper-warm-retrofit-programme-demonstrator.md#ai-assisted-decision-coverage); evidenced scheme route, deterministic rules and Finance/human approval remain mandatory |
| Challenge whether a requested agent is needed, or decide what to build instead | [Agent Request Challenge](./research/company/agent-request-challenge.md) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Test whether richer inputs (phone photos, geotagging, structured invoices) change any agent verdict | [Agent What-If Study](./research/company/agent-what-if-study.md) | [Agent Request Challenge](./research/company/agent-request-challenge.md) |
| Design pilot measurement, baselines, comparison cohorts or a benefits dashboard | [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Practise constraint discovery, or test workflow and agent concepts on realistic records | [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) and its [data dictionary](./research/retrofit-synthetic-data/data-dictionary.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md); do not open the owner's answer key until blind findings are recorded |
| Prepare or challenge the final presentation, architecture or pitch | [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) | [Project Memory](./memory.md), [Case Study 48 Addendum](../case_study_48_addendum.md), [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) and [85-day roadmap](../case-study-85-day-roadmap.svg) |
| Design a looped agent goal | [Capstone Deliverables and Storage Map](../capstone/README.md) | Where each capstone asset (deck, pitch transcripts, thought leadership artifact, code) must be stored for the rubric gate, and which criteria score 0 until it exists |
| [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | [Project Memory](./memory.md) |
| Find proven use cases, customer evidence or reusable solutions | [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |

## Catalog

### Project Documents

| Document | Summary | Updated |
| --- | --- | --- |
| [Original Case Study 48](../case_study_48_original.md) | Initial problem specification. Preserved unchanged | 2026-09-10 |
| [Case Study 48 Addendum](../case_study_48_addendum.md) | Dated v0.12.0 assumption/acceptance history plus 2026-10-11 mandatory real AI/SQL/Azure for subsequent delivered prototypes/PoCs/MVPs. Retained generated data, #58 feasibility, scoped budget override and independent parallel experiment distinguished from production approval/benefit | 2026-10-11 |
| [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | v0.16.0 draft candidate: nine controlled workflows, human/resident authority and separate business-value tests. CON-007/AC-086 require real-platform exercise evidence; 44 FRs, 86 ACs, 9 NFRs, 7 constraints, 24 rules. Company baselines/approvals and measured benefits remain unresolved; fresh business/quality review required | 2026-10-11 |
| [Proper Warm Retrofit Programme Workbench PRD](../prds/proper-warm-retrofit-programme-demonstrator.md) | v0.13.0 candidate awaiting fresh requirements review/owner acceptance; v0.12.0 acceptance retained as history. CON-009/AC-057 require actual Azure/SQL/AI workflow and durability evidence. 46 FRs, 57 ACs, 13 NFRs, 9 constraints; sixteen exercise dispositions and operational questions retained. #58 narrow feasibility does not establish calibration, three-class screening, benefit or full acceptance | 2026-10-11 |
| [ADR 0001 Azure Architecture](../adrs/0001-azure-architecture.md) | Historical/proposed full topology with dated 2026-10-11 applicability: mandatory actual AI/SQL/Azure does not require every premium service or approve production. Pinned #58 lean deployment and later source tests distinguished. Bicep in [infra](../../infra/README.md) | 2026-10-11 |
| [ADR 0002 Pilot-Readiness Architecture](../adrs/0002-pilot-readiness-architecture.md) | Historical/proposed pilot decisions with current exercise applicability: retain generated stock/programme and prove changed-build real services; source-tested controls not automatically deployed. Full Entra/user/permissions/performance/human gates remain distinct from #58 feasibility | 2026-10-11 |
| [Capstone Rubric Review of the Agentic Retrofit Programme BRD](./research/company/capstone-brd-rubric-review.md) | Criterion-by-criterion readiness assessment of the BRD against the FY27 AMA capstone rubric, with floor analysis and a four-gate remediation plan | 2026-09-30 |
| [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) | Evidence, team and bounded assistant requirements for finding delivery constraints | 2026-09-19 |
| [Idea Register](../ideas/idea-register.md) | Research ideas that are not yet validated requirements | 2026-09-24 |
| [System One Decision Models for Retrofit Agents](../ideas/typesafe-system-one-agent-fit.md) | Dated #58 real selection/generation feasibility, provider-host correction and binary/three-class caveat; parallel R/D/A/H experiment intake separates technical integration from calibrated quality and net benefit. Historical API/pricing/Jev/Kev evidence preserved; no production selection or blanket spending authority | 2026-10-11 |
| [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) | Deck for the first mentoring session, with 14 slides and a knowledge-organisation appendix. It covers the request and its gaps, research loops, role agents, the value challenge, agent-led modernisation, pilot measurement and transparency, the what-if stress test, BRD quality, lessons, a traceability chain and mentor questions. Iteration 6 updates the Git evidence and repairs source footers. The validated working build is ready, but the 2026-09-27 published binary remains in place because PowerPoint held it open on 2026-09-30. Maintained with the `ama-mentor-deck` skill. Working files: `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/` | Validated working build, 2026-09-30; publish blocked |
| [85-day roadmap](../case-study-85-day-roadmap.svg) | C-suite solution roadmap diagram, with its [Excalidraw source](../case-study-85-day-roadmap.excalidraw) | Binary file |

### Research Syntheses

| Document | Summary | Updated |
| --- | --- | --- |
| [Housing Association Primer](./research/sector/housing-association-primer.md) | What a UK housing association is, sector scale and archetypes, tenure types, lease responsibility rules for retrofit, resident needs, board capital patterns, funding model and implications for Proper North Homes | 2026-09-25 |
| [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) | Provisional sector benchmarks for energy, repairs, safety, grants, finance, delivery and quality | 2026-09-11 |
| [UK Social Housing Baseline Source Register](./research/sector/uk-social-housing-baseline-source-register.md) | Official publications and datasets behind each baseline benchmark | 2026-09-11 |
| [Company Profile Research](./research/company/company-profile-research.md) | Confirmed not-for-profit status, comparators, modelled customer profile (estimates, not company facts), common sector problems, role map and company gaps for the role agents | 2026-09-26 |
| [Agent Request Challenge](./research/company/agent-request-challenge.md) | Role-agent challenge of the five requested agents: real problems, non-agent alternatives, bounded AI fit, shared foundation, value tests and stop criteria | 2026-09-26 |
| [Agent What-If Study](./research/company/agent-what-if-study.md) | Follow-up thought experiment running 20 augmentation scenarios across the requested agents, from phone-captured evidence and structured invoices to funder integrations, sensors and call transcription, with role-agent clarification answers re-run against the current proposal, a value-versus-complexity grid and a reconciliation with the agent-led modernisation reframe; headline verdict unchanged after the post-merge review | 2026-09-27 |
| [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | Role-agent challenge of measuring acceleration with a dashboard, short history and non-pilot comparison, plus the owner's modernisation decision: Comparison 1 and 2, frozen protocol, benefits scorecard, guardrails, vanity metrics and history sources | 2026-09-26 |
| [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) | Version 2.0.0: fifteen months of constructed operating records for 980 candidate homes. The case presents a professional team aware of bottlenecks but not where they occur. The pack covers the tracker, stage event log, property register, CRM contacts, supplier appointments, safety holds, QA and evidence, grant and finance, capacity, board reports and issues log, with realistic record-keeping imperfections, a data dictionary and a manifest. These records are for the exercise and are not evidence of actual company performance. The answer key and generator are held outside the knowledge base so analysis can stay blind | 2026-10-06 |
| [Program Manager Document Workspace Journey](./research/ux/program-manager-document-workspace-journey.md) | Stakeholder-informed JTBD analysis, journey map, accessibility requirements and design handoff for the repository-backed Program Workbench canvas. All behavioural findings remain reported or assumed pending direct user research | 2026-10-02 |
| [Proper Warm Prototype Profile Review](./research/ux/proper-warm-prototype-profile-review.md) | Nine company-role critiques, eleven-perspective UX synthesis and four relayed discussions, plus separately dated owner feedback on a later application: preserve brand/clarity, correct reddish status meaning, contextualize role/workflow, expose readiness/ownership/agent boundaries and provide a full-screen case with minimum-necessary synthetic contact context. Eight proposed next-prototype checks; no prototype changes or passed usability claims | 2026-10-07 |
| [Prototype Learnings and Simplicity Review](./research/ux/prototype-learnings-and-simplicity-review.md) | Historical eight-angle simplicity critique plus dated #58 real-platform learning: assistance optional per record, real AI mandatory per delivered application; calibration/benefits and direct human usability unproved | 2026-10-11 |
| [Gap Analysis and Next Build](./research/gap-analysis-next-build.md) | Dated prior gaps retained; current 2026-10-11 direction reuses generated-data MVP and requires real AI/SQL/Azure, not rebuilding already delivered features. Independent platform/control work and experiment-value gates separated | 2026-10-11 |
| [Decision 1 Behaviour Specification](./research/decision-1-behaviour-specification.md) | Implementation-independent record of the PR 58 Decision 1 assist (tasks, thresholds, provider contract, guard order, spend ledger, tests, open questions) for a clean rebuild |
| [Proper Warm MVP](../../mvp/README.md) | Local case-management MVP built to SA-001 to SA-010 on realistic constructed data placed on private stock-geography addresses; run instructions, privacy limits and honest scope | 2026-10-08 |

### Regulatory Sources

The [Regulatory Source Register](./regulatory/README.md) holds the authority
hierarchy, current-use status, change likelihood, monitoring cadence and
official links for every snapshot. Check it before relying on any file below.

| Topic folder | Snapshots | Use status summary |
| --- | --- | --- |
| [energy-efficiency/](./regulatory/energy-efficiency/) | Net Zero 2050 Target Order 2019; social rented sector MEES consultation and impact assessment 2025; government response and final impact assessment 2026 | 2026 government response and final impact assessment are the final policy position, not a commenced landlord duty; 2025 material is historical |
| [social-housing-regulation/](./regulatory/social-housing-regulation/) | Social Housing (Regulation) Act 2023; Safety and Quality Standard 2024; Awaab's Law regulations 2025 and Phase 1 and Phase 2 guidance | Phase 1 in force from 27 October 2025; Phase 2 planned from 30 November 2026 |
| [data-protection/](./regulatory/data-protection/) | UK GDPR current consolidated text; UK GDPR adopted text; Data Protection Act 2018 | Use the current consolidated UK GDPR text; the adopted text is historical |
| [retrofit-standards-and-funding/](./regulatory/retrofit-standards-and-funding/) | PAS 2035:2023 BSI overview; Warm Homes: Social Housing Fund Wave 3 technical annex | Overview and allocation method only; the licensed standard and grant agreement govern |

### Resources

| Document | Summary | Updated |
| --- | --- | --- |
| [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | Internal hub entry points, nonprofit hero use cases, patterns mapped to each Proper Warm agent, customer evidence and lessons | 2026-09-25 |

### Method and Memory

| Document | Summary |
| --- | --- |
| [Project Memory](./memory.md) | AMA programme process, capstone rubric review requirement, customer-first presentation and demo guidance, and owner preferences |
| [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) | Complete FY27 participant rubric for technical excellence, communication and executive presence, consultative and stakeholder skills, and the thought leadership artifact |
| [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | Coaching prompt that turns a recurring task into a Goal Card for an agent working in an assess, act, check and adjust loop |
| [Knowledge Base Log](./log.md) | Chronological record of knowledge base changes |

### Agents

| Agents | Purpose |
| --- | --- |
| `company-*` in [.github/agents/](../../.github/agents/) | Proper North Homes role agents for interrogating the problem. Grounded in [Company Profile Research](./research/company/company-profile-research.md) |
| [company-executive-reviewer.agent.md](../../.github/agents/company-executive-reviewer.agent.md) | Owner-delegated, draft-only target ratification or changes-requested decision; not company approval or operational authority |
| `ama-*` in [.github/agents/](../../.github/agents/) | AMA helper agents for solution orchestration and presentation communications |

## Maintenance

### Ingest a New Source

1. Classify the source using the categories in the repository instructions.
2. Place an official regulatory, funding or standards snapshot in the matching
   [regulatory/](./regulatory/) topic folder and add it to the
   [Regulatory Source Register](./regulatory/README.md). Record other sources
   in the synthesis that uses them.
3. Integrate the findings into the existing synthesis or project document.
   Create a new synthesis page only when no existing page can hold the topic.
4. Flag contradictions with existing pages rather than overwriting them.
5. Update this index and append an `ingest` entry to the
   [Knowledge Base Log](./log.md).

### File Back a Durable Answer

When a question produces a comparison, analysis or finding worth keeping,
save it into the relevant synthesis or project document with its evidence,
update this index when a page is added, and log it as a `query` entry.

### Lint the Knowledge Base

Run a lint pass before a major deliverable, submission or regulatory
commencement date. Check for:

* Broken relative links and files missing from this index
* Contradictions between syntheses, project documents and sources
* Stale claims superseded by a newer source or a regulatory change
* Snapshots past their monitoring cadence in the register
* Orphan pages with no inbound link from this index or another page

Record the result as a `lint` entry in the log.

### Placement Rules

| Material | Location |
| --- | --- |
| Official legislation, standards, policy, guidance or funding material | `regulatory/{topic}/` |
| Sector research and benchmarks | `research/sector/` |
| Research about Proper North Homes and its roles | `research/company/` |
| AMA training material and reusable prompts | `method/` |
| Internal or external resource pointers and their retrieved findings | `resources/` |
| Owner notes and preferences | `memory.md`, only when the owner asks |
| Problem specification, BRDs, ideas and presentations | Existing folders under `docs/` |
| Private owner material, such as the cohort map | `support/`, outside the knowledge base |

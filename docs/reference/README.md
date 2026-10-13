---
title: Project Knowledge Base
description: Entry point and index for the AMA Case Study 48 second brain, routing agents and people to the right evidence for each task
ms.date: 2026-10-13
ms.topic: overview
---

## Purpose

This folder is the project's knowledge base, a persistent second brain for the
Zava Forward research. It gathers the evidence, syntheses, working method and
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
| Answer as a Zava North Homes role | [Company Profile Research](./research/company/company-profile-research.md) | The matching `company-*` agent in [.github/agents/](../../.github/agents/) |
| Estimate Zava North Homes' tenure, leasehold, resident or financial scale | [Modelled Customer Profile](./research/company/company-profile-research.md#modelled-customer-profile) in Company Profile Research | [Housing Association Primer](./research/sector/housing-association-primer.md) |
| Quote a benchmark, cost or sector statistic | [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) | [UK Social Housing Baseline Source Register](./research/sector/uk-social-housing-baseline-source-register.md) |
| Make a regulatory, legal or funding claim | [Regulatory Source Register](./regulatory/README.md) | The snapshot for the topic under [regulatory/](./regulatory/) |
| Design Awaab's Law, damp and mould or safety controls | [social-housing-regulation/](./regulatory/social-housing-regulation/) | [Company Profile Research](./research/company/company-profile-research.md) |
| Design EPC C, energy standard or grant logic | [energy-efficiency/](./regulatory/energy-efficiency/) and [retrofit-standards-and-funding/](./regulatory/retrofit-standards-and-funding/) | [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) |
| Handle resident data, consent or automated decisions | [data-protection/](./regulatory/data-protection/) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Write or review requirements | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Build or review a subsequent AMA prototype/PoC/MVP | [Subsequent Application Exercise Builds](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11) | BRD CON-007/AC-086 and PRD CON-009/AC-057 require actual AI/SQL/Azure on continuing generated data; [current model learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11) separates feasibility from parallel-experiment benefit |
| Refine prototype usability from owner feedback | [Owner Usability Feedback (2026-10-07)](./research/ux/zava-forward-prototype-profile-review.md#owner-usability-feedback-2026-10-07) | [Zava Forward Workbench PRD](../prds/zava-forward-retrofit-programme-demonstrator.md); reported impressions and proposed checks are not verified implementation or acceptance |
| Compare Azure development with M365 and business-platform implementation | [Implementation Options and Provisional Platform Recommendation](../case_study_48_addendum.md#implementation-options-and-provisional-platform-recommendation) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) and [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) |
| Evaluate a new idea | [Idea Register](../ideas/idea-register.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Migrate company/programme branding to Zava North Homes / Zava Forward | [One-off migration script and guide](../../tools/rename-zava.md) | Dry-run inventory, tracked text/paths, PPTX/YAML/logo handling, readable image assets and historical exceptions; [observed from-empty Azure rebuild](../../infra/README.md#from-empty-rebuild-observed-on-2026-10-12), real SQL/model checks, [callback-only initialization](../../infra/README.md#post-deployment-api-authentication-initialization) and [tenant provisioning consent boundary](../../infra/README.md#api-registration-management-with-the-existing-m365-session) |
| Configure public workbench entry and own Entra account photos | [Public welcome and Microsoft account photos](../../infra/README.md#public-welcome-and-microsoft-account-photos) | Exact public exemptions, delegated own-user User.Read, private token store/daily renewal, image-only Blob CSP and binary-render regression; real-user acceptance remains separate |
| Initialize tenant people and workbench roles | [Tenant staff and application-role initialization](../../infra/README.md#tenant-staff-and-application-role-initialization) | App-role plus SQL oid binding, private roster, preserved work codes/history, scoped Contractor and required cached-roster restart |
| Diagnose Microsoft account switching or interpret deployment learning | [Account selection and safe flow diagnostics](../../infra/README.md#account-selection-and-safe-flow-diagnostics) | [ADR identity/session mechanics](../adrs/0002-pilot-readiness-architecture.md#observed-exercise-identity-and-session-learning-2026-10-13), [PRD learning](../prds/zava-forward-retrofit-programme-demonstrator.md#review-learning-disposition) and [dated addendum observations](../case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213); chooser routes/logs are not authenticated-session acceptance |
| Hand over the current #65 deployment or assess what merging approves | [Current exercise handover](../../infra/README.md#current-exercise-handover-2026-10-13) | [ADR delivery delta](../adrs/0002-pilot-readiness-architecture.md#current-exercise-delivery-delta-2026-10-13), [MVP limits](../../mvp/README.md#honest-limits) and [migration history exceptions](../../tools/rename-zava.md#deliberate-exceptions-and-edge-cases); historical identifiers stay exact and document merge does not approve product/pilot/production gates |
| Design System One scoring or assisted funding forms | [Decision 1 reassessment](../ideas/typesafe-system-one-agent-fit.md#microsoft-decision-1-reassessment-2026-10-10) | [PRD AI/form contract](../prds/zava-forward-retrofit-programme-demonstrator.md#ai-assisted-decision-coverage); evidenced scheme route, deterministic rules and Finance/human approval remain mandatory |
| Challenge whether a requested agent is needed, or decide what to build instead | [Agent Request Challenge](./research/company/agent-request-challenge.md) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Test whether richer inputs (phone photos, geotagging, structured invoices) change any agent verdict | [Agent What-If Study](./research/company/agent-what-if-study.md) | [Agent Request Challenge](./research/company/agent-request-challenge.md) |
| Design pilot measurement, baselines, comparison cohorts or a benefits dashboard | [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Practise constraint discovery, or test workflow and agent concepts on realistic records | [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) and its [data dictionary](./research/retrofit-synthetic-data/data-dictionary.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md); do not open the owner's answer key until blind findings are recorded |
| Prepare or challenge the final presentation, architecture or pitch | [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) | [Project Memory](./memory.md), [Case Study 48 Addendum](../case_study_48_addendum.md), [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) and [85-day roadmap](../case-study-85-day-roadmap.svg) |
| Configure or troubleshoot rubric scoring authentication | [Capstone Rubric Gate](../../.github/rubric/README.md#owner-setup) | Built-in Actions token, job-scoped permissions and Copilot inference eligibility; compilation and a passing score do not establish product acceptance |
| Design a looped agent goal | [Capstone Deliverables and Storage Map](../capstone/README.md) | Where each capstone asset (deck, pitch transcripts, thought leadership artifact, code) must be stored for the rubric gate, and which criteria score 0 until it exists |
| [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | [Project Memory](./memory.md) |
| Find proven use cases, customer evidence or reusable solutions | [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |

## Catalog

### Project Documents

| Document | Summary | Updated |
| --- | --- | --- |
| [Original Case Study 48](../case_study_48_original.md) | Initial problem specification. Preserved unchanged | 2026-09-10 |
| [Case Study 48 Addendum](../case_study_48_addendum.md) | Preserved baseline and mandatory real-platform builds; dated 2026-10-12/13 rebuild, asset, identity/binding, private history-preserving initialization, account-picker and CI learning. Technical/owner-reported evidence separated from full acceptance and measured benefit | 2026-10-13 |
| [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | v0.16.0 draft candidate: nine controlled workflows, human/resident authority and separate business-value tests. CON-007/AC-086 require real-platform exercise evidence; 44 FRs, 86 ACs, 9 NFRs, 7 constraints, 24 rules. Company baselines/approvals and measured benefits remain unresolved; fresh business/quality review required | 2026-10-11 |
| [Zava Forward Retrofit Programme Workbench PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | v0.13.1 evidence-only learning update; candidate approval unchanged. CON-009/AC-057 and 46 FRs/57 ACs/13 NFRs/9 constraints unchanged. Records app-role plus oid binding, current-name/history preservation, welcome/photo/explicit account choice and safe diagnostic implications; real-session and full acceptance remain separate | 2026-10-13 |
| [ADR 0001 Azure Architecture](../adrs/0001-azure-architecture.md) | Proposed full topology with current #65 operator handover and exact historical warm-* deployment IDs; actual AI/SQL/Azure does not approve every premium service or production. Bicep in [infra](../../infra/README.md) | 2026-10-13 |
| [ADR 0002 Pilot-Readiness Architecture](../adrs/0002-pilot-readiness-architecture.md) | Proposed decisions and dated historical table retained; current delivery delta distinguishes real SQL/Blob/CI/Entra work from earlier blockers. Role plus oid, cache, private lineage preservation, own-photo CSP/token store and select_account documented; guest, full-permission, human and production gates remain open | 2026-10-13 |
| [Capstone Rubric Review of the Agentic Retrofit Programme BRD](./research/company/capstone-brd-rubric-review.md) | Criterion-by-criterion readiness assessment of the BRD against the FY27 AMA capstone rubric, with floor analysis and a four-gate remediation plan | 2026-09-30 |
| [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) | Evidence, team and bounded assistant requirements for finding delivery constraints | 2026-09-19 |
| [Idea Register](../ideas/idea-register.md) | Research ideas that are not yet validated requirements | 2026-09-24 |
| [System One Decision Models for Retrofit Agents](../ideas/typesafe-system-one-agent-fit.md) | Dated #58 selection/generation feasibility and parallel experiment boundaries retained; historical revision ca-properwarm-mvp--0000018 restored exactly, not renamed into a fictitious deployment. No calibrated benefit, production selection or blanket spending authority | 2026-10-13 |
| [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) | Published 15-slide deck, including the knowledge-organisation appendix, with Zava branding. Covers research, value challenge, governance, learning and mentor questions. #65 migration validation is recorded; 2026-10-13 audit confirms delivery bytes equal the working PPTX, superseding the earlier publish-blocked note. Existing narrative/layouts were not freshly redesigned. Maintained with `ama-mentor-deck`; working files remain under `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/` | Publication equality checked, 2026-10-13 |
| [Zava Forward executive capstone deck](../capstone/deck/zava-forward-executive-draft.pptx) | Council proposal connecting the five-agent request to a shared, measurable and transparent way of working: research challenge, bounded assistance, retained teams and suppliers, staged Excel adoption, resident choice and accountable decisions. Sole published executive deck; the presentations-folder duplicate is retired. Measured benefits, full security assurance, timed rehearsal and production approval remain separate gates | 2026-10-11 |
| [85-day roadmap](../case-study-85-day-roadmap.svg) | C-suite solution roadmap diagram, with its [Excalidraw source](../case-study-85-day-roadmap.excalidraw) | Binary file |

### Research Syntheses

| Document | Summary | Updated |
| --- | --- | --- |
| [Housing Association Primer](./research/sector/housing-association-primer.md) | What a UK housing association is, sector scale and archetypes, tenure types, lease responsibility rules for retrofit, resident needs, board capital patterns, funding model and implications for Zava North Homes | 2026-09-25 |
| [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) | Provisional sector benchmarks for energy, repairs, safety, grants, finance, delivery and quality | 2026-09-11 |
| [UK Social Housing Baseline Source Register](./research/sector/uk-social-housing-baseline-source-register.md) | Official publications and datasets behind each baseline benchmark | 2026-09-11 |
| [Company Profile Research](./research/company/company-profile-research.md) | Confirmed not-for-profit status, comparators, modelled customer profile (estimates, not company facts), common sector problems, role map and company gaps for the role agents | 2026-09-26 |
| [Agent Request Challenge](./research/company/agent-request-challenge.md) | Role-agent challenge of the five requested agents: real problems, non-agent alternatives, bounded AI fit, shared foundation, value tests and stop criteria | 2026-09-26 |
| [Agent What-If Study](./research/company/agent-what-if-study.md) | Follow-up thought experiment running 20 augmentation scenarios across the requested agents, from phone-captured evidence and structured invoices to funder integrations, sensors and call transcription, with role-agent clarification answers re-run against the current proposal, a value-versus-complexity grid and a reconciliation with the agent-led modernisation reframe; headline verdict unchanged after the post-merge review | 2026-09-27 |
| [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | Role-agent challenge of measuring acceleration with a dashboard, short history and non-pilot comparison, plus the owner's modernisation decision: Comparison 1 and 2, frozen protocol, benefits scorecard, guardrails, vanity metrics and history sources | 2026-09-26 |
| [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) | Version 2.0.0: fifteen months of constructed operating records for 980 candidate homes. The case presents a professional team aware of bottlenecks but not where they occur. The pack covers the tracker, stage event log, property register, CRM contacts, supplier appointments, safety holds, QA and evidence, grant and finance, capacity, board reports and issues log, with realistic record-keeping imperfections, a data dictionary and a manifest. These records are for the exercise and are not evidence of actual company performance. The answer key and generator are held outside the knowledge base so analysis can stay blind | 2026-10-06 |
| [Program Manager Document Workspace Journey](./research/ux/program-manager-document-workspace-journey.md) | Stakeholder-informed JTBD analysis, journey map, accessibility requirements and design handoff for the repository-backed Program Workbench canvas. All behavioural findings remain reported or assumed pending direct user research | 2026-10-02 |
| [Zava Forward Prototype Profile Review](./research/ux/zava-forward-prototype-profile-review.md) | Nine company-role critiques, eleven-perspective UX synthesis and four relayed discussions, plus separately dated owner feedback on a later application: preserve brand/clarity, correct reddish status meaning, contextualize role/workflow, expose readiness/ownership/agent boundaries and provide a full-screen case with minimum-necessary synthetic contact context. Eight proposed next-prototype checks; no prototype changes or passed usability claims | 2026-10-07 |
| [Prototype Learnings and Simplicity Review](./research/ux/prototype-learnings-and-simplicity-review.md) | Historical eight-angle simplicity critique plus dated #58 real-platform learning: assistance optional per record, real AI mandatory per delivered application; calibration/benefits and direct human usability unproved | 2026-10-11 |
| [Gap Analysis and Next Build](./research/gap-analysis-next-build.md) | Dated prior gaps and 2026-10-11 build direction retained; later #65 handover prevents repeating recovered deployment/identity blockers. Reuse generated-data MVP; platform/control work and experiment-value gates remain separate | 2026-10-13 |
| [Decision 1 Behaviour Specification](./research/decision-1-behaviour-specification.md) | Clean-rebuild contract linked to the overall application design: workbench/API integration, scoring versus generation, human review and application boundaries, tasks, thresholds, provider contract, guard, liabilities and tests | 2026-10-11 |
| [Zava Forward MVP](../../mvp/README.md) | Continuing local/Azure application on retained constructed cases and private stock geography; real SQL/model evidence, Entra initialization, welcome/photo/account choice and current tests distinguished from historical snapshots. Full workflow, human, recovery, accessibility and production acceptance remain separate | 2026-10-13 |

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
| [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | Internal hub entry points, nonprofit hero use cases, patterns mapped to each Zava Forward agent, customer evidence and lessons | 2026-09-25 |

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
| `company-*` in [.github/agents/](../../.github/agents/) | Zava North Homes role agents for interrogating the problem. Grounded in [Company Profile Research](./research/company/company-profile-research.md) |
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
| Research about Zava North Homes and its roles | `research/company/` |
| AMA training material and reusable prompts | `method/` |
| Internal or external resource pointers and their retrieved findings | `resources/` |
| Owner notes and preferences | `memory.md`, only when the owner asks |
| Problem specification, BRDs, ideas and presentations | Existing folders under `docs/` |
| Private owner material, such as the cohort map | `support/`, outside the knowledge base |

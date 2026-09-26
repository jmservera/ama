---
title: Project Knowledge Base
description: Entry point and index for the AMA Case Study 48 second brain, routing agents and people to the right evidence for each task
ms.date: 2026-09-26
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
| Evaluate a new idea | [Idea Register](../ideas/idea-register.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Challenge whether a requested agent is needed, or decide what to build instead | [Agent Request Challenge](./research/company/agent-request-challenge.md) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Design pilot measurement, baselines, comparison cohorts or a benefits dashboard | [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Prepare a presentation or pitch | [Project Memory](./memory.md) | [Proper Warm CXO initial proposal](../presentations/proper-warm-cxo-initial-proposal.pptx) and [85-day roadmap](../case-study-85-day-roadmap.svg) |
| Design a looped agent goal | [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | [Project Memory](./memory.md) |
| Find proven use cases, customer evidence or reusable solutions | [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |

## Catalog

### Project Documents

| Document | Summary | Updated |
| --- | --- | --- |
| [Original Case Study 48](../case_study_48_original.md) | Initial problem specification. Preserved unchanged | 2026-09-10 |
| [Case Study 48 Addendum](../case_study_48_addendum.md) | Evolving critical assessment, agent-led modernisation proposal with a business value measure per agent capability, trade-offs and business value | 2026-09-26 |
| [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | Business requirements for safe, resident-centred and financially controlled retrofit delivery, including tenure, eligibility, hazard-awareness and contractor-instruction controls from the agent request challenge, and the pilot measurement protocol (Comparison 1 and 2), benefits scorecard and guardrail pause from the pilot measurement challenge; framed since version 0.4.0 as agent-led modernisation of the existing retrofit model; since version 0.5.0 adds explainability and transparency controls (UK GDPR Articles 12 to 15 and 22A to 22C, explanation records, published prioritisation policy, AI capability register and output provenance); uses canonical FR, AC, NFR, CON, RULE and BG identifiers with a legacy BR and OBJ alias map | 2026-09-26 |
| [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) | Evidence, team and bounded assistant requirements for finding delivery constraints | 2026-09-19 |
| [Idea Register](../ideas/idea-register.md) | Research ideas that are not yet validated requirements | 2026-09-24 |
| [System One Decision Models for Retrofit Agents](../ideas/typesafe-system-one-agent-fit.md) | Research on typed decision models for IDEA-001 | 2026-09-24 |
| [Proper Warm CXO initial proposal](../presentations/proper-warm-cxo-initial-proposal.pptx) | Initial executive presentation deck | Binary file |
| [85-day roadmap](../case-study-85-day-roadmap.svg) | C-suite solution roadmap diagram, with its [Excalidraw source](../case-study-85-day-roadmap.excalidraw) | Binary file |

### Research Syntheses

| Document | Summary | Updated |
| --- | --- | --- |
| [Housing Association Primer](./research/sector/housing-association-primer.md) | What a UK housing association is, sector scale and archetypes, tenure types, lease responsibility rules for retrofit, resident needs, board capital patterns, funding model and implications for Proper North Homes | 2026-09-25 |
| [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) | Provisional sector benchmarks for energy, repairs, safety, grants, finance, delivery and quality | 2026-09-11 |
| [UK Social Housing Baseline Source Register](./research/sector/uk-social-housing-baseline-source-register.md) | Official publications and datasets behind each baseline benchmark | 2026-09-11 |
| [Company Profile Research](./research/company/company-profile-research.md) | Confirmed not-for-profit status, comparators, modelled customer profile (estimates, not company facts), common sector problems, role map and company gaps for the role agents | 2026-09-26 |
| [Agent Request Challenge](./research/company/agent-request-challenge.md) | Role-agent challenge of the five requested agents: real problems, non-agent alternatives, bounded AI fit, shared foundation, value tests and stop criteria | 2026-09-26 |
| [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | Role-agent challenge of measuring acceleration with a dashboard, short history and non-pilot comparison, plus the owner's modernisation decision: Comparison 1 and 2, frozen protocol, benefits scorecard, guardrails, vanity metrics and history sources | 2026-09-26 |

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
| [Project Memory](./memory.md) | AMA programme process, presentation guidance and owner preferences |
| [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | Coaching prompt that turns a recurring task into a Goal Card for an agent working in an assess, act, check and adjust loop |
| [Knowledge Base Log](./log.md) | Chronological record of knowledge base changes |

### Agents

| Agents | Purpose |
| --- | --- |
| `company-*` in [.github/agents/](../../.github/agents/) | Proper North Homes role agents for interrogating the problem. Grounded in [Company Profile Research](./research/company/company-profile-research.md) |
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

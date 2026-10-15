---
title: Project Knowledge Base
description: Entry point and index for the AMA Case Study 48 second brain, routing agents and people to the right evidence for each task
ms.date: 2026-10-15
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
| Design sensor data capture, map signals or prioritisation | [Sensor Data Capture, Analysis and Map](../adrs/0002-pilot-readiness-architecture.md#sensor-data-capture-analysis-and-map) | [Case Study 48 Addendum](../case_study_48_addendum.md#sensor-data-capture-analysis-and-map-demonstrator-design) and BRD RULE-014/AC-047; simulator only, with sensor inventory and operational thresholds still open |
| Design EPC C, energy standard or grant logic | [energy-efficiency/](./regulatory/energy-efficiency/) and [retrofit-standards-and-funding/](./regulatory/retrofit-standards-and-funding/) | [UK Social Housing Baseline Research](./research/sector/uk-social-housing-baseline-research.md) |
| Assess Responsible AI and operational activation | [RAI release position and verified recovery](../case_study_48_addendum.md#responsible-ai-release-position-2026-10-14) | [PRD RAI contract](../prds/zava-forward-retrofit-programme-demonstrator.md#responsible-ai-release-and-oversight-contract-2026-10-14) and [ADR control plane](../adrs/0002-pilot-readiness-architecture.md#responsible-ai-control-plane-2026-10-14); proposals pending human acceptance, not compliance certification |
| Handle resident data, consent or automated decisions | [data-protection/](./regulatory/data-protection/) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Write or review requirements | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Build or review a subsequent AMA prototype/PoC/MVP | [Subsequent Application Exercise Builds](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11) | BRD CON-007/AC-086 and PRD CON-009/AC-057 require actual AI/SQL/Azure on continuing generated data; [current model learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11) separates feasibility from parallel-experiment benefit |
| Retire a draft experiment or decide what to carry forward | [PM/UX draft closure review](./research/gap-analysis-next-build.md#draft-experiment-closure-review-2026-10-13) | Pinned #19/#24/#27 learning-only retirement recommendations, unresolved #58 capability queue, [UX evidence](./research/ux/prototype-learnings-and-simplicity-review.md#draft-ux-closure-review-2026-10-13) and [ADR regressions](../adrs/0002-pilot-readiness-architecture.md#retained-draft-architecture-learning-2026-10-13); owner-authorized PR closure is not product acceptance or resource teardown |
| Refine prototype usability from owner feedback | [Owner Usability Feedback (2026-10-07)](./research/ux/zava-forward-prototype-profile-review.md#owner-usability-feedback-2026-10-07) | [Zava Forward Workbench PRD](../prds/zava-forward-retrofit-programme-demonstrator.md); reported impressions and proposed checks are not verified implementation or acceptance |
| Understand all users' motivations, pains, gains and agent-assisted journeys | [Customer Journey Atlas](./research/ux/customer-journeys/customer-journey-atlas.md) | Nine linked company-role contributions, 28 stage-based maps, nomination/source-change subjourneys and 24 bounded opportunities; research hypotheses with current-delivery reconciliation, not observed user validation or approved features |
| Compare Azure development with M365 and business-platform implementation | [Implementation Options and Provisional Platform Recommendation](../case_study_48_addendum.md#implementation-options-and-provisional-platform-recommendation) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) and [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) |
| Evaluate a new idea | [Idea Register](../ideas/idea-register.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Migrate company/programme branding to Zava North Homes / Zava Forward | [One-off migration script and guide](../../tools/rename-zava.md) | Dry-run inventory, tracked text/paths, PPTX/YAML/logo handling, readable image assets and historical exceptions; [observed from-empty Azure rebuild](../../infra/README.md#from-empty-rebuild-observed-on-2026-10-12), real SQL/model checks, [callback-only initialization](../../infra/README.md#post-deployment-api-authentication-initialization) and [tenant provisioning consent boundary](../../infra/README.md#api-registration-management-with-the-existing-m365-session) |
| Configure public workbench entry and own Entra account photos | [Public welcome and Microsoft account photos](../../infra/README.md#public-welcome-and-microsoft-account-photos) | Exact public exemptions, delegated own-user User.Read, private token store/daily renewal, image-only Blob CSP and binary-render regression; real-user acceptance remains separate |
| Initialize tenant people and workbench roles | [Tenant staff and application-role initialization](../../infra/README.md#tenant-staff-and-application-role-initialization) | App-role plus SQL oid binding, private roster, preserved work codes/history, scoped Contractor and required cached-roster restart |
| Diagnose Microsoft account switching or interpret deployment learning | [Account selection and safe flow diagnostics](../../infra/README.md#account-selection-and-safe-flow-diagnostics) | [ADR identity/session mechanics](../adrs/0002-pilot-readiness-architecture.md#observed-exercise-identity-and-session-learning-2026-10-13), [PRD learning](../prds/zava-forward-retrofit-programme-demonstrator.md#review-learning-disposition) and [dated addendum observations](../case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213); chooser routes/logs are not authenticated-session acceptance |
| Review Azure Policy, Defender plans, locks, tags or policy exceptions | [Governance controls](../../infra/README.md#governance-controls) | Audit-mode policy, Free-until-approved Defender plans, pilot locks, tag standard and EX-001; cost, expiry and Deny stance open |
| Review identities, role assignments or Entra registration | [Identity and role assignments](../../infra/README.md#identity-and-role-assignments-issue-141) | Matrix checked against Bicep, no-shared-key tests, declarative app roles; owner sign-off, B2B guests and live comparison open |
| Rotate Key Vault secrets or review vault access | [Key Vault secret lifecycle](../../infra/README.md#key-vault-secret-lifecycle) | Inventory, expiry alerts, rotation order and access review; live rotation and owners open |
| Hand over the current #65 deployment or assess what merging approves | [Current exercise handover](../../infra/README.md#current-exercise-handover-2026-10-13) | [ADR delivery delta](../adrs/0002-pilot-readiness-architecture.md#current-exercise-delivery-delta-2026-10-13), [MVP limits](../../mvp/README.md#honest-limits) and [migration history exceptions](../../tools/rename-zava.md#deliberate-exceptions-and-edge-cases); historical identifiers stay exact and document merge does not approve product/pilot/production gates |
| Design System One scoring or assisted funding forms | [Decision 1 reassessment](../ideas/typesafe-system-one-agent-fit.md#microsoft-decision-1-reassessment-2026-10-10) | [PRD AI/form contract](../prds/zava-forward-retrofit-programme-demonstrator.md#ai-assisted-decision-coverage); evidenced scheme route, deterministic rules and Finance/human approval remain mandatory |
| Challenge whether a requested agent is needed, or decide what to build instead | [Agent Request Challenge](./research/company/agent-request-challenge.md) | [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) |
| Test whether richer inputs (phone photos, geotagging, structured invoices) change any agent verdict | [Agent What-If Study](./research/company/agent-what-if-study.md) | [Agent Request Challenge](./research/company/agent-request-challenge.md) |
| Design pilot measurement, baselines, comparison cohorts or a benefits dashboard | [Pilot Measurement Challenge](./research/company/pilot-measurement-challenge.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) |
| Practise constraint discovery, or test workflow and agent concepts on realistic records | [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) and its [data dictionary](./research/retrofit-synthetic-data/data-dictionary.md) | [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md); do not open the owner's answer key until blind findings are recorded |
| Explain agents in the retrofit process or their proactive use | [Process map and text equivalent](../capstone/README.md#agents-in-the-retrofit-process-2026-10-13) | [Five PRD contracts](../prds/zava-forward-retrofit-programme-demonstrator.md#five-reactive-and-proactive-assistants-2026-10-13), [runtime/config/API](../../mvp/README.md#five-retrofit-assistants-2026-10-13-implementation) and [ledger/source evidence](../adrs/0002-pilot-readiness-architecture.md#fresh-ledger-and-synthetic-coverage-learning-2026-10-13). Image05/enriched ledger baseline serves in revision12; five real operator model paths and SQL content survive restart, with no human/browser/semantic/value acceptance claim. Normal assistant authority remains off after bounded QA |
| Populate or rebuild the synthetic MVP operating baseline | [Dated generator recipe and coverage](./research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13); [needs inventory and phase gate](./research/retrofit-synthetic-data/README.md#synthetic-data-needs-inventory-and-phase-gate-2026-10-15); seeds, manifests and [refresh policy](./research/retrofit-synthetic-data/README.md#determinism-manifests-and-refresh-policy-2026-10-15) | [Provenance register](./research/retrofit-synthetic-data/provenance-register.json) and [dataset coverage](./research/retrofit-synthetic-data/data-dictionary.md#dataset-coverage-and-provenance), [Private JSON schema](./research/retrofit-synthetic-data/data-dictionary.md#separate-private-mvp-json-extension), 60000 stock versus 980 cases, dated visits and pending/unverified queues; retain private tenant staff bindings, and require effective reset authority before changing Azure SQL |
| Prepare or challenge the final presentation, architecture or pitch | [Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md) | [Project Memory](./memory.md), [Case Study 48 Addendum](../case_study_48_addendum.md), [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) and [85-day roadmap](../case-study-85-day-roadmap.svg) |
| Explain the solution architecture to executives or technical architects | [Executive and technical Excalidraw views](../architecture/README.md) | Source-linked interactions, official Azure icons, current single-API assistants versus deferred workers, development network exceptions and conditional M365; [ADR 0001](../adrs/0001-azure-architecture.md) and [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) retain decision history |
| Configure or troubleshoot rubric scoring authentication | [Capstone Rubric Gate](../../.github/rubric/README.md#owner-setup) | Built-in Actions token, job-scoped permissions and Copilot inference eligibility; compilation and a passing score do not establish product acceptance |
| Design a looped agent goal | [Capstone Deliverables and Storage Map](../capstone/README.md) | Where each capstone asset (deck, pitch transcripts, thought leadership artifact, code) must be stored for the rubric gate, and which criteria score 0 until it exists |
| [Loop Goal Designer Prompt](./method/loop-goal-designer-prompt.md) | [Project Memory](./memory.md) |
| Find proven use cases, customer evidence or reusable solutions | [Microsoft Industry Hub](./resources/microsoft-industry-hub.md) | [Case Study 48 Addendum](../case_study_48_addendum.md) |

## Catalog

### Project Documents

| Document | Summary | Updated |
| --- | --- | --- |
| [Original Case Study 48](../case_study_48_original.md) | Initial problem specification. Preserved unchanged | 2026-09-10 |
| [Case Study 48 Addendum](../case_study_48_addendum.md) | Preserved baseline and mandatory real-platform builds; dated rebuild/identity/session/CI learning and experiment-retirement boundary. Adds proposed RAI release/oversight gates and a provisional humidity/temperature simulator design, map signal and human condition-review path; no sensor inventory, thresholds or production authority is assumed. #19/#24/#27 may retire as learning; #58 needs explicit capability disposition | 2026-10-14 |
| [Recovered RAI baseline audit](../../.copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md) | Six-framework bounded audit of original v0.14.0/source baseline: 29 checks, 7 PASS/11 PARTIAL/11 NOT_ASSESSED; 8 MEDIUM/3 LOW residuals. Inline recovery and report contracts validated; baseline report owner-accepted on 2026-10-15 for remediation planning only; controls proposed/Not run, qualified approval pending, live use BLOCKED | 2026-10-14 |
| [RAI remediation implementation plan](../../.copilot-tracking/plans/2026-10-15/rai-remediation-plan.md) | Six phases/thirteen tasks covering eleven residuals and eleven unassessed evidence gates; current PRD v0.16.0 IDs, test ownership and default-deny authority. Independent standard critique Complete/Pass; offline engineering ready, real-service/legal/human/live gates remain | 2026-10-15 |
| [RAI remediation backlog coverage review](../../.copilot-tracking/github-issues/prds/rai-remediation/artifact-analysis.md) | Post-merge Functional Planner review: all thirteen tasks and 22 open checks map to twelve existing issues; owner review added chat issue 164; all thirteen body updates are now applied and verified, without enabling chat or implementing remediation. No issues were created. [Executed handoff](../../.copilot-tracking/github-issues/prds/rai-remediation/handoff.md) records completed owner review and verified issue updates; operational evidence gates remain. | 2026-10-15 |
| [Agentic Retrofit Programme BRD](../brds/agentic-retrofit-programme-brd.md) | v0.18.0 draft candidate: nine controlled workflows, human/resident authority, representative/commitment/remedy and in-use monitoring requirements through FR-048/AC-090. CON-007/AC-086 require real-platform exercise evidence; 50 FRs, 98 ACs, 11 NFRs, 7 constraints, 26 rules, 13 goals, 49 open decisions. v0.18.0 adds a proposal for per-user agent chat and memory (BG-013, FR-049/050, RULE-025/026, NFR-010/011, OD-44 to OD-49), inactive until the owner, DPO and Legal decide. Company baselines/approvals and measured benefits remain unresolved; fresh business/quality review required | 2026-10-14 |
| [Zava Forward Retrofit Programme Workbench PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) | v0.17.0 combined candidate: journey/sensor FR-048 to FR-050 and AC-062 to AC-068 retained; proposed RAI controls reconciled to FR-051 to FR-054/AC-069 to AC-073/NFR-014; adds a proposed per-user agent chat and memory section with a journey, agent and UI mapping (FR-055 to FR-059, NFR-015/016, AC-091 to AC-103, OQ-020 to OQ-025), inactive until BRD OD-44. 59 FRs/86 ACs/16 NFRs/9 constraints; fresh review and RAI dependencies remain. Historical acceptance and mandatory real-platform evidence do not approve these controls or live use | 2026-10-15 |
| [ADR 0001 Azure Architecture](../adrs/0001-azure-architecture.md) | Proposed full topology with current #65 handover and historical deployment IDs; proposed RAI release/version/incident boundaries apply to future workers, not evidence of isolated identities in the current MVP. Bicep in [infra](../../infra/README.md) | 2026-10-14 |
| [ADR 0002 Pilot-Readiness Architecture](../adrs/0002-pilot-readiness-architecture.md) | Lean five-assistant runtime, corrected shutdown/manual-access contracts, exact local image and actual disposable-SQL contract/recovery coverage. Adds a proposed RAI control plane and simulator-only sensor path through SQL, deterministic trend signals, map overlay and human review queue; device integration, thresholds and production approval remain open | 2026-10-14 |
| [ADR 0003 Journey-Derived Capabilities Runtime Fit](../adrs/0003-journey-derived-capabilities-runtime-fit.md) | Proposed: carry representative authority, confirmed commitments and open remedies in the existing SQL/API runtime and five bounded assistants; IoT Hub as the in-use monitoring ingestion product with deterministic review-only signals; no new assistant authority. Atlas remains hypothesis evidence | 2026-10-14 |
| [ADR 0004 Per-User Agent Chat and Memory](../adrs/0004-per-user-agent-chat-and-memory.md) | Accepted by the owner 2026-10-15 (OD-44); live personal data gated on OD-45 to OD-49: staff-only case-linked threads on the five existing assistants, then opt-in per-user memory in Azure SQL behind a DPIA gate; compares no chat, shared case memory and preview managed memory; open decisions for the owner, DPO and Legal (BRD OD-44 to OD-49; backlog #157 to #164) | 2026-10-15 |
| [ADR 0005 Regulatory Compliance Assistant](../adrs/0005-regulatory-compliance-assistant.md) | Operational proposal; owner permits synthetic development with labelled fictional roles, simulated approvals and original contract/grant fixtures (2026-10-15). No fabricated law, real sign-off or operational authority; versioned sources, deterministic alerts and cited home chat remain subject to qualified review. BRD FR-051, PRD FR-060. Phase 1 law store and read-only viewer implemented in `mvp/` (#210), seeded from the local snapshots; owners and review still unnamed |
| [In-Use Monitoring Analytics Research Plan](./research/iot-sensor-analytics-research-plan.md) | Phases R1 to R5 to find how to analyse IoT Hub humidity and temperature data (dew point, trends) with unverified leads, constraints and exit criteria; no method or threshold validated | 2026-10-14 |
| [Executive and technical solution architecture](../architecture/README.md) | Two editable Excalidraw views with official Azure SVG icons and SVG/PNG previews, grounded in #68. Executive view explains accountable workflow/value; technical view maps service, identity, storage, model, network, token, operational and deferred interactions. Sensor proposal is documented separately and not depicted as deployed. Static source snapshot, not new deployment or production acceptance | 2026-10-14 |
| [Capstone Rubric Review of the Agentic Retrofit Programme BRD](./research/company/capstone-brd-rubric-review.md) | Criterion-by-criterion readiness assessment of the BRD against the FY27 AMA capstone rubric, with floor analysis and a four-gate remediation plan | 2026-09-30 |
| [Retrofit Flow and Constraint Discovery Brief](../brds/retrofit-flow-discovery-brief.md) | Evidence, team and bounded assistant requirements for finding delivery constraints | 2026-09-19 |
| [Idea Register](../ideas/idea-register.md) | Research ideas that are not yet validated requirements | 2026-09-24 |
| [System One Decision Models for Retrofit Agents](../ideas/typesafe-system-one-agent-fit.md) | Dated #58 selection/generation feasibility and parallel experiment boundaries retained; historical revision ca-properwarm-mvp--0000018 restored exactly, not renamed into a fictitious deployment. No calibrated benefit, production selection or blanket spending authority | 2026-10-13 |
| [AMA mentor progress review](../presentations/ama-mentor-progress-review.pptx) | Published 15-slide deck, including the knowledge-organisation appendix, with Zava branding. Covers research, value challenge, governance, learning and mentor questions. #65 migration validation is recorded; 2026-10-13 audit confirms delivery bytes equal the working PPTX, superseding the earlier publish-blocked note. Existing narrative/layouts were not freshly redesigned. Maintained with `ama-mentor-deck`; working files remain under `.copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/` | Publication equality checked, 2026-10-13 |
| [Native agent process map](../capstone/deck/zava-forward-executive-draft.pptx) | Editable PowerPoint slide 13 in the 24-slide deck, retaining five native capability cards, human owners, on-request help, OFF-labelled proactive triggers and aligned deterministic workflow. [Current preview](../capstone/deck/agents-in-retrofit-process-native.png) and [text equivalent/value tests](../capstone/README.md#agents-in-the-retrofit-process-2026-10-13); original [SVG](../capstone/deck/agents-in-retrofit-process.svg)/[PNG](../capstone/deck/agents-in-retrofit-process.png) remain reference illustrations. Benefits hypotheses, not autonomous authority | 2026-10-14 |
| [Zava Forward executive capstone deck](../capstone/deck/zava-forward-executive-draft.pptx) | Current 24-slide UX/PPTX refresh: native executive architecture10, runtime19, operations23, deferred24 and retained native map13; top-aligned peers and source-linked notes. Explicit alternatives, evidence versus outstanding acceptance, planning-only owner/deliverable decision and return links. Planned 18-slide main route plus six optional appendices; no actual rehearsal or audience validation. Sole executive copy; authority/scans off and production approval separate | 2026-10-14 |
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
| [Retrofit Operating-Data Exercise Pack](./research/retrofit-synthetic-data/README.md) | Version 2.0.0: fifteen months of constructed operating records for 980 candidate homes. The case presents a professional team aware of bottlenecks but not where they occur. The pack covers the tracker, stage event log, property register, CRM contacts, supplier appointments, safety holds, QA and evidence, grant and finance, capacity, board reports and issues log, with realistic record-keeping imperfections, a data dictionary and a manifest. These records are for the exercise and are not evidence of actual company performance. The answer key and generator are held outside the knowledge base so analysis can stay blind. Stock-to-case link report and synthetic fabric attributes for the 60,000-home stock added; synthetic EPC, survey records and a seeded EPC conflict manifest added (#170) | 2026-10-15 |
| [Program Manager Document Workspace Journey](./research/ux/program-manager-document-workspace-journey.md) | Stakeholder-informed JTBD analysis, journey map, accessibility requirements and design handoff for the repository-backed Program Workbench canvas. All behavioural findings remain reported or assumed pending direct user research | 2026-10-02 |
| [Customer Journey Atlas and Company-Role Maps](./research/ux/customer-journeys/customer-journey-atlas.md) | Nine company-role contributions cover employees, professionals, residents/representatives, suppliers and external assurance readers: 28 stage-based maps, two missing subjourneys, motivations/pains/gains and 24 practical/exploratory agent requests with authority, fallback and non-AI comparisons. Snapshot provenance reconciled to Zava naming and current five-assistant operator evidence; no user/benefit validation or authority expansion | 2026-10-14 |
| [Regulatory Literacy for Journey Users and Agents](./research/ux/regulatory-literacy-for-journeys.md) | What each journey role should know about current law, with the agent integration pattern (desk research, 2026-10-15) |
| [Zava Forward Prototype Profile Review](./research/ux/zava-forward-prototype-profile-review.md) | Nine-role/eleven-perspective synthesis, owner feedback and eight proposed checks retained. Later pinned #24 filtering/reset source is reconciled without overriding reported owner experience or passing UX-02/03; no new user-validation claim | 2026-10-13 |
| [Prototype Learnings and Simplicity Review](./research/ux/prototype-learnings-and-simplicity-review.md) | Historical simplicity/platform learning plus requested UX Designer draft review: exact-intent/tab-local recovery, owner/source reconciliation and unique #58 journeys absent from main. Corrects untested first-task claims; real AI/SQL/Azure, human UX and quality/value gates stay separate | 2026-10-13 |
| [Zava Forward Workbench Design System Foundations](./research/ux/design-system.md) | Design tokens, component inventory with seven states, blocked-step and AI suggestion (SA-004) patterns, non-colour signal rules and a proposed extend-current-UI decision (issue #150). Owner confirmation, brand colours and map marker shapes remain open; no accessibility conformance claim | 2026-10-15 |
| [Zava Forward Workbench WCAG 2.2 Conformance Baseline](./research/ux/wcag-conformance-baseline.md) | Proposed WCAG 2.2 AA target and scope, first audit with computed contrast, fixes (focus indicator, field border, chart table equivalent), automated check coverage, manual check record per role and accessibility statement draft with known gaps (issue #151). Owner confirmation, rendered scanner, and all screen-reader, zoom and target-size tests remain open; no conformance claim | 2026-10-15 |
| [Zava Forward Workbench Content Standard, Glossary and Copy Audit](./research/ux/content-standard.md) | Plain-language content standard, status and next-action glossary, blocked-message pattern (reason, owner, next action), AI suggestion wording (SA-003, SA-004) and the core-flow copy audit (issue #153). Named human review of resident-facing wording, reading-age targets and user testing remain open | 2026-10-15 |
| [Chat and Memory Data Protection Analysis Record](./research/chat-memory-dpia.md) | Draft DPIA working record for per-user chat and memory: data map, decision record with no lawful basis, notice, DPIA or retention recorded, rights handling, logging, provider and redaction. DPO and Legal decisions remain open (issue #163) | 2026-10-15 |
| [Gap Analysis and Next Build](./research/gap-analysis-next-build.md) | Dated gaps/build direction and #65 recovery retained; PM/UX closure matrix pins four drafts, recommends learning-only retirement for #19/#24/#27 and keeps #58 unresolved with capability/requirement/evidence queue. No wholesale import, product acceptance or resource deletion | 2026-10-13 |
| [Decision 1 Behaviour Specification](./research/decision-1-behaviour-specification.md) | Clean-rebuild contract linked to the overall application design: workbench/API integration, scoring versus generation, human review and application boundaries, tasks, thresholds, provider contract, guard, liabilities and tests | 2026-10-11 |
| [Zava Forward MVP](../../mvp/README.md) | Continuing local/Azure application on retained constructed cases and private stock geography; real SQL/model evidence, Entra initialization, welcome/photo/account choice and current tests distinguished from historical snapshots. Full workflow, human, recovery, accessibility and production acceptance remain separate; evaluation dataset registry and seeded 60,000-home fixture added; frozen protocol, BG-011 MDE register, release decisions and breach pauses recorded (#126, no approvals claimed) | 2026-10-15 |

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
| `ama-*` in [.github/agents/](../../.github/agents/) | AMA helper agents for solution orchestration, presentation communications and backlog delivery coordination |

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

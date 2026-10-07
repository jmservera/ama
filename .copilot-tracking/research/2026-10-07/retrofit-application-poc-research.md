<!-- markdownlint-disable-file -->
# Task Research: retrofit-application-poc

| Field | Value |
| --- | --- |
| Date | 2026-10-07 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md |

## Research Brief

* What to research: requirements, prototype reuse, architecture boundaries and runnable PoC options for Proper Warm.
* Why it matters: demonstrate controlled property progression rather than disconnected agents.
* Audience or intended use: capstone stakeholders and implementation maintainers.
* Scope: current BRD/PRD, synthetic records, local containers and provisional Azure-led hybrid architecture.
* Non-goals: live resident data, consequential decisions, production compliance claims, unnecessary cloud spend or tenant changes.
* Criteria: executable end-to-end journey, fail-closed gates, explainable ownership, persistent audit, explicit synthetic/model status and resource inventory.
* Requested outputs: implementation-ready evidence supporting architecture and PoC.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1: current application contract; Q2: smallest credible runtime; Q3: authority and failure boundaries |
| Codebase scope | docs, existing prototype and implementation files discovered beneath this worktree |
| External scope | official runtime and Azure documentation |
| Initial internal candidate areas | docs/prds, docs/brds, synthetic pack, prototype, capstone guide |
| Initial external candidate areas | Azure Container Apps, managed identity, container runtime, application framework |
| Research posture | balanced |
| Posture provenance | bounded implementation against existing mature requirements |
| Explicit limits / deadline | none |
| Completion basis | scope coverage with adequate evidence and contrarian challenge |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints | no live authority; synthetic data; owner permission for resources does not prove tenant/company architecture approval |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Contract | Decision |
| --- | --- | --- | --- | --- |
| Instruction | AMA repository guidance | all paths | preserve original, index/log, controlled authority | selected |
| Skill | rpi-research | selected RPI Agent | three-wave evidence | selected |
| Skill | frontend-design / webapp-testing | application UI | implementation and browser validation | deferred to Implement |
| Specialist | hve-core-all:rpi-researcher | registered research lane | PRD/prototype evidence, no implementation | selected for substantial independent contract lane |
| Specialist | Housing roles | registered | hypothetical stakeholder review | skipped; existing PRD critiques already available |

## User Participation and Research Decisions

| Checkpoint | Context | Answer | Decision |
| --- | --- | --- | --- |
| Intake | complete full RPI loop using synthetic local PoC first | Enter automatic mode | proceed automatically; resource creation must be inventoried |

## Scope and Success Criteria

* Build scope is derived from the current PRD, not assumed to be the earlier read-only prototype.
* Verify available Docker, runtime and Azure tooling without exposing credentials.
* Record gaps separately from demonstrated behavior.

## Task Research Requests

* Owner requests architecture and PoC, authorises Azure/M365 resources where needed, requires documentation of everything created.
* Cloud and tenant resources are optional, not a mandate to create unnecessary infrastructure.

## Direction Controls

| Type | Boundary | Source | Effect |
| --- | --- | --- | --- |
| add | architecture and working PoC | owner request | include executable domain workflow |
| exclude | production resident/safety/finance authority | current BRD/addendum | synthetic demonstrations only |

## Research Questions

| # | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Which PRD workflows, contracts and prior prototype behavior must be carried forward? | depth | High | answered |
| Q2 | Which locally available runtime permits reliable container execution and tests? | straightforward | High | answered |
| Q3 | What challenges a proposed architecture or apparent successful PoC? | depth | High | answered |

## Prior Knowledge Gate

* Reviewed original, addendum, BRD opening, reference index and memory.
* Verified owner baseline: Azure-led hybrid is provisional and non-production; consequential human approvals remain open.
* Existing read-only prototype is not evidence of a working transactional application.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Plan: independent requirements/prototype lane; parent environment and architecture evidence.
* Worker: registered RPI Researcher owns `subagents/2026-10-07/retrofit-poc-contract-lane.md`; current PRD, prior prototype and synthetic-pack contracts.
* Reflection: current PRD is a stronger implementation contract than the original five-agent brief. Docker 29.8.2, Compose 5.5.1, Node 24.18.0, npm 11.16.0, Python 3.14.5 and Azure CLI 2.87.0 are present. Docker responds and the Azure session reports enabled. No account IDs, credentials or private tenant contents collected.
* Lane return: C7-C10 establish nine workflows, versioned case API, independent home gates, proposal-only AI, persistent handoffs and scope-reconciled metrics. Prototype is fixture/visual prior art only, not a transactional codebase.

#### Wave 2: Deeper

* Parent prioritised persistence, authority and minimum moving parts.
* Node `node:sqlite` successfully executed an in-memory prepared query. A dependency-free Node application can use built-in HTTP, SQLite and tests; SQLite has single-writer/scaling limitations and runtime-version sensitivity.
* W1/W2: Container Apps local storage is ephemeral. An unchanged SQLite app must not be deployed with multiple replicas or portrayed as durably stored in ACA.
* W3: managed identity authenticates the application, not the human decision-maker. Human authorisation must still exist in the domain API.
* Reflection: choose a local single-instance transactional PoC first; document Azure SQL-backed deployment as a target, not a tested lift-and-shift.

#### Wave 3: Contrarian

* Challenge: immediate Azure/M365 creation is not needed to demonstrate the current domain contract and would add cost, permissions and incomplete identity controls.
* Existing app/addendum demands measured value, not Azure service count (C5). A deterministic simulator must not be called an evaluated autonomous agent.
* A named-volume local store reduces deployment risk but does not prove immutable regulated audit or production reliability. Demo actor selection demonstrates role gates, not authentication.
* Reflection: no resource creation in Azure/M365 for the initial PoC. Include explicit target architecture, resource inventory, release blockers and task-level assistant evaluation.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Nine represented workflows and connected home journey | C4, C7 | accepted | minimum credible end-to-end PoC |
| Prior prototype as transactional base | C8 | rejected | no API/store/audit or recovery |
| Local Node/SQLite single-instance container | W1, W2, runtime probes | accepted | smallest viable persistent implementation without extra paid services |
| Production/cloud readiness | C3, C9, W2, W3 | deferred | identity, managed persistence, human approvals and customer evidence not supplied |
| Genuine AI/autonomy claim from deterministic fixtures | C5 | rejected | must disclose simulator and unevaluated model integration |

#### Cycle Re-entry Evaluation

* No additional cycle required: current application contracts, executable runtime and authority boundaries are evidenced. Production unknowns are explicitly outside this constructed PoC.
* Planning Readiness: Ready for bounded PoC; not for production.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | original requests five agents and approvals | docs/case_study_48_original.md:25 | view | High |
| C2 | deterministic controls and bounded AI replace end-to-end autonomy | docs/case_study_48_addendum.md:326 | view | High |
| C3 | Azure-led hybrid only provisional demonstrator baseline | docs/case_study_48_addendum.md:410 | view | High |
| C4 | end-to-end non-production journey required | docs/brds/agentic-retrofit-programme-brd.md:130 | view | High |
| C5 | scalable Azure control layer is candidate, and scripted flow is not agentic evidence | docs/case_study_48_addendum.md:470 | view | High |
| C6 | all twenty rubric criteria, section floors and no individual 1 apply | docs/reference/method/ama-capstone-assessment-guide.md:136 | view | High |
| C7 | shared versioned case/API and nine workflow scenario contract | docs/prds/proper-warm-retrofit-programme-demonstrator.md:136-149,292-308 | delegated view | High |
| C8 | prior prototype has only client-side interactions | .copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:908-1037 | delegated view | High |
| C9 | perspective selection is not identity; operational details unapproved | docs/prds/proper-warm-retrofit-programme-demonstrator.md:215-231,932-947 | delegated view | High |
| C10 | synthetic join/defect contract and metrics continuity | docs/prds/proper-warm-retrofit-programme-demonstrator.md:609-616 | delegated view | High |

### External Evidence

| ID | Finding | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | DatabaseSync supports prepared statements; API maturity is runtime-version-sensitive | https://nodejs.org/docs/latest-v24.x/api/sqlite.html | 2026-10-07 | High |
| W2 | Container/replica storage is ephemeral; Azure Files is separate persistent storage | https://learn.microsoft.com/en-us/azure/container-apps/storage-mounts | 2026-10-07 | High |
| W3 | managed identity provides app identity; service and human authorisation still differ | https://learn.microsoft.com/azure/container-apps/managed-identity | 2026-10-07 | High |

Context7 mixed some latest-major examples with v24. Implementation will use only APIs verified locally in Node 24 rather than newer statement finalisation methods.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | nine workflows, connected versioned home and owned exceptions | C4, C7-C10 | implement representative paths, disclose narrower-than-full-MVP coverage |
| Q2 | Node 24 built-ins, SQLite and Compose work locally | W1, environment probes | dependency-free local implementation |
| Q3 | cloud persistence, demo identity, synthetic AI and missing business approvals prevent production claims | C3, C5, C9, W2-W3 | document target separately; no tenant deployment needed |

## Alternatives and Decision State

* Selected: Node 24 modular monolith, SQLite persistent local volume, same-origin web UI, deterministic domain commands and bounded assistant simulator; Azure-led target with relational managed storage, Entra and optional governed M365 evidence.
* Evidence: C3-C5, C7-C10, W1-W3. Confidence high for local PoC, not a production selection.
* Rejected immediate tenant deployment: permissions are available but there is no need or verified data/identity contract; it would add cost without proving domain behavior.
* Rejected nine independent microservices: coupling around one versioned case and transaction warrants one process at PoC scale.
* Deferred managed model selection: provider adapter can be documented or implemented opt-in, but simulated output is not model evaluation.

## Open Questions, Risks, and Residual Uncertainty

Actual company data, human ratification, tenant permissions and production operating model remain unknown.

## Current Decisions

Automatic mode confirmed. Use synthetic local PoC first.

## Potential Next Research

Contract lane and environment probes below.

## Planning Readiness

Ready for bounded local PoC with documented production gaps. Evidence C3-C10, W1-W3. No research blockers. No human business/legal approval inferred.

## Research Disposition

Executed, complete. Automatic RPI Agent owns eligible Plan continuation.

## Self-Check

Opening state persisted before substantive research. Evidence and readiness will be reconciled after all three waves.

## Closeout Record

Wider, Deeper and Contrarian complete in order; specialist evidence recorded in `subagents/2026-10-07/retrofit-poc-contract-lane.md`. Parent accepted contracts, rejected premature production/autonomy claims and deferred operational activation.

## Advisory Next Step

Automatic parent activates rpi-plan with C3-C10 and W1-W3, then exactly one candidate critique. No routine owner input required.

## Sources

* W1 - Node.js SQLite - https://nodejs.org/docs/latest-v24.x/api/sqlite.html (retrieved 2026-10-07).
* W2 - Container Apps storage - https://learn.microsoft.com/en-us/azure/container-apps/storage-mounts (retrieved 2026-10-07).
* W3 - Container Apps managed identity - https://learn.microsoft.com/azure/container-apps/managed-identity (retrieved 2026-10-07).

## Artifact Self-Check

* [x] Questions answered, with production unknowns explicitly excluded.
* [x] All three waves, synthesis, re-entry basis and disposition recorded.
* [x] Evidence IDs, sources, extension provenance and authority boundaries recorded.
* [x] Recommendation and alternatives grounded; simulator and identity limits disclosed.
* [x] No secrets or live data collected; immutable regulatory snapshots preserved.

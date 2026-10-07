<!-- markdownlint-disable-file -->
# RPI Plan: Proper Warm Architecture and PoC

## Task Metadata

* Task ID: 4aaf9ee3-da69-4ebb-812a-edccc5637af7
* Task slug: retrofit-application-poc
* Planning status: Ready after one critique and direct corrections
* Plan date: 2026-10-07
* Phase details: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-07/retrofit-application-poc-plan-critique.md

## Executive Summary

Build a runnable local container application showing one home from candidate
to synthetic handover, with nine workflow representations, owned exceptions,
versioned evidence, persistent events and deterministic approval gates. Write
an Azure-led hybrid target architecture without pretending it is deployed.
Keep the demonstrator cheaper and easier to reproduce than a tenant-specific
build while exposing the exact work needed for operational release.

### User Decisions and Requirements Highlights

* Architecture and PoC are both deliverables; every created resource is inventoried.
* Automatic RPI loop confirmed. Synthetic local PoC first.
* Azure/M365 permission is available when needed, not a mandate to consume it.

### What You May Not Know

The existing HTML is read-only and its aggregate metrics do not reconcile with
its eight cases. This build requires a real state/API boundary. Demo role
selection is NOT authentication. Local SQLite is not an ACA multi-replica store.
The offline assistant is explicitly a simulator, not evaluated model autonomy.

### Unresolved Decisions or Blockers

No blockers for synthetic PoC. Live identity, resident data, professional,
legal and Finance approval, production model/region and platform selection
remain out-of-scope release blockers, disclosed in documentation.

## User Decisions and Requirements

* Build the architecture and a PoC of the application.
* Local Docker and Azure CLI are available; resources and M365 artefacts may be created if necessary.
* Document everything created.
* Enter automatic mode to complete Research, Plan, Implement and one Review.

## Goals

* Show reduced coordination ambiguity: what blocks a home, who owns it and what happens next.
* Demonstrate state, control gates and history rather than static screen navigation.
* Make unknowns, failure handling and production gaps inspectable.

## Scope and Non-Goals

### In Scope

* apps/proper-warm: Node 24, built-in SQLite/HTTP/test, same-origin vanilla UI, synthetic fixture cases.
* Nine workflow portfolio: prioritisation, technical readiness, resident service, capacity, hazards, quality, finance/grants, handoffs and portfolio.
* Connected synthetic lifecycle, role-gated commands, versioned audit, retries/idempotency, owned errors.
* Offline bounded evidence/draft assistant with disablement/failure path and evaluation.
* Local container build/run/persistence verification and browser interaction.
* Architecture, resource ledger, runbook, traceability/coverage and complete-rubric gap challenge.
* Git commit/push and PR to main under repository workflow; do not merge.

### Non-Goals

* Full PRD MVP compliance: workbook import/quarantine, bulk actions, full forecast/heatmap/history analytics, eleven production workspaces, actual document uploads and all external adapters remain disclosed gaps.
* Live safety clocks, resident contact, supplier instruction, payment, claims, production legal interpretation or tenant changes.
* Mandatory live model invocation or claims of agentic capability from a simulator.

## Functional Requirements

* Cases list/detail must disclose workflow, home/building IDs, lifecycle, current owner, blocker rationale, evidence versions, resident update commitment and handoff states.
* Case writes use only POST /api/cases/:id/commands with version + idempotency key and x-demo-role.
* Separate assessment and design roles, scoped resident decision, committed capacity, quality evidence, invoice match and grant stages; progression requires all applicable prerequisites.
* Hazard hold/referral remains separate and cannot be released or reclassified by this application.
* Contact/access is never consent; eligible no-access uses strict >5, excludes provider no-show/cancel/reschedule and never pauses hazard referral.
* Handoff sent/received/accepted distinct; current owner transfers only on acceptance, retaining resident-update owner.
* Assistant creates cited drafts only; no command or external action. Failure reports explicit error and owned manual task, never fabricated success.
* Portfolio metrics derive from exactly the active filtered case set and disclose numerator/denominator/as-of/synthetic status.
* JSON export preserves versions, evidence and events; no production immutability claim.

## Non-Functional Requirements

* Server prepared statements, transactional command+event+idempotency commit, optimistic version conflict and fail-closed rollback.
* Local-only host publication, same-origin checks for writes, bounded request sizes, safe DOM rendering and CSP.
* Non-root container, persistent named volume, no credentials, no third-party runtime dependencies.
* Structured request logs with correlation/latency/status, health/store probe and aggregate operational metrics.
* Keyboard-accessible forms, focus/announced updates, responsive UI and visible errors.
* Synthetic performance target: case-list p95 <=250ms over 100 sequential localhost requests, report measured scope rather than company SLO compliance.

## Acceptance Criteria

* AC-P01: Node tests cover all nine represented workflows, exact gate errors, separate authority, version conflicts, retry replay and same-key different-payload rejection.
* AC-P02: A happy home progresses candidate -> assessed -> designed -> resident_ready -> scheduled -> installed -> quality_accepted -> handed_over with sourced synthetic decisions; negative cases remain blocked.
* AC-P03: Restart preserves accepted commands and event history in SQLite; no reset on startup.
* AC-P04: Browser filtering, case selection, one command, assistant draft/error, export and lifecycle controls work with visible rejection states.
* AC-P05: Offline assistant evaluation reports cited draft validity and prohibited-action protection, labelled simulator-only; no model-quality claim.
* AC-P06: Documentation inventories container/image/volume/network/port/generated files and records zero Azure/M365 creations; run/stop/reset instructions target only these resources.
* AC-P07: Architecture alternatives, trust boundaries, failure domains, scale/migration path, cost-per-business-outcome assumptions and every rubric criterion/floor are disclosed.

## Implementation Context Record

| Item | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md |
| Changes | .copilot-tracking/changes/2026-10-07/retrofit-application-poc-changes.md |
| Critique | one final-candidate run executed; PC-001-PC-009 disposed |
| Continuation | automatic RPI parent completes publication, then one Review |

## Sources

* Research C3-C10, W1-W3 and contract lane.
* docs/prds/proper-warm-retrofit-programme-demonstrator.md v0.7.0, current requirements, not operational approval.
* docs/reference/method/ama-capstone-assessment-guide.md, all twenty criteria and floor rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Build controlled domain API

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement persistent cases, commands, audit and assistant

* Owner: backend implementer. Targets apps/proper-warm/src and tests.
* Dependencies: research and critiqued plan.
* Completion: semantic domain/API tests and deterministic assistant evaluation.

<!-- rpi:phase id=P02 -->
### [x] P02: Build the connected workbench

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement accessible UI using stable API contract

* Owner: frontend implementer. Targets apps/proper-warm/public only.
* Dependencies: agreed API contract; final integration requires P01.
* Completion: nine views, filters, case detail and command/draft/error paths.
* Evidence: config-driven public files delivered; syntax and in-memory contract
  smoke passed, including retained retry, replay and failure/task refresh.
  Real browser/server integration remains explicitly P04-T01.

<!-- rpi:phase id=P03 -->
### [x] P03: Document and containerise the architecture

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author architecture, runbook, inventory and coverage

* Owner: parent. Targets docs/architecture, apps/proper-warm/README.md and container files.
* Dependencies: plan; actual resource record finalises after execution.
* Completion: discoverable documentation, index/log updated, existing original and memory unchanged.

<!-- rpi:phase id=P04 -->
### [ ] P04: Validate, publish and review

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Run tests, container journey/persistence and browser checks

* Owner: parent. Targets tests/integration coverage and measured report.
* Dependencies: P01, P02 and P03.
* Completion: unit/API/evaluation pass, container healthy and responsive, browser and restart verified.

<!-- rpi:task id=P04-T02 -->
#### [ ] P04-T02: Commit coherent change, open PR and prepare one Review

* Owner: parent; automatic RPI parent subsequently owns the one Review.
* Dependencies: P04-T01.
* Completion: committed/pushed PR and reconciled review-ready evidence; no merge.
  Review execution/outcome and routed follow-ups belong to the subsequent RPI
  Review phase, not an implementation prerequisite for itself.

## Locked Change and Test Boundary

* Exact removals: none.
* Canonical targets: apps/proper-warm, docs/architecture/proper-warm-poc.md, docs/architecture/proper-warm-resources.md, README.md, .gitignore, docs/reference/README.md, docs/reference/log.md and current tracking artefacts.
* Maximum additions: one application directory with no third-party runtime dependencies, two architecture documents, task tracking evidence and at most one scoped CI workflow.
* Generated targets: SQLite data, image, named volume, container/network and session-only screenshots; never commit database/credentials/node_modules.
* Backend owns semantic tests (domain/API/assistant). Parent owns container/browser integration and performance checks. Existing unrelated tests stay untouched.
* Regression coverage: original research documents and existing prototype preserved, no extension changes.
* Evidence: tests and measured commands recorded in changes and resource ledger, not ungrounded pass claims.

## Dependencies

* Node 24.18.0 and Docker/Compose verified locally.
* Same-origin browser uses API contract; server does not depend on frontend state for authorisation.
* SQLite single process only; managed SQL/real identity must precede cloud scale-out.

## Critique Disposition

Execution complete, verdict Revise. All findings are compatible direct planner
corrections, resolved before implementation; no second critique.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | resolved | details frozen authority/stage matrix; separate assessment/handover acceptance |
| PC-002 | resolved | details validity/recovery contract and dependency invalidation tests |
| PC-003 | resolved | details replay algorithm, actor/intent binding and client retry/refetch |
| PC-004 | resolved | details shared shapes/action payloads and destination/receipt guards |
| PC-005 | resolved | details atomic seed, fail-closed startup and interrupted-write oracle |
| PC-006 | resolved | versioned manifest, paired homes, explicit reduced grant semantics |
| PC-007 | resolved | appointment dedup/evidence, rule version and single owned investigation |
| PC-008 | resolved | citation/prohibited-action evaluation and durable failure task |
| PC-009 | resolved | before-create collision checks, owned objects and ignored test data |

## Follow-Up Items

* Entra-backed identity and managed relational persistence before cloud deployment.
* Evaluate a real model on approved corpus before any AI/autonomy claim.
* Human operating-model and legal/control ratification before operational validation.

## Handoff

Ready for Implement. Critique executed once; PC-001 through PC-009 disposed
with concrete frozen contracts and acceptance oracles. No user decision required.

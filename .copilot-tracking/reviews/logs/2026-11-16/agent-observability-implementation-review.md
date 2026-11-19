<!-- markdownlint-disable-file -->
---
description: Scoped review of privacy-safe agent instrumentation and conditional Agent 365 capstone delivery
ms.date: 2026-11-16
---

# Review: Agent observability implementation

## Executive Summary

* Assessment: one confirmed development-install defect in P01/P02; P04
  publication is not yet complete.
* Review execution: Complete for the scoped comparison.
* Assessed outcome: Defects found.
* Validation coverage: 22 core, 79 worker and 10 API focused tests pass;
  strict core/agents/API types, focused Ruff and native capstone Verify pass.
* Limits: complete local gate and independent exact-head assessment pending.
  Draft capstone has reproduced baseline diagram provenance failures.

Parent Decision Record owns the final decisions.

## What You May Not Know

Direct Azure export was deferred by owner decision after SDK inspection.
Only explicitly enabled OTLP is implemented; no collector, tenant or model
activation is authorized. Diagnostics do not replace protected SQL governance,
financial evidence, meaningful explanations or human approval.

## Findings and Proposed Routes

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Fresh API and agents development installs omit the SDK

The new tests import the real telemetry SDK through the shared test fixture,
but these components' development extras install only core's base API.
The shared local environment already contained core's development extra and
therefore concealed this installation gap.

* Related scope: P01-T01, P02-T01/T02, FR-001/003 and P04 reproducibility.
* Expected: the existing per-component hosted/gate development installation
  can import and run its new tests without a prior core development install.
* Evidence: src/core/tests/telemetry_support.py imports opentelemetry.sdk;
  src/api/tests/test_keepalive.py and test_assistants_dispatch.py and
  src/agents/tests/test_dispatch.py import that fixture. API/agents
  pyproject.toml development extras omit core telemetry. Hosted src-ci.yml
  installs base dependency projects and only the selected project's dev extra.
  The independent lane also traced this ordering in the local gate.
* Impact: fresh selected component checks cannot import the new test modules;
  aggregate-environment passes are insufficient publication evidence.
* Resolution: fresh component-local installations must include the pinned SDK
  and exporter, run affected tests/types and pass the full exact-head gate.
* Proposed destination: rpi-implement; fix the development dependency contract,
  not skip tests or weaken CI.

Other helper candidates were not accepted as defects: cancellation is a
bounded error classification and the runbook excludes naive business failure
rates; stop/redelivery labels describe distinct existing paths; standby
deliberately stays cheap; API invalid configuration already fails explicitly
with a content-free exception; documented optional SDK installation remains a
prerequisite. Structured logs are intentionally console records under P02-T02,
not an implied new OTLP log transport. No unsupported metric-name allegation
is adopted: names were verified against the current GenAI sources during
implementation, including the moved convention repository.

## Parent Decision Record

### Current Disposition

* Based on events: RD-001 through RD-007.
* Review execution: Complete.
* Final outcome: Defects found; RV-001 requires correction before publication.
* Finding decisions and next actions: RV-001 resolved by child implementation/
  fresh-install evidence, not by rewriting this original assessment. Child
  P04 evidence now supports publication; owner retains PR review/merge.
* Decisions still needed: none; walkthrough skipped-auto.

### Decision History

| Event | Subject | Decision source | Status or value | Proposed destination | Final destination | Owner | More information needed | Smallest next action | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| RD-001 | participation | user/automatic parent | agent-owned | none | Review | parent | comparison | Assess P01-P03 | User selected Handle it end to end; standard depth default |
| RD-002 | walkthrough | automatic parent | skipped-auto | none | none | parent | none | Decide from evidence | Retained automatic participation |
| RD-003 | RV-001 | parent verified source/independent lane | accepted | rpi-implement | rpi-implement | agent | fresh-install proof | Correct dev extras and test isolated installs | SDK fixture imports are not satisfied by component metadata |
| RD-004 | execution/outcome | parent | Complete / Defects found | none | none | parent | publication checks | Preserve this original result | Scoped comparison complete; not acceptance or an exact-head gate |
| RD-005 | continuation | automatic parent | required in-scope correction | rpi-implement | rpi-implement | agent | RV-001 resolution plus P04 | Resume bounded correction and publication | No new critique or Review phase authorized |
| RD-006 | RV-001 resolution | child implementation validation | resolved | rpi-implement | P04 publication | agent | full receipt/exact-head assessment | Commit correction and original evidence | Fresh agents 79 tests/types and API 10 tests/types plus pip check pass; identity guard retained |
| RD-007 | Child publication acceptance | parent from completed child evidence | P04 complete; original Review outcome preserved | Follow-up | owner PR review | owner | human merge approval, separate from delivered scope | Review #1823 and #1834 | Exact head 425b7d76/base 4c3f1d13 passes all 17 local groups with immediately verified receipt and all ten hosted jobs in run 43973038649. Bounded independent assessment has no publication blocker; helper Partial read-limit and parent gap reconciliation preserved. Draft deck remains Partial, no live acceptance or second full Review claimed |

## Validation Evidence

| Check | Scope | Status | Summary |
|---|---|---|---|
| Focused unittest | Core telemetry/diagnostics | Passed | 22 tests, including real SDK export isolation |
| Focused unittest | Worker dispatch/runtime/queue/lifecycle/dependency | Passed | 79 tests |
| Focused unittest | HTTP and actual assistant composition | Passed | 10 tests |
| Strict mypy | Core/agents/API | Passed | 328/57/305 source files |
| Ruff | Changed runtime and tests | Passed | Focused lint/format |
| Native Build/Verify | Existing capstone | Passed | 55 slides/notes, 32 shape checks, protected financial XML unchanged |
| Preview | Delivered draft | Passed | 55 pages, 108 jumps, 10 preview tests |
| Diagram generators/architecture | Draft provenance | Failed | 2 generators and 4 assertions also fail on exact pre-change HEAD 723d5026 |
| Full local receipt/hosted CI | P04 | Unavailable | Not yet run/published |
| Live Azure/model/Agent 365 | Excluded | Skipped | No live authorization |

## Risks, Blockers, and Residual Work

* P04 remains active: full gate, independent exact-head assessment, publication
  and observed hosted CI, with owner merge approval.
* Existing diagram provenance failures remain a separate unselected follow-up;
  the draft receipt is Partial, not a fully validated presentation claim.
* Original checkout contains unrelated ignored inputs and a newly dirty,
  unrelated paper PDF; preserve them and validate a clean committed worktree.

## Review Record

### Scope and Evidence

* Task: agent-observability-implementation, 2026-11-16.
* Review scope: P01-P03 and P04 readiness; no claim of P04 completion.
* Candidate: 1212f5db62bc6ebc975f0d804a6e8b1d485d039b, implementation
  64d26bd6 plus owner-authorized merge of main bfed6c99.
* Depth: standard, default. Participation: agent-owned, user-selected automatic.
* Review execution: Complete.
* Plan: .copilot-tracking/plans/2026-11-16/agent-observability-implementation-plan.md
* Critique: .copilot-tracking/reviews/plans/2026-11-16/agent-observability-implementation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-16/agent-observability-implementation-changes.md
* Research: .copilot-tracking/research/2026-11-16/agent-observability-agent365-research.md
* Helper: one independent runtime-contract comparison for P01/P02 and packaging,
  using RPI Reviewer host defaults; parent retains business/deck/operating
  evidence and owns findings. Exact-head continuation will reuse that context.

### Opening Review State

* Goal: assess source/offline observability and future-only presentation against
  approved scope without mistaking diagnostics for business governance.
* Evidence readiness: P01-P03 marked complete with explicit draft validation
  limits; merged candidate is committed. Publication evidence remains pending.
* Acceptance basis: FR-001 through FR-005, NFR-001 through NFR-003, cited
  PRD/BRD/ADRs and PC-001 through PC-006.
* Boundary: source, tests and supplied validation; no real data or deployment.
* Authority: parent writes only this Review record during assessment; helper
  findings are suggestions requiring verification.
* Initial blockers: no review blocker; P04 gate and hosted evidence outstanding.

### Acceptance and Change Coverage

| Requirement or scope | Implementation and evidence | Assessment |
|---|---|---|
| P01-T01, FR-001/003, NFR-001/002 | telemetry.Configuration/initialize/operation, real-SDK resource/sampling/canary/blocked-export tests and independent source comparison | Runtime foundation supported; fresh component dev installs fail RV-001 |
| P02-T01/T02, FR-001/002/003 | HTTP keep-alive/no-response, actual assistant composition, worker late-thread/slot/postback regressions and diagnostic tests; wrapper/source comparison | Causal, privacy and existing control contracts supported within offline scope; RV-001 blocks fresh execution |
| P03-T01, FR-004 | infra/monitoring-runbooks.md, Explicit OTLP Instrumentation: exact enablement, source/offline/live matrix, protected audit joins, sampling and denominator limits | Met within source/documentation scope; no live acceptance |
| P03-T02, FR-004 | docs/capstone/source/slides.json existing future-roadmap slides, generated pitch/questions-and-answers.md B27; native Verify after main merge | Met as synchronized draft with explicitly Partial diagram receipt |
| P04-T01, FR-005, NFR-003 | Committed candidate descends from current main; complete receipt, exact-head assessment and hosted CI not yet available | Not assessed for publication; remaining active work |
| PRD-2026-AMA48-001 NFR-004, docs/prds/zava-forward-retrofit-programme-demonstrator.md | Protected business audit retained; telemetry adds random correlation, not an actor or source of business authority | No intended-outcome drift; runtime lane still checking implementation |
| PRD NFR-007, same source | Runbook Harm/billing/meaningful explanations row and Agent 365 adoption gates distinguish reconstruction/explanation from traces | Existing forecast contract unchanged; forecast acceptance not newly assessed |
| PRD NFR-011, same source | Runbook enablement, disable-and-restart, privacy/retention/network/owner gaps and finite export/shutdown behavior | Source guidance supports operability; live owner/restart/retention acceptance explicitly unproved |
| PRD NFR-014, same source | Runbook evidence matrix and remaining harm/quality/incident obligations | No new harm-monitor or live-threshold claim; existing business contract preserved |
| PRD NFR-017, same source | Runbook Metrics and safe synthetic receipt retains supplier billing/consumption as financial authority | Metering intent unchanged; reconciliation and live budgets unproved |
| PRD NFR-019, same source | Runbook privacy boundary excludes raw content/PII; provider and HTTP synthetic canaries; default-off export | Source-level support, not resident-slice security/retention/DPIA acceptance |
| PRD Observability and SLO Measurement Method, same source | Owned SDK service/environment/SDK resources; structured log fields; seconds histograms; explicit scenario-denominator gap | Implemented subset only; no accepted business-scenario p95/error-budget assertion |
| BRD-2026-AMA48-001 NFR-004, docs/brds/agentic-retrofit-programme-brd.md | Existing timeout/slot/manual-control tests and no hazard-control edits | No design-intent drift; operational outage/restart acceptance unproved |
| BRD NFR-012, same source | Protected consumption remains authoritative; diagnostic metrics have no monetary/financial-authority claim | No intended-outcome drift; invoice reconciliation not delivered |
| BRD NFR-014, same source | No identity/grant/retention/control change; no raw document/resident diagnostics or Agent 365 activation | Existing boundaries preserved in scope; not new resident approval |
| ADR 0001 worker identity boundary, docs/adrs/0001-azure-architecture.md | SDK packaging grants no identity permission; optional worker still posts results to API, not direct SQL/blob access | No architecture-decision drift |
| ADR 0006 dependency direction, docs/adrs/0006-src-layout-and-cutover.md | Shared core owns instrumentation; workloads consume core; five locks remain explicit; no legacy layout or private-data access | No architecture-decision drift |
| Owner OTLP-first decision and native-deck selection | Azure exporter absent from shipped declaration; only existing native capstone updated | Confirmed scope retained |
| Owner advanced-main decision | Feature commit 64d26bd6 followed by merge 1212f5db, preserving research parent and no rewrite | Authorized integration completed |

Business-source metadata: PRD v0.21.0 remains in-review/unsigned, owned by
AMA project owner (exercise approval) and Retrofit Programme Manager (exercise
product-owner role). BRD v0.21.0 remains draft, owned by AMA Research Team.
Both have empty supersession arrays. ADR frontmatter records no status or
deciders fields; their bodies state Proposed (0001) and Accepted (0006).
These are not new approvals. Changes record Business Alignment is None;
the bounded delivery and explicit unproved acceptance do not change a cited
outcome, business rule, constraint, KPI or accepted decision.

### Critique and Follow-Up Assessment

PC-001 through PC-006 remain resolved in plan task requirements and decisions:
real SDK/privacy/configuration cases; scenario-versus-invocation evidence
matrix; tooling/status/source clarification; numeric export bounds and image
locks; random diagnostic IDs versus protected business joins; explicit failure
handling and Agent 365 schema incompatibility caveat. The original Complete/
Revise critique is preserved, not regraded.

The Azure SDK inspection led to an explicit pause and owner-selected OTLP-only
correction before dependent completion. Its rationale is independently
observable in package selection and the operating/deck caveats; no private
vendor patch or fabricated Azure ingestion evidence. The owner separately
authorized main integration. No new business approval is inferred.

| Follow-up | Why outside immediate scope | Owner/next action | Assessment |
|---|---|---|---|
| Baseline diagram provenance | Both generators and four architecture assertions fail on exact pre-change HEAD 723d5026 and this candidate; diagrams retain incumbent semantics | Separate provenance maintenance scope | Keep explicit Partial draft receipt; native Verify and runtime gate do not cover those failures |
| Live collector/Azure/Agent 365 and full scenario/harm/billing evidence | Explicitly excluded from current authorization | Accountable operator/control owners after approval | Deferred, not success; cannot be used to approve live release |

### Reviewer Self-Check

* Scoped contracts, supplied validation, source intent, decisions, critique
  and residuals assessed once; publication/live limitations remain explicit.
* RV-001 was verified against the actual manifest and hosted install commands,
  not accepted solely from helper recollection. Its realized fresh-import
  failure is still to be reproduced during correction.
* Independent lane returned Partial after excessive investigation; no tests,
  installs or repository writes were performed by it. Parent does not adopt
  its speculative lower-impact leads as demonstrated defects.
* Source was not changed during Review; only this record was written.
* Original Complete/Defects found assessment and accepted route are preserved
  for later correction evidence, not overwritten with a passing verdict.

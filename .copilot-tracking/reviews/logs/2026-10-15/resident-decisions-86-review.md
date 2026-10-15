---
title: Resident decisions implementation review
description: Single post-implementation RPI Review for issue 86
ms.date: 2026-10-15
---

## Scope and Evidence

* Task ID: issue-86 / resident-decisions-86.
* Review date: 2026-10-15.
* Review scope: full bounded implementation P01-P03; publication follows Review.
* Assessed boundary: resident-owned scoped answers, representative authority,
  dependent release, redress, privacy, src placement and local evidence.
* Plan: .copilot-tracking/plans/2026-10-15/resident-decisions-86-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md
* Plan critique: .copilot-tracking/plans/2026-10-15/resident-decisions-86-critique.md
* Changes: .copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md
* Research: .copilot-tracking/research/2026-10-15/resident-decisions-86-research.md
* Other evidence: changed core/API source and tests, component guides,
  reference index/log, local five-project validation and browser results.

## Opening Review State

* Interpreted goal: compare the implemented synthetic exercise against the
  reconciled plan and issue criteria, without claiming operational acceptance.
* Evidence readiness: one unambiguous artifact set, six critique dispositions,
  completed local commands/results, documented owner/live evidence gaps.
* Acceptance basis: A1-A5, P01-P03, PC-001 through PC-006, user constraints,
  Accepted ADR 0006 and the src parity mapping.
* First comparison boundary: core decision/authority and release semantics,
  then API/UI, regression evidence and remaining acceptance.
* Active read-only boundaries: only this canonical Review record may change
  during Review; no implementation, plan, details or changes edits.
* Initial blockers: none for reviewing the bounded implementation. Full
  operational acceptance is explicitly outside the available evidence.

## Execution Status

* Execution status: Complete.
* Review execution evidence: artifact reconciliation and direct source/test
  comparison; no repeated critique and no second Review planned.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01, A1-A2 | Core semantics and guards | Reconciled | Exact context, supplied source, immutable history, latest task/date/contact authority |
| P01-T02, A3 | Guard and transaction wiring | Reconciled | Case-wide advance versus explicitly bound work orders and QA records |
| P02-T01 | API/UI wiring | Reconciled | Blank answer selection; actual actor from session; existing endpoint reused |
| P02-T02 | Two new modules and affected fixtures | Reconciled | JSON/SQLite semantics and actual local HTTP; no removed tests |
| P03-T01, A5 | Recorded command/results | Reconciled | All src suites and quality checks pass; Docker denial and live gaps explicit |
| P03-T02 | Existing guides and reference index/log | Reconciled for documentation | Review now executed; commit/push/PR intentionally follow Review |
| A4, Follow-Up Items | Unmet Acceptance and Follow-Up | Reconciled, not accepted operationally | Named local review/complaint records are not real resident access evidence |

## Completed Work Assessment

| Marker | Files | Change and purpose | Evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/resident_decisions.py | Explicit measure/scope/design, versioned representative task/date/source/wishes/contact, independent review | Source comparison and JSON/SQLite negative tests | Supports bounded A1-A3; no inferred consent |
| P01-T02 | src/core/src/zava_forward/core/{store,sqlstore,procurement,quality,projection,ai_tasks,insights}.py | Current release checks, per-operation bindings, detached restricted projections, scoped status and AI labels | Stale two-store release refusal, sibling work/QA release, projection/restart tests | Source and regression evidence consistent |
| P02-T01 | src/api/src/zava_forward/api/server.py and web/{app,panels,ops}.js | Existing authenticated endpoints, explicit bindings and blank supplied-answer forms | Actual loopback HTTP and browser/static checks | Resident consent remains human-owned |
| P02-T02 | src/core/tests/test_resident_decisions.py; src/api/tests/test_resident_api.py; affected fixtures | Source-backed synthetic readiness rather than legacy acceptance | Complete project suites, no removed tests | Synthetic fixture clean scan is explicitly labelled and production scanner unchanged |
| P03 | src/core/README.md; src/api/README.md; docs/reference/{README,log}.md | Contract, endpoint, evidence limits and knowledge routing | Relative path review and diff | No memory, regulatory, original case study or mvp change |

## Implementation-Time Plan and Detail Update Assessment

| Area | Update and reason | Trigger and user intent | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T02 | All aggregate answers are historical, including refusals | Original research selection and sibling-isolation criterion | Removed stale details phrase that treated legacy refusal as another hold | Immediately relevant clarification, not scope expansion |
| P01-T02, PC-001 | QA release uses its own measure/context binding | Case-wide check would block independent sibling QA | Details, source, tests and component guides agree | Preserves approved binding/isolation direction |
| P02-T02 | Synthetic readiness metadata marked synthetic clean | Scanner regression tried to fetch nonexistent fixture blobs | Only test fixture records changed; scanner code unchanged | Necessary fixture correction, not weakened scanning |
| P01-T02 | Resident dependency state cleared on successful save and lock exit | Direct inspection before Review found duplicated exit cleanup | Cleanup moved and nested-lock regression added; full core rerun | Preserves existing transaction lifecycle |
| P02-T01 | Disclosure check returns normal authorized staff projection | Existing resident endpoint response convention | API guide explicitly states no send/token or transport | Justified compatibility detail; not recipient disclosure |

## Critique and Material Revision Assessment

* PC-001: explicit work-order version and QA bindings; unknown bindings refuse;
  B-only release succeeds with A paused/withdrawn; fresh acceptance needs review
  evidence. Dependency applicability is not inferred from free text.
* PC-002: registration/currentness compare the technical design counter;
  revisions are monotonic and technical design changes invalidate old answers.
* PC-003: exact latest authority lineage and exclusive review-date boundary are
  rechecked at use and transactional commit; multiple representatives, disputed/
  revoked authority and safe-contact change-back have negative controls.
* PC-004: projected context/history are copied before redaction; narrative/
  authority fields require both resident-workflow and recorded-need roles.
  Audit/model inputs exclude new wishes/authority narratives.
* PC-005: checked-address template refusal is decoupled from staff-facing AI
  proposals, preserving adapter/release/human approval controls.
* PC-006: review binds an actual recorded decision actor; reviewer differs from
  actor and handler and exclusively updates/closes it. No consent mutation.
* All six dispositions are compatible with confirmed user intent. The
  implementation clarifications above do not require a new architecture or
  significant owner decision. One final-candidate critique was executed;
  no repeat critique or early resumption across an unresolved decision occurred.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Route |
| --- | --- | --- | --- |
| Operational authority/retention permissions | Cannot infer legal/company policy from a demonstrator | Owner/compliance ratify field roles, lifecycle and retention | RV-001, distinct governance follow-up |
| Formal complaints and real accessible independent review | No real route/integration or human participant evidence supplied | Service/resident-engagement owner supplies and validates actual routes | RV-002, distinct service-acceptance follow-up |
| Actual inference, SQL Server/Azure and container execution | Local fixtures are not authorized live infrastructure evidence; Docker daemon denied | Authorized technical owner/CI supplies actual evidence | RV-003, distinct runtime-evidence follow-up |

These remain outside P01-P03 implementation completion and full issue acceptance.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Operational authority and retention policy remains unratified

* Evidence: representative records say retention Unknown; core/API guides and
  plan Follow-Up Items explicitly label the exercise role intersection.
* Impact: local field controls cannot be claimed as approved operational policy.
* Destination: distinct governance follow-up; owner/compliance decision before
  production use, with `rpi-plan` only after that supplied decision.
* Smallest next action: ratify the authority lifecycle, permitted roles,
  safe-contact and retention rules against the documented exercise contract.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Real complaints access and without-detriment acceptance is unproven

* Evidence: service_open creates an owned local record, not an external
  submission; the panel explicitly says so. Core/HTTP tests show state
  independence, not real resident reachability or human review quality.
* Impact: issue #86's fourth criterion remains unticked. An actual resident
  cannot be claimed to reach the association's formal complaints route.
* Destination: distinct service integration and human acceptance follow-up.
* Smallest next action: named service/resident-engagement owners supply actual
  accessible formal and independent-review routes and acceptance evidence.
  Do not invent URLs, response commitments or delegated decision rights.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Actual runtime and container evidence remains unavailable locally

* Evidence: synthetic AI adapter and SQLite/loopback tests; Docker socket
  permission denial; no actual model, SQL Server or Azure invocation.
* Impact: local tests cannot certify live inference, SQL Server transactions,
  deployment or images. Existing dependency rules and release gates are not
  substitutes for runtime evidence.
* Destination: distinct authorized runtime-evidence follow-up and CI image checks.
* Smallest next action: let CI run image/project checks, then use approved
  synthetic data and authorized services for real inference/SQL Server/Azure.

## Defects

* No implementation defect established within the assessed bounded source/test
  boundary. This is not a vulnerability audit or a full operational acceptance.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct governance follow-up | Owner/compliance ratification, then rpi-plan | Missing operational policy, not invented implementation scope |
| RV-002 | Distinct service/human-acceptance follow-up | Service/resident-engagement owner supplies real routes/evidence | Explicitly unmet issue criterion |
| RV-003 | Distinct runtime-evidence follow-up | CI and authorized technical owner | Local environment/evidence limit |

## Residual Work

* RV-001 through RV-003 remain open and must not be reported as completed.
* No source correction or second Review is started in this task.

## Blockers and Remaining Work

* No blocker to publishing the bounded PR with Refs #86.
* Full issue/operational acceptance remains blocked by RV-001 through RV-003.
* Remaining lifecycle work: authenticated commit, push only the named topic,
  open PR to main with complete command/results, and leave merge to owner.

## Validation Evidence

| Command or check | Status | Summary |
| --- | --- | --- |
| Project unittest discovery, commands in changes artifact | Passed | Core 343; API 479 run/97 skipped; agents 70; orchestrator 17; importer 39 |
| Per-project ruff check/format --check/mypy | Passed | All five configured project checks; core/API rerun after final cleanup |
| API test_resident_api and test_document_controls | Passed | 16 after cleanup; actual health/app/authenticated loopback and SQLite restart |
| checks.design_system_browser_check | Passed | Existing keyboard/reflow/forced-colour/reduced-motion checks, no uncaught JS |
| Namespace entrypoints and dependency-rule suites | Passed | Five namespace distributions; no core workload import or new image dependency |
| node --check app.js, panels.js, ops.js | Passed | No JavaScript syntax errors |
| git diff --check; forbidden-path diff; state JSON | Passed | No whitespace errors or changes in mvp/.env/.vscode/github-issues |
| docker info | Unavailable | Permission denied on daemon socket; no escalation or image claim |
| Actual inference, SQL Server, Azure, resident/formal-route acceptance | Unavailable | Not supplied or authorized; synthetic tests are not actual evidence |

## Outcome

* Outcome: Residual work.
* Severity summary: 0 Critical, 0 High, 3 Medium, 0 Low.
* Rationale: bounded implementation and local evidence support A1-A3 and A5.
  A4 remains incomplete; Review must not call the full issue conformant.
  Explicit owner/service/runtime follow-ups are not defects silently added
  to current implementation scope.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None established | No return to Implement or repeat Review |
| Decision gap | Distinct RV-001 governance follow-up | Operational owner/compliance ratification |
| Material evidence gap | Distinct RV-002/RV-003 follow-ups | Real service/human and authorized runtime evidence |
| Non-blocking residual work | Publish bounded PR | Parent completes commit/push/PR, then awaits selection |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: all local src project suites/quality checks and synthetic
  local app/browser evidence; explicit Docker and actual/human evidence limits.
* Blockers: none to PR publication; full acceptance remains open as above.

---
title: Issue 166 needs inventory implementation review
description: One post-implementation review of the bounded engineering delivery
ms.date: 2026-10-15
---

## Metadata and assessed boundary

Task issue-166 / issue-166-needs-inventory. One Review execution started.
Boundary: inventory/scenario integration, public provenance corrections,
documented iteration/build-start gate, core regression tooling and recorded
local verification. Publication is an authorized parent action after Review.
Not application acceptance, full #103 delivery, owner ratification or live
AI/SQL/Azure verification.

## Inputs

* .copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md
* .copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md
* .copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md
* .copilot-tracking/changes/2026-10-15/issue-166-needs-inventory-changes.md
* Current scoped Git diff and new scenario manifest.

## Execution and outcome

Execution: Complete. Outcome: Residual work.
One complete comparison was performed inline; no independent uncertainty
justified another subagent. No implementation fixes or repeat Review ran.
No engineering defect identified in the bounded metadata/test changes.
Full issue acceptance remains open for the routed items below.

## Plan-to-change reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Inventory v1.2.0 retains all thirteen complete SN rows; exact reciprocal scenario path; sensor generator distinguished from canonical materialization | Complete |
| P01-T01 | Scenario v0.1.0 binds version/date/reviewed IDs, synthetic label and automated-review identity; all eleven/nine paths/checks deferred | Complete for integration seed, not full #103 |
| P01-T01 | Provenance v1.1.0, pack/core guides, reference routing row and append-only log | Reconciled, no private data read or published |
| P01-T02 | Existing test file retains structural/gap checks; five new methods exercise canonical data and twelve negative mutations | Complete, eleven tests passed |
| P02-T01 | Selected core and four other suites, five-project lint/format/mypy, isolated changed-file checks, synthetic HTTP smoke | Complete with explicit exclusions/skips and Docker limit |
| P02-T02 | Review once, then authorized commit/push/main PR | Review complete; publication remains parent action |
| Plan follow-ups | Owner approvals/historical matrix and full #103 evidence kept outside local completion | Distinct routes below; not implemented in this task |

The gate still requires issue/PR citations before a data-consuming build
starts, and owner scope/volume decisions for partial/missing coverage.
Regression tests check recorded metadata, not chronology or authority. The
review checks do not approve the inventory or residents' decisions.

## Implementation-time updates and critique dispositions

PC-001: two private-reader provenance cases were removed from the selected
suite before execution, not patched or run and later suppressed.
PC-002: scratch/TMPDIR preflight resolved inside the assigned worktree;
constructed fixture generators and app used owned temporary paths.
PC-003: fresh account resolution and derived author/committer identity remain
mandatory before publication; not yet claimed executed at this review point.

The initial 102-character lint lines and incorrect shared PYTHONPATH were
ordinary implementation/invocation corrections, fully recorded. Passing
reruns cover them. No material scope/architecture/user decision changed,
therefore no repeated planning critique or extra user approval was needed.
Plan/detail markers and remaining publication action agree with changes.

## Validation evidence

| Check | Result | Boundary |
| --- | --- | --- |
| Core selected discovery | Passed, 264 tests | Two named private readers Not run |
| Agents discovery | Passed, 70 tests | Documented invocation, no shared core PYTHONPATH |
| API discovery | OK, 459 tests, 92 skipped | SQL Server/opt-in checks not run |
| Orchestrator/importer | Passed, 17/39 tests | Existing constructed fixtures |
| All five ruff/format/mypy runs | Passed | Existing migration exemptions still apply |
| Isolated changed-test lint/format and strict mypy | Passed | Bypasses migration exemptions; one source file |
| Focused inventory tests | Passed, eleven twice | Includes stale version/date, missing/duplicate/unknown rows, broken reciprocal links and false authority mutations |
| Local loopback HTTP/SQLite smoke | Passed | Login, scoped list, responsive app and safe blocked transition; no billable inference |
| JSON/relative links/diff | Passed | Three JSON documents, three gate-section links; prohibited paths unchanged |
| Docker | Unavailable | Permission denied at daemon socket; CI owns image execution |
| Real AI, SQL Server and Azure deployment | Not run | No delivered app/runtime change; local smoke is not application acceptance |

## Findings and routes

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Owner ratification and historical reconciliation remain open

* Evidence: inventory `status`, `open_items`, manifest `owner_review: pending`;
  issue #166's owner comment and the plan's unchecked human acceptance.
* Impact: this PR cannot close #166 or authorize partial-row consuming builds.
* Destination: distinct owner review follow-up; if changed decisions affect
  scope, the next task starts with rpi-plan.
* Smallest next action: owner reviews v1.2.0 SN-01 through SN-13, confirms row
  owners, proposed volumes/scope and gap mapping, and supplies/reconciles the
  2026-10-14 handoff matrix or records an explicit disposition.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Full scenario-manifest evidence remains deferred to #103

* Evidence: scenario `status: partial-inventory-integration`, all eleven
  profiles/nine workflows deferred, no executed default/endpoint scripts.
* Impact: reciprocal link and engineering review do not pass full FR-035,
  AC-043 or prove repeated future iteration reviews.
* Destination: distinct #103 follow-up, rpi-research for current
  profile/workflow script and fixture evidence before planning.
* Smallest next action: inventory the current default IDs/order/selection,
  fixture versions, safe endpoints and same-home/building dependencies;
  retain honest unavailable/deferred statuses until checks execute.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Image and SQL Server verification depends on CI

* Evidence: Docker daemon permission denied; API 92 skips; changes ledger.
* Impact: no local container or SQL Server success may be claimed.
* Destination: distinct PR CI gate, not a source-code fix or new build.
* Smallest next action: inspect src/mvp/rubric checks after publication and
  leave merge to owner. A passing CI run still does not supply human approval
  or actual AI/Azure application acceptance.

## Defects, blockers and residual work

Implementation defects found: none. No local engineering publication blocker.
RV-001 and RV-002 are existing acceptance residuals, not newly expanded active
plan tasks. RV-003 requires CI evidence. No residual was silently accepted or
implemented, and no conformant full-issue outcome is asserted.

## Outcome and handoff

Review execution Complete; outcome Residual work. The engineering integration
is supported by the recorded evidence; #166 remains open. Parent proceeds
only with the already authorized commit/push/Refs #166 main PR, then records
publication state and offers/ranks these existing follow-ups without starting
a new task. This Review runs exactly once.

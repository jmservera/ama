---
title: Source change monitoring acceptance review
description: One post-implementation review of the bounded offline issue 213 slice
ms.date: 2026-10-16
---

## Scope and Evidence

Task: 213 / source-change-monitoring. One Review; no second review planned.
Assessed boundary: offline executable source changes under src/, supporting
READMEs/index/append-only log and RPI evidence. Full issue operational
acceptance is explicitly outside this delivery claim.

* Research: .copilot-tracking/research/2026-10-16/source-change-monitoring-research.md
* Plan: .copilot-tracking/plans/2026-10-16/source-change-monitoring-plan.md
* Details: .copilot-tracking/details/2026-10-16/source-change-monitoring-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-16/source-change-monitoring-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/source-change-monitoring-changes.md
* Acceptance audit: src/core/README.md, Source change monitoring and review
* Implementation: src/core/src/zava_forward/core/source_monitor.py,
  rulecards.py, rule_engine.py; src/orchestrator/src/zava_forward/orchestrator/source_monitor.py
* Evidence: core monitoring/lifecycle/engine tests, orchestrator tests,
  targeted API law/rule tests and project static checks.

## Opening Review State

Goal: compare implementation with all six issue criteria, explicit offline
constraints, critique dispositions and named-human legal boundary. Evidence
is available. Source changes stop before publication, not before simulated
review/regression/release. No missing actual human approval is labelled
completed. P01/P02 and P03-T01 complete; P03-T02 publication remains the
authorized handoff. Review creates this record only.

## Execution Status

Execution: Complete. Outcome: Residual work.
Reviewed the complete supplied bounded implementation and acceptance audit,
not a live official source, Azure deployment or legal interpretation.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Four append-only monitoring tables; immutable candidate blobs; real baseline hash/version; capped diff and explicit impact; linked existing reviews | Reconciled; discovery does not change current law retrieval or cards |
| P01-T02 | Local-JSON orchestrator page, source cadence, next_after, recorded failures/nonzero CLI | Reconciled; hosted schedule and network adapters are not claimed |
| P02-T01 | Named exercise owner; separate card approval; immutable source review/test plan; exact latest result/date/eligibility gates; atomic release/rollback | Reconciled within single-source changed-card boundary; overlaps fail closed |
| P02-T02 | 26 core and four job tests, updated existing future-activation engine assertion, retained local regression suites | Reconciled; tests stay outside packages; no network fixture tests |
| P03-T01 | Project Ruff/format/mypy, full core/orchestrator suites, targeted API regressions, README audit/index/append-only log | Reconciled; SQL Server opt-in tests remain skipped, no Azure claim |
| P03-T02 | This Review is complete; commit/push/PR are publication actions after review | Publication remains pending at this review boundary |

## Critique and Implementation-Time Update Assessment

* PC-001: activate and release consult the monitoring guard, including new
  cards and alternate versions; no-change review can release an exact held
  card after regression. Replacement cannot supersede a hold.
* PC-002: approval binds candidate/config/baseline, exact card histories,
  fixture plan/digest, evaluator version and clock. New material observations
  invalidate approval even after reversion; latest failed runs block release.
  SQL adapter serializes writers with the existing exclusive application lock.
* PC-003: extracted one shared citation eligibility function. Missing,
  historical, partial, unreviewed or noncurrent citations cannot pass release;
  positive fixtures run through RuleEngine on actual local SQL facts.
* PC-004: rollback compares complete activation histories and restores only
  captured eligible prior active versions, or the captured no-change hold.
  Intervening human decisions, repeated rollback and expired prior cards fail.
  Multi-card injected failures roll back all events.
* PC-005: exact canonical source matching, historical/current card histories,
  candidate/config binding, explicit unmapped impact. Newly citing card IDs
  require refreshed observation/review. Cross-source overlaps fail closed.
* PC-006: rejected with justification. The critique's asserted temporary-path
  ban was not in the caller's constraints and contradicted /tmp/zf164.
* PC-007: simulated labels persist in approval, regression, activation,
  rollback and existing linked assessment records. Fixture source content
  explicitly disclaims law/real approval.

These are in-scope refinements, not new legal decisions or new approvers.
No repeat critique or Review is required or claimed.

## Acceptance Assessment

| Issue criterion | Assessed result |
| --- | --- |
| Differences and affected cards/journeys/tests/communications | Met for bounded declared inventory, with exact histories/differences and explicit unknowns; exhaustive live impact analysis remains unmet |
| Unverified scraping/discovery pending provenance/completeness | Met for local inputs and simulated owner review evidence; actual official currentness and human review remain unassessed |
| Detection never overwrites approved cards | Met locally; current law index/source retrieval and card history are unchanged by discovery |
| Approval, regression, effective-date activation and rollback | Met for simulated single-source executable existing-source cards; coordinated sources and verified new-source publication remain unmet; no legal activation claim |
| Per-source configurable cadence | Met locally, with explicit due boundaries and bounded pages; hosted timer/adapter/missing-run alert remain unmet |
| High/Medium/Low likelihood per register | Met as exact enum and retained source-specific register rationale; no automatic policy synchronization or human ratification claim |

## Findings and Routing

No material implementation defect is established within the explicitly
bounded local slice. These residual requirements remain distinct follow-up
work, not completed acceptance.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Coordinated multi-source releases are unavailable

* Evidence: SourceMonitor.activate refuses overlapping changed sources.
* Impact: a card citing two changed sources cannot be released by this slice.
  It fails closed instead of letting one source's review approve another.
* Destination: distinct follow-up, beginning in rpi-plan.
* Next action: design one owner-reviewed multi-source evidence bundle and
  atomic activation/rollback without weakening existing holds.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: New-source publication and actual human approval remain unmet

* Evidence: monitor candidates never enter reg_version/provision/index;
  approvals use the named exercise owner and are explicitly simulated.
* Impact: local rule releases prove lifecycle controls against reviewed
  synthetic baseline provisions, not activation of new law or real approval.
* Destination: distinct follow-up, beginning in rpi-plan with the named owner.
* Next action: define verified source publication, approval evidence and
  source rollback semantics before operational reliance.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Live monitoring, operational suites and communications are not delivered

* Evidence: local observation JSON is the only job input; test IDs bind
  deterministic fixture cases, not arbitrary Python-suite execution.
* Impact: no actual official retrieval, hosted cadence/missing-run alert,
  operational privacy/accessibility regression or notification is proved.
* Destination: distinct follow-up, beginning in rpi-plan.
* Next action: authorize official adapters and hosting, complete the impact
  inventory with the owner, then design operational tests and communication
  approval/delivery. Do not activate a legal control from discovery output.

## Validation Evidence

* Core final full local suite: 463 run, 1 opt-in skip, including the final
  overlap-boundary test. Latest monitoring suite: 26 passed. Core project
  Ruff, format and mypy (89 files) passed after the final executable batch.
* Orchestrator full local suite: 21 passed, including multiple-source paging
  and CLI failure persistence. Project Ruff, format and mypy (10 files) passed.
* API law-store suite: 34 run, 16 opt-in SQL Server skips; rule suite: 5
  passed. Skips are not live verification.
* State JSON, README file-link targets and Git whitespace check passed.
* No live scraper, network fixture test, private dataset, protected file,
  Azure deployment, real human/legal approval or new endpoint.

## Outcome and Handoff

Execution Complete; outcome Residual work, not full issue acceptance.
The bounded local slice is review-ready for PR publication with its honest
acceptance audit. RV-001/002/003 route to later distinct tasks. No new
implementation is authorized by this review, and no second Review is planned.
Publication of P03-T02 is pending the authorized commit, normal push and
Refs #213 pull request. Merge remains with the owner.

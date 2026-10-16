---
title: Source change monitoring plan
description: Issue 213 bounded implementation plan
ms.date: 2026-10-16
---

Task: 213 / source-change-monitoring. Full-plan scope.

## Executive Summary

Extend the shared law/rule stores with append-only offline observations,
source-specific cadence and owner-reviewed changes. Keep discovery outside
the provision index. Bind deterministic local regression cases to immutable
replacement cards before effective-date activation and owner rollback.
Add an orchestrator job accepting only local fixture inputs; no live scraper,
HTTP endpoint, deployment or legal acceptance is claimed.

## User Decisions and Requirements

* Implement #213 in src/ on merged #210/#211/#212, extending delivered #127.
* Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
  No new approvals or real legal interpretation are invented.
* Discovery is unverified until provenance and completeness review.
* Retain approved cards, source versions and effective dates; regression
  before activation, effective-date gating and rollback are required.
* Cadence is configurable per source; likelihood is High/Medium/Low.
* Use local fixtures, portable SQL, tests outside packages and no core workload
  imports. Use /tmp/zf164, pip, absolute project PYTHONPATH, ruff and mypy.
* Update READMEs and append knowledge log, produce RPI evidence, push and PR.
  Use Refs #213, not issue-closing syntax. No force push or protected files.

## Goals

Prove safe candidate detection, retained impact/owner review and a reproducible
exercise rule-release sequence without implying law or operational approval.

## Scope and Non-Goals

Canonical executable targets: core/source_monitor.py, core/rulecards.py and
orchestrator/source_monitor.py. Tests: core/tests/test_source_monitor.py,
orchestrator/tests/test_source_monitor.py and existing rule-card tests.
Generated targets: none. Removals: none. Maximum new test methods: 30.
No new API endpoints, network retrieval, source publication, hosted timer,
resident messaging or real approvals.

## Functional Requirements

* Persist source configuration revisions, observations, differences and
  lifecycle events through existing SQL adapters and snapshot store.
* Review items include source versions/hash/provenance, difference categories,
  affected card versions, requirements, journeys, tests and communications.
  Explicitly label unmapped impact and do not imply impact completeness.
* Reuse per-card source reviews, extend their impact shape, and require owner
  assessments before a release plan can be approved.
* Approval requires reviewed provenance and complete content, exact approved
  target cards, full impacted-card coverage, effective date and regression
  fixtures covering every configured test ID.
* Run fixtures through the existing deterministic evaluator after approval;
  persist pass/fail evidence and block activation on any failed/missing test.
* Gate existing direct activation for monitored target cards too. Activation
  and rollback are atomic owner-only operations, never scheduled agent actions.
* Rollback restores exact captured prior active cards, not held cards or a
  silently different active version; preserve every event and require reason.

## Non-Functional Requirements

Append-only tables with SQLite triggers and SQL Server ledger/trigger support.
Parameterised portable DML; no SQLite replacement/ignore/pragma/autoincrement.
Trusted in-process identity boundary only, matching existing rule store.
New modules are typed; narrowly permit calls to migrated untyped interfaces.
Durable errors and failure observations; no success-shaped missing retrievals.

## Acceptance Criteria

Audit all six issue criteria individually in README/review/PR. Locally met
criteria are distinct from unmet live retrieval, complete impact inventory,
verified source promotion and human/production acceptance.

## Phase Checklist

* [x] P01 Persistence and detection
* [x] P02 Controlled release
* [ ] P03 Validation and publication handoff

<!-- rpi:phase id=P01 -->
### P01 Persistence and detection

* [x] P01-T01 Add typed monitor, portable append-only configuration,
  observations and candidates; extend existing review impact.
* [x] P01-T02 Add bounded local-fixture orchestrator and cadence tests.

<!-- rpi:phase id=P02 -->
### P02 Controlled release

* [x] P02-T01 Add owner assessment, regression plans/results, effective
  activation gate and exact atomic rollback.
* [x] P02-T02 Cover negative authority/provenance/test/date paths, restart,
  atomic failure, candidate isolation and adapter SQL contracts.

<!-- rpi:phase id=P03 -->
### P03 Validation and handoff

* [x] P03-T01 Run affected project local suites, ruff and mypy;
  update READMEs, index and append log with honest acceptance audit.
* [ ] P03-T02 Reconcile RPI evidence, run one implementation Review,
  commit, push and open Refs #213 PR.

## Dependencies

P02 depends on P01. P03 depends on P02. Existing changes #210/#211/#212
are present in HEAD even where issue checkboxes remain open.

## Critique Disposition

Executed once, verdict Revise. PC-001 through PC-005 and PC-007 accepted
as direct planner corrections: gate activate/release by affected card,
bind immutable approval/results to candidate/config/baseline/card lifecycle,
require runtime citation eligibility, compare exact lifecycle heads on rollback,
exact-match source IDs and preserve simulated labels everywhere.
PC-006 rejected: its claimed temporary-directory prohibition is not present
in the caller's constraints and conflicts with the explicit /tmp/zf164 request.
No user decision or second critique is required.

## Follow-Up Items

Live official adapters, hosted job, verified source publication,
coordinated multi-source release, staff/communication UX and human
legal/platform acceptance are outside this offline slice. Overlapping changed
sources fail closed rather than accepting one source's approval for another.
These must not be reported as delivered.

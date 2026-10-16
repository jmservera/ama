---
title: RPI Plan - Rule engine gating regressions
description: Bounded plan for issue 329
ms.date: 2026-10-16
---

## Task Metadata

* Task ID: 329
* Task slug: rule-engine-gating-329
* Planning status: Complete; implemented, reviewed and published as PR 334
* Plan date: 2026-10-16
* Phase details: .copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-16/rule-engine-gating-329-plan-critique.md

## Executive Summary

Pin exact consultation/historical applicability labels and the shared-home
24-hour attention publication limit across distinct cases and clock episodes.
Change production code only if the new tests demonstrate a real defect.
Publish the regression evidence and a references-only PR on the existing clean
test/rule-engine-gating-329 topic branch.

### What You May Not Know

Existing source tests accept either unknown or not applicable, so incorrect
labelling passes. Existing attention tests mostly replay one episode, where
episode deduplication masks a missing cross-episode throttle.

## User Decisions and Requirements

* Implement issue 329, including consultation/historical gating and cross-episode attempts.
* Fix any real defect exposed; demonstrate rejected mutations.
* Code only in src/, tests outside packages, portable SQL, no private data or protected configuration reads/edits.
* Use pip venv unit suites, ruff and mypy; no uv, Docker or Azure.
* Update relevant README, append reference log, produce RPI artifacts, push and open a PR.
* PR body uses Refs #329 only, without issue-closing keywords.
* Authenticate before commit; privacy-safe author/committer email 8036360+jmservera@users.noreply.github.com and required Copilot trailer.

## Goals

* Guard exact applicability semantics and home-scoped alert fatigue behavior.
* Retain checks and immediate breach escalation while throttling only attention publication.

## Scope and Non-Goals

* In scope: src/core/tests/test_rule_engine.py, a demonstrated defect in
  src/core/src/zava_forward/core/rule_engine.py if any, core README, reference
  log and routing index, task artifacts.
* Non-goals: source retrieval, legal interpretation, operational approval,
  deployment, private data, unrelated rule-engine refactoring.

## Functional Requirements

* Eligible cards citing consultation/historical/future provisions return exactly
  not applicable, retain source metadata and publish no alert.
* Incomplete/unreviewed/superseded/missing sources return unknown.
* Same home/card/step/item attention publications across cases or changed due
  times are suppressed before 24 elapsed hours and allowed at the exact boundary.
* Every attempted evaluation remains persisted; breach escalation bypasses
  attention throttling. Different throttle dimensions remain independent.

## Non-Functional Requirements

* Deterministic UTC fixtures, installed packages, no network in test cases.
* Production behavior unchanged unless a red regression proves a defect.
* Full core unit suite, ruff check/format and mypy pass in a pip venv.

## Acceptance Criteria

* Independent gating mutations and disabling cross-episode throttling each
  fail the specific intended regression, not an unrelated error.
* Distinct episodes and persisted publication counts are asserted, including
  just-before and exact 24-hour boundaries.
* README/log accurately distinguish local synthetic evidence from acceptance.
* One critique and one post-implementation review recorded; branch pushed and PR open.

## Sources

* Issue 329 (body and empty comments), read first with gh.
* src/core/src/zava_forward/core/rule_engine.py: citation eligibility, shared
  throttle and separate episode keys.
* src/core/tests/test_rule_engine.py: constructed SQL fixtures and coverage gaps.
* src/core/README.md: deterministic-checks-and-alerts-212 contract.
* docs/adrs/0006-src-layout-and-cutover.md: installed src packages and external tests.
* docs/case_study_48_original.md, docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md: project boundaries.

Research disposition: reused. Planning Readiness: Ready. No unresolved product
decision or additional external/legal research is needed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Pin behavior and publish verified evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused regressions and repair a demonstrated defect

* Tighten source results and add distinct-case/episode attention tests, boundary
  checks, throttle-key isolation and cross-case breach bypass.
* Dependencies: installed core/dev tools and one completed critique.
* Complete: one tightened method and three new methods; original production
  code passes all regressions. No defect or production edit required.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate, document and deliver

* Run targeted tests, full core suite, ruff/format/mypy and in-memory mutation
  checks, preserving the working implementation after every mutation.
* Update docs, record changes and one review, then commit/push/open PR.
* Dependency: P01-T01.
* Local implementation/validation/docs complete; one Review completed,
  Conformant, no findings. Core 466 tests, one explicit Azure opt-in skip;
  targeted 20 pass; ruff check/format/mypy pass; nine assertion-failing mutations.
* Published https://github.com/jmservera/ama/pull/334, OPEN to main on the
  existing topic branch. Verified empty closingIssuesReferences; hosted checks
  queued/running. Initial implementation commit f5b297b.

## Test Ownership and Validation Lock

* Canonical test owner: src/core/tests/test_rule_engine.py.
* Removals: none; tighten the existing combined source-gating test.
* Maximum additions: six focused test methods plus a small fixture extension
  only if necessary to test independent card identity.
* No generated test files or package-level tests. Semantic tests use the real
  temporary SQLite stores and simulated approvals; mutations are regression
  sensitivity evidence, not operational acceptance.
* Test the original implementation first. If it already satisfies the
  contract, retain production code unchanged and demonstrate failures with
  deliberately removed guards instead of inventing a fix.

## Critique Disposition

* One final-candidate critique executed, verdict Pass, no findings. Evidence:
  .copilot-tracking/reviews/plans/2026-10-16/rule-engine-gating-329-plan-critique.md.

## Follow-Up Items

* None.

## Handoff

* Implementation evidence: .copilot-tracking/changes/2026-10-16/rule-engine-gating-329-changes.md
* All implementation and delivery tasks complete; one Review Conformant.
* No blockers. Await hosted checks and owner's review/merge decision on PR 334.

---
title: Resident decisions implementation plan
description: Issue 86 bounded implementation and evidence gates
ms.date: 2026-10-15
---

Task: issue-86 / resident-decisions-86. Status: Implementation locally validated,
single Review complete, PR #319 published; newer-main integration/CI blocked.

## Executive Summary

Extend migrated core resident workflows and existing API/UI to bind supplied
human decisions to exact home/measure/scope/design, enforce representative
authority and stop dependent discretionary release. Preserve sibling choices
and independent hazard/complaint intake. No live acceptance claim.

## User Decisions and Requirements

* Full research, plan, implement, review loop and committed artifacts.
* Work only in the named worktree/branch; code and tests only in src.
* ADR 0006 and merged #296-302 govern placement and dependencies.
* Consent and withdrawal are human decisions, never model inference.
* Reuse enabled AI proposal pathways and approval gates; no private data.
* Portable SQL, pip only, no deployment beyond Azure, no .env/.vscode edits.
* Validate locally, document commands/results, push and PR to main with Refs #86.
* Do not tick unsupported owner/live-evidence criteria.

## Goals

Current scoped answers and task-limited authority govern release/disclosure.
Pause/withdrawal affects only its measure while dependent readiness requires
human review. Independent review and complaints remain available.

## Scope and Non-Goals

Existing resident mixin, store gate/draft, procurement guard, SQL dependency
validation, role projection, API resident endpoint and web forms. No new
database schema, AI task, real service transport, legal or retention policy.

## Functional Requirements

* Register explicit scope and positive design version per measure with source.
* Record supplied source/answer with authenticated actor, append-only versions.
* Version multiple representative references with tasks, measure/scope/design,
  evidence/date/review, resident wishes and safe-contact binding. Missing,
  expired, disputed, unclear or changed-contact authority denies disclosure and
  works decisions; scheduling/interpreting alone never authorizes consent.
* Readiness derived from latest exact-scope answer; changed scope/design is
  unknown. Paused/withdrawn creates a measure review flag, not a sibling rewrite.
* Release guards cover advance, issue/reissue/correction, booking/completion.
  Transactional dependent validation rechecks those guards for SQL-backed writes.
* Disclosure-check returns a minimal authorization result, sends nothing.
  Legacy representative-addressed templates are refused pending checked route.
* Add independent review as a distinct service type with a distinct redress
  owner; complaints/reviews remain reachable after pause/closure/AI failure.
* Restrict authority/source/wishes fields to resident-workflow roles and omit
  from AI input; preserve existing contractor minimum projections.

## Non-Functional Requirements

No workload import from core, no new SQL dialect, no driver/image dependency
change, rejected input must not mutate case/audit. Persist existing case bodies.

## Acceptance Criteria

* [x] A1: New scopes start Not recorded; contact, legacy case answer and AI do
  not produce a scoped decision; version/source/sibling isolation tested.
* [x] A2: Representative negative controls and disclosure fail closed.
* [x] A3: Measure pause/withdrawal flags human review and blocks dependent
  release without changing unrelated choices, hazard intake or complaints.
* [ ] A4: Independent review and complaint synthetic routes have distinct
  owners; actual formal route, without-detriment and human acceptance unproven.
* [x] A5: Local suites/ruff/mypy/app exercise recorded honestly; live
  AI/SQL Server/Azure and container evidence not assumed.

## Phase Checklist

<!-- P01 -->
### P01: Core semantics and guards
* [x] P01-T01: Extend resident context, authority, decision and service actions.
* [x] P01-T02: Wire release, disclosure, privacy and SQL dependency guards.
<!-- P02 -->
### P02: API/UI and regression evidence
* [x] P02-T01: Wire explicit non-prefilled forms and existing resident endpoint.
* [x] P02-T02: Add core/API semantic tests and adapt only affected fixtures.
<!-- P03 -->
### P03: Validation and delivery
* [x] P03-T01: Run project suites, ruff, mypy, synthetic local app and Docker probe.
* [x] P03-T02: Update component guides, reference index/log; one review and PR.

P03-T02 documentation, single Review and PR publication are complete. PR #319
has four conflicts with newer main; no hosted checks have run and no merge/
rebase is authorized. Owner-authorized base integration is a distinct delivery
follow-up, not a second Review in this task. A1-A3 and A5 are bounded local
exercise evidence only. A4 and the full issue's operational/human acceptance
remain open; the PR must use Refs #86.

## Locked Test Ownership and Evidence

Core semantics: src/core/tests/test_resident_decisions.py. API app exercise:
src/api/tests/test_resident_api.py. Existing affected fixture/test files may be
adapted to explicit synthetic scopes without weakening prior assertions.
Exact removals: none. Maximum new test modules: two. No generated product
targets. Semantic tests cover exact authority/expiry/source/readiness; existing
project suites provide regression coverage. Run all five project suites and
configured ruff/mypy; API loopback test is a real local app with synthetic data,
not live inference or actual resident evidence. Probe Docker; defer denied build
and real platform evidence to CI/authorized future work.

## Critique Disposition

Executed once; verdict Revise, six compatible findings applied directly:

* PC-001: Work-order versions bind explicit measure/context IDs. Case advance
  covers all measures; work-order release covers only its explicit bindings.
  Missing bindings block release. Reissue/correction requires new explicit
  bindings; ordinary booking/completion uses the saved version. New acceptance
  records explicit review evidence to resolve a prior pause review.
* PC-002: A registered context has a monotonic revision and must match the
  current technical design counter. No technical design means unknown and
  blocks registration. Any global technical design change invalidates all
  resident contexts conservatively; history never reactivates by switching back.
* PC-003: Recheck the exact latest authority version at use time (not any
  representative). Evidence dates cannot be future, review must be later than
  evidence and strictly later than today; review date itself is expired.
  Superseded/disputed/unclear/revoked authority and contact changes hold release.
* PC-004: All resident projections are detached. Authority records and supplied
  narratives are restricted to both resident-workflow and recorded-need roles
  (default RLO and Programme Manager). Other staff receive coded status/context
  and owned confirmation tasks only, contractors existing minimum. Audit stores
  event/context IDs, not narratives. Operational matrix/retention unapproved.
* PC-005: Decouple AI staff proposals from addressed template construction;
  use non-addressed fallback for summaries/messages, retaining existing model
  adapter/release/review semantics. Addressed representative templates refuse.
* PC-006: Independent review binds the contested recorded actor and reference.
  Reviewer cannot be that actor or service handler; only that named reviewer
  updates/closes the independent review. Neither complaints nor reviews mutate
  works, priority, hazards or resident choices.

No significant/divergent user decision required; no repeated critique.

## Follow-Up Items

Owner-authorized integration of newer-main #315/#316 is required for PR #319:
four files conflict and hosted CI has not run. No silent merge/rebase/force push.
Formal complaints integration, representative retention/role ratification,
real user independent-review/without-detriment testing and authorized live
Foundry/SQL Server/Azure evidence are not local implementation acceptance.

## Handoff

Research: .copilot-tracking/research/2026-10-15/resident-decisions-86-research.md.
Details: .copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md.

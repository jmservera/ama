---
title: Hazard referral and retrofit hold plan
description: Bounded issue 85 delivery plan
ms.date: 2026-10-15
---

Task ID: 85. Slug: src-hazard-referral-85.

## Executive Summary

Extend merged core workflows and API/UI to distinguish a reported observation,
referral sent, separately evidenced receipt and acceptance, external repair
evidence and independent release of a home-scoped retrofit hold. Never own the
hazard service's classification, legal clocks, resident contact or closure.
Engineering delivery does not establish live service or full issue acceptance.

## User Decisions and Requirements

* Full automatic RPI loop and tracked research, plan, changes and review in PR.
* Work only in the supplied worktree/branch, new code/tests in src per ADR 0006.
* Reuse building and handoff delivery; preserve dependency and identity rules.
* AI stays available under existing release/human gates; no AI prerequisite for
  urgent referral, no private data, no nonportable SQL, Azure-only deployment.
* Run local project suites, ruff, mypy and synthetic app first; pip only.
* Do not invent owner decisions or live evidence. PR uses Refs #85, no merge.
* Update reference index/log. Never touch excluded owner paths.

## Sources

Research: `.copilot-tracking/research/2026-10-15/src-hazard-referral-85-research.md`,
evidence C1-C7 and W1-W2. Issue has no comments as retrieved.

## Goals

Make hazard referral accountability and the distinct retrofit restriction
auditable, durable and visible without expanding authority.

## Scope and Non-Goals

Core workflow, case projection, staff HTTP actions, existing safety panel,
JSON/SQLite semantic and HTTP tests, component READMEs and reference routing.
No new service, transport, legal deadlines, building register editor, model
capability, deployment, production activation or operational acceptance.
Hold scope is explicitly the linked home/case, not a building-wide release.

## Functional Requirements

* Capture immutable source/awareness and authenticated reporter on new reports.
* Treat existing category/urgency only as unverified report observations.
* Link sent evidence to destination and external case; keep sender follow-up
  until designated safety receiver separately records receipt and acceptance.
* Record externally supplied response/update due and actual times with evidence;
  missing timings remain unknown. Never calculate statutory deadlines.
* Require external repair evidence and independent safety-role hold-release
  reason; release only the retrofit hold. Preserve consent and other blockers.
* Record immutable versioned snapshots and ledger events. No replay or invalid
  actor/index may mutate state. Legacy history must not be fabricated.

## Non-Functional Requirements

No SQL additions; use existing JSON case-body persistence on all stores.
Preserve field minimisation and contractor default deny. No workload imports
in core, no SQL/blob changes to agents image. Existing AI human gates remain.

## Acceptance Criteria

* [x] Local tests show create/link-only semantics, no hazard closure or clocks.
* [x] Sent, receipt and acceptance have distinct actor/time/evidence snapshots.
* [x] Home hold scope, accountable role and independent release are durable.
* [x] External response/resident-update times and unknowns are visible.
* [x] Local suites, ruff/mypy and loopback synthetic application results recorded.
* [ ] Full issue acceptance remains unchecked without owner/live evidence.

## Phase Checklist

<!-- P01 -->
### P01 Core accountability

* [x] P01-T01 Extend existing workflows, detail and note projection, strict indexes,
  legacy read compatibility and JSON/SQLite semantic tests.

<!-- P02 -->
### P02 Staff surfaces

* [x] P02-T01 Wire API actions and safety panel; test roles, replays, evidence,
  persisted timings, independent hold release and uninterrupted referral.

<!-- P03 -->
### P03 Evidence and delivery

* [x] P03-T01 Update related docs, run project checks and synthetic local app,
  record commands/results and unresolved acceptance.
* [ ] P03-T02 Run one post-implementation RPI review; commit/push and open PR.

## Locked Test and Target Contract

Canonical source: existing core workflows/store/projection and API server/web.
No generated production targets or removals. Maximum two new test modules:
`src/core/tests/test_hazard_referral.py` (semantic, JSON/SQLite) and
`src/api/tests/test_hazard_api.py` (HTTP/local synthetic app).
Update directly coupled legacy workflow/UI tests and endpoint inventory;
retain existing building, consent and dependency-rule regressions.
No new broad lint exemptions; only permit typed tests to call migrated
untyped interfaces using the established narrowly scoped mypy override.
Every executed command/result is recorded in the changes artifact and PR.

## Critique Disposition

Single critique executed Complete, verdict Revise. All compatible corrections
applied directly; no new owner decision and no second critique:

* PC-001: explicitly allow raise/refer on closed records without changing
  completion, stage, consent or ownership, including reachable UI and tests.
* PC-002: active legacy raised/referred/repaired holds use a prospective
  re-referral/binding step with new sent evidence, preserving legacy history.
  Never infer receiver/receipt/acceptance from display names or dates; repaired
  legacy holds need fresh external repair evidence after new acceptance.
  Already released holds remain released and cannot be re-referred.
* PC-003: update shared gate/status and newly emitted emergency audit wording
  to hold-only/manual-referral language, no same-day policy promise; preserve
  historical ledger entries unchanged.

## Follow-Up Items

Owner-approved timing/escalation policy; verified external transport/service
receipt; real permitted model task, SQL Server durability, Azure run and human
acceptance. Do not implement or mark these complete without evidence.

## Handoff

Phase details: `.copilot-tracking/details/2026-10-15/src-hazard-referral-85-phase-details.md`.
Planned changes record: `.copilot-tracking/changes/2026-10-15/src-hazard-referral-85-changes.md`.
Readiness: Ready for bounded engineering after direct critique dispositions.
Implementation P01/P02/P03-T01 complete; one Review assesses the source/docs/
test boundary before P03-T02 delivery bookkeeping. Full issue acceptance and
owner/live platform follow-ups remain explicitly open.

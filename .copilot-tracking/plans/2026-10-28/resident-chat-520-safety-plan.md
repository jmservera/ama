---
title: Resident chat safety routing correction plan
description: Bounded correction for PR 525 thread PRRT_kwDOUU8JX86xVvlj
ms.date: 2026-10-28
---

Task ID: 520-safety. Status: Original Review complete; local commit pending; publication blocked.

## Executive Summary

Extended the existing host-owned safety-first route with bounded report/context
combinations and ordered smoke-report phrases. SAFETY unchanged; 47 positive
reports and 30 ordinary negative questions covered through routing and HTTP.
API discovery, focused units, Ruff100/format/mypy and actual browser checks pass.
Commit correction and original dated RPI evidence locally; required full
publication gate invokes prohibited az, so do not push or resolve remotely without
that evidence. No new advice, model authority, operational report or UI change.

## Sources

Research: .copilot-tracking/research/2026-10-28/resident-chat-520-safety-research.md,
C1-C7, disposition executed, Planning Readiness Ready.
State: .copilot-tracking/rpi-sessions/2026-10-28/resident-chat-520-safety-state.json.
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-safety-phase-details.md.

## User Decisions and Requirements

* Correct the named open thread on PR #525, branch feat/resident-chat-520.
* Recognize both quoted hazards and plausible CO, smoke/fire, gas, electrical
  and flooding-with-electrics reports before ordinary topics.
* Preserve ordinary questions and the existing safety response verbatim.
* Run relevant API units and affected browser check; Ruff limit 100.
* Acquire heavy lock with flock -n, retry at most 40 minutes, never indefinitely.
* No az/Azure, secrets, .env, private data, force push or merge.
* Commit RPI artifacts with Conventional Commit and required Copilot trailer;
  leave a local commit if publication is blocked by the az-dependent full gate.
* Keep PR text Refs #520, never a closing keyword.

## Goals

Prevent home-record answers for recognized hazard reports without expanding
assistant authority or changing ordinary record questions.

## Scope and Non-Goals

Canonical source: src/api/src/zava_forward/api/resident_demo/chat.py.
Tests: src/api/tests/test_resident_chat_api.py and the existing
src/api/checks/resident_assistant_browser_check.py.
Documentation: directly related src/api/README.md routing description.
Non-goals: UI/assets, request schema, model, records, SQL, infrastructure, new
legal or safety advice, broader matching of all questions containing alarm/water.

## Functional Requirements

FR1: existing safety tokens and new bounded report/context checks run before
unknown/ordinary-topic checks.
FR2: normalize through existing whole-word lower-case tokenization, not substring
matching. Combine CO/carbon monoxide with active alarm/exposure cues; smoke with
observational cues; electrical terms with sparks/smoking/shocks/burning; flood or
leak/water with electrical context. Keep detector/document/status queries ordinary.
FR3: return the unchanged SAFETY text and sources, rules-only, no appointment
action and no model call for recognized reports.
FR4: preserve all existing ordinary routing branches in their current order.

## Non-Functional Requirements

Keep logic explicit and deterministic; no dependencies, configurable classifier,
model inference or unbounded regular expressions. Ruff line length 100 and
existing strict mypy. Tests use constructed residents and disposable local SQLite.

## Acceptance Criteria

AC1: both exact quoted reports return safety at route and HTTP layers, byte-equal
SAFETY answer, human source label, no own-home details, no appointment action.
AC2: table covers CO alarm/CO exposure, smoke, fire, gas smell, sparking/smoking
sockets, shocks, water/flooding near electrics, case/punctuation and topic priority.
AC3: ordinary detector documents/status, socket improvements, smoking-policy,
water questions, home/status/documents/forms/consent/appointments/rules and unknown
requests retain their existing routes and bounded answers.
AC4: relevant API tests and actual resident-assistant browser check pass, or
specific prerequisite failures are recorded without fabricating acceptance.
AC5: one independent critique with dispositions and one original independent
Review, preserving adverse outcomes and routing residuals to later tasks.
AC6: clean local Conventional Commit includes original dated evidence; full-gate
blocker prevents push/resolution; no prohibited command runs.

## Test Ownership and Change Budget

Retain all existing tests; removals: none. Add at most three test methods to
test_resident_chat_api.py: positive routing table, ordinary route table, HTTP
hazard/ordinary assertions (may combine the first two if clearer). Add both quoted
reports to the existing browser run, not a new harness. Test data tables supply
semantic positive/negative coverage, HTTP assertions prove request-path behavior,
and the existing browser exercises integration. No generated production targets.
Validation: failing reproduction first, focused units, package discovery,
Ruff100/format, mypy, browser with pinned axe when available, git diff --check.
No new full receipt claim. External evidence stays in this session's files/.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement safety-first matching and regressions

* [x] P01-T01: Add positive and ordinary-negative route/HTTP regressions; preserve failing baseline.
* [x] P01-T02: Implement bounded matching before ordinary topics; reuse SAFETY unchanged.
* [x] P01-T03: Add quoted reports to browser assertions and document routing boundary.

P01 complete: focused suite 33 tests passed; final package/browser validation in P02.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, independently review, and hand off

Depends on P01.

* [x] P02-T01: Acquire bounded nonblocking heavy lock and run relevant units/API/static/browser checks.
* [x] P02-T02: Reconcile changes/details and execute one independent original Review.
* [ ] P02-T03: Commit source and dated evidence with privacy-safe identity; verify clean exact head.
* [ ] P02-T04: Publish/reply/resolve only with mandatory full-gate evidence; otherwise retain local handoff.

P02-T01 evidence: 33 focused tests; API discovery 1182 tests, OK with 316 skips;
Ruff100; 51 files formatted; mypy 97 files; actual Chromium with pinned axe,
32 states, zero reported violations and seven color-contrast incomplete states.
No console errors or external browser requests. These are engineering checks,
not SQL/full-gate or accessibility/human acceptance.

P02-T02: exactly one independent original Review, execution Complete / outcome
Residual work. Bounded source correction conformant; no implementation defects.
RV-001 Medium: full-receipt/publication gap. RV-002 Low: retained contrast/human
acceptance. Findings routed to distinct later work, not a second Review or fix loop.

## Critique Disposition

Execution: Complete. Original verdict: Revise. Output:
.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-safety-critique.md.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001, HIGH, alternate shared lock/scratch | Rejected: conflicts with caller's explicit /tmp/ama-rpi-heavy.lock requirement. The worker cites a no-system-temp restriction not present in the parent execution contract. Do not substitute a different lock or weaken serialization. | User explicitly names /tmp/ama-rpi-heavy.lock; existing runner and README use that shared path. External task-owned evidence/scratch remains permitted. Original critique preserved unchanged. |

No unresolved significant decision or implementation blocker. Publication
blocker remains separately recorded. No second critique.

## Follow-Up Items

Mandatory exact-head full publication receipt needs separately authorized
az-dependent validation by the coordinator. Human/resident/assistive-technology
and hosted acceptance remain inherited gates, not this correction's acceptance.
The seven color-contrast incomplete states are retained for human assessment,
including the new hazard-response state; no conformance claim is made.

## Handoff

Implementation/local validation and original independent Review complete.
Only local commit and publication handoff remain; no source
implementation work is outstanding. Changes path:
.copilot-tracking/changes/2026-10-28/resident-chat-520-safety-changes.md.

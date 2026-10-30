---
title: Resident chat launcher 520 implementation plan
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 520
* Task slug: resident-chat-launcher-520
* Planning status: Ready; single critique dispositioned
* Phase details: .copilot-tracking/details/2026-10-30/resident-chat-launcher-520-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/resident-chat-launcher-520-plan-critique.md

## Executive Summary

Finish the existing resident chat's document-answer gap rather than build another
launcher. Admit ordinary complete questions about missing documents, providing
them and warning/error meanings. Typed document answers will retain all
host-owned own-case facts, source references and no-approval wording, with the
existing bounded optional AI guidance selector and truthful fallback.

### What You May Not Know

The other requested surfaces already exist. Typed document generation currently
can replace required document facts, although explicit topic requests cannot.
Only documents move to that fact-preserving path; other generated topics stay.
Live authenticated acceptance, operational consents/calendar history and human/AT
acceptance are not established by this synthetic local task.

## User Decisions and Requirements

* Deliver exactly issue #520, including the owner's document-answer criterion.
* Run research, plan, implement, review in order; retain dated original evidence.
* Use current feat/resident-chat-launcher-520 at a02984e8; local commit only.
* Source in src, tests outside packages, pip only, no Azure/deploy/sign-in/secrets.
* Preserve Fluent 2 foundations, WCAG baseline, plain wording, native controls,
  reduced motion, non-colour labels, consent, safety and manual routes.
* Run requested API discovery, Ruff check/format, mypy and real local browser/axe;
  heavy work uses flock -w 600 /tmp/ama-rpi-heavy.lock.
* Use Refs #520, privacy-safe author/committer and required Copilot trailer.

## Goals

* Answer resident document questions from available own-case metadata without
  granting document acceptance, uploading or model authority over facts.
* Preserve and freshly exercise all existing #520 behaviours.

## Scope and Non-Goals

Included: resident route grammar, document advisor dispatch, one discoverability
sentence, API regression/browser cases and directly related API README.
Excluded: new projection/SQL/schema, calendar integration, operational consent,
actual uploads, new model route, styling overhaul, deployment or live inference.

## Functional Requirements

* Recognise bounded complete document questions, including "What does my
  document warning or error mean?", upload/provide/send wording and "Which
  documents do I still need to provide?". Retain complete-match refusals.
* Typed document questions use the existing fixed-topic document advisor.
  Mandatory facts/citations remain unchanged with AI off, success or failure.
  No new arbitrary generated document prose is rendered.
* Preserve own-record authorization and consent-before-read/model, late
  revocation fencing, unknown states and all protected routes.

## Non-Functional Requirements

* No new dependencies, storage or network capabilities. UI text only; use
  existing native widget and Fluent-derived tokens.
* Browser check requires zero axe violations in its scoped scans; exercise
  mouse/touch/keyboard, 320/390/1280px, reduced motion and 200% root text resize.
  This is engineering evidence, not native zoom/human/AT acceptance.

## Acceptance Criteria

| Issue criterion | Required evidence |
| --- | --- |
| 1: Launcher on all resident pages, mouse/touch/keyboard/focus | Existing loopback resident check: signed-out, signed-in, loading/error |
| 2: Own record only | Real HTTP two-resident tests; browser identity switch; AI payload excludes other record |
| 3: Dated local regulatory citations, no legal conclusions | Existing API tests and local browser source/refusal checks |
| 4: Free slot proposals, explicit confirmation, cancel/manual | Existing real SQLite agenda tests and actual browser search/book/cancel |
| 5: AI-off label and AI suggestion boundary | API deterministic selector success/off/failure plus browser rules label |
| 6: Unit/automated accessibility, pending human/AT | Requested API gates, browser pinned axe; explicit pending acceptance |
| 7: Missing/provision/warning document answers | Ordinary complete questions, mandatory own-record facts/citations across AI states, no upload/approval; browser latest-reply assertions |

## Sources

Research: .copilot-tracking/research/2026-10-30/resident-chat-launcher-520-research.md
(C1-C7, W1). Issue #520 and comments retrieved using gh. No unresolved planning
dependency; tool availability is verified during execution.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and expose grounded document answers

Dependencies: completed Research and dispositioned critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend bounded wording and fact-preserving dispatch

Modify chat.py grammar and app.py document dispatch, retain all other topic
behaviour. Update assistant.js text with supported document question examples.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile regressions, browser cases and API guide

Depends on P01-T01. Expand current parameter cases and update the outdated
refusal test rather than create a parallel suite. Up to 2 new API test methods;
no test file additions, no test removals. Canonical coverage:
src/api/tests/test_resident_chat_api.py; generated targets: none.
Extend existing browser check, no new browser framework.
Semantic coverage: facts, dates, source refs, unknown, no approval/upload.
Regression coverage: full-message refusal, protected intents, cross-case data,
revocation, AI failure and unchanged non-document generation.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile implementation evidence

Dependencies: P01. Run focused regression then requested full API suite, Ruff,
format check, mypy and JS syntax; actual local browser/axe using constructed
fixtures. Keep raw logs/screenshots external and summarize results in changes.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run local gates and reconcile all plan markers

Use the user's exact PYTHONPATH. Verify the selected Python imports this
worktree, not another editable checkout. Never mutate a shared tool environment.
If missing packages block validation, install this worktree's distributions
with pip into a task-owned external venv. Heavy gates hold the shared lock.

## Dependencies

Pinned existing Python/dev packages, Chromium, pinned axe 4.10.3 and task-owned
synthetic fixtures/SQLite. Complete publication gate after local commit requires
its documented prerequisites and clean exact candidate.

## Critique Disposition

Single critique executed: Revise, one Medium PC-001 (scratch/lock feasibility).
Disposition: not applicable to parent environment. The critique worker reports
a worker-specific restriction on /tmp; no such restriction applies to this
parent, and the user explicitly requires /tmp/ama-rpi-heavy.lock. Preflight found
no lock holder; the parent successfully ran the pre-change 27-test suite with
the exact shared flock path and system python3 (20.032s). Keep scratch and output
task-owned/external, retain shared serialization, never inspect another gate's
output. Original critique preserved, no repeat critique. Its functional
assessment found the approach credible and all other planned coverage sufficient.

## Follow-Up Items

* Owner's live authenticated resident check and human/AT acceptance remain
  outside authorized local work. No screen-reader/voice acceptance claimed.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/resident-chat-launcher-520-changes.md.
P01/P02 complete: 61 focused tests; full API discovery 1380 tests, 320 skips;
Ruff check/format and mypy pass. Actual browser/axe passes its assertions,
32 scans with zero violations; incomplete axe checks remain explicit in changes.
Ready for one independent Review, with open findings routed to later work.
Commit original evidence locally, then attempt the complete local gate with the
reviewed main base. Do not push. Record prerequisite/base blockers honestly.

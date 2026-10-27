---
title: Resident content and journey implementation plan
description: Bounded documentation and copy changes for issues 153 and 154
ms.date: 2026-10-27
---

## Task Metadata

Task ID: issues-153-154. Slug: resident-content-153-154.
Planning status: Ready; one critique completed, direct corrections applied.
Details: .copilot-tracking/details/2026-10-27/resident-content-153-154-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-27/resident-content-153-154-plan-critique.md.

## Executive Summary

Extend the existing content audit with a concrete surface inventory, unresolved
error/wording gaps and a truthful acceptance matrix. Add six resident task
designs and a shared representative view contract to the existing resident
journey document. Correct a few literal labels without changing authority,
stored data, layouts or workflows.

### What You May Not Know

The owner appointed Juan Manuel Servera as wording reviewer on 2026-10-15;
the standard is stale about appointment. No completed wording review is
evidenced. Resident journeys remain unvalidated hypotheses even when existing
records and automated tests work. Both issues require `Refs`, not `Closes`.

## User Decisions and Requirements

* Deliver #153 and #154 together on the supplied branch in one PR to main.
* Run research, plan, implement and review in order; commit dated evidence.
* Documentation plus the smallest safe existing-web copy fixes only.
* Preserve Fluent 2, WCAG baseline, non-colour signals, reduced motion,
  optional AI/manual paths and human/resident decisions.
* Local tests only; no full gate, no Azure, secrets, private data or uv.
* Human wording/usability/AT acceptance remains an owner step; do not guess
  Legal/DPO/Compliance decisions.
* Commit Conventional Commits with required trailer and privacy-safe email;
  push without force and create one evidence-bearing PR.

## Goals

* Make audited coverage and residual risk explicit rather than certify universal copy.
* Turn resident research maps into reviewable task flows and text wireframes.

## Scope and Non-Goals

Included: content-standard.md, customer-journeys/residents.md, knowledge-base
index/log, literal copy in app.js, assistants.js, panels.js, timecapture.js and
focused tests outside the package. Excluded: portal, messaging, translations,
stored-value migrations, backend behavior, CSS/framework and governance policy.

## Functional Requirements

* Each resident task specifies trigger, information, choice/action, receipt,
  owner/next step, negative state and non-digital equivalent.
* Representative design limits fields/actions to current task, scope and
  dates, denies unclear/expired/revoked access, and separates interpreting,
  scheduling, information sharing and works decisions.
* Candidate messages preserve unknown, proposed, recorded and confirmed states.
* App draft and assistant acceptance copy explicitly disclaims decision approval.

## Non-Functional Requirements

* No changes to endpoints, identifiers, stored values, approval or consent checks.
* Native semantics, focus/status mechanisms, tokens and reduced-motion CSS unchanged.
* No fabricated human acceptance or service SLA/contact details.

## Acceptance Criteria

* AC1: Dated surface inventory includes source-owned and dynamic text; unresolved
  jargon and reason/owner/action gaps have exact references and follow-up owners.
* AC2: Six journey contracts cover choices, pause/withdrawal, appointments,
  updates, handover/aftercare and challenge/remedy, each with a non-digital route.
* AC3: Shared representative text wireframe and negative cases cover task
  authority, dates/revocation, several representatives and changed unsafe contact.
* AC4: Issue-by-issue criteria matrix distinguishes design evidence, local
  regression and Not run human validation; no overall closure claimed.
* AC5: Focused API units, JS syntax and existing relevant synthetic browser
  checks pass or have explicit blocked results; no full/scoped heavy gate
  planned because this is a small documentation/literal-copy change.

## Sources

Research: .copilot-tracking/research/2026-10-27/resident-content-153-154-research.md,
C1-C13/W1-W4; linked BRD/PRD requirement IDs and existing tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Document the bounded audit and journeys

Dependencies: completed Research.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend content audit and human review status

Inventory current core and supporting assets, distinguish raw server/evidence
copy and residuals, correct reviewer appointment without claiming review.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Specify resident and representative task designs

Extend residents.md in place with six flows/text wireframes, common
safe-contact/authority rules, non-digital alternatives and owner validation
scripts; update knowledge-base index and append log.

<!-- rpi:phase id=P02 -->
### [x] P02: Correct copy and verify engineering boundaries

Dependencies: P01 design/audit; fetched web guidelines.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Apply literal copy changes and regression coverage

Rename "Write to the resident" to a draft-only heading and add a no-send/
human-review disclaimer; clarify representative review date boundary;
rename technical "Invocation"; add assistant draft-only review disclaimer;
replace ordinary "hold the same role" wording.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run targeted local validation and reconcile evidence

Run API targeted content/design/accessibility units, existing relevant browser
checks and JS syntax. Reconcile plan/details/changes and preserve failures.

<!-- rpi:phase id=P03 -->
### [ ] P03: Independent Review and publication

Dependencies: implementation and validation complete.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run one independent Review and publish honest evidence

Refresh guidelines, independently review exact candidate once; retain outcome
and route findings, not another implementation/review loop. Commit/push one PR
using Refs for both issues, no full gate. Human approval remains incomplete.

## Test Ownership and Locked Boundary

Owner: API project. Removals: none. Maximum additions: four unittest methods
in existing test_content_standard.py; no new dependencies or test files.
Canonical targets: four named JS assets and existing UX documents.
Generated targets: none. Lexical guard extension covers timecapture.js; other
supporting files are manually inventoried, not claimed lexically clean.
Regression tests assert exact corrected literals, disclaimers and absence
of old copy. Semantic authority behavior is unchanged and remains owned by
existing resident/appointment/assistant tests, not inferred from string tests.
Validation from src/api:
`PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest
test_content_standard test_design_system test_accessibility_baseline
test_resident_api test_assistants -q`;
`python3 -m checks.design_system_browser_check` uses its owned fixture/server.
`node --check` on each changed JS file from the repository root.
Use a session-only Playwright callback with
`checks.design_system_browser_check.main(callback)` for four rendered copy
assertions below, without modifying browser-check sources or dependencies.
Set TMPDIR to the worktree's `.venv/ux153-tmp` before Python/Chromium starts.
Run Markdown/link review and git diff check. No --changed heavy run justified.

| Surface | Source regression | Rendered evidence |
| --- | --- | --- |
| Resident draft | Exact heading and no-send/human-review text | Actual owned synthetic case page |
| Representative date | Exact exclusive-boundary label | Actual owned synthetic case panel, expanded details |
| Assistant proposal | Exact label and review disclaimer | Actual assistantProposal renderer with constructed bounded proposal fixture, not authority acceptance |
| Time capture | Exact same-role sentence | Actual timeView renderer with constructed /api/time/status response, not enabling time capture |

Unavailable required local engineering checks block publication. Human wording,
usability and AT evidence intentionally remains Not run, not an engineering pass.
Publish only if the one independent Review accepts the unchanged reviewed
source boundary and required local checks pass. On Not accepted/Blocked Review
or required-check failure, preserve evidence and stop publication without a
silent repair/review loop. No later source correction may reuse acceptance.

## Critique Disposition

Execution: Complete. Original verdict: Revise; preserved unchanged.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Planner: applied directly | Explicit unchanged-boundary acceptance and required-check publication stop rule above and P03 details |
| PC-002 Medium | Planner: applied directly | Real unit/browser commands, worktree TMPDIR and four-surface source/render table above; P02 details |

No significant user decision or second critique is required.

## Follow-Up Items

* Universal server-message/error coverage: requires broader typed error and
  accountable-owner work; #153 remains partial.
* Actual wording review by appointed Juan Manuel Servera and #155 resident/
  representative usability/AT sessions remain Not run.
* OD-41/42 operational representative/privacy/service decisions remain with
  Resident Engagement, Legal and DPO; do not invent expiry/retention policy.

## Handoff

Details and critique paths above; implementation creates
.copilot-tracking/changes/2026-10-27/resident-content-153-154-changes.md.
Ready after critique disposition. Publication uses the owner's explicit
local-only validation exception, not the repository's full --all gate.

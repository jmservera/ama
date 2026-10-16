---
title: Issue 215 regulatory alert and chat UX plan
description: Synthetic implementation plan
ms.date: 2026-10-16
---

Task ID: 215. Slug: regulatory-alert-chat-ux. Full plan.

## Executive Summary

Present existing scoped deterministic alerts outside optional chat, give existing
roles short recognition guidance, and render regulatory answers as accessible
sections with unchanged source excerpts. Keep approvals and access unchanged.
Local engineering evidence is deliverable; real-staff comprehension is not.

## User Decisions and Requirements

* Implement #215 atop merged #328, #331 and #348; open PR with Refs #215 only.
* ADR 0005 accepted for synthetic development only on 2026-10-16.
* Juan Manuel Servera is exercise Legal, Compliance and DPO owner.
* Code only in src/; no private data, environment files, legacy trees or Azure.
* Automated and keyboard accessibility checks, ruff, mypy and local app required.
* Produce research, plan, changes, review; README and append-only KB log update.
* Real repairs/housing/grants comprehension stays unmet with a test protocol.

## Goals

Recognition and safe routing without legal interpretation; honest evidence.

## Scope and Non-Goals

Existing API web assets, tests/checks and related documentation only.
No new rights, rule activation, statutory calculations, provider or live sending.

## Functional Requirements

All seven audience patterns; noticed/source/status/action/owner/clock fields;
plain-language presentation without paraphrasing legal excerpts; explicit missing
source, doubt, disabled and outage states. Existing persisted doubt route reused.

## Non-Functional Requirements

Semantic headings, native keyboard controls, visible focus, text statuses,
polite status/errors, wrapped source text and 320px reflow. No conformance claim.
Server projection remains authoritative.

## Acceptance Criteria

Audit each issue criterion in README and PR, not the issue body. Role patterns,
alert shape and doubt/missing-source states must have local evidence. Accessibility
is partially evidenced by automated/keyboard checks, not certified. Staff trial
is Not run and unmet.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01 Presentation

* [x] P01-T01 Add role guidance and home alert panel using scoped GET endpoint.
* [x] P01-T02 Render structured chat, plain mode, dates, missing sources and doubt.

<!-- rpi:phase id=P02 -->
### P02 Evidence and delivery

* [x] P02-T01 Add browser regression/axe and keyboard tests using synthetic local app.
* [x] P02-T02 Run targeted regressions, ruff/mypy; document limits and staff protocol.
* [x] P02-T03 One post-implementation review, commit, push and open PR.

P01 and P02 complete for the declared synthetic engineering/delivery scope.
Published PR #354; full issue acceptance remains partial as audited.

<!-- rpi:phase id=P03 -->
### P03 Owner-requested independent review findings

Bounded continuation after independent CHANGES verdict on d79a737. Existing
critique remains historical; no additional critique or full UX Review.

* [x] P03-T01 Merge origin/main, keeping both append-only log histories.
* [x] P03-T02 Run the regulatory harness in src-api CI with pinned optional axe;
  unavailable download must not skip functional/keyboard/size checks.
* [x] P03-T03 Measure visible interactive targets at least 24px in both axes,
  retaining the designed 44px cited-lookup summary; prove removal of its CSS rule fails.
* [x] P03-T04 Run local CI-equivalent validation, update README/KB/evidence and
  PR body with honest unmet criteria, commit and push without waiting on CI.

Approved write boundary: workflow, src/api checks/tests and directly coupled
web sizing if necessary, READMEs, KB index/log and existing RPI artifacts.
No backend authority changes, private data, legacy trees, Azure or issue edits.

P03 complete. Corrections published as d2b8df4 after merge 91ed90e; existing
PR #354 body updated with CI wiring, mutation evidence and unchanged unmet
criteria. Hosted CI is pending; owner explicitly requested no waiting.

## Test Ownership and Boundary

No removals. Maximum two new test/check files, owned by API. Canonical targets:
web/chat.js, web/app.js, web/style.css, existing tests, new API browser check.
No generated production assets. Browser semantic assertions and axe/keyboard
checks complement existing server authorization and citation regressions.
Install missing dependencies with pip only. Browser scanner may use already
available axe or a pinned public axe script, never send app content externally.

## Critique Disposition

One final-candidate critique executed, verdict Revise; reconciled without rerun.
PC-001: accept the blocker-reporting gate; a blocking review finding leaves the
PR draft and delivery partial. Reject reopening Implement inside the one-pass
Review, as the parent lifecycle explicitly forbids it. Fix validation failures
before Review; route any later defect explicitly with severity and owner.
PC-002: accept an explicit matrix, but retain the issue's actual seven audiences
(repairs/intake, safety, assessor/coordinator, programme, finance/grants,
data handlers, suppliers), not the critique's substituted research audiences.
Leasehold and resident patterns are supplementary design-only proposals.

## Follow-Up Items

* Real staff comprehension with authorized repairs, housing and grants participants.
* Full manual assistive-technology/WCAG assessment and ADR chat-value ship test.
* Actual delegates and verified sources before operational reliance.

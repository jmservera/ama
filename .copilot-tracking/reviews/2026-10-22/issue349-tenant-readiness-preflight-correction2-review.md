---
title: Issue 349 preflight correction2 review
description: One post-implementation RPI review of malformed collection handling
ms.date: 2026-10-22
---

## Scope and Evidence

Task ID: 349. Slug: issue349-tenant-readiness-preflight-correction2.
Date: 2026-10-22. Original candidate:
4753af1edf74db7f5cf0ec1025b69d22f72f18f5.
Base: b4d467cad84535ed106cffa1ae9aa303db7bfed2.
Assessed boundary: correction2 P01 source/test changes, task requirements,
plan/detail reconciliation, critique dispositions and focused validation.
P02 publication and independent final PR assessment remain separate gates.

* Research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction2-research.md.
* Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan.md.
* Details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-correction2-changes.md.

## Opening Review State

Interpreted goal: assess the supplied malformed-collection correction without
turning offline checks into tenant acceptance. Evidence set is coherent and P01
is complete; P02-T01/P02-T02 are accurately pending. Compare the source guards,
CLI matrix and compatibility expectations first, then planning dispositions and
validation. Only this review record is writable during Review. No live calls
or source changes. Initial review blockers: none.

## Execution Status

Complete. Exactly one post-implementation Review executed on 2026-10-22,
directly in the parent context; no unnecessary review delegation.
No final independent PR review is claimed.

## Plan-to-Change Reconciliation

| Plan area | Evidence and comparison | Assessment |
| --- | --- | --- |
| P01-T01 | Three local guards precede iteration; all non-null non-list shapes produce fixed unknown/malformed-response without raw facts | Complete |
| P01-T01 compatibility | Null/absent remain empty; list filtering/counts unchanged; callback-target failure precedes redirect validation | Preserved |
| P01-T01 tests | Exactly three added methods, no removals; 60 malformed cases across both renderers, nine absent/null/empty cases and mixed-list/target regression | Complete |
| P01-T02 | 32 tests, isolated Ruff/format and strict script mypy pass; git diff --check clean | Complete |
| P02-T01 | This single Review assesses reconciled artifacts, code and evidence | Executed |
| P02-T02 | Commit, full gate, final fetch, receipt verification, push and draft PR intentionally still pending | Accurate remaining work |

## Completed Work Assessment

The correction validates the expected container shapes rather than catching
TypeError or converting arbitrary iterables. Falsey values cannot bypass the
guards. Dictionary keys cannot falsely satisfy audience, identifier URI or
callback membership. Each malformed check has empty facts; fixed strings and
existing rendering never echo response content. Unrelated checks continue.

The CLI test matrix asserts exit 1, blocked JSON/text, acceptanceEstablished false,
empty stderr and sentinel redaction. A separate Review cross-check set all three
fields malformed simultaneously: three fixed unknown findings, blocked and exit 1.
All transport calls in these checks use Fake; no tenant call is made.

## Implementation-Time Update Assessment

P01-T02's adjacent api/web binding clarification is justified: strict mypy errors
were reproduced on the original candidate and eliminated by binding each raw
value before the existing dict guard. No casts, ignore additions or runtime
behavior changes in the script. Changes, plan status and details reconcile this
as ordinary local type-safe work; no significant decision or scope expansion.

## Critique Assessment

Original one-pass verdict Revise is preserved. PC-001's temporary-directory ban
is unsupported in the parent's execution context and conflicts with the caller's
explicit shared-lock gate requirement; rejecting its proposed blocker is justified.
PC-002 is accepted in details with an explicit post-gate fetch and fail-closed
base-movement branch. No repeated critique, hidden material decision or premature
dependent work is evident.

## Findings and Routing

No implementation defects, unresolved design decisions or material research gaps
found within this correction. No later rpi-implement/plan/research route is needed.

### RV-001 [Low]: Publication evidence remains pending

* Scope: P02-T02, not a source defect.
* Evidence: plan and changes explicitly leave commit/full gate/publication pending.
* Impact: focused checks cannot authorize publication or validate the new head.
* Destination: distinct publication follow-up owned by this parent under the
  caller's existing authorization, not another RPI Review.
* Next action: commit current evidence, run exactly one full gate with unchanged
  shared lock, fetch main again and verify new-head/current-base receipt before push.

### RV-002 [Low]: Independent final PR assessment and live acceptance remain external

* Scope: plan Follow-Up Items and original issue #349 criteria.
* Evidence: caller explicitly reserves final assessment to coordinator; all six
  issue criteria were open/unticked at intake.
* Impact: code correction does not establish real sign-in, credential delivery,
  authority, staff binding or any issue acceptance.
* Destination: distinct coordinator exact-head assessment and authorized-owner
  live/human work. Do not start it or tick criteria in this task.

## Validation Evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Focused unittest discovery | Passed | 32 tests; red-first failures recorded before implementation |
| Isolated Ruff E,F,I,B,UP and format | Passed | Both changed Python files, line length 100, py312 |
| Strict mypy | Passed | Corrected script; external cache |
| Simultaneous malformed-field CLI cross-check | Passed | Three sanitized findings; blocked exit 1 |
| git diff --check | Passed | No whitespace defects |
| New-head complete local gate and receipt | Pending | Requires committed candidate, P02-T02 |
| Independent final PR review | Not performed | Explicit coordinator boundary |
| Live tenant/sign-in/acceptance | Not performed | Explicitly prohibited/outside authorization |

## Outcome

Outcome: Residual work. The bounded source correction meets its functional
requirements with no source defects found. Do not claim full-task conformance,
publication readiness or live acceptance while RV-001/RV-002 remain open.
Review execution is Complete; publication remains gated.

## Closeout Routing Record

Implementation defect: none. Decision gap: none. Research gap: none.
RV-001 returns to the parent's authorized publication step after this Review.
RV-002 remains coordinator/authorized-owner work outside the correction loop.
No second Review, source-fix loop, independent final assessment or merge is
authorized by this record. Preserve prior NEEDS CHANGES and old receipts as history.

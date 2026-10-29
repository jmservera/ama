---
title: Case journey round seven plan
description: Outcome-aware submission barriers and focused regressions
ms.date: 2026-10-29
---

## Task Metadata

Task 526-round7; slug case-journey-526-round7; PR #529; Refs #526.

## Executive Summary

Preserve server mutation outcomes and prevent stale actions from being repeated
after committed or uncertain errors. Audit and repair the same assumption in
case, proposal, draft, priority, upload and procurement paths while retaining
correctable explicit refusals and copyable drafts.

Execution complete; independent Review Complete / Not accepted. RV-001 High
and RV-002 Medium are routed follow-ups below, not repaired or re-reviewed in
this task. Implementation and original evidence retained locally at 6e353416.

### What You May Not Know

A 409 can also carry committed, so checking only 503 is insufficient. A case
history barrier must survive measure/tab changes and failed GETs. Local checks
are not a publication receipt or human accessibility acceptance.

## Sources

.copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md, C1-C9/W1-W2.

## User Decisions and Requirements

* Full RPI loop and sibling audit for seventh correction on the existing branch.
* Preserve outcome; committed/uncertain must return check-history and block retry.
* Run requested unit suites and journey/assistants browser checks with pinned axe.
* Shared .venv; flock -n heavy admission with <=40-minute retry; no Azure/secrets.
* Commit locally with Conventional Commit and required Copilot trailer; no push.
* PR retains Refs #526, no closing keyword; coordinator owns reply/resolution.

## Goals

No duplicate mutation following an ambiguous/committed response before
authoritative recovery; retain ordinary refusal correction.

## Scope and Non-Goals

app.js, assistants.js, ops.js and directly coupled raw forms in panels.js;
audit case-workspace.js without gratuitous edits. Owning tests/checks and API
README only. No framework, visual, backend authority or dependency change.

## Functional Requirements

One shared outcome-aware error predicate. Preserve status/reasons/outcome on API
errors. Shared refresh blocks case submissions after ambiguous outcomes, including
empty-field actions, until successful authoritative case GET. Proposal/draft/
priority/invocation/procurement paths must retain blocked state and actionable
history feedback; upload must dispatch inside the existing guarded refresh.
Raw resident/challenge forms must treat uncertain like committed.

## Non-Functional Requirements

Keep native semantics, existing status channels and editable/copyable drafts.
No new libraries, generated code, secrets or private fixtures. Ruff 100 columns.

## Acceptance Criteria

HTTP 409 and 503 with committed/uncertain and transport failures block duplicate
dispatch; 409 without such outcome remains retryable. Quality measure changes,
tab changes and failed reload do not unlock. Successful authoritative reload
unlocks only current evidence/action state. Both requested unit modules pass;
both browser checks pass with pinned axe and no serious/critical violation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement outcome preservation and sibling guards

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Shared API outcome classifier, case barrier and sibling corrections.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Focused unit/browser matrices and related README update.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and independently review

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Locked unit, lint/type and requested axe browser checks.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: One independent Review; preserve outcome; commit locally.

## Test Ownership and Locked Boundary

Owner src/api. Removals: none. Maximum additions: four unit methods and two
bounded browser helper functions, preferring extensions to existing matrices.
Canonical targets: shipped JS and test_case_journey/test_workspace_scripts.
Generated targets: none. Semantic matrices execute shipped handlers and count
dispatches; browser checks exercise actual api() with intercepted HTTP failures,
unchanged refusal behavior, authoritative recovery and axe. Existing tests retained.
External logs stay under the session files directory. No full gate claiming:
the repository complete gate requires az and conflicts with explicit no-Azure
direction; publication remains coordinator-blocked pending that separate gate.

## Critique Disposition

Sole critique Complete / Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round7-plan-critique.md.
PC-001 accepted: recovery snapshots must be captured before relevant GETs and
match the still-current barrier token. Case GET recovers case submissions and
invocation; proposal listing recovers uncertain proposal reviews by ID/revision.
Retained draft reviews, priority reviews and procurement remain blocked until
full workspace/page reload unless their own current resource is rehydrated.
PC-002 accepted: prepare file locally before guarded POST; existing form pending
guard excludes concurrent FileReader runs. Preparation failures remain retryable.
PC-003 accepted: extend existing shared-refresh, proposal and aiNotes unit
matrices; add at most four shipped-handler methods for API, upload, priority/
invocation/procurement and raw resident/challenge. Browser quality/proposal
matrices own actual HTTP outcomes, failed/old reads and recovery. No new critique.
Planning readiness: Ready.

## Follow-Up Items

* RV-001 High, later rpi-implement: persist pending identities across fieldless
  shared actions and rebuilt raw resident/challenge forms; prove one POST.
* RV-002 Medium, later rpi-implement: preserve unresolved shared-queue reason/
  JSON through old and fresh listings; keep actions guarded and drafts copyable.
* Coordinator: required exact-head publication gate and human/hosted approvals.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-29/case-journey-526-round7-changes.md.
All Pxx markers denote execution/retention, not acceptance. Review remains
Not accepted; no post-Review source fix or second Review was performed.

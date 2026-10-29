---
title: Case journey round eight plan
description: Correction of round-seven pending locks and queue draft loss
ms.date: 2026-10-29
---

Task: 526-round8. Parent: 526-round7. PR #529, Refs #526.

## Executive Summary

Guard the shared JSON mutation transport by action and target, including raw
resident/challenge handlers, so rendering and GETs cannot release pending POSTs.
Reuse revision-bound field recovery for the shared proposal queue. Retain all
historical findings and obtain one independent critique and post-implementation
Review for this correction. No publication or Azure action.

## User Decisions and Requirements

* Full research, plan, implement and review correction on the existing topic.
* Fix RV-001 High and RV-002 Medium; audit all sibling mutation paths.
* Focused unit and real journey/assistant browser checks with pinned axe.
* Worktree src imports, shared venv, Ruff 100 columns; no secrets or .env.
* Nonblocking heavy-check lock, retry at most 40 minutes.
* Conventional local commits with required trailer; never push or close #526.

## Goals

Exactly one pending POST per action/target, independent of DOM lifetime; no
silent loss or transfer of unsubmitted review edits during queue refresh.

## Scope and Non-Goals

app.js shared transport and field helpers, panels.js raw mutations,
assistants.js queue restoration, owning tests/checks and API documentation.
Audit ops.js, chat.js, case-workspace.js and other changed web files without
gratuitous edits. No framework, layout, authorization, server semantics or
historical evidence changes. No full publication gate requiring Azure tooling.

## Functional Requirements

* Persistent transport lock spans dispatch, HTTP headers and JSON parsing.
  Reads do not modify locks; changed note/JSON/revision cannot bypass a lock.
* Action/target keys distinguish unrelated records/actions without using mutable
  payload content. Every employee POST shares this boundary.
* Duplicate entry yields explicit status feedback, not uncertain/committed
  classification. Existing refusal retry and history barriers remain.
* Raw-handler JSON parsing stays strict for every HTTP status. Parse failure
  releases the transport lock but retains drafts and requires a history check;
  it never becomes a success-shaped empty response.
* Snapshot latest queue edits immediately before replacement; restore matching
  ID/revision only. Changed/missing proposals retain read-only copy recovery.
* Failure retains drafts and a read-only retry path. Success consumes only
  unchanged submitted values, never later edits or unsubmitted JSON.
* Queue state cannot leak across authenticated sessions or survive explicit
  navigation discard unexpectedly; warnings include recovery-only drafts.

## Non-Functional Requirements

Native labels, status feedback, manual routes, Fluent styling, consent and
approval boundaries remain. No automatic POST retry or private-data access.

## Acceptance Criteria

* Held fieldless, shared-field and rebuilt resident/challenge POSTs dispatch once,
  even across same-case refresh; mutable edits do not change lock identity.
* Sibling quality, finance, grant, technical, funding, handoff, hazard,
  procurement, draft review, invocation and chat routes use shared transport.
* Different action/target can proceed; lock survives body parsing and releases
  after success, explicit refusal, transport failure or malformed response.
* Queue reason and edited JSON survive pending, old, failed and fresh listings;
  changed/missing versions remain copyable without enabling stale review.
* Existing src/api unit tests and journey/assistants browser checks pass with axe.
* Independent review execution and outcome retained honestly; no human,
  deployed, hosted or publication acceptance inferred.

## Test Ownership

Canonical semantic regressions: test_case_journey.py (at most four added methods,
extend existing raw-form/proposal matrices as needed). Regression owner:
test_workspace_scripts.py unchanged unless its isolation fixture needs a new
shared global. At most one new helper in each existing browser check; extend
existing outcome matrices. Removals: none. Generated evidence: new external
session directory only; no generated source or golden replacement.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Correct and exercise shared state

* [x] P01-T01 Implement transport lock and revision-safe queue recovery.
* [x] P01-T02 Add focused unit/browser regressions and API documentation.

<!-- rpi:phase id=P02 -->
### P02: Validate and independently assess

* [x] P02-T01 Run focused and related unit/static/browser checks under lock.
* [x] P02-T02 Independent Review; reconcile evidence and commit locally.

## Critique Disposition

Sole critique Complete / Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round8-plan-critique.md.
PC-001 High applied directly: strict raw-response parsing and malformed 2xx/
409/503 coverage added to existing matrices.
PC-002 Medium rejected: the worker asserted a prohibition on temporary file
operations that is absent from the parent execution instructions and conflicts
with the user's exact required `/tmp/ama-rpi-heavy.lock` protocol. Preserve the
requested interoperable lock; never substitute an isolated lock.

## Follow-Up Items

Coordinator owns publication exact-head gate, push, hosted checks and human
acceptance. This local correction cannot establish those gates.
Round-eight Review Complete / Not accepted routes raw-form mounted feedback
and retained challenge recovery to a distinct correction child, selected by
the user's original "until Conformant" direction. Original verdict is retained.

## Handoff

Research: .copilot-tracking/research/2026-10-29/case-journey-526-round8-research.md.
Details: .copilot-tracking/details/2026-10-29/case-journey-526-round8-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/case-journey-526-round8-changes.md.
Execution complete; sole Review Complete / Not accepted. Original round-seven
defects are corrected; the two new Medium findings route to round nine.
Local source/evidence commit follows this reconciled record; publication separate.

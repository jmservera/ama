---
title: Case journey round nine recovery plan
description: Repair raw-form presentation state across refresh and recovery
ms.date: 2026-10-29
---

Task 526-round9; parent 526-round8. PR #529, Refs #526.

## Executive Summary

Keep raw-form presentation state in the case session and bind each rebuilt or
retained form to it. Publish eventual feedback to the mounted form. Reconcile
retained challenge buttons only after an authoritative history read, without
releasing a still-pending lock. Preserve the prior Review and run an independent
Review of this distinct correction.

## User Decisions and Requirements

* Original user instruction selects corrections until Conformant.
* Preserve pending action/target exclusion, drafts and outcome boundaries.
* Validate focused/related units and both browsers with axe under shared lock.
* Local commits only, trailer required, no Azure/secrets/push; Refs #526.

## Goals

Visible eventual raw mutation feedback and usable retained drafts after fresh
history recovery, without changing the already-corrected transport/queue paths.

## Scope and Non-Goals

panels.js raw presentation/restore lifecycle, existing unit/browser matrices
and API README. No server, transport-lock or queue behavior redesign.

## Functional Requirements

* Rebuilt same-session raw forms retain pending/uncertain/committed/refused state
  and latest feedback. No duplicate click is needed to surface the outcome.
* Retained challenge controls synchronize after fresh history recovery, but
  pending or pre-outcome/failed reads cannot unlock them.
* Correctable refusals re-enable current controls; retained drafts survive.
* Preserve the distinct acknowledged challenge draft guard: later edits in its
  original submitted form cannot repeat a known recorded action. Explicit
  confirmed discard, not history recovery alone, releases that draft guard.
* Success with failed reload still surfaces history instructions; no POST retry.
* Session-owned presentation state must not invoke a completed handler's stale
  refresh closure or repaint a different case after navigation.

## Non-Functional Requirements

Existing native labels, polite status, focus, plain content and manual routes
remain; the shared transport continues owning exclusion and strict parsing.

## Acceptance Criteria

* Hold POST, reconstruct without a second click, deliver uncertain/committed:
  current visible status explains history recovery, button disabled, one POST.
* Refusal permits corrected current-form retry with retained later input.
* Fresh same-case history recovery re-enables retained challenge/resident input;
  another corrected POST occurs once, only after recovery.
* Pending case refresh, old/failed reads and raw malformed responses remain safe.
* Focused/related unit suites, journey and assistants checks with axe pass.
* Independent Review records Complete / Conformant only if evidence supports it.

## Test Ownership

Extend existing raw unit matrix and journey mutation_reconstruction helper;
at most one added unit method for retained-form restoration if needed.
No new browser helper, test removal or generated source. Existing assistant
suite remains regression ownership for the prior queue correction.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Repair raw presentation lifecycle

* [x] P01-T01 Implement shared raw-form presentation state and retained sync.
* [x] P01-T02 Extend regressions and API documentation.

<!-- rpi:phase id=P02 -->
### P02: Validate and assess

* [x] P02-T01 Focused/related units, static and both browser checks under lock.
* [x] P02-T02 Sole independent Review and local evidence commit.

## Critique Disposition

Sole critique Complete / Pass, no findings, retained at
.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round9-plan-critique.md.

## Follow-Up Items

Publication exact-head gate, push, hosted/human approval remain coordinator-owned.

## Handoff

P01/P02 completed. Sole independent Review Complete / Conformant, zero findings;
correction and original evidence retained in the local commit, without push.
Research and phase details use this task's
2026-10-29 slug; original findings remain at the round-eight Review path.

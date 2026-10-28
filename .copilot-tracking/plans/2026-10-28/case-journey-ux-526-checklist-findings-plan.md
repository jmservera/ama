---
title: Case journey checklist Review findings implementation
description: Later scoped implementation of RV-001 and RV-002 without repeating original Review
ms.date: 2026-10-28
---

Task: 526-checklist-findings; parent 526-correction.

## Executive Summary

The original correction Review is Complete / Not accepted. Preserve it unchanged.
Its two High findings are ordinary local implementation defects in the user's
explicitly requested checklist root fix, not a new feature or user-owned design
choice. This later invocation implements those exact findings, adds their
missing transitions to the existing runner and records new validation. It does
not rerun or claim to supersede the original Review.

## User Decisions and Requirements

* Existing user instruction requires each of seven bugs fixed at its root.
* Same branch/worktree, stepper unchanged, no Azure/az/secrets/.env.
* Browser lock uses flock -n with 15-second retries and 40-minute ceiling.
* No force push. Publication remains blocked; local safe commit is authorized.

## Goals

Ensure recovery cannot overwrite newer live evidence or be cleaned by an
unrelated successful submission.

## Scope and Non-Goals

Only RV-001/RV-002, relevant helpers in app.js, quality panel in ops.js,
and transitions in existing journey browser check. No repeated original
critique or Review, new design, framework, endpoint or authority.

## Functional Requirements

Reconcile recovery on every measure paint; live controls take precedence for
duplicate keys. Snapshot only quality controls represented in the request,
excluding all read-only recovery. Preserve other measure/version evidence.

## Non-Functional Requirements

Keep all original tests and human/consent/safety boundaries. No new runner.

## Acceptance Criteria

A -> B -> refresh -> A -> edit -> refresh retains the newer A value.
Saving B with recovered A present preserves dirty/copyable A across refresh.
Saving a current checklist version preserves earlier-version recovery.
Existing journey/axe and assistant checks remain valid; unit/static/types pass.
These are later implementation tests, not independent closure or acceptance.

## Phase Checklist

<!-- P01 -->
### P01: Implement routed findings

* [x] P01-T01: Fix live/recovery precedence and quality payload cleanup.
* [x] P01-T02: Add exact regression transitions and run admitted checks.
* [x] P01-T03: Reconcile evidence and commit all local work safely.

## Critique Disposition

Original correction critique retained. No planning direction, requirement,
architecture or user-owned choice changes; no new critique.

## Follow-Up Items

Original Not accepted Review, complete gate/no-az conflict, independent exact-head
assessment and normal publication/thread resolution remain outstanding.
Human/live acceptance remains distinct.

P01 complete: later implementation and regressions are locally verified and
committed in b314ed0061a7f8447ab39b159cb78b457324c4ba.
The original Review's adverse outcome is unchanged;
these passing tests are not independent acceptance or a repeat Review.

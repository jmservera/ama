---
title: Capacity booking checkpoint plan (Refs #440 #82 #81)
description: Plan for the eleventh stabilization checkpoint record, index paragraph and log entry
ms.date: 2026-11-06
ms.topic: reference
---

Task ID: 440-capacity-booking-checkpoint. Slug: capacity-booking-checkpoint-440. Mode: manual, focused documentation tier.

## Executive Summary

Append one eleventh, local candidate checkpoint to the cutover evidence pack, one README index paragraph and one appended log entry. It records three separate pins, document-qualified traceability for the capacity booking gate merged by PR 1229 (and the quality interaction, plus #1228 provenance wording), a 193-test light observation on an immutable `af891a5cc` export, and a continue recommendation with no approval, closure or tick. Research is committed before this plan; the plan, details and the single critique are committed before any pack, index or log edit.

## User Decisions and Requirements

* Prospective order Research, Plan and details, Implementation, Review; commit research and plan/details before any pack, index or log edit.
* New bounded checkpoint; not a rewrite or third correction of finance or lifecycle records; preserve all prior and adverse records.
* Pins stay separate: governance `a97bea15`, lifecycle `af891a5cc`, main `bb3a3b03`.
* Light and focused only; no SQL, service, browser, heavy gate, lock, install or cleanup; no SQL claim at the parent; tree equality is not a run.
* Distinguish supplied evidence from what was read or run; do not reproduce the false zero-nonzero assertion; do not copy raw bundles.
* Bounded semantics: sole capacity failure rethrows structurally; mixed stays ValueError; Fail for known deficit or date; Unknown for absent order, missing, stale or unreadable inputs; Pass internal only; capacity last; RV-C1 is not a current defect.
* No approval, pivot, closure or tick; native HVE Deferred is not Pass; C7 and C8 stay unticked.

## Goals

* Honest eleventh record: trigger, identities, traceability, boundaries, human and safety gates, manual paths, classification, recommendation and remaining backlog.

## Scope and Non-Goals

* In scope: the pack, README index, log and this RPI evidence.
* Non-goals: source, policy, ADRs, approvals, heavy gates, whole 81, 82 or 440 closure.

## Functional Requirements

* Heading names it eleventh with an explicit anchor; ninth, tenth and eighth anchors untouched.
* Each evidence row is classified local observed, Azure observed, implemented-unverified, deferred, blocked or unknown with source and date.
* PRD FR-008, FR-016 and FR-017 and BRD FR-008 are qualified by document.

## Non-Functional Requirements

* ASCII, `*` bullets, no em dashes, zero removed lines in docs, external caches.

## Acceptance Criteria

* Diff adds lines only to docs; `git diff --check` clean; anchors resolve; worktree clean including ignored files after each commit; a final Review follows the final checks.

## Critique Disposition

Critique executed once (fresh worker), verdict Revise, six direct planner-owned findings (3 Medium, 3 Low), all applied without a user decision or second critique. File: .copilot-tracking/plans/2026-11-06-capacity-booking-checkpoint-440-critique.md.

* PC-001 applied: FULL, SQL, hosted and functional results are labelled supplied and historical for candidate 272146f4e (tree equality is identity, not a parent run); the functional result is a code-review result, not an approval.
* PC-002 applied: the diff size is stated as 23 files, +519/-16 for #1228 plus #1229 over `cd271cfa5`, with #1229 alone 17 files, +447/-15.
* PC-003 applied: the pack states the `/tmp` evidence is session-only and the sha256 is the durable pointer.
* PC-004 applied: the 13 expected nonzero probes are attributed to the #82 comment, not read here, and the false assertion is not quoted.
* PC-005 applied: each document blob carries its path; the PRD is the zava-forward file (0.21.0, `c788b917`).
* PC-006 applied: this section is now final and the eleventh anchor follows the tenth anchor pattern.

## Phase Checklist

* [ ] P01 Record: P01-T01 identities, P01-T02 traceability and boundaries, P01-T03 evidence and observation, P01-T04 recommendation and gates.
* [ ] P02 Index and log.
* [ ] P03 Validate.
* [ ] P04 Close: changes, one Review, state JSON, commit.

## Follow-Up Items

* Remaining #82 gate families and named rule review: #82. Integrated parent FULL and SQL: coordinator admission after the heavy holder releases.

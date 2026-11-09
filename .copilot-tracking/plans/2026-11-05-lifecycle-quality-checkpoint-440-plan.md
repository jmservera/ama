---
title: Lifecycle quality-gate checkpoint plan (Refs #440 #82 #81)
description: Plan for the tenth stabilization checkpoint record, index paragraph and log entry
ms.date: 2026-11-05
ms.topic: reference
---

Task ID: 440-lifecycle-quality-checkpoint. Slug: lifecycle-quality-checkpoint-440. Mode: manual, focused documentation tier.

## Executive Summary

Append one tenth, local DRAFT checkpoint to the cutover evidence pack, one index paragraph and one appended log entry. It records three separate pins, document-qualified traceability for the fail-closed quality gate merged by PR 1226, a 183-test light observation on an immutable `cd271cfa` export, and a continue recommendation with no approval, closure or tick. Research is done and recorded first; the pack, index and log are edited only after this plan, details and the single critique exist.

## User Decisions and Requirements

* Prospective RPI order; this is a new checkpoint, not a correction of the finance record; preserve finance, r2, r3 and adverse history.
* Pins stay separate: governance target `1faadaa3`, lifecycle source `cd271cfa`, main `bb3a3b03`.
* Light observation only; no heavy lock, SQL Server, browser, Docker or cloud; no SQL claim at the parent; tree equality is not a run.
* Distinguish supplied evidence, independently read, historical source `10161` and new parent `cd271`.
* No approval, closure, tick, pivot, relaxation or issue proposal without a confirmed defect; append-only log; no amend.

## Goals

* Honest tenth record with traceability, store boundaries, identity and roles, evidence visibility, independence, resident and safety gates, manual paths and remaining backlog.

## Scope and Non-Goals

* In scope: `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`, this RPI evidence.
* Non-goals: source, policy, requirements, ADRs, approvals, heavy gates, whole 81, 82 or 440 closure.

## Functional Requirements

* Heading names it tenth with an explicit anchor; finance ninth and baseline eighth anchors untouched.
* Evidence table classifies each row local observed, Azure observed, implemented-unverified, deferred, blocked or unknown, with source and date.
* PRD FR-008 and BRD FR-008 are qualified by document.

## Non-Functional Requirements

* ASCII, `*` bullets, no em dashes, no bolded-prefix items, zero removed lines in the log and pack, external caches.

## Acceptance Criteria

* Diff adds lines only to the pack, index and log; checks pass; worktree clean after commit including ignored files.

## Critique Disposition

Critique executed once (fresh worker), verdict Revise, five direct planner-owned findings, all applied without a user decision or second critique. Critique file: .copilot-tracking/plans/2026-11-05-lifecycle-quality-checkpoint-440-critique.md.

* PC-001 applied: the record separates SQLite-backed `SqlStore` variants observed in the 183 tests from SQL Server and the full SQL gate, which stay implemented-unverified at the parent.
* PC-002 applied: the skip is stated as inferred from the single `skipTest` in `test_hazard_referral.py`, not shown by the non-verbose log.
* PC-003 applied: PRD AC-010, AC-011, AC-067 and AC-144 are listed as mapped criteria with acceptance Not run; passing light tests do not tick them.
* PC-004 applied: the record states that the light run predated this plan, as research-phase read-only observation.
* PC-005 applied: re-check the three pins before commit and note that `/tmp` evidence is identified by hash only.

## Phase Checklist

* [ ] P01 Record: append the tenth pack record (P01-T01 identities, P01-T02 traceability and boundaries, P01-T03 evidence and observation, P01-T04 recommendation and gates).
* [ ] P02 Index and log: add the README paragraph and one appended log entry.
* [ ] P03 Validate: whitespace, ASCII on added lines, zero removals, anchors and links, JSON state.
* [ ] P04 Close: changes record, one Review, state JSON, commit with privacy-safe identity.

## Follow-Up Items

* Remaining #82 gate families and named rule review: owned by #82, not this record.
* Heavy SQL or full gate at the lifecycle parent: after #144 releases heavy resources, by coordinator admission.

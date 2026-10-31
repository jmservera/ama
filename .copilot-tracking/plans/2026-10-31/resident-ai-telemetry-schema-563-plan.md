<!-- markdownlint-disable-file -->
---
title: Resident AI telemetry schema correction plan
ms.date: 2026-10-31
---

## Task Metadata

* Task ID: pr-585-telemetry-schema-correction-563-2026-10-31
* Task slug: resident-ai-telemetry-schema-563
* Planning status: Complete, implementation-ready
* Details: .copilot-tracking/details/2026-10-31/resident-ai-telemetry-schema-563-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/resident-ai-telemetry-schema-563-plan-critique.md

## Executive Summary

Append a dated, controlling resource-specific handoff to the original changes
record. Preserve both historical legacy blocks; supply corrected equivalents
for the future query and historical aggregate without pretending either was
executed. Only that original artifact and this new dated RPI evidence change.
No live cause, model dispatch/spend or whole #563 acceptance is established.
No implementation blocker; later publication still requires fresh full gates.

## User Decisions and Requirements

* Correct the real PR #585 schema finding; Refs #563 only.
* Run Research, Plan, Implement and Review in order with dated tracking artifacts.
* Preserve earlier records by appending a dated correction.
* Docs only; no Azure, secrets, source changes or push.
* Commit locally on ops/resident-ai-diagnosis-563 with the requested Copilot trailer.

## Goals

* G1: provide one authoritative future query matching the recorded destination.
* G2: preserve earlier observations and qualify what local evidence proves.

## Scope and Non-Goals

In scope: original changes artifact plus seven new dated lifecycle artifacts.
Non-goals: source/infra/production-doc edits, other PRs' historical queries,
Azure/model/SQL access, live telemetry, issue closure, publication.

## Functional Requirements

* FR1: append both resource-specific query variants and explicitly supersede
  the old future handoff, not the actually attempted denied query.
* FR2: retain exact windows, app/revision, event labels, SDK extraction,
  projection/aggregation and privacy/authorization boundaries.
* FR3: account for all seven original PR paths; no additional duplicate was found.

## Non-Functional Requirements

* NFR1: zero deletions or replacements of original bytes.
* NFR2: zero source/test additions or removals; no generated runtime targets.
* NFR3: future snippets contain zero legacy table/column identifiers.

## Acceptance Criteria

* AC1: current future snippet uses ContainerAppConsoleLogs, ContainerAppName,
  RevisionName and Log with unchanged TimeGenerated and semantics.
* AC2: equivalent corrected aggregate exists, explicitly not executed.
* AC3: all original paths are byte-identical except an append to changes.
* AC4: original critique/Review verdicts and live blockers remain unchanged;
  new Review reports documentary scope, not live approval.
* AC5: local commit has privacy-safe author/committer, required trailer and
  Refs #563; no push. Final clean status and exact changed-path scope verified.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-31/resident-ai-telemetry-schema-563-research.md,
Complete/Ready, C1-C5. Changes path:
.copilot-tracking/changes/2026-10-31/resident-ai-telemetry-schema-563-changes.md.
Caller explicitly authorizes remaining phases; no indefinite automatic session.

## Sources

* Research C1-C5: exact changed paths, historical/future query distinction and
  infra/README.md resource-specific contract.
* Explicit user request: authority for local commit, no publication.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Append schema correction

Dependency: completed Research and one critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Append two corrected query variants

FR1-FR3, AC1-AC3; target original changes record; detail P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, review and persist

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate documentary invariants and perform one Review

AC1-AC4; exact snippet comparison, seven-path preservation, diff and Markdown
review. One independent reviewer, original outcome preserved.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Commit locally and verify persistence

AC5; dependency P02-T01. Explicitly stage only intended documentation artifacts.

## Dependencies

Canonical schema, preserved original bytes at bbbd969b, critique, original new
Review before commit. No runtime tests apply to a query documentation append.
No full local publication gate is claimed or run: no push/publication is
authorized. A later coordinator must fetch current main and run and verify a
fresh complete exact-head gate before publication; local review is not approval.

## Critique Disposition

Independent critique executed Complete / Pass, zero findings; no revision or
significant decision required. Original critique retained, no repeat.
Test ownership locked to
documentary assertions only; test removals none; test additions maximum zero;
canonical target is the original changes appendix; generated targets none.
Semantic coverage compares corrected snippets exactly to legacy snippets with
the four known schema substitutions. Regression coverage checks original-byte
prefix and all six other original files unchanged.

## Follow-Up Items

* Coordinator-owned private telemetry acquisition remains outside this local
  correction; historical access/dispatch/root-cause blockers remain open.
* Publication requires fresh full gate, hosted checks and human decision.

## Handoff

P01 and P02-T01 complete. Independent Review executed once Complete /
Conformant, zero findings, for the working-tree documentary boundary.
P02-T02 complete: candidate 2fcf2f0985ee9be8ae5502ebb510bb0c94b54495
committed locally and verified clean, identity/trailer and exact scope passed.
This parent closeout records the actual result in a second local evidence-only
commit; no source/content correction, additional scope or repeated
critique/Review. No push; this caller-bounded loop ends, no child task started.

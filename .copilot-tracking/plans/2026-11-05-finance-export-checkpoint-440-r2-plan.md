---
title: Finance export checkpoint correction plan (r2, Refs #440 #96)
description: Plan for the bounded documentation correction of the DRAFT d2679106 finance checkpoint
ms.date: 2026-11-05
ms.topic: reference
---

Task ID: 440-finance-export-checkpoint-r2. Details: [details](../details/2026-11-05-finance-export-checkpoint-440-r2-details.md). Research: [research](../research/2026-11-05-finance-export-checkpoint-440-r2-research.md).

## Executive Summary

Correct the local DRAFT finance checkpoint (d26791065) by documentation edits only: add a process qualification, rename its ordinal from eighth to ninth with a preserved old anchor, remove the unsupported hosted-status claim, make supplied versus observed evidence and the conditional recommendation unambiguous, repair the current index link and append a new log correction. Original files and prior log lines stay unchanged. Readiness: Ready after one critique.

## User Decisions and Requirements

* Prospective loop: research, plan, details and critique are written and verified as the only additions before any corrective pack, index or log edit.
* Original d267 process is not retroactively compliant; adverse evidence preserved; no rewriting.
* Ninth is the new ordinal; old anchor kept; log correction appended, prior lines untouched.
* Remove or qualify the "latest run on main completed (rubric scorer path)" claim.
* FOCUSED documentation tier; no rerun of the 40 tests; no heavy resource; no source, policy, requirement, authority, HVE or deployment change; no push, PR, issue or human box.

## Goals

* A corrected, unambiguous ninth checkpoint record and honest process chronology.

## Scope and Non-Goals

* In scope: the finance section of docs/architecture/cutover-evidence-pack.md, the current finance paragraph in docs/reference/README.md, one appended log entry, new r2 RPI files.
* Out of scope: the baseline eighth section (integrated parent topic), original RPI files, prior log lines, source, tests, #96 worktree.

## Functional Requirements

* FR1 Process qualification section. FR2 Heading ninth plus explicit old anchor. FR3 Main row states commit and tree identity only. FR4 Evidence classes: source-observed, locally executed (40 tests, historical to this correction), coordinator-supplied unverified (hosted checks, approval, receipt 07ae). FR5 Recommendation conditional on coordinator consumption; #96 stays paused. FR6 Index link repaired, log correction appended.

## Non-Functional Requirements

* ASCII only, no em dashes, append-only log, YAML frontmatter on new Markdown, no `.copilot-tracking` references in production docs beyond existing practice.

## Acceptance Criteria

* AC1 Only r2 research, plan, details and critique are added before implementation (verified by git status). AC2 New anchor resolves and old anchor resolves. AC3 Log diff has zero deletions. AC4 No "scorer path" completion claim remains in the finance section. AC5 git diff --check, ASCII, JSON and link checks pass. AC6 Original artifacts byte-identical to d267. AC7 The appended log entry states the eighth to ninth relabel, the current anchor, old-anchor retention and no #96 release.

## Phase Checklist

* [ ] P01 Corrective documentation edits (tasks P01-T01 to P01-T05)
* [ ] P02 Checks and changes record
* [ ] P03 One review and state

## Critique Disposition

Critique executed once (Complete, verdict Revise): [critique](../plans/2026-11-05-finance-export-checkpoint-440-r2-critique.md). PC-001 (log correction must explicitly relabel eighth to ninth, name anchors, restate no #96 release) applied directly to P01-T05 and AC7. No further critique will run.

## Follow-Up Items

* Coordinator independent exact-head assessment; publication and hosted gates; #96 resume only after valid checkpoint consumption.

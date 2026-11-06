---
title: Sensor integration retained-evidence checkpoint 440 plan
description: Plan for an additive retained-evidence qualification of the Sixteenth sensor parent checkpoint
ms.date: 2026-11-06
---

## Task

Task ID `440-sensor-retained-evidence-checkpoint`, slug `sensor-retained-evidence-checkpoint-440`. Research: `.copilot-tracking/research/2026-11-06-sensor-retained-evidence-checkpoint-440-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-06-sensor-retained-evidence-checkpoint-440-details.md`. Critique: `.copilot-tracking/plans/2026-11-06-sensor-retained-evidence-checkpoint-440-critique.md`.

## Executive summary

The Sixteenth checkpoint already records the sensor parent integration but labelled the child receipt figures as supplied. This plan appends one additive subsection under it that records what was read from the retained r20 files (receipt, SQL logs, supplement log and cleanup, image scan JSON) with exact classification, appends a log entry and a short index note. Local documentation only; no new checkpoint number.

## User Decisions and Requirements

* Execute the due sensor checkpoint through bounded RPI in the existing cutover pack; target #1222 branch unchanged; local handoff only, no push, PR or ticks.
* Consume actual retained evidence; no repeated heavy execution; no new defects invented; no duplicate issues.
* Distinguish maintained SQL 285 with one declared JSON-only skip from the owned 68-test supplement with zero skips, and package skips; record current image risk 42 (40 High, 2 Critical), fixable 0, not security-clean.
* Keep live Hub or SQL, credentials, calibration, statistical validity, provenance and named approvals unproven; weather is not indoor measurement.
* Record CONTINUE, FIX or HOLD, gates for #184, #185, #188, and independent lanes. Preserve older checkpoints, append-only log and the index.
* Do not repeat the R10 typo correction or create index-only correction loops.

## Goals

* One compact additive subsection and log and index entries, traceable to files read.

## Scope and Non-Goals

Scope: pack subsection, log entry, index note, new tracking records. Non-goals: source, tests, requirements, ADRs, earlier sections, new issues, heavy checks, any publication.

## Functional Requirements

* FR1 Subsection under the Sixteenth with pins, document blobs, retained-evidence table with classification, SQL kinds, image risk, boundaries, exclusions, recommendation and gates.
* FR2 Log entry appended; README note after the Sixteenth or provenance paragraph.

## Non-Functional Requirements

* NFR1 ASCII, `*` lists, no H1 in new Markdown with frontmatter, no em dashes.
* NFR2 Append-only: add the new section at the end of the pack, after the Seventeenth, as a labelled additive qualification of the Sixteenth; no insertion into earlier text.
* NFR3 Noreply identity, Conventional message with Copilot trailer, no amend.

## Acceptance Criteria

* AC1 Every numeric claim in the subsection matches the file read; unread parts are stated as unread.
* AC2 Pack and log diffs are additions only; README is additions only; all earlier tracking records unchanged.
* AC3 `git diff --check`, ASCII, frontmatter, link and anchor, JSON parse pass; ignored-inclusive status clean at freeze.
* AC4 The subsection states the receipt belongs to child head `6887377` and not the parent squash commit, labels diff-size figures by scope, and does not cite unread browser results.

## Phase Checklist

* [ ] P1 Append pack subsection, log entry and index note
* [ ] P2 Run focused checks
* [ ] P3 Changes, later author Review, state, commit

## P1 Append pack subsection, log entry and index note

* [ ] P1-T1 Pack subsection (FR1).
* [ ] P1-T2 Log entry and README note (FR2).

## P2 Run focused checks

* [ ] P2-T1 Pins, additions-only diffs, prior-record invariance, anchors, ASCII, frontmatter, status.

## P3 Changes, Review, state, commit

* [ ] P3-T1 Changes after checks.
* [ ] P3-T2 Author Review in a later turn.
* [ ] P3-T3 State once, commit, verify clean.

## Follow-Up Items

* Verify the cause of the 42 versus 39 image findings (scanner database versus image content); owner #188 lane.
* Receipt at the intended parent head, and the unread parts of the browser results, remain for the coordinator or the owning lane.
* Published 136 topology unresolved (unrelated).

## Critique Disposition

One independent critique ran (Revise; 0 Critical or High, 4 Medium, 3 Low). The critic read the critique SKILL.md and template. All findings applied directly; no user decision; no second critique.

* PC-001 Medium, applied: 192 exit 0 and 13 exit 1 are now read from `receipt.json` command `exit_code` fields (confirmed this session). The explanation of the 13 as expected probes is attributed to the child's native log, not to retained receipt data.
* PC-002 Medium, applied: the 42 are vulnerability instances. Unique vulnerability IDs per image were read from all four scan JSON files this session: 17 each. The subsection states both counts.
* PC-003 Medium, applied: browser results are not cited as evidence; stated as not assessed.
* PC-004 Medium, applied: new AC4 below; the 99-file (including tracking records) and 19-file (source and tests) figures are labelled as different scopes, and the receipt is stated as belonging to child head `6887377`.
* PC-005 Low, applied: README note placed after the R10 paragraph, with the append-only rationale.
* PC-006 Low, applied: AC1 method is a scripted recomputation of numeric claims from the files, recorded in Changes.
* PC-007 Low, applied: this section is now final.

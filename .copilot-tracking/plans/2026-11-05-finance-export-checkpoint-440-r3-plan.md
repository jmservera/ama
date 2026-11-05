---
title: Finance export checkpoint r3 plan (Refs #440 #96)
description: Plan to correct one evidence statement about the failed initial archive-root attempt
ms.date: 2026-11-05
ms.topic: reference
---

Task ID: 440-finance-export-checkpoint-r3. Research: ../research/2026-11-05-finance-export-checkpoint-440-r3-research.md. Details: ../details/2026-11-05-finance-export-checkpoint-440-r3-details.md.

## Executive Summary

Replace the incorrect "output not preserved" sentence in the ninth finance checkpoint with the preserved wrapper error and exit 1 and the absent dedicated test output, and append one log correction. Documentation only; repaired 40-test exit 0 stays historical.

## User Decisions and Requirements

* Prospective loop; originals and r2 preserved; edit only this evidence statement.
* Cite `/tmp/rpi-440-finance-export-checkpoint-20261105.log` and persist the exact snippet in r3 records.
* Append one log correction; keep ninth heading and old anchor; no rerun; no other recommendation change; #96 stays paused.

## Goals

* Accurate statement of what the failed attempt did and did not preserve.

## Scope and Non-Goals

* In scope: one pack paragraph, one appended log entry, r3 files. Out: source, other pack text, README, r2/original files.

## Functional Requirements

* FR1 State: wrapper error and exit 1 preserved in the native log; failure on cd before any Python or test command; no test executed; no dedicated per-test output file. FR2 Cite log path. FR3 Keep repaired exit 0 historical, not rerun.

## Non-Functional Requirements

* ASCII, append-only log, YAML frontmatter on new files.

## Acceptance Criteria

* AC1 Only r3 research, plan, details, critique untracked before edits. AC2 Old statement absent from live pack; snippet present in r3 changes. AC3 Log removals 0, one entry added. AC4 diff check, ASCII, JSON, anchors pass. AC5 Other files unchanged.

## Phase Checklist

* [ ] P01 Edit pack paragraph (P01-T01) and append log entry (P01-T02)
* [ ] P02 Checks, changes record with snippet
* [ ] P03 One review, state, commit

## Critique Disposition

Critique executed once (Complete, Revise). PC-001 (name the exact log target docs/reference/log.md; native log stays immutable) applied directly to P01-T02. No further critique.

## Follow-Up Items

* Coordinator assessment, publication, hosted gates and consumption.

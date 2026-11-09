---
title: UI and cache recovery checkpoint wave 3 plan (Refs #440)
description: Plan for the focused current-main observation and documentation-only checkpoint record
ms.date: 2026-11-05
ms.topic: reference
---

## Plan

Research: `.copilot-tracking/research/2026-11-05-ui-cache-checkpoint-wave3-440-research.md`. Details: `.copilot-tracking/details/2026-11-05-ui-cache-checkpoint-wave3-440-details.md`. Tier: focused. Local only.

* [ ] Phase 1: pin freshly fetched completed-main state (after scorer run 42036086584 completes; stop if main is still moving).
* [ ] Phase 2: create the clean detached exact-main auxiliary worktree and its own verified environment.
* [ ] Phase 3: run the two focused checks under the actual non-queued exclusive heavy lock, or record the holder and resume point.
* [ ] Phase 4: append the seventh checkpoint to `docs/architecture/cutover-evidence-pack.md`, add the minimal index and log entries.
* [ ] Phase 5: validate (links, ASCII, diff, static), write changes, run one Review, commit locally, freeze.

## Decisions

* Observation target is main only; parent source is described by blob and never run as main.
* Original six comparability checkpoint and #1213 records and their NOT CLEAN outcome remain parent-only and immutable.
* No new issue unless a reproduced finding differs from #1214 or #1215; none is implemented here.
* The log is append-only; preserve full contents.

## Critique (single, final candidate, self-performed)

An independent critique agent was not run for this documentation-only focused tier; the independent exact-head assessment belongs to the coordinator. Self-critique findings applied directly: label the rubric commit and the pin explicitly; never describe the pre-merge partial receipt as observed; keep BRD/PRD/ADR IDs document-qualified; state that ADR 0003 and ADR 0006 trace only indirectly.

## Stop conditions

* Main still moving at observation time: stop before observation, record exact resume point.
* Lock held: no queue or retry; record the holder and unfinished observation.
* Missing Chromium, axe or interpreter: block only that slice; never convert to Pass.

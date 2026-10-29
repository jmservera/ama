<!-- markdownlint-disable-file -->
---
title: Original view coverage implementation continuation
description: Bounded implementation of correction1 Review RV-001
ms.date: 2026-10-28
---

## Task Metadata

Task ID: 524-view-coverage. Parent: 524-correction1. Status: Ready.
This is the routed bounded implementation continuation, not a second Review or
a repeated critique. Existing researched/approved actual-invocation requirement
is unchanged. Owner requires completion of decisive browser assertions before
publication; runtime validation exposed this directly coupled remaining gap.

## Executive Summary

Measure the original roleScreensView function-entry count with already enabled
precise coverage. A load-listener wrapper can install after the loader's promise
continuation and miss the earliest call. Preserve the adverse correction Review.

## User Decisions and Requirements

* Finish the owner-requested RV-001/RV-002 corrections and decisive browser proof.
* Preserve original evidence; no new script source, retry semantics or live work.

## Goals

Directly observe original-function invocation without event-listener races.

## Scope and Non-Goals

Only existing workspace_scripts_browser_check.py; no executable additions/removals.
No production changes, repeated RPI Review, repeated critique or scope expansion.

## Functional Requirements

Use the real original function's coverage entry count, not a wrapper. Require zero
calls after delayed settlement before revisit and one after a legitimate revisit.
Retain top-level evaluation, readiness, route/status/login and request assertions.

## Non-Functional Requirements

Python lines <=100; existing Ruff/mypy; real Chromium under authorized shared lock.

## Acceptance Criteria

Direct original-function zero/one counts pass all existing delayed scenarios.
Node/session/static regressions remain passing; precise coverage is enabled before
navigation and counts are sampled only at deterministic observed boundaries.

## Sources

Correction Review: .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-correction1-review.md, RV-001.
Existing research/critique remain valid; no new design choice or planning gap.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate original-function measurement

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Replace wrapper with actual function-entry coverage and validate

## Critique Disposition

No new critique: ordinary routed implementation of a localized Review finding,
using the original approved requirement and existing browser owner.

## Follow-Up Items

* Parent publication continuation and owner-pending live verification.

## Handoff

Final exact-head assessor must explicitly include this post-Review delta rather
than claiming the preserved Not accepted Review was re-run or changed to Pass.

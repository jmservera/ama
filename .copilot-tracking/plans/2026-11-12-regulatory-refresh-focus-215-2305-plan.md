---
title: Plan - restore keyboard focus after Refresh alerts (#215-R1)
description: Focused failing-first plan for one bounded focus-recovery defect
ms.date: 2026-11-12
ms.topic: reference
---

## Objective

Keep a keyboard user's place after "Refresh alerts" completes, without stealing focus. Research: [research](../research/2026-11-12-regulatory-refresh-focus-215-2305-research.md). Details: [details](../details/2026-11-12-regulatory-refresh-focus-215-2305-details.md).

## Tier

FOCUSED. Small local UI fix, no SQL, security, infrastructure, deployment, dependency or gate change. Checks: regulatory unit tests, the pinned-axe browser harness, `node --check`, ruff, mypy for the harness, run in the owned pip venv under `flock -n /tmp/ama-rpi-heavy.lock`. No complete gate, no hosted CI, no push.

## Phases

* [ ] Phase 1: Add the keyboard focus regression to the harness; run it on unchanged `chat.js` and capture the red result.
* [ ] Phase 2: Fix `chat.js` focus recovery; run green.
* [ ] Phase 3: One README description sentence; focused validation and the web guidelines review of changed files.
* [ ] Phase 4: Commit locally with the privacy-safe identity; one independent Review.

## Critique

Executed once, independently, before any edit: Revise, four findings, all accepted and applied in the details. See [critique](./critiques/2026-11-12-regulatory-refresh-focus-215-2305-plan-critique.md). Not rerun.

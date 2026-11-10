---
title: Issue 136 binding C1 details
description: Phase details for the bounded C1 on the public simulation startup binding
ms.date: 2026-11-10
---

## Phase 1 Research

Done: [research](../research/2026-11-10-issue-136-binding-c1-1110-research.md); owned venv with pip-installed core, agents and api; image ID confirmed; `src/` unchanged since the base.

## Phase 2 Plan

This plan, details and one critique. Critique findings are applied directly.

## Phase 3 Implement

* Capture red: run the old recipe with an unimportable module (expect no `/healthz`), and the old real-clock assertion with a stepped clock (expect nonzero `added`).
* Edit the recipe, the test and the README; run Bicep build and lint, policy, container contract, Hub and API regressions, the startup test, ruff isolated and mypy.
* Run scenarios fresh, reuse, key-only, corrupt, import-error and boundary determinism, each with full output and exit.
* Record the changes artifact.

## Phase 4 Review

One review after implementation, frozen after observation, then commit-complete with the actual HEAD and `verify`.

## Dependencies

Docker image reuse needs the non-queued heavy lock; busy blocks only the affected validation.

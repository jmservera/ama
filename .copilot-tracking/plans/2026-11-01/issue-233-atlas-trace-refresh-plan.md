---
title: Issue 233 plan, atlas trace refresh
ms.date: 2026-11-01
---

## Plan

1. Edit trace doc: scope paragraph and status cells (main vs open PR) per the research snapshot.
2. Add `registered_screens` and `status_drift` check in `atlas_screen_trace.py` (reads role-screens.js, compares `(main` labels); add tests outside the package.
3. Validate: core unit tests, ruff check, ruff format --check, mypy for `src/core`.
4. Commit, push, open PR with `Refs #233` listing unmet criteria.

## Critique (single pass)

Verdict: proceed. Risk: parsing JS with a regex is brittle; limit to `id: "..."` lines inside role-screens.js and skip the check with a clear gap if the file is absent. Scope kept to the drift check; no new screens.

## Decisions

* Issue not closed: criteria 1, 2, 4, 5, 6 lack full proof.

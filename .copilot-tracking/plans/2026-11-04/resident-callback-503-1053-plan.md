---
title: Plan - resident callback 503 (#1053)
ms.date: 2026-11-04
---

## Stacked slices

* Slice 1 (this PR): honest page when no agenda is configured (option B).
* Slice 2 (later, gated): connect a synthetic agenda in the demo composition (infra/deployment; coordinator gate).

## Slice 1 checklist

* [x] `view_for` adds `callbacks_available`.
* [x] Chat `appointments` returns a not-connected answer with the manual route and no `action`/`callback_search` when no agenda.
* [x] `demo.js`/`index.html`: lede, optional link, form, unavailable text and nav label depend on `callbacks_available`.
* [x] Tests for both states; focused tests, ruff, mypy.

Critique (one pass, self): signed-out lede must be true in both states, so it now says only that records are read-only. Sensors untouched (phase 2). Human approval and consent boundaries unchanged; manual route text retained.

---
title: Issue 233 changes, atlas trace refresh
ms.date: 2026-11-01
---

## Changes

* `docs/reference/research/ux/atlas-screen-trace.md`: status cells now say main (#652, #653, #654, #655, #657) or unmerged (PR 656, 662); scope paragraph updated.
* `src/core/.../atlas_screen_trace.py`: `registered_screens`, `status_drift`, optional `role_screens_js` argument to `check`, `ROLE_SCREENS` path.
* `src/core/tests/test_atlas_screen_trace.py`: two drift tests.

## Validation (focused tier)

* `python -m unittest tests.test_atlas_screen_trace`: 13 passed.
* `ruff check`, `ruff format --check`, `mypy src` in `src/core`: clean after formatting.
* No divergence from plan. No heavy gate; CI is the evidence.

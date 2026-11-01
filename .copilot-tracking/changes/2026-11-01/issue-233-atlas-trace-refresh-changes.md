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
* No divergence from plan. CI is not a substitute for the local RPI gate.

## Correction cycle 1 (review threads on PR 713)

* `status_drift` now applies each `(main` / `(unmerged` status only to the screens named before it, so mixed-status cells no longer false-fail; new test added (15 pass).
* Index row in `docs/reference/README.md` and a dated `docs/reference/log.md` entry now match the nine-of-twelve status.
* Merge of origin/main was a no-op (already up to date).
* The complete local gate (`tools/rpi-checks.py --all`) runs on the committed head with an external receipt; its actual outcome is reported on the PR, not stored here, because any later commit would invalidate it. If prerequisites (SQL, browser, scanner) are missing, publication is recorded as blocked.

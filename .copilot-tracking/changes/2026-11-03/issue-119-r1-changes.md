---
title: Issue 119 r1 changes
ms.date: 2026-11-03
---

## Changes

* `src/api/src/zava_forward/api/web/app.js`: tile failure note.
* `src/api/tests/test_ui_support.py`: static test.
* `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`: protocol and log.

## Validation run

* `test_ui_support.py` via unittest discover with PYTHONPATH to this worktree's src: 11 tests OK (a logged law-store traceback is expected noise).
* `test_accessibility_baseline.py`, `test_map_fullscreen.py`: 8 tests OK each.
* ruff and mypy (cache /tmp/mypy-119) on the changed test: clean. `node --check` on app.js: OK.

## Not run

Gate, full suites, benchmarks, real-browser or screen-reader runs. web-design-guidelines fetched (first 8000 characters of the rules); the changed lines were read against the accessibility and copy rules. The installed `zava_forward` packages point at another worktree, so PYTHONPATH was used for this run only.

## Divergences

None. Plan critique amendment (no clearing on tile load) applied before commit.

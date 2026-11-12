---
title: Details - restore keyboard focus after Refresh alerts (#215-R1)
description: Phase detail for the focused focus-recovery change
ms.date: 2026-11-12
ms.topic: reference
---

## Phase 1: harness regression (red first)

In `regulatory_ux_check.py` add `check_refresh_focus(page, expect, fixture)` called once after the existing source-changed refresh step; it adds no scan, so the 21 scan count and later state are unchanged. Keyboard only, each case checked after the `AsyncAction` wrapper settles (`aria-busy` removed):

* Initial load never takes focus: before pressing, the focused element is not the button.
* Success: focus the button, press Enter, wait for the completed status, expect focus on the button.
* API error: `fixture.app.law = None`, Enter, expect the unknown-coverage status and focus on the button; restore in `finally`.
* Law-store-unloaded branch: set the cached `me.services.law_alerts` false, Enter, expect that status and focus on the button; restore in `finally`.
* No stealing: capture (do not continue) the `/api/law/alerts` route, Enter, assert the request and loading state, move focus to the plain-language toggle, continue the captured route, wait for the completed status, expect focus still on the toggle. Repeat with a pointer press on non-focusable heading text and expect focus not returned to the button. Unroute in `finally`.

## Phase 2: fix

In `regulatoryAlertsPanel` `load()`: capture `held = document.activeElement === refresh`; add capture-phase `focusin` and `pointerdown` listeners that set `moved` for any target other than the button; in the sync law-store branch `await Promise.resolve()` while still disabled (so `AsyncAction` never owns the disabled state); in a single `finally` re-enable, remove listeners, and call `refresh.focus()` only when `held && !moved` and `document.activeElement` is `body`.

## Phase 3

One sentence in the existing keyboard/plain-mode harness paragraph of `src/api/README.md`, keeping "not WCAG conformance". Run the five regulatory unit modules, the harness with pinned axe 4.10.3 (sha256 `880970c0...a68bb`), `node --check`, `ruff check/format --check`, mypy on the harness.

## Non-goals

No ticks, no staff trial, no model/cloud call, no `app.js`, `style.css` or other source, no new test file.

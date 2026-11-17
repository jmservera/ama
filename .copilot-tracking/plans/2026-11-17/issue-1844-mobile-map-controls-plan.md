---
title: Issue 1844 plan
ms.date: 2026-11-17
---

## Plan

* [x] Phase 1: add failing-first regression to `map_fullscreen_browser_check.py` (4 viewports x 2 tile states, 9-point hit tests for 3 markers and 2 zoom controls, summary/map overlap, overflow, attribution, Escape, Close, open another home, served-byte hash of `app.js` and `style.css`).
* [x] Phase 2: one-line CSS: at max-width 600px the home card is static below the map.
* [x] Phase 3: run targeted checks and the Core integrity tests.

Details: [issue-1844-mobile-map-controls-details.md](../../details/2026-11-17/issue-1844-mobile-map-controls-details.md).

## Critique

One critique pass, self-performed: the static-card option is the smallest change and matches the expanded dialog. Rejected: moving the card into a bottom sheet (redesign) and `inert` on covered controls (hides controls, keeps the covering problem). No conflict with confirmed decisions.

---
title: Issue 1844 research, mobile map controls hidden by home summary
ms.date: 2026-11-17
---

## Scope

Issue #1844: at 320 and 390 px widths the open home summary (`.map-home-card`, absolutely positioned over `.map-stage`) covers markers and zoom controls that stay focusable. Base origin/main f1df574bba2b94cd83bb2a783079ec94cd584c90 (the brief overrides the issue's parent-topic base). Tier FOCUSED: CSS and browser check only; no SQL, authorization, infrastructure, deployment or dependency change.

## Research disposition

Executed. Process note: the opening file and `research-open` witness preceded search; the research reading and the first test edit were interleaved, and the plan, details and changes files were written after the implementation, not before it (see the changes file).

## Findings

* `style.css` `.map-home-card` is `position:absolute` over the map stage. Inside the expanded dialog `.map-dialog .map-home-card` is already `position:static` in the sidebar (prior art).
* The card is the last child of `.map-stage`, after the Leaflet element, so a static card sits directly below the map with no DOM change; semantics, Escape and Close focus return in `app.js` are untouched.
* The existing check `src/api/checks/map_fullscreen_browser_check.py` is the employee-map browser check. It is not the workbench recipe, so `scenario-manifest.json` is not affected; the Core manifest and needs-inventory tests were still run.
* Existing 320/390 px assertions only checked overflow and Close in viewport; none tested coverage.
* Base flake: `filter label and focus fit at 390x568` in `check_expanded_filters` failed in 1 of 4 runs on unchanged code.

## Planning Readiness

Ready.

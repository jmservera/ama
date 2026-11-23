---
title: Epic 149 law viewer reflow defect and fix (Refs #149)
description: Measured 320 CSS pixel reflow failure of provision text on the law viewer page, the scoped style fix, its regression test and the per-criterion status of the UX epic for the synthetic demo
ms.date: 2026-11-23
ms.topic: reference
---

Refs #149. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18. This note ticks nothing on the epic. A web file under `src/api` changed, so the tier classification is full; only targeted local checks ran and the complete gate stays with the coordinator.

## Finding

`law.html` renders each provision as a `pre` element (`src/api/src/zava_forward/api/web/law.js`). The style sheet wrapped `pre` only inside `.case-tab-panel`, so the law viewer kept the browser default `white-space: pre`. A long provision line therefore widened the whole page.

Measured with Playwright Chromium at 320x640 (1280 px at 400 percent zoom), `/api/law/*` routes stubbed with one provision that has long lines and a long URL, static files served on a throwaway local port:

| State | `documentElement.scrollWidth` | `clientWidth` | `pre` computed `white-space` |
| --- | --- | --- | --- |
| Before | 2772 | 320 | `pre` |
| After | 320 | 320 | `pre-wrap` |

Screenshots: `.copilot-tracking/evidence/2026-11-23/issue-149-live-r2/before.png` and `after.png`. The result concerns WCAG 2.2 SC 1.4.10 (Reflow) for this one screen; it is engineering evidence, not conformance.

## Fix and regression test

* `style.css`: the existing `.case-tab-panel pre` rule now also matches `#law-out pre`. The technical-record `pre` elements in `assistants.js` are unchanged because they are focusable scroll regions.
* `src/api/tests/test_law_viewer_reflow.py`: fails without the rule (checked by reverting the style change), passes with it.

Local checks: the new test, `test_accessibility_baseline`, `test_content_standard`, `test_epic149_landmarks_skip_link_focus_order`, `test_design_system` and `test_static_assets` (80 tests OK); `ruff check`, `ruff format --check` on the new test; `mypy` in `src/api` clean.

## Live Azure

Not used for this defect. The deployed `/api/law/*` answers 503 because the law store is not configured (recorded 2026-11-18), so a provision cannot be rendered there; the browser measurement above is stubbed-API evidence and is labelled so.

## Epic criteria

| Criterion | Status for the demo |
| --- | --- |
| #440 stabilization checkpoint | Unproven: #440 triage and owner decisions are not recorded as complete; owner-gated |
| Child features are accepted | Unproven: all sub-issues (#150 to #156, #225 to #233) read CLOSED on 2026-11-23, but acceptance is an owner decision and a closed issue is not acceptance |
| Accessibility, content and usability evidence recorded | Already ticked; the 80 local tests above ran green |
| Design artefacts traceable | Already ticked; not re-executed |

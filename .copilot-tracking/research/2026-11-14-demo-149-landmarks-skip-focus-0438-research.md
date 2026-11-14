---
title: Epic 149 landmarks, skip link and focus order research
ms.date: 2026-11-14
---

Task: `demo-149-landmarks-skip-focus-0438` (Refs #149). Stacked child of `test/demo-149-journey-requirement-trace-0430` at `9340dd757`. Research disposition: executed. Planning Readiness: Ready. Tier: focused (one new test under `src/api/tests/`).

## Evidence

* The API is a standard-library `ThreadingHTTPServer` (`server.py`), not ASGI, so there is no `TestClient`. Existing served tests start a local server; the new test does the same.
* Primary routes: `/` (welcome.html), `/app` (index.html) and `/law.html`. All declare `lang="en-GB"` and distinct titles.
* Only `/app` has a skip link (`#app`, `<main id="app" tabindex="-1">`) and a named `nav`. `/` and `/law.html` have header and main but no skip link or nav; recorded as shrink-only gaps.
* CSS: `:focus-visible` outline plus box-shadow, no outline removal; `--motion` zeroed and spinner animations and widget transitions disabled under `prefers-reduced-motion`; two `forced-colors` blocks use system colours.

## Boundaries

Source and served-HTML engineering evidence. Not WCAG conformance, assistive-technology or rendered focus-order acceptance.

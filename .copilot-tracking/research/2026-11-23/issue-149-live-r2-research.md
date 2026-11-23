---
title: Issue 149 live r2 research
ms.date: 2026-11-23
---

# Research opened

Epic #149 (UX design, accessibility, usability). Prior live worker (2026-11-19) wrote only a docs note. This task picks a new code angle.

Unticked criteria: (1) #440 stabilization checkpoint, owner-gated; (2) child features accepted (all sub-issues #150-#156, #225-#233 now CLOSED per `gh api .../sub_issues`; acceptance is an owner call). Owner-only items are skipped.

Planning Readiness: Ready once findings below are recorded. Disposition: executed.

## Findings (2026-11-23 19:11Z)

* Earlier angles (reduced motion, heading hierarchy, landmarks, form-error association, manual fallback, tab titles, autocomplete) already have tests on main; probed and skipped.
* New angle: `law.html` renders each provision with `el("pre", p.text)` (`web/law.js:58`). `style.css` only styles `pre` inside `.case-tab-panel` (line 415) and `.pre`; the law viewer `#law-out pre` keeps the browser default `white-space: pre`.
* Browser proof (Playwright Chromium, 320x640 viewport = 1280 px at 400 percent zoom, API routes stubbed with a long provision, static server on a throwaway local port): `documentElement.scrollWidth` 2772 against `clientWidth` 320, computed `white-space: pre`. This is a WCAG 2.2 SC 1.4.10 Reflow failure on a read-only reference screen. Screenshot: `.copilot-tracking/evidence/2026-11-23/issue-149-live-r2/before.png`.
* Live Azure not used: the deployed `/api/law/*` returns 503 (law store not configured, per 2026-11-18 notes), so the screen cannot render a provision there. Stated, not worked around.
* No existing test covers reflow of `law.html` provision text (tests naming `law.html`: baseline, content standard, landmarks, static assets).
* Planning Readiness: Ready. Fix: scoped CSS rule `#law-out pre{white-space:pre-wrap;overflow-wrap:anywhere}` plus a regression test.

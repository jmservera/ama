---
title: Issue 232 resident engagement screens accessibility research
ms.date: 2026-11-13
---

## Scope

Issue #232 criterion 4 only: "Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation". Screens: `resident-choice` (Resident choice and update queue) and `resident-service-issues` (Resident service issue queue) in `src/api/src/zava_forward/api/web/role-screens.js`. Out of scope: regulatory alert and home chat modules (#215), `infra/`, ranking archive. Tier: Focused. Base `origin/main` `36a2a57335dc95273292d6fda54fe60ff9f9b4f9`.

## Disposition

Research disposition: executed (builds on the earlier audit `.copilot-tracking/changes/2026-11-13/232-housing-screen-a11y-audit-1905-changes.md`, which found all existing automated checks passing and changed nothing). Planning Readiness: Ready.

## Reading done

Case study original and addendum, knowledge base index, memory, design system, WCAG baseline, content standard and the web-design-guidelines skill, with the guideline source fetched fresh on 2026-11-13 from the skill's URL (retrieval succeeded, 8,055 bytes).

## Evidence found

Rendered probe (throwaway Playwright script, Chromium 156, synthetic data, 1280 and 320 px, queue and selected-home states, axe 4.10.3 with wcag2a/2aa/21a/21aa/22aa plus best-practice tags):

* Axe: no violations in all eight state/width combinations. `color-contrast` incomplete at 320 px only; `elementFromPoint` showed no real overlap, so the incomplete is an axe background-resolution limit.
* Landmarks, skip link ("Skip to main content" to `#app`), focus moved to `main`, no duplicate ids, every table captioned with `th scope="col"`, labelled focusable table regions, no write or contact controls.
* Defect D1 (WCAG 1.3.1, H63): every resident-screen table had zero row headers; the first column (home, measure, request, issue) was a `td`.
* Defect D2 (textual state meaning): the choice screen's service request table showed a bare status word, while the service issue screen states status and meaning.
* Coverage gaps: axe ran only on the selected-home state; Tab reach at 320 px was asserted only for the 231p/231qp stories; no rendered row-header assertion.
* Observed, not changed: panels under "Selected home" are flat `h2` siblings (no skipped level) in a shared shell used by other roles; the long download note on the choice screen is dense. Both are outside this change.

## Limits

Synthetic constructed data, Chromium only, no assistive technology. Axe and DOM checks are automated WCAG evidence, not live assistive-technology user evaluation. No `aria-invalid` site or scenario recipe is touched, so `test_accessibility_baseline.py` counts and `scenario-manifest.json` SHA need no update (verified by running `test_accessibility_baseline`, `test_scenario_manifest`, `test_needs_inventory`).

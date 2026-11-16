---
title: "Issue 1297 320px summary-bottom regression plan"
ms.date: 2026-11-16
---

## Objective

Fix the independent-review blocking finding: restore the 320x800 `.case-summary` bottom limit to 1600 (it was relaxed to 1700 in 2e9bd4ab6 to pass an observed 1637px layout) and compact the narrow top navigation just enough to meet it with keyboard and touch accessibility intact. Tier: FULL (gate-tool and SQL-sensitive change with a web test correction). No waiver, no threshold change, no unrelated UI change.

Research: `.copilot-tracking/research/2026-11-16/issue-1297-mobile-regression-research.md`. Details: `.copilot-tracking/details/2026-11-16/issue-1297-mobile-regression-details.md`. Critique: `.copilot-tracking/critiques/2026-11-16/issue-1297-mobile-regression-critique.md`.

## Phases

* [ ] Phase 1: record the independent finding and the pre-fix reproduction (1637.41 > 1600) in the changes artifact, then record `implement-start`.
* [ ] Phase 2: restore `bottom <= 1600` in `src/api/checks/case_journey_browser_check.py`, remove the "about 490px" waiver comment, and add 320px nav link target assertions (each link at least 24px wide and 40px tall, one tab-order stop per link left to the browser).
* [ ] Phase 3: in `style.css`, inside the existing `@media(max-width:600px)` rule, set `#nav` column gap and `#nav a` horizontal padding to `var(--sp-1)`.
* [ ] Phase 4: add a CSS regression test in `src/api/tests/test_design_system.py` for the narrow nav compaction and for the preserved 1.5rem screen-evidence link rule; run it, the real journey check, targeted tests and lint.
* [ ] Phase 5: self-review, commit, then a FRESH full gate only if the heavy lock is free; otherwise return a frozen correction and named handoff.

## Gates

* The limit stays 1600. If the layout cannot meet it without changing design acceptance, stop with a blocked handoff.
* Preserve the screen-evidence link target, focus ring, `touch-action`, reduced-motion and forced-colours rules, SQL skip and clean-input guards.
* Do not touch `/tmp/ama-gate-1297-20261116T105339Z`, `/tmp/rpi-1297-pyc-full-20261116T1530Z` (stale after this change, kept as evidence) or any witness log. Do not queue for or compete with a held heavy lock.

---
title: "Issue 1297 320px summary-bottom regression research"
ms.date: 2026-11-16
---

## Status

Research disposition: executed. Planning Readiness: Ready. Source head 132f0b1ca1a229556f7c48a5b9e64f63a556f5de, origin/main 18d3de459f20018e91fab3af87ab0d89123661c6. Earlier #1297 RPI artifacts, the failed receipt `/tmp/ama-gate-1297-20261116T105339Z/receipt.json`, the old-head full receipt `/tmp/rpi-1297-pyc-full-20261116T1530Z/receipt.json` and all witness logs are preserved and only referenced.

## Independent review finding

Blocking, medium, functional: `src/api/checks/case_journey_browser_check.py:1546` relaxed the 320x800 acceptance limit `.case-summary` bottom from 1600 to 1700 (commit 2e9bd4ab6) to pass an observed 1637px layout. That changes design acceptance instead of fixing the layout. The threshold must stay 1600 and the layout must be compacted.

## Findings

* Reproduced on this head: the real case journey check with only the limit restored to 1600 (scratch copy in `/tmp/repro1297`, repository untouched) fails with `320x800 summary within one viewport scroll (1637.40625)`.
* Layout at the failing moment (320px, case ZF-4): `.top` is 487px tall. The ten `#nav` links wrap to eight rows (42px each) starting at y=126, because each link has `var(--sp-2)` horizontal padding and the nav has a 1rem column gap, so "Overview" and "Funding" and most other links sit alone on a row. `.workspace-status` follows at y=499 and `.case-summary` starts at 883 and is 755px tall (6 stacked values).
* Cause of the 37px overrun: the 320px navigation wrapping, not summary content. Commit 3cef6982d (the evidence-panel link target) is not involved.
* Smallest compaction: at max-width 600px reduce the nav column gap and link horizontal padding to `var(--sp-1)`, so more links share a row. Link height (`min-height:2.5rem`) is unchanged, so touch targets stay at least 40px tall and far above the 24px WCAG 2.2 target minimum; focus ring, `touch-action`, aria-current underline, wrapping and forced-colours rules are untouched.
* Not in scope: summary content, the screen-evidence link rule (`style.css`, #1297 3cef6982d), design tokens, desktop layout, SQL skip and clean-input guards.

## Guideline basis

Current Vercel Web Interface Guidelines (fetched 2026-11-16): keep visible focus, `touch-action: manipulation`, avoid unwanted overflow, flex over JS measurement. `redesign-existing-projects` applied as a targeted fix only; Fluent 2 tokens (`--sp-*`), WCAG baseline and reduced-motion behaviour retained.

## Residuals

Scratch files in `/tmp/repro1297` left in place. The heavy lock was not observed as held (`lsof /tmp/ama-rpi-heavy.lock` empty) at 16:2xZ; recheck before the gate.

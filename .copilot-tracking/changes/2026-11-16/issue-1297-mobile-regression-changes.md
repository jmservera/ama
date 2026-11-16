---
title: "Issue 1297 320px summary-bottom regression changes"
ms.date: 2026-11-16
---

## Independent review finding (recorded before source edit)

An independent exact-head reviewer found a blocking medium functional regression at `src/api/checks/case_journey_browser_check.py:1546`: commit 2e9bd4ab6 relaxed the 320x800 `.case-summary` bottom limit from 1600 to 1700 to pass an observed 1637px layout. Owner direction: restore 1600, compact the narrow navigation, do not waive.

## Pre-fix reproduction

At head 132f0b1ca1a229556f7c48a5b9e64f63a556f5de, a scratch copy of the journey check with only the limit restored to 1600 (`/tmp/repro1297/cj1600.py`) fails: `AssertionError: 320x800 summary within one viewport scroll (1637.40625)`. Diagnosis: `.top` is 487px tall; ten nav links wrap to eight 42px rows; summary starts at 883px.

## Changes

* `src/api/src/zava_forward/api/web/style.css`: in the existing `@media(max-width:600px)` rule, added `#nav{column-gap:var(--sp-1)}#nav a{padding-inline:var(--sp-1)}`. Link `min-height:2.5rem`, focus ring, `touch-action`, forced-colours and the `.screen-evidence p>a:only-child` 1.5rem target are unchanged.
* `src/api/checks/case_journey_browser_check.py`: restored `bottom <= 1600` (waiver comment removed) and added a 320px assertion that every `#nav a` is at least 24px wide and 40px tall.
* `src/api/tests/test_design_system.py`: `test_narrow_navigation_is_compact_and_keeps_touch_targets` (failed before the CSS change, passes after).

## Validation

* Unit regression failed before the CSS edit, passes after; `tests.test_design_system` 10 OK.
* Real case journey check (axe 4.10.3 SHA-verified, all 87 scans, exit 0) at the restored 1600 limit: `320x800 summary within one viewport scroll (1549.40625)` and the nav target check pass. Pre-fix the same limit measured 1637.40625 and failed.
* ruff format and check clean on the changed Python files.
* No SQL skip, clean-input, gate runner or screen-evidence code was changed. The limit was not relaxed.

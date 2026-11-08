---
title: Issue 1214 phase details
description: Phase details for the 320px nav row-gap correction
ms.date: 2026-11-05
ms.topic: reference
---

## Context

Evidence IDs refer to the research artifact (C1 to C8). Task ID issue1214-mobile-summary-gate.

## P01 Apply nav row-gap correction

* P01-T01 (C3, C6, C7): in `src/api/src/zava_forward/api/web/style.css` add `.top nav{row-gap:.125rem}` inside the existing `@media(max-width:600px)` block at style.css:317. Specificity `.top nav` (0,1,1) beats `nav{gap:1rem}`; row-gap only, so column gap stays 1rem. Literal `.125rem` is used because no local XXS spacing token exists; adding a token for one use is rejected as larger than needed.
  * Done when: the rule is the only functional diff; no HTML, JS or check change.
* P01-T02 (web guidelines): refetch the guidelines source, review changed `style.css` lines, report `file:line` findings. Confirm focus styles, touch-action, reduced motion untouched.
* Cache impact (PC-004): `static_assets.py` hashes content and rewrites `?v=`; no manual bump.
* Stop rule (PC-005): if bottom still exceeds 1600, stop, record adverse result, do not alter the bound or hide content.
* PC-002: screenshot a focused nav link at 320 and 390 and confirm the focus ring is visible.

## P02 Focused validation

* P02-T01: `run-browser.sh` (heavy-lock nonblocking, candidate PYTHONPATH asserted, PYTHONDONTWRITEBYTECODE, external output) against the candidate; record exit code and dump geometry at 320. The geometry dump hook is extended to record nav and summary geometry at 390 and 1280 (after the existing reflow loop), first run before the CSS edit on the unchanged candidate to capture the 390/1280 baseline, then after the edit. The 320 baseline is already in the research artifact.
  * Done when: process exit 0; bound unchanged.
* P02-T02: unit tests from `src/api` with `PYTHONPATH` candidate paths and `-B`; then `python3 tools/rpi-checks.py --changed` only if it does not create source bytecode or touch the shared environment; otherwise record the blocker. Done when exit codes are recorded.
* P02-T03: record the root-cause finding in the changes record. No knowledge-base page expected; if one is changed, update `docs/reference/README.md` and `log.md`.

## Test Ownership

Coverage owner: existing `checks/case_journey_browser_check.py:1526` assertion (semantic layout contract). Removals: none. Additions: none. Canonical target: `style.css`; no generated targets. Validation evidence: external run logs plus changes record.

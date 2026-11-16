---
title: "Issue 1297 320px summary-bottom regression review"
ms.date: 2026-11-16
---

## Execution and outcome

Review executed once by the RPI worker over the uncommitted diff at head 132f0b1ca1a229556f7c48a5b9e64f63a556f5de (style.css, case_journey_browser_check.py, test_design_system.py). Outcome: conformant for the reviewed boundary. This is self-review and does not replace the coordinator's independent exact-head review, human approval or hosted CI.

## Independent review finding

Blocking medium finding at `src/api/checks/case_journey_browser_check.py:1546` (limit relaxed 1600 to 1700 to pass 1637px): resolved by restoring 1600 and compacting the 320px navigation. The limit is not waived or changed from its original value; the real journey measures 1549.41px (was 1637.41).

## Checks

* Reproduced before the fix (1637.41 > 1600); passes after with the full journey (axe 4.10.3, exit 0).
* Accessibility: link height still `min-height:2.5rem`, new assertion requires at least 24x40 px per nav link at 320px; focus ring, `touch-action`, reduced-motion, forced-colours, aria-current and the screen-evidence 1.5rem link target untouched; change confined to max-width 600px, so desktop and tablet are unchanged. Fluent `--sp-1` token used, no redesign.
* Web guidelines (fetched 2026-11-16): no `transition: all`, no outline removal, no new JS layout measurement in product code; the measurement exists only in the browser check.
* SQL skip, clean-input and gate runner code unchanged.
* Tests: `test_design_system` 10 OK (new test failed before CSS edit); 70 related api UX tests OK; ruff clean.

## Findings routed to later work

* Hosted CI and the fresh full gate on the committed head are pending; the old full receipt `/tmp/rpi-1297-pyc-full-20261116T1530Z/receipt.json` is stale for this head and retained as evidence.
* Real-device 320px acceptance remains manual per the design-system record.
* Prior follow-up (wire ZF_RESIDENT_MSSQL classes into the SQL group) is unchanged.

---
title: Issue 80 capacity browser check time-status expectation, review
description: Native review (not independent) of the C1 correction at the working tree before commit
ms.date: 2026-11-10
---

Review executed once after implement-done; native author review, explicitly not independent. Boundary: the `capacity_browser_check.py` hunk and the focused validation in the [changes record](../../changes/2026-11-10/issue-80-capacity-c1-1110-changes.md). Outcome: **OPEN FINDINGS** (the targeted correction is verified; the whole check still fails for a different, unrelated reason).

## Findings

* C1-R1 (Medium, open): whole `capacity_browser_check --axe` still exits 1 in `browser-run2.log` at `capacity_browser_check.py:517`, `Unchecked manager route '#/aftercare'`. The empty-capacity zero-anchor assertion and later scenarios were not reached, so withholding on empty is still verified by source reading only. Original R1 disposition: its `#/time` cause is resolved (the corrected assertion passed at runtime), its consequence (empty-state not reached) is NOT resolved. Publication stays blocked pending a Root-admitted `MANAGER_ROUTES` alignment for `#/aftercare` (new nav from #1400, source-read attribution) and one re-run. Not repaired here by instruction.
* C1-R2 (Info, closed): the `#/time` expectation asserts the real rendered copy (exact for enabled and for the maintained switched-off fixture; reason sentence plus `Owner:` and `Next action:` for other blocked states), not "some message", and does not read the server `reason`. Run 2 shows `Manager route #/time: PASS`.
* C1-R3 (Low): the exact switched-off sentence duplicates the string in `timecapture.js`; a future copy change will need the check updated, as happened here. Accepted; `test_timecapture_copy.py` owns the copy contract.
* C1-R4 (Low): the third branch (other blocked states) is not exercised by the maintained fixture; it is shape-only and unverified at runtime.
* C1-R5 (Info): original R2 to R5 are unchanged and accepted by Root as bounded limitations (single package, single manager role, distinct anchor names, source-only attribution to #1343). C2, C4 and #73 stay open; no source or web file other than the checker changed.

## Evidence boundary

Distinguish: observed rendered DOM, keyboard downloads, axe 0 violations (seeded state), and `#/time` PASS; not available: screenshot or layout review, manual screen-reader testing, deployed or user acceptance, empty-state rendering, conformance. No fresh web-guidelines review was performed (no web file edited).

## Ranked follow-ups

1. Admit a minimal `MANAGER_ROUTES` entry for `#/aftercare` (check-only) and one re-run to reach the empty assertion. Highest value, smallest.
2. Independent exact-head review after that run.

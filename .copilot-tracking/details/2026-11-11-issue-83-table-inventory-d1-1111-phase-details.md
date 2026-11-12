---
title: Issue 83 table inventory D1 phase details
ms.date: 2026-11-11
task_id: issue-83-table-inventory-d1-1111
---

## P01 Audit

* Keep `.copilot-tracking/reviews/logs/2026-11-11/issue-83-table-inventory-d1-1111-pre-change.txt` (failing output at dd3c).
* Confirm 13 regex-matched sites, one added by dd3c in `app.js` `handoffWaitingView`: caption first child, `th scope="col"` x7, `th scope="row"` case link, named `table-scroll` region with `tabindex="0"`, global `:focus-visible`, text-only status and reasons.

## P02 Test metadata

* File `src/api/tests/test_accessibility_baseline.py`, test `test_every_table_has_a_caption_and_column_headers`: change `assertEqual(tables, 12, ...)` to 13; extend the comment with the 2026-11-11 handoff waiting table. Nothing else in the test changes.

## P03 Record

* `docs/reference/research/ux/wcag-conformance-baseline.md` Tables row: append a dated 2026-11-11 (#83, refs) entry: inventory now 13, source audit of the waiting table, constructed-browser tests are rendering and failure behaviour only, not tested: screen-reader, reflow at 320 px, zoom, AT, manual acceptance; no conformance claim and no approved OD-09 times. Keep the 11 and 12 observations unchanged.
* `docs/reference/README.md`: update the baseline entry summary and date column.
* `docs/reference/log.md`: append one entry, no earlier entry rewritten.

## P04 Validation

Per plan. Record commands, head, exits, skips. Prove product bytes with `git diff --name-only dd3c32910 HEAD` listing only test, docs and `.copilot-tracking` paths, and `git diff dd3c32910 -- src/api/src` empty.

## P05 Review

One original Review by independent subagent lens plus root reconciliation; findings routed, no further source change.

---
title: Issue 133 aftercare C3 table audit research
description: Research for corrective cycle C3 (3 of 5), CI failure of the table inventory (Refs #133)
ms.date: 2026-11-10
---

Phase activation Research: 2026-11-10T00:05:44Z (date -u). Refs #133. Parent task: C2 (state `.copilot-tracking/rpi-sessions/2026-11-09/assisted-aftercare-133-c2-state.json`). C2, partial Stage A review, chronology and 6000-character guideline qualifications are immutable. Full fresh guidelines fetched 2026-11-10T00:05Z, 8055 bytes, identical to the coordinator copy.

## Reproduction (actual head b1b0d6c, worktree issue-133-aftercare-1109, branch feat/demo-assisted-aftercare-133-1109)

* `python -m unittest tests.test_accessibility_baseline` in `src/api`: 12 tests, 1 failure, `12 != 11`, at `test_accessibility_baseline.py:130`, matching the CI report (exit 1). Log `/tmp/issue133-c3/logs/c3-red-baseline.log`.
* Cause: the unwired `aftercare.js` added a script-built table (`aftercare.js:188`). The inventory test counts `h("table", {}` sites and requires a caption within 60 characters.

## Audit of the new table (aftercare.js `aftercareEvaluatorView`)

* Caption: `h("caption", {}, "Observed baseline and late means, with concerns by home")`, first child, visible, names the table. Pass.
* Headers: six `th scope="col"` in `thead`; first body cell of each row is `th scope="row"` (home reference); other cells are `td`. No bare `th`. Pass.
* Content: `Unknown` text for missing comparison, numeric values with a unit; no colour-only status. Pass.
* Responsive behaviour: six columns, global `table{width:100%}`, and the table is NOT inside a `.table-scroll` region. Other wide tables use `div.table-scroll[role=region][tabindex=0][aria-label]` (`app.js:2081,2173,2177`, `ops.js:320`; CSS `.table-scroll{max-width:100%;overflow-x:auto}`). At narrow widths (WCAG 1.4.10 reflow) the page could scroll sideways or clip. Small defect: wrap it as the existing pattern does.
* Not tested: real browser reflow at 320 px, screen-reader table navigation, served page. Static source and a DOM-shape test only.

## Record

`docs/reference/research/ux/wcag-conformance-baseline.md` Tables row says "all 11 script-built workbench tables" (2026-11-04, #151); the test is its check. The record needs a dated note that the inventory is 12 with the aftercare evaluator table, still partial, no conformance claim. Log: append an entry to `docs/reference/log.md`; the index is unchanged (no file added or moved).

## Planning readiness: Ready.

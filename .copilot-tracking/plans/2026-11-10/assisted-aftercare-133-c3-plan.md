---
title: Issue 133 aftercare C3 plan and details
description: Plan and phase details for corrective cycle C3 (Refs #133)
ms.date: 2026-11-10
---

Plan written after the 2026-11-10T00:06:08Z readback and before the one critique; Implement activated 2026-11-10T00:07:25Z (date -u). The first draft estimated the plan time; this is the corrected record. Critique findings C3-01..03 are applied here: region label equals caption, run the whole screen module (13 tests with the new one), and the record note separates the static guard from the manual audit. Scope: audit the aftercare table, fix the one small defect, update inventory test and record. No server, app.js, role-screens, store, procurement or sqlstore edits.

## Phases

1. Red: tighten `test_every_table_has_a_caption_and_column_headers` (count 12) and add a DOM regression in `src/api/tests/test_aftercare_screen.py` that the evaluator table sits inside a `table-scroll` region with `tabindex` 0, `role` region and an `aria-label`, keeps a first-child caption, `th scope=col` headers and `th scope=row` first cells. The DOM test must fail before the JS fix.
2. Green: wrap the table in `aftercare.js` with `h("div", {class: "table-scroll", role: "region", tabindex: "0", "aria-label": <caption text>}, table)`. Markup otherwise preserved.
3. Record: update the Tables row of the WCAG baseline record with a dated C3 note (12 tables, aftercare evaluator table audited statically, still partial). Append a log entry (no earlier rewrite).
4. Validate: whole accessibility-baseline module, 12 screen and 65 core tests, content-standard and static-asset tests, API mypy, ruff format/check, `node --check`, in a worktree-owned venv with import paths proved. No SQL, browser, full gate, model, network.
5. Review once, clean freeze, handoff to coordinator files.

## Details

* Aria-label reuses the caption text so the region name equals the table name; the caption stays inside the table.
* No new CSS: `.table-scroll` exists.
* Not claimed: WCAG, assistive-technology or human acceptance, served or browser reflow. Fluent 2 unchanged.
* Divergence rule: if the shared served DOM is needed, one non-queued lock admission; otherwise record pending.

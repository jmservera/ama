---
title: Issue 151 WCAG baseline refresh research
ms.date: 2026-11-17
---

## Task

Issue #151, refresh the counted facts in `docs/reference/research/ux/wcag-conformance-baseline.md` from the existing counted guard tests. Docs only, demo-first, desktop-only. Tier FOCUSED. Refs #151.

## Research disposition

Executed. Planning Readiness: pending measurement (see below).

## Plan of measurement

* Run `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` sequentially.
* Count served assets, table builders and aria-invalid sites from source and compare to the record (22 assets, 15 tables, 9 aria-invalid sites).

## Measurements (worktree, base eb51af5c9)

* `test_accessibility_baseline` plus `test_wcag_workbench_baseline_151`: 20 tests OK.
* `unittest discover -s tests -p "*wcag*.py"`: 150 tests OK; `"*a11y*.py"`: 16 OK; `"*accessib*.py"`: 35 OK (patterns overlap, not additive).
* Source counts match the record: 22 web assets (16 js, 6 html/css), 15 table builders, 9 `aria-invalid` sites, 2 fixed-position rules.
* Gap: the record has no measured guard-suite totals and no list of the per-role screen guard files that cover demo-path pages. Rows C4 (manual screen reader) stay Not run.

Planning Readiness: Ready.

---
title: Issue 120 changes
date: 2026-11-17
---

# Changes

Status: complete. The plan checkboxes were ticked before implementation in error; the work below is the evidence that they now hold.

## Files

* docs/adrs/0002-pilot-readiness-architecture.md: decision 7 gained a "Current build" list and an unmet-evidence table.
* src/api/tests/test_timecapture.py: `DecisionRecordTests` (one test).
* docs/reference/log.md: entry.

## Validation (FOCUSED)

* Baseline before edits: `unittest tests.test_timecapture tests.test_timecapture_copy` with worktree PYTHONPATH, 38 tests OK, 5 skipped. The default environment imported the main checkout (editable install), so worktree paths were set explicitly.
* New test fails with the original ADR (stash check, 1 failure) and passes with the fix.
* After: 39 tests OK, 5 skipped (browser opt-in).
* `mypy src` in `src/api`: no issues in 29 files.
* `ruff format --isolated --line-length 100 --check tests/test_timecapture.py`: reports reformatting; the same result occurs on the unmodified file (pre-existing long import line), and src-ci does not list this file. Not changed.
* `git diff --check`: clean. Full gate, SQL, browser and hosted CI not run (heavy lock held; not required by FOCUSED docs scope).

## Unmet

Criterion 3 (staff notice approved, enabling action ratified) needs the DPO, Legal, HR and administrator; unticked.

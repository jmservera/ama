---
title: Epic 149 form error summary associations changes
ms.date: 2026-11-14
---

## Added

* `src/api/tests/test_epic149_form_error_summary_associations.py` (8 tests).

## Validation

* New test: 8 passed.
* `test_accessibility_baseline.py` and other `test_epic149_*`/`test_*accessibility*` tests: pass, except `test_epic149_role_workbench_heading_hierarchy.py`, which fails 22 subtests (H1_NOT_FIRST and unnamed tables). Pre-existing at HEAD 931319817; no web file changed here. Its recorded follow-up already names the H1 gap.
* `ruff check .` and `ruff format --check .`: clean.
* `mypy`: one pre-existing error, `test_epic149_landmarks_skip_link_focus_order.py:83` (untyped `App`). None in the new file.
* Not run: complete local gate, hosted CI (Focused tier). Not pushed.

## Divergence

None from the plan. Counted `aria-invalid` baseline (8) is unchanged.

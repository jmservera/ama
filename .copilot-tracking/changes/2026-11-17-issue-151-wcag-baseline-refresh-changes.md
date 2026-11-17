---
title: Issue 151 changes
ms.date: 2026-11-17
---

## Planned changes

* `docs/reference/research/ux/wcag-conformance-baseline.md`: new measurement section.
* `src/api/tests/test_wcag_workbench_baseline_151.py`: one regression test.
* `docs/reference/log.md`: appended entry.

## Done

* Section added to the baseline record, one test `test_counted_guard_measurement_section_matches_source`, log entry appended.
* Validation: `python3 -m unittest tests.test_wcag_workbench_baseline_151 tests.test_accessibility_baseline` (src/api) 21 OK; `ruff format --isolated --line-length 100 --check` on the test file clean. mypy not run: no package source changed. Hosted CI not observed.

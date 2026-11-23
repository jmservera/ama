---
title: Issue 470 live research r2 (2026-11-22)
ms.date: 2026-11-22
---

* Research disposition: executed. Planning Readiness: Ready.
* Issue 470 has one unticked criterion: measured full-run time before and after recorded in the PR.
* Main at 10cad2e413 contains this branch head. PR #2272 (the combined speed-up for #2186 to #2190) merged 2026-11-22T21:14:34Z; issues 2186 to 2190 remain open and are not duplicated here.
* Prior note: docs/reference/research/issue-470-live-2026-11-22.md found criterion 4 unproven because #2272 was unmerged. That premise is now stale; the "after" tree exists on main.
* Constraint: the brief forbids `rpi-checks.py --all` and PR publication, so a matched before/after pair cannot be produced here.
* Gate tests: `python3 -m unittest discover -s tools -p 'test_rpi_checks*.py'` ran 128 tests, OK.

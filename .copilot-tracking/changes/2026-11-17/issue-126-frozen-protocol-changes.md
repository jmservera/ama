---
title: Issue 126 changes, work-package breach pause
ms.date: 2026-11-17
---

# Changes

Status: complete (Focused tier).

* `src/core/tests/test_governance.py`: new `test_work_package_breach_pauses_only_cases_with_active_orders_in_it` (runs against the JSON and SQL-fixture store variants).
* `src/core/src/zava_forward/core/governance.py`: `guard_case_event` also checks `work package` scopes from the case's active work orders; read-only access to procurement data.
* `src/core/README.md`: breach paragraph states work package enforcement and that a workstream breach is recorded but not enforced.
* `docs/reference/log.md`: appended entry.
* Divergence: the implement-start witness recorded "source already dirty" because the test edit was issued in the same batch as the witness call; the test was written after the changes file existed.

## Validation (worktree source via PYTHONPATH, src/core)

| Command | Result |
| --- | --- |
| fail-before `unittest discover -s tests -p test_governance.py -k work_package` | 2 failures, PermissionError not raised ([log](issue-126-fail-before.log)) |
| `unittest discover -s tests -p test_governance.py -q` | 77 OK, 16 skipped (opt-in loopback SQL, not run) |
| `-p "test_rai_*.py"`, `-p test_bulk*.py`, `-p test_finance_signoffs.py`, `-p test_procure*.py` | 27, 39, 33 OK; procure pattern matched none |
| `ruff check .`, `ruff format --check .`, `mypy` in src/core | all clean (274 files formatted, 327 sources) |
| full `unittest discover -s tests -q` in src/core | ran 15 min; the summary line scrolled out of a tail of the timing output, so it is not claimed as passed |
| `ruff format --isolated --line-length 100 --check` on two files | reports reformat; src/core project config (the one CI uses for this project) passes; isolated variant applies only to the non-project scripts listed in src-ci |

Not applicable: SQL loopback, browser, image, `rpi-checks.py --all` (heavy lock held; Focused tier).

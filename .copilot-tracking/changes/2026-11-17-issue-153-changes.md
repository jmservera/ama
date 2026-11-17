---
title: Issue 153 changes
ms.date: 2026-11-17
---

## Changes

* `app.js`, `role-screens.js`: two snake_case identifiers replaced with plain words.
* `test_content_standard.py`: new snake_case prose guard; observed red on exactly the two leaks before the fix, green after.
* `test_exception_register_screen.py`: assertion updated to the new wording (it failed once after the first edit because I changed line 183 instead of 184; corrected).
* `content-standard.md`, `docs/reference/log.md`: dated audit section and log entry.

## Validation (FOCUSED tier)

* `python3 -m unittest tests.<m>` from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`: test_content_standard 30 OK, test_data_steward_screen_wcag 17 OK, test_exception_register_screen 22 OK, test_workspace_scripts 10 OK.
* `mypy src/zava_forward` in `src/api`: no issues in 29 files.
* `ruff format --isolated --line-length 100 --check`: `test_exception_register_screen.py` clean; `test_content_standard.py` was already unformatted on the base (pre-existing, unrelated lines at 424 to 506), left untouched.
* Not run: rpi-checks --all (full tier not required; heavy lock held), browser harness (copy-only change, no layout/logic change).

## Unmet

Criterion 5, named human review of resident-facing wording. No closing keyword.

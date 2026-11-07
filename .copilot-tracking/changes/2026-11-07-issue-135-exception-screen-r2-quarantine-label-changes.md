---
title: Issue 135 exception screen r2 quarantine label correction changes
ms.date: 2026-11-07
---

* Plan: `.copilot-tracking/plans/2026-11-07-issue-135-exception-screen-r2-quarantine-label-plan.md`. Base commit `26ce7c711ebffb37129fe0ca24b7b94c0d8356e1`.

## Changes

* `src/api/src/zava_forward/api/web/role-screens.js:876-879` (`exceptionHappened`): quarantine is recognised with a case-insensitive string comparison, so the real `"Quarantined"` value shows "Quarantined." A failed-AI item with no reason now reads "How it failed is Unknown." instead of claiming a fallback. Fallback wording needs a reason.
* `src/api/tests/test_exception_register_screen.py`: fixtures use the real returned `"Quarantined"` and `"Not reviewed"` statuses, plus a lowercase compatibility item (`legacyQuarantined`) and a reason-less item (`noReason`); the label test asserts each with a distinct reason so the lowercase row cannot mask the real one.

## Validation (actual)

* Failed before the fix: the new test file run against the unmodified HEAD renderer gave 1 failure ("Quarantined. ... Reason: Real quarantine reason" not found; the real row read "Fell back to rules or template"). Literal output: `/mnt/ama-gates/g135-r2-evidence/regression-before-fix.txt`.
* After the fix: `python3 -m unittest tests.test_exception_register_screen tests.test_data_operator_screen` from `src/api`, 19 tests OK. `node --check` OK. `ruff check` and `ruff format --check` clean for the changed files.
* `mypy` reports 4 errors in `tests/test_ai_consumption_api.py` only (an `import-not-found` note on an existing `type: ignore`). That file is untouched; the focused gate's own static group is the authoritative result.
* Not yet run: the focused gate and the real-DOM exception story on the frozen head.

## Not changed

* Backend, auth, store, schema, model call, controls, roles, F3 to F6, original RPI artifacts and Review.

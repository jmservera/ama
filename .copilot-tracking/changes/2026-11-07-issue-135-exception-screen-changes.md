---
title: Issue 135 employee exception screen changes
ms.date: 2026-11-07
---

## Files changed

* `src/api/src/zava_forward/api/web/role-screens.js`: host passes `(signal, data.items, c)` to `overview`; new `exception*` helpers and `exceptionRegisterView`; data-operator `overview` shows an explicit "Open the exception register" link, or the register when the hash has `exceptions=1`, beside the existing page summary.
* `src/api/tests/test_exception_register_screen.py` (new): constructed synthetic responses through a node `vm` fake DOM; 10 tests.
* `src/api/tests/test_data_operator_screen.py`: one source test (GET only, no write or HTML sinks in the new block).
* `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}` dated issue-135 evidence.

## Behaviour

* Renders returned `state`, `items`, `unrouted`, `sources`, `banner`, `access`, `note`. Items show kind, reference, status, configured owner, reason, placeholder runbook text, source or run reference and eligibility. Conflicts show every returned value with source, version, date, resolution owner and Unknown eligibility; no winner.
* Failed AI items say Quarantined or Fell back to rules or template and that no model result was delivered; a fixed note says workflow-only processing is neither a failure nor a model result and never appears here.
* 403 shows server text with "Your access has not changed"; other failures, non-JSON shape or null show an unavailable panel with "Do not read this as all clear". Non-object items are counted as unreadable. Aborted loads rethrow (nothing rendered); 401 is rethrown so sign-in is not overwritten.
* Only `api("/api/exceptions", undefined, signal)` (GET). No new control other than one link.

## Amendments and divergences

* Critique finding 5 (widen roles for named staff) was not applied; no `roles`, server, store or `ZF_EXCEPTION_STAFF` change.
* No divergence from the plan.

## Validation actually run (venv `/tmp/zf135venv`, editable installs of src/core, agents, api)

* `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_exception_register.Config tests.test_exception_register_screen tests.test_data_operator_screen tests.test_role_screens tests.test_role_screens_conformance` from `src/api`: 40 tests OK, exit 0, no skips.
* New tests with `role-screens.js` stashed: 2 failures, 8 errors (they fail without the feature).
* `ruff check`, `ruff format --check`, `mypy` on both test files: pass. `node --check role-screens.js`: pass.

## Not run (pending, not claimed)

* Focused browser feature check (keyboard, narrow reflow, real DOM abort): pending coordinator heavy admission.
* `Register` and `Endpoint` classes of `test_exception_register.py` (SQL store and local server fixtures) and `tools/rpi-checks.py --changed`: not run to avoid heavy resources; coordinator to admit.
* No human or assistive-technology acceptance (#151/#155); no runbook or staff naming approval.

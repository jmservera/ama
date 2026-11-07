---
title: Issue 73 workbench integration changes (exception screen child 135)
ms.date: 2026-11-07
---

* Task `issue73-workbench-integration`. Research, plan, details and state: dated files with the same slug. The prospective 17:xx files were created before the child merged and are preserved; refresh sections are appended and labelled.
* Topic fast-forwarded from `23b26a7f…` to the merged child `d17aee537ec267162af106e14056440274ae589d` (no overwrite of the four owned files).

## Files changed by this task

* `src/api/tests/test_exception_register_screen.py`: new `HostIntegration` class (5 tests) driving the real `roleScreensView` in a node `vm` with a fake `api`, `h` and `show`: manager request reaches `/api/exceptions` once with the page summary and no write; default hash makes no request; other roles reach neither screen nor endpoint; superseded navigation renders nothing; 403 renders a denied panel with no rows.
* `docs/architecture/cutover-evidence-pack.md`: dated parent-topic checkpoint (observed and candidate, not merged-main, Azure or human acceptance) and `ms.date` 2026-11-07.
* `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}` issue73 evidence.

## Source decision

* No necessary change to `role-screens.js`: the host seam is correct in source and the mutation checks below show the new test detects its breakage. No server, store, auth, schema, model, infrastructure, dependency, producer or recovery change.

## Amendments and divergences

* Plan critique C1 to C4 applied; C5 rejected (conflicts with the open owner decision F3); C6 recorded only. Plan phases 4 and the heavy part of 5 deferred by the resource boundary, not dropped.
* Divergence: none from the refreshed plan.

## Validation actually run

* Dedicated venv `/tmp/venv73` with editable installs of `src/core`, `src/agents`, `src/api`; import path confirmed in this worktree.
* `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_exception_register.Config tests.test_exception_register_screen tests.test_data_operator_screen tests.test_role_screens tests.test_role_screens_conformance` from `src/api`: exit 0, 45 tests OK.
* Mutants of `role-screens.js` (host passes `[]` and `null`; explicit-request rule forced true; data-operator roles widened): `HostIntegration` failed in each (1 failure); file restored, diff empty.
* `ruff check`, `ruff format --check`, `mypy` on the test file and `node --check role-screens.js`: pass.

## Not run (open gates, not Pass)

* `tools/rpi-checks.py --changed`, integrated browser observation, `Register` and `Endpoint` SQL and server classes: the sole heavy holder is original #1231; no additional heavy job was started or queued. A new coordinator admission is required.
* Independent assessment, hosted checks on the final head, human and assistive-technology acceptance.

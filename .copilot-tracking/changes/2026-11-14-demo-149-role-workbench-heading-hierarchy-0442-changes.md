# Changes: demo-149-role-workbench-heading-hierarchy-0442

* Date: 2026-11-14
* Plan: [.copilot-tracking/plans/2026-11-14/demo-149-role-workbench-heading-hierarchy-0442-plan.md](../plans/2026-11-14/demo-149-role-workbench-heading-hierarchy-0442-plan.md)

## Added

* `src/api/tests/test_epic149_role_workbench_heading_hierarchy.py`: 6 tests over 8 roles and about 200 rendered views.

## Amendments and divergences

* The brief names `TestClient`; the API has none (stdlib server) and views are client-rendered, so the test uses the real local server and headless Chromium via Playwright. Skips cleanly when unavailable.
* One real defect recorded as a shrink-only gap, not fixed: staff `#/` and `#/all` render `h2`/`h3` before the page `h1`.

## Validation (from `src/api`, worktree `PYTHONPATH`)

* `python3 -m unittest tests.test_epic149_role_workbench_heading_hierarchy`: 6 tests OK (about 11 s).
* `ruff check` and `ruff format --check` on the new file: pass.
* `mypy` (strict, whole project): no errors in the new file. One pre-existing error remains in `tests/test_epic149_landmarks_skip_link_focus_order.py:83` (`App` untyped), identical on the parent commit and untouched here.
* Hosted CI not observed; nothing pushed.

# Research: #152 manifest aftercare navigation (1433)

Refs #152, #133, #149. Tier: Focused. Research disposition: executed. Planning Readiness: Ready.

## Question

Why do four cases of `test_existing_roles_have_exact_manifest_destinations` fail (`#/aftercare` in `src/api/checks/workbench-manifest.json` but absent from role navigation)?

## Findings

* The test is `src/api/tests/test_workbench.py::WorkbenchNavigation`. It compares `navigation()` in `src/api/src/zava_forward/api/workbench.py` with each role's `navigation` list in the manifest.
* At `dafed6a27`, `workbench.py` declares `#/aftercare` (visible when `user.role in VIEW_ROLES` from `zava_forward.core.aftercare_intake`), added by `64c3f9191` (#1400) together with the manifest rows. `app.js` routes `#/aftercare` (lines 345, 442). Source and manifest agree; no contract drift.
* The shell's editable installs (`pip list`) resolve `zava-forward-api/core/agents` to `/home/azureuser/source/ama/src/*`, a different, stale checkout whose `workbench.py` has no aftercare entry. Running the tests there produces exactly 4 failing subtests (the roles that list `#/aftercare`: RLO, PM, Coordinator, Programme Support Officer).
* With `PYTHONPATH` pointing at the worktree, or a venv with `pip install -e src/core -e src/agents -e src/api` from the worktree, the test passes.
* `scenario-manifest.json` and hashed files are not involved; none are edited.

## Verification (clean venv `/tmp/venv-152`, pip only)

* `test_workbench*` glob (12 tests across files, including the browser-check helper tests), `test_design_system*` (8), `test_accessibility_baseline*` (13), `test_aftercare*` (21) in `src/api`: OK.
* `src/core` `test_scenario_manifest*` (8), `test_needs_inventory*` (11): OK.
* `ruff check`, `ruff format --check`, strict `mypy` (run from `src/api` as CI does; 236 files): clean.

## Conclusion

No source or manifest defect exists. The failure is a stale editable-install environment artefact outside the repository. A code change to weaken or remove `#/aftercare` would break the #1400 contract. The deliverable is this evidence plus the reproduction guidance; `role-screens.js` and `chat.js` are untouched.

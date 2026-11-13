# Changes: #152 manifest aftercare navigation (1433)

Refs #152, #133, #149.

* No source, manifest or JavaScript change. `workbench.py`, `workbench-manifest.json`, `app.js`, `role-screens.js` and `chat.js` are unchanged and consistent.
* Added tracking evidence only: research, plan, details, critique, this record, state file.
* Reproduction of the 4 failures: run `test_workbench` where `pip list` shows `zava-forward-*` editable installs under `/home/azureuser/source/ama/src/*`.
* Remedy: use a venv with `pip install -e src/core -e src/agents -e src/api` from the worktree, or set `PYTHONPATH` to the worktree `src/*/src`.
* Validation (clean venv, pip only): `test_workbench*` 12, `test_design_system*` 8, `test_accessibility_baseline*` 13, `test_aftercare*` 21, core `test_scenario_manifest*` 8, `test_needs_inventory*` 11 all OK; `ruff check`, `ruff format --check`, strict `mypy` (236 files) clean.
* Failing-first: the failure was reproduced in the stale environment (4 subtests) before concluding.

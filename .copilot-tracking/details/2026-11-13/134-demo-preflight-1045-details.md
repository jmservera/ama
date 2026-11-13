---
title: Issue 134 demo preflight details
ms.date: 2026-11-13
---

## Phase details

* Venv: `python3 -m venv /tmp/venv-preflight-1045`; `pip install --no-deps -e src/core -e src/agents -e src/api -e src/importer`. Verify `zava_forward.core.__file__` etc. start with the worktree `src/`.
* Tests (cwd per component, `env -u ZF_DATA`, unittest): core `test_generated_dataset test_scenario_manifest test_needs_inventory` with `PYTHONPATH` unset; importer `test_document_form_fixtures`; api `test_case_journey` (needs node, no browser). Exit via `echo $? > status`, not pipelines.
* Inspection script: reuse the test builder (patch `load_register` with the test `register()`), build to a temp dir, load with `Store`, and for each of the five ids print archetype, stage, count of damp reports, sensor backfill availability, conflict/blocker records (stock_reconciliation, gate), and `home_case_view` payload readiness as a synthetic staff user. Unknown keys are reported as `absent`, never invented.
* Record script source, sha256, module origins, unit counts and exits in the changes log. Remove the venv.

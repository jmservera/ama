---
title: Issue 89 current main adoption details
ms.date: 2026-11-10
---

## Step 1-2

* Merge message `chore(integration): adopt current main into parent 89 staging`, `Refs #89`, Copilot trailer. Author and committer are the repo-local `8036360+jmservera@users.noreply.github.com`. Any conflict is edited only with the edit tool; Core `pyproject.toml` is parsed with `tomllib` after merge; any manifest hash comes from `sha256sum` of the resulting file.

## Step 4 exact commands (cwd src/core, env `/tmp/i89-1110`, `PYTHONDONTWRITEBYTECODE=1`)

* Core, one `python -m unittest discover -s tests -p test_<m>.py -q` per module: aftercare_intake, aftercare_store, aftercare, scenario_manifest, needs_inventory, resident_decisions, resident_showcase, learning_test_bundles, device_registry_azure.
* API (cwd src/api, `PYTHONPATH=../core/tests:../agents/tests`): aftercare_served, aftercare_screen, accessibility_baseline, static_assets, auth, role_endpoint_inventory, role_screens_conformance, nomination_screen, handoff_read_guidance, atlas_tensions_checker, workbench, progress_dashboard, simulator_admin, live_control, workspace_scripts, browser_asset_urls.
* Configured `ruff check`, `ruff format --check` and `mypy` for Core and API; `node --check` of the web scripts.
* Heavy under `flock -n /tmp/ama-rpi-heavy.lock`: focused 36 `test_aftercare_store` against the disposable SQL Server using the Root script pattern (owned container, label guard, redacted output); browser checks aftercare, workbench, nomination, progress, workspace_scripts, employee_workspace.
* Not run: full Core or API discovery, full gate, `--changed`, infra tests, image checks, model, cloud, private data.
* A red result is classified against both parents before any statement; no repair.

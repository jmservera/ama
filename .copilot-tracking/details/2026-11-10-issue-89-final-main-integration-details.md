---
title: Issue 89 final main integration details
ms.date: 2026-11-10
---

## Step 1-2

* Merge message `chore(integration): adopt current main into parent 89 staging`, `Refs #89`, Copilot trailer, author and committer `8036360+jmservera@users.noreply.github.com`. The conflicted JSON is edited only with apply_patch; resolution compares `sha256sum` of `src/api/checks/workbench-manifest.json` and `src/api/checks/workbench_browser_check.py` in the merged tree with the two entries. The manifest tests (`test_scenario_manifest`) validate the result.

## Step 4 targeted modules (selected from the current delta)

* Core: test_aftercare_intake, test_aftercare_store, test_aftercare, test_scenario_manifest, test_needs_inventory, test_learning_test_bundles, test_resident_decisions, test_resident_showcase.
* API: test_aftercare_served, test_aftercare_screen, test_accessibility_baseline, test_static_assets, test_auth, test_role_endpoint_inventory, test_role_screens_conformance, test_nomination_screen, test_handoff_read_guidance, test_atlas_tensions_checker, test_workbench, test_progress_dashboard, test_simulator_admin, test_live_control.
* Configured ruff check, ruff format check, mypy for Core and API; node `--check` of changed web scripts.
* Heavy (non-queued `flock -n /tmp/ama-rpi-heavy.lock`): aftercare_browser_check, workbench and nomination browser checks. Focused SQL 36 only if child SQL inputs changed; otherwise a source-qualified carry-forward.
* Red results are classified against both parents before any claim; no repair.

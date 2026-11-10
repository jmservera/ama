---
title: Issue 109 actual remote parent and main adoption changes
ms.date: 2026-11-10
task_id: 109-actual-parent-main-1110
---

## Status

Prospective declaration written before `implement-start`; actuals recorded at implement-done.

## Planned changes

* One ordinary no-fast-forward merge of the actual remote parent squash `bd2a6494464b451572fc3dc7c8d53c549e0f9dad` and main `64c3f9191a2ffa97ef2dc07245422333ad4d6585` into HEAD `20addb9ae1d7c652ecf1882401e54523fee97ba0`, committed once with these dated records.
* No authored product, test, config, workflow or dependency change.

## Actuals

Merge (implemented-unverified local candidate; not published, not hosted-CI verified): `git merge --no-ff --no-commit origin/feat/demo-sensor-review-109-1110 origin/main` from HEAD `20addb9ae1d7c652ecf1882401e54523fee97ba0`; pins re-fetched unchanged (squash `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`, main `64c3f9191a2ffa97ef2dc07245422333ad4d6585`). No conflict, zero unmerged paths; staged tree `d45426bd28850d893622b48df1a2649a13135992` equals the dry run. Auto-merged: `server.py`, `projection.py`, `src/core/pyproject.toml`. Preserved: sensor draft routes and aftercare routes in `server.py`; the child's `projection.py` edit plus main's `aftercare` addition; Core `iothub` and `dev` pins, the draft-module exemption group, and main's `test_aftercare_store` addition to the seed-merge group; API `test_aftercare_served` override; API sensor-test `type: ignore[no-untyped-call]` (once). All other non-tracking paths equal main or the squash. No source authored.

Checks (raw logs, scripts, true exits in ROOT `checks-109-actual-parent-main-1110/`; owned venv `/tmp/z109-pi-1110/venv`, no new installs, import origins proven inside this worktree):

* Core: `test_sensor_review_draft` 65 run, 22 opt-in skips (not SQL passes) OK; `test_sensor_analysis` 11, `_store` 9, `test_scenario_manifest` 8, `test_device_registry_azure` 39, `test_aftercare_intake` 39 OK; `test_aftercare_store` 36 run, 13 skips, OK.
* API: `test_sensor_review_draft_api` 6, 0 skips; `test_aftercare_served` 8; `test_aftercare_screen` 13; `test_accessibility_baseline` 12; `test_workbench` 5, all OK. `test_role_endpoint_inventory` first run RED (import error: `test_role_matrix` not on `PYTHONPATH`, the first command omitted `src/api/tests`; preserved in `03-api-test_role_endpoint_inventory.txt`); rerun with `src/api/tests` on the path: 24 OK. A harness path omission, not a source defect.
* Configured Core mypy green (296 files), API mypy green (224 files); Core and API ruff check and format check pass; `node --check` of `ops.js`, `aftercare.js`, `app.js` pass.
* Actual sensor browser, one `flock -n` attempt, short owned cwd (removed): 33 passed, exit 0; unchanged check, mock and synthetic only.
* Fresh scoped MSSQL `MssqlDraftCases`, one `flock -n` attempt, own disposable container (removed): 22 run, 0 skips, OK; local synthetic SQL, not Azure SQL.
* Not run by design: full discovery, full gate, `--changed`, aftercare browser, aftercare MSSQL selectors, images, cloud, provider, private data.

Gaps carried: unforced `ConflictError` and `CommittedReloadError`; scoped mypy exemptions (incl. main's aftercare ones, not broadened here); Core opt-in skips (22 draft, 13 aftercare store); inherited aftercare Mediums #1401 and #1402 open and not repaired here; no accessibility, Azure, live UI or model acceptance; Registry #1393 source-only.

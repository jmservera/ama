---
title: Issue 109 actual remote parent and main adoption plan
ms.date: 2026-11-10
task_id: 109-actual-parent-main-1110
---

Research: [research](../research/2026-11-10-sensor-review-109-actual-parent-main-1110-research.md). Details: [details](../details/2026-11-10-sensor-review-109-actual-parent-main-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-review-109-actual-parent-main-1110-plan-critique.md). Changes: [changes](../changes/2026-11-10-sensor-review-109-actual-parent-main-1110-changes.md).

## Objective

One ordinary `git merge --no-ff --no-commit origin/feat/demo-sensor-review-109-1110 origin/main` into local HEAD `20addb9ae1d7c652ecf1882401e54523fee97ba0` (squash `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`, main `64c3f9191a2ffa97ef2dc07245422333ad4d6585`), committed once with the dated records. Local candidate only, not published; the actual remote parent is not main.

## Tier: FOCUSED demo (basis recorded)

The merge authors no workflow, dependency, Dockerfile, permission, schema or gate line. Inherited main content does change Core and API source, Core and API pyproject mypy overrides (scoped test-module untyped-call exemptions) and an SQL store, and the sensor-review code shares `server.py`, `projection.py` and `src/core/pyproject.toml` with it. That is an input change to the earlier checks, so affected checks are refreshed; it is not a deployment, infrastructure, SQL-schema authorship, secret, permission or security-control change authored here, so the full tier and a blanket `--changed` or full gate are not run. Doubt rule: any NEW dependency, permission, workflow or exemption line beyond the two known main hunks stops for Root. Hosted CI, independent review and human approval remain required; none is claimed.

## Steps

* [x] Research (`research-open`).
* [ ] Plan, details, one critique, prospective changes, `plan-done`.
* [ ] Implement: recheck pins, `implement-start`, merge, invariants, planned checks, actuals, `implement-done`.
* [ ] Review once, `review-done`, commit, `commit-complete`, verify.

## Merge protocol and invariants

Recheck `git fetch`; if the squash or main moved, stop for Root. If git refuses a two-extra-parent merge or any path is unmerged or semantically conflicting, stop with exact paths and intent. No rebase, reset, amend, force, cherry-pick, patch or hand edit of source. Invariants: non-tracking paths equal `origin/main` or the squash (squash equals child) except the three overlap files, whose merged content must preserve both sides: `src/core/pyproject.toml` keeps `iothub` and `dev` pins, the child's draft-module exemption group, and main's `test_aftercare_store` additions to the seed-merge group; `src/api/pyproject.toml` keeps main's `test_aftercare_served` override; `server.py` keeps the sensor draft routes and aftercare routes; `projection.py` keeps both. The `tomllib` parse must pass. Excluded: sibling unmerged work; Mediums #1401 and #1402 are not repaired.

## Environment

Reuse owned `/tmp/z109-pi-1110/venv` (declared pins only). Re-verify import origins inside this worktree; `pip install` only after an observed missing-dependency failure, never shared. External HOME and mypy caches, `PYTHONDONTWRITEBYTECODE=1`, no provider, cloud or private data. Remove ignored build artifacts afterwards.

## Checks (raw logs, commands, true exits under ROOT `checks-109-actual-parent-main-1110/`)

1. Import origins; TOML parse; marker greps.
2. Core, `src/core`: `tests.test_sensor_review_draft` (expect 65, 22 opt-in skips), `test_sensor_analysis`, `test_sensor_analysis_store`, `test_scenario_manifest`, `test_device_registry_azure`, `test_aftercare_store`, `test_aftercare_intake`.
3. API, `src/api`, CI-style `PYTHONPATH`: `tests.test_sensor_review_draft_api` (6, 0 skips), `test_role_endpoint_inventory`, `test_aftercare_served`, `test_aftercare_screen`, `test_accessibility_baseline`, `test_workbench` (the overlap and manifest consumers of `server.py`, `index.html`, `app.js`).
4. Configured Core and API `ruff check`, `ruff format --check`, `mypy --no-incremental`; `node --check` of `ops.js`, `aftercare.js`, `app.js`.
5. Actual sensor browser `checks.quality_sensors_browser_check`: one `flock -n /tmp/ama-rpi-heavy.lock` attempt reporting the holder, short owned cwd, unchanged check, mock and synthetic only, expect 33 passed. BUSY stops admission.
6. Fresh scoped MSSQL `tests.test_sensor_review_draft.MssqlDraftCases` (22 run, 0 skips): one `flock -n` attempt, own disposable container, throwaway password not logged, container removed. Core SQL source (`sqlstore.py`, `projection.py`) changed in main, so no carry.

Not run by design: full source discovery, full gate, `--changed`, aftercare and other browsers, aftercare MSSQL selectors (aftercare lane's own evidence), images, cloud, provider, private data. Skips are not passes. Carried gaps: unforced `ConflictError` and `CommittedReloadError`; scoped mypy exemptions; opt-in skips; no accessibility, Azure, live UI or model acceptance.

## Stop rules

Pin drift, unmerged path, failing configured or selected check that indicates a source bug (record, stop the affected activity, do not fix), BUSY lock, refused marker. No self-heal or retrospective record.

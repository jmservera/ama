---
title: Issue 89 current main adoption research
ms.date: 2026-11-10
---

## Task and boundary

* Task `issue-89-current-main-adoption-1110`, child of `issue-89-final-main-integration-1110`. Ordinary actual-main adoption only: no source repair, no new allowance, no #132 takeover or held code. Whole #89, #133 and #134 stay open and unticked. Original Stage A, C4, C5 and integration RPI, witness records, adverse findings and the frozen `c6c0e4d2590eab632238e45cfec0c009d15691e1` lineage are preserved unchanged.
* Research disposition: executed. Brief: `brief-89-current-main-adoption-1883.txt` in the Root files directory.

## Source identities (observed after fetch)

* Local HEAD `c6c0e4d2590eab632238e45cfec0c009d15691e1`, tree `4b148614e27fd05549d5334349d660681300dbde`, clean. Published parent `origin/feat/demo-quality-workflows-89-1109` is `4f5dc382bfca69c286fca6e60aa24b9a8ebbeb0e` (an ancestor of HEAD; no published move).
* Main `origin/main` is `6cc59776666620309fb6b67ad2fdafb343d40998`, tree `eaf44bcdec8bdf5e9dfab2e73b1ded5459d8ff3c`, src tree `af889a4f05a2a3f20ea25ff55237fd41a7188c20`. Previous base `65c2ab9d947d1498dafd37e24a377d1ff503e86f`. Merge base with HEAD is `65c2ab9d`.
* Main delta over the previous base: 16 non-tracking paths. Rubric README and latest.json; infra README, main.bicep, containerapps.bicep, guard.bicep and three infra tests; API checks `employee_workspace_browser_check.py`, `workspace_scripts_browser_check.py`, new `script_retry.py`, tests `test_browser_asset_urls.py`, `test_workspace_scripts.py`; Core README, `pyproject.toml`, new `synthetic/device_registry_azure.py` and `tests/test_device_registry_azure.py`. Commits: #1393 Registry backend, #1392 workspace oracle repair, #1394 docs, #1390 delayed route, #1380 infra startup, rubric score records.
* Dry-run `git merge-tree --write-tree HEAD origin/main` returned tree `7af3d7fcc4478639fb9d29ac9f6520a2da277763` and no conflict output, so overlap in the Core and API READMEs, `log.md` or Core `pyproject.toml` is expected to auto-merge. To be confirmed by the real merge.

## Selector reasoning

* Not touched by main: `sqlstore.py`, `store.py`, `aftercare_store.py`, `aftercare_intake.py`, `projection.py`, `dataset.py`, `server.py`, `aftercare.js`, `app.js`, the API pyproject.
* Touched dependency input: Core `pyproject.toml` adds the optional `iothub` extra and puts `azure-iot-hub==2.7.0` and `six==1.17.0` in `dev`. The planned dependency inputs therefore changed, so the child SQL 36/0-skip result cannot be carried forward silently. Plan: run the focused 36 disposable SQL once under a non-queued heavy lock, using the existing task-owned script pattern, and never count skips as passes.
* Mypy and ruff on Core now cover `device_registry_azure.py`; if the Registry SDK is missing from the own environment, install exactly the pinned dev dependency into the own environment only after the actual failure.
* Browser: the two generic workspace checks changed on main (#1392) and are in scope together with aftercare, workbench, nomination and progress.

## Open items preserved

* Inherited Mediums (1000-key order, raw blank `FileStateStore`) stay OPEN, unrepaired, not high-volume acceptance. #1384 closed by Root; generic oracles no longer waived red. Registry live credentials, provisioning and teardown are unproved. #440 NomUX plus Bicep 6119 record is consumed by Root as bounded CONTINUE offline (PR 1396, hosted CI pending); whole release and human gates are not cleared.

## Planning readiness

* Ready.

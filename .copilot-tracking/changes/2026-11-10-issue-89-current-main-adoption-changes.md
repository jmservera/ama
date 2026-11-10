---
title: Issue 89 current main adoption changes
ms.date: 2026-11-10
---

## Status

* Complete. Registered prospectively before implement-start (witness seq 4); actual results below, recorded before implement-done.

## Changes

* Ordinary no-ff merge of main `6cc59776666620309fb6b67ad2fdafb343d40998` into the parent at `c6c0e4d2590eab632238e45cfec0c009d15691e1`: merge commit `a664e316a508a1c6bcc5ab89fb59edc29fa42ad5`, tree `7af3d7fcc4478639fb9d29ac9f6520a2da277763` (equals the dry-run prediction), parents `c6c0e4d2` and `6cc59776`. Author and committer: repo-local noreply identity; Copilot trailer.
* Zero conflicts. Auto-merged: `src/core/README.md`, `src/core/pyproject.toml` (both pyproject files parse with `tomllib`), `docs/reference/log.md` (all 11399 lines of the parent and all 11385 of main retained, 0 missing). No manual edit, no source change beyond the two sides, no `.copilot-tracking` file modified or deleted against the parent.
* Identities: src tree `c322b0f7a710c7f121fcd75b6685683ff57fa893`; infra tree equals main `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`. `sqlstore.py`, `store.py`, `aftercare_store.py`, `aftercare_intake.py`, `projection.py`, `test_aftercare_store.py`, `dataset.py` and the API pyproject are byte-identical to `c6c0e4d2`; only Core `pyproject.toml` changed (Registry SDK pins), so the old SQL result was not carried over.

## Validation (raw output in the external checks-89-current-main-adoption-1110 directory)

* Core targeted exit 0: aftercare_intake 39, aftercare_store 36 (13 SQL-gated skips, not counted as passes), aftercare 21, scenario_manifest 8, needs_inventory 11, resident_decisions 371 (132 skips), resident_showcase 41, learning_test_bundles 21.
* `test_device_registry_azure` first run exit 1 (34 failures, 16 errors, `SDK_MISSING` cascades): the pinned Registry SDK was missing from my own env, an environment gap, not a product defect. Installed `azure-iot-hub==2.7.0` and `six==1.17.0` into `/tmp/i89-1110` only; the rerun passed 39 tests. First output preserved.
* API targeted exit 0 for 16 modules including workspace_scripts (10) and browser_asset_urls (10); handoff_read_guidance has 4 skips.
* Core and API ruff check, format check and mypy exit 0; node `--check` of 15 web scripts exit 0.
* Focused SQL: `test_aftercare_store` run once against a disposable SQL Server under non-queued `flock -n /tmp/ama-rpi-heavy.lock`: 36 tests, OK, 0 skips, imports from this worktree, container removed, no leftover databases. This replaces the old carry-forward.
* Browser under the same lock (free at admission): aftercare, workbench, workspace_scripts, employee_workspace and nomination (axe 4.10.3) exit 0. Progress first exited 1 on my own invocation (out directory already existed); one rerun with a fresh out directory exited 0.
* Not run: full Core or API discovery, full gate, `--changed`, infra tests, images, model, cloud, private data.

## Open items preserved

* Inherited Mediums (1000-key order, raw blank `FileStateStore`) stay OPEN, unrepaired, not high-volume acceptance. Registry live credentials, provisioning and teardown remain unproved. #132 excluded; whole 89, 133 and 134 open; the #440 record is consumed by Root only as bounded CONTINUE offline.

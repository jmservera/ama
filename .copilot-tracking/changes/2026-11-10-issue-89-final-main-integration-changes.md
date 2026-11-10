---
title: Issue 89 final main integration changes
ms.date: 2026-11-10
---

## Status

* Complete. Registered prospectively before implement-start (witness seq 4); actual results recorded below before implement-done.

## Changes

* Fast-forward only: 50e1d2147d04d0440318932f44e693a114ea7d9c to 4f5dc382bfca69c286fca6e60aa24b9a8ebbeb0e (merged child 133 PR 1385); tree cc3a1dcdbe54714f8c8b885b37946c2324bb1a26 equals the frozen child tree. Source clean before launch.
* Ordinary merge (no-ff) of main 65c2ab9d947d1498dafd37e24a377d1ff503e86f as commit 03d06a1aea3072f517cba0d2e3771318c9d836e3, tree e3fd04ea802b2a8671d7857c551f8f613556de5d, parents 4f5dc382 and 65c2ab9d. Author and committer are the privacy-safe local noreply identity.
* One conflict only, as predicted: docs/reference/research/retrofit-synthetic-data/scenario-manifest.json sources. Resolved by keeping the parent workbench hash 6552264950fd... and the main recipe hash 9a9755434d07..., each verified equal to sha256sum of the actual merged src/api/checks/workbench-manifest.json and workbench_browser_check.py. Edited with the edit tool only.
* Auto-merged without conflict: docs/reference/log.md (both parents' lines retained, 11373 and 11385 lines, 0 missing, merged 11399), src/api/README.md, src/core/README.md, app.js (hunks from both sides present).
* Preservation: the non-tracking changed-file set against the parent equals main's delta since a600221; no .copilot-tracking deletions against either parent; no source change beyond the two sides.

## Validation (raw output in the external checks-89-final-main-integration-1110 directory)

* Core targeted: aftercare_intake 8, aftercare_store 36 (OK, skipped=13 SQL-gated, not counted as pass), aftercare 11, scenario_manifest 21, needs_inventory, learning_test_bundles, resident_decisions, resident_showcase 41; all exit 0.
* API targeted: aftercare_served, aftercare_screen, accessibility_baseline, static_assets, auth, role_endpoint_inventory, role_screens_conformance, nomination_screen, handoff_read_guidance (4 skipped), atlas_tensions_checker, workbench, progress_dashboard, simulator_admin 30, live_control 34; all exit 0.
* Core and API ruff check, ruff format check and mypy exit 0; node --check of 15 web JS files exit 0.
* Heavy browser checks under the non-queued heavy lock: first probe busy (holder run_all.sh pid 4109830 via flock pid 4109828), one later attempt succeeded. aftercare and workbench (shared IA checks) exit 0; nomination first two invocations failed on my own invocation arguments (missing tests path, missing --axe/--out), then passed with the pinned axe 4.10.3 sha 880970c0...; no product edit.
* SQL: not rerun. Source-qualified carry-forward of the child 36/0-skip evidence only: sqlstore.py, store.py, aftercare_store.py, aftercare_intake.py, projection.py, test_aftercare_store.py, dataset.py and both pyproject files are byte-identical between 4f5dc38 and HEAD; infra tree equals main. Local SQL-gated tests skipped here and are not claimed as passes.

## Open items preserved

* Inherited Mediums (1000-key order, raw blank FileStateStore) stay OPEN; no repair. Generic workspace oracles stay with 1384. The new 440 stabilization record is a pending parallel input. Held 132 not included; no C6; whole 89/133/134 unticked.

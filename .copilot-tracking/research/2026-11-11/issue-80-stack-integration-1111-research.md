---
title: Issue 80 stack integration research
description: Parent PR1423 integration after child PR1424 squash, against current main
ms.date: 2026-11-11
---

## Source identities

* Own previous head `cc210fa4460c28bb6f57b1389a183ae3dc7902cc`, clean; fetched `origin/test/demo-export-entrypoints-80-1110` = `adbca56e8938bdee91a267ef422cb37e4dc7f811` (child PR1424 squash, "export read-only unaccepted handoff waiting times").
* `cc210fa4` is an ancestor of `adbca56e`, so `git merge --ff-only` was used (no force, rebase or reset). Head after: `adbca56e`.
* Fetched `origin/main` = `b8394cd5a75db75d79411c1f43959ac5e13e1848`; merge base with parent `6d4cd62475ba89a214055f761b8e3276ef063d44`.
* Main delta over `6d4cd624`: `b8394cd5` rubric score only, `83c28132` household inventory #1422 (issue 131), `6f5e5007` Atlas visible design version #1421 (issue 1362). Files: core `resident_decisions.py` and its test, `test_resident_api.py`, `atlas_tensions_browser_check.py` and its test, two READMEs, rubric score, tracking state. Child 1419 is not in main; unmerged 1360/144 siblings are excluded.

## Mergeability

* Parent delta over `6d4cd624` touches `server.py`, `app.js`, `test_role_endpoint_inventory.py`, handoff CSV tests, README and own tracking. Only `src/api/README.md` overlaps main.
* `git merge-tree --write-tree` returned exit 0 with tree `93f5a0c927f0fc6cedcc1aa121b353ae06915e2c`, no conflicts. A trial `git merge --no-commit` in an owned scratch worktree gave the same tree and automatic README merge.
* No real conflict, so no merge commit is made in the parent branch; a merge would only generate activity. Decision: validate the combined content (parent plus main) in the scratch worktree and record the trial tree; Root's hosted checks decide mergeability.
* Source hunks do not overlap; approved inventory 131 behaviour and the handoff 1419/consent/manual/unknown contracts are both preserved by construction (disjoint files).

## Impacted tests

* Child: `test_unaccepted_handoff_csv_api` (13), `test_unaccepted_handoff_download_ui` (6, real Chromium, no skip), handoff guidance (9) if relevant.
* Parent: `tests.test_case_journey` (31), `test_list_export_api` (11), static modules (60), `test_role_endpoint_inventory`.
* Main-side, combined: `test_resident_api`, `core tests.test_resident_decisions`, `test_atlas_tensions_checker`, as integration guards.
* Capacity/checker files are unchanged by child and main, so the earlier whole `capacity_browser_check --axe` PASS (about 84 s, source `2cc34027`) may be carried with hash provenance; no new broad browser campaign.

## Limits

* Environment: new owned venv `/tmp/ama-80-stack-venv-1111` with editable installs from the scratch tree; mypy and playwright installed there as the owned environment's setup, not as repair of a failure.
* Native, non-independent review. Hosted checks are not run locally.

## Planning Readiness

Ready. Research disposition: executed.

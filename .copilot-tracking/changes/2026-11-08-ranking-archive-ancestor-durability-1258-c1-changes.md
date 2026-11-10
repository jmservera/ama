---
title: Ranking archive ancestor durability 1258 correction 1 changes
description: Source and test changes that remove the writable-parent cutoff and honor an archive mount point
ms.date: 2026-11-08
---

Refs #1258. Start head `cbb1cc5bbb415b7a74fea3b708fcb07b14b69d92`; Main `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (fetched, unchanged). Earlier Changes records are historical and not edited. Plan: [c1 plan](../plans/2026-11-08-ranking-archive-ancestor-durability-1258-c1-plan.md). Scratch: `/home/azureuser/.local/share/ama/gates/g1258-c1-light-1108` (own venv, non-editable out-of-tree install, `ZF_DATA` synthetic under it, external pip cache and `TMPDIR`).

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: `_ancestors()` no longer stops before a parent that is not writable; returns an empty chain when the resolved archive is itself a mount point; otherwise parents nearest first through the first mount point or the root. `publish` docstring updated. `_confirmed`, messages, runner and API are unchanged.
* `src/core/tests/test_ranking_publication.py` (`AncestorDurabilityTests`): added `test_failed_ancestor_then_permission_change_retry_stays_unconfirmed` (non-root chmod fixture, restored in `finally`, skipped as uid 0), `test_mocked_denied_access_does_not_skip_any_ancestor_sync` (mocked `os.access`, two subtests), `test_archive_that_is_itself_a_mount_point_is_not_synced_past_its_filesystem` (mocked `ismount`), `test_required_ancestor_open_failure_is_reported_not_skipped` (pins existing behavior; passed before the fix). Replaced the cutoff assertions: `test_chain_stops_after_a_mount_point_ancestor` and `test_non_writable_ancestor_is_still_synced_through_a_read_only_handle`; removed the redundant mocked-root test.

## Red before the fix (unfixed install, raw log `red.log`, sha256 `74261f05ea7bd0ab27a4f22510e0d8fb1b71febb06d046023b8f6268e61f91ff`)

`python -m unittest test_ranking_publication.AncestorDurabilityTests -v` from `src/core` with `PYTHONPATH=tests`: Ran 13, FAILED (failures=3, errors=1), exit 1. Failing: the archive-mount test (ERROR: host parent `b` synced and faulted), the permission-change retry (FAIL), and the mocked denied-access test for `a` and for `b` (two FAIL subtests). Not a fake red: the open-failure test and the pre-existing tests passed.

## Green after the fix (reinstalled non-editable, import origin `.../g1258-c1-light-1108/venv/lib/python3.12/site-packages/zava_forward/core/ranking_publication.py`)

* Core `test_ranking_publication test_ranking_publication_runner`: Ran 89, OK, exit 0 (`green-core.log`, sha256 `c7aa39bab498f3119bae8a43a5b447ba3f32787ed509d1527108c42a2710bac5`). `AncestorDurabilityTests` 12 tests OK, none skipped as uid 1000.
* API `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py`: Ran 23, OK, exit 0 (`green-api.log`, sha256 `118822cf0317c9fabfb63fd51c9f7e03a279940ea18c01770c90a3c3744ca45d`). Verbose run `green-api-503.log` shows the 503 tests executed, not skipped (readiness L2): `test_unsupported_hard_links_are_a_storage_failure_not_an_authorization_one` and `test_link_and_cleanup_failure_is_logged_and_path_free`, both asserting status 503.
* `ruff check src/core src/api`: exit 0; `ruff format --check` on both changed files: clean; `mypy -p zava_forward.core.ranking_publication`: no issues.
* An earlier API invocation with the wrong module path failed with `ModuleNotFoundError` (exit 1); it was a command error, retained in `green-api.log` history only as the first run, and corrected by using `discover`.

## Readiness dispositions

* M1 (stale active state): superseded by the dated correction state in `.copilot-tracking/rpi-sessions/2026-11-08/ranking-archive-ancestor-durability-1258-state.json`; the cbb1cc5b receipt passed but current functional findings block publication and it is now historical.
* L1 (unchecked pre-gate F1-F4): the pre-gate plans stay unchanged and unticked as history. The correction plan and this record supersede them.
* L2 (503 locator): located and executed as above; criterion 4's 503 evidence is the two tests named, passing in this run only (a fresh FULL is pending).

## Not done

No FULL, `--all`, `--changed`, SQL, browser, Docker, scanner, model or Azure work. No push, PR, issue or board change.

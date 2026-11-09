---
title: Ranking archive ancestor durability 1258 correction 2 changes
description: Mount-table ancestor boundary replacing os.path.ismount, with raw red and green evidence
ms.date: 2026-11-08
---

Refs #1258. Start head `e40a89ed469292965bb6aabbd63dc46ddd19d899`; planning records committed first as `e641b181e5d37c757c7c413c6bedb602678f8f02` (research, plan, one independent critique, all before any code or test edit). Main `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (fetched, unchanged). Plan: [c2 plan](../plans/2026-11-08-ranking-archive-ancestor-durability-1258-c2-plan.md). Earlier records are unedited history, including the correction 1 critique-after-draft deviation and its broad ignored-file cleanup, which this correction did not repeat.

Scratch (new, refused if existing): `/home/azureuser/.local/share/ama/gates/g1258-c2-light-1108` (own venv, non-editable installs of `src/core`, `src/agents`, `src/api`, external pip cache and `TMPDIR`, synthetic `ZF_DATA`). No private data, no `uv`, no `PYTHONPATH` beyond the documented tests path.

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: new `_read_mountinfo()` and `_active_mounts()` (byte-safe parse, first ` - ` separator, at least six head fields, octal unescape, mounts hidden by a later mount at the same or an ancestor path dropped, any malformed line raises `OSError`). `_ancestors()` uses the mount table instead of `os.path.ismount`; unknown mount data raises `OSError`, which `_confirmed` already maps to `DurabilityUnconfirmedError` (record kept, audit and 409 unchanged). Docstrings updated. Runner, store, API production code unchanged.
* `src/core/tests/test_ranking_publication.py` (`AncestorDurabilityTests`): `mount_table()` helper and `mounts()` patch; rewrote the two `ismount` mocks; added archive-inside-a-mount, subvolume (mocked `ismount` true, not in the table), hidden-mount, unreadable-table, parser and malformed-line tests.
* `src/api/tests/test_ranking_publication_wiring.py`: `test_unreadable_mount_table_is_audited_as_unconfirmed_and_retry_is_sound`.

## Red on the unfixed e40 install (raw logs, sha256 in parentheses)

* Core `python -m unittest test_ranking_publication.AncestorDurabilityTests -v` (`PYTHONPATH=tests`): Ran 18, FAILED (failures=4, errors=6), exit 1 (`red-core.log` `0baae221...cc9`). Errors: archive-itself mount (host parent faulted), archive-inside-mount, parser (helper absent, 4 incl. 3 subtests). Failures: mount-ancestor stop, hidden mount, subvolume (chain stopped at the mocked boundary, no unconfirmed), unreadable table (reader not used).
* API `discover -s tests -p test_ranking_publication_wiring.py -v`: Ran 24, FAILED (failures=1), the unreadable-table test (`red-api.log` `bc911e26...f21a`).
* Behavioral reds use `patch.object(..., create=True)` so they exercise the old `ismount` code rather than only failing on a missing attribute.

## Green after the fix (reinstalled non-editable; installed module sha256 equals source `b784f2bb7442777e261b7e8ef7b82a6d77251c0082dc51923eafacd99790453b`; origin is the scratch venv site-packages)

* Core `test_ranking_publication test_ranking_publication_runner`: Ran 95, OK, exit 0 (`green-core.log`). `AncestorDurabilityTests`: 18 OK, no skips as uid 1000.
* API `test_ranking_publication_wiring`: Ran 24, OK, exit 0 (`green-api.log`), including the two 503 tests from correction 1.
* `ruff check src/core src/api` passes; `ruff format --check` clean; `mypy -p zava_forward.core.ranking_publication` no issues.
* An earlier core ruff reformat of the source was applied before the green run; no other command failed.
* Real filesystem tests read the host `/proc/self/mountinfo` and passed.

## Correction to correction 1

The c1 Review's single "fail-closed" label covered two different cases. Bind mounts (PC-001) were a false-failure risk; Btrfs subvolume roots (PC-004) could omit a possibly unsynced parent, a false-confirmation risk. This record supersedes that label. Both are addressed by the mount table. The c1 Review is not edited.

## Not done

No FULL, `--all`, `--changed`, SQL, browser, Docker, scanner, model or Azure work; no real mount, sudo or kernel change. The shared FULL lock holder was not inspected or polled.

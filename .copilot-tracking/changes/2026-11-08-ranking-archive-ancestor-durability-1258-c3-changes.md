---
title: Ranking archive ancestor durability 1258 correction 3 changes
description: Source, test and evidence changes for correction 3
ms.date: 2026-11-08
---

Refs #1258. Correction 3 implemented after the one independent critique (Revise) and its dispositions. Start a0038709874ffdc3200b9ac9dc3fb074ce425c43; planning commit c577eea9e precedes all source and test edits. `origin/main` is 3c57a02d4d2ef61f6922436025b245c8a97e2694; `ranking_publication.py` is identical to f548b65f there, so no integration was needed or done.

## Source: `src/core/src/zava_forward/core/ranking_publication.py`

* `publish` opens the archive folder once (after `makedirs`) and runs everything through it. `_publish_held` stages, links (`os.link` with `src_dir_fd` and `dst_dir_fd`), reads an existing record (`_existing(held, name, path, snap)`, which also returns the record inode) and removes its own stage (`_remove(stage, held)`) with relative names. Staging, loser, cleanup, owner-only mode and original-date behaviour are otherwise unchanged. `_DIR_FD_OK` is evaluated at import; where it is false publication refuses with ENOSYS before writing anything.
* `_mount_id(fd)` and `_parse_mount_id` read `mnt_id:` from `/proc/self/fdinfo/<fd>` strictly. `_walk` follows `..` from the held descriptor and stops at the filesystem root or before the first parent on another mount; bind mounts are boundaries, Btrfs-subvolume-shaped device changes are not. Errors are raised.
* `_confirmed(outcome, ino, archive_dir, held)`: check the path still names the held folder and the name still holds the recorded inode; walk; sync held then parents nearest first; walk again and compare `(st_dev, st_ino, mnt_id)`; check again. Any difference or error is `DurabilityUnconfirmedError`.
* Removed: `_fsync_dir`, `_read_mountinfo`, `_active_mounts`, `_ancestors`, the c2 mountinfo parser and its escape handling.

## Tests

* Core (`test_ranking_publication.py`): added a `mount_ids` seam helper and tests for path swap before and after the link, record removed or replaced during the syncs, mount id change between walks, bind-mount shape, mount-root boundary, device change with the same mount id (retained-shape check, passes on both sources), unreadable mount id, strict parsing, a real fdinfo read (skips without `/proc`), and refusal without descriptor-relative calls. Migrated: the ancestor open-failure test now fails the `..` open from the held chain; `test_stage_already_gone...` accepts `dir_fd` keywords; the source assertion expects `os.unlink(stage, dir_fd=held)`. Removed with the mechanism: `mount_table`, `mounts()`, chain-stops, archive-inside-a-mount, subvolume via `ismount`, hidden-mount and the two parser tests (their behavioural intent is covered by the new mount-id tests except the hidden-mount rule, which no longer exists).
* API (`test_ranking_publication_wiring.py`): the c2 unreadable-mount-table test now faults `_mount_id`; it keeps the record and original date, path-free 409, committed_unconfirmed audit and sound retry assertions.

## Red then green (scratch `/home/azureuser/.local/share/ama/gates/g1258-c3-light-1108`)

| Run | Source | Result | SHA256 of log |
| --- | --- | --- | --- |
| red-core.log | installed a0038709 module (sha b784f2bb...453b, from the c2 venv, read only) | 28 tests, 6 failures, 5 errors; every new behavioural test fails (path swap, replaced and removed record, mount-id change, bind and mount-root shapes, unreadable id, ENOSYS refusal, parser and real-fdinfo by missing function) | a0eb0c57f3cbfb42275202129ffea2bb4aa35b8e6fd70fd33ac998d79bc9b6e5 |
| red-api.log | same | 24 tests, 1 failure (unreadable mount id confirmed with 200) | 3304950ce2462c962ae3fca2af4d9dbaf55884bc4be9ad8ac641f5bd18087e64 |
| green-core-attempt1-dirfd-gate.log | edited, first draft | 26 errors: `os.supports_dir_fd` was evaluated per call while tests replace `os.link`; fixed by evaluating once at import | f482af61e43e97f7117b4c20cdf6c7f0c3f5a10c113a0c38063fa4a54f94d155 |
| green-core-attempt2-one-test-migration.log | edited | 1 error: a fixed two-argument fake `os.link`; test migrated | da11e4de46a3ff29b3cad608264d83c6e51687117db8390a2ec5f143aba4c3bc |
| green-core.log | edited, installed sha abd3ea66d5d3fd46b1a8876b4834c221c40336305a2d8c41cb9beca9ce3a07fe equals the tree file | 57 tests OK, 0 skipped | d211ad2f59dcd9db1fdd40dac5b52b066255de0ce2eaca5e2e556969c2c082c8 |
| green-api.log | installed edited core | 24 tests OK | 7ef8394020fdef7c8b780dded1f230386d541f10dba45bd4fdb7c3b13ad70b7c |

The recorded red run used the earlier form of the refusal test (patching `os.supports_dir_fd`); the committed form patches `rp._DIR_FD_OK`, which on a0038709 fails by `AttributeError`. Static: ruff check and format check clean on the three files; mypy on the module clean.

Commands: core from `src/core` with `PYTHONPATH=tests python -m unittest test_ranking_publication`; API from `src/api` with `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py`; venv `.../g1258-c3-light-1108/venv`, distributions pip installed, TMPDIR and ZF_DATA under the scratch directory, no private data. No gate, SQL, browser, Docker, scanner, model or Azure work was run.

## Honest limits

* PC3-1 (move out, sync, move back, ABA) is not closed and no test claims it is; it is returned as a Blocking platform-contract decision in the critique record.
* All mount shapes are mocked at the `_mount_id` seam. The path-swap, record replacement and real fdinfo read use real files; no real bind mount, Btrfs subvolume, power loss, chroot or overlayfs case was run.
* R1 real power loss, R4 sync cost (now two walks and extra `/proc` reads per confirmation), pre-existing operator symlinks, execute-only ancestors and deployment permissions remain unproved. No chmod broadening.
* The record-inode check follows a symlink at the final name, as the earlier read did; operator symlinks stay unproved.

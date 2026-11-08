---
title: Ranking archive ancestor durability 1258 correction 2 plan
description: Plan to use the mount table instead of os.path.ismount as the ancestor sync boundary
ms.date: 2026-11-08
---

Tier FULL for final publication. This correction runs LIGHT only: bounded synthetic unit tests, one worker, no gate runner, SQL, browser, Docker or scanner; the shared FULL lock is held elsewhere and is not polled. Base `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. Research: [c2 research](../research/2026-11-08-ranking-archive-ancestor-durability-1258-c2-research.md). Details inline. Sequence is strict: critique before any code or test edit.

* [x] C2.1 Critique and dispositions (one independent execution), recorded before edits. Correction 1's late critique stays disclosed history.
* [x] C2.2 Failing-first tests in the existing files, run on the unfixed e40 install with raw output kept: bind-mount-archive with a faulting host parent (mount table lists the archive; `ismount` is false), Btrfs-like subvolume (differing `st_dev`, not in the mount table; chain must continue past it and fault on the parent), mount data unavailable or malformed gives `DurabilityUnconfirmedError` with the record kept (core), and the API-level unconfirmed audit stays through the existing parent-fault test.
* [x] C2.3 Fix in `src/core/src/zava_forward/core/ranking_publication.py` only: a private `_mount_points()` reading `/proc/self/mountinfo` with octal unescape and strict parsing, used by `_ancestors()` instead of `os.path.ismount`; docstrings updated.
* [x] C2.4 Update tests that mocked `os.path.ismount` (`test_chain_stops_after_a_mount_point_ancestor`, the c1 archive-mount test) to patch the mount-table reader; keep real-filesystem tests unchanged.
* [x] C2.5 Paired green: Core `test_ranking_publication` and `test_ranking_publication_runner`, API `test_ranking_publication_wiring`, ruff, mypy; reinstall non-editable into a new scratch venv and prove installed module bytes equal the edited source (sha256).
* [x] C2.6 Changes and one authored Review superseding the c1 "fail-closed" label for both cases. Commit with the repository-local privacy-safe identity.
* [ ] C2.7 Final FULL pending. Proposed new short external output `/home/azureuser/.local/share/ama/gates/g1258-c2-full`; validate new and at most 58 bytes at admission; no tracked edit after a passing receipt.

## Decisions

* D6 mount boundary: the mount table, not `st_dev` or `ismount`. Unavailable or malformed data is an `OSError` through the existing unconfirmed path, never success-shaped.
* Platform: Linux mountinfo. Non-Linux runs report unconfirmed; any wider platform support needs a human decision (reported, not assumed).
* D3/D5 from correction 1 unchanged: no permission cutoff, extra steady-state syncs.
* Out of scope: store, runner, API production, `#1259` path-health, schemas, policies, infra, real mounts, chmod broadening.
* Cleanup: only explicit scratch paths created in this run; no `git clean`.

## Unproved and carried

R1 real power loss, R4 overhead, pre-existing operator symlinks, PC-003 execute-only ancestors and deployment permissions.

## Critique dispositions

Revise, one run, before any code. PC-001 applied: a mount is active only when no later mountinfo line has the same or an ancestor mount point; hidden entries are ignored (walk continues). PC-002 accepted as an unproved operational precondition (stable topology). PC-003 applied: byte-safe parsing, first ` - ` separator, octal unescape, every parse or decode error becomes `OSError`. PC-004 applied: added parser, overmount, bind-subdirectory and API reader-failure tests; red expectations per test are in the critique. Test list for C2.2 is extended accordingly. See the [c2 critique](2026-11-08-ranking-archive-ancestor-durability-1258-c2-critique.md).

---
title: Issue 1231 research (ranking archive concurrent-writer metadata)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 04:41Z, before any source or test edit in this worktree. This is a new scoped issue (#1231), not a resumption of #79 and not permission to repurpose #79 artifacts. The original #79 r11 diagnosis under `/tmp/79-concurrency-r11-1106/` is read-only and is not edited. Its Research and Plan (04:25:02Z) predate its probe creation (04:25:11Z) and execution (04:25:14Z). Its author Review's broad "no overwrite" statement is qualified here by the narrower probe actually run (below), not changed there.

## Identity and pins (intake)

* Branch `fix/ranking-archive-concurrent-writer-metadata`, head `397419724e68b24bce879512a24c7df430177f87`, tree `c728049e33a3a0e20d9a7bf16b3738fabfbc14d7`, ignored-inclusive status empty.
* Parent #79 local branch `feat/ranking-publication-runner-79` at that exact head (not yet remote); its parent #73 `feat/case-workbench-integration-73@ead177ef90d24666557708ea344848a1be43bdf8`; reviewed main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Eventual PR target is the #79 parent, not main. Nothing fetched, moved or rebased.
* Research disposition `executed`.

## Original evidence read (unchanged)

* Issue #1231 body and readback (coordinator session files `79-r11-archive-race-issue-body-r32.md`, `ranking-archive-race-created-r32.json`). Label `bug`, parent #79 link confirmed by coordinator. The referenced backlog-planning instructions file was missing and was not loaded.
* Original r11 files: probe.py `f2fca244...c7017a`, research.md `6be862cd...`, plan.md `0811ab29...`, review.md `aa1c7a10...`, findings.md `e2ed061b...`, probe1.log `3214a753...`, probe1.exit `0`; control and interleave fixtures each 504 bytes (control `5ee9e737...a82c08`, interleave `8fd0b0a1...c832e`).
* Confirmed by that probe: one deterministic two-thread interleaving in one process on the local filesystem. A returned `published`, written True, 2026-11-05; the retained record said 2026-11-06; B got a real `FileNotFoundError` converted to `publish_failed`; verify showed no problem; B's sequential retry was `already_published` with 2026-11-06. Not shown: lost publication, overwrite of a finished record, likelihood, separate processes, Windows, network filesystems, production.

## Source read (child worktree, hashes at intake)

* `ranking_publication.py` `83304551...eed76ad`: `publish` validates, `makedirs`, derives the name from policy version, as-of and hash (not the date), `os.path.exists` pre-check, then writes the single shared `<final>.tmp` and `os.replace`. `verify` lists only `ranking-*.json`, so any `.tmp` is invisible to it. The module docstring and a test (`test_module_has_no_clock_and_no_delete`) state and scan for "never deleted here" (scan words include `unlink`, `os.remove`, `rmtree`).
* `ranking_publication_runner.py` `d4de4197...`: `run("publish")` verifies, skips the capacity check when the target exists, calls `publish`; `OSError` becomes `publish_failed`. No locking.
* `store.publish_ranking_snapshot` calls `publish` under the in-process `self.lock` (RLock), so threads in one API process are already serialized there; the runner and CLI path and separate processes are not.
* Tests: `test_ranking_publication.py` (`4206a16a...`) and `test_ranking_publication_runner.py` (`e0c0b446...`).

## Root cause (confirmed by reading plus the original probe)

The pre-check `exists` and the write are not atomic and the staging name is shared by all writers of one snapshot. Equal-length content (dates differ in digits only) lets a later writer rewrite the staged inode, so the first `os.replace` publishes the other caller's bytes while its own caller is told its own date. `os.replace` also overwrites. By the same reasoning (not probed) a contender delayed between the pre-check and its replace could overwrite an already finished record with a different date. This is labelled reasoned, not confirmed.

## Repository atomicity and locking patterns

* `store.save` and `ranking_snapshot` use fixed `<path>.tmp` plus `os.replace` (overwrite-intended mutable files, in-process lock). Not applicable to an immutable no-overwrite record.
* `tools/rpi-checks.py` and `src/api/checks` use `fcntl.flock` for non-blocking process locks (POSIX only, local developer and gate tooling, not the product data path).
* `tools/tracking_retention.py` uses `O_CREAT|O_EXCL|O_NOFOLLOW` for exclusive creation.
* No `os.link`, hard link, `mkstemp` or advisory lock exists in product code. Hard links are not used or documented anywhere.

## Supported archive filesystem and deployment contract (evidence)

* Archive placement: `Store._ranking_archive()` is `ranking-archive/` beside the per-user `ZF_DATA` file or the database path; the runner takes an explicit `--archive DIR` and reads no default. README: no SQL table holds the archive; retention and scheduler are unset deployment/Legal decisions.
* Container: `src/api/Dockerfile` sets `ZF_DATA=/data/zavaforward.json`, `ZF_STATE=/state` ("a writable volume at /state"). Infra defines no volume or mount for `/state` or `/data`; the only Azure Files mount in infra is the read-only certificate share of the simulator job. So the production archive filesystem is not defined anywhere in the repository.
* Platforms: CI and container are Linux (`ubuntu-latest`, self-hosted linux); the local gate and its tests are POSIX (`fcntl`, util-linux `flock`). No Windows or network-filesystem support is claimed or tested. No document names a hard-link requirement or prohibition.
* Existing code already relies on same-directory atomic rename on a local POSIX filesystem. No concurrent-writer guarantee is claimed.

## Design options considered

1. Unique per-writer staging file (exclusive create, same directory, name that `verify` ignores) plus `os.link(stage, final)` and removal of the owned stage. Atomic on POSIX local filesystems (ext4, xfs, overlayfs, tmpfs, NFS), no lock, no stale-lock state, no dependency, no overwrite possible (`FileExistsError`), content is complete before the final name appears. The winner returns its own date; a `FileExistsError` loser reads the finished record and returns its date with `written=False`. Requires hard-link support. SMB/CIFS mounts (for example Azure Files over SMB) generally do not support hard links; there `os.link` would raise `OSError`, surface as `publish_failed` through the existing runner refusal and leave the archive unchanged. That is a loud refusal, not a silent fallback or data loss, and no such mount is defined or supported today.
2. `O_CREAT|O_EXCL` on the final name and write in place: a reader or loser can see a partial record and a crash leaves a truncated permanent record. Rejected (weaker than today's atomic replace).
3. Exclusive lock file with `O_EXCL`: stale lock after a crash needs an owner recovery rule. Rejected.
4. `fcntl.flock` on the archive: POSIX-only like option 1, unreliable on network filesystems, a new lock-file artifact, no benefit. Rejected.
5. Keep `os.replace` and only add a unique stage plus a second exists check: still overwrites. Rejected.

## Gate analysis

* Material platform change? Option 1 narrows one assumption (hard-link support on the archive directory) on a deployment that the repository has not defined, within a documented Linux/POSIX local-file contract. No supported platform is lost today; the failure on an unsupported mount is explicit and fail-closed. Judged an ordinary implementation detail inside the existing contract, not a stop gate, with an explicit qualification and an open follow-up question for the owner: if the production archive is mounted on a filesystem without hard links (for example Azure Files SMB), a different mechanism must be chosen before deployment. This is recorded as an unresolved deployment question, not an approval.
* Module invariant: the helper says and a test scans that it never deletes. Removing its own staging file needs `unlink`. The invariant protects archived records. The narrowing is: never delete an archived record; remove only this call's exclusively created staging file. The scanning test will be narrowed to forbid `os.remove`, `rmtree` and any unlink other than the single owned-stage removal, and behavioural tests will assert that an existing record and foreign temporary files survive. This is a purposeful guard refinement inside the helper's own scope and is flagged for the independent assessor; it is not an owner approval.
* Retention, policy, freshness, approvals are untouched.

## Planning Readiness

`Ready`, with the two flagged qualifications above (hard-link support; the unlink-scan guard refinement).

## Environment and limits

* Heavy boundary: another workstream (#188) owns the heavy wrapper; this task takes no heavy lock and runs only light focused tests, Ruff and mypy. No FULL, SQL, browser, container, install or cleanup.
* `/tmp/zf79venv` is read-only here. Its editable `zava_forward` namespace points at the sibling `issue-79-publisher` worktree, so the child must be put first on `PYTHONPATH` and proved by `__file__` and hash before any result counts.

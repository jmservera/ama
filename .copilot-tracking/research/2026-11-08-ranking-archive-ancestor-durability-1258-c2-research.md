---
title: Ranking archive ancestor durability 1258 correction 2 research
description: Verification of the same-filesystem bind mount and Btrfs subvolume boundary defects left by correction 1
ms.date: 2026-11-08
---

Refs #1258. Correction 2. Research disposition: executed, read-only (no code or test drafted; this record precedes the plan and critique). Planning Readiness: Ready.

## Start state

* Head `e40a89ed469292965bb6aabbd63dc46ddd19d899`, tree `69b5d0fa70819e317e168f6e06ea0e5c204622bc`, ignored-inclusive clean (0 entries). `origin/main` `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (fetched, unchanged).
* The correction 1 records ([critique](2026-11-08-ranking-archive-ancestor-durability-1258-c1-research.md) siblings: c1 critique, Changes, Review) are read and stay unedited history. The cbb1cc5b receipt, the e40 author Residual outcome and both earlier critiques are not regraded.

## Findings carried from correction 1

* H1 permission cutoff: locally fixed with retained red 13 (3 failures, 1 error) and green Core 89, API 23. Not reopened.
* PC-001 (blocking in the c1 critique): `os.path.ismount` compares `st_dev` and inode with the parent, so a bind mount of a directory on the same filesystem is not recognised (same `st_dev`). If the archive is a bind mount, the walker climbs into host ancestors and may fault on them.
* PC-004: a Btrfs subvolume root has a different `st_dev` from its parent but is not a mount. `ismount` returns true, so the walker stops there and omits a parent entry that may be unsynced.
* Correction: the c1 Review labelled both fail-closed. That is unsupported. PC-001 is a false-failure (extra sync can fault, reported unconfirmed). PC-004 is a possible false confirmation, which breaks the issue's first criterion. This record supersedes that label; the c1 Review is preserved unedited.

## Mechanism research

* `st_dev` alone cannot be the boundary: it is the wrong answer for both cases (misses the bind mount, falsely stops at the subvolume).
* Linux `/proc/self/mountinfo` lists real mount points (field 5, octal escapes) including bind mounts, and does not list an unmounted Btrfs subvolume. Field 4 is the root within the source filesystem, so same-source bind mounts appear as separate mount entries.
* Existing prior art in this repository: `tools/rpi-checks.py` (about lines 745-770) parses `/proc/self/mountinfo` with `re.sub(r"\\([0-7]{3})", ...)` octal unescape and fails closed with a `GateError` when it cannot resolve. That is a tool, not a runtime package, so it is not importable by core; the same small unescape logic is the reference for a private helper. No mount helper exists in `src/`.
* Supported platform: the demonstrator and its containers are Linux (this host ext4, Python 3.12; project requires 3.12). Required behavior when mount data is unavailable (no `/proc`, unreadable, malformed) is the existing explicit unconfirmed path, not an `ismount` fallback, because a fallback reintroduces the PC-004 false confirmation. Trade-off: a non-Linux developer run would report `committed_unconfirmed` for every publication. The hard-link requirement already restricts supported storage; a platform decision beyond Linux is a human decision and is reported, not assumed.

## Candidate design (for the plan)

Replace both `os.path.ismount` calls with membership of the real path in the set of mount points read from `/proc/self/mountinfo` for this call. Empty chain when the resolved archive is a mount point. Otherwise parents nearest first, including the first mount point, or the root. Any failure to read or parse mount data raises `OSError` from the walker, which `_confirmed` already maps to `DurabilityUnconfirmedError` (record kept, path-free message, audit and 409 unchanged).

Considered and rejected: `st_dev` comparison (wrong for both), `statfs`/`findmnt` subprocess (new dependency), keep `ismount` with a documented limit (rejected by the owner brief), per-call cache (stale risk; mounts are read each confirmation, a few hundred lines).

## Limits stated now

* A mount point of a different but same-device bind within the chain after the first is not an issue; only the first boundary matters.
* Mocked mountinfo is not a real mount; no mount creation, sudo or kernel change is made.
* R1 real power-loss, R4 sync overhead (plus one `/proc` read per confirmation), pre-existing operator symlinks and PC-003 execute-only ancestor and deployment-permission acceptance remain unproved.
* Mount points containing newline or other escapes are handled by the octal unescape; a malformed line is an error, not skipped.

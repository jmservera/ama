---
title: Research, issue 1259 live run 8 (real-filesystem angle)
ms.date: 2026-11-23
---

Disposition: executed. Scope: unticked AC4 (regressions, failing-first) and AC5 (process gate).

Prior workers (git log origin/main --grep 1259: #1461, #2006, #2066, #2148, #2151, #2177, #2278, #2285, #2288, #2296) re-ran the existing `UnusableArchivePathTests`. Those cover a regular file, a dangling link, a dangling ancestor and a stat failure that is mocked with `patch("os.stat")`.

New angle: classifications that only a real filesystem produces and no test exercises.

* Archive below a regular file (lstat raises ENOTDIR, not FileNotFoundError).
* Symlink loop as archive and as ancestor (ELOOP, errno 40).
* Real EACCES on an unsearchable parent (chmod 0 as a non-root user), replacing the mock.

Probe on head 5c08bedd8f through `runner.run` for verify, schedule and publish: every case returns `problem`/`problem`/`refused archive_unreadable`, `due` null and no temp-root path in the JSON. Behaviour is already correct, so no src change; gap is test coverage only.

Live: apps are image-based and no ranking job is deployed, so Azure cannot prove this; no Azure change.

Planning Readiness: Ready.

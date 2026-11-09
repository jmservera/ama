---
title: Ranking archive ancestor durability 1258 FULL continuation research
description: Currency and validation research before the final FULL gate for issue 1258
ms.date: 2026-11-08
---

Research disposition: executed. Planning Readiness: Ready.

* Start: branch `fix/ranking-archive-ancestor-durability`, HEAD `6d793bc3ad3fd8427f745530a633bb1e553ec0ef`, tree `b614f00833645a952e5e90867e6e9b15371119d8`, ignored-inclusive status clean. `git fetch` confirms `origin/main` is `f548b65f4aa31eb92a2cc9cb801130e422daed7f`, equal to the prior reviewed base, so no merge and no source currency change is required.
* Issue #1258 is open; body re-read and unchanged in substance (five criteria, FULL tier, parent #79 as source ordering). #1259 is not an implementation dependency; its worktree is not touched.
* Resources before admission: 4 CPUs, about 8 GiB available RAM, about 39 GiB free on the root filesystem; the shared heavy lock file has no holder visible to a `lsof` check of that file and no `rpi-checks` process other than this session's own shell probe. `--jobs 2` needs 9 GiB available and four CPUs, so it may admit one worker; admission is never weakened.
* Original and continuation artifacts (research, plan, details, critique, changes, review, cont-*) are preserved. Original Review outcome Residual work and R1 (no real power-loss proof) and R4 (extra-sync visibility) stay open.
* Gate scope: FULL via `tools/rpi-checks.py --all`, external output only; no source change is planned unless the gate exposes a real defect.

---
title: "#184 C4 plan amendment: full local gate"
ms.date: 2026-11-08
---

Details: [details](../details/2026-11-08-live-simulator-cohort-control-184-c4-fullgate-details.md).

* [ ] Coordinator admits the gate non-queued after #1292 releases the heavy lock.
* [ ] Clean exact-head worktree of f28e278d (or the later reviewed head), no deletion of ignored files.
* [ ] Fetch origin/main and run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-dir>`.
* [ ] Verify the receipt with `--verify-receipt <receipt.json> --base <current-origin-main-sha>` immediately before push and independent exact-head assessment.
* [ ] Any later commit, rebase, base movement or dirty input invalidates the receipt.
* [ ] Missing SQL, browser or scanner prerequisites block publication; no cloud fallback.

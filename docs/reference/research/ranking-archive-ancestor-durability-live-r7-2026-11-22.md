---
title: Ranking archive ancestor durability live evidence r7
description: Demo evidence for the remaining acceptance criterion of issue 1258
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only. Head and origin/main are both 10cad2e413; `src/core` is identical between them. Issue 1258 is open and only the last criterion is unticked.

Evidence recorded in `issue-1258-live-r7-2026-11-22/`:

* `tests.txt`: from `src/core`, `PYTHONPATH=src:tests python3 -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner -q` ran 110 tests, OK.
* `strace-order.txt` and `run-result.txt`: a real `publish` into a missing nested archive on a local temporary filesystem (script `publish-first-run.py`). The trace shows `mkdir` of each ancestor, `fsync` of the staged file, `linkat`, then `fsync` of the archive folder and of each ancestor up to `/`, all returning 0. The call returned `written`.

Limits: this shows syscall order on one filesystem. It is not crash or power-loss proof and says nothing about Azure storage. Live Azure was not used because the criterion concerns local directory-entry durability, which no Azure resource can show; nothing was created or changed there.

The unticked criterion bundles four gates. Original RPI is evidenced by the dated artifacts in this commit. A current FULL receipt, an independent exact-head review and hosted checks remain unproven: no source changed (so FULL is not triggered), `rpi-checks.py --all` is barred for this worker, and nothing may be pushed. Per-criterion table: `.copilot-tracking/changes/2026-11-22/issue-1258-live-r2-changes.md`.

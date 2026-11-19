---
title: Research for issue 1258 (live demo run 3)
ms.date: 2026-11-18
---

Opening note. Task `1258`, slug `issue-1258-live`, branch `test/archive-ancestor-live-20261118T1855Z`, base `origin/main` cfd272051.
Issue boxes 1 to 4 are ticked; only AC5 (original RPI, current FULL receipt, independent exact-head review, hosted checks) is unticked. The prior run-2 note exists under `docs/reference/research/issue-1258-live-closure-r2-2026-11-18.md`.

Plan: confirm on the current head that nothing regressed (tests, mypy, ruff), repeat the real-ext4 `strace` order and kernel fault proof, re-observe Azure demo configuration read-only, and state per criterion what is proven. Tier FOCUSED while no `src` file changes; `rpi-checks.py --all` is not run.

Disposition: Research `executed`.

Findings: Core 110 tests OK, API wiring 36 tests OK, mypy clean (396 files), ruff format/check clean. Real ext4 strace order and EIO kernel injection reproduce run 2. Azure demo API has Blob variables and no ranking archive path variable. Main push CI at 612cbed78 succeeded. Details in `docs/reference/research/issue-1258-live-r3-2026-11-18.md`. Planning Readiness: Ready.

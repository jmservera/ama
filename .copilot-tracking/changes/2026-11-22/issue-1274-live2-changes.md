---
title: Changes, issue 1274 live re-proof (run 2)
ms.date: 2026-11-22
---

Tier: focused (documentation and tracking only; no src, workflow or dependency change). Refs #1274.

## Changes

* Added docs/reference/research/issue-1274-live-evidence-2026-11-22-run2.md, index row and log entry.
* Added dated RPI artifacts under .copilot-tracking/ and replaced the earlier state file content for this session.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Identify failing endpoints and installers | Proven for actionlint (#1243, #1271) and AWF checksums endpoint (#1271); unproven for #1273 | Job logs 128696067639, 128680975934, 128681102295 re-read; 504 on release URLs in bootstrap steps |
| 2 Bounded fail-closed retrieval | Proven (ticked, on main via #1275) | 12 install-actionlint tests OK |
| 3 Regressions and rpi-checks tests | Proven (ticked) | tools.test_rpi_checks 127 OK |
| 4 Real exact-version verification, review, hosted CI | Proven for actionlint 1.7.7 locally (`a.tgz: OK`, binary 1.7.7) and main run 42497999337 success; unproven for AWF 0.28.23 (upstream installer) and hosted CI on a new reviewed head (no push allowed) | Research note run 2 |
| 5 Dependent PR resume route | Proven (ticked) | Earlier notes |

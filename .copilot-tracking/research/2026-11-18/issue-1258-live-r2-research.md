---
title: Research for issue 1258 (live demo run 2)
ms.date: 2026-11-18
---

Opening note. Task `1258`, slug `issue-1258-live`, branch `test/w-1258-live-20261118T1651Z`, base `origin/main` b285d6039.
Issue acceptance boxes 1 to 4 are ticked (2026-11-13 and 2026-11-18 audits). Only AC5 is unticked: original RPI, current FULL receipt/verification, independent exact-head review, hosted checks.

Plan for this run (owner decisions 2026-11-18: synthetic demo, desktop only; live Azure allowed in resource group `ama`, no production change):

* Re-run the ranking publication tests and mypy/ruff on current main.
* Add a real-syscall proof with `strace` on a real filesystem (first publication into a missing nested archive), which the earlier mock-only evidence lacked. This is syscall order, not a crash test.
* Observe hosted checks for current main.
* Check whether Azure holds any ranking archive state relevant to the demo.
* Record per-criterion proven/unproven and separate production-only and FULL-tier needs.

Disposition: Research `executed`. Tier FOCUSED while no `src` file changes.

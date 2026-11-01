---
title: Issue 687 closeout research
ms.date: 2026-11-01
---

Disposition: reused. Planning readiness: Ready.

Evidence:

* PR #689 (merged 2026-11-01): per-read timing and load context in the 60,000-case benchmark, opt-in CPU contention (ZF_BENCH_CONTENTION). Uncontended filtered page about 110 ms; 32 burners on 4 CPUs reached 1,533 ms.
* PR #720 (merged 2026-11-01): opt-in ZF_BENCH_IO_CONTENTION fsync writers reproduced a single-group stall (filtered page 59,647 ms, other groups 61-179 ms), attributing the one-off class to disk contention.
* Threshold assertions remain 1500 ms (src/core/tests/test_sqlreads.py lines 297 and 376).
* Fresh run on main 37283f6c under load1=6.7 on 4 CPUs: filtered page 201 ms, all groups under 300 ms.

Criteria mapping:

* AC1: environment attribution reproduced under defined IO contention; the original 2026-10-23 image-restore cause stays unproven (receipt gone), which the criterion permits as environment attribution.
* AC2: failure output carries timings and load context.
* AC3: threshold unchanged; core ruff, format and mypy pass.

No source change is required.

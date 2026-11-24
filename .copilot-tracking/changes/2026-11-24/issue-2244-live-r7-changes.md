---
title: Issue 2244 live run 7 changes
ms.date: 2026-11-24
---

No source change. Added the research note `docs/reference/research/issue-2244-live-r7-2026-11-24.md` and the dated RPI artifacts. Tier: focused (documentation only); `rpi-checks.py --all` not run. No deployment, drill, SQL access or credential read.

## Per-criterion proven and unproven table

The issue has no tick-box list, so no box was ticked. Criteria C1 to C5 come from the first run note.

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff on start-up lock timeout | Proven by code and tests; live revision carries the code (md5 match); no live lock timeout occurred | research note |
| C2 skip the write lock when the schema is current | Proven by tests and md5 match; replica started in about 41 s with no lock line | research note |
| C3 live API starts without a crash-loop | Proven for 0000061: Healthy, restart count 0, `/healthz` 200 x3, no probe failure | research note |
| C4 long concurrent writer cannot take the demo down | Unproven: needs holding the live write lock, a drill the owner excluded | none |
| C5 lock holder of the 2026-11-22 incident identified | Unproven: past event, no log names it, no SQL lock read | none |

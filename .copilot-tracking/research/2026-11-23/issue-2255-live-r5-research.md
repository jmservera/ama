---
title: Research, issue 2255 run 5 (live)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

Live re-probe on API revision 0000056 (only active, traffic 100): 22 of 22 hazard rows show elapsed hours and a response due time, 0 unknown, 17 overdue, 5 open, 44 owner matches, API total 23. Evidence: [research note](../../../docs/reference/research/issue-2255-live-r5-2026-11-23.md).

First unticked criterion satisfiable by code or tests: survival of the seeded clock across a re-seed. The regression test was absent on this branch (it sits on a sibling branch), so it is added to `src/core/tests/test_seed_merge.py`. The generator change and destructive re-seed stay owner-gated.

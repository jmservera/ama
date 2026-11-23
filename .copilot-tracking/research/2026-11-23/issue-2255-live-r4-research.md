---
title: Issue 2255 live run 4 research
ms.date: 2026-11-23
---

Opening note. Prior runs (r1 to r3) proved clocks on revisions up to 0000055; only the re-seed criterion stayed open. Run 4 re-checks the live revision and re-reads the seeding code path for a fixable defect. Status: Planning Readiness pending.

## Findings

* Live API revision `ca-cutover-test-demo-api--0000055` is the only active revision (100 percent traffic).
* Playwright desktop probe as staff: 22 of 22 hazard rows show elapsed hours with a response due time; 0 unknown; 17 overdue and 5 open; named owner on every row; hazard API total 23. Evidence in `docs/reference/research/issue-2255-live-r4-2026-11-23/`.
* Re-seed survival is not provable for the demo: `SqlStore.merge_seed` is insert-only and the dataset generator is outside this repository (see run 3).
* No code defect found. Research disposition: executed. Planning Readiness: Ready.

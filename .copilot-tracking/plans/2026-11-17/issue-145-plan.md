---
title: Issue 145 plan
ms.date: 2026-11-17
---

1. Add a dated reassessment section to `infra/sql-recovery-runbook.md`: re-measured baseline, backup-redundancy caveat, what unblocks C2 and C4.
2. Extend `infra/tests/test_sql_tier.py` with one case asserting the runbook records the Local-redundancy caveat and keeps the restore status "Not performed".
3. Run `python3 -m unittest infra.tests.test_sql_tier`, `ruff format --isolated --line-length 100 --check` on the test, and review the diff.

Details: [details](../../details/2026-11-17/issue-145-details.md). Critique: executed once, below.

## Critique (single pass)

Verdict: compatible. Do not tick C2 or C4 and use `Refs #145`. Keep the claim about Local redundancy worded as an owner decision input, with the Microsoft Learn doc named for verification. Applied directly.

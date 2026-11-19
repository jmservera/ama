---
title: Issue 108 live r4 changes 2026-11-19
---
Stop outcome: all remaining acceptance criteria are production-only, need a human, or need registering Microsoft.Quota (outside the authorised scope). No source change; artifacts only. Validation: `python3 -m unittest discover -s src/agents/tests -p test_candidate_comparison.py -q` ran 19 tests, OK. Basis for prior live facts: docs/reference/research/issue-108-live-r2-20261119-2026-11-19.md.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Names, versions, quotas in region | Partly proven (r2 live: deployments, versions, capacity, rate limits); subscription quota unproven, Microsoft.Quota NotRegistered |
| 2 | Frozen independent held-out split | Unproven: needs independent labeller |
| 3 | Human detection of seeded critical errors | Unproven: needs authorised participants |
| 4 | Effort and cost vs alternatives | Unproven: needs people and Finance |
| 5 | Hashes, serving version, reviewer protocol | Unproven: needs real held-out batch and reviewers |
| 6 | Actual-call authorization and consent | Unproven: production authority |
| 7 | Real AI/SQL/Azure proof (CON-009/AC-057) | Unproven: production build |
| 8 | Routing or caching one lever, same cases | Unproven: offline gate tested; no lever measured live |

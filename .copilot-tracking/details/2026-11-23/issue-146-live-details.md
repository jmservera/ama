---
title: Issue 146 live details (2026-11-23)
ms.date: 2026-11-23
---

P2: split the single extend in query ai-variance-by-period into two extends so UnreconciledVariance references a prior statement's AzureCostRows. Test in infra/tests/test_monitoring_workbook.py asserts no tile extend references a column defined in the same extend for this query.

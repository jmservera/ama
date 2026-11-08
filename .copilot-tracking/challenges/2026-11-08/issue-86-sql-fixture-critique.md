---
title: Issue 86 resident-control SQL fixture critique
description: One independent read-only critique of the fixture correction research, plan and details, with dispositions
ms.date: 2026-11-08
---

Scope: issue #86 only. Reviewer: rubber-duck agent, read-only, one pass. Verdict as returned: Revise. The seed diagnosis was judged supported and `merge_seed` plausible, pending MSSQL validation.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Baseline conclusion too strong; B1/B2 need unskipped execution and separate observation from diagnosis | Accepted; plan step 3 amended |
| 2 | Blocking | Explicit test import path and origin proof missing | Accepted; plan amended |
| 3 | Non-blocking | Ledger claim must be scoped to the normal-database trigger | Accepted; plan amended |
| 4 | Non-blocking | Fixture invariants: exactly 41 inserted, reopen, preserve assertions | Accepted; plan amended |

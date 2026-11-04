<!-- markdownlint-disable-file -->
---
title: Issue 146 AI-limit evaluator details
description: Phase details
ms.date: 2026-11-04
---

## Details

* `evaluate_ai_limits(usage, limits, expires_at, as_of, approved_by, constructed, price_source, owner)`: per-dimension status; blocked when live limits lack a named approver, limits or clock invalid; cost Unknown without a price source; absent usage Insufficient; usage above limit or at/after expiry is a breach with the owner and runbook `ai-limits`. No clock read.
* `reconcile_events(events, window_start, window_end)`: distinct `event_id` count in a half-open window; duplicates, out-of-window and invalid events reported; invalid window yields no count.
* Tests in `src/core/tests/test_monitoring_coverage.py`.

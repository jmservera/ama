# Research: workbook availability, errors, latency and cost vs budget (Refs #146)

Date: 2026-11-14. Base: origin/main 0999ce7bf. Disposition: executed. Planning Readiness: Ready.

* `infra/monitoring-workbook.json` already has `availability` (AppAvailabilityResults), `requests` (failure percent, weighted p95), `operation-errors-latency`, `cost-and-budget` text (80% actual / 100% forecast, not a hard cap) and `cost-vs-budget` (configured budget, Unknown actual/forecast, Unreconciled variance), plus the PR #1606 AI usage/variance panels.
* Cost is deliberately unreconciled; no billing source is connected. Fabricating spend would break honesty rules.
* Gap: no test proving all four dimensions together. No source gap in the workbook.

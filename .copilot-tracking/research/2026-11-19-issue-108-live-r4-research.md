---
title: Issue 108 live r4 research 2026-11-19
---
Research disposition: reused. Planning Readiness: Ready (stop outcome).

Evidence reused: docs/reference/research/issue-108-live-r2-20261119-2026-11-19.md (live deployments, versions, capacity, rate limits; Microsoft.Quota NotRegistered) and the offline single-lever gate (src/agents candidate_comparison, src/core tokenomics_comparison, both tested).

Finding: every unticked criterion is production-only, needs a human or labeller, or needs a subscription change (registering Microsoft.Quota) outside the authorised scope. The lever gate already exists with tests; measuring a lever needs an authorised live held-out batch.

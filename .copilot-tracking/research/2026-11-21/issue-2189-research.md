---
title: Issue 2189 research - Source CI critical path
---

Research disposition: executed. Planning Readiness: Ready (for an evidence-only outcome).

Findings and per-criterion status are in [docs/reference/research/ci-critical-path-2189.md](../../../docs/reference/research/ci-critical-path-2189.md). Key points: src-api is 22-28 min and dominated by the unit-test step; mssql gating already exists in tools/ci-affected.py; sharding and pip cache are absent; hosted timing cannot be re-measured without a push.

---
title: "Plan: #432 resident adapter usage sink"
ms.date: 2026-11-03
---

Details: [details](../details/2026-11-03-issue-432-resident-usage-details.md)

* [x] 1. Add optional `record_usage` callback to `AzureTopicProvider`; validate with `ai_consumption.usage`; pass counts or None (unknown); contain sink failures.
* [x] 2. Tests: valid, cached, inconsistent and absent usage; invalid reply still records; sink failure contained.
* [x] 3. Focused tests, ruff, mypy (cache /tmp/mypy-432).
* [x] 4. Commit, push, PR with Refs #432.

Stacked slices still routed to owner decisions (see 2026-11-02 research): host wiring of the sink to the ledger, OD-51, spend authority, billing, live admission, pitch.

## Critique (single pass)

* Risk: sink failure after a paid call. Applied: failure is contained, topic outcome unchanged, resident gets the same result as without a sink.
* Risk: raw content leakage. Applied: only validated integer counts reach the sink, never prompt, reply or identifiers.
* Risk: implying cost. Applied: no price, no charge; None means unknown.
* Rejected: wiring the sink to the ledger now; it needs owner scope for an expired, disabled adapter.

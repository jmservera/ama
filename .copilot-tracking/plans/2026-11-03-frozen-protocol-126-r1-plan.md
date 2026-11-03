---
title: Issue 126 round 1 plan
ms.date: 2026-11-03
---

* [x] Slice 1: AI running-cost line and booked-destination value claims in governance.py, API actions, README
* [x] Tests in test_governance.py (JSON and SQL), ruff, mypy
* [ ] Slice 2 (stacked, later): AI economics report and limit breaches in release decisions, after NFR-012 metering exists
* [ ] Slice 3 (later): RAI closure evidence and qualified owner decisions

Details: [details](../details/2026-11-03-frozen-protocol-126-r1-details.md)

## Critique (executed once)

Verdict: compatible. Making the AI line a capture-gate requirement matches "before capture"; existing fixtures updated. Value is never booked by recording; confirmation is a reference, not an AI or system signature. No AI feature is added, so no AI-unavailable path applies.

Tier: focused. The slice touches the SQL-backed store only through the existing governance document (no schema or deployment change) and no security control; the coordinator owns any gate.

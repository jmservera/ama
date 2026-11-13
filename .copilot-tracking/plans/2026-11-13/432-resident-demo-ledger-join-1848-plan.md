---
title: Issue 432 resident demo ledger join plan
description: Plan for F1 and F2
ms.date: 2026-11-13
---

## Phases

* [ ] P1 `test_resident_ledger_meter.py`: add `call_join` helper asserting reserved-to-completed join and content-free canary for advisor question, advisor guidance and topic provider, including failure path.
* [ ] P2 `test_ai_consumption_api.py`: add `read-document` text `call_join` and canary test.
* [ ] P3 `test_ai_call_site_inventory.py`: keep classifications, tighten notes, add guard that no host calls `advisor_meters` (reclassify when wired).
* [ ] P4 Validate (inventory, consumption core and api, resident tests, ruff, mypy), review, commit.

Details: [details](../../details/2026-11-13/432-resident-demo-ledger-join-1848-details.md). Research: [research](../../research/2026-11-13/432-resident-demo-ledger-join-1848-research.md).

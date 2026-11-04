---
title: Issue 79 plan, slice 2
ms.date: 2026-11-04
---

* [x] Phase 1: store methods `publish_ranking_snapshot`, `ranking_publication_status` (manager-only, audited).
* [x] Phase 2: API routes, role inventory entries, HTTP wiring tests.
* [x] Phase 3: README note, log entry, evidence.

Details: [details](../../details/2026-11-04/issue-79-r2-details.md). Stacked next: scheduler (deployment) and retention (Legal), after the owner is named.

Critique (single pass, self-run): the endpoint writes a file, so it is manager-only, idempotent, audited and never overwrites; GET publishes nothing; policy stays unsigned and the status reports `policy_signed: false`. Tier remains focused: no auth, SQL schema, infrastructure or deployment change; flagged that it adds a write route, so the coordinator may judge security sensitivity. Applied directly; no significant issue.

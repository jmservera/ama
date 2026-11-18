---
title: Issue 145 live run 3 critique
ms.date: 2026-11-18
---

Executed once. Verdict: proceed with changes applied directly.

* Risk: probe reads production-like source. Mitigation: read-only SELECTs plus `sp_verify_database_ledger` (read-only); no grants, no writes.
* Risk: resurrection cannot be proven on empty tables and seeding the source is a production-demo change. Decision: report as unproven, no seeding of the source.
* Risk: identifier leakage in raw output. Mitigation: redact server, subscription, identity names in the retained file; keep counts and hashes.
* Risk: orphaned billable resources. Mitigation: delete database and job, then list to confirm.

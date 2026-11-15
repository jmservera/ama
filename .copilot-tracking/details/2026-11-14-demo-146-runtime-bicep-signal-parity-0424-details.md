---
title: Runtime to Bicep signal parity details
ms.date: 2026-11-14
---

* Phase 1: tests assert Bicep marker queries equal `digest_blob.ALERT_MARKER`/`OK_MARKER` and `AI_LIMIT_BREACH`; runbook reason set equals emitted set; platform metrics and poison queue shape; no PII or content tokens and no `project` in alert queries.
* Phase 2: add `request-depth-limit` and `duplicate-attempt` to the calls class in `infra/monitoring-runbooks.md`.
* Phase 3: the two unittest modules and ruff check/format on the new test.

---
title: "Plan critique 144 probes and restart persistence"
ms.date: 2026-11-13
---

Execution: complete (rubber-duck, single pass). Verdict: Revise. Compatible findings applied directly.

* PC-001 heartbeat margin: applied. Test claims only the provider-call margin and idle cadence; no worst-case guarantee.
* PC-002 restart test: applied. Crash before post and crash after post before ack, replacement worker, duplicate-result assertion.
* PC-003 C5 label: applied. Evidence is SQL store reopen; hosted restart stays Unmet.
* PC-004 rollback: applied as explicit Unmet; only configuration is asserted.

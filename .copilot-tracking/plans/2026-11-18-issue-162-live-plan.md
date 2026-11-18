---
title: Plan for #162 live break-glass proof
ms.date: 2026-11-18
---

* Goal: prove or bound criterion 6 on the live demo; docs only, tier FOCUSED.
* Phase 1: read-only config check of `ca-cutover-test-demo-api` for `CHAT_BREAKGLASS_*`.
* Phase 2: Playwright probes of `POST /api/chat/breakglass` with before and after `/api/audit-check`.
* Phase 3: run `test_chat_isolation.py` for the grant path; write the research note, index and log entries.
* Out of scope: setting app config, SQL reads, DPO/Legal review.

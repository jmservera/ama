---
title: Issue 2303 latency review (2026-11-25)
ms.date: 2026-11-25
---

Review executed once on the working-tree diff. Outcome: conformant for the stated goal locally; live proof and the Full gate are routed to later work.

* Correctness: cache key (function, golden SHA-256) keeps the existing chat-failure test valid; deep copies stop callers mutating shared state; lock gives single-flight; state bounded to 8 entries.
* Behaviour preserved: response shape unchanged; missing golden still raises (Dockerfile contract unaffected); verified by 52 endpoint and consumption tests.
* Trade-off recorded: `ai_eval` latency measurements are now a one-time snapshot per process; first request during warm-up waits.
* Open items routed: deploy and re-measure live (needs an owner-approved image build); coordinator Full gate and receipt (criterion 4).
* No material findings open.

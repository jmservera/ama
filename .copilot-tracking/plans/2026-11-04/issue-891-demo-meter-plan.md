---
title: Plan for #891 demo meter seeding
ms.date: 2026-11-04
---

* Slice 1 (this PR): under the owner-approved demo switch only, `chat_admission` idempotently records a synthetic, labelled, one-day, low-cap authority and price for the chat configuration, and the synthetic price may admit a live call for the chat capability only while the switch is honoured.
* Phase 1: new `chat_demo_meter.ensure` in core; wire it in `server.chat_admission` demo branch.
* Phase 2: `Ai.synthetic_price_capabilities` (empty by default) relaxes only the `live` synthetic-price hold.
* Phase 3: real-store regression tests (SqlStore, real `Ai`, real ledger; only the HTTPS transport and token are faked).
* Validation tier: focused. No SQL schema, infrastructure or deployment change, so no gate. The coordinator decides any gate.
* Boundaries kept: default deny without the switch; production never honours it; per-call limits (one call per request root, 20 calls, 100000 tokens, 1 USD synthetic units per day); privacy refs, retention, suspension and refusals unchanged; no approval or consent changes; manual route and rules-only fallback unchanged when the model is unavailable or held.
* Critique: executed once (inline). Finding applied: a synthetic price must not weaken the live hold outside the demo, so the exception is scoped by capability and set only when the switch is honoured; a test proves the hold remains otherwise. Finding applied: seed lazily per admission so the authority renews daily without a restart and a failed seed only logs and leaves the call held.
* Details: [details](../../details/2026-11-04/issue-891-demo-meter-details.md).

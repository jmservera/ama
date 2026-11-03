---
title: Issue 891 round 1 plan
ms.date: 2026-11-03
---

* Slice 1 (this PR): demo-only record and gate in `ai_registry`, `/api/chat/status` demo fields, `chat.js` disclaimer and model-generated label, tests, docs and log.
* Slice 2 (stacked, later): wire `ZF_CHAT_DEMO_ACTIVATION` and `ZF_DEPLOYMENT_PROFILE=demo` into the demo deployment (infra), owner-authorised deploy, warm-up, live check.
* Critique (single pass, self-run): compatible findings applied directly: require the profile marker as well as the switch; never alter the registry entry's unknown authorities; keep refusals, gate and storage refs unchanged; no production/pilot path.
* Details: [details](../details/2026-11-03-chat-demo-activation-891-r1-details.md).

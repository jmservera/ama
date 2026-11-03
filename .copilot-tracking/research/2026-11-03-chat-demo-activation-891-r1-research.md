---
title: Issue 891 round 1 research
ms.date: 2026-11-03
---

* Disposition: executed (code reading). Planning Readiness: Ready.
* Prior delivery: no merged PR or branch commit references #891; nothing to avoid redoing.
* Cause: `server.chat_admission` returns `activation-not-approved` because `ai_registry.authorizes_live(chat-case-conversation)` needs every authority recorded; all are `unknown`.
* Model turns also need stored chat (the three privacy refs); `unstored-ask` never calls a model. Refs already exist for the demo per chat-demo-storage-approval-2026-11-01.
* Demo app sets `ZF_ENV=production` when sign-in is on (`infra/modules/containerapps.bicep`), so ZF_ENV cannot identify the demo. A separate `ZF_DEPLOYMENT_PROFILE=demo` marker is needed.
* Slice chosen: registry record, env switch, status endpoint, panel disclaimer and label, tests, docs. Infra wiring and the live check are a follow-up (sensitive tier, coordinator gates).

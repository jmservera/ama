---
title: Issue 891 chat demo activation research
description: Evidence for remaining criteria of #891 against origin/main 0209b46bf
ms.date: 2026-11-07
---

## Disposition

Research executed (direct repository and read-only Azure inspection). Planning Readiness: Ready.

## Evidence

* Already on main: switch #892 (`ai_registry.demo_activation_honoured`), `chat_demo_meter`, `server.chat_admission`, status fields `demo_activation`/`demo_disclaimer`, model label in `src/api/src/zava_forward/api/web/chat.js`, tests in `src/api/tests/test_chat_panel.py` and `test_continuity.py` (price, authority, second call held, no switch no seed).
* Gap 1 (criterion 1): no test proved suspension, missing privacy references/retention and the one-call cap with the switch ON.
* Gap 2 (criterion 2): a Playwright run (720 px viewport) showed `#chat-demo-disclaimer` appended inside `.chat-widget-intro` (max-height 30%, overflow auto) was squeezed to 31 px so the disclaimer was outside the visible box. Existing check had no demo scenario. Content standard: AI label "AI suggestion, not approved" retained; the model label adds model-generated per `docs/reference/research/chat-demo-storage-approval-2026-11-01.md`.
* Live (criterion 3): `ca-cutover-test-demo-api` revision `--0000026`, image `1f465bf5e` (contains #892 and #1200), env has `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`, `ZF_DEPLOYMENT_PROFILE=demo`, `AI_ENDPOINT`, `AI_DEPLOYMENT=standard`, the three chat refs. `/healthz` 200 (3 of 3, warm). Unauthenticated `/api/chat/status` returns 401 from Easy Auth. Sign-in needs the owner-held test-user password (infra README, resident/employee acceptance), not available to the agent; no secret was read.
* Deployment of the new UI change needs the `src-deploy.yml` workflow after merge; not performed (no push by instruction).

## Decisions

* Place the disclaimer in a separate `flex:none` bordered note before the intro (non-colour signal, native `role=note`).
* Do not use the agent's own Azure CLI token to impersonate a test user.

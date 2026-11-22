# Research: issue 2245 (employee chat) and 2243 (resident AI expiry), live demo

Date 2026-11-22. Disposition: executed. Planning Readiness: Ready.

## Findings

* Live employee chat (revision 0000050, probe `docs/reference/research/issue-2245-live-2026-11-22/before_probe.json`): five asks, all HTTP 200, every ask `model_calls` 0 and `provider_outcome` `activation-not-approved`. No 500 in this run.
* Azure side is healthy: deployment `standard` (gpt-4.1-nano, GlobalStandard) Succeeded, API identity holds Cognitive Services OpenAI User and Foundry User on `aif-cutover-test-rzsrg`, private endpoint present, env `AI_ENDPOINT`, `AI_DEPLOYMENT`, `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`, `ZF_DEPLOYMENT_PROFILE=demo` all correct.
* Root cause: `chat_admission` (server.py) returns the continuity block; live `/api/continuity` holds open suspension SUS-1 (scope all, 2026-11-18, "Demo probe: negative test", restart authority TBD, `actual_hold` true). `ChatModel` maps every denial to `activation-not-approved`, so the widget says "assistant not available" and the status banner still claims AI generation. The suspension cannot be lifted by the app (restart needs OD-35 authority and an `ai_restart` OID-bound role; `actual_hold` survives restart).
* Rules-first intents (`unblock`, `claim`, `pas2035`, `sensor`) never call the model by design; stock and funding questions are answered by rules even when AI is available.
* 500 on first POST: not reproduced in this run; cause unreadable (Log Analytics denied); the earlier SQL serialisation fix (PR 2227) is deployed.
* 2243: `assistant.py` hard-codes EXPIRES 2026-11-01; live resident label "AI unavailable: the AI exercise has ended" reproduced (`before_resident_probe.json`).

## Decision

Fix in code: honest hold reporting (employee), env-driven expiry (resident). Do not weaken or bypass the suspension control; its removal needs an owner decision.

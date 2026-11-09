---
title: Issue 891 employee AI live observation research
description: Prospective research for first-party identity attestation and one guarded employee model demonstration
ms.date: 2026-11-08
---

Disposition: reused. Planning Readiness: Ready.

* Worktree `issue-891-employee-ai-live`, branch `test/demo-employee-ai-live-891`, HEAD = origin/main `ecb28815b`. No source, tests, config or cloud writes.
* Deployed app unchanged from the earlier release: revision `--0000027`, source `e2ecee25`. This is a deployed-source observation, not current-main acceptance.
* Prior block: Entra directory read denied (earlier adverse outcome preserved). The documented 2 Nov route (docs/architecture/cutover-evidence-pack.md, independent identity row) takes the expected object from an `id_token` issued by the Entra token endpoint for the test account, in memory, before contacting the app.
* Model authority: owner issue 891 live-check authorisations and the demo-only meter in `core/chat_demo_meter.py`: synthetic one-day authority, 20 calls, 100000 tokens, USD 1 label, one call per question, activation honoured only under the demo switch. Capacity authority 2026-11-05 stays within the USD 700 cap. No reset, no new budget.
* Employee app is served at `/app`; `/` is the public welcome page.

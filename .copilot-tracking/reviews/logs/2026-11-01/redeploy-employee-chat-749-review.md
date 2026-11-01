---
title: Redeploy employee chat fix from main 1a644d317, review
ms.date: 2026-11-01
---

Review executed once (parent, evidence read-back). Outcome: deployment conformant; #749 behaviour proven live.

* Backups first, constraints kept, registry restored, `CHAT_*` preserved, health green, no rollback, resident and agents untouched.
* Open items: complete local gate not run (focused only); test-user credential exposure in the session transcript needs rotation; carried observation: employee `GET /api/chat/regulatory/status` 403.
* Human review boxes remain unchecked: owner review required.

## Follow-ups (ranked)

1. Rotate both test-user passwords (security, small).
2. Run the complete local gate if the owner wants deployment evidence at full tier.
3. Investigate the 403 on `/api/chat/regulatory/status` for the employee test role.

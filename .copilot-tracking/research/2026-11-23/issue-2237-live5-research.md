---
title: Research issue 2237 live5
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

## Remaining criteria

* Reproduce, cause, regression test and live 200 were proven by earlier runs (`docs/reference/research/issue-2237-live3-2026-11-23.md`, live 200 on revision 0000056).
* The live4 fix (unreadable trigger date listed for review) is on main (commit 3bfb0b5cf4, 2026-11-23T22:36Z) but the live API revision `ca-cutover-test-demo-api--0000058` was created 2026-11-23T19:20Z, so the fix is not deployed.
* `az acr show` reports `publicNetworkAccess` Disabled on `crcutovertestrzsrg`; manifest listing is refused. A new image cannot be built or pushed without changing the registry network rules, which is an estate change outside this goal. Live proof of the new code is therefore unprovable for the demo.
* Code gap: `approve_retention_deletion` calls `_trigger` unguarded, so an unreadable date raises a raw `strptime` ValueError message to the user instead of a plain fail-closed refusal (live4 follow-up 1).

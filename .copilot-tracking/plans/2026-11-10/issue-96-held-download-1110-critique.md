---
title: Issue 96 served Held draft download consumer critique
description: Single final-candidate critique of the plan and details, run by the author with no nested agent
ms.date: 2026-11-10
---

## Execution

Executed once, by the implementing author, against the final plan and details. No nested agent was used. This is author self-critique, not independent review; independent exact-head assessment remains required.

## Findings and dispositions

* PC-1 (details wording): Phase 1 contained a garbled status condition. Disposition: applied; the condition is any status other than `Held` returns 409 without an attachment.
* PC-2 (inventory blind spot): the coverage test regex only sees quoted `/api/...` strings, and the route is spliced from path parts, so the existing test would pass without any entry. Disposition: applied; an explicit `GET_ENDPOINTS` entry plus a dedicated coverage test mirroring the job-pack pattern.
* PC-3 (guard honesty): `ZF_DEPLOYMENT_PROFILE=demo` is set on the real demo API by Bicep, so profile alone is insufficient and the exact new switch is a second, owned condition. The switch attests synthetic data but is not proof. Disposition: accepted as a documented limit in the plan, README and handoff; no Bicep change, so deployed demo stays OFF.
* PC-4 (HEAD): `do_HEAD` runs the export without a body. Read-only; accepted and tested for no mutation.
* PC-5 (stale semantics): the screen could imply the downloaded file equals the shown version. Disposition: applied; link note states the file is built at request time, shows the on-screen `input_version` and says the file carries its own version and hash.
* PC-6 (map index argument): passing `fundingDraftPanel` straight to `map` would hand the index as the second parameter. Disposition: applied; explicit arrow.
* PC-7 (disabled disclosure): disabled state must not reveal existence. Disposition: generic 404 for every caller after authentication, same as unknown routes.
* PC-8 (scope creep): no change to core `view`; the view flag is added in the server wrapper only when enabled so default contracts are unchanged. Accepted.

## Verdict

Revise; all findings are compatible with confirmed decisions and applied directly. No significant or divergent issue needs a user decision. No repeat critique.

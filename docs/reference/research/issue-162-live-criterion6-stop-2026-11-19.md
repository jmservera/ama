---
title: Issue 162 Criterion 6 Stop Decision (2026-11-19)
description: Re-check of the only unticked #162 criterion, with a fresh isolation test run and the reason no demo-provable or buildable work remains
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Result

Criterion 6 ("Administrator and break-glass access is audited, with purpose, and the policy is decided") is the only unticked item. Nothing remains that can be proven or built for the demo without a decision or an authorisation the owner has not given. The issue box stays unticked.

## Fresh evidence

From `src/api`, `python3 -m unittest tests.test_chat_isolation` with the documented `PYTHONPATH` ran 35 tests, all OK, on 2026-11-19. They cover default deny, short purpose, self-target refusal and audited grants.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| 1 to 5 | Proven and ticked; see [live audit](./issue-162-live-audit-2026-11-18.md) |
| 6 | Unproven for the demo |

## Why criterion 6 stops here

* Refusals are audited live and grants with purpose are proven by tests, per the [2026-11-18 proof](./chat-breakglass-live-proof-2026-11-18.md).
* A live grant needs `CHAT_BREAKGLASS_ROLES` and `CHAT_BREAKGLASS_REF` on the shared demo app, a new revision that the 2026-11-18 authorisation (no production changes) excludes.
* The administrator Entra role, user notification and audit retention are owner policy decisions. Code that chose them would invent policy.
* DPO and Legal approval is not needed for the demo.

The owner can accept the combined evidence, decide the three policy points, or authorise a temporary app setting. No Azure resource was created or changed.

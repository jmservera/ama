---
title: Issue 358 close-out details
ms.date: 2026-11-13
---

## Details

* Tier: Focused. Existing tests cover all three items (see research); no source change.
* Mutation check on `infra/scripts/setup-entra.py` guard, restored afterwards (clean `git status`).
* Live inspect: `az containerapp show -n ca-cutover-test-api -g ama` projecting name, hasKv, hasIdentity only; never values.
* Residual: populated live round-trip remains unmet (issue #358 comments, #360).
* Critique by rubber-duck before any further action; review by code-review after.

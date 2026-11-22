---
title: Issue 2192 live plan (round 3, redeploy)
date: 2026-11-22
---

Tier: focused (no src change). Basis: live Azure change limited to one revision of `ca-resident-demo` in resource group `ama` (image only), under the 2026-11-18 owner authorisation; no Bicep, secret, role or network change left behind. No push, no PR.

## Phases

* [x] Research: round 2 defect fixed by PR 2225; live revision 0000020 predates it.
* [ ] Implement: build `src/api/Dockerfile.resident-demo` from `origin/main`, push inside the trapped window with `/tmp/acr-push.sh <ip> <image>`, `az containerapp update --image` by digest, verify ACR readback (Disabled, Deny, no rules, exports disabled) and the new revision healthy.
* [ ] Prove: run `live_probe.py` style Playwright run; employee state for the resident case before, after untick (withheld), after restore.
* [ ] Record: research note with revision, digest, per-criterion table, `infra/README.md` section, index, log, changes record.

## Critique (executed once)

* Verdict: accept with changes. Finding 1: the update must change only the image; capture the prior template (image, env names, scale) first and diff after (accepted). Finding 2: the trap must leave ACR Disabled even on failure; read back afterwards and fix by hand if the trap fails (accepted). Finding 3: the test resident must be restored to its initial state in a finally block, including on a probe failure (accepted). Finding 4: the case-id home may have no controls, so the employee state may not change; if so, record unproven with the cause rather than altering data (accepted).

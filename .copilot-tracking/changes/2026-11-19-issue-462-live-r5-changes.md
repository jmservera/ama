---
title: Issue 462 live r5 changes
ms.date: 2026-11-19
---

Refs #462. Evidence-only; no source change, so the focused tier applies and no lint/type/test run was needed. No secrets read or printed; Azure access was read-only.

## Evidence

* `az containerapp show -g ama -n ca-resident-demo`: Running, image `crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:65481780cb3f5a55621f637fa783230004b263085dcaece1dfca93a928bbbd19`, FQDN `ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io`.
* Unauthenticated curl: `/` 200 (first attempt timed out on cold start, retry 0.1 s), `/login` 404, `/api/case` 404, `/staff` 404.
* `gh api graphql` on PR #455: MERGED 2026-10-25T21:25:42Z, one unresolved thread (comment 4372517587); #444 CLOSED. Its fix is on main as `0d90c2bee` (#2112).

## Per-criterion table

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven | Threat models of 2026-11-16 and 2026-11-17, r3 note, this run's artifacts |
| 2. #444/#455 and rubric resolved | Unproven, needs a human | Thread 4372517587 unresolved on GitHub; no-manual-score-edit confirmation and hosted rerun are maintainer/hosted actions; no push allowed |
| 3, 4, 5, 8 (ticked) | Not re-run | No change in scope |
| 6. Pre-spend record | Proven for the demo | r3 note; owner decision 2026-11-18 supersedes the October cap |
| 7. Deployed showcase in a browser | Proven for the demo, desktop | r3 note; live app still Running on the same digest, unauthenticated paths deny |

Unmet: criterion 2 only. #462 must not be closed.

---
title: Issue 462 live r6 changes
ms.date: 2026-11-19
---

Refs #462. Evidence-only; no source change, focused tier. No secrets read or printed; Azure access read-only.

## Evidence

* `az containerapp show -g ama -n ca-resident-demo`: Running, image digest `sha256:65481780cb3f5a55621f637fa783230004b263085dcaece1dfca93a928bbbd19`, FQDN `ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io`.
* Unauthenticated curl: `/` 200 (first attempt timed out on cold start; retry 0.1 s), `/login` 404, `/api/case` 404, `/staff` 404.
* `gh api graphql` PR #455: MERGED 2026-10-25T21:25:42Z, one unresolved review thread.

## Per-criterion table

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven | Threat models 2026-11-16 and 2026-11-17, r3 to r5 notes, this run |
| 2. #444/#455 and rubric resolved | Unproven, needs a human | Thread unresolved; rubric rerun and no-manual-edit confirmation are maintainer or hosted actions; no push allowed |
| 3, 4, 5, 8 (ticked) | Not re-run | No scope change |
| 6. Pre-spend record | Proven for the demo | r3 note; owner decision 2026-11-18 supersedes the October cap |
| 7. Deployed showcase in browser | Proven for the demo, desktop | r3 note; app still Running on the same digest; unauthenticated paths deny |

Unmet: criterion 2 only. #462 must not be closed. Every remaining criterion needs a human, so no code or test was built.

Witness note: first commit-complete and early plan/implement/review calls were refused because the state file lacked artifact paths; corrected and re-recorded, then a follow-up commit.

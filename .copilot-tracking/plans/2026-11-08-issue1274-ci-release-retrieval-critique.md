---
title: Issue 1274 hosted CI release retrieval plan critique
ms.date: 2026-11-08
---

Single pass, executed by the native session on the final candidate plan.
Verdict: proceed with amendments, all compatible and applied directly.

| Finding | Disposition |
| --- | --- |
| Pinning the archive digest in code makes a legitimate actionlint bump a code change. | Accepted as intended: exact identity is the requirement. Bump is a reviewed edit of constants. |
| A truncated body from a 200 response can pass a naive check. | Applied: digest and size check, retry on mismatch. |
| Sending the token to a redirect target leaks it. | Applied: drop Authorization on host change, tested. |
| New tool file not in `ci-affected.py` or `src-ci.yml` `paths` would skip or force-all the namespace job. | Applied in P3. |
| Browser URL is currently 504 (E5), so the API source is the only working path today; fallback order should not hide that. | Applied: log which source succeeded. |
| AWF cannot be fixed here. | Accepted as recorded partial blocker, no workaround. |
| Running `rpi-checks.py --changed` here would escalate to the full matrix because a workflow path is unmapped. | Not run; owner policy is CI-first. Recorded as skipped with reason. |

No finding conflicts with a confirmed user decision; no user decision required.

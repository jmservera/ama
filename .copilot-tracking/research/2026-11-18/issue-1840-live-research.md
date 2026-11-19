# Research: issue 1840 old-image insufficient classification (live demo run)

Date: 2026-11-18. Task: issue-1840-live. Mode: automatic. Status: open (research opened).

## Opening

Goal: classify incomplete old-image execution as `INSUFFICIENT` in `completed()` of `src/api/checks/old_image_sql_probe.py`, with focused regressions. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised within resource group `ama` (cap USD 700), no drills, no Key Vault rotation, no production changes.

## Findings

Evidence (commands run 2026-11-18, no secrets involved):

* `ls src/api/checks | grep -i old` in this worktree (base `16880f509`, origin/main): no `old_image_sql_probe.py`.
* `git cat-file -t 510fd90f` in the main checkout and this worktree: `Not a valid object name`.
* `git fetch origin 510fd90f4f8c15bfe4da24b761d29990d3986a85`: `fatal: remote error: upload-pack: not our ref`.
* `gh api repos/jmservera/ama/commits/510fd90f...`: HTTP 422, no commit found.
* `git ls-remote origin 'refs/heads/test/assistant-old-image*'`: no output; the parent topic `test/assistant-old-image-sql-107` named by the issue is not published.
* `grep -rl "restart_after_mismatch|after_mismatched_restart"` over `src docs tools .copilot-tracking`: no match. The sibling worktree `issue-107-20261117T2352` (branch `docs/issue-107`) has no `old_image_sql_probe.py` either.
* `gh search code old_image_sql_probe --repo jmservera/ama`: no results. Issue 107 is OPEN.

Conclusion: the diagnostic `completed()` function and the helpers of frozen candidate `510fd90f` exist in none of the reachable repositories, refs or worktrees. The issue itself says the implementation depends on those helpers.

Live Azure: the defect is in an offline fixture-driven diagnostic (issue text: "No actual historical-image, SQL, live AI or whole-#107 acceptance follows from fixture tests"). The authorised demo resources (`ca-cutover-test-demo-api`, `ca-resident-demo`, `evhns-cutover-test-demo`) do not execute this probe, so no Azure action could prove a criterion. None was run and no throwaway resource exists.

## Planning Readiness

Disposition `executed`. Planning Readiness: Ready to plan a blocked outcome (record blocker, no source edit). Writing the fix against a reconstructed file would invent code and would not match the pinned candidate, so it is rejected.

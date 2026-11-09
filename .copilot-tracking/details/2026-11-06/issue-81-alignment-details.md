<!-- markdownlint-disable-file -->
# Details: issue #81 parent alignment (2026-11-06)

Plan: [plan](../../plans/2026-11-06/issue-81-alignment-plan.md).

## P1 Pre-alignment commit

* Files: research, plan, details, critique, state under `.copilot-tracking/*/2026-11-06/`.
* Commit with repository-local `{id}+{login}@users.noreply.github.com` from a fresh `gh api user`, Conventional Commit, Copilot trailer.

## P2 Rebase

* `git fetch origin main`; re-pin; if main advanced beyond `56eec7369` record the new SHA and re-run the dry merge.
* `git update-ref refs/ama/issue81-start af891a5cc...` (local ref only, keeps start identity; not pushed).
* `git rebase origin/main`.

## P3 Preservation proof

* `git merge-base --is-ancestor origin/main HEAD`.
* `git rev-list --reverse origin/main..HEAD`, map old to new via `git range-diff af891a5cc~3..af891a5cc origin/main..<new-tip-of-child-commits>`.
* Compare `git rev-parse <rev>:<path>` for each of the eight source/test paths with the recorded blobs; compare every path under the three child evidence trees (`git diff --stat refs/ama/issue81-start HEAD -- src` must be empty).
* Verify issue-82 original RPI files unchanged by `git diff --name-status refs/ama/issue81-start HEAD -- .copilot-tracking`.

## P4 Regression commands

Run from `src/core` with scratch env; record command, exit code and counts. Failures are recorded as adverse, not retried into green without cause.

## P5 Checkpoint

Append a new dated section at the end of the existing recent-checkpoint area of
`docs/architecture/cutover-evidence-pack.md` (follow the fourth checkpoint
format: source and identities, covered PRs, requirement traceability,
exclusions, commands, classification, gaps/owners/resume conditions,
recommendation). Exclude unmerged #86 behavior. Classify only no-service
observations as local observed; FULL, service, SQL, browser, Azure and manual
acceptance as implemented-unverified, blocked or unknown. Link from changes
and review records. Do not tick any issue criterion.

## Dependencies

P1 before P2; P2 before P3, P4; P3 and P4 before P5.

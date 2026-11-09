# Issue 1258 main preparation details (2026-11-09)

Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-main-prep-plan.md`.

## Phase 1: prospective commit

Add only the main-prep research, plan, details and critique files. Author and committer `8036360+jmservera@users.noreply.github.com` (repo-local). Conventional Commit `docs(rpi): ...` with the Copilot trailer. No logs.

## Phase 2: merge

* Re-fetch, require `git rev-parse origin/main` to equal `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939`, else stop. Then `git merge --no-ff -m <Conventional Commit with Copilot trailer> 9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` (immutable SHA). Verify author and committer equal the repo-local identity on the merge commit. If it stops with conflicts, abort with `git merge --abort` only (restores the pre-merge state; does not discard committed work) and report.
* Expected delta: 36 docs and tracking paths from F1.

## Phase 3: checks (scratch logs in an owned `mktemp -d` outside the repository)

1. `git diff --name-only <pre-merge HEAD> HEAD | grep -E '^(src|infra|tools|\.github)/'` must be empty.
1b. The delta path list equals the 36 pinned paths of the research (compare `git diff --name-only 06e3f2f45 9f9aacc8b` against the merge delta); no root configuration file appears.
2. Equivalence claim is limited to the tested application trees. For each of `src`, `infra`, `tools`, `.github`: `git rev-parse <52f9b61b>:<path>` equals `git rev-parse HEAD:<path>` (where the path exists).
3. `git diff --check` of the merge delta; `git status --short` clean.
4. Link and reference review of the three records (relative paths exist).
5. No code tests rerun when 1 and 2 hold. Record the inherited c5 outcomes with their source and mark them inherited.

## Phase 4: records

New unique paths: `.copilot-tracking/changes/2026-11-09-ranking-archive-blob-1258-main-prep-changes.md`, `.copilot-tracking/reviews/2026-11-09-ranking-archive-blob-1258-main-prep-review.md`, `.copilot-tracking/rpi-sessions/2026-11-09/ranking-archive-blob-1258-main-prep-state.json`; stop if any exists. Changes record (actual commands, exit codes, identities), one Review, state JSON, and a final local commit. Coordinator handoff `handoff-1258-main-preparation.md` in `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/`. No push, PR, issue or board change.

## Literal unmet criteria carried

Azurite or real account run, Blob container, WORM or immutability, role grant, Bicep env, deployment, folder-record migration decision, hosted CI, independent exact-head closure of c4 finding 1, final Store/API integration after #1292 merges, Minor R-1 policy-name guard. Use `Refs #1258` only.

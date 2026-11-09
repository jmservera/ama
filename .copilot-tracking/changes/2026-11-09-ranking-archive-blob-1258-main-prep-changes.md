# Issue 1258 main preparation changes (2026-11-09)

Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-main-prep-plan.md` with the re-pin addendum `...-main-prep-repin-addendum.md`.

## Identities

| Item | Value |
| --- | --- |
| Source-approved candidate | `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, tree `20901b61eddb68d3740f6976187d17ff5fc0cea2` |
| Prospective records commit | `c292024138d2f57ef5b2615d6e2775dcc958335a` (research, plan, details, critique) |
| Re-pin addendum commit (pre-merge HEAD) | `e54b6f2f62c66ca5cf48b34dc3cba58dfeb7701e` |
| Merged main (immutable pin) | `ba5cc74b8b717957b046fd1d28804a989a7f3dd7` |
| Merge commit | `8033379faa83238892092a33b8b4e353776eac0b`, tree `f82e015928f28c3a5934223041990136b0e7b58f` |
| Author and committer | `8036360+jmservera@users.noreply.github.com` (repo-local), Copilot trailer present |

## Actual producer commands and exits

* Pin check 1: `git fetch origin main` then compare with `9f9aacc8b`: not equal (`ba5cc74b8`); guarded merge not run, exit 1 from the guard. No merge, tree untouched. Preserved as an adverse step, not retried silently; addendum written and committed first.
* Prospective commit `c2920241`: exit 0. Addendum commit `e54b6f2f`: exit 0.
* Pin check 2 equal; `git merge --no-ff ba5cc74b8`: exit 0, no conflicts, worktree clean after.
* Delta check: 37 paths, equal to `git diff --name-only 06e3f2f45 ba5cc74b8` (diff exit 0).
* `git diff --check <pre-merge> HEAD`: exit 0.
* Ancestry: `52f9b61b` and `ba5cc74b8` are both ancestors of the merge; `origin/main...HEAD` is `0 17` (zero behind).

## Source equivalence

* Tree object IDs equal between `52f9b61b` and the merge for `src` (`f9cde8bc6f70...`), `infra` (`b0969f8b7b8c...`) and `tools` (`8ccabea4c209...`).
* `.github` differs only at `.github/rubric/scores/latest.json`, a generated data record; no workflow, permission, pin, image, package, secret or deployment file changed.
* Docs-side Python, JSON and Node files in the main delta are unrelated paper tooling; not run and not claimed.

## Validation tier

Owner DEMO targeted tier, docs-only advance. No test was re-run. The c5 results (core 137 OK, API wiring 35 OK, ruff, mypy on the adapter) are INHERITED by tree identity from `52f9b61b`, not re-observed here. No full gate, SQL, scanner, browser, image, emulator, cloud or deploy step. Scratch listings in `/tmp/ama1258-mainprep.efFCqm` (not committed, not deleted).

## Remaining #1292 plan

As in the plan: PR 1308 (head `6ded235e`, OPEN, UNSTABLE) is not in main. Its 12 `src` paths include `core/store.py`, `api/server.py` and `core/README.md`, which this branch also changes. Read-only `git merge-tree` forecast against that head: exit 0, no conflicts (forecast only). Final Store/API integration, targeted Core/API/runner checks and worktree origins wait for the real merge; source resolution needs new issue-specific authorization.

## Unmet criteria (literal, carried)

Azurite or real account run, Blob container, WORM or immutability, role grant, Bicep env (`ZF_RANKING_ARCHIVE`, `ZF_RANKING_BLOB_CONTAINER`), deployment, folder-record migration decision, hosted CI on this head, independent exact-head closure of c4 finding 1, final Store/API integration after #1292 merges, Minor R-1 policy-name guard. Use `Refs #1258`.

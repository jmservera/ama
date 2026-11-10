# Issue 1258 main preparation research (2026-11-09)

Refs #1258. Read-only research recorded before any merge, test or source edit. Task `1258-ranking-archive-blob-main-prep`, parent task `1258-ranking-archive-blob-c5`. Not a sixth correction cycle. Cycles c1 to c5 are spent (five of five); this task authorizes only ordinary source-preserving integration and preparation. Earlier c1 to c5 records, the independent c4 `approve_with_comments` verdict and every original adverse outcome are history and are not edited.

## Research disposition

Executed (new fetch and read-only comparison). Planning Readiness: Ready.

## Pinned identities (fetched 2026-11-09)

| Item | Value |
| --- | --- |
| Branch | `fix/ranking-archive-ancestor-durability` |
| Source-approved candidate HEAD | `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, tree `20901b61eddb68d3740f6976187d17ff5fc0cea2`, worktree clean |
| Previous base (merge-base) | `06e3f2f456ab008f8e41f013d9019c2d82ea05b9` |
| Fetched `origin/main` | `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` (2 commits ahead of the merge-base) |
| PR 1308 (#1292) | OPEN, not merged, head `6ded235e2a7b8ca36edc4414bcd903be8690d4e3`, base `daf45a46c`, merge state UNSTABLE, `src-api` check has no conclusion |
| Issue 1258 | OPEN |

## Findings

* F1. The main advance is `daf45a46c` (paper judging docs, PR 1307) and `9f9aacc8b` (architecture checkpoint, PR 1309). `git diff --name-only 06e3f2f45 origin/main` lists 36 paths, all under `.copilot-tracking/`, `docs/architecture`, `docs/capstone/...` and `docs/reference` (README and log). There is no path under `src/`, `infra/`, `tools/` or `.github/`.
* F2. No path overlaps the branch's own change set against the merge-base (56 paths, no `docs/reference/README.md` or `log.md` edit). A textual conflict is not expected.
* F3. The merged `docs/reference/README.md` text names #1288, #1292, #144, #189, #1295 and #1296 as excluded unmerged work. That statement already excludes #1292; it does not claim #1258.
* F4. #1292 is not in `main`: PR 1308 is open and `mergedAt` is null. The condition for "complete real final sharedStore/API integration" is therefore not met.
* F5. PR 1308 changes 12 paths under `src/` (including `core/store.py`, `core/sqlstore.py`, `core/mssqlstore.py`, `core/continuity.py`, `api/server.py`, `core/README.md` and tests). The branch also changes `core/store.py`, `api/server.py` and `core/README.md`. This is the future integration surface.
* F6. A read-only `git merge-tree --write-tree` of this branch against the PR 1308 head completes with exit 0 and no conflict list. This is a textual forecast only. It writes objects, not refs or the worktree, and is not an import, a semantic proof or SQL evidence.
* F7. Unchanged c5 boundary: Store/API publish is a conditional create. Azure/Azurite, role grant, immutability, Bicep env, deployment, folder-record migration, hosted CI and final Store/API integration remain unperformed.

## Alternatives

* A. Merge `origin/main` now, record source equivalence, prepare the exact remaining #1292 plan (chosen).
* B. Import PR 1308 now. Rejected: forbidden by the brief (unmerged #1292).
* C. Rebase. Rejected: history rewrite is prohibited.
* D. Do nothing and report. Rejected: the brief expects the docs/ancestry advance.

## Planning Readiness

Ready. Remaining open item: whether a docs-only advance warrants a re-run. Decision basis: the brief says no broad rerun for docs-only advance and permits recorded inherited source equivalence. The plan verifies equivalence by comparing trees of `src`, `infra`, `tools` and `.github` between the approved HEAD and the merge result.

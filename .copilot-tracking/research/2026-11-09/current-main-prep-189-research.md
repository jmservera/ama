<!-- markdownlint-disable-file -->
# Issue 189 current-main preparation research (2026-11-09)

Task `issue-189-current-main-prep`, parent `issue-189-simulator-control-c1-api-capture`. Prospective: written and committed before any merge or edit. Research disposition: `executed` (read-only git inspection). Planning Readiness: `Ready`.

## Pinned identities

* Worktree head `8ab64519ce17aed2b4565f4f185957ab79a270bf` (tree `602f2510c0f8031647aa2e618d0298acfe9a679f`), branch `feat/demo-simulator-control-189-1109`, clean.
* Fetched `origin/main` `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` (checkpoint #1309 squash, tree `bc21a50a4d7abbadb36065968fd68fb1283d5454`), confirmed by `git fetch origin main` at 2026-11-09 15:1x UTC.
* Merge base of head and main: `df8e858b2150198e5e22c73d224a0d3592c73daa` (unchanged since the original and C1 records).
* Source of intent: C1 handoff (`3d8a7a012`), API capture (`8ab64519c`: producer exit 0, 2105 tests, 365 skips), original independent Functional review (adverse, three findings, preserved), historical F3 cause UNKNOWN.

## Main versus base (199 files, +35291/-1720)

Dominant areas: `docs/capstone` (46), `.copilot-tracking` records of other lanes (about 100), `docs/architecture`, `tools/capstone`, `docs/reference/README.md` and `log.md`, `skills-lock.json`.

Source-bearing paths in main since base (complete list under `src/`, `infra/`, `tools/`):

* `src/agents/src/zava_forward/agents/queue_azure.py` (new, 217 lines) and `src/agents/tests/test_queue_azure.py` (new, 253 lines): a queue adapter. No `src/api` file imports it (grep for `queue_azure` in `src` finds only these two files).
* `infra/README.md` (1 line), `tools/capstone/*` and `tools/cowork-native-recovery/Invoke-StoryReview.ps1`: unrelated to the simulator control screen.
* No change under `src/api`, `src/core` or `src/orchestrator` since base.

## Overlap with the #189 change set

* #189 touched 12 `src/api` files plus tracking records; `git diff --name-only` intersection with main is empty. No same-file edit, so no textual conflict is expected; `git merge-tree --write-tree HEAD origin/main` is clean (tree `95364e78...`).
* Docs intent: main appends to `docs/reference/log.md` and edits `docs/reference/README.md`; #189 changes neither, so both stay. #189 adds no knowledge-base file, so no index or log entry is owed by this preparation beyond the merge itself.
* RPI intent: main carries other lanes' `.copilot-tracking` records under the same date folders. #189 records use the `simulator-control-189-*` prefix; no filename collision.

## #1292 sibling (read-only comparison, nothing imported)

Remote and sibling head `6ded235e2a7b8ca36edc4414bcd903be8690d4e3` (moving, CI correction in progress; not merged into main). Against its own merge base it changes `src/api/.../server.py` (+9/-?, ai/priority POST `CommittedReloadError` handling near the `/api/ai/priority` route), `src/api/.../web/app.js` (+17, `priorityPanel` hold note and pending/`checkHistory` guard), `src/api/tests/test_case_journey.py`, and `src/core` store, SQL store, MSSQL store, continuity, `sqlguard.py`, priority and resident tests.

Overlap with #189 is confined to `server.py` and `app.js`; the hunks are in different regions (#1292 in the `/api/ai/priority` POST route and `priorityPanel`; #189 in the GET prelude after `s = app.store`, the POST hook after the CSRF and view-only gate, and the loader entry and route registration). A trial `git merge-tree --write-tree HEAD 6ded235e2` is read-only and reports a clean tree (`0b852555...`); it is an observation only, not an import and not the final integration, because the #1292 head can still move.

## Impact assessment

Main's source changes (`queue_azure`) do not reach the admin, simulator, `live_control`, `server.py` or App surface. The directly impacted surface after a normal merge is therefore unchanged API/web source, so existing targeted checks are re-run as cheap integration confirmation, not as new acceptance: `test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_content_standard`, `test_design_system`, `test_workspace_scripts`, the 11-state Chromium plus axe check for default-deny read-only-admin mutation, Stop in all readable writable states and manual/disabled paths, and `test_queue_azure` only if the agents package is importable and relevant (informational). No web file changes, so Fluent 2 and web-guidelines review is not triggered; the web-guidelines source is not refetched unless a web file changes.

## Not decided here

Future #1292 SQL authority, transaction and `CommittedReloadError` behaviour is not guessed. Final Store and current-SQL integration and publication wait for #1292 actually landing on main.

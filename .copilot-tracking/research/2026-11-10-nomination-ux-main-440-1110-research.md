<!-- markdownlint-disable-file -->
# Task research: nomination and UX integration wave checkpoint (#440, 2026-11-10)

* Task ID `440-nomination-ux-main-1110`, slug `nomination-ux-main-440-1110`. Worktree `issue-440-nomination-ux-main-1110`, branch `docs/demo-nomination-ux-checkpoint-440-1110`, base `origin/main` `65c2ab9d947d1498dafd37e24a377d1ff503e86f` (tree `520d12561000e9dc596ed0b03f9f862a9240b32f`).
* Research disposition: `executed` (stub written before the witness `research-open` record; the findings below were added after it). Planning Readiness: `Ready`.
* Scope: a new recurring observation and documentation checkpoint after PR 1381 and PR 1376 reached main. Not the old #440 C6, not the separate CSV-learning record, no source fix.
* Inputs to be read: Root handoffs and raw checks for the 130 nomination-only and 149 combined local predictions, the two independent records, the fresh Web Interface Guidelines retrieval, the two tree-equivalence proofs, the existing cut-over evidence pack, the index and the log.

## Findings (read 2026-11-10 after the witness `research-open` record)

### Source and identity facts (read with git and gh)

* `origin/main` after `git fetch` is `65c2ab9d947d1498dafd37e24a377d1ff503e86f`, tree `520d12561000e9dc596ed0b03f9f862a9240b32f`, equal to the worktree HEAD. `HEAD:src` `70d956b06f31cabfd8321b4ee9c203ae8b21d89c`, `HEAD:infra` `d94040329d5497aee252300972cb3c7497689d25`.
* PR 1381 (`Refs #130 #81`) merged 2026-11-10T12:58:55Z as `0376606dc97a14ebd0cbc81bb8fe136e836a3d1b`, tree `0368d5e6689cb58be2606d255b7d20bd9e5d6011`, published head `210161bdc1779953c349049565312d6983e160fb`, 19 reported checks (18 check runs plus the `rubric/score` status context), all SUCCESS at read time.
* PR 1376 (`Refs #149 #440 #233 #231 #230 #153 #156 #152`) merged 13:02:24Z as `65c2ab9d947d1498dafd37e24a377d1ff503e86f`, head `621f29d29b363dfd25729079180bb33f94ba0b20`, 19 reported checks all SUCCESS. Child PR 1382 merged earlier (12:20:13Z) into the parent branch as `621f29d29`, not into `main`.
* Commit-scoped check runs read for the exact main commit `65c2ab9d9` show only 7 runs (one `detection` in progress, the rest skipped or the Copilot activation set); no Source projects CI result is available for the exact main commit. PR-head metadata is not a result for the merge commit.
* Root proofs: `149-current-main-equivalence-1307.txt` lists `520d1256...` as the actual UX main tree, the single differing path `.github/rubric/scores/latest.json` against the tested local union tree `bb90e4d3...`, and equal `src` ids `70d956b0...` for both. `130-current-main-rubric-equivalence-1254.txt` lists the actual nomination-main prediction `0368d5e6...`, differing from the tested `36b16ae7...` only at the same rubric file, with equal `src` `e1b868d2...` and `infra` `d9404032...`. These were read, not recomputed by this task. The tested compositions were source-qualified local predictions (`git merge-tree` and ordinary local merges), not a GitHub merge preview and not an observation on `65c2ab9d9`.
* Nomination blobs at HEAD: `app.js` `c735acad6350`, `panels.js` `5f37f2a71b4a`, `style.css` `32234917f66e`, `test_nomination_screen.py` `4d0481a27961`, `nomination_browser_check.py` `81cafcb4d434`, `workbench_browser_check.py` `0fbe0be3b0c3`, `src/api/README.md` `b117333c3e1d`, `scenario-manifest.json` `e6624d6d0c71`. Pack, index and log before this task: `5f223b53b7ed`, `28b3ec408855`, `058338f4903c`.
* Documents at the pin: BRD 0.21.0 `draft` `34d88395de86` (FR-037, AC-065, RULE-005); PRD Zava Forward 0.21.0 `in-review` `c788b917bafa`; PRD Proper Warm 0.13.0 `in-review` `f7f9b7675e60`; ADR-0007 `Proposed` (`abb21088a9bb`); ADR-0006 source layout (`956da1a3b804`). Draft, in-review and proposed are not approval.

### Raw evidence consumed (Root, local, not re-run by this task)

* Nomination-only (aux worktree, tested tree `36b16ae7`): API 11 selectors 120 OK and 1 skip, simulator 30, Core learning 21, Agents paired-command 21, ruff, format (137 files), mypy API (217 files), `node --check`, nomination browser three axe scans with zero violations and zero incomplete, no non-GET request while viewing (six GET paths listed), challenge browser axe. The passing nomination output still contains law-store-unavailable tracebacks, assistants 503 and client-disconnect lines, so no zero-server-error claim.
* 149 combined (tested tree `bb90e4d3`): API unit 379 run with 16 skips, nomination and resident 25 run with 1 skip, Core 88 with 7 opt-in SQL skips, Core integrity 35, six static runs exit 0, one non-queued heavy-lock acquisition, handoff browser 9, role screens 47, 70, 36, 36, 47 and 46, atlas 362, paging 89, Held 31, workbench 124, progress 58, nomination three scans. Axe ran only in the named selectors; the 5-empty and 2-populated split of the 21 empty-queue lines was not independently re-derived.
* Independent records: 149 combined `approve_with_comments`, zero new, two inherited Mediums (#1362, #1360) and the #156 M1 proposal unapproved, with a fresh-guideline addendum; 130 current-main `approve`, zero new, known Low heading skip (h2 to h4, `panels.js` 326, 353, 369, 385) OPEN. Rule retrieval `web-interface-guidelines-fresh-1257.md`, SHA-256 `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234` (re-hashed here and equal). No complete conformance, assistive-technology, WCAG or human content acceptance is claimed.

### Traceability facts (static read of `panels.js` `nominationPanel`, `app.js` Resident tab and the tests)

* The panel is read only: it renders `c.nomination_records` and `challenge_targets` supplied by the server; it issues no request itself and the browser check observed no non-GET request while viewing. It returns `null` for a role without the fields (denied) and a distinct "No nomination or self-referral is recorded for this home." for an authorised empty list (`test_authorised_empty_and_role_denied_differ`).
* Original and corrected accounts are shown separately; missing or unknown values render "Not recorded" or "Unknown", never "none"; review staleness uses the version fields; acknowledgement shows "Delivery unverified"; the view states it does not contact, decide eligibility, change priority or assign an owner, and that a recorded review is a staff record, not an approval. Non-AI and manual route: the text "Staffed non-digital route" and the server record fields only; no assistant call renders it.
* Handoff read guidance (#153) and Resident tab composition in `app.js` are disjoint hunks that auto-merged (Root handoff); paging, Held and workbench behaviours are PR 1376 (parent 149) observations, not nomination.

### Open owners (read live) and exclusions

* #130, #149, #156, #440 OPEN; #1360, #1362 OPEN (existing owners of the generic transfer message and the atlas version assertion); #1383 (rubric scorer failed on main, 901fea60e) OPEN with no comments; #1384 (workspace exhaustion checker alignment) OPEN. The heading Low has no separate issue; it is recorded in the #130 independent record and is not duplicated. No new issue or source fix is proposed.
* Excluded by assignment: unmerged 136 and 175 Bicep, 89 aftercare parent and child 133, held 132, contractor identities, the #1384 checker fix, the old C6 and CSV-learning record, whole-workspace acceptance.

### Planning Readiness

Ready. Inputs are present, identities are verified, and the work is one scoped documentation record with an index paragraph and a log entry.


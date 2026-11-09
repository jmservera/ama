# Issue 1258 SQL main integration research (2026-11-09)

Refs #1258. Read-only research recorded before any merge, test or source edit. Task `1258-ranking-archive-blob-sql-main`, parent task `1258-ranking-archive-blob-main-prep`. Not a sixth correction cycle: c1 to c5 are spent (five of five), with zero productive cycles available. This task authorizes only ordinary source-preserving merge and validation. If a manual source resolution is needed, the task stops with the exact conflict. Earlier records, the independent c4 `approve_with_comments` verdict (finding 1 CLOSED by the independent c5 review) and every original adverse outcome are history and are not edited.

## Research disposition

Executed (fresh fetch and read-only comparison). Planning Readiness: Ready.

## Pinned identities (fetched 2026-11-09)

| Item | Value |
| --- | --- |
| Branch | `fix/ranking-archive-ancestor-durability`, worktree clean |
| Candidate HEAD | `9cdf267242d2f0a0b9de03f945d3ffda8a281d39` |
| Source-approved candidate | `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` (c5) |
| Previous base (merge-base) | `ba5cc74b8b717957b046fd1d28804a989a7f3dd7` |
| Fetched `origin/main` | `8d6f029cac004506953f36606862168bbe9d9412`, descendant check passes; HEAD is 18 ahead and 1 behind |
| PR 1308 (#1292) | merged, squash `8d6f029c`, all 19 checks passed (coordinator brief) |

## Findings

* F1. `origin/main` is exactly the PR 1308 squash. `git diff --stat ba5cc74b8 origin/main` over `src` lists 12 paths: `api/server.py`, `api/web/app.js`, `api/tests/test_case_journey.py`, `core/README.md`, `core/pyproject.toml`, `core/continuity.py`, `core/mssqlstore.py`, `core/sqlstore.py`, `core/store.py`, `core/tests/sqlguard.py`, `core/tests/test_priority_order.py`, `core/tests/test_resident_decisions.py`.
* F2. Overlap with this branch's own change set: `core/store.py`, `api/server.py`, `core/README.md`. A read-only `git merge-tree --write-tree HEAD origin/main` completes with exit 0 and no conflict (resulting tree `94552275c219438b94b62a34603c73005c2193be`). This is a textual forecast, not semantic proof.
* F3. Different hunks, no semantic collision found by reading:
  * `store.py`: branch changes `_ranking_archive`, `ranking_publication_status` and `publish_ranking_snapshot` (Blob selection, `BlobArchiveError`, uncertain-write audit). Main adds `_rec_view` `order_note`, `ORDER_NOTE`, `_order_unresolved`, `rec_order_unresolved`, and an `resolve_priority` guard. These touch the priority recommendation path only.
  * `server.py`: branch changes `/api/ranking/publish` error mapping (`ArchiveWriteUncertainError`, 409 `committed_unconfirmed`). Main changes `/api/ai/priority` and the priority resolve route (`CommittedReloadError`, 409 `committed`). Distinct routes.
  * `core/README.md`: both add sections; textual merge expected.
* F4. `SqlStore` initialises `self.db_path`, so the Store `_ranking_archive` fallback (`dirname(live_path or db_path)/ranking-archive`) works for the SQL-backed store; Blob selection by `ZF_RANKING_ARCHIVE` is independent of the database backend. The ranking archive is not persisted in SQL, so SQL behaviour is covered by #1292's own owned disposable SQL evidence and is not re-run or inferred here.
* F5. `ranking_publication.py`, `ranking_publication_runner.py`, `ranking_archive_blob.py` and their tests are untouched by main; they need no source change.
* F6. Unchanged boundary: actual emulator qualification exists on the byte-identical adapter through #1259 and is not relabelled Azure, WORM, immutability or managed-identity acceptance. No role grant, Bicep env, deployment, folder-record migration decision, policy-name guard or retention work is added.
* F7. Parent final-schema changes arriving from main (`core/pyproject.toml` mypy override, `test_priority_order`, `sqlguard`) need only directly appropriate tests; no full matrix, private database, permission or model call.

## Alternatives

* A. Ordinary `git merge` of the pinned main SHA, targeted validation (chosen).
* B. Rebase or sibling import. Rejected: history rewrite and import prohibited.
* C. Resolve a conflict manually. Not authorized; stop and report with the exact conflict.

## Planning Readiness

Ready.

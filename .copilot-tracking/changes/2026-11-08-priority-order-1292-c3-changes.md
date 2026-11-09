<!-- markdownlint-disable-file -->
# Release Changes: priority order 1292, correction cycle C3

**Related Plan**: [.copilot-tracking/plans/2026-11-08-priority-order-1292-c3-plan.md](../plans/2026-11-08-priority-order-1292-c3-plan.md)
**Base**: C2 head `f8e9ea7da2534600f1cc9932e8a27b5905d56372` (tree `f27ead2e2d0ca578321b34c47d6d22115b296542`)
**Research and plan commit**: `7e037bfbd` (written before any source or test edit)

## Summary

Third correction after the independent C2 review (5 High, 4 Medium; all nine verified true in source).
Prior research, plans, reviews, C1/C2 logs and earlier SQL results are unchanged and are historical for the new source.
Light SQLite and static evidence only. No SQL Server, Docker, browser, heavy lock, full gate, push, PR or board write.

## Changes by finding

| Finding | Change | Files |
| --- | --- | --- |
| F1, F2 proof model | New `_proven_later`/`_unproven_latest`: the newest eligible record per employee is confirmed only if, against every other eligible record, both audit positions agree and either unedited insertion `seq` (inside one batch) agrees or `created` strictly agrees with no `seq` contradiction. Ties, edited rows, orphan or late events, missing audit and a timestamp alone are unproven. Ordinals are never changed. Linear per employee. | `sqlstore.py` |
| F3, F4 historical review | `_review_priority_order` (marker `rec_order_review` = 3) replaces the C0-only review, runs once in the migration transaction before the zero-row backfill, regardless of batch metadata. It assesses only ordinals in heuristic ranges (legacy rows and batch ranges), without `seq`, and records a `source=review` batch with `ordinals_changed=false`. | `sqlstore.py` |
| F5 server boundary | `_rec_view` marks the employee's unresolved newest record `order_confirmed` false, `actionable` false, `relied_on` false with `order_note`. `resolve_priority` raises `PermissionError` for accept and edit; reject stays. The priority panel renders `order_note` in a `role="status"` paragraph. | `store.py`, `app.js` |
| F6 anchors | Evidence cache stores a fingerprint of the digest files and re-verifies when it changes; the incremental path rejects an entry appended to a sealed year. | `sqlstore.py` |
| F7 BEGIN failure | `BEGIN IMMEDIATE` is now inside its own `try`; on failure unsaved recommendations and their pending creation events are dropped and no rollback is attempted. | `sqlstore.py` |
| F8 task ownership | `require_task_owned_loopback` also requires container evidence from `docker inspect` metadata (id match, running, label `zf.task=1292-sql-disposable`, loopback-only `1433/tcp` publish at `ZF_SQL_PORT`, provisioned password, age). It never contacts the listener. `write_manifest` takes the container id; schema `zf-task-sql/2`. Tests use a fake inspector. | `sqlguard.py` |
| F9 unresolved cost | One `rec_unres:<id>` meta row per flag (primary-key lookup, written once). The old `rec_order_unresolved` list is copied once (marker `rec_unres_index`) and left untouched. | `sqlstore.py` |
| Docs | README section updated. | `src/core/README.md` |

## Intentional expectation changes in existing tests (policy changes, disclosed)

* Audited same-second creations with an edited older proposal: newest is now flagged unresolved instead of confirmed (edit removes the `seq` signal, so audit alone is insufficient).
* Ambiguous-group, rollback-batch, unresolved-view, contradicted-event, rechain, C0 review and broken-chain tests: only the employee's newest record is listed (previously every record of a group); C0 review batch source is now `review` and the simulated C0 database deletes the new marker.
* `LoopbackGuard` tests: manifests carry a container id and positive cases pass a fake inspector.
* The backward-clock-step test is unchanged and still confirmed (audit and `seq` agree).

## Tests added (class `SqliteC3Corrections`, SQLite only, plus guard tests)

Mixed audited/unaudited, unaudited with different timestamps, clock step staying confirmed, tied seq, orphan event, prior-batch review with a zero row, C0 cross-timestamp audit inversion, server refusal of accept/edit with reject allowed, already accepted unresolved not relied on, static `app.js` check, same-head new digest, sealed-year append, BEGIN failure with later flush and save, repeated batches write only their flags, old list adopted once, and a guard negative with fake-inspector positive.

## Results (light tier; logs in [.copilot-tracking/changes/logs/1292-2026-11-08-c3/](logs/1292-2026-11-08-c3/))

| Check | Exit | Result |
| --- | --- | --- |
| Red: new tests on C2 source copy (`red-c2-source`) | 1 | 47 run, 22 failed or errored, including all 14 new behaviour tests (guard test is test-side and passes) |
| Green `test_priority_order` (`green-priority-order`, before lint fixes) | 0 | 70 run, OK, 19 skipped (SQL Server class, opt-in) |
| Green `test_priority_order` (`final-green-priority-order`, final source) | 0 | 70 run, OK, 19 skipped |
| `test_resident_decisions` (includes the two original selectors on SQLite) | 0 | 256 run, OK, 93 skipped (SQL Server) |
| `test_sqlstore`, `test_sqlqueues`, `test_sqlreads`, `test_taskqueues` | 0 each | 18, 14, 15, 21 run, OK |
| `ruff check src tests` | first run 1 (6 findings), `final-ruff-check` 0 | findings fixed in tests only |
| `ruff format --check` on the two test files | first run 1, `final-ruff-format` 0 | formatted |
| `mypy` | first run 1 (1 error), `final-mypy` 0 | annotation fixed |
| `git diff --check` | 0 | clean |

The first (failing) lint logs are retained beside the final ones. Skips are the opt-in SQL Server classes; no SQL Server, ledger-enabled migration or Docker path was run, so none is claimed.

## Source identities (sha256)

* `src/core/src/zava_forward/core/sqlstore.py` 206164cb401c0b2d7a941a13a92de5f2402fab87c51aba5c3cfd19570da6b632
* `src/core/src/zava_forward/core/store.py` c7643dfabef44868dc8a8ad335d51d998644ba15f74f351aa94f968d39de3f40
* `src/core/tests/sqlguard.py` 8cfd5942c47c901d9e7d09ce07a43eb577d67074c67e8cc84b1d46d2dcb048d9
* `src/core/tests/test_priority_order.py` 591728c756fc7c55161b8c86281fb741413d321cc7a7b28f981066a0dcb6c42e
* `src/api/src/zava_forward/api/web/app.js` 19fd369a07b0b0ce72d26f5d3ffe028334020ce0f3b710378a4c3220cf409390
* `src/core/README.md` 107e841ca30488aa0a896d4fb434a08a20b1cb6dbfb002f3da8bbcfcbf77fdf1

## Web guidance

The web-interface-guidelines source was fetched before the edit (first 8000 characters only, partial) and again before review (complete, 20000 characters). The one-line change adds a semantic `p` with `role="status"` and plain text with a next step; no style, motion or control change.

## Divergences and process notes

* The proof model keeps the plan's refinement: no timestamp alone proves order, and unaudited legacy rows are always unresolved for the newest record. This is conservative by design; it may flag many legacy employees until the data owner decides.
* `sqlguard.py` and the README were first rewritten with a scripted edit rather than the edit tool; contents were reviewed in the diff.
* The red run used a copy of the C2 tree in `/tmp/ama-1292-scratch/c2tree-c3` (created, not removed); no existing path was changed.

## Overlap with other work

The running #1288 branch also changes `src/core/README.md` and may change the priority UI in `app.js`. This change touches the "Priority recommendation creation order (#1292)" README section and one line in the priority panel. Integration order and conflict resolution are left to the coordinator.

## Unproven or pending

Native SQL Server red/green for the C3 source, the two original selectors on SQL Server, the ledger-enabled migration, SQL Server scale, the real Docker provisioning and `docker inspect` path, the FULL local gate with verified external receipt, independent exact-head review, hosted CI and current-base integration with #184 and #1288. Data-owner resolution of flagged records and the rolling-release boundary remain human decisions; no resolution mechanism was added.

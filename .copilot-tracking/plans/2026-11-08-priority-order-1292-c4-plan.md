---
title: Issue 1292 C4 correction plan
description: Plan to correct the fourth independent review with a stricter in-batch proof, a fence-based cutover proof, C1 history review, a shared unresolved projection, adapter BEGIN recovery, committed-reload outcome, bounded repair work and stronger fixture and anchor checks
ms.date: 2026-11-08
---

Task `1292-priority-order-reload`, correction C4 (FULL tier because of SQL migration and safety; earlier tier amendments stand). Original plan, critique, amendment and C1 to C3 plans are unchanged. Details: `.copilot-tracking/details/2026-11-08-priority-order-1292-c4-details.md`. Research: `.copilot-tracking/research/2026-11-08-priority-order-1292-c4-research.md`.

## Phases

1. Commit this research, plan and details before any source or test edit.
2. Write failing tests first (red on unchanged source), then correct `sqlstore.py`, `store.py`, `continuity.py`, `mssqlstore.py`, `ledger`-facing validation in `sqlstore.py`, `tests/sqlguard.py`, the committed-outcome handling in `server.py` and the priority panel in `web/app.js`.
3. Run light SQLite, in-memory and fake-adapter red/green, ruff, mypy, `git diff --check` with unique retained logs and individual exits. Refresh the web guidelines before the web edit and again before review.
4. Write the C4 changes record and one original review; commit issue-owned files only.

## Red/green scenarios (synthetic, light)

* F1: historical orphan event A (10:00), committed B (10:01), later insertion and edit of A: B is flagged. Tied `seq` with different timestamps and audit agreement: flagged. Audit, distinct unedited `seq` and a backward clock step all agreeing: confirmed.
* F2: genuine C1-shaped metadata (`rec_order_backfills` list, no batch keys, positive ordinal, no `rec_order_review`): reviewed at open, A flagged, ordinals unchanged, review batch recorded; malformed list flags conservatively.
* F3: full and limited continuity exports for flagged Proposed, Accepted and Edited latest: `actionable` and `relied_on` false, `order_confirmed` false, `order_note` present; unflagged and other employees unchanged.
* F4: fake driver whose BEGIN batch raises after opening: original error kept, rollback issued (or connection discarded when rollback fails), `in_tran` false, next BEGIN not nested; SQLite store BEGIN failure issues no rollback.
* F5: native A, old-writer singleton B same second with creation events: B confirmed, accept allowed; two old-writer zero rows B, C same second: flagged; flagged previous newest propagates; second employee unaffected.
* F6: post-commit reload exhaustion raises `CommittedReloadError`; exactly one durable proposal; HTTP layer returns a committed outcome (not a retry-inviting 500).
* F7: legacy Accepted and Edited flagged latest: panel renders the accessible note after reload (static and string-level check on `app.js` plus API payload).
* F8: guard negatives: `127.0.0.1` listener versus binding `127.0.0.2`, IPv4 versus `::1`, `localhost` name, remote `DOCKER_HOST`, non-default `DOCKER_CONTEXT`; all before connection or inspection.
* F9: pending `ai_record` for a dropped `ai_task` and an `ai_run_end` quarantined without losing unrelated entries; failure before and after BEGIN; later flush and save persist neither task nor event.
* F10: repeated singleton repairs for one employee fetch and decode a constant number of history rows (counted through a row-decoding probe), not growing with history.
* F11: many singleton batches in metadata upgrade with a bounded comparison count (range coalescing probe) and unchanged flags.
* F12: digest made unreadable without changing size or mtime invalidates cached evidence; a same-size same-mtime replacement invalidates; restoring readability recovers.
* F13: digest files `{}`, a JSON array, non-integer, boolean, zero and negative counts, and a self-consistent rechain conflicting with a valid digest are unusable evidence; no exception at startup.

## Out of scope and pending

SQL Server red/green, real lock timeout and `@@TRANCOUNT` evidence, ledger-enabled migration, scale, real Docker admission, FULL gate with external receipt, independent review, hosted CI, integration with #184 and #1288, data-owner resolution of flagged records and the rolling-release boundary.

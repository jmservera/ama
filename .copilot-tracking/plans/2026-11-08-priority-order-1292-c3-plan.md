---
title: Issue 1292 C3 correction plan
description: Plan to correct the third independent review with a two-signal order proof, a versioned historical review, a server-enforced unresolved boundary, anchor revalidation, BEGIN-failure quarantine, indexed unresolved records and verifiable fixture provisioning
ms.date: 2026-11-08
---

Task `1292-priority-order-reload`, correction C3 (FULL tier because of SQL schema and migration; the earlier gate-tier amendment stands). Original plan, critique, amendment, C1 and C2 plans are unchanged. Details: `.copilot-tracking/details/2026-11-08-priority-order-1292-c3-details.md`. Research: `.copilot-tracking/research/2026-11-08-priority-order-1292-c3-research.md`.

## Phases

1. Commit this research, plan and details before any source or test edit.
2. Write failing tests first (red on unchanged source), then correct `sqlstore.py`, `store.py`, `tests/sqlguard.py` and the priority panel in `web/app.js`.
3. Run light SQLite and in-memory red/green, the existing JS syntax check if available, ruff, mypy, `git diff --check`; unique retained logs and individual exits.
4. Write the C3 changes record and one original review; commit issue-owned files only.

## Red/green scenarios (SQLite, synthetic)

* F1: audited A (10:00) then unaudited B (09:59) legacy, same employee: latest is unresolved. Fully unaudited pair with a backward clock and unedited seq disagreement: unresolved. Unaudited pair with agreeing timestamp and distinct unedited seq: confirmed. Edited older row: unresolved. Another employee and `ai_task` unaffected.
* F2: historical orphan event A, intervening B, later insertion and edit of A, audit order A then B: latest view is not confirmed. Tied transaction seq with same second: unresolved.
* F3: database with `rec_order_batches` written by C1 and an unproven latest: reviewed once at open, ordinals unchanged, marker set, review batch recorded. C0 database plus an old-writer zero row at startup: review still runs before the repair batch.
* F4: C0 positive ordinals B (09:59, audit 2) before A (10:00, audit 1) across timestamps: A flagged.
* F5: GET latest, direct POST accept and edit on a flagged Proposed record raise `PermissionError` and record nothing; reject succeeds; an already accepted flagged row projects `actionable` false and `relied_on` false; a non-flagged older record is unaffected; `web/app.js` renders `order_note` (static check).
* F6: same-head newly appearing mismatching daily digest invalidates cached evidence; an appended entry dated in a sealed year whose year digest differs invalidates the incremental extension.
* F7: one-shot injected `BEGIN IMMEDIATE` failure: no rollback of an unopened transaction, recommendation and pending `ai_run_end` quarantined, lock-exit flush and later unrelated save persist neither.
* F8: guard negatives (no container, container not running, wrong label, non-loopback binding, wrong port, password mismatch, old container, manifest-only) all before any connection; positive with a fake inspector; no real Docker call.
* F9: repeated ambiguous batches: unresolved rows grow by at most one per employee per batch, per-batch writes do not read or rewrite earlier records (counted statements), lookup is a primary-key read; existing JSON list is copied once under its marker and left in place.

## Gates

* Light only now: unittest red/green, ruff, mypy, `git diff --check`.
* Pending and not started: actual SQL Server (two original selectors, `MssqlPriorityOrder`), ledger-enabled migration, SQL scale, Docker provisioning path, FULL local gate and verified external receipt, independent exact-head review, hosted CI, current-base integration with #184 and #1288.

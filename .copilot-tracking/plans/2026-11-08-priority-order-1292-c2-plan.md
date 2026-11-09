---
title: Issue 1292 C2 correction plan
description: Plan to correct the second independent review with an atomic retryable reader, rollback-safe queue sync, provable audit ordering, visible unresolved state, bounded repair and verified fixture admission
ms.date: 2026-11-08
---

Task `1292-priority-order-reload`, correction C2. Original plan, critique, gate-tier amendment and the C1 plan are preserved unchanged. Details: `.copilot-tracking/details/2026-11-08-priority-order-1292-c2-details.md`. Research: `.copilot-tracking/research/2026-11-08-priority-order-1292-c2-research.md`.

## Phases

1. Commit this research, plan and details before any source or test edit.
2. Add failing tests first (red on unchanged source), then correct `sqlstore.py`, `store.py` and `tests/sqlguard.py`.
3. Run light SQLite and in-memory red/green, ruff, mypy and `git diff --check` with unique retained logs.
4. Write the C2 changes record and one original review, then commit.

## Findings to red/green scenarios (SQLite, synthetic)

* F1: an old writer commits a zero-ordinal row (insert plus `meta.seq` bump on a second connection) at each of three barriers: after the first sequence read, after the recommendation fetch and after the second sequence read. `latest_priority` must be the true newest after each; a later `save` and a second employee must be unaffected and the zero row must never be cached.
* F2: queue failure injected after an old insert; another old write then reuses the sequence number; recommendations and case views must reflect it.
* F3: real A then B through `ai_priority` with `datetime` stepped backward; migration must keep audit order and the batch text must match.
* F4: missing and broken audit with A, B, edit of A: API `latest_priority` must return `order_confirmed=false`, `actionable=false`; a different employee and an `ai_task` record must be unaffected.
* F5: injected non-conflict `save` failure after the creation event; the recommendation and event must not persist; an intervening B plus later unrelated save leaves B newest. Historical orphan event with unedited `seq` contradiction must be flagged unresolved.
* F6: self-consistent rechain with `audit_head` rewritten and a retained mismatching digest; order must not be trusted.
* F7: database opened by the C0 source (archive of `16375e3ca`), then opened by C2: affected group listed as unresolved, ordinals unchanged, one `c0-review` batch.
* F8: repeated singleton repairs with a large synthetic audit: audit verification runs once per process and per-batch records are separate keys (counted, not timed alone).
* F9: guard negative cases: loopback without manifest, manifest for another port, manifest with another password digest, group-writable manifest, all before any connection.

## Gates

* Light only here: unittest red/green, ruff, mypy, `git diff --check`.
* PENDING and not started: native SQL Server red/green on a verified task-owned container, the two original selectors, ledger-enabled migration, SQL Server scale, FULL local gate with verified external receipt, independent exact-head review, hosted CI. All need separate coordinator admission to the shared heavy resource.
* Human decisions: how the named data owner resolves flagged legacy records; the rolling-release boundary for draining pre-fix writers.

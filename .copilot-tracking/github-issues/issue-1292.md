---
title: Preserve the newest priority recommendation after SQL reload
description: Issue metadata and acceptance status for #1292, the SQL recommendation creation-order defect
ms.date: 2026-11-08
ms.topic: reference
---

## Issue

* Issue: #1292, https://github.com/jmservera/ama/issues/1292 (open when read 2026-11-08).
* Labels: area:ai, bug, delivery:demo-next. Severity: Medium. Project: AMA Plan (In Progress).
* Refs: #81 (selected SQL evidence blocked on this fix) and #440.
* Branch: fix/priority-reload-1292 (worktree issue-1292-priority-order), base 6354b13f7abf1441a815e92f2b01dc184ce0b0ac, PR target main.
* Dependencies: none for the bounded fix. No stacking on #184 or #1288 (no file overlap in core sqlstore or store at their current heads, per coordinator).
* Scope: SQL recommendation order only. No ranking-policy, approval, consent, deployment or live-data change.

## Acceptance criteria status (local frozen candidate)

* [x] Deterministic creation ordering across cold and incremental reload: implemented (immutable `created_ord`), SQLite and in-memory executed; see changes record.
* [x] Same-transaction ties, edits of older proposals, multiple users, interleaved writers; legacy transition documented (README, `meta.rec_order_legacy`).
* [ ] Focused regression on actual SQL Server with zero skips: red/green on SQLite done (base source fails 2 failures, 3 errors; head OK); SQL Server PENDING heavy-lock admission.
* [x] Review and approval boundary unchanged.
* [ ] RPI evidence delivered via PR: records committed on the branch; PR not opened (coordinator).

The issue stays open. Use Refs, not a closing keyword, until native SQL Server evidence, independent exact-head review and hosted CI exist.

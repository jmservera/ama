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

## Acceptance criteria status (local frozen candidate; updated by the changes record)

* [ ] Deterministic creation ordering across cold and incremental reload: see changes record.
* [ ] Same-transaction ties, edits of older proposals, multiple users, truthful legacy transition: see changes record.
* [ ] Focused regression red then green, SQLite and in-memory parity, actual SQL Server with zero skips: SQL Server PENDING heavy-lock admission.
* [ ] Review and approval boundary preserved: see changes and review records.
* [ ] RPI research, plan, changes and review evidence on this branch.

The issue stays open. No closing keyword is justified until native SQL Server evidence, independent exact-head review and hosted CI exist.

---
title: Issue 86 reconciliation of published parent c5edb32 plan
description: Plan, one normal merge with explicit conflict resolution, light checks (Refs #86)
ms.date: 2026-11-08
---

Eventual tier FULL (lifecycle, SQL and security-sensitive controls). This step is LIGHT only: no gate, lock, Docker, scanner, browser, SQL Server or images.

1. Commit prospective research, plan, details and the independent critique alone; verify nothing else changed.
2. One normal `git merge --no-ff c5edb32` (pinned, existing local object). No rebase, force, push or retarget; parent worktree untouched.
3. Resolve only the three conflicts, per hunk, keeping both intents: for each file confirm that the published side's hunks are contained in the child side (superset proof), then take the child's content. Stop with a scoped human decision if any source hunk is not contained. Authorised exception (critique finding 1): the evidence pack's one-line `ms.date` difference keeps the child's newer 2026-11-07 date.
4. Prove: both parents; `c5ed` and `e888` ancestors; main `f548` ancestor; non-tracking merged tree equal to the child's tree (or list each difference); `store.py` contains `require_quality_evidence` and `quality_evidence_gate`; incoming tracking blobs equal c5ed's; complaint source blobs unchanged; log prefix unchanged.
5. Light checks from a whole git archive, non-editable own-source venv in `/home/azureuser/.local/share/ama/gates/g86-receiver-light-r1` with origin proof: core `test_quality_procurement`, `test_gates`, `test_hazard_referral`, `test_quality_procurement` (covers the appointment outcomes), `test_resident_decisions`; strict mypy; ruff on `src tests` (not the build directory).
6. Changes (every resolution and auto-merge explained) and one author Review; commit; freeze.

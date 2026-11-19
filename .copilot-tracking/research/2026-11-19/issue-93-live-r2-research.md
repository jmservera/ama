---
title: Issue 93 live research, first unmet DEMO criterion (2026-11-19)
ms.date: 2026-11-19
---

Task `issue-93-live-20261119`. Refs #93. Base `b9e3f98d4` (origin/main had moved to `e5a9a59d9` when fetched). Disposition: executed (opening record; findings appended below).

## Opening scope

* Issue #93 has three criteria: C1 stabilization checkpoint #440 (unticked), C2 all child features closed or deferred (unticked), C3 no automated finance authority (ticked).
* First unmet: C1. It is an evidence and owner-decision criterion, not a code gap; a prior audit (`docs/reference/research/issue-93-epic-audit-live-2026-11-18.md`) found no confirmed finance defect needing a fix.
* Plan: re-prove C1 sub-points and C3 with fresh local tests and a read-only live probe, record a per-criterion proven/unproven table, change no source.

## Findings

* A same-day earlier run (`issue-93-live-*` artifacts, test `tools/test_epic_93_child_disposition.py`) is preserved unchanged; this run uses the `-r2` suffix. The earlier opening record above was drafted before that collision was noticed and the tracked files were restored.
* Fresh evidence: 269 offline tests OK (45 skipped), 4 existing disposition tests OK, read-only live probe (five GETs, 200), revision 0000033, GitHub state unchanged (#96 and #440 OPEN, no owner deferral).
* New finding: the #93 body cites BRD FR-018 and FR-019, which are handoff and capacity rules in the BRD; the finance rows are FR-023, FR-024, RULE-009, RULE-010, RULE-012.
* Planning Readiness: Ready. Gap for code: none confirmed (C1 and C2 are owner-decision gated); evidence note only. Full detail in `docs/reference/research/issue-93-first-unmet-criterion-live-2026-11-19.md`.

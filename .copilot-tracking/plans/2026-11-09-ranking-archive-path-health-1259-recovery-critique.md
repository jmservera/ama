---
title: Issue 1259 recovery preparation critique
description: Single final-candidate critique of the recovery preparation plan
ms.date: 2026-11-09
---

Execution: Complete (one pass, author-run, not independent). Verdict: Proceed with changes, all applied directly.

* RC-001 (High) Default editable installs point at the primary checkout and would test the wrong source. Applied: out-of-tree non-editable venv from `git archive HEAD`, origin printed.
* RC-002 (Medium) Old red/green numbers are historical author claims. Applied: re-derive current counts and a scratch red check; report old figures only as retained evidence.
* RC-003 (Medium) A moving parent must not be merged or polled. Applied: dry-run `merge-tree` forecast only; resume point conditional on a frozen, reviewed parent.
* RC-004 (Medium) Do not imply the original AC are closed or deferred under Blob. Applied: explicit proposed-scope text, AC marked unmet.
* RC-005 (Low) Correction budget must not be reset or inferred. Applied: state retained-evidence count, unknown remainder, no consumption.

No finding conflicts with a confirmed owner decision; none requires an owner question.

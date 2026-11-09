---
title: Issue 86 reconciliation of published parent c5edb32 research
description: Prospective research for one normal merge of the actual published parent head (Refs #86)
ms.date: 2026-11-08
---

Scope: Refs #86 only; LIGHT preparation, not FULL or publication. Start `a8bfcca03fdc8515b7930712a32694fcd7b49bbf`, tree `a25e8f6c…`, ignored-clean, branch `feat/formal-complaints-adapter-86`. PR 1243 target `feat/controlled-lifecycle-integration-81` unchanged. Main `f548b65f…`.

## Premise correction

The earlier FULL attempt stopped correctly: published parent `c5edb320ad10d3d73bb985bfb82b2d0bee94381a` is NOT an ancestor of this child (explicit ancestry exit 1; merge-base `56eec736…`; child 76 commits ahead, published parent 5 ahead). The coordinator's earlier assertion was wrong (a shell OR swallowed exit 1). The local parent `e888a499` IS an ancestor. The dry-merge object `04180f9a…` in the coordinator note is not a candidate.

## Actual delta of c5ed since the merge-base (9 non-tracking paths)

`cutover-evidence-pack.md`, `appointments.py`, `gates.py`, `procurement.py`, `quality.py`, `store.py`, `test_gates.py`, `test_hazard_referral.py`, `test_quality_procurement.py`; commits #1226 (fail-closed quality gate), #1228 (FR-008 provenance), #1229 (capacity gate outcomes), plus two issue-81 tracking commits. These three commits are not ancestors of main; the local parent line carries them as separate commits with later corrections.

## Conflicts and dependent auto-merges (git merge-tree)

* Conflicts: `cutover-evidence-pack.md`, `appointments.py`, `test_quality_procurement.py`. Auto-merged: `quality.py`, `store.py`.
* Evidence that the child already contains the published input: `git diff c5ed HEAD` has zero deleted lines for `appointments.py`, `test_quality_procurement.py`, `quality.py`, `gates.py`, `procurement.py`, `test_gates.py`, `test_hazard_referral.py`. In `appointments.py` the child adds the later "sole missing capacity confirmation is Unknown" `elif` branch (commit `b205ed37`). The evidence pack: `git diff c5ed HEAD` is 185 insertions and 1 deletion; the one deleted line is the older `ms.date` (2026-11-06) and the 184 other added lines are child-side cut-over content to preserve. `store.py` deletions are main's ranking-archive hunks (older base lines) and a typing import; c5ed's own `store.py` change (`require_quality_evidence`, `quality_evidence_gate` import) must be present in the result.
* Expected resolution: the child's side for the three conflicts, justified by the superset proof, not a blind side choice; the merged non-tracking tree should equal the child's tree. To be verified after the merge, not assumed.

## Open and unchanged

Original Medium findings, adverse browser outcome, #1238 supersession policy, approvals. Limits: per-store registry, point-in-time guard, no real receiver.

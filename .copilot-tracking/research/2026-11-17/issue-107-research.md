---
title: Issue 107 evidence and closure audit research
ms.date: 2026-11-17
---

## Scope

Audit of issue 107 criteria against base eb51af5c9 (worktree base; origin/main later moved to 41322741). Docs plus one focused test, tier FOCUSED. Research disposition: executed. Planning Readiness: Ready.

## Criterion audit (checked boxes in the issue body)

* Fourteen of sixteen RAI/tokenomics/capability boxes are ticked; two stay unticked: the composite SQL race/restart/old-image criterion and delivered-build real-AI/Azure acceptance (CON-009/AC-057).
* The 2026-11-17 closure correction restored the composite criterion because the old-image proxy in `src/api/tests/test_assistant_restart_non_replenishment.py` is a current service built from fixtures, and PR 1268 did not run a real earlier image.
* The retained-old-image probe (db7ad278 and 510fd90f) was never executed against Docker/SQL; no result is claimed.

## Measured gap

`MaterialMismatch.variations()` in the restart file exercises five live changes on a separate worker and after restart: prompt, policy, permissions, scope, model version. `rel.BOUND` has thirteen bound fields. Live (not stored-row) changes to provider, endpoint, deployment, data and provenance had no separate-worker or restart test; the stored-row test in `test_assistant_release.py` (`test_each_binding_mismatch_denies_reactive_and_proactive_with_no_calls`) does not cover the revocation-persistence or late-completion paths.

Measurement: probe adding those five variations ran `test_assistant_restart_non_replenishment.py` locally on SQLite, 14 tests OK (17.7 s). No product defect found; the gap was coverage only. Probe diff preserved at `/home/azureuser/.local/share/ama/phase-witness/107-20261117T2352/probe-measure.diff`, then reverted so the implement phase starts clean.

## Limits

SQLite proxy only. No old image, actual SQL, real AI or Azure was run. Criteria 8 composite and delivered-build acceptance stay unticked; nothing here is closure evidence.

## Follow-ups

1. Actual old-image/disposable-SQL execution (needs the full tier and immutable image).
2. Issue 1840 malformed-completion false-VIOLATED case (separate issue).

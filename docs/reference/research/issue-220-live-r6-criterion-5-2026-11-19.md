---
title: Issue 220 criterion 5 classification (2026-11-19, run 6)
description: Stop note for the last unticked criterion of issue 220 with offline test re-run and live image check
ms.date: 2026-11-19
---

## Scope

Synthetic demo, desktop only. Refs #220. Only "No retaliation, inferred refusal or delayed hazard response" is unticked.

## Evidence

* Source on main already holds the guard (`no_retaliation_guard.py`, `challenges.py`) and the signed-in principal fix (`_same_signed_in_person` in `resident_decisions.py`). Code and tests for the criterion exist, so nothing remains to build on this base.
* Re-run in `src/core`: `python3 -m unittest` over `test_no_retaliation_guard_220`, `test_challenge_no_retaliation_220`, `test_issue_220_challenge_route` and `test_challenges`: 30 tests OK.
* `az containerapp show -g ama -n ca-cutover-test-demo-api` still reports image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`, the digest recorded before the identity fix. A successful live write cannot be observed without building and deploying a new image, which the owner did not authorise.

## Per-criterion result

| Criterion | Result |
| --- | --- |
| Digital and staff-recorded routes work | Ticked earlier; offline proven |
| Explanations, owner, next update, resolution visible | Ticked earlier; offline proven |
| Only dependent proposals and reviews stale | Ticked earlier; offline proven |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Ticked earlier; offline proven |
| No retaliation, inferred refusal or delayed hazard response | Offline proven (30 tests). Live unproven: needs an image redeploy. Real retaliation over time is production-only. Stays unticked. |

No source, Azure or credential change; no resource created.

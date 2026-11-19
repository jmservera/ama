---
title: Issue 220 stop note (2026-11-19, run 7)
description: Last unticked criterion of issue 220 is not buildable for the demo; offline proof re-run and live image re-checked
ms.date: 2026-11-19
---

## Scope

Synthetic desktop demo. Refs #220. Only "No retaliation, inferred refusal or delayed hazard response" is unticked.

## Evidence

* Main already holds the guard (`no_retaliation_guard.py`, `challenges.py`) and the signed-in principal fix. Nothing remains to build.
* In `src/core`, `PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 test_challenge_no_retaliation_220 test_issue_220_challenge_route test_challenges`: 30 tests OK.
* `az containerapp show -g ama -n ca-cutover-test-demo-api`: revision 0000033, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`, unchanged since the [run 6 note](./issue-220-live-r6-criterion-5-2026-11-19.md). A live successful write needs a rebuild and redeploy, which is not authorised.

## Per-criterion result

| Criterion | Result |
| --- | --- |
| Digital and staff-recorded routes work | Proven offline (ticked) |
| Explanations, owner, next update, resolution visible | Proven offline (ticked) |
| Only dependent proposals and reviews stale | Proven offline (ticked) |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven offline (ticked) |
| No retaliation, inferred refusal or delayed hazard response | Offline proven; live unproven; retaliation over time is production-only. Stays unticked |

No source, Azure or credential change; no resource created.

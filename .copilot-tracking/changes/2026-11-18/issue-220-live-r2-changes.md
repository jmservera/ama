---
title: Changes for issue 220 live proof, third pass
ms.date: 2026-11-18
---

Refs #220. Validation tier: FOCUSED (documentation only; no `src/` change, no `rpi-checks.py --all`).

## Files

* Appended a third-pass section to `docs/reference/research/issue-220-live-challenge-route-evidence-2026-11-18.md`.
* Appended an entry to `docs/reference/log.md`; added these `issue-220-live-r2-*` RPI artifacts and updated the state file.

## Observations

* `az containerapp show` for `ca-cutover-test-demo-api`: revision `ca-cutover-test-demo-api--0000031`, digest `sha256:5368f4e4...e17e5fb`, modified 2026-11-17T19:41:58Z (unchanged); `/healthz` 200. A first `az containerapp revision list` call returned an ARM 503 and was not retried. Observed; raw output not retained.
* `src/core/src/zava_forward/core/resident_decisions.py` line 1112 still has `actor != _person(store, user.get("email"))`.
* `tests.test_no_retaliation_guard_220` in `src/core`: 5 OK. `tests.test_challenge_non_retaliation_hazard_guard` in `src/api`: 9 OK. Observed; raw output not retained.

## Per-criterion table

| Criterion | Status for the demo |
| --- | --- |
| Digital and staff-recorded routes work on constructed challenges | Unproven live (offline proven); Entra staff writes still refused |
| Permitted explanations, owner, next update, resolution visible | Unproven live; no challenge and no AI priority suggestion |
| Only dependent proposals and reviews become stale | Unproven live; needs a correction write |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Partly proven (forbidden fields refused 400, state unchanged); positive write unobserved |
| No retaliation, inferred refusal or delayed hazard response | Unproven live; guarantees and assurance flags observed in the earlier live pass, 14 offline tests pass |

Mypy, ruff and web tests not applicable (no source or web change). No Azure resource created; nothing to delete. No credential was read or printed in this pass.

## Follow-ups

1. Fix the Entra principal versus roster comparison in `resident_decisions._operation` (FULL tier; redeploy needs owner approval), then rerun `run1.py`.
2. Exercise `challenge_open` once AI priority suggestions are enabled.

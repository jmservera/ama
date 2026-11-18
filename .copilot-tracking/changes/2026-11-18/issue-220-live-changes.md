---
title: Changes for issue 220 live proof
ms.date: 2026-11-18
---

Refs #220. Validation tier: FOCUSED (documentation and evidence only; no `src/` change, no `rpi-checks.py --all`). Note: `docs/reference/research/issue-220-live-challenge-route-evidence-2026-11-18.md`.

## Files

* Added the research note, evidence folder `.copilot-tracking/evidence/2026-11-18/issue-220-live/`, and RPI artifacts.
* Updated `docs/reference/README.md` and appended `docs/reference/log.md`.

## Per-criterion table

| Criterion | Status for the demo |
| --- | --- |
| Digital and staff-recorded routes work on constructed challenges | Unproven live (offline proven); Entra staff writes refused by identity defect |
| Permitted explanations, owner, next update, resolution visible | Unproven live; no challenge exists and no AI priority suggestion available |
| Only dependent proposals and reviews become stale | Unproven live; needs a correction write |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Partly proven: forbidden fields refused 400, state hashes unchanged; positive write unobserved |
| No retaliation, inferred refusal or delayed hazard response | Unproven live; guarantees and assurance flags observed live, 14 offline tests pass |

## Validation

* `python3 -m unittest tests.test_no_retaliation_guard_220` in `src/core`: 5 OK.
* `python3 -m unittest tests.test_challenge_non_retaliation_hazard_guard` in `src/api`: 9 OK.
* Literal credential scan of evidence: no match. No Azure resource created; none to delete.
* Mypy, ruff and web tests not applicable (no source or web change).

## Follow-ups

1. Fix Entra principal versus roster comparison in `resident_decisions._operation` (FULL tier; redeploy needs owner approval).
2. Rerun `run1.py` after redeploy; exercise `challenge_open` with an AI priority suggestion.

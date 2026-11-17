---
title: Challenge non-retaliation research (issue 220)
ms.date: 2026-11-14
---

## Scope

Final unticked acceptance criterion of issue #220: "No retaliation, inferred refusal or delayed hazard response". Base c9d4204029692886e26fdf56011c25d2fd180e1a (stacked on PR #1639).

## Evidence

* `src/core/src/zava_forward/core/challenges.py`: store-independent register that states a `NOT_INFERRED` list but has no enforcement on the live case path.
* `src/core/src/zava_forward/core/resident_decisions.py`: live writers `_res_challenge_open`, `_res_challenge_resolve` and `_res_nomination_correct` (the data-correction path) mutate the case inside the serialized writer; a raised error rolls the write back.
* Ranking inputs (`ranking.py`): open hazard, support, `days_in_stage`, `stage`. Consent state: `measure_decisions` and `resident_reviews`. Hazard clocks: `hazards[*]` fields such as `response_due_at`, `released`, `hold`.
* `Store.detail` supplies `challenge_targets` only to readers with challenge rights; `panels.js` `affectedChallengePanel` renders the explanatory text.
* Existing tests: `src/core/tests/test_challenges.py`, `src/api/tests/test_resident_api.py`.

## Findings

* The criterion is stated in text only; nothing would stop a future change from altering protected state in these writers.
* Planning readiness: Ready. No owner-approved hazard clock limit exists or is introduced; the guard only asserts nothing changes.

## Boundaries

No legal interpretation, no change to hazard process, consent or ranking policy.

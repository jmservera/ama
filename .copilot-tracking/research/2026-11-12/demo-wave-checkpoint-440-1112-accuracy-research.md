---
title: Research, accuracy follow-up, demo wave checkpoint 440 (2026-11-12)
description: Additive research for two documentation accuracy items in the frozen checkpoint record; originals are unchanged
ms.date: 2026-11-12
---

Task `demo-wave-checkpoint-440-1112-accuracy`, parent `demo-wave-checkpoint-440-1112` (frozen head `26cb3968028c8cda9f0211fdec939a71f32df201`). Refs #440 only. Documentation accuracy of this new recurring record; not a source, HVE or coordinator-code correction, not a reopening of the exhausted old #440 campaign and not a new correction pool. Research disposition: `executed` (source reading plus the existing source-unchanged diagnostic). Planning Readiness: `Ready`.

## Item 1: 1467 wording

* Source at pin (`e3339de62`): `_finite_observation` returns true for any `int` (no `isfinite` call, which would overflow) and for a finite `float`; otherwise the observation is Unknown. T2 `test_huge_integer_observation_still_breaches` and `test_nonfinite_observation_is_unknown_not_within` agree.
* The pack row (`cutover-evidence-pack.md` line 7409) says "non-finite or huge-integer-unsafe ... observation as Unknown", which wrongly implies huge integers become Unknown. Correct statement: NaN or infinite observations become Unknown (pause); arbitrarily large integers are assessed normally and no `isfinite` overflow occurs. No product defect is implied.
* The original research (table row for 1467) says "non-finite committed or tolerance observation becomes Unknown (pause)"; it is accurate and is not edited. The original Review is not edited either; this follow-up and its Review addendum carry the correction.

## Item 2: agents namespace None

* `02b-preflight-origins.log` printed `None` for `zava_forward.agents.__file__` because it is a namespace package; the namespace alone proves no concrete origin. It is preserved unchanged.
* A post-freeze, source-unchanged import trace (same owned venv, cwd, `env -i` and `PYTHONPATH`; 2026-11-12 17:41Z) imported the seven T5/T6/T7 test modules and compared each loaded module `__file__` hash with `git hash-object` against `HEAD:<path>`: 14 of 14 matched, none from the primary checkout. Concrete agents modules: `chat` `ae03ad5f25e5`, `dispatch` `2e2306c62790`, `regulatory_chat` `d8937e62df1a` (all under `src/agents/src/zava_forward/agents/`). Helpers: `release_support` `49f5dd6feda9`, `test_assistants` `0caa5d78b5b8`, `test_mvp` `cb44625f4869`, `checks.data_operator_ai_state` `37193aaa1e68`.
* Limitation: a fresh import trace of the same selectors, not instrumentation of the original 281-test runs; only T5 imports `zava_forward.agents` directly; transitive imports of the other modules were not traced. Raw diagnostic: `/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112/diag/agents-origin.out` and `.err`.

## Scope guards

* Tested source pin stays `bbb1d20cc984`, source-equal fresh main `5ee8ac14c70f`. Newer main (`088e8c3`, containing PR 1470) is outside the tested wave and is not claimed as accepted.
* No test rerun, install, service, rebase or push; #134 integration (`0003a55` on `088e8c3`) and publication stay with the coordinator.

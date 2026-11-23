---
title: Issue 220 thirteenth run, camelCase, punctuation and Unicode key variants in the challenge guard (2026-11-23)
description: Second code gap in the non-retaliation guard, fixed with a regression test, with a per-criterion proven and unproven table
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Finding

After the [twelfth run](./issue-220-live-r12-key-normalisation-2026-11-23.md) the guard in `src/core/src/zava_forward/core/challenges.py` still accepted `hazardPause`, `RetaliationFlag`, `inferredRefusal`, `noAccess`, `hazard.pause`, `hazard/pause`, `hazard__pause`, an en-dash variant, a full-width spelling of `retaliation` and `retaliation` followed by a zero-width space (probe 2026-11-23). The canonical key form now applies NFKC, removes format characters, splits camelCase and collapses every non-alphanumeric run to one underscore.

## Evidence

* Regression test `test_adverse_keys_are_rejected_despite_camel_case_punctuation_and_unicode_variants` in `src/core/tests/test_challenge_no_retaliation_220.py`: 10 sub-test failures without the change, pass with it; benign keys (`consentGiven`, `hazardNote`) stay accepted.
* The four 220 challenge core modules pass (33 tests); ruff check and format pass; mypy reports no error in the changed files.
* No live Azure change. The demo apps still run the earlier guard; deployment is a separate step.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven live (r11) | Earlier probe |
| Explanations, owner, next update, resolution visible | Proven live and offline (r11) | Earlier probe; tests |
| Only dependent proposals and reviews stale | Proven offline (r11) | Tests |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live (r11) | Earlier probe |
| No retaliation, inferred refusal or delayed hazard response | Proven for the constructed case; guard hardened offline again, not deployed. Behaviour over time needs production history and cannot be shown in the demo | Tests; probe |

Owner-gated: ticking the final checkbox. Not needed for the demo: billing, DPO or Legal approval, person-run assistive-technology testing.

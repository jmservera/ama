---
title: Issue 220 twelfth run, adverse-key normalisation in the challenge guard (2026-11-23)
description: Code gap found and fixed in the non-retaliation guard, with a per-criterion proven and unproven table
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Finding

`reject_adverse_mapping` and `assert_no_adverse_challenge_effects` in `src/core/src/zava_forward/core/challenges.py` matched forbidden keys exactly. A probe on 2026-11-23 showed `Retaliation_Flag`, ` refusal`, `hazard-pause`, `HAZARD_PAUSE` and `priority penalty` were all accepted. Keys are now compared after strip, lower case and mapping of hyphens and spaces to underscores.

## Evidence

* Regression test `test_adverse_keys_are_rejected_despite_case_spacing_and_hyphen_variants` in `src/core/tests/test_challenge_no_retaliation_220.py` fails before the change and passes after it.
* The 10 tests in the two 220 core modules pass; ruff check and format pass on the changed files; mypy reports no error in `challenges.py` (3 existing errors in other files).
* No live Azure change: the fix is not deployed, so the live app still runs the earlier guard. The live proof of the constructed case stays in the [eleventh-run note](./issue-220-live-r11-revision-0054-2026-11-23.md).

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven live (r11) | Earlier probe |
| Explanations, owner, next update, resolution visible | Proven live and offline (r11) | Earlier probe; tests |
| Only dependent proposals and reviews stale | Proven offline (r11) | Tests |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live (r11) | Earlier probe |
| No retaliation, inferred refusal or delayed hazard response | Proven for the constructed case; guard hardened offline this run, not yet deployed. Behaviour over time needs production history and cannot be shown in the demo | Tests; probe |

Owner-gated: ticking the final checkbox. Not needed for the demo: billing, DPO or Legal approval, person-run assistive-technology testing.

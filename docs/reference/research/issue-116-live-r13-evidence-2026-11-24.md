---
title: Issue 116 live round 13 evidence (2026-11-24)
description: Closes a part-count gap in the shared provider-boundary allowlist and records per-criterion status for the demo
ms.date: 2026-11-24
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. The [r12 note](./issue-116-live-r12-evidence-2026-11-23.md) capped aggregate image bytes; this round rereads the part loop of `approved_payload`. No credential was read and no Azure resource was created or changed.

## Finding and fix

`approved_payload` in `src/core/src/zava_forward/core/ai.py` bounded text bytes and decoded image bytes but not the number of parts. A list of empty text parts, or of empty images, passed every size allowlist, so the provider body had no bound. Lists above `MAX_PARTS` (8) are now refused as `input-too-many-parts` before the verifier, hold and meter. `look_at`, the only real multi-part caller, sends two parts.

## Results

| Check | Result |
| --- | --- |
| New test (nine empty parts refused with the reason, eight accepted), without the fix | Import error on `MAX_PARTS` (fails) |
| core `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_ai_dispatch_marker` with the fix | 40 tests, OK |
| api `test_ai_consumption_api`, `test_assistants_dispatch`, `test_resident_assistant_provider`, `test_ai_boundary_caller_inventory` | 59 tests, OK |
| agents `test_dispatch` | 19 tests, OK |
| ruff check and format check on changed files | Clean |
| mypy in `src/core` | 3 errors in 2 files, as in the r12 baseline |

## Status

The only unticked box (allowlists at every provider boundary) stays unticked: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; `rpi-checks.py --all` was not run. Refs #116.

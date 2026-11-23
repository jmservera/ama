---
title: Issue 116 live round 12 evidence (2026-11-23)
description: Closes an aggregate-size gap for image parts in the shared provider-boundary allowlist and records what stays unproven
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The [r11 note](./issue-116-live-r11-evidence-2026-11-23.md) fixed unencodable text; this round rereads the size limits of `approved_payload`. No credential was read and no Azure resource was created or changed.

## Finding and fix

`approved_payload` in `src/core/src/zava_forward/core/ai.py` capped each image at 4 MiB but summed only text bytes. A structured payload with many images, each under the cap, passed the size allowlist, so total provider input was unbounded. The decoded image bytes are now summed across parts and refused as `input-image-too-large` above `MAX_IMAGE_BYTES`, before the verifier, hold and meter. `look_at`, the only real image caller, sends one image, so its behaviour is unchanged.

## Results

| Check | Result |
| --- | --- |
| New test (three half-cap images refused, two accepted), without the fix | 1 failure |
| core `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_ai_dispatch_marker` with the fix | 39 tests, OK |
| api `test_ai_consumption_api`, `test_assistants_dispatch`, `test_resident_assistant_provider` | 57 tests, OK |
| ruff check on changed files | Clean |
| mypy in `src/core` | 3 errors in 2 files, unchanged from baseline |

## Status

The box stays unticked: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; `rpi-checks.py --all` was not run. Refs #116.

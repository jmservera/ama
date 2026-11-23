---
title: Issue 116 live round 10 evidence (2026-11-23)
description: Closes a raw-content gap in the shared provider-boundary allowlist for image data and records what stays unproven
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The [r9 note](./issue-116-live-r9-evidence-2026-11-23.md) fixed the string-size ordering; this round rereads the image branch of `approved_payload`. No credential was read and no Azure resource was created or changed.

## Finding and fix

`approved_payload` in `src/core/src/zava_forward/core/ai.py` accepted any text after `data:image/png;base64,` or `data:image/jpeg;base64,`. A structured part carrying free text there passed the type allowlist and reached the provider labelled as an image. The function now decodes the data with strict base64 validation and refuses failures as `input-type-not-approved` before the verifier, hold and meter. `look_at` encodes real bytes, so its output is unaffected. Magic-byte checks were not added because existing tests send non-image bytes deliberately.

## Results

| Check | Result |
| --- | --- |
| New test with four malformed payloads, without the fix | 4 failures |
| core `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_ai_dispatch_marker` with the fix | 37 tests, OK |
| api `test_ai_consumption_api`, `test_assistants_dispatch`, `test_resident_assistant_provider` | 57 tests, OK |
| ruff on changed files | Clean |
| mypy in `src/core` | 3 errors in 2 files, unchanged from baseline |

## Status

The box stays unticked: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; `rpi-checks.py --all` was not run. Refs #116.

---
title: Issue 116 live round 11 evidence (2026-11-23)
description: Closes an error-labelling gap in the shared provider-boundary allowlist for unencodable text and records what stays unproven
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The [r10 note](./issue-116-live-r10-evidence-2026-11-23.md) fixed image data content; this round rereads the text branch of `approved_payload`. No credential was read and no Azure resource was created or changed.

## Finding and fix

Text containing a lone surrogate (for example `"\ud800"`) made `str.encode("utf-8")` raise `UnicodeEncodeError` in `approved_payload`. No provider call happened, but `Ai.evidence` reported `provider-unavailable` with no reason instead of `input-refused`, so the refusal was not visible as an input refusal. The size count now goes through `_utf8_size`, which refuses unencodable text as `input-type-not-approved` in `src/core/src/zava_forward/core/ai.py`. Replacing characters while encoding was rejected because it would silently alter the text.

## Results

| Check | Result |
| --- | --- |
| New test with three payloads (system, string user, list part), without the fix | 3 errors (`KeyError: 'reason'`) |
| core `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_ai_dispatch_marker` with the fix | 38 tests, OK |
| api `test_ai_consumption_api`, `test_assistants_dispatch`, `test_resident_assistant_provider` | 57 tests, OK |
| ruff check on changed files | Clean |
| mypy in `src/core` | 3 errors in 2 files, unchanged from baseline |

## Status

The box stays unticked: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; `rpi-checks.py --all` was not run. Refs #116.

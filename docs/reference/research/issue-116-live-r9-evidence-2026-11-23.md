---
title: Issue 116 live round 9 evidence (2026-11-23)
description: Closes an ordering gap in the shared provider-boundary allowlist for string input and records what stays unproven
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 116 shows one unticked box: allowlists at every provider boundary. The [r8 note](./issue-116-live-r8-evidence-2026-11-23.md) reran the suites; this round rereads `approved_payload` and finds a real gap. No credential was read and no Azure resource was created or changed.

## Finding and fix

`approved_payload` in `src/core/src/zava_forward/core/ai.py` returned early for a string `user`. The 128 KiB limit for strings ran later in `_request_body`, after the simulation verifier and the data-protection hold. A new test showed that with a hold in place an oversized string produced no `input-too-large` reason, so the shared allowlist did not bound string input by itself. The function now wraps a string as one text part, so strings and structured parts share one type and size check before any other gate. The later body-length check stays as defence in depth.

## Results

| Check | Result |
| --- | --- |
| New test, oversized string with a hold, before the fix | Failed (no `reason`) |
| core `test_ai_input_bounds`, `test_ai_provider_payload_spy`, `test_ai_dispatch_marker` | 36 tests, OK after the fix |
| api boundary and call-site inventories, `test_assistants_dispatch`, `test_resident_assistant_provider` | 25 tests, OK |
| ruff on changed files | Clean |
| mypy in `src/core` | 3 errors in 2 files, identical at baseline (missing opentelemetry stubs and an unused ignore); none from this change |

## Status

The box stays unticked by this note: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; the coordinator runs the gates and `rpi-checks.py --all` was not run. Refs #116.

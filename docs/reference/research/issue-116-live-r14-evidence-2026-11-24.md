---
title: Issue 116 live round 14 evidence (2026-11-24)
description: Closes the held-out provider gap in the provider-boundary allowlist and records per-criterion status for the demo
ms.date: 2026-11-24
---

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. No credential was read and no Azure resource was created or changed. The [r13 note](./issue-116-live-r13-evidence-2026-11-24.md) bounded the part count; this round walked every HTTP provider call site.

## Boundary inventory

| Boundary | Input allowlist before the request |
| --- | --- |
| core `Ai` (`ai.py`) | `approved_payload` (type, size, parts, image bytes) |
| resident assistant (`resident_demo/assistant.py`) | 512-byte ASCII prompt cap, fixed topic word |
| resident advisor (`resident_demo/aoai.py`) | 1 to 500 character question, fixed schema |
| held-out provider (`agents/heldout_aoai.py`) | None: system and prompt were sent as given |

## Finding and fix

The held-out provider built its request body from any `system` and `prompt` strings. It now calls the shared `approved_payload` first and returns an unmeasured `failed` envelope, with no HTTP request, for a non-string input or one above 128 KiB. No parallel validator was added.

## Results

| Check | Result |
| --- | --- |
| New test (oversize prompt, oversize system, `None` system, bytes prompt: no request, `failed`), without the fix | Fails |
| agents `test_heldout_aoai`, `test_heldout_batch` with the fix | 57 tests, OK |
| ruff check, ruff format check, mypy in `src/agents` | Clean |

## Status

The unticked box (allowlists at every provider boundary) stays unticked: live payload contents are not observable from the deployed apps, and independent review and hosted CI are outstanding. A src change takes the full tier; `rpi-checks.py --all` was not run. Refs #116.

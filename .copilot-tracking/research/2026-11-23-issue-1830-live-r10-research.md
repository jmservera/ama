---
title: Issue 1830 live r10 research (2026-11-23)
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

Scope: r6 to r9 covered receipts, queue wait, preflight and lock-line validation. New angle (r10): the receipt body itself. `load_receipt` and `commands_of` in `tools/rpi-gate-timing.py` trust the receipt content after the sha256 and schema check.

Hypothesis from reading lines 36-80: invalid JSON, a command lacking `group`, `argv`, `started` or `finished`, an unparseable timestamp, a naive-versus-aware timestamp mix, or `finished` before `started` raises an uncaught exception (traceback) or yields negative durations that corrupt the span and critical chain, instead of the tool's `REFUSED:` exit 2. Verified by experiment before the fix (see changes record).

Criteria 2 and 3 are proven for the demo by r6 to r8; criterion 4 needs a pull request (forbidden). Live Azure is out of scope by the issue boundary. Criterion 1 remains partly proven (receipts retained locally only).

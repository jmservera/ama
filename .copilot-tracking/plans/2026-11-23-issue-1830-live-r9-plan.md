---
title: Issue 1830 live r9 plan (2026-11-23)
ms.date: 2026-11-23
---

Tier: FOCUSED. Basis: `tools/rpi-gate-timing.py` is a read-only analysis tool; no runner, gate semantics, receipt scope, permission or security control changes. `rpi-checks.py` is untouched.

Plan: make `report --log` explicit about queue wait. A log whose first line is not the lock line reports `queue_wait_seconds: null` with a reason; a malformed timestamp or a negative wait is refused (exit 2). Add focused tests and a note in the r9 research and changes records.

## Critique (executed once)

Verdict: accept. Risk: changing JSON shape for existing consumers; disposition: the key is added only when `--log` is given and the valid path is unchanged. Risk: refusing a log from an older runner; disposition: a missing lock line is reported as null, not refused. No conflict with confirmed decisions; no repeat critique.

---
title: Issue 1830 live r16 review (2026-11-27)
ms.date: 2026-11-27
---

Review executed once, outcome: conformant for the stated scope. Boundary: `tools/rpi-checks.py` main(), its test, one README sentence, docs.

* The refusal compares each value with the parser default, so a legitimate `--preflight` call is unchanged (replay exit 0, label kept).
* `--lock-timeout` default 600 and `--heavy-lock-fd` are covered by the same loop; not separately tested (low risk, minor gap).
* Routed later work: independent exact-head review, hosted CI, and confirming #1297 merged first (owner-gated).

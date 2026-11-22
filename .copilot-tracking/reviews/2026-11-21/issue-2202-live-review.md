---
title: Issue 2202 review
ms.date: 2026-11-21
---

## Review

* Execution: one pass, executed after implementation.
* Boundary: working-tree diff (resident handler logging, one test, receipt note, index row, log entry) plus the recorded live evidence.
* Outcome: conformant for the proven criteria; two criteria stay unproven and are stated as such (half of homes with readings, resident hardening). No material finding is open in the change itself.
* Checks: targeted tests (55 OK), mypy and ruff clean. The logging line prints only the exception class and a code truncated to 40 characters, so no secret or resident data is logged.
* Not run: the full local gate (coordinator owns it); the logging change is not deployed.

## Routed follow-ups

1. Resident app hardening is unset: decide whether to enforce it (needs a rolled image).
2. Find why the `zavaforward_write` lock was held beyond 15 s (receiver or simulator contention).
3. Explain employee chat saying "Monitoring consent is unknown" for `ZF-2025-0031` while readings show.
4. Raise homes with readings beyond 2.3 percent (per-device secret limit).

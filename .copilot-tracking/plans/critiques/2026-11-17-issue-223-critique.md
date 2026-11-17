---
title: Issue 223 plan critique (one pass)
ms.date: 2026-11-17
---

Verdict: proceed. Findings applied directly.

* The new panels must go through the real store path, not call `gate_satisfied` directly: applied (use `run_panel`).
* A mutation-style test is needed so the checks cannot pass vacuously: applied (patch gate to always accept).
* Do not tick or imply any criterion; keep the "scripted, not people" wording and OQ-017 open items: applied.
* No SQL, security, infrastructure or deployment impact; FOCUSED tier holds.

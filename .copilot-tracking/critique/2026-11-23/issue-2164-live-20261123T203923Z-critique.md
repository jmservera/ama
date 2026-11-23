---
title: Critique for issue 2164 live r11
ms.date: 2026-11-23
---

Verdict: proceed. Executed once.

* Risk: reusing `authorize` staff resolution would change unbound Entra behaviour on the challenge route, which needs a real roster row. Disposition: mirror the `_gate` checks locally instead; applied.
* Risk: tests need a role that passes `appointment_evidence_visible`. Disposition: probe the role in the test and fail loudly if the baseline case is not allowed; applied.
* Live proof stays unproven (needs a roster edit and an Entra-bound account on the challenge route); stated as such.

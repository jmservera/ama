---
title: Critique for issue 110 live plan
ms.date: 2026-11-18
---

Single critique pass. Risks: (1) probe sends via SAS/HTTPS, not the production X.509 MQTT receiver, so the note must scope the claim to the demo; (2) leftover roles/job must be removed and checked; (3) key leakage mitigated by in-memory keys and a full-text leak check. Verdict: proceed; no conflicts with owner decisions. Disposition: all applied.

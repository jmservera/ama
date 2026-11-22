---
title: Issue 2201 review (second pass)
ms.date: 2026-11-21
---

Review executed once, after implementation. Outcome: conformant for local scope; deployment-dependent criteria remain open and are routed to the coordinator or owner.

* Retry affects only the bounded window and only `SENSOR_SQL_UNAVAILABLE`; `SENSOR_COMMIT_UNCERTAIN` never repeats (test). Sleep is clamped to the window deadline; maximum added delay 52 s fits the 1620 s replica timeout over the 1500 s window.
* Claims in the research note match the evidence: two captured stderr lines, one Succeeded run, probe JSON with `observed_at` 22:45:00Z. Unproven items (database fault cause, numeric exit code, older failures, deployment, three consecutive successes) are stated as unproven.
* Corrected the earlier note's "all 26 Failed" count in the new note rather than editing the old one.
* No secrets in evidence: the probe reads sign-in values at runtime; the screenshot masks addresses; the JSON holds synthetic data.
* Routed follow-up 1: build and deploy the image, then observe three windows. Follow-up 2: allow this client in the log workspace network rule to name the database fault.

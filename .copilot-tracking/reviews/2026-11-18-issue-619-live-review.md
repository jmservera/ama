---
title: Issue 619 live demo review
ms.date: 2026-11-18
---

Review executed once. Outcome: conformant for a docs-only, evidence-only change; no source touched.

* Claims in the note were checked against `employee_proof.json`, `employee_followup.json` and `resident_proof.json`; counts and labels match.
* Limits are stated: engineering evidence is not a screen-reader run, viewport sizes are not zoom, synthetic resident is not a real resident.
* Adverse evidence kept (429 limiter, selector corrections, 320 by 256 chat input below the fold).
* Routed follow-up: when a production build exists, run the person-run protocol (#1905 to #1908) and consider making the chat input visible without scrolling at 320 by 256.
* Open: hosted CI and independent exact-head review (not performed here).

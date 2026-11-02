---
title: "Plan: issue 466 chart text summaries (r5), 2026-11-02"
ms.date: 2026-11-02
---

* Scope: add a visible plain-language summary under each sensor chart and reuse it in the SVG `desc`; client-side only, derived from the resident's own already-filtered history. No new data, endpoint, AI, consent or approval path changes.
* Steps: (1) `sensorSummary` in demo.js and `.sensor-summary` style; (2) extend `checks/resident_sensors_browser_check.py`; (3) run focused checks; (4) focused gate; (5) PR with `Refs #466`.
* Critique (executed once, verdict Proceed): low risk, text is built with textContent (no injection); non-breaking space keeps value and unit together; no colour-only signal; wording avoids safety claims.
* Rejected: CO2 gauge (dataset change), AI-generated chart narration (cost and consent boundary).

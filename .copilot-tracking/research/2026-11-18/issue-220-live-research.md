---
title: Research for issue 220 live proof
ms.date: 2026-11-18
---

* Disposition: executed. Planning readiness: Ready.
* Only unticked criterion: "No retaliation, inferred refusal or delayed hazard response". Production-only criteria stay deferred (#1905-#1908).
* Findings: live read paths prove guarantees, assurance flags and forbidden-field refusal; every Entra staff write to the route returns 403 because `resident_decisions._operation` compares the full Entra principal with a roster row (reproduced offline, `evidence/2026-11-18/issue-220-live/local-repro.txt`). Fixing needs src change, FULL tier and an unauthorised redeploy, so it is routed as a follow-up.
* Offline tests pass: 5 core, 9 api.
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-220-live/`; note `docs/reference/research/issue-220-live-challenge-route-evidence-2026-11-18.md`.

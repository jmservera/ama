---
title: Issue 1288 live audit r12, research
ms.date: 2026-11-23
---

Task: re-audit unticked criteria 3 to 8 of #1288 for the synthetic desktop demo. Research disposition: executed (new live probe and focused tests); prior notes r2 to r11 are reused as context only.

Opening findings (to be confirmed below): r11 concluded that the model leg is blocked by a missing approved release record (OQ-017). Source delivered in #1331.

Planning Readiness: Ready (audit only; src change only if a code gap is found).

## Evidence (read-only, 07:08 to 07:20Z)

* Active revisions unchanged: `ca-cutover-test-demo-api--0000055` Running, `ca-resident-demo--0000027` RunningAtMaxScale.
* Probe `evidence/2026-11-23/issue-1288-live12/live_probe.py` (read-only, no assistant request called): role Retrofit Programme Manager; of 12 listed cases, 7 `ok` with 12 readings, 4 `consent-withheld`, 1 HTTP 503 on first call (ZF-2025-0148, not retried). Reading IDs `LIVE-<sensor>-<UTC>Z`, source "Outdoor weather. Not calibrated.", provenance `synthetic-weather-derived`.
* `/api/assistants`: all assistants refused, "approved, unexpired release record" missing, owner not appointed (OQ-017). Forecast `proactive` false, `call_allowance` 0. `rai-metrics` invocation/tokens/consumption 0 before and after. Simulation lane `unavailable`/`not-configured`.
* Screenshots: `live-sensor-panel.png`, `live-ai-tab.png`.
* Focused tests: see `focused_tests.txt`.

## Conclusion

Criteria 3 and 5 to 7 hold as local engineering evidence; 4 and 8 stay blocked by the missing release record, which the owner decisions do not authorise creating. Planning Readiness: Ready. No source change is justified.

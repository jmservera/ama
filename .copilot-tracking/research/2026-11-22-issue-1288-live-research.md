---
title: Issue 1288 live research
ms.date: 2026-11-22
---

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Main check: `git fetch origin main`; `HEAD..origin/main` is empty, so HEAD `3219004e90` is current main. Source delivery of #1331 stands; criteria 1, 2 and 9 are ticked, 3 to 8 are not.
* Prior audits r1 to r8 in `docs/reference/research/`; r8 is the latest and concluded criteria 4 and 8 stay blocked at release admission (OQ-017).
* Focused tests rerun at `3219004e90` from `src/api`: `tests.test_quality_sensor_grounding tests.test_quality_sensors_correlation tests.test_quality_sensors_c7`: 92 tests OK, 9 skipped, 111 s (`.copilot-tracking/evidence/2026-11-22/issue-1288-live9/focused_tests.txt`).
* Live probe (read-only, Playwright, signed in as Retrofit Programme Manager; credentials read at runtime): seven of twelve homes `ok`, 12 readings each, IDs `LIVE-<sensor>-<UTC>Z`; five `consent-withheld`. Home sensors panel screenshot taken at 23:32 UK time (5.45 degC, 93.46 %RH, "2 minutes ago", outdoor-derived, not calibrated, no retrofit comparison, explicit no-quality-record context).
* Assistants list: all five assistants, including `quality-evidence`, refuse with "approved, unexpired release record" missing; authority gaps OQ-017.
* New anomaly: another worker rolled revision `--0000054` at 23:14Z. `GET /api/assistants/forecast` returned 503 then 504 in this window (200 in r8); `/api/assistants`, `rai-metrics`, sensors and UI stay 200. `rai-metrics` now shows `invocation` 1, `persisted` 3, `tokens` 0, `consumption` 0, identical before and after the probe; no model consumption.
* No Azure resource created or changed; nothing to delete.

## Conclusion

Criteria 3, 5, 6, 7 proven as local engineering evidence; 6 also seen live. Criteria 4 and 8 unproven: the Quality model leg needs a human-approved release record that no named owner has supplied; writing one would fabricate authority and a mock outcome is excluded by the criterion. No source change; focused tier.

---
title: "Changes: issue 466 chart text summaries (r5), 2026-11-02"
ms.date: 2026-11-02
---

* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: `sensorSummary`, visible summary in each chart caption and in the SVG `desc`.
* `src/api/src/zava_forward/api/resident_demo/web/demo.css`: `.sensor-summary`.
* `src/api/checks/resident_sensors_browser_check.py`: three assertions for the summaries.
* `docs/reference/log.md`: one appended entry.
* Divergences: none.
* Validation: resident_sensors_browser_check all PASS (Chromium, loopback, generator output); resident_assistant_browser_check PASS; `unittest -k resident` in src/api: 204 tests OK (12 skipped); resident_demo_browser_check needs SQL, not run (no cloud fallback).

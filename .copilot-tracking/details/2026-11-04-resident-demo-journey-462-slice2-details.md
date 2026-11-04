---
title: Details for #462 slice 2
ms.date: 2026-11-04
---

* Phase 1 files: `src/api/src/zava_forward/api/resident_demo/web/index.html` (banner, lede id, sign-in intro), `demo.js` (lede switching, field-specific errors).
* Phase 2 files: `demo.js` (Intl en-GB Europe/London, chart margin 56, tick anchor 50), `demo.css` (axis text 1.25rem), sign-out failure copy.
* Phase 3 files: `src/api/tests/test_resident_demo_api.py` (three static tests), `src/api/checks/resident_sensors_browser_check.py` (UK time assertion).
* Success: existing 42 resident API tests plus three new pass; the sensor browser check passes at 320, 390 and 1280px with no overflow.

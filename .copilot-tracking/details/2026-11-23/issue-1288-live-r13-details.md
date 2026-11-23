---
title: Details r13 for issue 1288
date: 2026-11-23
---

* P1 limits reuse `PLAUSIBLE_HUMIDITY_PCT` and `PLAUSIBLE_TEMPERATURE_C`; a row is implausible when a value is missing, not finite or outside the limits. Keys are only added when rows are implausible, so existing snapshots, digests and tests are unchanged.
* P2 trigger adds `not sensors.get("implausible_readings")`. Status order: rejected, reviewed, conflicting-readings, implausible-readings, not-current, manual-proposal, uncited, review-suggested. Effect text states the reading is outside the possible range and routes to the ordinary quality check; it never approves work.
* P3 FLAG_TITLES gets one entry; the notice renders as a status paragraph like the conflict one.
* Known limit: only implausibility present at capture time is handled; a later bad arrival after capture is not downgraded (the UI health badge still shows it).

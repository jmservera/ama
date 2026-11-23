# Issue 1288 r13 plan details

Phase 1: in src/api/src/zava_forward/api/server.py add a module-level helper logging `sensor-unavailable GET <path> exc=<ClassName> at=<file:line:func>` at WARNING via `logging.getLogger(__name__)`. Call it inside `except Exception as exc:` for `/sensors` and `/sensor-drafts`.

Phase 2: test patches `self.service.sensors` to raise RuntimeError("secret-host") and asserts 503, unchanged body, `assertLogs("zava_forward.api.server")` contains `RuntimeError` and not `secret-host`.
---
title: Details r13 for issue 1288
date: 2026-11-23
---

* P1 limits reuse `PLAUSIBLE_HUMIDITY_PCT` and `PLAUSIBLE_TEMPERATURE_C`; a row is implausible when a value is missing, not finite or outside the limits. Keys are only added when rows are implausible, so existing snapshots, digests and tests are unchanged.
* P2 trigger adds `not sensors.get("implausible_readings")`. Status order: rejected, reviewed, conflicting-readings, implausible-readings, not-current, manual-proposal, uncited, review-suggested. Effect text states the reading is outside the possible range and routes to the ordinary quality check; it never approves work.
* P3 FLAG_TITLES gets one entry; the notice renders as a status paragraph like the conflict one.
* Known limit: only implausibility present at capture time is handled; a later bad arrival after capture is not downgraded (the UI health badge still shows it).

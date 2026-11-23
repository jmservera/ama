---
title: Plan r13 for issue 1288
date: 2026-11-23
---

Refs #1288. Tier FULL (src change); targeted tests only, no rpi-checks --all, no push.

* [ ] P1 sensor_view: `implausible_rows`, `implausible_readings` and `implausible_notice` in `capture_source`.
* [ ] P2 assistants: no proactive request while captured readings are implausible; `review_flag` status `implausible-readings` (not autonomous, human route).
* [ ] P3 assistants.js: title for the new status and notice paragraph.
* [ ] P4 test in test_quality_sensor_grounding.py (written first, failing before the change).
* [ ] P5 targeted tests, ruff and mypy; changes record with per-criterion table; research note r13; commit.

Details: [details](../../details/2026-11-23/issue-1288-live-r13-details.md). Critique: [critique](../../critique/2026-11-23/issue-1288-live-r13-critique.md).

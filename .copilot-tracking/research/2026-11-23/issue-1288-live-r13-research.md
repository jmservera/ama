---
title: Research r13 for issue 1288 (implausible sensor readings reach the Quality model)
date: 2026-11-23
---

Disposition: executed. Tier FULL only if src changes (it will); no rpi-checks --all, no push. Planning Readiness: Ready.

## Evidence

* Prior audits r2..r12 (docs/reference/research/issue-1288-live-r*): criteria 4 and 8 blocked only by a missing approved release record (OQ-017); that is owner-only and is not bypassed.
* Code gap found in this round: `sensor_view.reading_health` flags fault or out-of-range latest readings in the employee UI only. `capture_source` (the snapshot the model receives) carries no such marker, and `review_flag` / the proactive trigger treat only `conflicting_readings` as blocking. An impossible reading (for example 250 %RH) can therefore be sent to the model and cited in an autonomous L4 flag while the UI says "do not rely on it". This contradicts criterion 3 (identical evidence) and criterion 6 (rejected or conflicting readings give an explicit insufficient state, no silent normal).
* Live: read-only probe of the demo only; no model consumption possible without a release.

## Plan target

Add an `implausible_readings` marker and notice to the captured sensor source, block the autonomous flag and proactive trigger for it (status `implausible-readings`, human route), label it in the UI, and test it locally.

# Research: issue 2118 live Hub to SQL to map walkthrough (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

* Issue #2118 has one unticked criterion: a recorded live Hub to SQL to UI map walkthrough once live transport is active.
* Live transport is active: simulator and receiver jobs Succeeded, hub ingress equals egress (2095), route enabled.
* Map shows a fresh reading 79 s old for ZF-2025-0030; sensors route fresh for two homes; consent-withheld for a third.
* Main (`dbf4e45fa7`) map sensor tests pass (16); live revisions 0000054 / 0000026 behave as tested. No code gap.
* Unproven: per message SQL trace, reading ids this run, resident live view (consent declined).
* Evidence: `.copilot-tracking/evidence/2026-11-23/issue-2118-live/`; note `docs/reference/research/issue-2118-live-iot-map-walkthrough-2026-11-23.md`.

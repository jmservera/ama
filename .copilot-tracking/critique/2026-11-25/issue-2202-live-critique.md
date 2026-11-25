---
title: Issue 2202 live critique 2026-11-25
ms.date: 2026-11-25
---

Critique executed once. Verdict: proceed with one compatible adjustment.

* Read-only claim holds (no write statements in `sensor_view` or `sensor_map`; `authorize` only selects). Applied directly.
* Isolation drops from SERIALIZABLE to autocommit read committed; acceptable for a bounded display read, and the forecast already does it. Applied directly.
* Cannot be proven live: deploying a new image is a production change and the registry refuses this identity. Record as unproven, not as fixed live.
* Do not widen to other GETs (proposals, chat threads write). Applied.

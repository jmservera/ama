---
title: Issue 2008 review, 2026-11-22
ms.date: 2026-11-22
---

Review executed once on the final change. Outcome: conformant for scope (local, not deployed).

* Dependency rule kept (api imports core only); no new dependency; image unchanged.
* Guards reused unchanged (size, entity, formula, content scan); preview only, source hash unchanged.
* Web guidelines read against `app.js`: labelled input, captioned tables, text status words, empty states handled. A 200-row list is not virtualised (desktop demo, capped).
* Open, routed to follow-up: deploy and rerun live (criterion 3); full-tier gate and hosted CI by the coordinator.
* Core suite (4159 tests): one real failure from this change (stale link in the Fabric note), fixed; remaining 57 failures/errors are environment-related (missing Azure IoT SDK, package path) in untouched files, unverified against `main`.

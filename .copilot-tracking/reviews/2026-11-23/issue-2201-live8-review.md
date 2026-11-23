---
title: Issue 2201 live8 review
ms.date: 2026-11-23
---

Review executed once. Outcome: conformant with routed open work.

* The diff is three files; the stable `IOT_CALLBACK_FAILED` code is unchanged and only the class name is exposed, never a message.
* The new test would fail without the change (attribute absent) and checks the marker string is not stored.
* Open, routed to a later owner-authorised task: build and deploy the image to `job-live-receiver`, then read `callback_error_type` from the next failure; exit code still absent from execution records.
* Not observed: hosted CI (not pushed); full local gate left to the coordinator.

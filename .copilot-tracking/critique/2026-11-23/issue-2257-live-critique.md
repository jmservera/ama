---
title: Issue 2257 live critique
ms.date: 2026-11-23
---

Executed once. Verdict: proceed.

* Rejected: client retry of JSON 500 (contradicts the pinned test and a confirmed design that app errors are shown, not hidden).
* Accepted: degrade the optional sensor overlay to the existing `unavailable` state when its transaction fails, log class only, so the map stays usable. Claim limited: cause of the live ProgrammingError is unproven.
* Risk: masking. Mitigated by a class-only warning log and the visible "Sensor readings could not be read" label.
* No deploy: live proof of the hardening is not possible without changing the estate; marked unproven.

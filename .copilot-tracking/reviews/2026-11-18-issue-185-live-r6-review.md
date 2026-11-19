---
title: Issue 185 live r6 review
ms.date: 2026-11-18
---

Executed once by the implementing worker (self-review; independent exact-head review and hosted CI remain required). Outcome: conformant for scope, with routed follow-ups.

* Diff read in full: SAS branch sends no key and discards the response; X.509 path byte-identical in behaviour (39 baseline tests pass unchanged). Thumbprint uniqueness check correctly ignores SAS items.
* Tests would fail without the change (`SasEnrollment` absent). Key-leak test covers return, logging, repr, error and traceback.
* Honest limits: no live run of the new code; durable storage unproven; FULL gate not run; the process deviations in the changes record are retained.
* No secrets in the diff; the fake key is a labelled sentinel.

Routed follow-ups: (1) coordinator FULL-tier gate and independent review; (2) live adapter run once an image carries `azure-iot-hub` (needs owner approval to push to the registry); (3) durable key storage design.

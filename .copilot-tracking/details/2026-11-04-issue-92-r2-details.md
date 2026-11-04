---
title: Issue 92 r2 details
ms.date: 2026-11-04
---

* procurement.py: `contract_event` joins the actions that skip contract-authority checks (it cannot let or renew); new method uses `_proc_operation` so audit is atomic with rollback on failure.
* Tests in test_consultation_controls.py: held and audited for let and renew with supplied "complete"; package data unchanged; bad event and non-manager rejected with no writes.
* Human approval boundary kept: a supplied record cannot release the hold. Manual path: Legal and the contract owner confirm outside this service. AI is not involved.

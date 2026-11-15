---
title: Runtime to Bicep signal parity review
ms.date: 2026-11-14
---

Review executed once. Outcome: conformant for the stated scope; no material findings open.

* Markers, reason codes and platform metrics verified against source constants.
* Limits: job failure, poison-queue and IoT alerts rely on platform signals that cannot be verified from source; they stay candidates pending deployed-workspace verification. `import-jobs-poison` has no producer.
* Follow-ups: (1) verify StorageQueueLogs and job metric dimensions in a deployed workspace; (2) human review and hosted CI on the exact head.
* No `Closes` keyword; #146 stays open (`Refs #146`).

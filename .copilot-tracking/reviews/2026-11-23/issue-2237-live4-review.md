---
title: Review issue 2237 live4
ms.date: 2026-11-23
---

Review executed once; outcome conformant. Boundary: doc_controls.py diff and the new test. Fail-closed check: rows with unreadable triggers are listed, never deleted; `approve_retention_deletion` still raises on them (verified by reading, not by test). Follow-up: deploy and re-prove live; make approval give a clear 4xx for unreadable triggers.

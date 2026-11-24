---
title: Issue 2244 live run 7 details
ms.date: 2026-11-24
---

Step 1 uses `az containerapp show`, `revision list`, `replica list`, `logs show` and `exec md5sum`, plus `curl /healthz`. Step 2 states C4 and C5 unproven with reasons. No credential file is read.

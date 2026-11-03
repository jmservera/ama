---
title: "Issue 163 age-based retention details (2026-11-03)"
ms.date: 2026-11-03
---
* `chatthreads.py`: both `purge_threads` implementations compare `created_at` with the cutoff. Messages are removed with their thread. No schema change; `created_at` already exists on both stores.
* Boundary: no scheduler runs the purge (infrastructure, separate review). No period is applied until CHAT_RETENTION_REF and CHAT_RETENTION_DAYS are recorded.
* Human approval and resident consent boundaries are unchanged; the demo holds constructed data only.

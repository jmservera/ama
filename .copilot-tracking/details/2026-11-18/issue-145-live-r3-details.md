---
title: Issue 145 live run 3 details
ms.date: 2026-11-18
---

* Cost: one S0 database and one 0.5 vCPU job for about an hour; far below the USD 700 cap.
* Restore name `retrofit-pitr145r3`; job name `job-145r3-probe`. Both throwaway.
* Evidence is hashes, counts, timestamps and status only.
* Tier: FOCUSED (no src change); Azure-tier evidence, not SQLite emulation.

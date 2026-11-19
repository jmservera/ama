---
title: Issue 115 plan details
ms.date: 2026-11-19
---

Job name capped at 31 characters, so `job-cutover-test-ledger-verify-s` (still matches the alert query prefix). Cron `*/5 * * * *`. Exported the existing job YAML, set trigger Schedule, removed `--publish`. Temp files lived in /tmp and were removed.

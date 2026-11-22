---
title: Issue 2201 live6 critique
ms.date: 2026-11-22
---

Verdict: approve with direct dispositions. Executed once on the final candidate plan.

* Risk: claiming the callback exception is captured when it did not recur. Disposition: note states it is unproven and routes a logging change.
* Risk: counting the 15:30 run before it ends. Disposition: excluded; streak uses 14:00, 14:30, 15:00.
* Risk: Log Analytics ingestion lag hides the 15:00 console line. Disposition: judged by execution status plus a failure-line query, lag stated.
* Risk: credential exposure in the probe. Disposition: probe reuses the runtime-login helper and prints no secrets; emails masked.
* Scope: no source edit, so focused tier; no rpi-checks --all.

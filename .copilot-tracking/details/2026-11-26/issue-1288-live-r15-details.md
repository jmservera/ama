---
title: Issue 1288 live r15 details
description: Step details and stop rules
ms.date: 2026-11-26
---

* Stop rules: call allowance never above 10 and tokens 200000; stop and revert if any call fails with an unexpected cost or any non-demo case is touched; never print credentials; no push.
* Revert is `az containerapp update` removing the five ZF_ASSIST_* variables set here; record revisions before and after.
* Evidence: live_walkthrough.py (read-only plus Playwright UI), outputs scrubbed of emails.
* Criterion 8 counts only if the flag cites the same `LIVE-` reading IDs shown by the UI, is attributed to the model and is shown unapproved.

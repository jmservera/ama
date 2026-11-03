---
title: Issue 531 derive retry counts details
ms.date: 2026-11-03
---

* Add `script_attempts()` and `SCRIPT_ATTEMPTS`: parse the `SCRIPT_RETRY_DELAYS` array in `app.js`, return 1 + its length, assert if the declaration is missing.
* Replace the literal 4 in the required-script request-count assertion, the terminal-failure test, the expected request count and the helper bootstrap loop (`range(1, SCRIPT_ATTEMPTS + 1)`).
* Leave the 1-request and 2-request expectations unchanged.

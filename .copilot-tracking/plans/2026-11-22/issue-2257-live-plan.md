---
title: Issue 2257 plan
ms.date: 2026-11-22
---

* Phase 1: edit `fetchReadRetrying` to retry transport failures (`TypeError`) up to 2 times, respecting the abort signal, with the existing status message wording replaced by a transport-specific plain-language one.
* Phase 2: amend `test_first_load_reads_retry_a_cold_start_gateway_failure` to cover recovery, bounded retries and abort.
* Phase 3: prove on the live demo by serving the patched `app.js` through Playwright route interception and aborting the first `/api/map` request; run `test_workspace_scripts.py`, `test_accessibility_baseline.py`, `test_content_standard.py`.
* Tier: FULL classification applies because source changes; the complete gate is run by the coordinator, not here.

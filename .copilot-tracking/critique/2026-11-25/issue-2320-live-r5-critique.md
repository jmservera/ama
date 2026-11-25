---
title: Issue 2320 live r5 critique
ms.date: 2026-11-25
---

Critique executed once on the final candidate plan. Verdict: proceed with direct dispositions.

* Risk: swallowing every error hides faults. Applied: catch only `is_write_lock_busy`; other errors still raise.
* Risk: a fallback that claims a stale figure is current. Applied: the answer names itself as not recorded, with a plain-language reason; a stale cached briefing for the same user and case list is reused only with that reason.
* Risk: skipped audit weakens the ledger. Disposition: no AI output is shown in the fallback (template text only, source `template`), so no AI run goes unrecorded; the briefing is read-only data already visible to the user.
* Risk: test on SQLite cannot reproduce SQL Server lock. Applied: inject the driver error shape used by `test_error_logging.py` into `audit`.

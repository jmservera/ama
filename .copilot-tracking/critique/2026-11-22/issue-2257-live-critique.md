---
title: Issue 2257 critique
ms.date: 2026-11-22
---

Critique executed once on the final candidate. Verdict: proceed.

* Risk: retrying hides real outages. Mitigation: bounded to 2 retries with 400 ms and 1200 ms delays, only for GET reads through `fetchReadRetrying`, plain-language status shown, final failure still surfaces the original error.
* Risk: retrying POST duplicates changes. Mitigation: mutations use `fetch` directly, not touched.
* Risk: an aborted navigation retries. Mitigation: `signal.aborted` re-throws immediately.
* Conflicts with confirmed decisions: none. The existing "network failure never retried" test encoded a cold-start-only scope; it is amended deliberately.
* Alternative rejected: raising infra min replicas to 1; production changes are not authorised for this task, and it is recorded as a follow-up.

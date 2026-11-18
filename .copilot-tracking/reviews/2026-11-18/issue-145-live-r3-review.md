---
title: Issue 145 live run 3 review
ms.date: 2026-11-18
---

Executed once. Outcome: conformant for the documentation and evidence scope.

* Links in the note resolve to existing files; index and log updated.
* Raw file contains no server, subscription or identity names (grep 0); hashes are public audit-chain values.
* Claims match raw output: 1694/1770 entries, head match at entry 1694, native verify denied, 64 ledger tables.
* Open and routed: native ledger verification permission, seeded resurrection test and re-apply mechanism (needs `src` change, full tier), #121 retention decision (production).
* No src change; mypy, ruff and unit tests not applicable.

---
title: Issue 144 permit SQL E5 correction authored review
description: Authored review of the E5 correction outcome
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Outcome

Review executed once. Outcome: both Medium comments and the case 3 receipt gap are corrected and statically and SQLite-validated; SQL qualification remains NOT run. This is not publication or whole-#144 acceptance.

## Observed

* Old behaviour reproduced, then fixed, by HARNESS-ONLY probes (16 of 16 on final bytes).
* Ruff, format and strict mypy pass; 15 SQLite selectors OK; 7 skipped with the exact reason; discovery 7.

## Not observed

* Real SQL, DMV and clock witnesses, N1/N2 controls. The probe does not prove lock behaviour.
* The manifest binds exact paths, ownership and permissions but is launcher-written: the launcher must create it, and verify it, before imports. No launcher exists yet.

## Routed follow-up

Same independent review of the final code, then Root decides SQL admission. E5 is spent; any further correction needs new authority.

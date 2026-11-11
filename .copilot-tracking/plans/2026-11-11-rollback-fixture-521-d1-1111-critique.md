---
title: Issue 521 rollback-fixture diagnostic D1 critique
ms.date: 2026-11-11
task_id: 521-rollback-d1-1111
---

One independent critique (rubber-duck agent, model claude-sonnet-5.5) of the final candidate, executed once. Verdict: no significant findings.

* Insert at `AUTHORITY_END + 1s`: `valid_to` is `DATETIME2(0)`; after `NOCHECK` only that constraint could block it; the provenance check passes; no triggers. No findings.
* Migration failure: the re-added `WITH CHECK` constraint (`valid_to <= '2028-01-01T00:00:00'`) rejects the row; `XACT_ABORT ON` plus `CATCH` rolls back and re-throws, so `@@TRANCOUNT` is 0. No findings.
* Cleanup: `DELETE` then re-applied migration succeeds. No findings.
* Minor 1: RED must be shown failing for the right reason (`assertRaises` "not raised" on the unchanged fixture), not a container or driver error. Disposition: applied; the RED log is retained and its failure text recorded.
* Minor 2: GREEN could pass for an unrelated error. Disposition: applied as evidence only; a separate disposable probe records the actual `mssql_python.Error` text and confirms a check-constraint conflict. No assertion change.
* Minor 3: fractional-second `maximum_expiry_utc` would truncate under `strftime`. Disposition: noted, benign today (value is whole seconds), not fixed.
* Minor 4: keep the container command and password out of the README and changes record. Disposition: applied; the README lists the route without the secret.

No direct conflict with a confirmed decision. No second critique.

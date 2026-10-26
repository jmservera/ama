---
title: Resident showcase 462 execution-readiness local stage independent review
ms.date: 2026-10-26
---

Original independent read-only review (code-review agent), run once at about 13:30Z against the
uncommitted local stage. Verbatim result:

One low-severity bug found; nothing in the guard or Bicep is exploitable. The reviewer did not run
the tests (python not on its PATH); `bicep build infra/resident-demo.bicep` compiled cleanly.

Issue: uppercase subscription GUID makes the what-if guard refuse every change.
File: infra/scripts/resident_demo_deploy.py, `allowed_ids()` / `check_changes()`. Severity Low (fails
closed, not a bypass). `allowed_ids()` uses `subscription` unchanged while `check_changes()` lowercases
the what-if resource id; the GUID regex accepts uppercase hex, so a legitimate run with an uppercase
`--subscription` refuses. Tests use a digit-only GUID. Suggested fix: lowercase the subscription when
building the root and add an uppercase-GUID test.

Checked, no bug found: Delete is rejected; casing is handled except the GUID; role-assignment scope
parsing is exact for the registry and the two secrets; Bicep `vaultUri` trailing slash, role scopes,
secret refs and guard are correct; `ZF_SQL_*` and `ZF_DEMO_*` match no forbidden prefix; all expiry
literals are consistent at 2026-11-01T00:00:00Z and later expiry is rejected by the script, service
and session lifetime.

## Disposition (appended by the implementer after the review, not part of the verdict)

* Finding accepted and fixed after the review (lowercase root plus an uppercase-GUID test). The fix
  was not independently re-reviewed; this stage has one review only, by design.
* Verdict as reported: no blocking or exploitable findings; one Low, fail-closed, now fixed.

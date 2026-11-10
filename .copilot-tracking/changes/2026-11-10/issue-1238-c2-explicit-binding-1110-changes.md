<!-- markdownlint-disable-file -->
# Changes: issue 1238 C2 explicit approval-role binding (1110)

Written 2026-11-10 after implementation. Plan:
[plan](../../plans/2026-11-10/issue-1238-c2-explicit-binding-1110-plan.md),
[critique](../../plans/2026-11-10/issue-1238-c2-explicit-binding-1110-critique.md).
Counter: C2 of 5 spent by this correction; three remain. No reset.

## Transitions (actual)

* Research, plan, details, critique recorded 00:34Z to 00:36Z (file birth times).
* Ordinary merge of main ddeebd0 (no conflict; ai.py and one ai test only).
* Red run 00:37:24Z: `-k supersede`, 45 selected: 27 errors (the new
  `SupersessionBinding` did not exist), 16 skipped (MSSQL class), 2 pass.
* Implementation 00:38Z. First green run had 2 errors (the in-flight test had
  no binding fixture); fixed in the test, then 45 OK.
* A mistaken `git stash` during lint was popped immediately; no content lost
  (status verified).

## Changes

* `resident_decisions.py`: new immutable `SupersessionBinding` (id, control
  owner and reviewer identities, digest); `_supersession_binding` (fail closed,
  captured in the SQL validation context and refused if different on replay);
  `_authorization_holds` (stored approval counts only under the current
  digest, for the bound person, with its audit entry); handler rewritten to
  use the binding instead of the request's service and redress owners;
  `_SUPERSEDE_ROLES` removed.
* `test_resident_decisions.py`: fixture `synthetic_binding`; existing supersede
  tests bound explicitly; reassignment test replaced; new cases for default
  denial plus forged rows, no binding from staff/requests/body, forged stored
  approval (no stamp, wrong stamp, correct digest without audit), changed
  binding, SQL replay swap, binding validation and immutability.
* `README.md` (Core): boundary text.

Not changed: Store, sqlstore, procurement, server, app.js, navigation, roles,
resident_demo, Quality files, schema. No binding or approval is populated.

## Validation (scratch: external, owner file OWNER.txt)

* Module `test_resident_decisions` JSON and SQLite: 362 tests OK, 129 skipped
  (MSSQL classes, not enabled in this run).
* Related modules: resident_preview, journey_store, handoff_lifecycle,
  finance_signoffs OK; priority_order OK (65 skipped, MSSQL).
* MSSQL selected (`-k supersede -k late_outcome -k forward`), one nonqueued
  heavy-lock admission (lock free, no holder), disposable localhost container:
  105 tests OK, 1 skipped (the SQL-replay test on the JSON class, by design);
  the MSSQL class ran all 35 selected including the replay swap.
* `ruff check` (Core and API) pass; `ruff format --check` on the test file
  pass; the source file was unformatted at base and left unformatted.
* Strict `mypy`: Core project 283 files pass; API project 211 files pass
  (after installing `src/agents` and `src/api[dev]` editable into the owned
  venv; the first API run failed on missing declared dependencies).
* Not run: whole MSSQL class, resident API module, browser, hosted CI.

## Limits

* Binding content, activation and rotation remain unprovided human gates.
* Restoring an earlier binding revalidates approvals that carry its digest.
* Audit cross-check does not re-verify the chain per call.
* The evidence is human-vouched; synthetic bindings are not actual approval.
* RV-1 (retention of authorizer identities) is unchanged.
